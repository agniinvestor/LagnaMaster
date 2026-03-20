"""
src/calculations/stronger_of_two.py — Session 59

Stronger-of-two planet comparison framework (PVRNR Ch.15 p194).

PVRNR explicit hierarchy (p194, Rudra calculation):
  1. More planets in conjunction (sign)
  2. Exaltation or own sign (if tied on #1)
  3. Joining exalted planets (if tied on #2)
  4. Aspected by more planets (rasi aspect)  (if tied on #3)
  5. More advanced in sign (higher degree)   (if tied on #4)

Used in:
  - Scorpio/Aquarius dual-lord arudha computation (Mars vs Ketu, Saturn vs Rahu)
  - Narayana Dasha start sign (stronger of lagna vs 7th)
  - Jaimini longevity (Brahma, Mahesvara, Rudra selection)
  - Any "take the stronger" rule

Public API
----------
  stronger_planet(p1, p2, chart) -> str  (returns name of stronger)
  stronger_sign(si1, si2, chart) -> int  (returns sign_index of stronger)
  planet_strength_score(planet, chart) -> PlanetStrengthScore
"""
from __future__ import annotations
from dataclasses import dataclass

_EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
_OWN      = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
              "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}

# Rasi aspect: movable aspects all fixed except adjacent; fixed aspects all movable except adjacent; dual aspects all dual
def _rasi_aspects(si: int) -> set[int]:
    """Signs aspected by sign si via rasi drishti."""
    movable = {0,3,6,9}
    fixed   = {1,4,7,10}
    dual    = {2,5,8,11}
    if si in movable:
        return fixed - {(si+1)%12}
    elif si in fixed:
        return movable - {(si-1)%12}
    else:
        return dual - {si}


@dataclass
class PlanetStrengthScore:
    planet: str
    cotenant_count: int     # #1: planets in same sign
    dignity_score: int      # #2: 2=exalt/own, 1=moolt, 0=neutral
    exalted_cotenants: int  # #3: exalted planets in same sign
    rasi_aspect_count: int  # #4: signs aspecting this sign
    degree_in_sign: float   # #5: tiebreaker

    def as_tuple(self) -> tuple:
        """For comparison — higher = stronger."""
        return (self.cotenant_count, self.dignity_score,
                self.exalted_cotenants, self.rasi_aspect_count,
                self.degree_in_sign)


def planet_strength_score(planet: str, chart) -> PlanetStrengthScore:
    pos = chart.planets.get(planet)
    if not pos:
        return PlanetStrengthScore(planet, 0, 0, 0, 0, 0.0)

    si  = pos.sign_index
    deg = getattr(pos, 'degree_in_sign', pos.longitude % 30)

    # #1: cotenants (other planets in same sign)
    cotenants = [p for p, pp in chart.planets.items()
                 if p != planet and pp.sign_index == si]
    cotenant_count = len(cotenants)

    # #2: dignity
    if _EXALT_SI.get(planet) == si or si in _OWN.get(planet, set()):
        dignity_score = 2
    else:
        _MOOLT = {"Sun":4,"Moon":1,"Mars":0,"Mercury":5,"Jupiter":8,"Venus":6,"Saturn":9}
        dignity_score = 1 if _MOOLT.get(planet) == si else 0

    # #3: exalted cotenants
    exalted_cotenants = sum(1 for p in cotenants
                             if _EXALT_SI.get(p) == chart.planets[p].sign_index)

    # #4: rasi aspects on this sign
    aspecting = sum(1 for p, pp in chart.planets.items()
                    if si in _rasi_aspects(pp.sign_index))
    rasi_aspect_count = aspecting

    return PlanetStrengthScore(
        planet=planet,
        cotenant_count=cotenant_count,
        dignity_score=dignity_score,
        exalted_cotenants=exalted_cotenants,
        rasi_aspect_count=rasi_aspect_count,
        degree_in_sign=round(deg, 4),
    )


def stronger_planet(p1: str, p2: str, chart) -> str:
    """Return the stronger of two planets per PVRNR hierarchy."""
    s1 = planet_strength_score(p1, chart)
    s2 = planet_strength_score(p2, chart)
    return p1 if s1.as_tuple() >= s2.as_tuple() else p2


def stronger_sign(si1: int, si2: int, chart) -> int:
    """
    Return the stronger of two sign indices.
    Used for Narayana Dasha start (lagna vs 7th house).
    Strength of a sign = strength of its lord.
    """
    _SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
                  6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}
    lord1 = _SIGN_LORD[si1 % 12]
    lord2 = _SIGN_LORD[si2 % 12]
    winner = stronger_planet(lord1, lord2, chart)
    return si1 if winner == lord1 else si2
