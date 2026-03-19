"""
src/db.py
==========
SQLite database setup and helpers for chart persistence.
Immutable insert pattern: charts are never updated, only appended.
"""

from __future__ import annotations
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "charts.db"


_SENTINEL = object()


def _resolve(path) -> Path:
    """Return path, defaulting to the current DB_PATH module variable."""
    return DB_PATH if path is _SENTINEL else path


def _conn(path=_SENTINEL) -> sqlite3.Connection:
    p = _resolve(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def get_db(path=_SENTINEL):
    conn = _conn(path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(path=_SENTINEL) -> None:
    """Create tables if they don't exist."""
    with get_db(_resolve(path)) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS charts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at  TEXT    NOT NULL,
                name        TEXT,
                year        INTEGER NOT NULL,
                month       INTEGER NOT NULL,
                day         INTEGER NOT NULL,
                hour        REAL    NOT NULL,
                lat         REAL    NOT NULL,
                lon         REAL    NOT NULL,
                tz_offset   REAL    NOT NULL DEFAULT 5.5,
                ayanamsha   TEXT    NOT NULL DEFAULT 'lahiri',
                -- Computed fields (JSON blobs)
                chart_json  TEXT    NOT NULL,
                scores_json TEXT
            );

            CREATE TABLE IF NOT EXISTS score_runs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chart_id    INTEGER NOT NULL REFERENCES charts(id),
                run_at      TEXT    NOT NULL,
                scores_json TEXT    NOT NULL
            );
        """)


def save_chart(
    year: int, month: int, day: int,
    hour: float, lat: float, lon: float,
    tz_offset: float, ayanamsha: str,
    chart_json: dict,
    scores_json: dict | None = None,
    name: str | None = None,
    path=_SENTINEL,
) -> int:
    """Insert a new chart record. Returns the new chart id."""
    with get_db(_resolve(path)) as conn:
        cur = conn.execute(
            """INSERT INTO charts
               (created_at, name, year, month, day, hour, lat, lon,
                tz_offset, ayanamsha, chart_json, scores_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                datetime.now(timezone.utc).isoformat(),
                name,
                year, month, day, hour, lat, lon,
                tz_offset, ayanamsha,
                json.dumps(chart_json),
                json.dumps(scores_json) if scores_json else None,
            ),
        )
        return cur.lastrowid


def get_chart(chart_id: int, path=_SENTINEL) -> dict | None:
    with get_db(_resolve(path)) as conn:
        row = conn.execute(
            "SELECT * FROM charts WHERE id = ?", (chart_id,)
        ).fetchone()
        if row is None:
            return None
        d = dict(row)
        d["chart_json"]  = json.loads(d["chart_json"])
        d["scores_json"] = json.loads(d["scores_json"]) if d["scores_json"] else None
        return d


def list_charts(limit: int = 50, path=_SENTINEL) -> list[dict]:
    with get_db(_resolve(path)) as conn:
        rows = conn.execute(
            "SELECT id, created_at, name, year, month, day, hour, lat, lon "
            "FROM charts ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
