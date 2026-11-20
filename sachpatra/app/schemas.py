from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=6000, description="Notice text, call transcript, or message content")
    language: Literal["en", "hi", "pa", "auto"] = Field(default="auto", description="Input/output language preference")
    channel: Literal["message", "call", "document"] = Field(default="message", description="Delivery channel of the suspected scam")


class Reason(BaseModel):
    id: str = Field(..., description="Rule ID (e.g. R01)")
    title: str = Field(..., description="Short title of the rule")
    why: str = Field(..., description="Explanation of why this indicates a scam")
    weight: int = Field(..., description="Rule weight contribute to score")
    snippet: str = Field(..., max_length=80, description="Matched text snippet (max 80 chars)")
    source_url: str = Field(default="", description="Official reference or advisory URL")


class ActionStep(BaseModel):
    step: int
    title: str
    description: str
    timebox_min: Optional[int] = None


class Drafts(BaseModel):
    complaint_text: str = Field(..., description="Pre-filled cybercrime portal complaint draft")
    script_1930: str = Field(..., description="5-line phone script for calling 1930 helpline")
    family_alert: str = Field(..., description="WhatsApp-ready alert message for family")


class AnalyzeResponse(BaseModel):
    verdict: Literal["likely_scam", "suspicious", "cannot_verify"]
    score: int = Field(..., ge=0, le=100, description="Risk score between 0 and 100")
    reasons: list[Reason] = Field(default_factory=list)
    advisory: bool = Field(default=False, description="True if text appears to be an official warning/advisory")
    language: Literal["en", "hi", "pa"]
    action_plan: list[ActionStep]
    drafts: Drafts
    disclaimer: str

    @field_validator("verdict")
    @classmethod
    def validate_verdict(cls, v: str) -> str:
        forbidden = ["safe", "authentic", "genuine", "legit", "clean"]
        v_lower = v.lower()
        for word in forbidden:
            if word in v_lower:
                raise ValueError(f"Verdict cannot contain '{word}'. Must be likely_scam, suspicious, or cannot_verify.")
        if v not in ("likely_scam", "suspicious", "cannot_verify"):
            raise ValueError(f"Invalid verdict: {v}")
        return v
