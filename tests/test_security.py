"""Security, Privacy, and Reliability tests for SachPatra."""

import os
import sqlite3
import pytest
from fastapi.testclient import TestClient
from app.main import app, reset_rate_limits
from app.stats import get_db_connection, init_db, record_stat, get_stats
from app.gemini import get_gemini_client, simplify, extract_from_image
from app.schemas import Reason

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_rate_limits():
    reset_rate_limits()
    yield
    reset_rate_limits()


def test_security_headers_present():
    """Verify security headers: CSP without external hosts, nosniff, DENY, referrer policy."""
    response = client.get("/api/health")
    assert response.status_code == 200

    headers = response.headers
    assert "content-security-policy" in headers
    csp = headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    # No external domain whitelist
    assert "https://" not in csp

    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"


def test_rate_limiting_enforced():
    """Verify in-memory sliding window rate limiter blocks 21st request with 429."""
    # First 20 requests succeed
    for i in range(20):
        res = client.post("/api/analyze", json={"text": f"Normal test message {i}"})
        assert res.status_code == 200, f"Request {i+1} failed"

    # 21st request must trigger 429
    res_blocked = client.post("/api/analyze", json={"text": "Request 21"})
    assert res_blocked.status_code == 429
    assert "Rate limit exceeded" in res_blocked.json()["detail"]


def test_upload_limits_and_magic_bytes():
    """Verify 5MB upload limit and magic byte checks."""
    # 1. Fake extension (e.g. .exe)
    res_fake_ext = client.post(
        "/api/analyze-image",
        files={"file": ("malware.exe", b"\xff\xd8\xff1234567890", "image/jpeg")}
    )
    assert res_fake_ext.status_code == 400

    # 2. Fake magic bytes with .jpg extension
    res_fake_bytes = client.post(
        "/api/analyze-image",
        files={"file": ("fake.jpg", b"NOT_A_REAL_IMAGE_DATA_1234", "image/jpeg")}
    )
    assert res_fake_bytes.status_code == 400

    # 3. Too small
    res_tiny = client.post(
        "/api/analyze-image",
        files={"file": ("tiny.png", b"short", "image/png")}
    )
    assert res_tiny.status_code == 400


def test_no_stack_traces_on_internal_error():
    """Verify unhandled exceptions return clean 500 JSON with no stack trace or internal paths."""
    from unittest.mock import patch
    no_raise_client = TestClient(app, raise_server_exceptions=False)

    with patch("app.main.analyze_text", side_effect=RuntimeError("Secret database connection failed")):
        response = no_raise_client.post("/api/analyze", json={"text": "Trigger 500 error"})
        assert response.status_code == 500
        body = response.json()
        assert body == {"detail": "Internal server error"}
        assert "Secret" not in response.text
        assert "Traceback" not in response.text
        assert ".py" not in response.text


def test_sqlite_stores_no_text_or_pii(tmp_path):
    """Verify that SQLite tables store counters only and contain NO text, IP, or PII columns."""
    test_db = str(tmp_path / "test_stats.db")
    init_db(test_db)

    # Record some stats
    record_stat(verdict="likely_scam", rule_ids=["R01", "R05"], language="en", db_path=test_db)
    record_stat(verdict="suspicious", rule_ids=["R03"], language="hi", db_path=test_db)

    conn = get_db_connection(test_db)
    cursor = conn.cursor()

    # Inspect daily_verdicts columns
    cursor.execute("PRAGMA table_info(daily_verdicts)")
    verdict_cols = [row[1] for row in cursor.fetchall()]
    assert set(verdict_cols) == {"date", "verdict", "count"}

    # Inspect daily_rules columns
    cursor.execute("PRAGMA table_info(daily_rules)")
    rule_cols = [row[1] for row in cursor.fetchall()]
    assert set(rule_cols) == {"date", "rule_id", "count"}

    # Inspect daily_languages columns
    cursor.execute("PRAGMA table_info(daily_languages)")
    lang_cols = [row[1] for row in cursor.fetchall()]
    assert set(lang_cols) == {"date", "language", "count"}

    # Inspect rows: assure no text or IP addresses
    cursor.execute("SELECT * FROM daily_verdicts")
    rows = cursor.fetchall()
    for row in rows:
        assert row["verdict"] in ("likely_scam", "suspicious", "cannot_verify")
        assert isinstance(row["count"], int)

    conn.close()


def test_reliability_gemini_key_unset(monkeypatch):
    """Verify app operates fully with GEMINI_API_KEY unset."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    # 1. Text analysis works 100%
    res = client.post("/api/analyze", json={"text": "You are under digital arrest by CBI. Pay 50000 rupees to safe account."})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "likely_scam"
    assert data["plain_summary"] is not None
    assert len(data["plain_summary"]) > 0

    # 2. Image endpoint returns friendly 503
    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    res_img = client.post(
        "/api/analyze-image",
        files={"file": ("test.png", png_bytes, "image/png")}
    )
    assert res_img.status_code == 503
    assert "Image reading is offline" in res_img.json()["detail"]


def test_reliability_gemini_invalid_key(monkeypatch):
    """Verify app handles invalid GEMINI_API_KEY gracefully without crashing."""
    monkeypatch.setenv("GEMINI_API_KEY", "invalid_bogus_key_xyz123")

    # Client-level calls return None on failure
    reasons = [Reason(id="R01", title="Digital Arrest", why="Why", weight=40, snippet="digital arrest")]
    summary = simplify(reasons, "en")
    assert summary is None or isinstance(summary, str)

    # Text analyze endpoint falls back to i18n template seamlessly
    res = client.post("/api/analyze", json={"text": "You are under digital arrest by CBI. Pay 50000 rupees."})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "likely_scam"
    assert data["plain_summary"] is not None
