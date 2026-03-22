"""
src/calculations/shoola_dasha.py — Session 95

Two additional rasi dasas from PVRNR textbook (preface p8):

1. Shoola Dasha — Ayur dasa for longevity timing
   Based on trines. Involves the three Shoola (trident) rasis.
   Sequence determined by odd/even lagna.

2. Sudasa — Rasi dasa for timing material success
   Based on a specific sequence of signs from the 8th house.
   Duration based on count of planets in each sign.

Both are rasi (sign-based) dasas; the active sign becomes the focus
of that period's events.

Source: BPHS, PVRNR preface ("Lagna Kendradi Rasi dasa and Sudasa
for timing material success") and standard references.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

_SIGN_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


@dataclass
class ShoolarasiPeriod:
    sign: str
    sign_index: int
    years: float
    start_date: date
    end_date: date
    trishoola_spike: bool  # one of the three Shoola rasis


@dataclass
class SudasaPeriod:
    sign: str
    sign_index: int
    years: float
    start_date: date
    end_date: date
    planets_in_sign: list[str]


def compute_shoola_dasha(chart, birth_date: date) -> list[ShoolarasiPeriod]:
    """
    Shoola Dasha (BPHS). Sequence based on Lagna.
    Odd Lagna → forward from Lagna; Even Lagna → reverse.
    Duration: each sign = number of planets in it + 1 year (simplified).
    Trishoola signs: Rudra's nakshatra sign and its two trines.
    """
    lagna_si = chart.lagna_sign_index
    is_odd_lagna = lagna_si % 2 == 0  # 0=Aries (odd)

    # Count planets per sign
    planet_count = {i: 0 for i in range(12)}
    for p, pos in chart.planets.items():
        planet_count[pos.sign_index] += 1

    # Generate sequence (12 signs from lagna in forward or reverse order)
    if is_odd_lagna:
        seq = [(lagna_si + i) % 12 for i in range(12)]
    else:
        seq = [(lagna_si - i) % 12 for i in range(12)]

    # Trishoola: lagna sign and its two trines
    trishoola = {lagna_si, (lagna_si + 4) % 12, (lagna_si + 8) % 12}

    # Elapsed fraction in first sign
    moon_pos = chart.planets.get("Moon")
    nak_fraction = 0.0
    if moon_pos:
        moon_lon = moon_pos.longitude % 360
        nak_fraction = (moon_lon % 30) / 30.0

    current_date = birth_date
    periods = []
    for i, si in enumerate(seq):
        years = max(1.0, float(planet_count[si] + 1))
        if i == 0:
            elapsed = nak_fraction * years
            current_date = birth_date + timedelta(days=-int(elapsed * 365.25))
        end = current_date + timedelta(days=int(years * 365.25))
        periods.append(
            ShoolarasiPeriod(
                sign=_SIGN_NAMES[si],
                sign_index=si,
                years=years,
                start_date=current_date,
                end_date=end,
                trishoola_spike=si in trishoola,
            )
        )
        current_date = end

    return periods


def compute_sudasa(chart, birth_date: date) -> list[SudasaPeriod]:
    """
    Sudasa — Rasi dasa for material success. PVRNR preface.
    Sequence starts from the stronger of Lagna or 8th house lord's sign.
    Duration: proportional to SAV bindus or fixed 1-12 year range.
    """
    from src.calculations.stronger_of_two import stronger_sign

    lagna_si = chart.lagna_sign_index
    eighth_si = (lagna_si + 7) % 12
    # Start from stronger of lagna or 8th
    start_si = stronger_sign(lagna_si, eighth_si, chart)

    planet_count = {i: 0 for i in range(12)}
    planets_in = {i: [] for i in range(12)}
    for p, pos in chart.planets.items():
        planet_count[pos.sign_index] += 1
        planets_in[pos.sign_index].append(p)

    # Sudasa: odd/even sequence from start sign
    is_odd = start_si % 2 == 0
    seq = (
        [(start_si + i) % 12 for i in range(12)]
        if is_odd
        else [(start_si - i) % 12 for i in range(12)]
    )

    current_date = birth_date
    periods = []
    for si in seq:
        # Duration proportional to planets in sign (1 year minimum, 12 max)
        years = min(12.0, max(1.0, float(planet_count[si] + 1) * 1.5))
        end = current_date + timedelta(days=int(years * 365.25))
        periods.append(
            SudasaPeriod(
                sign=_SIGN_NAMES[si],
                sign_index=si,
                years=round(years, 1),
                start_date=current_date,
                end_date=end,
                planets_in_sign=planets_in[si],
            )
        )
        current_date = end

    return periods
