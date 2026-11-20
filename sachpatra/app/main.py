"""FastAPI application entrypoint for SachPatra.
Provides /api/analyze, /api/health, /api/rules, and /api/stats.
Strict privacy: Zero request body logging. In-memory per-IP rate limiting.
"""

import time
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

from app.engine import analyze_text
from app.i18n import RULES_METADATA
from app.rules import RULES
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.stats import get_stats, init_db, record_stat


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    init_db()
    yield


app = FastAPI(
    title="SachPatra API",
    description="Citizen screening engine for Digital Arrest and cyber extortion scams",
    version="1.0.0",
    lifespan=lifespan
)

# CORS: closed by default (no wildcards or open origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# In-memory sliding window rate limiter: 20 requests/minute per client IP
RATE_LIMIT_WINDOW = 60.0
RATE_LIMIT_MAX_REQUESTS = 20
_ip_request_timestamps: Dict[str, List[float]] = defaultdict(list)


def rate_limiter(request: Request) -> None:
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    valid_window_start = now - RATE_LIMIT_WINDOW

    timestamps = [t for t in _ip_request_timestamps[client_ip] if t > valid_window_start]
    if len(timestamps) >= RATE_LIMIT_MAX_REQUESTS:
        _ip_request_timestamps[client_ip] = timestamps
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 20 requests per minute."
        )

    timestamps.append(now)
    _ip_request_timestamps[client_ip] = timestamps


def reset_rate_limits() -> None:
    """Helper for testing to reset rate limit counters."""
    _ip_request_timestamps.clear()


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/rules")
def get_rules() -> Dict[str, Any]:
    """Public transparency endpoint returning deterministic rules, categories, weights,
    explanations, and authoritative reference sources.
    """
    rule_list = []
    for r in RULES:
        meta = RULES_METADATA.get(r.id, {})
        rule_list.append({
            "id": r.id,
            "category": r.category,
            "weight": r.weight,
            "hard": r.hard,
            "title": meta.get("title", {}),
            "why": meta.get("why", {}),
            "source_url": meta.get("source_url", "")
        })
    return {"rules": rule_list, "total_rules": len(rule_list)}


@app.get("/api/stats")
def stats() -> Dict[str, Any]:
    """Public aggregated statistics endpoint (counters only, zero PII)."""
    return get_stats()


@app.post("/api/analyze", response_model=AnalyzeResponse, dependencies=[Depends(rate_limiter)])
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Screen submitted text for digital arrest and cyber extortion patterns.
    Privacy note: Request text is evaluated deterministically in-memory and discarded.
    Never logged, never written to disk.
    """
    response = analyze_text(payload)

    # Record anonymous counters only
    fired_ids = [r.id for r in response.reasons]
    record_stat(
        verdict=response.verdict,
        rule_ids=fired_ids,
        language=response.language
    )

    return response
