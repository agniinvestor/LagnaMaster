"""
src/calculations/lagnesh_strength.py — Session 51

Lagnesh (ascendant lord) global strength modifier.
Applied to all 12 house scores in SCORE_AllHouses.

9-condition table (CALC_LagneshStrength):
  Kendra/Trikon + Exalt   → +0.75
  Kendra/Trikon only       → +0.50
  Kendra/Trikon + Debil   → +0.25
  Neutral (no flags)       →  0.00
  Neutral + Exalt          → +0.25
  Neutral + Debil          → −0.25
  Dukshthan + Exalt        → −0.25
  Dukshthan only           → −0.50
  Dukshthan + Debil        → −0.75

India 1947: Venus (Lagnesh) in H3 (neutral), neutral dignity → 0.00 ✓
"""

from __future__ import annotations
from src.data.constants import DUSTHANA_HOUSES, KENDRA_HOUSES, SIGN_LORDS, TRIKONA_HOUSES
from dataclasses import dataclass

from src.calculations.dignity import EXALT_SIGN as _EXALT_SI, DEBIL_SIGN as _DEBIL_SI


@dataclass
class LagneshStrengthResult:
    lagnesh: str
    house: int
    dignity: str
    modifier: float
    condition: str

    def description(self) -> str:
        return (
            f"Lagnesh {self.lagnesh} in H{self.house} "
            f"({self.dignity}) — modifier {self.modifier:+.2f} applied to all 12 houses"
        )


def compute_lagnesh_strength(chart) -> LagneshStrengthResult:
    """Compute the Lagnesh global modifier."""
    lagna_si = chart.lagna_sign_index
    lagnesh = SIGN_LORDS[lagna_si % 12]

    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    house = hmap.planet_house.get(lagnesh, 1)

    # Dignity of Lagnesh in D1
    pos = chart.planets.get(lagnesh)
    dignity = "Neutral"
    if pos:
        si = pos.sign_index
        if _EXALT_SI.get(lagnesh) == si:
            dignity = "Exaltation"
        elif _DEBIL_SI.get(lagnesh) == si:
            dignity = "Debilitation"

    in_kendra = house in KENDRA_HOUSES
    in_trikona = house in TRIKONA_HOUSES
    in_strong = in_kendra or in_trikona
    in_dush = house in DUSTHANA_HOUSES
    is_exalt = dignity == "Exaltation"
    is_debil = dignity == "Debilitation"

    if in_strong and is_exalt:
        modifier, condition = +0.75, "Kendra/Trikona + Exaltation"
    elif in_strong and is_debil:
        modifier, condition = +0.25, "Kendra/Trikona + Debilitation"
    elif in_strong:
        modifier, condition = +0.50, "Kendra/Trikona"
    elif in_dush and is_exalt:
        modifier, condition = -0.25, "Dukshthan + Exaltation"
    elif in_dush and is_debil:
        modifier, condition = -0.75, "Dukshthan + Debilitation"
    elif in_dush:
        modifier, condition = -0.50, "Dukshthan"
    elif is_exalt:
        modifier, condition = +0.25, "Neutral + Exaltation"
    elif is_debil:
        modifier, condition = -0.25, "Neutral + Debilitation"
    else:
        modifier, condition = 0.00, "Neutral"

    return LagneshStrengthResult(
        lagnesh=lagnesh,
        house=house,
        dignity=dignity,
        modifier=modifier,
        condition=condition,
    )
