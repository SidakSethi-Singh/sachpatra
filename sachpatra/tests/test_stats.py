"""Tests for privacy-preserving SQLite statistics storage."""

import os
import sqlite3
import tempfile
import pytest
from app.stats import get_stats, init_db, record_stat


class TestStatsPrivacy:
    @pytest.fixture
    def temp_db(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        init_db(path)
        yield path
        if os.path.exists(path):
            os.remove(path)

    def test_schema_contains_no_pii_or_text_columns(self, temp_db):
        conn = sqlite3.connect(temp_db)
        cur = conn.cursor()
        tables = ["daily_verdicts", "daily_rules", "daily_languages"]
        forbidden_columns = {"text", "message", "body", "ip", "client_ip", "user", "phone", "image", "content"}

        for t in tables:
            cur.execute(f"PRAGMA table_info({t})")
            columns = [row[1].lower() for row in cur.fetchall()]
            for col in columns:
                assert col not in forbidden_columns, f"Forbidden column {col} in table {t}"
        conn.close()

    def test_counters_increment_correctly(self, temp_db):
        record_stat("likely_scam", ["R01", "R03", "R05"], "en", date_str="2026-11-20", db_path=temp_db)
        record_stat("likely_scam", ["R01"], "en", date_str="2026-11-20", db_path=temp_db)
        record_stat("cannot_verify", [], "hi", date_str="2026-11-20", db_path=temp_db)

        stats = get_stats(days=7, db_path=temp_db)
        assert stats["total_scans"] == 3
        assert stats["totals_by_verdict"]["likely_scam"] == 2
        assert stats["totals_by_verdict"]["cannot_verify"] == 1
        assert stats["by_language"]["en"] == 2
        assert stats["by_language"]["hi"] == 1

        top_rules = {r["rule_id"]: r["count"] for r in stats["top_rules"]}
        assert top_rules["R01"] == 2
        assert top_rules["R03"] == 1
        assert top_rules["R05"] == 1
