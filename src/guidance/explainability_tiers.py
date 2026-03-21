"""
src/guidance/explainability_tiers.py — Session 73

Three-tier explainability. Each tier is gated by user depth choice.

L1 (default, always shown):
  Single guidance sentence + signal bar + timing label + confidence indicator.
  No scores, no planet names in primary sentence (unless very natural).

L2 (on "Why?" click):
  3–5 factor bullets. Planet names and timing triggers allowed.
  No raw scores, no Shadbala components, no AV rekhas.

L3 (explicit opt-in modal, resets each session):
  Full technical trace: Shadbala, AV rekhas, rule firings, raw scores,
  LPI breakdown. Clearly labelled "Advanced technical view".
"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class L1Content:
    heading: str
    signal_bars: int
    signal_display: str
    timing_label: str
    summary: str
    confidence_indicator: str


@dataclass
class L2Content:
    factors: list[str]
    timing_note: str
    domain_context: str


@dataclass
class L3Content:
    raw_d1_score: float
    lpi_breakdown: dict
    dominant_factors: list[str]
    rule_firings: list[str]
    shadbala_note: str
    av_note: str
    confidence_components: dict
    disclaimer: str = "Advanced technical view — for practitioners and advanced students."


@dataclass
class GuidanceContent:
    domain: str
    l1: L1Content
    l2: L2Content | None = None
    l3: L3Content | None = None
    depth_requested: str = "L1"


def build_l1(domain: str, score: float, promise_strength: str,
             timing: str, confidence_label: str) -> L1Content:
    from src.guidance.score_to_language import (
        score_to_signal, signal_bars_display,
        domain_l1_sentence, format_confidence_indicator,
    )
    sig = score_to_signal(score)
    summary = domain_l1_sentence(score, domain, promise_strength, timing)
    heading = f"{domain.replace('_', ' ').title()} — {sig.timing_label}"
    return L1Content(
        heading=heading,
        signal_bars=sig.bars,
        signal_display=signal_bars_display(sig.bars),
        timing_label=sig.timing_label,
        summary=summary,
        confidence_indicator=format_confidence_indicator(confidence_label),
    )


def build_l2(domain: str, score: float, dominant_theme: str,
             active_dasha: str, dasha_activated: bool,
             transit_supported: bool, promise_strength: str) -> L2Content:
    """Compose human-readable factor bullets for L2."""
    from src.guidance.fatalism_filter import filter_output
    factors = []

    # Dasha factor
    if dasha_activated and active_dasha:
        factors.append(
            f"{active_dasha} period activates {domain.replace('_', ' ')} themes — "
            "this timing is significant for this area."
        )

    # Promise factor
    _promise_map = {
        "Strong":   f"Your chart holds strong potential in the {domain.replace('_', ' ')} area.",
        "Moderate": "Your chart holds moderate potential here — conditions can support progress.",
        "Weak":     "The natal foundation here is modest — steady effort matters more than timing.",
        "Absent":   "The natal chart does not hold strong promise here — reflection over action is wise.",
        "Negated":  "This area carries inherent challenges — patience and foundation-building are favoured.",
    }
    if promise_strength in _promise_map:
        factors.append(_promise_map[promise_strength])

    # Transit factor
    if transit_supported:
        factors.append("Current planetary transits add supportive energy to this area.")
    elif dasha_activated and not transit_supported:
        factors.append("Period is active but transit support is limited — action is possible but patience helps.")

    # Domain theme
    if dominant_theme:
        factors.append(filter_output(dominant_theme))

    if not factors:
        factors.append(f"Multiple chart layers were evaluated for {domain.replace('_', ' ')}.")

    timing_note = {
        "Now":    "Timing is particularly supportive — the next 4–8 weeks are activated.",
        "Soon":   "Timing is building — conditions should clarify over the next 1–3 months.",
        "Future": "This area is not strongly activated now — future periods will be more significant.",
        "Blocked":"The natal chart limits delivery here regardless of timing — foundation work is the path.",
    }.get(promise_strength, "Timing signals are mixed.")

    domain_ctx = {
        "career":          "Career and public role are seen through the 10th house and D10 chart.",
        "marriage":        "Partnership themes are seen through the 7th house, D9, and Upapada Lagna.",
        "wealth":          "Wealth potential is seen through the 2nd and 11th houses and planetary strength.",
        "health_longevity":"Vitality is seen through the 1st and 8th houses and the Lagna lord.",
        "mind_psychology": "Mental and emotional themes are seen through Moon and the Chandra Lagna axis.",
        "spirituality":    "Dharmic and spiritual themes are seen through the 9th house and D9 chart.",
        "children":        "Children and creative intelligence are seen through the 5th house.",
    }.get(domain, f"The {domain} domain was evaluated across multiple chart layers.")

    return L2Content(factors=factors, timing_note=timing_note, domain_context=domain_ctx)


def build_l3(score: float, lpi_data: dict, rules_fired: list[str],
             confidence_data: dict, shadbala_summary: str = "",
             av_summary: str = "") -> L3Content:
    """Compose full technical trace for L3 (opt-in only)."""
    return L3Content(
        raw_d1_score=round(score, 3),
        lpi_breakdown=lpi_data,
        dominant_factors=rules_fired[:5],
        rule_firings=rules_fired,
        shadbala_note=shadbala_summary or "Shadbala data from engine.",
        av_note=av_summary or "Ashtakavarga data from engine.",
        confidence_components=confidence_data,
    )


def explain(domain: str, score: float, depth: str = "L1",
            promise_strength: str = "Moderate", timing: str = "Future",
            confidence_label: str = "Moderate", active_dasha: str = "",
            dasha_activated: bool = False, transit_supported: bool = False,
            dominant_theme: str = "", lpi_data: dict | None = None,
            rules_fired: list[str] | None = None,
            confidence_data: dict | None = None) -> GuidanceContent:
    """Build full GuidanceContent at the requested depth."""
    l1 = build_l1(domain, score, promise_strength, timing, confidence_label)
    l2 = None
    l3 = None

    if depth in ("L2", "L3"):
        l2 = build_l2(domain, score, dominant_theme, active_dasha,
                      dasha_activated, transit_supported, promise_strength)

    if depth == "L3":
        l3 = build_l3(score, lpi_data or {}, rules_fired or [],
                      confidence_data or {})

    return GuidanceContent(domain=domain, l1=l1, l2=l2, l3=l3,
                            depth_requested=depth)
