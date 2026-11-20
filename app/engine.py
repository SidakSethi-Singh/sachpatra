"""Deterministic rule evaluation engine for SachPatra.
Applies text normalization, negation guards, awareness/advisory guards,
weighted scoring with multi-category synergy, and verdict determination.
"""

import re
from typing import List, Optional, Set, Tuple

from app.actions import build_action_plan, build_drafts
from app.gemini import simplify
from app.i18n import CANNOT_VERIFY_ADVICE, DISCLAIMER, PLAIN_SUMMARY_FALLBACK, RULES_METADATA
from app.rules import RULES, Rule, normalize_text
from app.schemas import ActionStep, AnalyzeRequest, AnalyzeResponse, Drafts, Reason

NEGATION_WORDS: Set[str] = {
    "no", "not", "never", "neither", "nor", "none", "dont", "don't", "wont", "won't",
    "cannot", "can't", "nahi", "nahin", "nhi", "na", "mat",
    "नहीं", "न", "मत", "ना", "ਨਹੀਂ", "ਨਾ", "ਮਤ", "ਕਦੇ ਨਹੀਂ", "ਕੋਈ ਨਹੀਂ"
}

AWARENESS_PATTERNS = [
    re.compile(r"\b(?:beware\s+of|be\s+aware|stay\s+alert|public\s+alert|public\s+advisory|public\s+notice|security\s+advisory|rbi\s+cautions|rbi\s+warns|police\s+advises|press\s+release|fine\s+imposed\s+on\s+bank|penalty\s+imposed\s+on\s+bank|caution\s+notice|do\s+not\s+share\s+otp|cyber\s+awareness|awareness\s+campaign|fact\s+check|cyber\s+dost|advisory\s+note|protect\s+yourself|cautioned\s+against|warning\s+against\s+fraud)\b", re.IGNORECASE),
    re.compile(r"(?:सावधान\s*रहें|सतर्क\s*रहें|सचेत\s*रहें|जनहित\s*में\s*जारी|प्रेस\s*विज्ञप्ति|धोखाधड़ी\s*से\s*बचें|आरबीआई\s*ने\s*चेतावनी\s*दी|बैंक\s*पर\s*जुर्माना|ओटीपी\s*(?:किसी\s*को\s*)?(?:न\s*दें|साझा\s*न\s*करें)|साइबर\s*जागरूकता)", re.IGNORECASE),
    re.compile(r"(?:ਸੁਚੇਤ\s*ਰਹੋ|ਸਾਵਧਾਨ\s*ਰਹੋ|ਚੌਕਸ\s*ਰਹੋ|ਜਨਤਕ\s*ਸੂਚਨਾ|ਪ੍ਰੈਸ\s*ਰਿਲੀਜ਼|ਠੱਗੀ\s*ਤੋਂ\s*ਬਚੋ|ਓਟੀਪੀ\s*ਸਾਂਝਾ\s*ਨਾ\s*ਕਰੋ|ਸਾਈਬਰ\s*ਜਾਗਰੂਕਤਾ)", re.IGNORECASE),
    re.compile(r"\b(?:savdhan\s*rahe|satark\s*rahe|bach\s*ke\s*rahe|fraud\s*se\s*bache|public\s*advisory|press\s*release|awareness\s*alert)\b", re.IGNORECASE)
]

