"""Integration tests for /api/analyze-image and multimodal processing (mocked offline)."""

import io
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app, reset_rate_limits

client = TestClient(app)


def make_valid_jpeg() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (20, 20), color="blue")
    img.save(buf, format="JPEG")
    return buf.getvalue()


def make_valid_png() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGBA", (20, 20), color="red")
    img.save(buf, format="PNG")
    return buf.getvalue()


def make_valid_webp() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (20, 20), color="green")
    img.save(buf, format="WEBP")
    return buf.getvalue()


class TestImageApiEndpoints:
    def setup_method(self):
        reset_rate_limits()

    def test_analyze_image_success(self):
        fake_extracted = {
            "text": "CBI Officer calling. You are under digital arrest. Stay on video call and pay fine to safe account.",
            "claimed_agency": "CBI",
            "sender": "Inspector Kumar",
            "links": ["http://bit.ly/cbi-order"],
            "amounts": ["50,000"],
            "doc_type": "Notice",
            "has_seal_or_signature": True
        }

        with patch("app.main.extract_from_image", return_value=fake_extracted):
            jpeg_bytes = make_valid_jpeg()
            files = {"file": ("notice.jpg", jpeg_bytes, "image/jpeg")}
            data = {"language": "en", "channel": "document"}

            resp = client.post("/api/analyze-image", files=files, data=data)
            assert resp.status_code == 200
            res = resp.json()

            assert res["verdict"] == "likely_scam"
            assert res["engine"] == "rules+gemini"
            assert res["extracted"] is not None
            assert res["extracted"]["claimed_agency"] == "CBI"
            assert res["extracted"]["has_seal_or_signature"] is True
            assert "1930" in res["disclaimer"]
            assert res["plain_summary"] != ""

    def test_analyze_image_offline_gemini_returns_503(self):
        with patch("app.main.extract_from_image", return_value=None):
            jpeg_bytes = make_valid_jpeg()
            files = {"file": ("notice.jpg", jpeg_bytes, "image/jpeg")}
            data = {"language": "en"}

            resp = client.post("/api/analyze-image", files=files, data=data)
            assert resp.status_code == 503
            assert "Image reading is offline" in resp.json()["detail"]

    def test_analyze_image_offline_gemini_returns_503_hindi(self):
        with patch("app.main.extract_from_image", return_value=None):
            png_bytes = make_valid_png()
            files = {"file": ("notice.png", png_bytes, "image/png")}
            data = {"language": "hi"}

            resp = client.post("/api/analyze-image", files=files, data=data)
            assert resp.status_code == 503
            assert "इमेज पढ़ने की सेवा अभी ऑफलाइन है" in resp.json()["detail"]

    def test_analyze_image_oversized_file_returns_413(self):
        oversized = b"X" * (5 * 1024 * 1024 + 100)
        files = {"file": ("large.jpg", oversized, "image/jpeg")}

        resp = client.post("/api/analyze-image", files=files)
        assert resp.status_code == 413
        assert "exceeds maximum allowed limit" in resp.json()["detail"]

    def test_analyze_image_wrong_extension(self):
        files = {"file": ("document.pdf", b"%PDF-1.4 sample content...", "application/pdf")}

        resp = client.post("/api/analyze-image", files=files)
        assert resp.status_code == 400
        assert "Invalid image extension" in resp.json()["detail"]

    def test_analyze_image_fake_extension(self):
        # File named photo.jpg but contains random ASCII text
        fake_content = b"This is plain text pretending to be a JPG file."
        files = {"file": ("photo.jpg", fake_content, "image/jpeg")}

        resp = client.post("/api/analyze-image", files=files)
        assert resp.status_code == 400
        assert "Magic bytes do not match" in resp.json()["detail"]

    def test_analyze_image_valid_webp(self):
        fake_extracted = {
            "text": "Cyber police notice regarding parcel seizure.",
            "claimed_agency": "Cyber Police",
            "sender": "Cyber Desk",
            "links": [],
            "amounts": [],
            "doc_type": "Notice",
            "has_seal_or_signature": False
        }
        with patch("app.main.extract_from_image", return_value=fake_extracted):
            webp_bytes = make_valid_webp()
            files = {"file": ("sample.webp", webp_bytes, "image/webp")}
            resp = client.post("/api/analyze-image", files=files)
            assert resp.status_code == 200
            assert resp.json()["engine"] == "rules+gemini"

    def test_analyze_text_includes_plain_summary(self):
        payload = {
            "text": "You are under digital arrest by CBI. Transfer money to safe account immediately.",
            "language": "en"
        }
        resp = client.post("/api/analyze", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "plain_summary" in data
        assert len(data["plain_summary"]) > 0
