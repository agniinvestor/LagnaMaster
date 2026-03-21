"""
src/calculations/graha_yuddha.py — LagnaMaster Session 32

Planetary war (Graha Yuddha) — when two planets are within 1° longitude
in the same sign, a war occurs. The planet with lesser latitude LOSES.
(Simplified: the one with lesser longitude loses in most traditions.)

The loser loses Shadbala strength and functional beneficence.
Only the 5 non-luminary, non-nodal planets can war:
  Mars, Mercury, Jupiter, Venus, Saturn.

Public API
----------
    compute_graha_yuddha(chart) -> list[YuddhaResult]
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class YuddhaResult:
    winner: str
    loser: str
    separation_degrees: float
    loser_longitude: float
    winner_longitude: float
    sign: str
    functional_impact: str   # how this affects the chart


_WAR_PLANETS = {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]


def compute_graha_yuddha(chart) -> list[YuddhaResult]:
    """Detect all planetary wars in the chart."""
    wars = []
    planets = list(_WAR_PLANETS)  # noqa: F841
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            p1, p2 = planets[i], planets[j]
            pos1 = chart.planets.get(p1)
            pos2 = chart.planets.get(p2)
            if pos1 is None or pos2 is None:
                continue
            if pos1.sign_index != pos2.sign_index:
                continue
            sep = abs(pos1.degree_in_sign - pos2.degree_in_sign)
            if sep > 1.0:
                continue
            # Loser = lesser longitude (lesser degree within sign in most traditions)
            if pos1.longitude < pos2.longitude:
                loser, winner = p1, p2
                loser_lon, winner_lon = pos1.longitude, pos2.longitude
            else:
                loser, winner = p2, p1
                loser_lon, winner_lon = pos2.longitude, pos1.longitude

            impact = (f"{loser} loses planetary war to {winner} — "
                      f"{loser}'s significations and strength severely reduced")
            wars.append(YuddhaResult(
                winner=winner, loser=loser,
                separation_degrees=round(sep, 3),
                loser_longitude=round(loser_lon, 4),
                winner_longitude=round(winner_lon, 4),
                sign=_SIGNS[pos1.sign_index],
                functional_impact=impact,
            ))
    return wars
