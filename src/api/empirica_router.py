"""src/api/empirica_router.py — REST endpoints for empirical validation."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/empirica", tags=["empirica"])

class EventIn(BaseModel):
    chart_id: str
    event_date: str
    event_type: str
    house_primary: int
    event_description: str = ""
    house_secondary: int | None = None
    manifested: int = 1
    confidence: int = 2
    notes: str = ""
    active_mahadasha: str = ""
    active_antardasha: str = ""
    d1_score_at_event: float = 0.0
    yoga_score: float = 0.0
    r04_fired: int = 0
    r15_fired: int = 0
    r02_fired: int = 0
    r09_fired: int = 0

@router.post("/events", status_code=201)
def create_event(body: EventIn):
    from src.calculations.empirica import EmpiricalEvent, record_event, init_empirica_db
    init_empirica_db()
    evt = EmpiricalEvent(**body.model_dump())
    eid = record_event(evt)
    return {"event_id": eid}

@router.get("/events/{chart_id}")
def list_events(chart_id: str):
    from src.calculations.empirica import get_events, init_empirica_db
    init_empirica_db()
    return get_events(chart_id)

@router.get("/accuracy")
def get_accuracy():
    from src.calculations.empirica import compute_accuracy, init_empirica_db
    init_empirica_db()
    r = compute_accuracy()
    return {
        "total_events": r.total_events,
        "manifested_count": r.manifested_count,
        "base_rate": r.base_rate,
        "rule_accuracies": [vars(x) for x in r.rule_accuracies],
        "by_house": r.by_house,
        "by_event_type": r.by_event_type,
        "by_mahadasha": r.by_mahadasha,
    }