URGENT_DEMAND_PATTERNS = [
    re.compile(r"\b(?:you\s+must\s+pay|pay\s+immediately|immediately\s+transfer|transfer\s+now|pay\s+now|deposit\s+immediately|clear\s+your\s+dues\s+now|otherwise\s+you\s+will\s+be\s+arrested|send\s+money\s+now|pay\s+fine\s+now)\b", re.IGNORECASE),
    re.compile(r"(?:तुरंत\s*(?:भुगतान\s*करें|पैसे\s*भेजें|जमा\s*करें|ट्रांसफर\s*करें)|आप\s*तुरंत\s*पैसे\s*दें|अन्यथा\s*गिरफ्तार\s*किया\s*जाएगा|अभी\s*पैसे\s*जमा\s*करो)", re.IGNORECASE),
    re.compile(r"(?:ਤੁਰੰਤ\s*(?:ਪੈਸੇ\s*ਭੇਜੋ|ਜਮ੍ਹਾਂ\s*ਕਰੋ|ਭੁਗਤਾਨ\s*ਕਰੋ)|ਨਹੀਂ\s*ਤਾਂ\s*ਗ੍ਰਿਫ਼ਤਾਰ\s*ਕੀਤਾ\s*ਜਾਵੇਗਾ|ਹੁਣੇ\s*ਪੈਸੇ\s*ਦਿਓ)", re.IGNORECASE),
    re.compile(r"\b(?:turant\s*(?:pay\s*karo|paisa\s*bhejo|transfer\s*karo)|abhi\s*ke\s*abhi\s*transfer|nahi\s*to\s*arrest\s*hoge)\b", re.IGNORECASE)
]


def detect_language(text: str) -> str:
    """Detect language by Unicode script block.
    Devanagari -> hi, Gurmukhi -> pa, else en.
    """
    devanagari_count = sum(1 for c in text if "\u0900" <= c <= "\u097f")
    gurmukhi_count = sum(1 for c in text if "\u0a00" <= c <= "\u0a7f")
    if devanagari_count > 0 and devanagari_count >= gurmukhi_count:
        return "hi"
    if gurmukhi_count > 0 and gurmukhi_count > devanagari_count:
        return "pa"
    return "en"


def is_negated_match(text: str, start: int, end: int, rule_id: str = "") -> bool:
    """Check if the matched pattern is preceded within 6 tokens in the current clause
    by negation words, or contains negation words within the matched span
    (except for rules like R02 and R06 whose definition inherently includes negative phrasing).
    """
    # Restrict preceding text to current clause/sentence boundary
    preceding_text = text[:start]
    clause_parts = re.split(r"[.!?।;\n]", preceding_text)
    current_clause = clause_parts[-1] if clause_parts else preceding_text

    tokens = re.findall(r"\S+", current_clause)
    recent_tokens = tokens[-6:] if len(tokens) >= 6 else tokens
    for token in recent_tokens:
        clean_tok = token.strip(".,;:!?\"'()[]{}<>-")
        if clean_tok in NEGATION_WORDS:
            return True

    # Check tokens inside match span for SOV languages where negation particle is before verb
    if rule_id not in ("R02", "R06"):
        match_tokens = re.findall(r"\S+", text[start:end])
        for token in match_tokens:
            clean_tok = token.strip(".,;:!?\"'()[]{}<>-")
            if clean_tok in NEGATION_WORDS:
                return True

    return False


def make_snippet(text: str, start: int, end: int, max_len: int = 80) -> str:
    """Extract an informative snippet of up to 80 characters around the match."""
    match_len = end - start
    if match_len >= max_len:
        return text[start:start + max_len - 3] + "..."

    remaining = max_len - match_len
    left_pad = remaining // 2
    right_pad = remaining - left_pad

    s = max(0, start - left_pad)
    e = min(len(text), end + right_pad)

    snippet = text[s:e].strip()
    if s > 0 and not snippet.startswith("..."):
        snippet = "..." + snippet
    if e < len(text) and not snippet.endswith("..."):
        snippet = snippet + "..."

    if len(snippet) > max_len:
        snippet = snippet[:max_len - 3] + "..."
    return snippet


def evaluate_rules(text: str, norm_text: str) -> List[Tuple[Rule, str]]:
    """Evaluate all 14 deterministic rules against normalised text with negation guard.
    Returns list of (fired_rule, matched_snippet).
    """
    fired: List[Tuple[Rule, str]] = []

    for rule in RULES:
        if rule.custom_checker:
            match_span = rule.custom_checker(norm_text)
            if match_span:
                start, end = match_span
                if not is_negated_match(norm_text, start, end, rule.id):
                    snippet = make_snippet(norm_text, start, end, max_len=80)
                    fired.append((rule, snippet))
            continue

        rule_matched = False
        for lang_key, pattern_str in rule.patterns.items():
            if not pattern_str:
                continue
            try:
                pattern = re.compile(pattern_str, re.IGNORECASE)
            except re.error:
                continue

            for m in pattern.finditer(norm_text):
                start, end = m.span()
                if not is_negated_match(norm_text, start, end, rule.id):
                    snippet = make_snippet(norm_text, start, end, max_len=80)
                    fired.append((rule, snippet))
                    rule_matched = True
                    break
            if rule_matched:
                break

    return fired


