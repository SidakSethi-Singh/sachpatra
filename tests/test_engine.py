"""Unit tests for the deterministic engine: scoring, guards, thresholds, and fuzzing."""

import random
import string
import pytest
from app.engine import analyze_text, detect_language, normalize_text
from app.schemas import AnalyzeRequest


class TestEngineGuardsAndScoring:
    def test_normalization(self):
        # Gurmukhi digits ੧੨੩ (123) and Devanagari digits ४५६ (456)
        text = "Hello\u200b World! ੧੨੩ ४५६"
        norm = normalize_text(text)
        assert "\u200b" not in norm
        assert "123" in norm
        assert "456" in norm
        assert norm == "hello world! 123 456"

    def test_language_detection(self):
        assert detect_language("This is English text.") == "en"
        assert detect_language("यह हिंदी में लिखा गया संदेश है।") == "hi"
        assert detect_language("ਇਹ ਪੰਜਾਬੀ ਵਿੱਚ ਲਿਖਿਆ ਗਿਆ ਸੁਨੇਹਾ ਹੈ।") == "pa"

    def test_negation_guard(self):
        # "Do not share OTP" - R10 should NOT fire
        req = AnalyzeRequest(text="Please do not share OTP with anyone.", language="en")
        res = analyze_text(req)
        assert not any(r.id == "R10" for r in res.reasons)

        # Hindi negation: "कोई पैसे नहीं देने हैं" - R05 should NOT fire
        req_hi = AnalyzeRequest(text="आपको कोई जुर्माना या पैसे नहीं देने हैं।", language="hi")
        res_hi = analyze_text(req_hi)
        assert not any(r.id == "R05" for r in res_hi.reasons)

        # Punjabi negation: "ਕੋਈ ਪੈਸੇ ਨਾ ਭੇਜੋ"
        req_pa = AnalyzeRequest(text="ਕਿਸੇ ਨੂੰ ਕੋਈ ਜ਼ਮਾਨਤ ਰਾਸ਼ੀ ਨਾ ਭਰੋ।", language="pa")
        res_pa = analyze_text(req_pa)
        assert not any(r.id == "R05" for r in res_pa.reasons)

    def test_advisory_guard(self):
        # RBI caution / awareness text
        adv_text = (
            "RBI cautions citizens: beware of digital arrest scams impersonating police and CBI. "
            "Never transfer money to safe accounts and do not share OTP."
        )
        req = AnalyzeRequest(text=adv_text, language="en")
        res = analyze_text(req)
        assert res.advisory is True
        # Must not be classified as likely_scam
        assert res.verdict != "likely_scam"

    def test_advisory_fine_imposed_on_bank(self):
        bank_adv = "RBI press release: Fine imposed on bank for non-compliance with KYC directives."
        req = AnalyzeRequest(text=bank_adv, language="en")
        res = analyze_text(req)
        assert res.advisory is True
        assert res.verdict == "cannot_verify"

    def test_verdict_thresholds(self):
        # Full scam text -> likely_scam
        scam_text = (
            "This is CBI officer. You are under digital arrest. Stay on video call. "
            "Pay fine to safe account immediately or face arrest warrant."
        )
        res_scam = analyze_text(AnalyzeRequest(text=scam_text, language="en"))
        assert res_scam.verdict == "likely_scam"
        assert res_scam.score >= 60

        # Suspicious text (only agency mentioned without coercive demands) -> suspicious
        susp_text = "Received letter mentioning Cyber Crime Cell and customs officer."
        res_susp = analyze_text(AnalyzeRequest(text=susp_text, language="en"))
        assert res_susp.verdict in ("suspicious", "cannot_verify")

        # Benign everyday text -> cannot_verify
        benign_text = "Hey, are we still meeting for lunch at 1 PM today near the park?"
        res_benign = analyze_text(AnalyzeRequest(text=benign_text, language="en"))
        assert res_benign.verdict == "cannot_verify"
        assert res_benign.score < 25

    def test_hard_combo_trigger(self):
        # R05 (payment demand 30) + R03 (agency 15) = 45 base score.
        # But hard rule specifies: (R05 or R10) AND (R03 or R01) -> likely_scam
        combo_text = "CBI officer instructed to pay fine to safe account."
        res = analyze_text(AnalyzeRequest(text=combo_text, language="en"))
        assert res.verdict == "likely_scam"

    def test_never_returns_safe_or_authentic(self):
        # Test various benign and ambiguous inputs
        samples = [
            "Everything is completely safe and authentic.",
            "Official verified order from government.",
            "Your order is delivered successfully.",
            "Meeting rescheduled to 4 PM.",
            "Good morning! Have a wonderful day ahead."
        ]
        forbidden = ["safe", "authentic", "genuine", "clean", "legit"]
        for s in samples:
            res = analyze_text(AnalyzeRequest(text=s, language="en"))
            assert res.verdict in ("likely_scam", "suspicious", "cannot_verify")
            for word in forbidden:
                assert word != res.verdict

    def test_random_1000_char_fuzz_never_crashes(self):
        random.seed(42)
        # Generate 20 different 1000-character random strings (Unicode, punctuation, mixed)
        char_pool = string.ascii_letters + string.digits + " \n\t.,;:?!/@#$%&*()-_+=[]{}|~" + "अआइईकखगघचछजझਟਠਡਢਣਤਥਦਧਨਸਹ੧੨੩४५६"
        for _ in range(20):
            rand_text = "".join(random.choice(char_pool) for _ in range(1000))
            res = analyze_text(AnalyzeRequest(text=rand_text, language="auto"))
            assert res is not None
            assert res.verdict in ("likely_scam", "suspicious", "cannot_verify")
            assert 0 <= res.score <= 100
            assert len(res.action_plan) == 6
            assert res.disclaimer != ""
