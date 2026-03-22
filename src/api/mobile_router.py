"""
src/api/mobile_router.py — Session 90

Lightweight FastAPI router for mobile companion.
Push notifications only for user-scheduled timing alerts (never unsolicited).
No notification streak mechanics. No engagement loops.
"""

from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mobile", tags=["mobile"])


class TimingAlertRequest(BaseModel):
    chart_id: str
    domain: str
    alert_date: str  # ISO date string
    user_timezone: str = "UTC"


class TimingAlertResponse(BaseModel):
    alert_id: str
    domain: str
    alert_date: str
    heading: str
    summary: str
    signal_bars: int
    timing_label: str
    disclaimer: str


class GuidanceSummaryResponse(BaseModel):
    """Lightweight guidance for mobile — L1 only by default."""

    domain: str
    heading: str
    summary: str
    signal_bars: int
    signal_display: str
    timing_label: str
    confidence_label: str
    disclaimer: str


@router.get("/guidance/{chart_id}/{domain}", response_model=GuidanceSummaryResponse)
async def mobile_guidance(chart_id: str, domain: str):
    """
    Lightweight mobile guidance endpoint — L1 only.
    Raw scores never returned. No push without explicit user scheduling.
    """
    from src.guidance.score_to_language import score_to_signal, signal_bars_display
    from src.guidance.disclaimer_engine import get_disclaimer

    # Simplified mobile response (full engine call in production)
    sig = score_to_signal(0.0)  # replace with real score from chart
    return GuidanceSummaryResponse(
        domain=domain,
        heading=f"{domain.title()} — {sig.timing_label}",
        summary=sig.l1_template,
        signal_bars=sig.bars,
        signal_display=signal_bars_display(sig.bars),
        timing_label=sig.timing_label,
        confidence_label="Moderate",
        disclaimer=get_disclaimer(domain),
    )


@router.post("/alerts/schedule", response_model=TimingAlertResponse)
async def schedule_timing_alert(req: TimingAlertRequest):
    """
    Schedule a user-requested timing alert.
    Only user-initiated. Never system-pushed without explicit opt-in.
    """
    import uuid
    from src.guidance.score_to_language import score_to_signal
    from src.guidance.disclaimer_engine import get_disclaimer

    sig = score_to_signal(0.0)  # replace with real score
    return TimingAlertResponse(
        alert_id=str(uuid.uuid4()),
        domain=req.domain,
        alert_date=req.alert_date,
        heading=f"{req.domain.title()} — {sig.timing_label}",
        summary=sig.l1_template,
        signal_bars=sig.bars,
        timing_label=sig.timing_label,
        disclaimer=get_disclaimer(req.domain),
    )
