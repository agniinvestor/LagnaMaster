"""
src/calculations/panchanga.py
==============================
Panchanga — the 5-limb Vedic almanac.

The five limbs (angas) are computed from birth date/time:
  1. Tithi     — lunar day (1-30), based on Sun-Moon elongation
  2. Vara      — weekday lord (Sun / Moon / Mars / Mercury / Jupiter / Venus / Saturn)
  3. Nakshatra — Moon's nakshatra and lord (re-uses calculations/nakshatra.py)
  4. Yoga      — 27 panchanga yogas, based on (Sun + Moon) longitude sum
  5. Karana    — half-tithi (60 per month: 1 fixed + 7 movable × 8 + 3 fixed)

Additionally exposes:
  - paksha  : "Shukla" (bright, Moon waxing) or "Krishna" (dark, waning)
  - is_full_moon / is_new_moon helpers
  - navamsha_chart: dict mapping "lagna" + 9 planets to D9 sign indices

Usage:
    from src.calculations.panchanga import compute_panchanga
    p = compute_panchanga(chart, birth_date=date(1947, 8, 15))
    print(p.tithi_name, p.vara, p.nakshatra, p.yoga_name, p.karana_name)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from src.ephemeris import BirthChart, SIGNS
from src.calculations.nakshatra import nakshatra_position, NAKSHATRAS

# ---------------------------------------------------------------------------
# 30 Tithi names (index 1–30 maps to list index 0–29)
# ---------------------------------------------------------------------------

_TITHI_NAMES = [
    "Pratipada", "Dvitiya",    "Tritiya",    "Chaturthi",  "Panchami",
    "Shashthi",  "Saptami",    "Ashtami",    "Navami",     "Dashami",
    "Ekadashi",  "Dwadashi",   "Trayodashi", "Chaturdashi", "Purnima",
    # Krishna paksha (same names for 16-29, except 30 = Amavasya)
    "Pratipada", "Dvitiya",    "Tritiya",    "Chaturthi",  "Panchami",
    "Shashthi",  "Saptami",    "Ashtami",    "Navami",     "Dashami",
    "Ekadashi",  "Dwadashi",   "Trayodashi", "Chaturdashi", "Amavasya",
]

# ---------------------------------------------------------------------------
# 27 Yoga names (Panchanga yoga ≠ birth-chart yoga)
# ---------------------------------------------------------------------------

_YOGA_NAMES = [
    "Vishkamba", "Priti",    "Ayushman",  "Saubhagya",  "Shobhana",
    "Atiganda",  "Sukarman", "Dhriti",    "Shula",      "Ganda",
    "Vriddhi",   "Dhruva",   "Vyaghata",  "Harshana",   "Vajra",
    "Siddhi",    "Vyatipata","Variyan",   "Parigha",    "Shiva",
    "Siddha",    "Sadhya",   "Shubha",    "Shukla",     "Brahma",
    "Mahendra",  "Vaidhriti",
]

# Auspiciousness: 1=auspicious, 0=mixed, -1=inauspicious
_YOGA_NATURE = [
    -1, 1, 1, 1, 1,   # Vishkamba(−), Priti, Ayushman, Saubhagya, Shobhana
     0, 1, 1,-1,-1,   # Atiganda(0), Sukarman, Dhriti, Shula(−), Ganda(−)
     1, 1,-1, 1, 0,   # Vriddhi, Dhruva, Vyaghata(−), Harshana, Vajra(0)
     1,-1, 1,-1, 1,   # Siddhi, Vyatipata(−), Variyan, Parigha(−), Shiva
     1, 1, 1, 1, 1,   # Siddha, Sadhya, Shubha, Shukla, Brahma
     1,-1,            # Mahendra, Vaidhriti(−)
]

# ---------------------------------------------------------------------------
# 11 Karana names
# ---------------------------------------------------------------------------

_MOVABLE_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti"]
_FIXED_KARANAS   = ["Kimstughna", "Shakuni", "Chatushpada", "Naga"]

# Karanas considered inauspicious
_INAUSPICIOUS_KARANAS = {"Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"}

# ---------------------------------------------------------------------------
# Vara (weekday) — weekday lords
# ---------------------------------------------------------------------------

# Python date.weekday(): 0=Monday … 6=Sunday
_VARA_LORDS = {
    6: "Sun",     # Sunday
    0: "Moon",    # Monday
    1: "Mars",    # Tuesday
    2: "Mercury", # Wednesday
    3: "Jupiter", # Thursday
    4: "Venus",   # Friday
    5: "Saturn",  # Saturday
}
_VARA_NAMES = {
    6: "Sunday",    0: "Monday",   1: "Tuesday",  2: "Wednesday",
    3: "Thursday",  4: "Friday",   5: "Saturday",
}

# ---------------------------------------------------------------------------
# D9 Navamsha chart
# ---------------------------------------------------------------------------

# Start sign by sign element (si % 4): Fire=Aries(0), Earth=Capricorn(9), Air=Libra(6), Water=Cancer(3)
_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}


def _d9_sign_index(longitude: float) -> int:
    """Return D9 navamsha sign index (0=Aries) for a sidereal longitude."""
    si   = int(longitude / 30) % 12
    d    = longitude % 30
    pada = int(d * 9 / 30)           # 0–8 (navamsha number within sign)
    return (_D9_START[si % 4] + pada) % 12


def compute_navamsha_chart(chart: BirthChart) -> dict[str, int]:
    """
    Return D9 navamsha sign indices for lagna + all 9 planets.
    Keys: "lagna", "Sun", "Moon", "Mars", …, "Ketu"
    Values: sign index 0–11.
    """
    result = {"lagna": _d9_sign_index(chart.lagna)}
    for pname, p in chart.planets.items():
        result[pname] = _d9_sign_index(p.longitude)
    return result


# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class Panchanga:
    """5-limb Vedic almanac for a birth chart."""

    # 1. Tithi
    tithi: int          # 1–30
    tithi_name: str     # e.g. "Purnima"
    paksha: str         # "Shukla" or "Krishna"

    # 2. Vara
    vara: str           # planet lord: e.g. "Saturn"
    vara_name: str      # weekday: e.g. "Saturday"

    # 3. Nakshatra (Moon)
    nakshatra: str      # e.g. "Pushya"
    nakshatra_lord: str # e.g. "Saturn"
    nakshatra_pada: int # 1–4

    # 4. Yoga (Panchanga)
    yoga: int           # 1–27
    yoga_name: str      # e.g. "Vriddhi"
    yoga_nature: str    # "auspicious" | "inauspicious" | "mixed"

    # 5. Karana
    karana: int         # 1–60
    karana_name: str    # e.g. "Bava"
    karana_inauspicious: bool

    # Helpers
    is_full_moon: bool
    is_new_moon: bool

    # D9 navamsha sign indices
    navamsha_chart: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_panchanga(chart: BirthChart, birth_date: date) -> Panchanga:
    """
    Compute the 5-limb Panchanga for a birth chart.

    Parameters
    ----------
    chart      : BirthChart from compute_chart()
    birth_date : Python date object for the birth day (determines Vara)

    Returns
    -------
    Panchanga dataclass with all 5 limbs populated.
    """
    sun_lon  = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude

    # ── 1. Tithi ──────────────────────────────────────────────────────────────
    # Tithi = floor((moon - sun) / 12) + 1, modulo 30
    elongation = (moon_lon - sun_lon) % 360
    tithi_idx  = int(elongation / 12)         # 0-based (0 = Pratipada)
    tithi      = tithi_idx + 1                # 1-indexed
    tithi_name = _TITHI_NAMES[tithi_idx]
    paksha     = "Shukla" if tithi <= 15 else "Krishna"
    is_full    = (tithi == 15)
    is_new     = (tithi == 30)

    # ── 2. Vara ───────────────────────────────────────────────────────────────
    dow  = birth_date.weekday()               # 0=Monday … 6=Sunday
    vara = _VARA_LORDS[dow]
    vara_name = _VARA_NAMES[dow]

    # ── 3. Nakshatra (Moon) ───────────────────────────────────────────────────
    nak_pos = nakshatra_position(moon_lon)
    nak_name  = nak_pos.nakshatra
    nak_lord  = nak_pos.dasha_lord
    nak_pada  = nak_pos.pada

    # ── 4. Yoga (panchanga) ───────────────────────────────────────────────────
    # Yoga index = floor((sun + moon) / (360/27))
    yoga_span  = 360.0 / 27
    yoga_sum   = (sun_lon + moon_lon) % 360
    yoga_idx   = int(yoga_sum / yoga_span)    # 0-based
    yoga       = yoga_idx + 1                 # 1-indexed
    yoga_name  = _YOGA_NAMES[yoga_idx]
    nature_val = _YOGA_NATURE[yoga_idx]
    yoga_nature = ("auspicious" if nature_val == 1
                   else "inauspicious" if nature_val == -1
                   else "mixed")

    # ── 5. Karana ─────────────────────────────────────────────────────────────
    # 60 karanas per month; each spans 6° of elongation
    karana_idx = int(elongation / 6)          # 0-based, 0–59
    karana     = karana_idx + 1               # 1-indexed

    if karana_idx == 0:
        karana_name = "Kimstughna"            # fixed, first half of 1st tithi
    elif karana_idx <= 56:
        karana_name = _MOVABLE_KARANAS[(karana_idx - 1) % 7]
    elif karana_idx == 57:
        karana_name = "Shakuni"
    elif karana_idx == 58:
        karana_name = "Chatushpada"
    else:  # 59
        karana_name = "Naga"

    # ── D9 navamsha chart ─────────────────────────────────────────────────────
    d9 = compute_navamsha_chart(chart)

    return Panchanga(
        tithi=tithi, tithi_name=tithi_name, paksha=paksha,
        vara=vara, vara_name=vara_name,
        nakshatra=nak_name, nakshatra_lord=nak_lord, nakshatra_pada=nak_pada,
        yoga=yoga, yoga_name=yoga_name, yoga_nature=yoga_nature,
        karana=karana, karana_name=karana_name,
        karana_inauspicious=(karana_name in _INAUSPICIOUS_KARANAS),
        is_full_moon=is_full,
        is_new_moon=is_new,
        navamsha_chart=d9,
    )
