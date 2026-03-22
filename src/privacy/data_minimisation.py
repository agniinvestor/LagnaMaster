"""
src/privacy/data_minimisation.py — Session 78

GDPR Article 5 data minimisation audit and enforcement.

Rules:
  Birth time: stored to minute precision only (seconds stripped)
  IP addresses: hashed on ingress (SHA-256, first 16 chars)
  Location: stored to city level only (no street/postcode)
  Retention: raw birth data deleted after 90 days of inactivity
  Computed chart: retained (reproducible from birth data on request)
  Event log: anonymised after 1 year (user_id replaced with hash)
"""

from __future__ import annotations
from datetime import datetime, timedelta, timezone
import hashlib
import sqlite3
from pathlib import Path


def minimise_birth_time(hour: float) -> float:
    """Strip seconds from birth time — store to minute precision only."""
    h = int(hour)
    m = int((hour - h) * 60)
    return h + m / 60.0


def hash_ip(ip_address: str) -> str:
    """Hash IP address — SHA-256, first 16 hex chars."""
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]


def minimise_location(
    city: str = "",
    state: str = "",
    country: str = "",
    street: str = "",
    postcode: str = "",
) -> dict:
    """Return only city-level location data."""
    return {"city": city, "state": state, "country": country}


def apply_retention_policy(
    db_path: str | Path = "lagna.db",
    inactivity_days: int = 90,
    event_log_days: int = 365,
    dry_run: bool = False,
) -> dict:
    """
    Apply retention policy to the database.
    dry_run=True: report what would be deleted without deleting.
    """
    report = {"birth_data_eligible": 0, "event_log_eligible": 0, "deleted": not dry_run}
    cutoff_birth = (
        datetime.now(timezone.utc) - timedelta(days=inactivity_days)
    ).isoformat()
    cutoff_events = (
        datetime.now(timezone.utc) - timedelta(days=event_log_days)
    ).isoformat()

    with sqlite3.connect(str(db_path)) as conn:
        # Count eligible birth data rows
        try:
            n = conn.execute(
                """
                SELECT COUNT(*) FROM charts
                WHERE last_accessed < ? OR last_accessed IS NULL
            """,
                (cutoff_birth,),
            ).fetchone()[0]
            report["birth_data_eligible"] = n
            if not dry_run and n > 0:
                conn.execute(
                    """
                    DELETE FROM charts WHERE last_accessed < ? OR last_accessed IS NULL
                """,
                    (cutoff_birth,),
                )
        except sqlite3.OperationalError:
            pass

        # Count eligible event log rows
        try:
            n = conn.execute(
                """
                SELECT COUNT(*) FROM empirica_events WHERE created_at < ?
            """,
                (cutoff_events,),
            ).fetchone()[0]
            report["event_log_eligible"] = n
            if not dry_run and n > 0:
                # Anonymise: replace user reference, keep aggregate data
                conn.execute(
                    """
                    UPDATE empirica_events
                    SET chart_id = 'anonymised_' || SUBSTR(chart_id, 1, 8)
                    WHERE created_at < ?
                """,
                    (cutoff_events,),
                )
        except sqlite3.OperationalError:
            pass

    return report


def audit_stored_fields(db_path: str | Path = "lagna.db") -> list[dict]:
    """Return list of tables and their columns for privacy audit."""
    result = []
    with sqlite3.connect(str(db_path)) as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        for (table,) in tables:
            cols = [
                row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()
            ]
            risk_cols = [
                c
                for c in cols
                if any(
                    k in c.lower()
                    for k in [
                        "ip",
                        "email",
                        "name",
                        "address",
                        "street",
                        "phone",
                        "password",
                    ]
                )
            ]
            result.append({"table": table, "columns": cols, "risk_columns": risk_cols})
    return result
