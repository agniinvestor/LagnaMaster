"""
src/calculations/ashtottari_dasha.py — Session 100

Ashtottari Dasha — 108-year nakshatra dasha.
PVRNR preface p8: "Vimsottari dasa and Ashtottari dasa — most commonly used".

Qualification: applicable when Sun is in non-Rahu nakshatra during day birth,
OR when Rahu is not in lagna or 7th house. Used as alternative to Vimshottari.

Planet sequence (8 planets, excluding Ketu):
  Sun=6, Moon=15, Mars=8, Mercury=17, Saturn=10, Jupiter=19, Rahu=12, Venus=21
  Total = 108 years

Starting planet = lord of Moon's nakshatra (same Vimshottari nakshatra lordship
but Rahu replaces Ketu in the sequence).

Source: BPHS Ch.47; PVRNR preface.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

_ASHTO_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus"]
_ASHTO_YEARS = [6, 15, 8, 17, 10, 19, 12, 21]
_ASHTO_NAK_MAP = {
    # nakshatra → starting lord (8-planet sequence)
    0: "Sun",
    1: "Moon",
    2: "Mars",
    3: "Mercury",
    4: "Saturn",
    5: "Jupiter",
    6: "Rahu",
    7: "Venus",
    8: "Sun",
    9: "Moon",
    10: "Mars",
    11: "Mercury",
    12: "Saturn",
    13: "Jupiter",
    14: "Rahu",
    15: "Venus",
    16: "Sun",
    17: "Moon",
    18: "Mars",
    19: "Mercury",
    20: "Saturn",
    21: "Jupiter",
    22: "Rahu",
    23: "Venus",
    24: "Sun",
    25: "Moon",
    26: "Mars",
}


@dataclass
class AshtottariPeriod:
    planet: str
    years: int
    start_date: date
    end_date: date


def qualifies_for_ashtottari(chart) -> bool:
    """
    Check if Ashtottari is applicable.
    Applicable: Rahu not in 1st or 7th house from lagna.
    """
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    rahu_h = hmap.planet_house.get("Rahu", 0)
    return rahu_h not in {1, 7}


def compute_ashtottari_dasha(chart, birth_date: date) -> list[AshtottariPeriod]:
    """Compute Ashtottari Dasha periods."""
    moon_pos = chart.planets.get("Moon")
    if not moon_pos:
        return []

    moon_lon = moon_pos.longitude % 360
    nak_idx = int(moon_lon * 27 / 360) % 27
    nak_fraction = (moon_lon * 27 / 360) - int(moon_lon * 27 / 360)

    start_lord = _ASHTO_NAK_MAP.get(nak_idx, "Sun")
    start_idx = _ASHTO_LORDS.index(start_lord)

    first_years = _ASHTO_YEARS[start_idx]
    elapsed = nak_fraction * first_years
    current_date = birth_date + timedelta(days=-int(elapsed * 365.25))

    periods = []
    for cycle in range(2):  # 2 cycles ≈ 216 years
        for i in range(8):
            planet_idx = (start_idx + i) % 8
            planet = _ASHTO_LORDS[planet_idx]
            years = _ASHTO_YEARS[planet_idx]
            end = current_date + timedelta(days=int(years * 365.25))
            periods.append(
                AshtottariPeriod(
                    planet=planet,
                    years=years,
                    start_date=current_date,
                    end_date=end,
                )
            )
            current_date = end

    return periods
