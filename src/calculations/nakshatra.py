"""
src/calculations/nakshatra.py
==============================
Nakshatra, Pada, Navamsha (D9) placement for any sidereal longitude.
Source: REF_Nakshatra (Excel), BPHS Ch.94-96.
"""

from __future__ import annotations
from dataclasses import dataclass
from src.ephemeris import SIGNS

# ---------------------------------------------------------------------------
# 27 Nakshatras  (REF_Nakshatra rows 6-32)
# Each spans 360/27 = 13.333... degrees
# ---------------------------------------------------------------------------

NAKSHATRA_SPAN = 360.0 / 27  # ≈ 13.3333°
PADA_SPAN      = NAKSHATRA_SPAN / 4   # ≈ 3.3333°

NAKSHATRAS = [
    # (name, dasha_lord, ganda_mool)  — index 0 = Ashwini
    ("Ashwini",           "Ketu",    True),
    ("Bharani",           "Venus",   False),
    ("Krittika",          "Sun",     False),
    ("Rohini",            "Moon",    False),
    ("Mrigashira",        "Mars",    False),
    ("Ardra",             "Rahu",    False),
    ("Punarvasu",         "Jupiter", False),
    ("Pushya",            "Saturn",  False),
    ("Ashlesha",          "Mercury", True),
    ("Magha",             "Ketu",    True),
    ("Purva Phalguni",    "Venus",   False),
    ("Uttara Phalguni",   "Sun",     False),
    ("Hasta",             "Moon",    False),
    ("Chitra",            "Mars",    False),
    ("Swati",             "Rahu",    False),
    ("Vishakha",          "Jupiter", False),
    ("Anuradha",          "Saturn",  False),
    ("Jyeshtha",          "Mercury", True),
    ("Mula",              "Ketu",    True),
    ("Purva Ashadha",     "Venus",   False),
    ("Uttara Ashadha",    "Sun",     False),
    ("Shravana",          "Moon",    False),
    ("Dhanishtha",        "Mars",    False),
    ("Shatabhisha",       "Rahu",    True),
    ("Purva Bhadrapada",  "Jupiter", False),
    ("Uttara Bhadrapada", "Saturn",  False),
    ("Revati",            "Mercury", True),
]

# Pada → Navamsha sign mapping: pada 1-4 across all 108 padas cycles Aries→Pisces
# Navamsha sign index = (nak_index * 4 + pada_index) % 12
# where pada_index = 0..3

def _navamsha_sign_idx(nak_idx: int, pada: int) -> int:
    """Return D9 navamsha sign index (0=Aries) for a given nakshatra and pada (1-4)."""
    return (nak_idx * 4 + (pada - 1)) % 12


@dataclass
class NakshatraPosition:
    longitude: float        # input sidereal longitude
    nak_index: int          # 0-based nakshatra index
    nakshatra: str          # e.g. "Pushya"
    pada: int               # 1-4
    dasha_lord: str         # e.g. "Saturn"
    is_ganda_mool: bool     # sensitive nakshatra
    navamsha_sign: str      # D9 sign, e.g. "Leo"
    navamsha_sign_idx: int  # 0-based


def nakshatra_position(longitude: float) -> NakshatraPosition:
    """
    Compute nakshatra, pada, and D9 navamsha sign for a sidereal longitude.

    Parameters
    ----------
    longitude : sidereal ecliptic longitude, 0–360°
    """
    lon = longitude % 360.0
    nak_idx = int(lon / NAKSHATRA_SPAN)          # 0-26
    deg_in_nak = lon - nak_idx * NAKSHATRA_SPAN
    pada = int(deg_in_nak / PADA_SPAN) + 1       # 1-4
    pada = min(pada, 4)                           # clamp edge case at boundary

    name, dasha_lord, mool = NAKSHATRAS[nak_idx]
    nav_idx = _navamsha_sign_idx(nak_idx, pada)
    nav_sign = SIGNS[nav_idx]

    return NakshatraPosition(
        longitude=lon,
        nak_index=nak_idx,
        nakshatra=name,
        pada=pada,
        dasha_lord=dasha_lord,
        is_ganda_mool=mool,
        navamsha_sign=nav_sign,
        navamsha_sign_idx=nav_idx,
    )
