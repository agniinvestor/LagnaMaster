"""
src/calculations/orb_strength.py — Session 57

Orb-sensitive association strength (PVRNR Ch.11 p135).

PVRNR explicitly: "conjunction should be close (say, within 6°)".
Example: 8° apart = weak; <1° = maximum strength (p149 Akbar example).

Strength curve (continuous, not binary):
  0° → 1.00  (full strength)
  3° → 0.75
  6° → 0.50  (PVRNR threshold — "within 6° or so")
  8° → 0.33  (weak, p149)
 15° → 0.00  (no effective conjunction)

Formula: strength = max(0, 1 - orb_degrees / 15)

Aspect strength uses same formula but PVRNR does not specify orb for aspects —
we use 12° for full aspects (graha drishti), 8° for rasi aspects.

Public API
----------
  conjunction_strength(p1_lon, p2_lon) -> float  0.0–1.0
  aspect_strength(p1_lon, p2_lon, aspect_type) -> float
  yoga_conjunction_strength(yoga_planets, chart) -> float
  association_strength(p1, p2, chart) -> AssociationStrength
"""
from __future__ import annotations
from dataclasses import dataclass

_CONJ_ORB_FULL = 15.0   # beyond this = no conjunction
_CONJ_PVRNR_6  = 6.0    # PVRNR threshold for "close"
_ASPECT_ORB    = 12.0   # for graha drishti


def _circular_diff(lon1: float, lon2: float) -> float:
    """Absolute circular distance between two longitudes (0–180°)."""
    diff = abs(lon1 - lon2) % 360
    return min(diff, 360 - diff)


def conjunction_strength(lon1: float, lon2: float) -> float:
    """
    0.0–1.0 strength of conjunction based on orb.
    PVRNR threshold: within 6° = strong; 8° = weak.
    """
    orb = _circular_diff(lon1, lon2)
    if orb >= _CONJ_ORB_FULL:
        return 0.0
    return round(max(0.0, 1.0 - orb / _CONJ_ORB_FULL), 4)


def aspect_strength(p1_lon: float, p2_lon: float,
                    aspect_type: str = "graha") -> float:
    """
    Strength of a graha drishti aspect.
    aspect_type: 'graha' (7th full, 4th/8th Mars, 5th/9th Jupiter, 3rd/10th Saturn)
    """
    diff = _circular_diff(p1_lon, p2_lon)
    # For 7th aspect: target is 180° ± orb
    # We compute general orb from nearest aspect angle
    sign_diff = int(diff / 30)
    remainder = diff % 30
    # Nearest aspect angle
    nearest = min(remainder, 30 - remainder)
    if nearest >= _ASPECT_ORB:
        return 0.0
    return round(max(0.0, 1.0 - nearest / _ASPECT_ORB), 4)


@dataclass
class AssociationStrength:
    planet1: str
    planet2: str
    orb_degrees: float
    strength: float          # 0.0–1.0
    quality: str             # "Tight"/"Strong"/"Moderate"/"Weak"/"Absent"
    in_same_sign: bool
    parivartana: bool        # mutual exchange of signs

    def reduces_yoga(self) -> bool:
        """True if orb too wide to deliver full yoga results (PVRNR > 8°)."""
        return self.orb_degrees > 8.0

    def is_pvrnr_close(self) -> bool:
        """True if within PVRNR's 6° threshold."""
        return self.orb_degrees <= 6.0


def association_strength(p1: str, p2: str, chart) -> AssociationStrength:
    """
    Compute full association strength between two planets.
    Includes conjunction orb, same-sign check, and parivartana.
    """
    pos1 = chart.planets.get(p1)
    pos2 = chart.planets.get(p2)
    if not pos1 or not pos2:
        return AssociationStrength(p1, p2, 360.0, 0.0, "Absent", False, False)

    orb = _circular_diff(pos1.longitude, pos2.longitude)
    strength = conjunction_strength(pos1.longitude, pos2.longitude)
    same_sign = pos1.sign_index == pos2.sign_index

    if strength >= 0.90:  q = "Tight"
    elif strength >= 0.60: q = "Strong"
    elif strength >= 0.33: q = "Moderate"
    elif strength > 0.0:   q = "Weak"
    else:                  q = "Absent"

    # Parivartana: each planet in sign owned by the other
    _SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
                  6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}
    lord1 = _SIGN_LORD[pos1.sign_index % 12]
    lord2 = _SIGN_LORD[pos2.sign_index % 12]
    parivartana = (lord1 == p2 and lord2 == p1)

    return AssociationStrength(
        planet1=p1, planet2=p2, orb_degrees=round(orb, 3),
        strength=strength, quality=q,
        in_same_sign=same_sign, parivartana=parivartana,
    )


def yoga_conjunction_strength(yoga_planets: list[str], chart) -> float:
    """
    For a multi-planet yoga, return the minimum pairwise conjunction strength.
    The weakest link determines the yoga's effective strength.
    PVRNR: "final judgment considers all factors".
    """
    if len(yoga_planets) < 2:
        return 1.0
    strengths = []
    for i in range(len(yoga_planets)):
        for j in range(i+1, len(yoga_planets)):
            s = association_strength(yoga_planets[i], yoga_planets[j], chart)
            if s.in_same_sign:
                strengths.append(s.strength)
    return round(min(strengths), 4) if strengths else 0.5
