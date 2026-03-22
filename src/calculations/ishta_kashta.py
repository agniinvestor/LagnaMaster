"""
src/calculations/ishta_kashta.py — Session 41

Ishta Phala (benefic effect) and Kashta Phala (malefic effect) per planet.
BPHS formula (Ch.27):
  Ishta  = √(Uchcha_Bala × Cheshta_Bala)   max = 60 Virupas
  Kashta = √((60-Uchcha_Bala) × (60-Cheshta_Bala))   max = 60 Virupas
Net Sphuta = Ishta - Kashta  (range −60 to +60)

Uchcha Bala = positional strength based on exaltation/debilitation distance.
Cheshta Bala = motional strength (direct/retrograde/speed).
"""

from __future__ import annotations
from dataclasses import dataclass
import math

_EXALT_LON = {
    "Sun": 10,
    "Moon": 33,
    "Mars": 298,
    "Mercury": 165,
    "Jupiter": 95,
    "Venus": 357,
    "Saturn": 200,
}
_DEBIL_LON = {
    "Sun": 190,
    "Moon": 213,
    "Mars": 118,
    "Mercury": 345,
    "Jupiter": 275,
    "Venus": 177,
    "Saturn": 20,
}

# Mean motion (degrees/day) for Cheshta Bala
_MEAN_MOTION = {
    "Sun": 0.9856,
    "Moon": 13.1764,
    "Mars": 0.5240,
    "Mercury": 1.3833,
    "Jupiter": 0.0831,
    "Venus": 1.2000,
    "Saturn": 0.0335,
}


def _uchcha_bala(planet: str, longitude: float) -> float:
    """Uchcha Bala: 0–60 Virupas based on distance from exaltation/debilitation."""
    exalt = _EXALT_LON.get(planet)
    _DEBIL_LON.get(planet)
    if exalt is None:
        return 30.0  # Rahu/Ketu: neutral
    # Angular distance from exaltation (shorter arc)
    diff = abs(longitude - exalt) % 360
    if diff > 180:
        diff = 360 - diff
    # At exaltation → 60, at debilitation → 0
    return max(0.0, min(60.0, 60.0 - (diff / 180.0) * 60.0))


def _cheshta_bala(planet: str, speed: float) -> float:
    """Cheshta Bala: motional strength. Retrograde = full 60, stationary = 30."""
    if planet in ("Sun", "Moon"):
        return 30.0  # Sun/Moon never retrograde; use 30 Virupas
    mean = _MEAN_MOTION.get(planet, 0.5)
    if speed < 0:  # retrograde
        return 60.0
    elif speed < mean * 0.1:  # nearly stationary
        return 30.0
    else:
        ratio = min(speed / mean, 2.0)
        return min(60.0, ratio * 30.0)


@dataclass
class IshtaKashta:
    planet: str
    uchcha_bala: float
    cheshta_bala: float
    ishta: float  # √(Uchcha × Cheshta)
    kashta: float  # √((60-Uchcha) × (60-Cheshta))
    net_sphuta: float  # Ishta - Kashta


def compute_ishta_kashta(chart) -> dict[str, IshtaKashta]:
    """Compute Ishta/Kashta Phala for all 7 planets."""
    result = {}
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        pos = chart.planets.get(planet)
        if not pos:
            continue
        ub = _uchcha_bala(planet, pos.longitude)
        cb = _cheshta_bala(planet, getattr(pos, "speed", _MEAN_MOTION.get(planet, 0.5)))
        ishta = round(math.sqrt(ub * cb), 3)
        kashta = round(math.sqrt(max(0, 60 - ub) * max(0, 60 - cb)), 3)
        result[planet] = IshtaKashta(
            planet=planet,
            uchcha_bala=round(ub, 3),
            cheshta_bala=round(cb, 3),
            ishta=ishta,
            kashta=kashta,
            net_sphuta=round(ishta - kashta, 3),
        )
    return result
