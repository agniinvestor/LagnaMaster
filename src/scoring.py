"""
src/scoring.py
===============
Thin wrapper around multi_axis_scoring.evaluate_house_detailed().
Provides the ChartScores/HouseScore/RuleResult public API for D1 scoring.

All rule evaluation logic lives in multi_axis_scoring.py (canonical).
This module converts the raw evaluation results into the structured
output format used by the API, UI, and worker.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from src.data.constants import SIGN_LORDS
from src.ephemeris import BirthChart
from src.calculations.multi_axis_scoring import (
    evaluate_house_detailed,
    _prepare_frame_context,
    _aspects,
)


# ---------------------------------------------------------------------------
# House meta: life domain names
# ---------------------------------------------------------------------------

HOUSE_DOMAIN = {
    1: "Self & Vitality",
    2: "Wealth & Family",
    3: "Courage & Skills",
    4: "Home & Happiness",
    5: "Intellect & Children",
    6: "Challenges",
    7: "Relationships",
    8: "Transformation",
    9: "Fortune & Dharma",
    10: "Career & Status",
    11: "Gains & Income",
    12: "Liberation & Loss",
}


# ---------------------------------------------------------------------------
# Graha Drishti — re-exported for backward compatibility (tests import this)
# ---------------------------------------------------------------------------


def _planet_aspects_house(planet: str, planet_house: int, target_house: int) -> bool:
    """Return True if planet in planet_house casts a full aspect to target_house."""
    return _aspects(planet, planet_house, target_house)


# ---------------------------------------------------------------------------
# Result dataclasses (public API)
# ---------------------------------------------------------------------------


@dataclass
class RuleResult:
    rule: str
    description: str
    score: float
    is_wc: bool = False  # Worth Considering (half weight in aggregate)
    triggered: bool = False  # True if rule contributed non-zero


@dataclass
class HouseScore:
    house: int
    domain: str
    bhavesh: str  # house lord planet name
    bhavesh_house: int  # house where lord sits
    rules: list[RuleResult] = field(default_factory=list)
    raw_score: float = 0.0
    final_score: float = 0.0  # clamped to [-10, +10]
    rating: str = ""

    def _aggregate(self) -> float:
        total = 0.0
        for r in self.rules:
            contribution = r.score * (0.5 if r.is_wc else 1.0)
            total += contribution
        return total


@dataclass
class ChartScores:
    lagna_sign: str
    houses: dict[int, HouseScore] = field(default_factory=dict)

    @property
    def house_scores(self):
        """Alias for backward compatibility — returns list of HouseScore."""
        return list(self.houses.values())

    def summary(self) -> str:
        lines = [
            f"Lagna: {self.lagna_sign}",
            f"{'H':>3} {'Domain':<24} {'Score':>7} {'Rating'}",
        ]
        lines.append("-" * 55)
        for h in range(1, 13):
            hs = self.houses[h]
            lines.append(f"{h:>3} {hs.domain:<24} {hs.final_score:>7.2f} {hs.rating}")
        return "\n".join(lines)


def _rating(score: float) -> str:
    if score >= 6:
        return "Excellent"
    if score >= 3:
        return "Strong"
    if score >= 0:
        return "Moderate"
    if score >= -3:
        return "Weak"
    return "Very Weak"


# ---------------------------------------------------------------------------
# Main scoring entry point — delegates to multi_axis_scoring
# ---------------------------------------------------------------------------


def score_chart(chart: BirthChart, query_date=None) -> ChartScores:
    """
    Apply BPHS rules across all 12 houses using functional benefic/malefic
    classification. Returns ChartScores with per-house and per-rule breakdown.

    All rule evaluation is performed by evaluate_house_detailed() in
    multi_axis_scoring.py — this function wraps the output.
    """
    lagna_si = chart.lagna_sign_index
    school = "parashari"

    yogakaraka, dusthana_lords, kendra_lords, trikona_lords, is_fb, is_fm, av_bindus = \
        _prepare_frame_context(chart, lagna_si, school)

    result = ChartScores(lagna_sign=chart.lagna_sign)

    for house in range(1, 13):
        house_si = (lagna_si + house - 1) % 12
        bhavesh = SIGN_LORDS[house_si]
        bhavesh_house = (chart.planets[bhavesh].sign_index - lagna_si) % 12 + 1 if bhavesh in chart.planets else house

        final_score, rule_tuples = evaluate_house_detailed(
            house, lagna_si, chart, school,
            av_bindus, yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
            is_fb, is_fm,
        )

        rules = [
            RuleResult(
                rule=name,
                description=desc,
                score=score,
                is_wc=is_wc,
                triggered=triggered,
            )
            for name, desc, score, is_wc, triggered in rule_tuples
        ]

        raw = sum(r.score * (0.5 if r.is_wc else 1.0) for r in rules)

        result.houses[house] = HouseScore(
            house=house,
            domain=HOUSE_DOMAIN[house],
            bhavesh=bhavesh,
            bhavesh_house=bhavesh_house,
            rules=rules,
            raw_score=raw,
            final_score=final_score,
            rating=_rating(final_score),
        )

    return result
