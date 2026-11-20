"""FastAPI application entrypoint for SachPatra.
Provides /api/analyze, /api/analyze-image, /api/health, /api/rules, and /api/stats.
Strict privacy: In-memory evaluation only, zero disk writes for uploaded media, zero request logging.
"""

import io
import os
import time
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Literal, Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

from app.engine import analyze_text
from app.gemini import extract_from_image
from app.i18n import IMAGE_OFFLINE_MESSAGE, RULES_METADATA
from app.rules import RULES
from app.schemas import AnalyzeRequest, AnalyzeResponse, ExtractedImageContent
from app.stats import get_stats, init_db, record_stat

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB limit


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


def validate_image_magic_bytes(content: bytes, filename: str) -> str:
    """Validate image magic bytes and verify file extension matches genuine image formats.
    Returns normalized MIME type or raises HTTPException.
    """
    ext = os.path.splitext(filename or "")[1].lower()
    allowed_exts = {".jpg", ".jpeg", ".png", ".webp"}
    if ext and ext not in allowed_exts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image extension. Only JPG, PNG, and WebP are accepted."
        )

    if len(content) < 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File too small or corrupted image."
        )

    # JPEG: starts with FF D8 FF
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"

    # PNG: starts with 89 50 4E 47 0D 0A 1A 0A
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"

    # WebP: starts with RIFF and has WEBP at bytes 8-12
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid image content. Magic bytes do not match JPEG, PNG, or WebP format."
    )


def strip_exif_in_memory(content: bytes, mime_type: str) -> bytes:
    """Strip EXIF metadata completely in memory; never writes to disk."""
    try:
        with Image.open(io.BytesIO(content)) as img:
            out = io.BytesIO()
            fmt = "PNG" if "png" in mime_type.lower() else ("WEBP" if "webp" in mime_type.lower() else "JPEG")
            img.save(out, format=fmt)
            return out.getvalue()
    except Exception:
        return content


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse)
def serve_index() -> FileResponse:
    index_file = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_file):
        raise HTTPException(status_code=404, detail="Index file not found")
    return FileResponse(index_file)


@app.get("/app.css", response_class=FileResponse)
def serve_css() -> FileResponse:
    css_file = os.path.join(STATIC_DIR, "app.css")
    if not os.path.exists(css_file):
        raise HTTPException(status_code=404, detail="CSS file not found")
    return FileResponse(css_file, media_type="text/css")


@app.get("/app.js", response_class=FileResponse)
def serve_js() -> FileResponse:
    js_file = os.path.join(STATIC_DIR, "app.js")
    if not os.path.exists(js_file):
        raise HTTPException(status_code=404, detail="JS file not found")
    return FileResponse(js_file, media_type="application/javascript")


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
    response = analyze_text(payload, engine_tag="rules")

    # Record anonymous counters only
    fired_ids = [r.id for r in response.reasons]
    record_stat(
        verdict=response.verdict,
        rule_ids=fired_ids,
        language=response.language
    )

    return response


@app.post("/api/analyze-image", response_model=AnalyzeResponse, dependencies=[Depends(rate_limiter)])
async def analyze_image(
    file: UploadFile = File(...),
    language: Literal["en", "hi", "pa", "auto"] = Form("auto"),
    channel: Literal["message", "call", "document"] = Form("document")
) -> AnalyzeResponse:
    """Screen an uploaded notice or screenshot (JPG/PNG/WebP, max 5MB).
    Validates magic bytes, strips EXIF in memory, extracts structured data via Gemini,
    and runs the deterministic verdict rule engine.
    Privacy guarantee: In-memory processing only; zero disk writes, zero content logging.
    """
    content = await file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File size exceeds maximum allowed limit of 5MB."
        )

    mime_type = validate_image_magic_bytes(content, file.filename or "")
    clean_bytes = strip_exif_in_memory(content, mime_type)

    # Multimodal transcription via Gemini
    extracted_data = extract_from_image(clean_bytes, mime_type)
    if extracted_data is None:
        target_lang = language if language in IMAGE_OFFLINE_MESSAGE else "en"
        msg = IMAGE_OFFLINE_MESSAGE.get(target_lang, IMAGE_OFFLINE_MESSAGE["en"])
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg
        )

    extracted_model = ExtractedImageContent.model_validate(extracted_data)

    # Combine extracted text + links + seal signals for deterministic rule evaluation
    text_components = [extracted_model.text]
    if extracted_model.links:
        text_components.append("\n" + "\n".join(extracted_model.links))
    if extracted_model.has_seal_or_signature:
        text_components.append("\nOfficial seal and arrest warrant copy attached.")

    combined_text = "\n".join(text_components).strip()
    if not combined_text:
        combined_text = "Notice document with no legible text."

    request_obj = AnalyzeRequest(
        text=combined_text[:6000],
        language=language,
        channel=channel
    )

    # Run deterministic screening
    response = analyze_text(request_obj, engine_tag="rules+gemini")
    response.extracted = extracted_model
    response.engine = "rules+gemini"

    # Record anonymous aggregate stats
    fired_ids = [r.id for r in response.reasons]
    record_stat(
        verdict=response.verdict,
        rule_ids=fired_ids,
        language=response.language
    )

    return response
