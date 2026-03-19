"""
src/db_pg.py — LagnaMaster Session 20
PostgreSQL persistence layer using psycopg2 (sync) with an immutable insert
pattern that mirrors src/db.py (SQLite).  Activated when PG_DSN env-var is set;
falls back to SQLite seamlessly so existing tests keep passing unmodified.

Environment variables
---------------------
PG_DSN        PostgreSQL DSN, e.g.
              postgresql://lagnamaster:secret@localhost:5432/lagnamaster
              If absent the SQLite layer (src/db.py) is used automatically.

PG_POOL_MIN   Minimum connections in pool  (default 1)
PG_POOL_MAX   Maximum connections in pool  (default 10)

Public API (mirrors src/db.py exactly)
---------------------------------------
    init_db()                           → None
    save_chart(...) → int               chart id
    get_chart(chart_id) → dict | None
    list_charts(limit=50) → list[dict]
    health_check() → dict               {"backend": "postgres"|"sqlite", "ok": bool}
"""

from __future__ import annotations

import json
import os
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator, Optional

# ── optional psycopg2 import ───────────────────────────────────────────────────
try:
    import psycopg2
    import psycopg2.pool
    import psycopg2.extras

    _PG_AVAILABLE = True
except ImportError:
    _PG_AVAILABLE = False


# ── SQLite fallback ────────────────────────────────────────────────────────────
import src.db as _sqlite_db

# ── module state ───────────────────────────────────────────────────────────────
_pool: Optional["psycopg2.pool.ThreadedConnectionPool"] = None
_pool_lock = threading.Lock()
_USE_PG: bool = False  # resolved in _ensure_pool()


# ──────────────────────────────────────────────────────────────────────────────
# Internal pool helpers
# ──────────────────────────────────────────────────────────────────────────────

def _ensure_pool() -> bool:
    """Return True if PostgreSQL pool is available, False → use SQLite."""
    global _pool, _USE_PG

    dsn = os.environ.get("PG_DSN", "")
    if not dsn or not _PG_AVAILABLE:
        _USE_PG = False
        return False

    with _pool_lock:
        if _pool is None:
            min_conn = int(os.environ.get("PG_POOL_MIN", "1"))
            max_conn = int(os.environ.get("PG_POOL_MAX", "10"))
            _pool = psycopg2.pool.ThreadedConnectionPool(
                min_conn,
                max_conn,
                dsn=dsn,
                cursor_factory=psycopg2.extras.RealDictCursor,
            )
        _USE_PG = True
    return True


@contextmanager
def _conn() -> Iterator["psycopg2.extensions.connection"]:
    """Yield a connection from the pool; return it on exit."""
    if _pool is None:
        raise RuntimeError("PostgreSQL pool not initialised — call init_db() first")
    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)


# ──────────────────────────────────────────────────────────────────────────────
# DDL
# ──────────────────────────────────────────────────────────────────────────────

_DDL = """
CREATE TABLE IF NOT EXISTS charts (
    id          SERIAL PRIMARY KEY,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    name        TEXT,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    hour        DOUBLE PRECISION NOT NULL,
    lat         DOUBLE PRECISION NOT NULL,
    lon         DOUBLE PRECISION NOT NULL,
    tz_offset   DOUBLE PRECISION NOT NULL DEFAULT 5.5,
    ayanamsha   TEXT NOT NULL DEFAULT 'lahiri',
    chart_json  JSONB NOT NULL,
    scores_json JSONB
);

CREATE TABLE IF NOT EXISTS score_runs (
    id          SERIAL PRIMARY KEY,
    chart_id    INTEGER NOT NULL REFERENCES charts(id),
    run_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    scores_json JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_charts_created ON charts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_charts_name    ON charts(name)
    WHERE name IS NOT NULL;
"""


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def init_db() -> None:
    """Initialise whichever backend is configured.

    PostgreSQL: creates tables + indexes if they don't exist.
    SQLite:     delegates to src.db.init_db().
    """
    if _ensure_pool():
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(_DDL)
    else:
        _sqlite_db.init_db()


def save_chart(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float,
    ayanamsha: str,
    chart_json: str,
    scores_json: Optional[str] = None,
    name: Optional[str] = None,
) -> int:
    """Insert a new chart row (immutable). Returns the new chart id."""
    if _USE_PG:
        chart_data = json.loads(chart_json)
        scores_data = json.loads(scores_json) if scores_json else None
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO charts
                        (name, year, month, day, hour, lat, lon,
                         tz_offset, ayanamsha, chart_json, scores_json)
                    VALUES
                        (%(name)s, %(year)s, %(month)s, %(day)s, %(hour)s,
                         %(lat)s, %(lon)s, %(tz_offset)s, %(ayanamsha)s,
                         %(chart_json)s, %(scores_json)s)
                    RETURNING id
                    """,
                    {
                        "name": name,
                        "year": year,
                        "month": month,
                        "day": day,
                        "hour": hour,
                        "lat": lat,
                        "lon": lon,
                        "tz_offset": tz_offset,
                        "ayanamsha": ayanamsha,
                        "chart_json": json.dumps(chart_data),
                        "scores_json": json.dumps(scores_data) if scores_data else None,
                    },
                )
                row = cur.fetchone()
                return row["id"]
    else:
        return _sqlite_db.save_chart(
            year, month, day, hour, lat, lon,
            tz_offset, ayanamsha, chart_json, scores_json, name,
        )


def get_chart(chart_id: int) -> Optional[dict]:
    """Retrieve a single chart by id. Returns None if not found."""
    if _USE_PG:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM charts WHERE id = %s", (chart_id,)
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return _pg_row_to_dict(row)
    else:
        return _sqlite_db.get_chart(chart_id)


def list_charts(limit: int = 50) -> list[dict]:
    """Return the most recent *limit* charts ordered newest-first."""
    if _USE_PG:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM charts ORDER BY created_at DESC LIMIT %s",
                    (limit,),
                )
                return [_pg_row_to_dict(r) for r in cur.fetchall()]
    else:
        return _sqlite_db.list_charts(limit)


def health_check() -> dict:
    """Return backend name and connectivity status."""
    if _USE_PG:
        try:
            with _conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
            return {"backend": "postgres", "ok": True}
        except Exception as exc:
            return {"backend": "postgres", "ok": False, "error": str(exc)}
    else:
        try:
            _sqlite_db.list_charts(limit=1)
            return {"backend": "sqlite", "ok": True}
        except Exception as exc:
            return {"backend": "sqlite", "ok": False, "error": str(exc)}


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _pg_row_to_dict(row: dict) -> dict:
    """Normalise a psycopg2 RealDictRow to a plain dict matching SQLite shape."""
    d = dict(row)
    # Serialise JSONB columns back to strings so callers see identical types
    if isinstance(d.get("chart_json"), dict):
        d["chart_json"] = json.dumps(d["chart_json"])
    if isinstance(d.get("scores_json"), dict):
        d["scores_json"] = json.dumps(d["scores_json"])
    # Normalise timestamps
    if isinstance(d.get("created_at"), datetime):
        d["created_at"] = d["created_at"].astimezone(timezone.utc).isoformat()
    return d
