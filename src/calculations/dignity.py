"""
src/calculations/dignity.py
============================
Dignity levels, weights, and Neecha Bhanga detection.
Source: REF_Dignity (Excel), BPHS Ch.3, Saravali Ch.1.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from src.ephemeris import BirthChart, PlanetPosition, SIGNS


class DignityLevel(str, Enum):
    DEEP_EXALT   = "deep_exaltation"
    EXALT        = "exaltation"
    MOOLTRIKONA  = "mooltrikona"
    OWN_SIGN     = "own_sign"
    FRIEND_SIGN  = "friendly_sign"
    NEUTRAL_SIGN = "neutral_sign"
    ENEMY_SIGN   = "enemy_sign"
    DEBIL        = "debilitation"
    DEEP_DEBIL   = "deep_debilitation"


# Score weights (REF_Dignity rows 17-29)
DIGNITY_WEIGHT: dict[DignityLevel, float] = {
    DignityLevel.DEEP_EXALT:   +2.0,
    DignityLevel.EXALT:        +1.5,
    DignityLevel.MOOLTRIKONA:  +1.0,
    DignityLevel.OWN_SIGN:     +0.75,
    DignityLevel.FRIEND_SIGN:  +0.5,
    DignityLevel.NEUTRAL_SIGN:  0.0,
    DignityLevel.ENEMY_SIGN:   -0.5,
    DignityLevel.DEBIL:        -1.5,
    DignityLevel.DEEP_DEBIL:   -2.0,
}

RETROGRADE_BONUS  = +0.25   # contested but present in REF_Dignity R28
COMBUST_DIRECT    = -1.0    # REF_Dignity R26
COMBUST_RETRO     = -0.5    # REF_Dignity R27
NEECHA_BHANGA     = +1.0    # cancellation bonus (treat as neutral) R29


# ---------------------------------------------------------------------------
# Reference tables  (derived from REF_Dignity + REF_Planets)
# ---------------------------------------------------------------------------

# sign_index: 0=Aries … 11=Pisces
_SIGN_IDX = {s: i for i, s in enumerate(SIGNS)}

# (exalt_sign_idx, exact_degree)
_EXALT: dict[str, tuple[int, float]] = {
    "Sun":     (_SIGN_IDX["Aries"],      10.0),
    "Moon":    (_SIGN_IDX["Taurus"],      3.0),
    "Mars":    (_SIGN_IDX["Capricorn"],  28.0),
    "Mercury": (_SIGN_IDX["Virgo"],      15.0),
    "Jupiter": (_SIGN_IDX["Cancer"],      5.0),
    "Venus":   (_SIGN_IDX["Pisces"],     27.0),
    "Saturn":  (_SIGN_IDX["Libra"],      20.0),
    "Rahu":    (_SIGN_IDX["Taurus"],     20.0),
    "Ketu":    (_SIGN_IDX["Scorpio"],    20.0),
}

# (debil_sign_idx, exact_degree)
_DEBIL: dict[str, tuple[int, float]] = {
    "Sun":     (_SIGN_IDX["Libra"],      10.0),
    "Moon":    (_SIGN_IDX["Scorpio"],     3.0),
    "Mars":    (_SIGN_IDX["Cancer"],     28.0),
    "Mercury": (_SIGN_IDX["Pisces"],     15.0),
    "Jupiter": (_SIGN_IDX["Capricorn"],   5.0),
    "Venus":   (_SIGN_IDX["Virgo"],      27.0),
    "Saturn":  (_SIGN_IDX["Aries"],      20.0),
    "Rahu":    (_SIGN_IDX["Scorpio"],    20.0),
    "Ketu":    (_SIGN_IDX["Taurus"],     20.0),
}

# Mooltrikona: (sign_idx, start_deg, end_deg) — None if no MLT
_MLT: dict[str, tuple[int, float, float] | None] = {
    "Sun":     (_SIGN_IDX["Leo"],        0.0, 20.0),
    "Moon":    (_SIGN_IDX["Taurus"],     4.0, 20.0),
    "Mars":    (_SIGN_IDX["Aries"],      0.0, 12.0),
    "Mercury": (_SIGN_IDX["Virgo"],      0.0, 15.0),
    "Jupiter": (_SIGN_IDX["Sagittarius"],0.0, 10.0),
    "Venus":   (_SIGN_IDX["Libra"],      0.0, 15.0),
    "Saturn":  (_SIGN_IDX["Aquarius"],   0.0, 20.0),
    "Rahu":    None,
    "Ketu":    None,
}

# Own signs (sign_idx list)
_OWN: dict[str, list[int]] = {
    "Sun":     [_SIGN_IDX["Leo"]],
    "Moon":    [_SIGN_IDX["Cancer"]],
    "Mars":    [_SIGN_IDX["Aries"], _SIGN_IDX["Scorpio"]],
    "Mercury": [_SIGN_IDX["Gemini"], _SIGN_IDX["Virgo"]],
    "Jupiter": [_SIGN_IDX["Sagittarius"], _SIGN_IDX["Pisces"]],
    "Venus":   [_SIGN_IDX["Taurus"], _SIGN_IDX["Libra"]],
    "Saturn":  [_SIGN_IDX["Capricorn"], _SIGN_IDX["Aquarius"]],
    "Rahu":    [_SIGN_IDX["Aquarius"]],   # BPHS convention
    "Ketu":    [_SIGN_IDX["Scorpio"]],    # BPHS convention
}

# Combustion orbs in degrees (direct motion) — REF_Dignity col M
_COMBUST_ORB_DIRECT: dict[str, float] = {
    "Moon":    12.0,
    "Mars":    17.0,
    "Mercury": 14.0,
    "Jupiter": 11.0,
    "Venus":   10.0,
    "Saturn":  15.0,
}
_COMBUST_ORB_RETRO_REDUCTION = 2.0   # Saravali Ch.3: Rx orb = direct orb − 2°


@dataclass
class DignityResult:
    planet: str
    sign: str
    degree_in_sign: float
    dignity: DignityLevel
    is_deep: bool          # within ±5° of exact exalt/debil peak
    weight: float          # dignity score modifier
    is_combust: bool       # combust by Sun
    is_cazimi: bool        # within 1° of Sun (overrides combustion)
    is_retrograde: bool
    neecha_bhanga: bool    # debilitation cancelled
    total_modifier: float  # sum of all applicable modifiers


def _angular_distance(a: float, b: float) -> float:
    """Shortest arc between two ecliptic longitudes (0-360°)."""
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _natural_relationship(planet: str, sign_lord: str) -> str:
    """
    Return natural (Naisargika) relationship of planet to sign_lord.
    Returns 'F', 'N', or 'E'.
    Derived from REF_NaisargikaFriendship matrix.
    """
    # Matrix: row planet views column planet  (F=Friend, N=Neutral, E=Enemy)
    _NAISARGIKA = {
        #           Sun   Moon  Mars  Merc  Jup   Ven   Sat
        "Sun":    ["—",  "F",  "F",  "N",  "F",  "E",  "E"],
        "Moon":   ["F",  "—",  "N",  "F",  "N",  "N",  "N"],
        "Mars":   ["F",  "F",  "—",  "E",  "F",  "N",  "N"],
        "Mercury":["F",  "E",  "N",  "—",  "N",  "F",  "N"],
        "Jupiter":["F",  "F",  "F",  "E",  "—",  "E",  "N"],
        "Venus":  ["E",  "E",  "N",  "F",  "N",  "—",  "F"],
        "Saturn": ["E",  "E",  "E",  "F",  "N",  "F",  "—"],
    }
    _ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    # Rahu/Ketu: no standard Naisargika entry → treat as neutral
    if planet in ("Rahu", "Ketu") or sign_lord in ("Rahu", "Ketu"):
        return "N"
    row = _NAISARGIKA.get(planet, {})
    if isinstance(row, dict):
        return "N"
    col_idx = _ORDER.index(sign_lord) if sign_lord in _ORDER else -1
    if col_idx < 0:
        return "N"
    val = row[col_idx]
    return val if val in ("F", "N", "E") else "N"


def compute_dignity(
    planet: str,
    sign_idx: int,
    degree_in_sign: float,
    is_retrograde: bool,
    sun_longitude: float,
    planet_longitude: float,
    lagna_sign_idx: int,
    chart: BirthChart | None = None,
) -> DignityResult:
    """
    Compute dignity level and score modifier for one planet.

    Parameters
    ----------
    planet           : planet name
    sign_idx         : sign index (0=Aries)
    degree_in_sign   : 0-30°
    is_retrograde    : retrograde flag
    sun_longitude    : Sun's sidereal longitude for combustion check
    planet_longitude : planet's sidereal longitude for combustion check
    lagna_sign_idx   : ascendant sign index (for house count)
    chart            : full BirthChart (optional — used for Neecha Bhanga)
    """
    dignity = DignityLevel.NEUTRAL_SIGN
    is_deep = False
    neecha_bhanga = False

    # --- Exaltation ---
    if planet in _EXALT:
        exalt_sign, exalt_deg = _EXALT[planet]
        if sign_idx == exalt_sign:
            diff = abs(degree_in_sign - exalt_deg)
            is_deep = diff <= 5.0
            dignity = DignityLevel.DEEP_EXALT if is_deep else DignityLevel.EXALT

    # --- Debilitation (only if not exalted) ---
    if dignity == DignityLevel.NEUTRAL_SIGN and planet in _DEBIL:
        debil_sign, debil_deg = _DEBIL[planet]
        if sign_idx == debil_sign:
            diff = abs(degree_in_sign - debil_deg)
            is_deep = diff <= 5.0
            dignity = DignityLevel.DEEP_DEBIL if is_deep else DignityLevel.DEBIL
            # Simple Neecha Bhanga: lord of debilitation sign in a kendra from lagna
            neecha_bhanga = _check_neecha_bhanga(planet, sign_idx, lagna_sign_idx, chart)
            if neecha_bhanga:
                dignity = DignityLevel.NEUTRAL_SIGN  # cancel debilitation

    # --- Mooltrikona ---
    if dignity == DignityLevel.NEUTRAL_SIGN and _MLT.get(planet):
        mlt_sign, mlt_start, mlt_end = _MLT[planet]
        if sign_idx == mlt_sign and mlt_start <= degree_in_sign <= mlt_end:
            dignity = DignityLevel.MOOLTRIKONA

    # --- Own sign ---
    if dignity == DignityLevel.NEUTRAL_SIGN and sign_idx in _OWN.get(planet, []):
        dignity = DignityLevel.OWN_SIGN

    # --- Natural friendship (only if none of the above) ---
    if dignity == DignityLevel.NEUTRAL_SIGN:
        sign_lord = _sign_lord(sign_idx)
        if sign_lord != planet:
            rel = _natural_relationship(planet, sign_lord)
            if rel == "F":
                dignity = DignityLevel.FRIEND_SIGN
            elif rel == "E":
                dignity = DignityLevel.ENEMY_SIGN
            # N → stays NEUTRAL_SIGN

    # --- Combustion ---
    is_combust = False
    is_cazimi = False
    if planet not in ("Sun", "Rahu", "Ketu"):
        dist = _angular_distance(sun_longitude, planet_longitude)
        if dist <= 1.0:
            is_cazimi = True    # Cazimi — overrides combustion (very strong)
        elif planet in _COMBUST_ORB_DIRECT:
            orb = _COMBUST_ORB_DIRECT[planet]
            if is_retrograde:
                orb -= _COMBUST_ORB_RETRO_REDUCTION
            is_combust = dist <= orb

    # --- Build total modifier ---
    total = DIGNITY_WEIGHT[dignity]
    if is_retrograde:
        total += RETROGRADE_BONUS
    if is_combust and not is_cazimi:
        total += COMBUST_RETRO if is_retrograde else COMBUST_DIRECT
    if neecha_bhanga:
        total += NEECHA_BHANGA  # additional bonus on top of neutralised dignity

    sign = SIGNS[sign_idx]
    return DignityResult(
        planet=planet,
        sign=sign,
        degree_in_sign=degree_in_sign,
        dignity=dignity,
        is_deep=is_deep,
        weight=DIGNITY_WEIGHT[dignity],
        is_combust=is_combust,
        is_cazimi=is_cazimi,
        is_retrograde=is_retrograde,
        neecha_bhanga=neecha_bhanga,
        total_modifier=total,
    )


def compute_all_dignities(chart: BirthChart) -> dict[str, DignityResult]:
    """Compute dignity for all 9 planets in a BirthChart."""
    sun_lon = chart.planets["Sun"].longitude
    results = {}
    for name, p in chart.planets.items():
        results[name] = compute_dignity(
            planet=name,
            sign_idx=p.sign_index,
            degree_in_sign=p.degree_in_sign,
            is_retrograde=p.is_retrograde,
            sun_longitude=sun_lon,
            planet_longitude=p.longitude,
            lagna_sign_idx=chart.lagna_sign_index,
            chart=chart,
        )
    return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Sign rulers (classical — Rahu/Ketu get modern assignments as per REF_Planets)
_SIGN_LORD = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

def _sign_lord(sign_idx: int) -> str:
    return _SIGN_LORD[sign_idx % 12]


def _check_neecha_bhanga(
    planet: str,
    debil_sign_idx: int,
    lagna_sign_idx: int,
    chart: BirthChart | None,
) -> bool:
    """
    Simplified Neecha Bhanga: debilitation lord in a Kendra (1/4/7/10) from Lagna.
    Full BPHS conditions are more complex; this covers the most common case.
    """
    if chart is None:
        return False
    lord = _sign_lord(debil_sign_idx)
    if lord not in chart.planets:
        return False
    lord_sign_idx = chart.planets[lord].sign_index
    house = (lord_sign_idx - lagna_sign_idx) % 12 + 1
    return house in (1, 4, 7, 10)   # Kendra houses
