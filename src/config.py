"""
src/config.py — LagnaMaster Session 26
School gate configuration: per-user calculation school preferences.

Supported schools
-----------------
  parashari   BPHS Parashari (default, always available)
  kp          Krishnamurti Paddhati (sub-lord system)
  jaimini     Jaimini (chara dasha, chara karakas)

Feature flags (environment variables)
--------------------------------------
  ENABLE_KP      "1" to activate KP endpoints (default "1")
  ENABLE_JAIMINI "1" to activate Jaimini endpoints (default "1")

Per-user preference is stored in the users.db `school` column.
Default school for all users: "parashari".

Public API
----------
    get_user_school(user_id, path=_SENTINEL) -> str
    set_user_school(user_id, school, path=_SENTINEL) -> None
    is_school_enabled(school) -> bool
    SUPPORTED_SCHOOLS: frozenset[str]
    school_gate(school)  -> FastAPI dependency (raises 403 if disabled)
"""

from __future__ import annotations

import os
import sqlite3

import src.auth as _auth

# ── constants ─────────────────────────────────────────────────────────────────
SUPPORTED_SCHOOLS: frozenset[str] = frozenset({"parashari", "kp", "jaimini"})
DEFAULT_SCHOOL = "parashari"

_SCHOOL_FLAGS = {
    "parashari": True,  # always on
    "kp": os.environ.get("ENABLE_KP", "1") == "1",
    "jaimini": os.environ.get("ENABLE_JAIMINI", "1") == "1",
}


def is_school_enabled(school: str) -> bool:
    """Return True if the given school is active via feature flag."""
    if school not in SUPPORTED_SCHOOLS:
        raise ValueError(f"Unknown school '{school}'. Supported: {SUPPORTED_SCHOOLS}")
    return _SCHOOL_FLAGS.get(school, False)


# ── DB migration helper (adds school column to existing users table) ───────────


def _ensure_school_column(path) -> None:
    """Add `school` column to users table if it does not exist yet."""
    db = _auth._db_path(path)
    with sqlite3.connect(db) as conn:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(users)")]
        if "school" not in cols:
            conn.execute(
                f"ALTER TABLE users ADD COLUMN school TEXT NOT NULL DEFAULT '{DEFAULT_SCHOOL}'"
            )


# ── public API ────────────────────────────────────────────────────────────────


def get_user_school(user_id: int, path=_auth._SENTINEL) -> str:
    """Return the calculation school preference for *user_id*."""
    _ensure_school_column(path)
    with _auth._connect(path) as conn:
        row = conn.execute(
            "SELECT school FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if row is None:
        raise ValueError(f"User {user_id} not found")
    return row["school"] or DEFAULT_SCHOOL


def set_user_school(user_id: int, school: str, path=_auth._SENTINEL) -> None:
    """Set the calculation school preference for *user_id*."""
    if school not in SUPPORTED_SCHOOLS:
        raise ValueError(f"Unknown school '{school}'. Supported: {SUPPORTED_SCHOOLS}")
    if not is_school_enabled(school):
        raise ValueError(f"School '{school}' is disabled on this server")
    _ensure_school_column(path)
    with _auth._connect(path) as conn:
        conn.execute("UPDATE users SET school = ? WHERE id = ?", (school, user_id))


# ── FastAPI dependency ────────────────────────────────────────────────────────


def school_gate(school: str):
    """Return a FastAPI dependency that 403s if *school* is disabled.

    Usage:
        @router.get("/kp/significators", dependencies=[Depends(school_gate("kp"))])
        def kp_endpoint(...): ...
    """
    from fastapi import HTTPException

    def _check():
        if not is_school_enabled(school):
            raise HTTPException(
                status_code=403,
                detail=f"School '{school}' is not enabled on this server. "
                f"Set ENABLE_{school.upper()}=1 to activate.",
            )

    return _check
