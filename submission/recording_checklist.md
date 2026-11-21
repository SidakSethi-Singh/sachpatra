# SachPatra Demo Video: Pre-Recording & Submission Checklist

This checklist ensures flawless presentation quality, privacy adherence, and smooth technical execution for the 2:30 hackathon demo video submission.

---

## 1. 🖥️ Screen & Display Configuration
- [ ] **Resolution**: Set display output to **1920 × 1080 (1080p, 16:9)** or **1280 × 720 (720p)**. Do not record on ultrawide monitors without letterboxing.
- [ ] **Browser Zoom**: Set browser zoom to **110% or 125%** so that Gurmukhi/Devanagari scripts, score numbers, and reason cards are crisp and easily readable on mobile screens.
- [ ] **Clean Desktop**: Hide desktop clutter, personal folders, and icons. Set the Windows taskbar to auto-hide or crop it out during recording.
- [ ] **Browser Profile**: Use a dedicated, clean browser profile (Chrome or Brave) with bookmarks bar hidden (`Ctrl + Shift + B`) and extension icons hidden.

---

## 2. 🎙️ Audio & Voice-Over Checks
- [ ] **Microphone**: Use an external USB or condenser microphone placed 6–8 inches away with a pop filter.
- [ ] **Room Acoustics**: Close windows and doors; turn off room fans, air conditioning, and PC fan turbos to eliminate background hum.
- [ ] **Level Test**: Record a 15-second audio sample. Check that vocal levels peak between **-6 dB and -3 dB** (no distortion, clipping, or quiet whispering).
- [ ] **Pacing & Tone**: Aim for **130 to 140 words per minute**. Keep sentences short, authoritative, and confident. Practice pronunciations: *SachPatra* (सच-पत्र), *Sanchar Saathi*, *Gurmukhi*.

---

## 3. 🧹 System & Workspace Hygiene
- [ ] **Notifications Disabled**: Turn on Windows **Focus Assist / Do Not Disturb** (`Win + N` -> Focus).
- [ ] **Close Background Apps**: Exit Telegram, WhatsApp Desktop, Discord, Slack, Outlook, and email clients to avoid incoming message dings or banner popups.
- [ ] **Single Tab Focus**: Keep only the SachPatra app window and a pre-staged terminal window open.

---

## 4. 🔒 Privacy, Security & Data Safety (Crucial)
- [ ] **Hide Environment Secrets**: Ensure `.env`, API keys (`GEMINI_API_KEY`), terminal history containing keys, and tokens are **NEVER visible on screen**.
- [ ] **Zero Real Personal Data**: Never display real Aadhaar numbers, real bank accounts, real names, or real phone numbers on screen.
- [ ] **Use Watermarked Samples Only**: Use exclusively the provided test files from `data/samples/` (`sample_01_arrest_warrant.png`, `sample_02_freeze_order.png`, etc.). Every notice image on screen must show the prominent diagonal watermark: `SAMPLE — INVENTED AGENCY — FAKE`. Never display actual police or CBI letterheads.

---

## 5. 🎬 Rehearsal & Dry Run (End-to-End Walkthrough)
Complete this 9-step rehearsal once before hitting record:
1. [ ] **Homepage Load**: Open `https://sachpatra.onrender.com` (or local `http://127.0.0.1:8000`). Confirm fast initial render.
2. [ ] **Punjabi Switch**: Tap **ਪੰ** button in navbar. Verify text switches to Punjabi smoothly.
3. [ ] **Sample Upload**: Switch to *Upload Notice Photo* mode. Tap sample chip **🚨 ਸੀ.ਬੀ.ਆਈ. ਡਿਜੀਟਲ ਅਰੈਸਟ**. Confirm image loads in preview box.
4. [ ] **Verdict Generation**: Tap **ਚੈੱਕ ਕਰੋ**. Confirm Red Verdict Card appears with Score 100 and reasons R01, R03, R05.
5. [ ] **Action Checklist & 1930**: Check off 2 checkboxes. Hover over `Call 1930` and official links.
6. [ ] **Read Aloud & Drafts**: Tap *Read Aloud* to test audio output. Switch to *Drafts* tab and tap *Copy Family Alert*.
7. [ ] **Benign Test (False Alarm Guard)**: Switch to *Paste message*. Tap *Authentic Bank OTP*. Click *Check*. Confirm neutral `cannot_verify` verdict with 0 risk score.
8. [ ] **Dashboard & Transparency**: Tap *Dashboard* tab (verify SVG charts render). Tap *Transparency* tab (verify 14 rules render).
9. [ ] **Terminal / Test Evidence**: Switch to terminal. Run `python -m pytest -q` or show `eval/report.md` metrics table.

---

## 6. 🎥 Video Recording, Editing & Export
- [ ] **Tool**: Use OBS Studio, Camtasia, Loom, or Windows Game Bar (`Win + G`).
- [ ] **Frame Rate**: Record at 30 fps or 60 fps at constant bitrate.
- [ ] **Duration Limit**: Video must be strictly between **2:15 and 2:30** (under 150 seconds).
- [ ] **Export Format**: **MP4** container with H.264 video codec and AAC stereo audio (44.1 kHz / 16-bit).
- [ ] **File Size**: Target **under 50 MB** (maximum 100 MB). If oversized, compress using HandBrake (Web Optimized, RF 22).

---

## 7. 🌐 Video Hosting & Access Verification
- [ ] **Upload Option A (Recommended — YouTube)**:
  - Upload as **Unlisted** (not Private).
  - Title: `SachPatra — Citizen Shield Against Digital Arrest (NxtWave IDEA//FORGE Hackathon)`
- [ ] **Upload Option B (Google Drive)**:
  - Share settings set to: **"Anyone with the link can view"**.
- [ ] **Incognito / Private Window Test**:
  - Open a **new Private / Incognito browser window** (where you are logged out of Google/YouTube).
  - Paste the video link and confirm it plays immediately without requesting access or permissions.
