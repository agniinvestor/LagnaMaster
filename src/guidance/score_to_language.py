"""
src/guidance/score_to_language.py — Session 71

Transforms all numerical engine output into human-safe guidance language.
Raw scores NEVER pass through to consumers at L1 or L2.

5-tier signal system (mobile-signal style — no percentages, no stars):
  5 bars  ●●●●●  ≥ +3.0   Clear passage
  4 bars  ●●●●○  +1.5–+3  Favourable
  3 bars  ●●●○○  +0.5–+1.5  Mixed — lean in
  2 bars  ●●○○○  −0.5–+0.5  Neutral
  1 bar   ●○○○○  −1.5–−0.5  Navigate carefully
  0 bars  ○○○○○  ≤ −1.5   Significant resistance
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SignalLevel:
    bars: int  # 0–5
    timing_label: str
    l1_template: str  # single guidance sentence
    guidance_tone: str  # for downstream fatalism filter


_TIERS = [
    (
        3.0,
        5,
        "Clear passage",
        "Strong foundations support action in this area.",
        "affirming",
    ),
    (
        1.5,
        4,
        "Favourable",
        "Conditions are generally supportive of your efforts here.",
        "encouraging",
    ),
    (
        0.5,
        3,
        "Mixed — lean in",
        "Some supporting factors are present; preparation will help.",
        "balanced",
    ),
    (
        -0.5,
        2,
        "Neutral",
        "Signals are mixed. Neither strongly supported nor obstructed.",
        "neutral",
    ),
    (
        -1.5,
        1,
        "Navigate carefully",
        "Some friction is present. Patience tends to work better than urgency.",
        "cautious",
    ),
]
_FLOOR = (
    None,
    0,
    "Significant resistance",
    "This area carries meaningful challenges. Building your foundation is wiser than forcing outcomes.",
    "grounded",
)


def score_to_signal(score: float) -> SignalLevel:
    """Map a raw engine score to a consumer SignalLevel."""
    for threshold, bars, label, template, tone in _TIERS:
        if score >= threshold:
            return SignalLevel(
                bars=bars, timing_label=label, l1_template=template, guidance_tone=tone
            )
    _, bars, label, template, tone = _FLOOR
    return SignalLevel(
        bars=bars, timing_label=label, l1_template=template, guidance_tone=tone
    )


def signal_bars_display(bars: int) -> str:
    """Visual representation of signal bars."""
    return "●" * bars + "○" * (5 - bars)


def domain_l1_sentence(
    score: float,
    domain: str,
    promise_strength: str = "Moderate",
    timing: str = "Future",
) -> str:
    """
    Compose a domain-specific L1 guidance sentence.
    Merges signal level with domain context and promise/timing awareness.
    """
    sig = score_to_signal(score)
    base = sig.l1_template

    # Promise-aware modifier
    if promise_strength in ("Absent", "Negated") and timing == "Blocked":
        base = "This area may benefit more from foundation-building than active pursuit right now."
    elif timing == "Now" and sig.bars >= 4:
        base = base.rstrip(".") + ", and timing is particularly supportive now."
    elif timing == "Soon" and sig.bars >= 3:
        base = base.rstrip(".") + "; conditions are building toward activation."

    return base


def format_confidence_indicator(confidence_label: str) -> str:
    """Map engine confidence label to consumer-friendly indicator."""
    return {
        "High": "Signal is consistent across multiple chart layers.",
        "Moderate": "Signals are reasonably consistent with some variation.",
        "Low": "Signals are mixed across chart layers — personal reflection is valuable.",
        "Uncertain": "Interpretation is uncertain in this area; consider a practitioner.",
    }.get(confidence_label, "Confidence data unavailable.")
