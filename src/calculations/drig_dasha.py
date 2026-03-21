"""
src/calculations/drig_dasha.py — Session 101

Drig Dasha — one of the "two rasi dasas that don't use navamsha" (PVRNR preface p8).
Used for timing events when Lagna is stronger than Moon.

Mechanism: Period lengths are determined by the number of signs aspecting each sign.
A sign receives aspects from signs 5, 7, and 9 from it (standard rasi aspects).
Stronger sign (more aspects + occupied by stronger planets) goes first if Lagna > Moon.

Duration formula (PVRNR):
  Count the number of rasi aspects received by the sign.
  Each aspecting sign contributes a fractional year.
  Base period = 12 years; modified by aspect count.

Sequence: Starts from Lagna (if Lagna > Moon) or Moon sign (if Moon > Lagna).
  Odd signs: go forward. Even signs: go backward.
  Full cycle through all 12 signs.

Source: PVRNR preface p8; BPHS Ch.41-43.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

_SIGN_NAMES = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
               "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

# Standard rasi aspects: every sign aspects the 7th from it.
# Special: Aries,Cancer,Libra,Capricorn also aspect 4th and 8th.
#          Taurus,Leo,Scorpio,Aquarius also aspect 3rd and 10th (via trines).
#          Gemini,Virgo,Sagittarius,Pisces also aspect 5th and 9th.
_SPECIAL_ASPECTS = {
    0: {3, 6, 7},   # Ar → Cn, Li, 7th
    1: {2, 9, 6},   # Ta → Ge, Cp, Li (via trine + 7th)
    2: {4, 8, 7},   # Ge → Le, Sg, 7th
    3: {6, 9, 0},   # Cn → Li, Cp, Ar
    4: {5, 1, 10},  # Le → Vi, Ta, Aq
    5: {7, 11, 8},  # Vi → Sc, Pi, Sg
    6: {9, 0, 3},   # Li → Cp, Ar, Cn
    7: {10, 4, 1},  # Sc → Aq, Le, Ta
    8: {10, 2, 5},  # Sg → Aq, Ge, Vi
    9: {11, 3, 6},  # Cp → Pi, Cn, Li
    10: {8, 4, 7},  # Aq → Sg, Le, Sc
    11: {1, 5, 8},  # Pi → Ta, Vi, Sg
}


def _aspects_received(sign_index: int) -> set[int]:
    """Return set of sign indices that aspect this sign."""
    return {s for s, targets in _SPECIAL_ASPECTS.items()
            if sign_index in targets}


def _drig_period_years(sign_index: int, chart) -> float:
    """
    Period length for a sign in Drig Dasha.
    Base = number of planets in the sign + aspects received (count).
    Scale to reasonable dasha periods.
    """
    aspects = len(_aspects_received(sign_index))
    planets_in = sum(1 for p, pos in chart.planets.items()
                     if pos.sign_index == sign_index)
    # Base formula: aspects contribute more weight
    years = max(1.0, aspects * 1.5 + planets_in * 0.5)
    return round(min(years, 12.0), 1)


@dataclass
class DrigPeriod:
    sign: str
    sign_index: int
    years: float
    start_date: date
    end_date: date
    aspects_received: int
    planets_in_sign: list[str]


def compute_drig_dasha(chart, birth_date: date) -> list[DrigPeriod]:
    """
    Compute Drig Dasha from birth.
    Start: Lagna sign (if Lagna lord stronger) or Moon sign.
    Sequence: odd signs go forward, even signs go backward.
    """
    lagna_si = chart.lagna_sign_index
    moon_pos = chart.planets.get("Moon")

    # Determine starting sign (simplified: use lagna)
    # Full rule: compare Lagna lord strength vs Moon strength
    start_si = lagna_si
    is_odd = (start_si % 2 == 0)  # 0=Aries is odd in Jyotish

    # Build 12-sign sequence
    if is_odd:
        seq = [(start_si + i) % 12 for i in range(12)]
    else:
        seq = [(start_si - i) % 12 for i in range(12)]

    # Elapsed in first period (Moon fraction)
    nak_frac = 0.0
    if moon_pos:
        nak_frac = (moon_pos.longitude % 30) / 30.0

    current_date = birth_date
    periods = []
    for i, si in enumerate(seq):
        years = _drig_period_years(si, chart)
        if i == 0:
            elapsed = nak_frac * years
            current_date = birth_date + timedelta(days=-int(elapsed * 365.25))
        end = current_date + timedelta(days=int(years * 365.25))
        planets_in = [p for p, pos in chart.planets.items()
                      if pos.sign_index == si]
        periods.append(DrigPeriod(
            sign=_SIGN_NAMES[si], sign_index=si, years=years,
            start_date=current_date, end_date=end,
            aspects_received=len(_aspects_received(si)),
            planets_in_sign=planets_in,
        ))
        current_date = end

    return periods
