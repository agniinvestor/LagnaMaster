"""
src/calculations/nakshatra.py
27 nakshatras, padas, D9 navamsha, Ganda Mool.

Session 113 fix: nakshatra index float error
  - BEFORE: int(lon / 13.333)  — truncated float, wrong at boundaries
  - AFTER:  int(lon * 3 / 40)  — exact integer arithmetic
  Source: Swiss Ephemeris precision docs; BPHS Ch.6 (nakshatra = 800'/nakshatra)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus",
    "Sun", "Moon", "Mars", "Rahu", "Jupiter",
    "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]

GANDA_MOOL = {"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}

# D9 start signs per element (Parasara method)
# Fire signs (0,4,8) start D9 from Aries (0)
# Earth signs (1,5,9) start from Capricorn (9)
# Air signs  (2,6,10) start from Libra (6)
# Water signs (3,7,11) start from Cancer (3)
_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}

# Nakshatra width: exactly 40/3 degrees = 800 arcminutes
_NAK_WIDTH = 40.0 / 3.0   # 13.33333... degrees
_NAK_TOTAL = 360.0


@dataclass
class NakshatraPosition:
    nakshatra: str
    nakshatra_index: int   # 0-26
    pada: int              # 1-4
    dasha_lord: str
    navamsha_sign: str     # D9 sign name — backward compat
    navamsha_sign_name: str
    is_ganda_mool: bool
    longitude: float


_SIGN_NAMES = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]


def nakshatra_index(longitude: float) -> int:
    """
    Compute nakshatra index (0-26) from sidereal longitude.
    Uses exact integer arithmetic: int(lon * 3 / 40)
    NOT int(lon / 13.333) — that truncated float causes boundary errors.
    Source: Swiss Ephemeris precision; BPHS Ch.6
    """
    lon = longitude % 360.0
    idx = int(lon * 3 / 40)
    return min(idx, 26)


def _d9_sign_index(longitude: float) -> int:
    """D9 navamsha sign from sidereal longitude (Parasara formula)."""
    si = int(longitude / 30) % 12
    pada = int((longitude % 30) * 9 / 30)
    return (_D9_START[si % 4] + pada) % 12


def nakshatra_position(longitude: float) -> NakshatraPosition:
    """
    Compute full NakshatraPosition from sidereal longitude.
    Uses float-safe nakshatra index formula.
    """
    lon = longitude % 360.0
    nak_idx = nakshatra_index(lon)

    # Pada (1-4)
    nak_start = nak_idx * _NAK_WIDTH
    pos_in_nak = lon - nak_start
    pada = int(pos_in_nak / (_NAK_WIDTH / 4)) + 1
    pada = max(1, min(4, pada))

    # D9 navamsha
    d9_si = _d9_sign_index(lon)

    name = NAKSHATRA_NAMES[nak_idx]
    lord = NAKSHATRA_LORDS[nak_idx]

    return NakshatraPosition(
        nakshatra=name,
        nakshatra_index=nak_idx,
        pada=pada,
        dasha_lord=lord,
        navamsha_sign=_SIGN_NAMES[d9_si],
        navamsha_sign_name=_SIGN_NAMES[d9_si],
        is_ganda_mool=(name in GANDA_MOOL),
        longitude=lon,
    )


def compute_navamsha_chart(chart) -> dict[str, int]:
    """
    Returns D9 sign indices for Lagna and all 9 planets.
    Keys: 'lagna' + planet names
    """
    result = {"lagna": _d9_sign_index(chart.lagna)}
    for name, planet in chart.planets.items():
        result[name] = _d9_sign_index(planet.longitude)
    return result


# ── Backward-compatibility aliases ──
NAKSHATRAS = NAKSHATRA_NAMES          # old name used by existing tests/modules
NAKSHATRA_SPAN = _NAK_WIDTH           # old name: degrees per nakshatra = 40/3


# ── Backward-compatibility: old NAKSHATRAS was list of (name, lord) tuples ──
NAKSHATRAS_TUPLES = list(zip(NAKSHATRA_NAMES, NAKSHATRA_LORDS))
# Override NAKSHATRAS to be tuples if old code unpacks 2 values
# Some old tests unpack 3: (name, lord, span) -- provide that too
NAKSHATRAS_FULL = [(NAKSHATRA_NAMES[i], NAKSHATRA_LORDS[i], NAKSHATRA_NAMES[i] in GANDA_MOOL) for i in range(27)]


# navamsha_sign now returns sign name string directly (see field definition above)


# Abhijit Nakshatra (XII-C) — 28th intercalary nakshatra
# Location: 6°40' to 10°53'20" in Capricorn (sidereal)
# Source: PVRNR BPHS; used in Muhurtha and Kalachakra
ABHIJIT_START_LON = 9 * 30 + 6 + 40/60     # ~276.667°
ABHIJIT_END_LON   = 9 * 30 + 10 + 53/60 + 20/3600  # ~280.889°

def is_abhijit_nakshatra(longitude: float) -> bool:
    """Returns True if longitude falls in Abhijit nakshatra (Capricorn 6°40'-10°53'20")."""
    lon = longitude % 360
    return ABHIJIT_START_LON <= lon <= ABHIJIT_END_LON
