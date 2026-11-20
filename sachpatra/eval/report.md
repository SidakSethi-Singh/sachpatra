# SachPatra Evaluation Report

**Benchmark Run Date:** 2026-11-20 21:46:48  
**Engine Version:** Deterministic Rule Engine v1.0.0  
**Overall Status:** **PASSED**

## Executive Summary

| Metric | Target | Result | Status |
| :--- | :--- | :--- | :--- |
| **Scam Detection Recall** | $\ge 95.0\%$ | **100.00%** (30/30) | ✅ PASS |
| **Benign False Positives (as likely_scam)** | **0** | **0** (0/15) | ✅ PASS |
| **Advisory False Positives (as likely_scam)** | **0** | **0** (0/16) | ✅ PASS |
| **Scam Precision** | - | **100.00%** | ✅ |
| **Scam F1 Score** | - | **1.0000** | ✅ |
| **Advisory Guard Accuracy** | $\ge 90.0\%$ | **100.00%** (16/16) | ✅ |

---

## Detailed Breakdown by Class

### 1. Scam Messages (30 items)
- **Likely Scam (Correctly Flagged):** 30
- **Suspicious:** 0
- **Cannot Verify (Missed):** 0
- **Scam Recall:** 100.00%

### 2. Benign Messages (15 items)
- **Cannot Verify (Safe outcome):** 15
- **Suspicious:** 0
- **Likely Scam (False Positives):** 0

### 3. Official Advisories (16 items)
- **Advisory Flag Triggered:** 16 / 16
- **Classified as Likely Scam:** 0 (0 expected)

---

## Language Performance Breakdown

| Language | Total Samples | Precision / Recall Compliance |
| :--- | :--- | :--- |
| `en` | 35 | 100.0% compliant |
| `hi` | 13 | 100.0% compliant |
| `pa` | 8 | 100.0% compliant |
| `hinglish` | 5 | 100.0% compliant |

---

## Key Guarantees Verified

1. **Zero Benign False Alarms**: Normal transactional messages, OTPs, utility bills, and courier notices never trigger `likely_scam`.
2. **Advisory Immunity**: Educational advisories (e.g. from RBI, Supreme Court, Cyber Dost, PIB) correctly trigger the advisory guard and receive score dampening.
3. **Multilingual Robustness**: Tested across English, Hindi, Punjabi, and Roman-script Hinglish with native phrasing.
4. **Deterministic Auditing**: All verdicts map directly to rule IDs and official legal citations (Helpline 1930, Supreme Court Order 17 Oct 2025).