def check_advisory(text: str, norm_text: str) -> bool:
    """Check if the text is a legitimate awareness or caution advisory."""
    matches_awareness = any(pat.search(norm_text) for pat in AWARENESS_PATTERNS)
    if not matches_awareness:
        return False
    has_urgent_demand = any(pat.search(norm_text) for pat in URGENT_DEMAND_PATTERNS)
    return not has_urgent_demand


def analyze_text(request: AnalyzeRequest, engine_tag: str = "rules") -> AnalyzeResponse:
    """Main deterministic analysis pipeline."""
    raw_text = request.text
    norm_text = normalize_text(raw_text)

    # 1. Language determination
    detected_lang = detect_language(raw_text)
    output_lang = detected_lang if request.language == "auto" else request.language
    if output_lang not in ("en", "hi", "pa"):
        output_lang = "en"

    # 2. Evaluate rules with negation guard
    fired_rules_with_snippets = evaluate_rules(raw_text, norm_text)

    # 3. Advisory guard
    is_advisory = check_advisory(raw_text, norm_text)

    # 4. Score calculation
    sum_weights = sum(r.weight for r, _ in fired_rules_with_snippets)
    distinct_categories = {r.category for r, _ in fired_rules_with_snippets}
    category_bonus = 10 if len(distinct_categories) >= 3 else 0

    base_score = min(100, sum_weights + category_bonus)
    if is_advisory:
        final_score = min(100, int(round(base_score * 0.3)))
    else:
        final_score = base_score

    # 5. Verdict determination
    fired_ids = {r.id for r, _ in fired_rules_with_snippets}
    has_payment_or_tech = ("R05" in fired_ids or "R10" in fired_ids)
    has_agency_or_digital_arrest = ("R03" in fired_ids or "R01" in fired_ids)
    hard_trigger = has_payment_or_tech and has_agency_or_digital_arrest

    if not is_advisory and (final_score >= 60 or hard_trigger):
        verdict = "likely_scam"
    elif final_score >= 25:
        verdict = "suspicious"
    else:
        verdict = "cannot_verify"

    # 6. Build Reasons
    reasons: List[Reason] = []
    for rule, snippet in fired_rules_with_snippets:
        meta = RULES_METADATA.get(rule.id, {})
        title_dict = meta.get("title", {})
        why_dict = meta.get("why", {})
        title = title_dict.get(output_lang, title_dict.get("en", f"Rule {rule.id}"))
        why = why_dict.get(output_lang, why_dict.get("en", "Suspicious pattern detected."))
        source_url = meta.get("source_url", "")
        reasons.append(
            Reason(
                id=rule.id,
                title=title,
                why=why,
                weight=rule.weight,
                snippet=snippet,
                source_url=source_url
            )
        )

    # 7. Action plan and reporting drafts
    action_plan = build_action_plan(output_lang)
    drafts = build_drafts(raw_text, output_lang)

    # 8. Plain-language summary (Gemini enhancement or i18n fallback)
    plain_summary = simplify(reasons, output_lang)
    if not plain_summary:
        plain_summary = PLAIN_SUMMARY_FALLBACK.get(verdict, {}).get(
            output_lang, PLAIN_SUMMARY_FALLBACK[verdict]["en"]
        )

    # 9. Disclaimer
    disclaimer = DISCLAIMER.get(output_lang, DISCLAIMER["en"])

    return AnalyzeResponse(
        verdict=verdict,
        score=final_score,
        reasons=reasons,
        advisory=is_advisory,
        language=output_lang,
        action_plan=action_plan,
        drafts=drafts,
        disclaimer=disclaimer,
        plain_summary=plain_summary,
        engine=engine_tag
    )
