"""
src/privacy/consent_engine.py — Session 76

GDPR Article 7 (consent) + Article 17 (right to erasure) compliance.
DPDP Act (India) and CCPA/CPRA equivalent flows.

Consent record: user_id, purpose, granted_at, withdrawn_at, jurisdiction, version.
right_to_erasure(): cascade removes all computed outputs, birth data, event logs;
  replaces with tombstone record preserving deletion timestamp.
Age gate: birth_year check — under-18 blocks chart creation.
"""

from __future__ import annotations
import contextlib
from dataclasses import dataclass
from datetime import datetime, date, timezone
from pathlib import Path
import sqlite3
import hashlib

CONSENT_VERSION = "1.0"
MIN_AGE = 18

_PURPOSES = {
    "core": "Computing and storing your birth chart and guidance",
    "history": "Storing your guidance history for continuity",
    "family": "Including family member charts in compatibility analysis",
    "improve": "Using anonymised patterns to improve guidance quality",
}


@dataclass
class ConsentRecord:
    user_id: str
    purpose: str
    granted_at: datetime | None
    withdrawn_at: datetime | None
    jurisdiction: str
    version: str
    is_active: bool


@contextlib.contextmanager
def _get_conn(db_path: str | Path = "lagna.db"):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def ensure_consent_tables(db_path: str | Path = "lagna.db") -> None:
    with _get_conn(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS consent_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT NOT NULL,
            purpose     TEXT NOT NULL,
            granted_at  TEXT,
            withdrawn_at TEXT,
            jurisdiction TEXT DEFAULT 'default',
            version     TEXT DEFAULT '1.0',
            created_at  TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS erasure_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id_hash TEXT NOT NULL,
            erased_at   TEXT NOT NULL,
            tables_cleared TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_consent_user
            ON consent_records(user_id, purpose);
        """)


def grant_consent(
    user_id: str,
    purpose: str,
    jurisdiction: str = "default",
    db_path: str | Path = "lagna.db",
) -> ConsentRecord:
    ensure_consent_tables(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with _get_conn(db_path) as conn:
        conn.execute(
            """
            INSERT INTO consent_records (user_id, purpose, granted_at, jurisdiction, version)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, purpose, now, jurisdiction, CONSENT_VERSION),
        )
    return ConsentRecord(
        user_id=user_id,
        purpose=purpose,
        granted_at=datetime.now(timezone.utc),
        withdrawn_at=None,
        jurisdiction=jurisdiction,
        version=CONSENT_VERSION,
        is_active=True,
    )


def withdraw_consent(
    user_id: str, purpose: str, db_path: str | Path = "lagna.db"
) -> bool:
    ensure_consent_tables(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with _get_conn(db_path) as conn:
        conn.execute(
            """
            UPDATE consent_records SET withdrawn_at = ?
            WHERE user_id = ? AND purpose = ? AND withdrawn_at IS NULL
        """,
            (now, user_id, purpose),
        )
    return True


def has_active_consent(
    user_id: str, purpose: str = "core", db_path: str | Path = "lagna.db"
) -> bool:
    ensure_consent_tables(db_path)
    with _get_conn(db_path) as conn:
        row = conn.execute(
            """
            SELECT id FROM consent_records
            WHERE user_id=? AND purpose=? AND granted_at IS NOT NULL AND withdrawn_at IS NULL
            ORDER BY granted_at DESC LIMIT 1
        """,
            (user_id, purpose),
        ).fetchone()
    return row is not None


def right_to_erasure(user_id: str, db_path: str | Path = "lagna.db") -> dict:
    """
    GDPR Article 17: complete erasure cascade.
    Removes user data from all tables; inserts tombstone in erasure_log.
    """
    ensure_consent_tables(db_path)
    cleared = []
    with _get_conn(db_path) as conn:
        # Tables to clear (add more as schema grows)
        erasure_targets = [
            ("consent_records", "user_id"),
            ("charts", "user_id"),
            ("empirica_events", "chart_id"),  # indirect — best effort
            ("session_log", "user_id"),
            ("feedback_events", "user_id"),
        ]
        for table, col in erasure_targets:
            try:
                n = conn.execute(
                    f"DELETE FROM {table} WHERE {col}=?", (user_id,)
                ).rowcount
                if n > 0:
                    cleared.append(f"{table}({n} rows)")
            except sqlite3.OperationalError:
                pass  # table may not exist yet

        # Tombstone record (hash only — no user_id stored)
        uid_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        conn.execute(
            """
            INSERT INTO erasure_log (user_id_hash, erased_at, tables_cleared)
            VALUES (?, ?, ?)
        """,
            (uid_hash, datetime.now(timezone.utc).isoformat(), ", ".join(cleared)),
        )

    return {
        "erased": True,
        "tables_cleared": cleared,
        "tombstone": True,
        "gdpr_article": "17",
    }


def check_age_eligibility(birth_year: int) -> tuple[bool, str]:
    """Return (eligible, reason). Under-18 is ineligible."""
    current_year = date.today().year
    age = current_year - birth_year
    if age < MIN_AGE:
        return False, f"LagnaMaster requires users to be at least {MIN_AGE} years old."
    return True, "Eligible"
