"""
src/feedback/dependency_prevention.py — Session 86

Session frequency monitor. Discourages compulsive checking.
No streak mechanics. No badges. No unsolicited notifications.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import sqlite3

_DAILY_CAP = 3  # sessions per day before nudge
_WEEKLY_CAP = 15  # sessions per week before nudge


@dataclass
class DependencyStatus:
    sessions_today: int
    sessions_week: int
    show_nudge: bool
    nudge_text: str
    is_overuse: bool


def ensure_session_table(db_path: str | Path = "lagna.db") -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS session_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    TEXT NOT NULL,
            started_at TEXT DEFAULT (datetime('now')),
            domain     TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_session_user ON session_log(user_id, started_at);
        """)


def log_session(
    user_id: str, domain: str = "general", db_path: str | Path = "lagna.db"
) -> None:
    ensure_session_table(db_path)
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            "INSERT INTO session_log (user_id, domain, started_at) VALUES (?, ?, ?)",
            (user_id, domain, __import__("datetime").datetime.now().isoformat()),
        )


def check_dependency_status(
    user_id: str, db_path: str | Path = "lagna.db"
) -> DependencyStatus:
    ensure_session_table(db_path)
    today = date.today().isoformat()
    week_ago = (date.today() - __import__("datetime").timedelta(days=7)).isoformat()

    with sqlite3.connect(str(db_path)) as conn:
        # Use string prefix match so timezone offset in stored datetime doesn't matter
        today_count = conn.execute(
            """
            SELECT COUNT(*) FROM session_log
            WHERE user_id=? AND started_at LIKE ?
        """,
            (user_id, today + "%"),
        ).fetchone()[0]
        week_count = conn.execute(
            """
            SELECT COUNT(*) FROM session_log
            WHERE user_id=? AND started_at >= ?
        """,
            (user_id, week_ago),
        ).fetchone()[0]

    is_overuse = today_count >= _DAILY_CAP * 2 or week_count >= _WEEKLY_CAP * 1.5
    show_nudge = today_count >= _DAILY_CAP or week_count >= _WEEKLY_CAP

    nudge = ""
    if is_overuse:
        nudge = (
            "You're checking in very frequently. For your wellbeing, "
            "consider stepping away and returning later — guidance is most "
            "useful when combined with rest, reflection, and real-world action."
        )
    elif show_nudge:
        nudge = (
            "Guidance works best as one input among many. "
            "Your own judgment and trusted advisors are always the primary source."
        )

    return DependencyStatus(
        sessions_today=today_count,
        sessions_week=week_count,
        show_nudge=show_nudge,
        nudge_text=nudge,
        is_overuse=is_overuse,
    )
