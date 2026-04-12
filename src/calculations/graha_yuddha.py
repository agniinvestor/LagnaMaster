"""
src/calculations/graha_yuddha.py — Planetary War (Graha Yuddha)

Two planets within 1° longitude in the same sign are at war.
Winner: planet with higher northward (celestial) latitude.
Tiebreaker: planet with greater speed (more energetic).

Source: BPHS Ch.28 v.1-12; Saravali Ch.66-68 v.7-13

The loser loses Shadbala strength and functional beneficence.
Only the 5 non-luminary, non-nodal planets can war:
  Mars, Mercury, Jupiter, Venus, Saturn.

Public API
----------
    compute_graha_yuddha(chart) -> list[YuddhaResult]
"""

from __future__ import annotations
from dataclasses import dataclass

from src.data.constants import SIGN_NAMES


@dataclass
class YuddhaResult:
    winner: str
    loser: str
    separation_degrees: float
    loser_longitude: float
    winner_longitude: float
    sign: str
    winner_reason: str  # "north_latitude" / "higher_speed"
    functional_impact: str


_WAR_PLANETS = {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}


def compute_graha_yuddha(chart) -> list[YuddhaResult]:
    """Detect all planetary wars in the chart.

    War condition: two war-eligible planets within 1° longitude in the same sign.
    Winner: higher northward celestial latitude (BPHS Ch.28 v.7-12).
    Tiebreaker: higher speed.
    """
    wars = []
    planets = list(_WAR_PLANETS)
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

            # Winner = higher northward latitude (BPHS Ch.28, Saravali Ch.66-68)
            lat1 = getattr(pos1, "latitude", 0.0)
            lat2 = getattr(pos2, "latitude", 0.0)

            if lat1 > lat2:
                winner, loser = p1, p2
                reason = "north_latitude"
            elif lat2 > lat1:
                winner, loser = p2, p1
                reason = "north_latitude"
            else:
                # Tiebreaker: higher speed (more energetic)
                speed1 = abs(getattr(pos1, "speed", 0.0))
                speed2 = abs(getattr(pos2, "speed", 0.0))
                if speed1 >= speed2:
                    winner, loser = p1, p2
                else:
                    winner, loser = p2, p1
                reason = "higher_speed"

            w_pos = chart.planets[winner]
            l_pos = chart.planets[loser]
            impact = (
                f"{loser} loses planetary war to {winner} — "
                f"{loser}'s significations and strength severely reduced"
            )
            wars.append(
                YuddhaResult(
                    winner=winner,
                    loser=loser,
                    separation_degrees=round(sep, 3),
                    loser_longitude=round(l_pos.longitude, 4),
                    winner_longitude=round(w_pos.longitude, 4),
                    sign=SIGN_NAMES[pos1.sign_index],
                    winner_reason=reason,
                    functional_impact=impact,
                )
            )
    return wars
