"""
Pushkara Navamsha — auspicious navamsha positions (Session 11).

There are 24 Pushkara Navamshas in the zodiac: exactly 2 per sign, each
spanning one navamsha (3°20' = 3.333...°).  A planet positioned in any
of these zones is said to receive "Pushkara" (nourishing/supporting)
strength — considered highly auspicious in Parashari Jyotish.

Source: Uttara Kalamrita, BPHS navamsha-strength chapter, and
Jaimini Sutras (cross-checked against Jagannatha Hora output).

Used by scoring.py Rule R21:
    bhavesh in Pushkara Navamsha → +0.5 per house
"""
from __future__ import annotations

_NAVAMSHA_WIDTH: float = 10.0 / 3.0  # exactly 3°20'

_PUSHKARA_STARTS: dict[int, tuple[float, float]] = {
    0:  (18 + 20/60,  25.0),
    1:  ( 3 + 20/60,  28 + 20/60),
    2:  (13 + 20/60,  25.0),
    3:  ( 1 + 40/60,  25.0),
    4:  (11 + 40/60,  19 + 10/60),
    5:  (23 + 20/60,  28 + 20/60),
    6:  ( 0.0,        23 + 20/60),
    7:  (19 + 10/60,  28 + 20/60),
    8:  ( 5.0,        23 + 20/60),
    9:  (10.0,        28 + 20/60),
   10:  ( 6 + 40/60,  25.0),
   11:  (13 + 20/60,  25.0),
}

_SIGN_NAMES = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
]


def is_pushkara_navamsha(sign_index: int, degree_in_sign: float) -> bool:
    if not (0 <= sign_index <= 11):
        return False
    for start in _PUSHKARA_STARTS[sign_index]:
        if start <= degree_in_sign < start + _NAVAMSHA_WIDTH:
            return True
    return False


def pushkara_navamsha_planets(chart) -> list[str]:
    result: list[str] = []
    for name, pos in chart.planets.items():
        if is_pushkara_navamsha(pos.sign_index, pos.degree_in_sign):
            result.append(name)
    return result


def pushkara_navamsha_zones(sign_index: int) -> list[tuple[float, float]]:
    starts = _PUSHKARA_STARTS.get(sign_index, (0.0, 0.0))
    return [(s, s + _NAVAMSHA_WIDTH) for s in starts]


def pushkara_strength_label(sign_index: int, degree_in_sign: float) -> str:
    return "Pushkara Navamsha" if is_pushkara_navamsha(sign_index, degree_in_sign) else ""
