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
    bhavadhipati_bala: float  # lord's Shadbala total
    dig_bala: float  # house's directional strength
    drishti_bala: float  # net benefic/malefic aspects on house cusp
    total: float
    strength: str  # "Strong" / "Moderate" / "Weak"


def compute_bhava_bala(
    house_num: int, chart, shadbala_results: dict
) -> BhavaBalaResult:
    """
    Bhava Bala for a single house.
    Source: BPHS Ch.27 v.32-41
    """
    from src.calculations.house_lord import compute_house_map

    _SIGN_LORDS_BB = {
        0: "Mars",
        1: "Venus",
        2: "Mercury",
        3: "Moon",
        4: "Sun",
        5: "Mercury",
        6: "Venus",
        7: "Mars",
        8: "Jupiter",
        9: "Saturn",
        10: "Saturn",
        11: "Jupiter",
    }

    lagna_si = chart.lagna_sign_index
    hmap = compute_house_map(chart)

    # Bhavadhipati Bala: strength of the house lord (from Shadbala)
    house_sign = (lagna_si + house_num - 1) % 12
    house_lord = _SIGN_LORDS_BB.get(house_sign)
    bhavadhipati_bala = 0.0
    if house_lord and house_lord in shadbala_results:
        bhavadhipati_bala = shadbala_results[house_lord].total

    # Bhava Dig Bala — BPHS Ch.27 v.26-29 (p.286)
    # Sign-based deduction: deduct specific house cusp from bhava cusp
    # based on which sign the bhava falls in.
    bhava_cusp_lon = (chart.lagna + (house_num - 1) * 30) % 360
    bhava_deg = bhava_cusp_lon % 30

    # Determine deduction house cusp based on bhava sign
    _DEDUCT_7TH = {2, 5, 6, 10}  # Gemini, Virgo, Libra, Aquarius
    _DEDUCT_4TH = {0, 1, 4}  # Aries, Taurus, Leo
    _DEDUCT_1ST = {3, 7}  # Cancer, Scorpio
    _DEDUCT_10TH = {11}  # Pisces

    if house_sign in _DEDUCT_7TH:
        deduct_house = 7
    elif house_sign in _DEDUCT_4TH:
        deduct_house = 4
    elif house_sign in _DEDUCT_1ST:
        deduct_house = 1
    elif house_sign in _DEDUCT_10TH:
        deduct_house = 10
    elif house_sign == 8:  # Sagittarius: first half→7th, second half→4th
        deduct_house = 7 if bhava_deg < 15 else 4
    elif house_sign == 9:  # Capricorn: first half→4th, second half→10th
        deduct_house = 4 if bhava_deg < 15 else 10
    else:
        deduct_house = 7  # fallback

    deduct_cusp_lon = (chart.lagna + (deduct_house - 1) * 30) % 360
    arc = abs(bhava_cusp_lon - deduct_cusp_lon) % 360
    if arc > 180:
        arc = 360 - arc
    dig_bala = min(60.0, arc / 3.0)

    # Drishti Bala — BPHS v.26-29: +1/4 benefic, -1/4 malefic aspects
    from src.calculations.sputa_drishti import bphs_drishti_with_specials
    from src.calculations.rule_firing import is_natural_malefic

    drishti_bala = 0.0
    for planet, pdata in chart.planets.items():
        arc_to_house = (bhava_cusp_lon - pdata.longitude) % 360
        virupas = bphs_drishti_with_specials(planet, arc_to_house)
        if virupas > 0:
            rupa = virupas / 60.0
            if is_natural_malefic(planet, chart):
                drishti_bala -= rupa * 0.25
            else:
                drishti_bala += rupa * 0.25
    drishti_bala = round(drishti_bala * 60.0, 3)  # convert to virupas

    # Special additions — BPHS Ch.27 v.30-31 (p.286)
    specials = 0.0
    # Jupiter/Mercury in house → +60 virupas; Saturn/Mars/Sun → -60
    for planet, pdata in chart.planets.items():
        p_house = hmap.planet_house.get(planet, 1)
        if p_house == house_num:
            if planet in ("Jupiter", "Mercury"):
                specials += 60.0
            elif planet in ("Saturn", "Mars", "Sun"):
                specials -= 60.0

    # Seershodaya signs in daytime → +15 virupas
    _SEERSHODAYA = {2, 4, 5, 6, 7, 10}  # Gemini, Leo, Virgo, Libra, Scorpio, Aquarius
    sun = chart.planets.get("Sun")
    if sun:
        is_day = not (90 <= sun.longitude % 360 < 270)
        if is_day and house_sign in _SEERSHODAYA:
            specials += 15.0
        if not is_day and house_sign not in _SEERSHODAYA and house_sign != 11:
            specials += 15.0  # Prishtodaya in nighttime

    total = round(bhavadhipati_bala + dig_bala + drishti_bala + specials, 3)

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
