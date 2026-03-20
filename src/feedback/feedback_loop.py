"""
src/feedback/feedback_loop.py — Session 84

Human-supervised feedback loop.
Feedback → human review queue (NEVER automated retrain).
Reproducibility lock: any guidance output is recomputable from chart + date + version.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

FEEDBACK_SCHEMA_VERSION = "1.0"


def ensure_feedback_tables(db_path: str | Path = "lagna.db") -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS feedback_events (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       TEXT NOT NULL,
            chart_id      TEXT NOT NULL,
            domain        TEXT NOT NULL,
            depth         TEXT NOT NULL DEFAULT 'L1',
            rating        TEXT NOT NULL,   -- 'helpful'|'not_helpful'|'concerning'
            on_date       TEXT NOT NULL,
            engine_version TEXT NOT NULL DEFAULT '3.0.0',
            reviewed      INTEGER DEFAULT 0,
            created_at    TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS review_queue (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id     INTEGER NOT NULL REFERENCES feedback_events(id),
            severity        TEXT NOT NULL DEFAULT 'routine',
            reviewed_by     TEXT,
            reviewed_at     TEXT,
            resolution      TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_feedback_user ON feedback_events(user_id);
        CREATE INDEX IF NOT EXISTS idx_review_unreviewed ON review_queue(reviewed_at) WHERE reviewed_at IS NULL;
        """)


@dataclass
class FeedbackRecord:
    feedback_id: int
    rating: str
    queued_for_review: bool
    reproducibility_key: str   # chart_id + date + engine_version


def record_feedback(user_id: str, chart_id: str, domain: str,
                    rating: str, on_date: str, depth: str = "L1",
                    engine_version: str = "3.0.0",
                    db_path: str | Path = "lagna.db") -> FeedbackRecord:
    """
    Record user feedback. 'concerning' → human review queue immediately.
    All ratings → output quality monitoring only (no auto-retrain).
    """
    ensure_feedback_tables(db_path)
    valid_ratings = {"helpful", "not_helpful", "concerning"}
    if rating not in valid_ratings:
        raise ValueError(f"rating must be one of {valid_ratings}")

    with sqlite3.connect(str(db_path)) as conn:
        cur = conn.execute("""
            INSERT INTO feedback_events
            (user_id, chart_id, domain, depth, rating, on_date, engine_version)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, chart_id, domain, depth, rating, on_date, engine_version))
        fid = cur.lastrowid

        queued = False
        if rating == "concerning":
            severity = "high"
            conn.execute("""
                INSERT INTO review_queue (feedback_id, severity) VALUES (?, ?)
            """, (fid, severity))
            queued = True

    repro_key = f"{chart_id}::{on_date}::{engine_version}"
    return FeedbackRecord(feedback_id=fid, rating=rating,
                           queued_for_review=queued, reproducibility_key=repro_key)


def get_quality_metrics(db_path: str | Path = "lagna.db") -> dict:
    """Output quality monitoring — never used for parameter changes."""
    ensure_feedback_tables(db_path)
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT domain, rating, COUNT(*) as n FROM feedback_events
            GROUP BY domain, rating
        """).fetchall()
        pending_review = conn.execute("""
            SELECT COUNT(*) FROM review_queue WHERE reviewed_at IS NULL
        """).fetchone()[0]

    by_domain: dict = {}
    for row in rows:
        by_domain.setdefault(row["domain"], {})[row["rating"]] = row["n"]
    return {"by_domain": by_domain, "pending_human_review": pending_review,
            "note": "Quality monitoring only. No automated model changes."}
