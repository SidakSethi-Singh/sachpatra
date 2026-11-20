"""Optional multimodal and plain-language explanation layer powered by Gemini.
Strictly decoupled from deterministic verdict logic.
8s timeout, 1 retry, zero content logging, silent fallback on any exception.
"""

import concurrent.futures
import json
import os
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from app.schemas import Reason

TIMEOUT_SECONDS = 8.0
MAX_RETRIES = 1


class ImageExtractionResult(BaseModel):
    text: str = Field(default="", description="Faithful full transcription of all visible text in Hindi, Punjabi, or English")
    claimed_agency: str = Field(default="", description="Name of claimed agency or police department if present")
    sender: str = Field(default="", description="Sender name, designation, phone, or email if present")
    links: List[str] = Field(default_factory=list, description="Any URLs, web domains, or QR code links found")
    amounts: List[str] = Field(default_factory=list, description="Any financial amounts mentioned")
    doc_type: str = Field(default="", description="Document classification (e.g. Notice, Warrant, Court Order, Chat)")
    has_seal_or_signature: bool = Field(default=False, description="Whether an official seal, stamp, or signature is visible")


def get_gemini_client() -> Optional[genai.Client]:
    """Retrieve Gemini client if API key is present; returns None immediately otherwise."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


def get_model_name() -> str:
    """Retrieve model name from env or default to a flash model."""
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def extract_from_image(image_bytes: bytes, mime_type: str) -> Optional[Dict[str, Any]]:
    """Extract and transcribe text, claimed agency, links, amounts, and visual seals from image.
    Uses response_mime_type application/json with strict schema.
    Enforces 8s timeout and 1 retry. Returns None on any failure.
    Zero content logging.
    """
    client = get_gemini_client()
    if client is None:
        return None

    def _call() -> Optional[Dict[str, Any]]:
        model_name = get_model_name()
        prompt = (
            "You are an expert document analyst for public cyber safety. "
            "Faithfully transcribe all text visible in this document or chat screenshot in its native script "
            "(Hindi, Punjabi, or English). Identify any claimed government agencies (CBI, ED, Police, TRAI, etc.), "
            "sender info, web links, financial amounts demanded, document type, and whether official-looking "
            "stamps, seals, or signatures appear. Return strictly formatted JSON matching the requested schema."
        )
        contents = [
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt
        ]
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ImageExtractionResult,
            temperature=0.0
        )
        resp = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config
        )
        if not resp or not resp.text:
            return None
        data = json.loads(resp.text)
        validated = ImageExtractionResult.model_validate(data)
        return validated.model_dump()

    for attempt in range(MAX_RETRIES + 1):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_call)
                res = future.result(timeout=TIMEOUT_SECONDS)
                if res is not None:
                    return res
        except Exception:
            if attempt == MAX_RETRIES:
                return None
    return None


def simplify(reasons: List[Reason], language: str) -> Optional[str]:
    """Generate a single short, plain-language paragraph (max 60 words) explaining WHY,
    specifically tailored for an elderly or non-technical reader.
    Prompt strictly forbids altering the verdict or inventing facts.
    Returns None on failure/timeout.
    """
    client = get_gemini_client()
    if client is None or not reasons:
        return None

    lang_name = {"hi": "Hindi", "pa": "Punjabi"}.get(language, "English")

    def _call() -> Optional[str]:
        model_name = get_model_name()
        reasons_summary = "\n".join([f"- {r.title}: {r.why} (Matched: {r.snippet})" for r in reasons])
        prompt = (
            f"You are a kind civic assistant explaining a suspicious message to an elderly citizen in {lang_name}.\n"
            f"Here are the specific red flags detected:\n{reasons_summary}\n\n"
            f"Write exactly ONE short, simple, reassuring paragraph (STRICTLY MAXIMUM 60 WORDS) explaining WHY this message is unsafe.\n"
            f"CRITICAL MANDATES:\n"
            f"1. You MUST NOT change, contradict, or soften the screening verdict.\n"
            f"2. You MUST NOT invent any new facts, names, cases, or numbers not present in the red flags.\n"
            f"3. Use warm, simple, everyday words that an elderly grandparent would easily understand.\n"
            f"4. Remind them gently to disconnect and call 1930 if pressured.\n"
            f"5. Answer strictly in {lang_name}."
        )
        config = types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=150
        )
        resp = client.models.generate_content(
            model=model_name,
            contents=[prompt],
            config=config
        )
        if not resp or not resp.text:
            return None
        text = resp.text.strip()
        words = text.split()
        if len(words) > 60:
            text = " ".join(words[:60]) + "..."
        return text

    for attempt in range(MAX_RETRIES + 1):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_call)
                res = future.result(timeout=TIMEOUT_SECONDS)
                if res is not None:
                    return res
        except Exception:
            if attempt == MAX_RETRIES:
                return None
    return None
