"""
src/calculations/confidence_model.py
Birth time uncertainty propagation — confidence intervals for chart scores.
Session 158 (Audit OB-5).

Every chart interpretation carries implicit uncertainty from:
  - Birth time uncertainty (±5 minutes typical)
  - Ayanamsha uncertainty (±0.3°)
  - Nakshatra boundary sensitivity

Sources:
  Swiss Ephemeris Manual §2.3 (Moon parallax, precision)
  Hart de Fouw & Robert Svoboda · Light on Life, App on Research
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UncertaintyFlags:
    """Flags that affect the reliability of chart interpretations."""
    # Lagna uncertainty
    lagna_near_sign_boundary: bool = False     # Lagna within 1° of sign cusp
    lagna_boundary_margin_deg: float = 0.0     # degrees from nearest cusp

    # Moon uncertainty
    moon_near_nakshatra_cusp: bool = False     # Moon within 0.5° of nak boundary
    moon_boundary_margin_deg: float = 0.0     # degrees from nearest nak cusp

    # Dasha uncertainty
    dasha_lord_uncertain: bool = False         # Moon too close to nakshatra boundary

    # Ayanamsha sensitivity
    sign_boundary_planets: list[str] = field(default_factory=list)  # planets within 1° of sign cusp

    @property
    def any_flag(self) -> bool:
        return (self.lagna_near_sign_boundary or
                self.moon_near_nakshatra_cusp or
                self.dasha_lord_uncertain or
                bool(self.sign_boundary_planets))

    @property
    def severity(self) -> str:
        flags_set = sum([self.lagna_near_sign_boundary, self.moon_near_nakshatra_cusp,
                         self.dasha_lord_uncertain])
        if flags_set >= 2: return "high"
        if flags_set == 1: return "moderate"
        return "low"


@dataclass
class ConfidenceInterval:
    """Confidence interval for a single house score."""
    house: int
    point_estimate: float
    lower_bound: float
    upper_bound: float
    confidence_pct: float      # 0-100
    uncertainty_sources: list[str]
    is_reliable: bool          # True if interval width < 2.0

    @property
    def interval_width(self) -> float:
        return self.upper_bound - self.lower_bound


@dataclass
class ChartConfidenceReport:
    """Full confidence analysis for a chart."""
    uncertainty_flags: UncertaintyFlags
    house_intervals: list[ConfidenceInterval]
    overall_reliability: str    # "high"/"moderate"/"low"
    recommendations: list[str]

    def interval_for_house(self, house: int) -> Optional[ConfidenceInterval]:
        return next((ci for ci in self.house_intervals if ci.house == house), None)


def _lagna_boundary_margin(lagna_lon: float) -> float:
    """Degrees from nearest sign boundary (0 = on boundary, 30 = center)."""
    deg_in_sign = lagna_lon % 30
    return min(deg_in_sign, 30 - deg_in_sign)


def _moon_nak_boundary_margin(moon_lon: float) -> float:
    """Degrees from nearest nakshatra boundary."""
    nak_width = 40.0 / 3.0  # 13.333...°
    deg_in_nak = moon_lon % nak_width
    return min(deg_in_nak, nak_width - deg_in_nak)


def compute_uncertainty_flags(chart) -> UncertaintyFlags:
    """
    Compute uncertainty flags for a chart.

    Birth time ±5 min → Lagna moves ±1.25° (1° per 4 minutes for avg rising time)
    Ayanamsha ±0.3° → affects all sign/nakshatra boundaries
    """
    flags = UncertaintyFlags()

    # Lagna boundary check
    lagna_lon = chart.lagna
    margin = _lagna_boundary_margin(lagna_lon)
    flags.lagna_boundary_margin_deg = round(margin, 3)
    # ±5 min birth time → ±1.25° Lagna movement (rough estimate)
    if margin < 1.5:
        flags.lagna_near_sign_boundary = True

    # Moon boundary check
    if "Moon" in chart.planets:
        moon_lon = chart.planets["Moon"].longitude
        moon_margin = _moon_nak_boundary_margin(moon_lon)
        flags.moon_boundary_margin_deg = round(moon_margin, 3)
        # Ayanamsha ±0.3° + topocentric ~0.5° = total ~0.8° uncertainty
        if moon_margin < 1.0:
            flags.moon_near_nakshatra_cusp = True
            flags.dasha_lord_uncertain = True

    # Sign-boundary planets
    for p, pd in chart.planets.items():
        deg_in_sign = pd.longitude % 30
        if deg_in_sign < 1.0 or deg_in_sign >= 29.0:
            flags.sign_boundary_planets.append(p)

    return flags


def compute_confidence_intervals(
    base_scores: dict[int, float],
    flags: UncertaintyFlags,
    birth_time_uncertainty_minutes: float = 5.0,
) -> list[ConfidenceInterval]:
    """
    Compute confidence intervals for house scores given birth time uncertainty.

    The interval width increases when:
    - Lagna is near a sign boundary (house assignments may change)
    - Moon is near nakshatra boundary (dasha lord may change)
    - Multiple planets are near sign boundaries
    """
    intervals = []
    base_uncertainty = birth_time_uncertainty_minutes / 5.0  # normalized

    for house in range(1, 13):
        score = base_scores.get(house, 0.0)
        sources = []
        extra_uncertainty = 0.0

        if flags.lagna_near_sign_boundary:
            extra_uncertainty += 1.5 * base_uncertainty
            sources.append(f"lagna_near_sign_boundary ({flags.lagna_boundary_margin_deg:.1f}° margin)")

        if flags.dasha_lord_uncertain:
            extra_uncertainty += 0.5 * base_uncertainty
            sources.append(f"moon_near_nakshatra_cusp ({flags.moon_boundary_margin_deg:.1f}° margin)")

        if len(flags.sign_boundary_planets) > 0 and any(
            p in ["Sun","Moon","Mars","Jupiter","Saturn"]
            for p in flags.sign_boundary_planets
        ):
            extra_uncertainty += 0.3
            sources.append(f"planets_near_sign_boundary: {flags.sign_boundary_planets[:3]}")

        half_width = 0.3 + extra_uncertainty
        lower = round(max(-10.0, score - half_width), 3)
        upper = round(min(+10.0, score + half_width), 3)
        conf_pct = max(30.0, 95.0 - extra_uncertainty * 20)

        intervals.append(ConfidenceInterval(
            house=house,
            point_estimate=round(score, 3),
            lower_bound=lower,
            upper_bound=upper,
            confidence_pct=round(conf_pct, 1),
            uncertainty_sources=sources,
            is_reliable=(upper - lower) < 2.0,
        ))

    return intervals


def compute_chart_confidence(
    chart,
    base_scores: dict[int, float],
    birth_time_uncertainty_minutes: float = 5.0,
) -> ChartConfidenceReport:
    """
    Full confidence analysis for a chart.

    Source: Hart de Fouw & Robert Svoboda · Light on Life, App on Research
    """
    flags = compute_uncertainty_flags(chart)
    intervals = compute_confidence_intervals(base_scores, flags, birth_time_uncertainty_minutes)

    # Overall reliability
    if not flags.any_flag:
        reliability = "high"
        recs = ["Birth time appears reliable. Chart scores have high confidence."]
    elif flags.severity == "moderate":
        reliability = "moderate"
        recs = []
        if flags.lagna_near_sign_boundary:
            recs.append(
                f"Lagna is {flags.lagna_boundary_margin_deg:.1f}° from sign boundary — "
                "birth time should be verified to within 2 minutes for reliable Lagna."
            )
        if flags.moon_near_nakshatra_cusp:
            recs.append(
                f"Moon is {flags.moon_boundary_margin_deg:.1f}° from nakshatra boundary — "
                "Vimshottari Dasha starting lord may be uncertain. Consider topocentric correction."
            )
    else:
        reliability = "low"
        recs = ["Multiple uncertainty flags — verify birth time precisely before prediction."]

    if flags.sign_boundary_planets:
        recs.append(f"Planets near sign boundary: {', '.join(flags.sign_boundary_planets)} — "
                    "sign dignity may differ by ±0.3° ayanamsha variation.")

    return ChartConfidenceReport(
        uncertainty_flags=flags,
        house_intervals=intervals,
        overall_reliability=reliability,
        recommendations=recs,
    )


from dataclasses import dataclass as _dc
from typing import Dict as _Dict

@_dc
class HouseConfidence:
    house: int
    overall_confidence: float   # 0.0-1.0
    confidence_label: str       # 'High'/'Moderate'/'Low'/'Uncertain'

class ChartConfidenceReport2:
    def __init__(self, houses, global_confidence, most_reliable_houses,
                 uncertainty_flags=None, recommendations=None):
        self.houses = houses                          # dict {int: HouseConfidence}
        self.global_confidence = global_confidence    # float 0-1
        self.most_reliable_houses = most_reliable_houses  # list of 3 ints

def compute_confidence(chart, birth_time_uncertainty_minutes: float = 5.0):
    flags = compute_uncertainty_flags(chart)
    base = {h: 0.0 for h in range(1, 13)}
    intervals = compute_confidence_intervals(base, flags, birth_time_uncertainty_minutes)

    houses = {}
    for ci in intervals:
        conf = max(0.0, min(1.0, ci.confidence_pct / 100.0))
        if conf >= 0.8:   label = "High"
        elif conf >= 0.6: label = "Moderate"
        elif conf >= 0.4: label = "Low"
        else:              label = "Uncertain"
        houses[ci.house] = HouseConfidence(ci.house, round(conf, 3), label)

    global_conf = round(sum(h.overall_confidence for h in houses.values()) / 12, 3)
    top3 = sorted(houses.values(), key=lambda h: h.overall_confidence, reverse=True)[:3]
    most_reliable = [h.house for h in top3]

    return ChartConfidenceReport2(houses=houses, global_confidence=global_conf,
                                   most_reliable_houses=most_reliable)
