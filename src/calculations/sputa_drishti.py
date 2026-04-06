"""
src/calculations/sputa_drishti.py
Sputa Drishti — exact degree-based aspect strength.
Session 128 (Phase 2).

Classical texts give aspectual influence as a function of the exact
longitudinal arc between aspector and aspected point.

Sources:
  Saravali Ch.3 (aspect orbs and partial strengths)
  Sarvartha Chintamani — aspectual strength table
  BPHS Ch.26 v.1-10 (full/partial aspects)
"""

from __future__ import annotations
from dataclasses import dataclass


# ─── BPHS Ch.26 v.6-8 Drishti Kona (speculum-based) ────────────────────────
# Piecewise linear function verified against the Speculum of Aspectual Values
# (pp.258-262). Maximum 60 virupas at 180° (full aspect = 1 Rupa).
# No aspect in 0°-30° and 300°-360° arcs.

def bphs_drishti_virupas(arc_degrees: float) -> float:
    """
    BPHS Ch.26 v.6-8: continuous aspect strength in virupas (0-60).

    arc_degrees: angular distance from aspector to aspected (0-360).
    Returns virupas of aspectual strength.

    Verified against BPHS speculum table (pp.258-262, Santhanam Vol 1).
    """
    a = arc_degrees % 360.0
    if a < 30.0 or a >= 300.0:
        return 0.0
    if a < 60.0:
        return (a - 30.0) / 2.0  # 0→15
    if a < 90.0:
        return (a - 60.0) + 15.0  # 15→45
    if a < 120.0:
        return (120.0 - a) / 2.0 + 30.0  # 45→30
    if a < 150.0:
        return 150.0 - a  # 30→0
    if a < 180.0:
        return (a - 150.0) * 2.0  # 0→60
    return (300.0 - a) / 2.0  # 60→0 (180-300)


# Special aspect houses where Mars/Jupiter/Saturn get full (60 virupa) strength
# BPHS Ch.26 v.9-12
_SPECIAL_ASPECT_HOUSES: dict[str, set[int]] = {
    "Mars": {4, 8},      # 4th and 8th from aspector
    "Jupiter": {5, 9},   # 5th and 9th
    "Saturn": {3, 10},   # 3rd and 10th
}


def bphs_drishti_with_specials(
    aspector: str, arc_degrees: float
) -> float:
    """
    BPHS drishti including special aspect boost for Mars/Jupiter/Saturn.

    At special aspect houses, the base strength is boosted to full (60 virupas)
    using a smooth interpolation within ±15° of the house center.
    BPHS Ch.26 v.9-12.
    """
    base = bphs_drishti_virupas(arc_degrees)
    special_houses = _SPECIAL_ASPECT_HOUSES.get(aspector)
    if not special_houses:
        return base

    # Check proximity to special aspect house centers
    a = arc_degrees % 360.0
    for house in special_houses:
        center = (house - 1) * 30.0  # house 4 → 90°, house 8 → 210°, etc.
        diff = min(abs(a - center), 360.0 - abs(a - center))
        if diff <= 15.0:
            # Within the special aspect house: boost to 60 virupas
            # with linear interpolation from house edge to center
            special_strength = 60.0 * (1.0 - diff / 15.0)
            return max(base, special_strength)
    return base

# ─── Aspect orb definitions ───────────────────────────────────────────────────
# Each planet can cast a full (100%), three-quarter (75%), half (50%),
# or quarter (25%) aspect depending on the arc from the aspector.
#
# Standard Parashari aspects:
# - All planets: full aspect at 180° (7th house)
# - Mars: additional full at 4th (90°) and 8th (210°)  — per BPHS 3/4 strength
# - Jupiter: additional at 5th (120°) and 9th (240°)   — 3/4 strength
# - Saturn: additional at 3rd (60°) and 10th (270°)    — 3/4 strength
#
# For Sputa Drishti, the strength varies smoothly with exact degrees


@dataclass
class AspectResult:
    aspector: str
    aspected_longitude: float
    arc_degrees: float  # 0-360 from aspector to aspected
    strength: float  # 0.0 to 1.0
    aspect_type: str  # "full" / "three_quarter" / "none"


