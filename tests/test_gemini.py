"""Tests for the optional Gemini multimodal and simplification layer (mocked offline)."""

import io
import os
from unittest.mock import MagicMock, patch
import pytest
from PIL import Image

from app.gemini import extract_from_image, simplify
from app.schemas import Reason


def create_sample_jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (10, 10), color="white")
    img.save(buf, format="JPEG")
    return buf.getvalue()


class TestGeminiLayer:
    def test_no_key_returns_none_immediately(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "")
        # Even with real bytes, must return None immediately
        res = extract_from_image(create_sample_jpeg_bytes(), "image/jpeg")
        assert res is None

        res_simp = simplify([Reason(id="R01", title="T", why="W", weight=40, snippet="S")], "en")
        assert res_simp is None

    def test_extract_from_image_success(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-mock")

        mock_resp = MagicMock()
        mock_resp.text = (
            '{"text": "CBI Digital Arrest Warrant", '
            '"claimed_agency": "CBI", '
            '"sender": "Officer Rao", '
            '"links": ["http://bit.ly/cbi-warrant"], '
            '"amounts": ["50,000"], '
            '"doc_type": "Warrant", '
            '"has_seal_or_signature": true}'
        )

        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.models.generate_content.return_value = mock_resp

            result = extract_from_image(create_sample_jpeg_bytes(), "image/jpeg")
            assert result is not None
            assert result["claimed_agency"] == "CBI"
            assert result["has_seal_or_signature"] is True
            assert "http://bit.ly/cbi-warrant" in result["links"]

    def test_extract_from_image_timeout(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-mock")

        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.models.generate_content.side_effect = TimeoutError("Simulated API timeout")

            result = extract_from_image(create_sample_jpeg_bytes(), "image/jpeg")
            assert result is None

    def test_extract_from_image_malformed_json(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-mock")

        mock_resp = MagicMock()
        mock_resp.text = "This is not valid JSON at all!"

        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.models.generate_content.return_value = mock_resp

            result = extract_from_image(create_sample_jpeg_bytes(), "image/jpeg")
            assert result is None

    def test_simplify_success(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "test-key-mock")

        mock_resp = MagicMock()
        mock_resp.text = (
            "Please be calm and disconnect the call right now. Real police officers never arrest "
            "anyone over video calls or ask for money into private accounts. Call helpline 1930 immediately."
        )

        with patch("google.genai.Client") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value = mock_client
            mock_client.models.generate_content.return_value = mock_resp

            reasons = [
                Reason(id="R01", title="Digital Arrest", why="No legal basis", weight=40, snippet="digital arrest"),
                Reason(id="R05", title="Payment", why="Safe account transfer", weight=30, snippet="pay fine")
            ]
            summary = simplify(reasons, "en")
            assert summary is not None
            assert len(summary.split()) <= 60
            assert "1930" in summary
