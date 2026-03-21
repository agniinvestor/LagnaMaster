"""
src/calculations/bhava_bala.py
Bhava Bala — combined strength of each house.
Session 125 (Phase 2).

Formula: Bhavadhipati Bala + Bhava Dig Bala + Drishti Bala
Source: BPHS Ch.27 v.32-41
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class BhavaBalaResult:
    house: int
    bhavadhipati_bala: float   # lord's Shadbala total
    dig_bala: float            # house's directional strength
    drishti_bala: float        # net benefic/malefic aspects on house cusp
    total: float
    strength: str              # "Strong" / "Moderate" / "Weak"


def compute_bhava_bala(house_num: int, chart, shadbala_results: dict) -> BhavaBalaResult:
    """
    Bhava Bala for a single house.
    Source: BPHS Ch.27 v.32-41
    """
    from src.calculations.house_lord import compute_house_map
    _SIGN_LORDS_BB = {0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"}

    lagna_si = chart.lagna_sign_index
    hmap = compute_house_map(chart)

    # Bhavadhipati Bala: strength of the house lord (from Shadbala)
    house_sign = (lagna_si + house_num - 1) % 12
    house_lord = _SIGN_LORDS_BB.get(house_sign)
    bhavadhipati_bala = 0.0
    if house_lord and house_lord in shadbala_results:
        bhavadhipati_bala = shadbala_results[house_lord].total

    # Bhava Dig Bala (positional strength of house)
    # Kendra = strong, Trikona = strong, others = moderate
    if house_num in (1, 4, 7, 10):
        dig_bala = 60.0
    elif house_num in (2, 5, 8, 11):
        dig_bala = 30.0
    else:
        dig_bala = 15.0

    # Drishti Bala: sum of benefic aspects on house cusp - malefic aspects
    house_cusp_sign = house_sign  # noqa: F841
    natural_benefics = {"Moon", "Mercury", "Jupiter", "Venus"}
    natural_malefics  = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

    from src.calculations.scoring_patches import get_aspect_strength, aspect_hits

    drishti_bala = 0.0
    for planet, pdata in chart.planets.items():
        p_house = hmap.planet_house.get(planet, 1)
        ha = aspect_hits(p_house, house_num)
        astr = get_aspect_strength(planet, ha)
        if astr > 0:
            if planet in natural_benefics:
                drishti_bala += astr * 30.0
            elif planet in natural_malefics:
                drishti_bala -= astr * 30.0

    total = round(bhavadhipati_bala + dig_bala + drishti_bala, 3)

    if total >= 250:
        strength = "Strong"
    elif total >= 150:
        strength = "Moderate"
    else:
        strength = "Weak"

    return BhavaBalaResult(
        house=house_num,
        bhavadhipati_bala=round(bhavadhipati_bala, 3),
        dig_bala=dig_bala,
        drishti_bala=round(drishti_bala, 3),
        total=total,
        strength=strength,
    )


def compute_all_bhava_bala(chart, shadbala_results: dict) -> dict[int, BhavaBalaResult]:
    """Compute Bhava Bala for all 12 houses."""
    return {h: compute_bhava_bala(h, chart, shadbala_results) for h in range(1, 13)}