# House-based aspect strength table (BPHS Ch.26)
# Keys: houses from aspector planet
_ASPECT_TABLE: dict[str, dict[int, float]] = {
    "Sun": {7: 1.0},
    "Moon": {7: 1.0},
    "Mars": {4: 0.75, 7: 1.0, 8: 0.75},
    "Mercury": {7: 1.0},
    "Jupiter": {5: 0.75, 7: 1.0, 9: 0.75},
    "Venus": {7: 1.0},
    "Saturn": {3: 0.75, 7: 1.0, 10: 0.75},
    "Rahu": {7: 1.0, 5: 0.75, 9: 0.75},  # some schools give Rahu Jupiter-like aspects
    "Ketu": {7: 1.0, 4: 0.75, 8: 0.75},  # Ketu Mars-like aspects per some schools
}

# House-center degrees for orb calculation
_HOUSE_CENTER_DEGREES: dict[int, float] = {
    1: 0.0,
    2: 30.0,
    3: 60.0,
    4: 90.0,
    5: 120.0,
    6: 150.0,
    7: 180.0,
    8: 210.0,
    9: 240.0,
    10: 270.0,
    11: 300.0,
    12: 330.0,
}

# Orb for aspect (degrees of arc before/after which aspect starts/fades)
ASPECT_ORB = 15.0  # degrees either side of exact aspect


def _arc(from_lon: float, to_lon: float) -> float:
    """Arc in degrees from aspector to aspected (0-360, anticlockwise)."""
    return (to_lon - from_lon) % 360.0


def _house_from_arc(arc: float) -> int:
    """Whole-sign house count from arc (1-12)."""
    return int(arc / 30) + 1


def sputa_drishti_strength(
    aspector: str,
    aspector_lon: float,
    aspected_lon: float,
    use_orbs: bool = True,
) -> float:
    """
    Compute Sputa Drishti strength (0.0 to 1.0) between aspector and aspected.

    When use_orbs=True: strength fades linearly within ±15° of exact aspect arc.
    When use_orbs=False: returns full strength if within aspect house, 0.0 otherwise.

    Source: Saravali Ch.3; BPHS Ch.26
    """
    aspect_table = _ASPECT_TABLE.get(aspector, {7: 1.0})
    arc = _arc(aspector_lon, aspected_lon)
    house = _house_from_arc(arc)

    base_strength = aspect_table.get(house, 0.0)
    if base_strength == 0.0:
        # Check adjacent houses for orb effect
        if not use_orbs:
            return 0.0
        # Check if near a valid aspect arc
        max_nearby = 0.0
        for asp_house, asp_str in aspect_table.items():
            center = _HOUSE_CENTER_DEGREES[asp_house]
            diff = min(abs(arc - center), 360 - abs(arc - center))
            if diff < ASPECT_ORB:
                fade = 1.0 - (diff / ASPECT_ORB)
                max_nearby = max(max_nearby, asp_str * fade)
        return round(max_nearby, 4)

    if not use_orbs:
        return base_strength

    # Apply orb fade: full strength at center of house, fades at edges
    center = _HOUSE_CENTER_DEGREES[house]
    diff = min(abs(arc - center), 360 - abs(arc - center))
    if diff <= ASPECT_ORB:
        # Linear fade in last 15° of house arc (house = 30°, so fade in outer half)
        fade_start = 15.0 - ASPECT_ORB / 2
        if diff > fade_start:
            fade = 1.0 - (diff - fade_start) / (ASPECT_ORB / 2)
            return round(base_strength * max(0.0, fade), 4)

    return base_strength


def compute_all_aspects(
    planet: str,
    planet_lon: float,
    target_lons: dict[str, float],
) -> list[AspectResult]:
    """
    Compute all aspects from a planet to a set of target longitudes.
    Returns only aspects with strength > 0.
    """
    results = []
    for target_name, target_lon in target_lons.items():
        if target_name == planet:
            continue
        arc = _arc(planet_lon, target_lon)
        strength = sputa_drishti_strength(planet, planet_lon, target_lon)
        if strength > 0:
            results.append(
                AspectResult(
                    aspector=planet,
                    aspected_longitude=target_lon,
                    arc_degrees=round(arc, 4),
                    strength=strength,
                    aspect_type="full" if strength >= 1.0 else "three_quarter",
                )
            )
    return results


def get_aspect_strength(aspector: str, houses_away: int) -> float:
    """
    Simple house-based aspect strength lookup.
    houses_away: 1-12 counting from aspector's position.
    Returns 0.0 if no aspect, else 0.75 or 1.0.
    """
    if houses_away == 7:
        return 1.0
    table = _ASPECT_TABLE.get(aspector, {7: 1.0})
    return table.get(houses_away, 0.0)
