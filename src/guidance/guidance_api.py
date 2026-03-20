"""
src/guidance/guidance_api.py — Session 74

Single consumer-facing contract for all guidance requests.
All engine calls are internal. Raw scores never in L1/L2 response schema.

POST /guidance → GuidanceResponse
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date


@dataclass
class GuidanceResponse:
    """Consumer-facing guidance response — no raw scores at L1/L2."""
    domain: str
    heading: str
    summary: str                  # L1 sentence
    signal_bars: int              # 0–5
    signal_display: str           # ●●●○○
    timing_label: str
    confidence_label: str
    confidence_note: str
    disclaimer: str
    # L2 (populated only if depth="L2" or "L3")
    factors: list[str] = field(default_factory=list)
    timing_note: str = ""
    domain_context: str = ""
    # L3 (populated only if depth="L3" and user has opted in)
    technical_detail: dict = field(default_factory=dict)
    depth_returned: str = "L1"


def get_guidance(
    chart,
    domain: str = "default",
    depth: str = "L1",
    on_date: date | None = None,
    dashas=None,
    school: str = "parashari",
    l3_opted_in: bool = False,
) -> GuidanceResponse:
    """
    Primary consumer-facing function. Assembles full GuidanceResponse.
    depth: "L1" | "L2" | "L3" (L3 requires l3_opted_in=True)
    """
    if on_date is None:
        on_date = date.today()
    if depth == "L3" and not l3_opted_in:
        depth = "L2"  # silently downgrade if not opted in

    # ── Engine calls ──────────────────────────────────────────────────────────
    try:
        from src.calculations.domain_weighting import compute_domain_lpi
        dlpi = compute_domain_lpi(chart, dashas, on_date, domain)
        primary_h = dlpi.primary_house or 1
        score = dlpi.house_scores.get(primary_h, 0.0)
    except Exception:
        score = 0.0

    try:
        from src.calculations.promise_engine import compute_house_promise
        primary_h_use = primary_h if 'primary_h' in dir() else 1
        promise = compute_house_promise(chart, primary_h_use)
        promise_strength = promise.promise_strength
        timing = "Future"
    except Exception:
        promise_strength = "Moderate"
        timing = "Future"

    try:
        from src.calculations.promise_engine import compute_full_promise
        full_promise = compute_full_promise(chart, dashas, on_date)
        ph = primary_h_use if 'primary_h_use' in dir() else 1
        mr = full_promise.get(ph)
        if mr:
            timing = mr.manifestation_timing
    except Exception:
        pass

    try:
        from src.calculations.confidence_model import compute_confidence
        conf = compute_confidence(chart)
        ph2 = primary_h_use if 'primary_h_use' in dir() else 1
        hc = conf.houses.get(ph2)
        confidence_label = hc.confidence_label if hc else "Moderate"
    except Exception:
        confidence_label = "Moderate"

    try:
        from src.calculations.dominance_engine import dominant_theme as dom_theme
        dom = dom_theme(chart, dashas, on_date)
    except Exception:
        dom = ""

    active_dasha = ""
    dasha_activated = False
    if dashas:
        try:
            from src.calculations.vimshottari_dasa import current_dasha
            md, _ = current_dasha(dashas, on_date)
            active_dasha = md.lord
            dasha_activated = True
        except Exception:
            pass

    # ── Build content ─────────────────────────────────────────────────────────
    from src.guidance.explainability_tiers import explain
    from src.guidance.fatalism_filter import filter_output
    from src.guidance.disclaimer_engine import get_disclaimer

    content = explain(
        domain=domain, score=score, depth=depth,
        promise_strength=promise_strength, timing=timing,
        confidence_label=confidence_label, active_dasha=active_dasha,
        dasha_activated=dasha_activated, dominant_theme=dom,
    )

    # ── Apply fatalism filter to all text ─────────────────────────────────────
    summary = filter_output(content.l1.summary)
    factors = [filter_output(f) for f in (content.l2.factors if content.l2 else [])]
    timing_note = filter_output(content.l2.timing_note if content.l2 else "")

    # ── Technical detail (L3 only) ────────────────────────────────────────────
    technical = {}
    if depth == "L3" and content.l3:
        technical = {
            "raw_d1_score": content.l3.raw_d1_score,
            "lpi_breakdown": content.l3.lpi_breakdown,
            "rule_firings": content.l3.rule_firings,
            "confidence_components": content.l3.confidence_components,
            "disclaimer": content.l3.disclaimer,
        }

    from src.guidance.score_to_language import signal_bars_display
    from src.calculations.score_to_language import score_to_signal  # noqa

    from src.guidance.score_to_language import score_to_signal as sts
    sig = sts(score)

    return GuidanceResponse(
        domain=domain,
        heading=content.l1.heading,
        summary=summary,
        signal_bars=content.l1.signal_bars,
        signal_display=content.l1.signal_display,
        timing_label=content.l1.timing_label,
        confidence_label=confidence_label,
        confidence_note=content.l1.confidence_indicator,
        disclaimer=get_disclaimer(domain),
        factors=factors,
        timing_note=timing_note,
        domain_context=content.l2.domain_context if content.l2 else "",
        technical_detail=technical,
        depth_returned=depth,
    )
