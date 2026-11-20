# SachPatra: project brief
Hackathon: NxtWave IDEA//FORGE, Track 1 (Civic Pulse, Digital Governance). Solo. Deadline 22 Nov 2026.
Problem: "Digital arrest" scams. Fraudsters impersonate CBI/ED/Police/TRAI/Customs on video calls, send forged notices, demand money. Govt data: 2.97 lakh complaints and Rs 4,057 cr lost (2022 to May 2026). Supreme Court took suo motu cognisance (order 17 Oct 2025). "Digital arrest" has no legal basis in India.
Product: user pastes text, uploads a notice image, or describes a call (EN/HI/PA). Returns verdict + reasons + 10-minute action plan + drafts + voice read-out + anonymised dashboard.

## Hard rules
1. Verdict comes ONLY from the deterministic rule engine. Gemini never decides the verdict.
2. Verdicts: "likely_scam", "suspicious", "cannot_verify". NEVER say safe or authentic.
3. Must work fully with NO API key (rules + templates). Gemini is optional enhancement, 8s timeout, silent fallback.
4. Privacy: never store or log notice text/images. Stats store only counters (verdict, rule ids, language, date).
5. Languages: en, hi, pa. All user-facing strings live in `app/i18n.py`. Roman-script Hinglish input must be detected too.
6. Stack: Python 3.11, FastAPI, pydantic v2, pytest, vanilla HTML/CSS/JS (no build step, no CDN dependencies), SQLite for stats.
7. Gemini via `google-genai` SDK. Model name from env `GEMINI_MODEL` (default: a Flash model that works on my plan). Key from env `GEMINI_API_KEY`.
8. Sample documents must be watermarked SAMPLE and must not copy any real agency letterhead.
9. Official refs only: 1930 helpline, cybercrime.gov.in, Sanchar Saathi (sancharsaathi.gov.in), Supreme Court order https://api.sci.gov.in/supremecourt/2025/59769/59769_2025_2_7_65003_Order_17-Oct-2025.pdf
10. Disclaimer on every result: "Automated screening, not legal advice. If in doubt, call 1930."

## Layout
app/{main.py,rules.py,engine.py,i18n.py,gemini.py,actions.py,stats.py,schemas.py}
app/static/{index.html,app.css,app.js}
data/samples/  eval/labelled.jsonl  eval/run_eval.py  tests/  Dockerfile  README.md
