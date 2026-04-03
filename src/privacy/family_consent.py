"""
src/privacy/family_consent.py — Session 77

Per-person consent gate for family charts.
Each family member is a separate consent principal.
Non-consenting members excluded from all cross-chart analysis.
Kundali Milan (compatibility) requires active consent from both individuals.
"""

from __future__ import annotations
import contextlib
from dataclasses import dataclass
from datetime import datetime, timezone
import sqlite3
from pathlib import Path


@contextlib.contextmanager
def _db(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


@dataclass
class FamilyMember:
    member_id: str
    owner_user_id: str
    relationship: str  # "spouse", "parent", "child", "sibling", "other"
    has_consented: bool
    consent_granted_at: datetime | None
    consent_withdrawn_at: datetime | None


def ensure_family_tables(db_path: str | Path = "lagna.db") -> None:
    with _db(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS family_members (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id             TEXT NOT NULL UNIQUE,
            owner_user_id         TEXT NOT NULL,
            relationship          TEXT NOT NULL DEFAULT 'other',
            consent_granted_at    TEXT,
            consent_withdrawn_at  TEXT,
            created_at            TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_family_owner
            ON family_members(owner_user_id);
        """)


def add_family_member(
    owner_user_id: str,
    member_id: str,
    relationship: str = "other",
    has_consented: bool = False,
    db_path: str | Path = "lagna.db",
) -> FamilyMember:
    ensure_family_tables(db_path)
    now = datetime.now(timezone.utc).isoformat() if has_consented else None
    with _db(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO family_members
            (member_id, owner_user_id, relationship, consent_granted_at)
            VALUES (?, ?, ?, ?)
        """,
            (member_id, owner_user_id, relationship, now),
        )
    return FamilyMember(
        member_id=member_id,
        owner_user_id=owner_user_id,
        relationship=relationship,
        has_consented=has_consented,
        consent_granted_at=datetime.now(timezone.utc) if has_consented else None,
        consent_withdrawn_at=None,
    )


def grant_family_consent(member_id: str, db_path: str | Path = "lagna.db") -> bool:
    ensure_family_tables(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with _db(db_path) as conn:
        conn.execute(
            """
            UPDATE family_members SET consent_granted_at=?, consent_withdrawn_at=NULL
            WHERE member_id=?
        """,
            (now, member_id),
        )
    return True


def revoke_family_consent(member_id: str, db_path: str | Path = "lagna.db") -> bool:
    ensure_family_tables(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with _db(db_path) as conn:
        conn.execute(
            """
            UPDATE family_members SET consent_withdrawn_at=? WHERE member_id=?
        """,
            (now, member_id),
        )
    return True


def delete_family_member(member_id: str, db_path: str | Path = "lagna.db") -> bool:
    ensure_family_tables(db_path)
    with _db(db_path) as conn:
        conn.execute("DELETE FROM family_members WHERE member_id=?", (member_id,))
    return True


def has_family_consent(member_id: str, db_path: str | Path = "lagna.db") -> bool:
    ensure_family_tables(db_path)
    with _db(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT * FROM family_members
            WHERE member_id=? AND consent_granted_at IS NOT NULL
            AND consent_withdrawn_at IS NULL
        """,
            (member_id,),
        ).fetchone()
    return row is not None


def can_run_compatibility(
    user_id: str, member_id: str, db_path: str | Path = "lagna.db"
) -> tuple[bool, str]:
    """
    Kundali Milan requires active consent from both individuals.
    Returns (allowed, reason).
    """
    from src.privacy.consent_engine import has_active_consent, ensure_consent_tables

    ensure_consent_tables(db_path)
    user_ok = has_active_consent(user_id, "core", db_path)
    member_ok = has_family_consent(member_id, db_path)
    if not user_ok:
        return False, "Primary user has not granted consent."
    if not member_ok:
        return False, f"Family member {member_id} has not consented to chart analysis."
    return True, "Both parties have consented."


def get_consenting_members(
    owner_user_id: str, db_path: str | Path = "lagna.db"
) -> list[FamilyMember]:
    ensure_family_tables(db_path)
    with _db(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT * FROM family_members WHERE owner_user_id=?
            AND consent_granted_at IS NOT NULL AND consent_withdrawn_at IS NULL
        """,
            (owner_user_id,),
        ).fetchall()
    return [
        FamilyMember(
            member_id=r["member_id"],
            owner_user_id=r["owner_user_id"],
            relationship=r["relationship"],
            has_consented=True,
            consent_granted_at=r["consent_granted_at"],
            consent_withdrawn_at=None,
        )
        for r in rows
    ]
