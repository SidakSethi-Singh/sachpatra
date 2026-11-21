# SachPatra (सचपत्र / ਸੱਚਪੱਤਰ) — Official Hackathon Submission Pack

> **Hackathon**: NxtWave IDEA//FORGE Hackathon (Nov 2026)  
> **Track**: Track 1 — Civic Pulse & Digital Governance  
> **Participant**: Sidak Sethi (Solo)  
> **Repository**: [https://github.com/SidakSethi-Singh/sachpatra](https://github.com/SidakSethi-Singh/sachpatra)  
> **Live Deployment**: `https://sachpatra.onrender.com` *(or local demo at `http://127.0.0.1:8000`)*  
> **Submission Deadline**: 22 November 2026  
> **Submission Form**: [https://bit.ly/onlinehackathon-ideaforge](https://bit.ly/onlinehackathon-ideaforge)

---

## 1. 📋 150-Word Project Description

SachPatra (सचपत्र) is an emergency digital shield protecting Indian citizens from "digital arrest" scams and cyber extortion syndicates that have defrauded over ₹4,057 crore nationwide. Fraudsters impersonate police, CBI, ED, and customs officials over video calls, brandishing forged warrants to demand immediate money transfers. SachPatra allows citizens to paste suspicious messages, describe calls, or upload notice photos in English, Hindi, and Punjabi. In milliseconds, a 100% deterministic 14-rule engine analyzes legal threats, agency impersonation, and payment coercion without risking LLM hallucinations or prompt injection. When fraud is detected, it delivers an actionable 10-minute crisis plan, one-tap national helpline 1930 dialing, native voice read-outs for elderly victims, pre-drafted cybercrime complaints, and WhatsApp family alerts. Built with a zero-PII privacy guarantee, notice texts and photos are processed in memory and discarded instantly, while anonymous aggregate counters power a live civic transparency dashboard.

---

## 2. 💡 5 "Why It Matters" Bullets

1. **Staggering National Financial Loss**: Ministry of Home Affairs (MHA) and I4C data presented to Parliament reveals over **₹4,057 crore lost across 2.97 lakh complaints** between 2022 and May 2026, making digital arrest India's most destructive cyber extortion format.
2. **Preys on Vulnerable Elderly Citizens**: Syndicates weaponize psychological isolation ("keep camera on, tell no one") to panic retirees and senior citizens into liquidating fixed deposits and retirement funds.
3. **Supreme Court Legal Precedent**: On October 17, 2025, the Supreme Court of India took suo motu cognisance (*WP Crl. 59769/2025*), conclusively establishing that **"digital arrest" has zero legal standing in Indian jurisprudence**. Real police never arrest citizens over video calls.
4. **Vernacular-First Accessibility**: By providing native Punjabi (Gurmukhi), Hindi (Devanagari), and English with native audio speech synthesis, SachPatra protects non-English speaking citizens across India’s digital divide.
5. **Deterministic Security with Zero-PII Privacy**: Eliminates LLM jailbreak and hallucination risks by keeping verdicts 100% rule-bound, while ensuring sensitive citizen messages and notice photos are never stored on disk or logged.

---

## 3. 🎯 Problem & Solution Overview

### The Problem
Transnational cyber syndicates (operating heavily from Southeast Asia per DoT/I4C reports) execute coordinated psychological extortion attacks:
- **Impersonation**: Fraudsters disguise themselves in fake police uniforms against forged agency backdrops (CBI, ED, Cyber Crime, Supreme Court).
- **Fabricated Allegations**: Victims are falsely told their Aadhaar or SIM was linked to money laundering, drug parcels, or terrorism.
- **Coerced Video Confinement**: Victims are forced to remain on Skype, WhatsApp, or Telegram video calls for hours or days under threat of immediate physical arrest.
- **Extortion of Savings**: Citizens are intimidated into transferring funds to bogus "RBI security" or "government clearance" accounts.

### The Solution: SachPatra
An instant, zero-friction civic screening portal designed for high-stress emergencies:
- **Tri-Modal Input**: Citizens paste text, upload notice photos, or describe an ongoing call.
- **Instant Deterministic Screening**: Evaluates 14 hardened indicators (R01–R14) with anti-obfuscation de-spacing, homoglyph mapping, and negation guards.
- **Calm Crisis Triage**: Replaces panic with a 10-minute step-by-step checklist, speed-dial to the **1930** cyber fraud helpline, and links to **cybercrime.gov.in** and **Sanchar Saathi**.
- **Elderly Audio Read-Out**: High-contrast UI with one-click speech synthesis in Hindi, Punjabi, and English.
- **Pre-Drafted Action Assets**: One-tap copyable 1930 call scripts, official cybercrime complaint text, and WhatsApp family alerts.

---

## 4. 🛠️ Complete Technical Stack

| Layer | Technology | Key Architectural Decisions |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.11 / 3.14 + FastAPI | Lightweight asynchronous API, strict Pydantic v2 data models, lifespan context managers. |
| **Verdict Engine** | Pure Python Standard Library (`re`, `unicodedata`) | **100% deterministic rule engine**. Zero LLM verdict dependency. Immune to prompt injections and hallucinations. |
| **Optional Multimodal AI** | Google GenAI SDK (`google-genai`) | Auxiliary document OCR (`extract_from_image`) and plain explanation simplification (`simplify`) with 8s timeout and silent offline fallback. |
| **Frontend** | Vanilla HTML5, CSS3, ES6 JavaScript | **Zero build tools, zero external CDN dependencies**. Fully self-contained, mobile-first responsive (375px to 1280px), native font stacks for Devanagari and Gurmukhi. |
| **Analytics & Storage** | SQLite (`stats.db`) | **Counters only schema**. Stores strictly aggregate daily counts by verdict, rule, and language. **Zero PII, zero message text, zero IP addresses**. |
| **Security & Hardening** | Custom FastAPI Middleware | Strict CSP (zero external hosts), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, sliding window rate limiting (20 req/min), memory-only EXIF stripping. |
| **Testing & CI/CD** | Pytest + GitHub Actions | 102 comprehensive tests (unit, adversarial, security, headless UI) running on every commit. |
| **Containerization** | Docker (`python:3.11-slim`) | Non-root security user (`appuser`), dynamic port binding (`PORT`), minimal image size. |

---

## 5. ⚖️ What Is Real vs. Limits (Honest Disclosure)

### What Is Real & Functional
1. **14 Auditable Deterministic Rules**: Evaluates explicit legal phrases, agency names, urgency markers, and payment coercion patterns.
2. **102 Automated Tests Passing**: Comprehensive test coverage spanning multilingual regexes, Cyrillic/Greek homoglyph evasion, intra-word letter spacing, upload limits, and headless browser XSS injection.
3. **High-Accuracy Benchmark**: Achieved 100% scam recall and 0 benign false alarms across the 61-sample labelled evaluation suite plus 25 fresh hostile audit messages.
4. **Complete Offline Capability**: The entire screening engine and action plan generator operate without internet or API keys.
5. **Zero-PII Storage**: Absolutely no notice text, telephone numbers, or citizen images are retained or logged.
6. **Live Civic Dashboard**: Renders real-time aggregate trend charts using lightweight inline SVG with no external charting libraries.

### Honest Limitations
1. **Cannot Confirm Authenticity**: SachPatra **never declares any notice "safe" or "authentic"**. Genuine legal notices served in person by law enforcement cannot be authenticated by an online screening tool. Unflagged items receive a `cannot_verify` verdict with instructions to verify through official police stations.
2. **Automated Screening, Not Legal Counsel**: SachPatra is an emergency civic aid, not a formal legal opinion. Citizens under duress or in doubt must immediately contact the national **1930** helpline.
3. **Evaluation Dataset Scope**: While rigorous, the benchmark dataset comprises 61 curated labelled cases and 25 adversarial test cases. Scammer syndicates continuously adapt tactics, requiring ongoing rule updates.
4. **Gemini Role is Strictly Auxiliary**: Gemini is used exclusively for multimodal OCR text extraction and plain-language simplification for elderly readers. **Gemini has 0% authority over verdicts**. Without an API key, image upload prompts the user to paste text directly into the offline engine.

---

## 6. ✅ Final Submission Checklist

- [x] **Public GitHub Repository**: [https://github.com/SidakSethi-Singh/sachpatra](https://github.com/SidakSethi-Singh/sachpatra) with clear documentation, MIT license, and CI test badges.
- [x] **Production Deployment Config**: [render.yaml](file:///c:/Users/sidak/OneDrive/Desktop/Nxt_Wave_Idea_forge_Hackthon/render.yaml) and [Dockerfile](file:///c:/Users/sidak/OneDrive/Desktop/Nxt_Wave_Idea_forge_Hackthon/Dockerfile) configured for seamless cloud hosting.
- [x] **Live Service Verified**:
  - `/api/health` returns `200 OK`.
  - Text screening flow verified with instant red flags and 10-minute action checklist.
  - Image upload flow verified with SAMPLE-watermarked documents.
  - Punjabi (Gurmukhi) and Hindi (Devanagari) UIs verified without missing glyphs.
  - Civic Dashboard verified with zero-dependency inline SVG charts.
- [x] **Demo Video (2:30)**: Recorded following [submission/video_script.md](file:///c:/Users/sidak/OneDrive/Desktop/Nxt_Wave_Idea_forge_Hackthon/submission/video_script.md) and checked against [submission/recording_checklist.md](file:///c:/Users/sidak/OneDrive/Desktop/Nxt_Wave_Idea_forge_Hackthon/submission/recording_checklist.md). Link verified in an Incognito window.
- [x] **Challazo Registration**: Hackathon registration completed on the portal.
- [x] **Official Submission Form**: Google Form ([https://bit.ly/onlinehackathon-ideaforge](https://bit.ly/onlinehackathon-ideaforge)) filled and submitted before 22 November 2026.
