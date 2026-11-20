"""Action plan and draft generation for SachPatra."""

import datetime
import re
from typing import List, Tuple
from app.i18n import ACTION_STEPS, DRAFT_TEMPLATES, RULES_METADATA
from app.schemas import ActionStep, Drafts


def extract_incident_facts(text: str, language: str) -> Tuple[str, str, str]:
    """Extract claimed agency, amount, and caller/UPI info from the text if available."""
    # 1. Agency extraction
    agency_patterns = [
        (r"\b(cbi|central\s+bureau\s+of\s+investigation)\b", "CBI (Central Bureau of Investigation)"),
        (r"\b(enforcement\s+directorate|ed\s+officer)\b", "Enforcement Directorate (ED)"),
        (r"\b(ncb|narcotics\s+control\s+bureau)\b", "Narcotics Control Bureau (NCB)"),
        (r"\b(trai|telecom\s+regulatory\s+authority)\b", "TRAI / Telecom Dept"),
        (r"\b(mumbai\s+police|delhi\s+police|cyber\s+crime\s+cell|cyber\s+cell|police)\b", "Police / Cyber Crime Cell"),
        (r"\b(customs\s+department|customs\s+officer)\b", "Customs Department"),
        (r"\b(supreme\s+court)\b", "Supreme Court"),
        (r"(सीबीआई|केंद्रीय\s*जांच\s*ब्यूरो)", "CBI (सीबीआई)"),
        (r"(ईडी|प्रवर्तन\s*निदेशालय)", "ED (प्रवर्तन निदेशालय)"),
        (r"(साइबर\s*सेल|पुलिस)", "Cyber Cell / Police"),
        (r"(ਸੀਬੀਆਈ)", "CBI (ਸੀਬੀਆਈ)"),
        (r"(ਪੁਲਿਸ|ਸਾਈਬਰ\s*ਸੈੱਲ)", "Police / Cyber Cell"),
    ]
    detected_agency = None
    for pat, label in agency_patterns:
        if re.search(pat, text, re.IGNORECASE):
            detected_agency = label
            break

    default_agency = {
        "en": "Impersonated Law Enforcement Agency (CBI/Police/ED)",
        "hi": "फर्जी जांच एजेंसी (CBI/पुलिस/ED)",
        "pa": "ਨਕਲੀ ਜਾਂਚ ਏਜੰਸੀ (CBI/ਪੁਲਿਸ/ED)"
    }.get(language, "Impersonated Law Enforcement Agency")
    agency = detected_agency or default_agency

    # 2. Amount extraction
    amount_match = re.search(r"(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|thousand))?)|\b([\d,]+)\s*(?:rupees|रुपये|ਰੁਪਏ|lakh|crore)\b", text, re.IGNORECASE)
    if amount_match:
        amount_str = amount_match.group(0).strip()
    else:
        amount_str = {
            "en": "Unspecified amount (demanded during coercive video/voice call)",
            "hi": "अनिर्दिष्ट राशि (कॉल के दौरान मांगी गई)",
            "pa": "ਅਣਦੱਸੀ ਰਕਮ (ਕਾਲ ਦੌਰਾਨ ਮੰਗੀ ਗਈ)"
        }.get(language, "Unspecified amount")

    # 3. Caller / UPI extraction
    upi_match = re.search(r"\b[\w.\-]+@(okhdfcbank|okaxis|oksbi|okicici|paytm|ybl|ibl|upi|axl|apl|barodampay|federal)\b", text, re.IGNORECASE)
    phone_match = re.search(r"(?:\+91[\s-]?)?[6789]\d{9}", text)

    if upi_match and phone_match:
        caller_or_upi = f"Phone: {phone_match.group(0)}, UPI: {upi_match.group(0)}"
    elif upi_match:
        caller_or_upi = f"UPI ID: {upi_match.group(0)}"
    elif phone_match:
        caller_or_upi = f"Phone Number: {phone_match.group(0)}"
    else:
        caller_or_upi = {
            "en": "Caller details recorded in incoming call logs and message history",
            "hi": "कॉलर का विवरण फोन के कॉल लॉग और मैसेज में उपलब्ध",
            "pa": "ਕਾਲਰ ਦੇ ਵੇਰਵੇ ਫੋਨ ਕਾਲ ਲਾਗ ਅਤੇ ਮੈਸੇਜ ਵਿੱਚ ਮੌਜੂਦ"
        }.get(language, "Details recorded in incoming call logs")

    return agency, amount_str, caller_or_upi


def build_action_plan(language: str) -> List[ActionStep]:
    """Build the 6-step actionable mitigation plan, time-boxed for immediate emergency response."""
    lang = language if language in ACTION_STEPS else "en"
    raw_steps = ACTION_STEPS[lang]
    return [
        ActionStep(
            step=item["step"],
            title=item["title"],
            description=item["description"],
            timebox_min=item["timebox_min"]
        )
        for item in raw_steps
    ]


def build_drafts(text: str, language: str) -> Drafts:
    """Generate pre-filled reporting drafts for cybercrime.gov.in, 1930, and family alert."""
    lang = language if language in DRAFT_TEMPLATES else "en"
    agency, amount, caller_or_upi = extract_incident_facts(text, lang)
    current_date = datetime.date.today().strftime("%d-%b-%Y")

    templates = DRAFT_TEMPLATES[lang]
    complaint = templates["complaint_text"].format(
        date=current_date,
        agency=agency,
        amount_or_details=amount,
        caller_or_upi=caller_or_upi
    )
    script = templates["script_1930"].format(
        agency=agency,
        amount_or_details=amount,
        caller_or_upi=caller_or_upi
    )
    family = templates["family_alert"].format(
        agency=agency
    )

    return Drafts(
        complaint_text=complaint,
        script_1930=script,
        family_alert=family
    )
