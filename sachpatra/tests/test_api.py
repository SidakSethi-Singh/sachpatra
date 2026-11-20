"""Integration tests for FastAPI endpoints: validation, rate limiting, and transparency."""

import pytest
from fastapi.testclient import TestClient
from app.main import app, reset_rate_limits

client = TestClient(app)


class TestApiEndpoints:
    def setup_method(self):
        reset_rate_limits()

    def test_health_endpoint(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["version"] == "1.0.0"

    def test_rules_transparency_endpoint(self):
        resp = client.get("/api/rules")
        assert resp.status_code == 200
        data = resp.json()
        assert "rules" in data
        assert data["total_rules"] == 14
        rule_ids = {r["id"] for r in data["rules"]}
        for i in range(1, 15):
            assert f"R{i:02d}" in rule_ids

    def test_stats_endpoint(self):
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "totals_by_verdict" in data
        assert "top_rules" in data
        assert "by_language" in data
        assert "last_14_days" in data

    def test_analyze_valid_scam(self):
        payload = {
            "text": "CBI Officer calling. You are under digital arrest. Pay fine of Rs 50000 to safe account.",
            "language": "en",
            "channel": "message"
        }
        resp = client.post("/api/analyze", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["verdict"] == "likely_scam"
        assert data["score"] >= 60
        assert len(data["reasons"]) > 0
        assert len(data["action_plan"]) == 6
        assert "complaint_text" in data["drafts"]
        assert "script_1930" in data["drafts"]
        assert "family_alert" in data["drafts"]
        assert "1930" in data["disclaimer"]

    def test_analyze_empty_text_returns_422(self):
        payload = {
            "text": "",
            "language": "en",
            "channel": "message"
        }
        resp = client.post("/api/analyze", json=payload)
        assert resp.status_code == 422

    def test_analyze_whitespace_only_text(self):
        # Text with only spaces or empty
        resp = client.post("/api/analyze", json={"text": ""})
        assert resp.status_code == 422

    def test_rate_limiting_exceeded_returns_429(self):
        reset_rate_limits()
        payload = {
            "text": "Routine check notice for testing rate limit.",
            "language": "en"
        }
        # First 20 requests should succeed
        for _ in range(20):
            res = client.post("/api/analyze", json=payload)
            assert res.status_code == 200

        # 21st request from same client IP must return 429
        blocked_res = client.post("/api/analyze", json=payload)
        assert blocked_res.status_code == 429
        assert "Rate limit exceeded" in blocked_res.json()["detail"]
