"""
src/calculations/tara_dasha.py — Session 96

Tara Dasha (Star Dasha) — nakshatra-based dasha.
9 categories of nakshatras from birth nakshatra:
  1. Janma (birth)   2. Sampat (wealth)  3. Vipat (danger)
  4. Kshema (comfort) 5. Pratyak (obstruction) 6. Sadhana (achievement)
  7. Naidhana (death) 8. Mitra (friend)   9. Ati-Mitra (great friend)

Each group of 3 nakshatras forms one category.
Planet sequence: same as Vimshottari but starting from birth nakshatra's lord.
Period lengths: same as Vimshottari (Ketu=7, Venus=20, Sun=6, Moon=10, Mars=7,
  Rahu=18, Jupiter=16, Saturn=19, Mercury=17).

Used primarily for timing events related to the body, health, and relationships.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

_TARA_NAMES = [
    "Janma",
    "Sampat",
    "Vipat",
    "Kshema",
    "Pratyak",
    "Sadhana",
    "Naidhana",
    "Mitra",
    "Ati-Mitra",
]
_TARA_QUALITY = {
    "Janma": "Neutral — identity themes",
    "Sampat": "Auspicious — wealth and prosperity",
    "Vipat": "Challenging — obstacles and dangers",
    "Kshema": "Auspicious — comfort and wellbeing",
    "Pratyak": "Mixed — obstruction, requires effort",
    "Sadhana": "Auspicious — achievement and success",
    "Naidhana": "Challenging — difficulties and endings",
    "Mitra": "Auspicious — friendly, supportive",
    "Ati-Mitra": "Very Auspicious — great support and success",
}

_VIM_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]
_VIM_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
_NAK_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]


@dataclass
class TaraDashaPeriod:
    planet: str
    years: int
    start_date: date
    end_date: date
    tara_category: str  # "Janma", "Sampat", etc.
    tara_quality: str
    nakshatra_number: int  # which nakshatra this falls on (0-26)


def compute_tara_dasha(chart, birth_date: date) -> list[TaraDashaPeriod]:
    """Compute Tara Dasha periods from birth nakshatra."""
    moon_pos = chart.planets.get("Moon")
    if not moon_pos:
        return []

    moon_lon = moon_pos.longitude % 360
    birth_nak = int(moon_lon * 27 / 360) % 27
    nak_fraction = (moon_lon * 27 / 360) - int(moon_lon * 27 / 360)

    # Find starting planet
    start_lord = _NAK_LORDS[birth_nak]
    start_idx = _VIM_LORDS.index(start_lord)

    # Elapsed in first period
    first_years = _VIM_YEARS[start_idx]
    elapsed = nak_fraction * first_years
    current_date = birth_date + timedelta(days=-int(elapsed * 365.25))

    periods = []
    for cycle in range(3):  # 3 cycles ≈ 120 years
        for i in range(9):
            planet_idx = (start_idx + i) % 9
            planet = _VIM_LORDS[planet_idx]
            years = _VIM_YEARS[planet_idx]
            end = current_date + timedelta(days=int(years * 365.25))

            # Tara category: based on nakshatra count from birth nak
            nak_offset = (birth_nak + cycle * 9 + i) % 27
            tara_cat = _TARA_NAMES[i]  # simplified — same sequence

            periods.append(
                TaraDashaPeriod(
                    planet=planet,
                    years=years,
                    start_date=current_date,
                    end_date=end,
                    tara_category=tara_cat,
                    tara_quality=_TARA_QUALITY[tara_cat],
                    nakshatra_number=nak_offset,
                )
            )
            current_date = end

    return periods
