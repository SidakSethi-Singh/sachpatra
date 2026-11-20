# SachPatra (सचपत्र)

> **Citizen Digital Arrest & Cyber Extortion Scam Screening Engine**  
> *NxtWave IDEA//FORGE Hackathon — Track 1: Civic Pulse & Digital Governance*

---

## 📌 Problem Context
"Digital arrest" scams are a pervasive cyber extortion menace in India. Impersonators pose as officers from the **CBI, Enforcement Directorate (ED), State Police, TRAI, Customs, or Supreme Court** over WhatsApp or Skype video calls, presenting forged warrants and coercing citizens into transferring money to so-called "RBI verification" or "safe holding" accounts.

- **Scale**: Over ₹4,057 crore lost across 2.97 lakh reported complaints (2022 to May 2026).
- **Judicial Context**: The Hon'ble Supreme Court of India took suo motu cognisance on 17 October 2025 ([Order Reference](https://api.sci.gov.in/supremecourt/2025/59769/59769_2025_2_7_65003_Order_17-Oct-2025.pdf)), affirming that **"digital arrest" has zero legal validity in India**. Genuine law enforcement never arrests citizens over video calls or demands money transfers.

---

## 🛡️ Core Architectural Principles (Hard Rules)
1. **100% Deterministic Rule Engine**: Verdicts (`likely_scam`, `suspicious`, `cannot_verify`) are strictly computed by transparent, auditable heuristic rules and regexes. **Gemini never decides the verdict.**
2. **Never Declares Safe**: Output verdicts never state "safe" or "authentic". Unflagged text is classified as `cannot_verify` with guidance to independently verify and call 1930.
3. **Works Without API Keys**: The application is 100% functional offline using rule templates. Multimodal AI (via `google-genai`) is an optional enhancement for transcribing notice photos and elderly plain explanations (8s timeout, 1 retry, silent fallback).
4. **Zero-PII Privacy Architecture**: No uploaded notice text or images are logged or persisted to disk. The SQLite database retains aggregate counters only (verdicts, rule IDs, language, date).
5. **Trilingual & Script Robust**: Native support for **English (EN)**, **Hindi (HI)**, and **Punjabi (PA)**, including Romanized Hinglish. Resilient to homoglyph attacks, zero-width characters, and character-spaced obfuscations.
6. **Zero External Dependencies**: Pure vanilla HTML5/CSS3/ES6 frontend with no external CDN or JavaScript build tools.

---

## 🚀 Getting Started

### 1. Installation
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Running the Application
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Navigate to `http://127.0.0.1:8000` in your web browser.

### 3. Optional Gemini Configuration
```bash
export GEMINI_API_KEY="your-api-key"
export GEMINI_MODEL="gemini-2.5-flash"
```
*(If unset, the app operates gracefully in offline rules mode.)*

---

## 🧪 Testing and Evaluation

### Run Test Suite
```bash
pytest -v
```

### Run Benchmark Evaluation Harness
```bash
python eval/run_eval.py
```
Outputs precision, recall, and safety metrics on the 61-sample labelled benchmark dataset.

---

## ⚖️ Official Helplines & Authorities
- **National Cybercrime Helpline**: Dial `1930`
- **National Cyber Crime Reporting Portal**: [cybercrime.gov.in](https://cybercrime.gov.in)
- **DoT Citizen Portal**: [sancharsaathi.gov.in](https://sancharsaathi.gov.in)
- **Supreme Court Suo Motu Order**: [Order dated 17-Oct-2025](https://api.sci.gov.in/supremecourt/2025/59769/59769_2025_2_7_65003_Order_17-Oct-2025.pdf)

*Disclaimer: Automated screening engine, not legal advice. If in doubt, immediately call 1930.*
