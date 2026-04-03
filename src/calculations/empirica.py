"""
src/calculations/empirica.py — Session 48

Empirical event log and validation engine (REF_EmpiricaSchema).
Records birth-chart events and computes per-rule accuracy metrics.

Schema (from REF_EmpiricaSchema):
  event_id, chart_id, event_date, event_type, event_description,
  house_primary, house_secondary, d1_score_at_event, active_mahadasha,
  active_antardasha, manifested (0/1), confidence (1-3),
  r04_fired, r15_fired, r02_fired, r09_fired, yoga_score

Public API
----------
  init_empirica_db(path)
  record_event(event, path) -> str (event_id)
  get_events(chart_id, path) -> list[dict]
  compute_accuracy(path)    -> AccuracyReport
"""

from __future__ import annotations
import contextlib
from dataclasses import dataclass, field, asdict
import sqlite3
import uuid
from pathlib import Path

_EVENT_TYPES = {
    "Career",
    "Marriage",
    "Divorce",
    "Health_Crisis",
    "Finance",
    "Travel",
    "Loss",
    "Education",
    "Other",
}

_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS empirica_events (
    event_id        TEXT PRIMARY KEY,
    chart_id        TEXT NOT NULL,
    event_date      TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    event_description TEXT,
    house_primary   INTEGER,
    house_secondary INTEGER,
    d1_score_at_event REAL,
    active_mahadasha TEXT,
    active_antardasha TEXT,
    manifested      INTEGER DEFAULT 1,
    confidence      INTEGER DEFAULT 2,
    notes           TEXT,
    r04_fired       INTEGER DEFAULT 0,
    r15_fired       INTEGER DEFAULT 0,
    r02_fired       INTEGER DEFAULT 0,
    r09_fired       INTEGER DEFAULT 0,
    yoga_score      REAL DEFAULT 0.0,
    created_at      TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_empirica_chart ON empirica_events(chart_id);
CREATE INDEX IF NOT EXISTS idx_empirica_type ON empirica_events(event_type);
CREATE INDEX IF NOT EXISTS idx_empirica_house ON empirica_events(house_primary);
"""


@dataclass
class EmpiricalEvent:
    chart_id: str
    event_date: str  # ISO date string
    event_type: str
    house_primary: int
    event_description: str = ""
    house_secondary: int | None = None
    d1_score_at_event: float = 0.0
    active_mahadasha: str = ""
    active_antardasha: str = ""
    manifested: int = 1
    confidence: int = 2  # 1=low, 2=moderate, 3=high
    notes: str = ""
    r04_fired: int = 0
    r15_fired: int = 0
    r02_fired: int = 0
    r09_fired: int = 0
    yoga_score: float = 0.0
    event_id: str = field(default_factory=lambda: f"EVT_{uuid.uuid4().hex[:8].upper()}")


@contextlib.contextmanager
def _get_conn(path: str | Path):
    p = Path(str(path))
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_empirica_db(path: str | Path = "data/empirica.db") -> None:
    with _get_conn(path) as conn:
        conn.executescript(_CREATE_SQL)


def record_event(event: EmpiricalEvent, path: str | Path = "data/empirica.db") -> str:
    """Insert an event record. Returns event_id."""
    if event.event_type not in _EVENT_TYPES:
        event.event_type = "Other"
    d = asdict(event)
    cols = ", ".join(d.keys())
    placeholders = ", ".join("?" * len(d))
    with _get_conn(path) as conn:
        conn.execute(
            f"INSERT OR REPLACE INTO empirica_events ({cols}) VALUES ({placeholders})",
            list(d.values()),
        )
    return event.event_id


def get_events(chart_id: str, path: str | Path = "data/empirica.db") -> list[dict]:
    """Retrieve all events for a chart."""
    try:
        with _get_conn(path) as conn:
            rows = conn.execute(
                "SELECT * FROM empirica_events WHERE chart_id=? ORDER BY event_date",
                (chart_id,),
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []


@dataclass
class RuleAccuracy:
    rule: str
    total_events: int
    fired_count: int
    manifested_when_fired: int
    accuracy: float  # manifested / fired
    lift: float  # accuracy vs base rate


@dataclass
class AccuracyReport:
    total_events: int
    manifested_count: int
    base_rate: float
    rule_accuracies: list[RuleAccuracy]
    by_house: dict[int, float]  # house → accuracy
    by_event_type: dict[str, float]
    by_mahadasha: dict[str, float]


def compute_accuracy(path: str | Path = "data/empirica.db") -> AccuracyReport:
    """Compute per-rule accuracy from the event log."""
    try:
        with _get_conn(path) as conn:
            all_events = [
                dict(r)
                for r in conn.execute("SELECT * FROM empirica_events").fetchall()
            ]
    except Exception:
        return AccuracyReport(0, 0, 0.5, [], {}, {}, {})

    if not all_events:
        return AccuracyReport(0, 0, 0.5, [], {}, {}, {})

    total = len(all_events)
    manifested = sum(1 for e in all_events if e.get("manifested", 0) == 1)
    base_rate = manifested / total if total > 0 else 0.5

    # Per-rule accuracy
    rule_accs = []
    for rule_col in ["r04_fired", "r15_fired", "r02_fired", "r09_fired"]:
        fired = [e for e in all_events if e.get(rule_col, 0) == 1]
        if not fired:
            continue
        mwf = sum(1 for e in fired if e.get("manifested", 0) == 1)
        acc = mwf / len(fired)
        rule_accs.append(
            RuleAccuracy(
                rule=rule_col.replace("_fired", "").upper(),
                total_events=total,
                fired_count=len(fired),
                manifested_when_fired=mwf,
                accuracy=round(acc, 3),
                lift=round(acc / base_rate, 2) if base_rate > 0 else 1.0,
            )
        )

    # By house
    by_house: dict[int, list] = {}
    for e in all_events:
        h = e.get("house_primary", 0)
        by_house.setdefault(h, []).append(e.get("manifested", 0))
    house_acc = {h: round(sum(v) / len(v), 3) for h, v in by_house.items() if v}

    # By event type
    by_type: dict[str, list] = {}
    for e in all_events:
        t = e.get("event_type", "Other")
        by_type.setdefault(t, []).append(e.get("manifested", 0))
    type_acc = {t: round(sum(v) / len(v), 3) for t, v in by_type.items() if v}

    # By Mahadasha
    by_md: dict[str, list] = {}
    for e in all_events:
        md = e.get("active_mahadasha", "")
        if md:
            by_md.setdefault(md, []).append(e.get("manifested", 0))
    md_acc = {md: round(sum(v) / len(v), 3) for md, v in by_md.items() if v}

    return AccuracyReport(
        total_events=total,
        manifested_count=manifested,
        base_rate=round(base_rate, 3),
        rule_accuracies=rule_accs,
        by_house=house_acc,
        by_event_type=type_acc,
        by_mahadasha=md_acc,
    )
