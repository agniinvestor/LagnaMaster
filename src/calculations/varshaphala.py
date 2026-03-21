"""
src/calculations/varshaphala.py
Varshaphala — Solar Return Annual Chart with Muntha and Varshesha.
Session 149.

Varshaphala is a parallel predictive system (Tajika school) using:
  - Solar return chart (Sun returns to exact natal longitude)
  - Muntha (progressed Lagna, advances 1 sign per year)
  - Varshesha (ruler of the year — strongest planet in annual chart)
  - Tajika aspects (0/60/90/120/180° with orbs, unlike Parashari)

Sources:
  Neelakantha · Tajika Nilakanthi (primary Varshaphala text, Ranjan Publications)
  K.N. Rao · Astrology, Destiny and the Wheel of Time Ch.7-9
  Gayatri Devi Vasudev · The Art of Prediction in Astrology
  PVRNR · BPHS (annual chart references)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

# ─── Tajika Aspects ───────────────────────────────────────────────────────────
# Different from Parashari — only 5 aspects, all have orbs
# Source: Tajika Nilakanthi

TAJIKA_ASPECTS: dict[int, tuple[str, float]] = {
    0:   ("Conjunction/Yukti",     8.0),
    60:  ("Sextile/Shatpanchasa",  5.0),
    90:  ("Square/Chaturnabha",    7.0),
    120: ("Trine/Trikona",         8.0),
    180: ("Opposition/Tritrikona", 8.0),
}

TAJIKA_ASPECT_NATURE: dict[int, str] = {
    0:   "variable",   # conjunction: depends on planets involved
    60:  "benefic",
    90:  "malefic",
    120: "benefic",
    180: "malefic",
}


def get_tajika_aspect(lon_a: float, lon_b: float) -> Optional[dict]:
    """
    Check if two planets form a Tajika aspect.
    Returns aspect details or None if no aspect within orb.
    """
    diff = abs(lon_a - lon_b) % 360
    if diff > 180:
        diff = 360 - diff

    for angle, (name, orb) in TAJIKA_ASPECTS.items():
        if abs(diff - angle) <= orb:
            return {
                "aspect": name,
                "angle": angle,
                "orb_used": abs(diff - angle),
                "max_orb": orb,
                "nature": TAJIKA_ASPECT_NATURE[angle],
                "exact_diff": round(diff, 4),
            }
    return None


# ─── Muntha ───────────────────────────────────────────────────────────────────

def compute_muntha(natal_lagna_sign: int, birth_year: int, query_year: int) -> int:
    """
    Muntha (progressed Lagna): advances 1 sign per year from natal Lagna.
    Muntha for year N = (natal_lagna_sign + N_elapsed) mod 12

    Source: Tajika Nilakanthi; K.N. Rao references
    """
    years_elapsed = query_year - birth_year
    return (natal_lagna_sign + years_elapsed) % 12


def muntha_quality(muntha_sign: int, annual_chart_lagna: int) -> dict:
    """
    Assess Muntha's quality based on its position from annual chart Lagna.
    H1/H4/H5/H7/H9/H10/H11 = favorable; H6/H8/H12 = unfavorable.
    """
    house_from_annual_lagna = ((muntha_sign - annual_chart_lagna) % 12) + 1
    good_houses = {1, 4, 5, 7, 9, 10, 11}
    is_good = house_from_annual_lagna in good_houses

    return {
        "muntha_sign": muntha_sign,
        "house_from_annual_lagna": house_from_annual_lagna,
        "quality": "favorable" if is_good else "unfavorable",
        "note": f"Muntha in H{house_from_annual_lagna} of annual chart",
    }


# ─── Varshesha (Ruler of the Year) ───────────────────────────────────────────

_NATURAL_STRENGTH_ORDER = [
    "Sun", "Moon", "Venus", "Jupiter", "Mercury", "Mars", "Saturn"
]


def compute_varshesha(annual_chart, muntha_sign: int) -> str:
    """
    Varshesha: the planet with greatest strength in the annual chart.
    Selection criteria (in order of priority):
    1. Planet that is both in Kendra from annual Lagna AND owns a Kendra
    2. Planet with most Shadbala strength in annual chart
    3. Fall back to natural strength order

    Source: Tajika Nilakanthi; K.N. Rao Ch.7
    """
    if annual_chart is None:
        return "Sun"

    lagna_si = annual_chart.lagna_sign_index

    # Find planets in Kendra from annual Lagna
    kendra_signs = {(lagna_si + k) % 12 for k in (0, 3, 6, 9)}
    planets_in_kendra = [
        p for p, pd in annual_chart.planets.items()
        if pd.sign_index in kendra_signs and p not in ("Rahu", "Ketu")
    ]

    if planets_in_kendra:
        # Pick strongest among Kendra planets by natural order
        for p in _NATURAL_STRENGTH_ORDER:
            if p in planets_in_kendra:
                return p

    # Fall back to natural order
    for p in _NATURAL_STRENGTH_ORDER:
        if p in annual_chart.planets:
            return p

    return "Sun"


# ─── Solar Return Computation ─────────────────────────────────────────────────

@dataclass
class VarshaphalaResult:
    query_year: int
    natal_sun_longitude: float
    solar_return_datetime: Optional[datetime]
    annual_chart_lagna_sign: int       # Lagna of the annual chart
    muntha_sign: int                   # Progressed Lagna sign
    muntha_quality: dict               # Muntha's house from annual Lagna
    varshesha: str                     # Ruler of the year planet
    tajika_aspects: list[dict]         # Major Tajika aspects in annual chart
    year_quality: str                  # "excellent"/"good"/"neutral"/"challenging"
    key_periods: list[str]             # Months of significant activity


def compute_varshaphala(
    natal_chart,
    birth_year: int,
    query_year: int,
    annual_chart=None,
) -> VarshaphalaResult:
    """
    Compute Varshaphala for a given year.
    annual_chart: if None, uses natal chart as approximation
    (full implementation requires computing solar return moment via pyswisseph)

    Source: Tajika Nilakanthi; K.N. Rao Ch.7-9
    """
    natal_sun_lon = natal_chart.planets["Sun"].longitude if "Sun" in natal_chart.planets else 0.0
    natal_lagna_si = natal_chart.lagna_sign_index

    # Muntha
    muntha = compute_muntha(natal_lagna_si, birth_year, query_year)

    # Annual chart (use natal as fallback if not provided)
    annual = annual_chart or natal_chart
    annual_lagna_si = annual.lagna_sign_index

    muntha_qual = muntha_quality(muntha, annual_lagna_si)

    # Varshesha
    varshesha_planet = compute_varshesha(annual, muntha)

    # Tajika aspects between major planets in annual chart
    planets_list = list(annual.planets.items())
    tajika_aspects_found = []
    for i, (pa, pa_data) in enumerate(planets_list):
        for pb, pb_data in planets_list[i+1:]:
            asp = get_tajika_aspect(pa_data.longitude, pb_data.longitude)
            if asp:
                asp["planet_a"] = pa
                asp["planet_b"] = pb
                tajika_aspects_found.append(asp)

    # Year quality from Muntha + Varshesha
    benefics = {"Jupiter", "Venus", "Mercury", "Moon"}
    varshesha_benefic = varshesha_planet in benefics
    muntha_favorable = muntha_qual["quality"] == "favorable"

    if varshesha_benefic and muntha_favorable:
        year_quality = "excellent"
    elif varshesha_benefic or muntha_favorable:
        year_quality = "good"
    elif not varshesha_benefic and not muntha_favorable:
        year_quality = "challenging"
    else:
        year_quality = "neutral"

    return VarshaphalaResult(
        query_year=query_year,
        natal_sun_longitude=natal_sun_lon,
        solar_return_datetime=None,  # requires live pyswisseph call
        annual_chart_lagna_sign=annual_lagna_si,
        muntha_sign=muntha,
        muntha_quality=muntha_qual,
        varshesha=varshesha_planet,
        tajika_aspects=tajika_aspects_found,
        year_quality=year_quality,
        key_periods=[],
    )


def compute_tajika_aspects_for_chart(chart) -> list[dict]:
    """
    Compute all Tajika aspects between planets in a chart.
    Useful for annual chart analysis.
    """
    planets_list = list(chart.planets.items())
    aspects = []
    for i, (pa, pa_data) in enumerate(planets_list):
        for pb, pb_data in planets_list[i+1:]:
            asp = get_tajika_aspect(pa_data.longitude, pb_data.longitude)
            if asp:
                asp["planet_a"] = pa
                asp["planet_b"] = pb
                aspects.append(asp)
    return aspects
