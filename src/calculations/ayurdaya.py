"""
src/calculations/ayurdaya.py
Ayurdaya (longevity) calculation: Pindayu + Amsayu + Nisargayu.
Session 133 (Phase 2).

Source: BPHS Ch.44; PVRNR commentaries
"""

from __future__ import annotations
from dataclasses import dataclass
from math import sqrt


# Pindayu years contributed by each planet in its exaltation sign
PINDAYU_EXALT_YEARS: dict[str, float] = {
    "Sun":     19.0,
    "Moon":    25.0,
    "Mars":    15.0,
    "Mercury": 12.0,
    "Jupiter": 15.0,
    "Venus":   21.0,
    "Saturn":  20.0,
}

# Nisargayu (natural) longevity years by planet
NISARGAYU_YEARS: dict[str, float] = {
    "Sun":     20.0,
    "Moon":    1.0,
    "Mars":    2.0,
    "Mercury": 9.0,
    "Jupiter": 18.0,
    "Venus":   20.0,
    "Saturn":  50.0,
}


@dataclass
class AyurdayaResult:
    pindayu: float      # years from planetary arc method
    amsayu: float       # years from navamsha positions
    nisargayu: float    # natural/fixed longevity
    combined: float     # (pindayu + amsayu + nisargayu) / 3
    category: str       # "Short" (<32) / "Middle" (32-64) / "Long" (>64)


def compute_pindayu(chart) -> float:
    """
    Pindayu: sum of each planet's arc contribution to longevity.
    Each planet contributes years proportional to its angular distance from Lagna.
    Source: BPHS Ch.44
    """
    lagna_lon = chart.lagna
    total = 0.0

    for planet, exalt_yrs in PINDAYU_EXALT_YEARS.items():
        if planet not in chart.planets:
            continue
        planet_lon = chart.planets[planet].longitude
        # Arc from Lagna in degrees
        arc = (planet_lon - lagna_lon) % 360
        # Contribution = exalt_years * arc / 360
        contribution = exalt_yrs * arc / 360.0

        # Reduction factors
        if chart.planets[planet].is_retrograde:
            contribution *= 0.5  # retrograde reduces by half
        # Combust reduction handled in dignity

        total += contribution

    return round(total, 2)


def compute_amsayu(chart) -> float:
    """
    Amsayu: longevity from navamsha (D9) positions.
    Each planet contributes based on its D9 sign strength.
    Source: BPHS Ch.44
    """
    try:
        from src.calculations.vargas import compute_varga_sign
    except ImportError:
        return 0.0

    total = 0.0
    for planet, exalt_yrs in PINDAYU_EXALT_YEARS.items():
        if planet not in chart.planets:
            continue
        lon = chart.planets[planet].longitude
        try:
            d9_si = compute_varga_sign(lon, 9)
        except Exception:
            continue
        # Full years if exalted in D9, proportional otherwise
        from src.calculations.dignity import EXALT_SIGN, OWN_SIGNS
        if planet in EXALT_SIGN and d9_si == EXALT_SIGN[planet]:
            frac = 1.0
        elif planet in OWN_SIGNS and d9_si in OWN_SIGNS[planet]:
            frac = 0.75
        else:
            frac = 0.5
        total += exalt_yrs * frac

    return round(total, 2)


def compute_nisargayu(chart) -> float:
    """
    Nisargayu: fixed natural longevity from Lagna lord's strength.
    Simplified: sum of NISARGAYU_YEARS for all planets, weighted by dignity.
    Source: BPHS Ch.44
    """
    total = 0.0
    for planet, yrs in NISARGAYU_YEARS.items():
        if planet not in chart.planets:
            continue
        from src.calculations.dignity import compute_dignity, DignityLevel
        d = compute_dignity(planet, chart)
        if d.dignity in (DignityLevel.DEEP_EXALT, DignityLevel.EXALT):
            total += yrs
        elif d.dignity in (DignityLevel.MOOLTRIKONA, DignityLevel.OWN_SIGN):
            total += yrs * 0.75
        elif d.dignity == DignityLevel.DEBIL:
            total += yrs * 0.25
        else:
            total += yrs * 0.5

    return round(total, 2)


def compute_ayurdaya(chart) -> AyurdayaResult:
    """
    Full Ayurdaya calculation combining all three methods.
    Source: BPHS Ch.44
    """
    pindayu   = compute_pindayu(chart)
    amsayu    = compute_amsayu(chart)
    nisargayu = compute_nisargayu(chart)
    combined  = round((pindayu + amsayu + nisargayu) / 3.0, 2)

    if combined < 32:
        category = "Short"
    elif combined < 64:
        category = "Middle"
    else:
        category = "Long"

    return AyurdayaResult(
        pindayu=pindayu,
        amsayu=amsayu,
        nisargayu=nisargayu,
        combined=combined,
        category=category,
    )
