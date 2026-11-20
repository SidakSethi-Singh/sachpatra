"""Privacy-preserving statistics store using SQLite.
Stores COUNTERS ONLY (date, verdict, rule_ids, language).
Never stores notice text, user IP, or any PII.
"""

import datetime
import os
import sqlite3
from typing import Any, Dict, List, Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "stats.db")


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = db_path or os.getenv("STATS_DB_PATH", DEFAULT_DB_PATH)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_verdicts (
                date TEXT NOT NULL,
                verdict TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (date, verdict)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_rules (
                date TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (date, rule_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_languages (
                date TEXT NOT NULL,
                language TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (date, language)
            )
        """)
    conn.close()


def record_stat(
    verdict: str,
    rule_ids: List[str],
    language: str,
    date_str: Optional[str] = None,
    db_path: Optional[str] = None
) -> None:
    """Increment counters for verdict, fired rule IDs, and language for the given date.
    Strictly records aggregate counts only; no request text or IP is ever retained.
    """
    target_date = date_str or datetime.date.today().isoformat()
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO daily_verdicts (date, verdict, count)
                VALUES (?, ?, 1)
                ON CONFLICT(date, verdict) DO UPDATE SET count = count + 1
                """,
                (target_date, verdict)
            )
            conn.execute(
                """
                INSERT INTO daily_languages (date, language, count)
                VALUES (?, ?, 1)
                ON CONFLICT(date, language) DO UPDATE SET count = count + 1
                """,
                (target_date, language)
            )
            for r_id in rule_ids:
                conn.execute(
                    """
                    INSERT INTO daily_rules (date, rule_id, count)
                    VALUES (?, ?, 1)
                    ON CONFLICT(date, rule_id) DO UPDATE SET count = count + 1
                    """,
                    (target_date, r_id)
                )
    finally:
        conn.close()


def get_stats(days: int = 14, db_path: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve aggregated stats: totals by verdict, top rule IDs, language counts,
    and daily breakdown over the last N days.
    """
    init_db(db_path)
    start_date = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    conn = get_db_connection(db_path)
    try:
        # 1. Totals by verdict
        cur = conn.execute(
            "SELECT verdict, SUM(count) as total FROM daily_verdicts GROUP BY verdict"
        )
        totals_by_verdict = {row["verdict"]: row["total"] for row in cur.fetchall()}

        # 2. Top rule IDs
        cur = conn.execute(
            "SELECT rule_id, SUM(count) as total FROM daily_rules GROUP BY rule_id ORDER BY total DESC LIMIT 10"
        )
        top_rules = [{"rule_id": row["rule_id"], "count": row["total"]} for row in cur.fetchall()]

        # 3. Totals by language
        cur = conn.execute(
            "SELECT language, SUM(count) as total FROM daily_languages GROUP BY language"
        )
        by_language = {row["language"]: row["total"] for row in cur.fetchall()}

        # 4. Last N days timeline
        cur = conn.execute(
            """
            SELECT date, verdict, count FROM daily_verdicts
            WHERE date >= ?
            ORDER BY date ASC
            """,
            (start_date,)
        )
        daily_map: Dict[str, Dict[str, Any]] = {}
        for row in cur.fetchall():
            d = row["date"]
            if d not in daily_map:
                daily_map[d] = {"date": d, "total": 0, "likely_scam": 0, "suspicious": 0, "cannot_verify": 0}
            daily_map[d][row["verdict"]] = row["count"]
            daily_map[d]["total"] += row["count"]

        last_14_days = sorted(daily_map.values(), key=lambda x: x["date"])

        total_scans = sum(totals_by_verdict.values())

        return {
            "total_scans": total_scans,
            "totals_by_verdict": totals_by_verdict,
            "top_rules": top_rules,
            "by_language": by_language,
            "last_14_days": last_14_days
        }
    finally:
        conn.close()
