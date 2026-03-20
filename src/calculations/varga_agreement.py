"""
src/calculations/varga_agreement.py — Session 56

Varga agreement flag (CALC_CompositeVargaScore col I).
Determines whether D1, D9, and D10 house scores point in the same direction.

Agreement flags:
  ★★  "All 3 agree" — D1/D9/D10 all positive or all negative
  ★   "D1+D9 agree" — D1 and D9 agree, D10 diverges
  ○   "Diverge"     — D1 and D9 disagree

Confidence modifier on LPI:
  ★★  → High confidence
  ★   → Moderate confidence
  ○   → Low confidence (nuanced interpretation needed)

Public API
----------
  compute_varga_agreement(chart, school) -> VargaAgreementReport
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HouseAgreement:
    house: int
    d1_score: float
    d9_score: float
    d10_score: float
    flag: str          # "★★" / "★" / "○"
    confidence: str    # "High" / "Moderate" / "Low"
    interpretation: str


@dataclass
class VargaAgreementReport:
    houses: dict[int, HouseAgreement]
    high_confidence_houses: list[int]
    low_confidence_houses: list[int]

    def confidence_for(self, house: int) -> str:
        ha = self.houses.get(house)
        return ha.confidence if ha else "Moderate"

    def flag_for(self, house: int) -> str:
        ha = self.houses.get(house)
        return ha.flag if ha else "○"


def _sign(x: float) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)


def compute_varga_agreement(chart, school: str = "parashari") -> VargaAgreementReport:
    """
    Compute per-house D1/D9/D10 agreement flag.
    Uses multi_axis_scoring to get all 3 axis scores.
    """
    from src.calculations.multi_axis_scoring import score_all_axes
    try:
        axes = score_all_axes(chart, school)
    except Exception:
        # Fallback: all diverge
        houses = {h: HouseAgreement(h, 0, 0, 0, "○", "Low", "Score unavailable")
                  for h in range(1, 13)}
        return VargaAgreementReport(houses=houses,
                                     high_confidence_houses=[],
                                     low_confidence_houses=list(range(1,13)))

    d1  = axes.d1.scores   if axes.d1  else {}
    d9  = axes.d9.scores   if axes.d9  else {}
    d10 = axes.d10.scores  if axes.d10 else {}

    houses = {}
    high_conf = []
    low_conf  = []

    for h in range(1, 13):
        s1  = d1.get(h, 0.0)
        s9  = d9.get(h, 0.0)
        s10 = d10.get(h, 0.0)

        sg1, sg9, sg10 = _sign(s1), _sign(s9), _sign(s10)

        if sg1 != 0 and sg1 == sg9 == sg10:
            flag, conf = "★★", "High"
            direction = "positive" if s1 > 0 else "negative"
            interp = f"All 3 vargas agree — {direction} across D1/D9/D10"
            high_conf.append(h)
        elif sg1 != 0 and sg1 == sg9:
            flag, conf = "★", "Moderate"
            interp = "D1+D9 agree; D10 diverges — nuanced"
        else:
            flag, conf = "○", "Low"
            interp = "Vargas diverge — D1 physical reality may differ from dharmic/career axis"
            if sg1 == 0 or sg9 == 0:
                interp = "One axis is neutral — insufficient agreement data"
            low_conf.append(h)

        houses[h] = HouseAgreement(house=h, d1_score=s1, d9_score=s9, d10_score=s10,
                                    flag=flag, confidence=conf, interpretation=interp)

    return VargaAgreementReport(houses=houses,
                                 high_confidence_houses=high_conf,
                                 low_confidence_houses=low_conf)
