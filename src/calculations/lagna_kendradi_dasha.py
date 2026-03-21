"""
src/calculations/lagna_kendradi_dasha.py — Session 102

Lagna Kendradi Rasi Dasha — PVRNR preface p8.
"Lagna Kendradi Rasi dasa" is explicitly named as one of the standard
rasi dasas in PVRNR's preface list.

Mechanism: Signs are grouped from Lagna by house type:
  Group 1: Kendra (1,4,7,10) from Lagna
  Group 2: Panapara (2,5,8,11) from Lagna
  Group 3: Apoklima (3,6,9,12) from Lagna

Sequence within each group: follow Zodiac order.
Duration: number of planets in sign + 1 (minimum 1, maximum 12 years).
Odd sign of Lagna: forward. Even sign of Lagna: reverse.

Source: PVRNR preface p8; BPHS Lagna Kendradi chapters.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

_SIGN_NAMES = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
               "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]


@dataclass
class LagnaKendradiPeriod:
    sign: str
    sign_index: int
    group: str        # "Kendra" | "Panapara" | "Apoklima"
    years: float
    start_date: date
    end_date: date


def compute_lagna_kendradi_dasha(chart, birth_date: date) -> list[LagnaKendradiPeriod]:
    """Compute Lagna Kendradi Rasi Dasha periods."""
    lagna_si = chart.lagna_sign_index
    is_odd = (lagna_si % 2 == 0)  # Aries=0 is odd

    # Count planets per sign
    planet_count = {i: 0 for i in range(12)}
    for p, pos in chart.planets.items():
        planet_count[pos.sign_index] += 1

    # Build groups relative to Lagna
    def _house_sign(house_offset):
        return (lagna_si + house_offset) % 12

    kendra   = [_house_sign(i) for i in [0, 3, 6, 9]]
    panapara = [_house_sign(i) for i in [1, 4, 7, 10]]
    apoklima = [_house_sign(i) for i in [2, 5, 8, 11]]

    # Within each group: odd Lagna = zodiac order, even = reverse
    if not is_odd:
        kendra   = list(reversed(kendra))
        panapara = list(reversed(panapara))
        apoklima = list(reversed(apoklima))

    sequence = ([(s, "Kendra")   for s in kendra] +
                [(s, "Panapara") for s in panapara] +
                [(s, "Apoklima") for s in apoklima])

    # Elapsed
    moon_pos = chart.planets.get("Moon")
    nak_frac = ((moon_pos.longitude % 30) / 30.0) if moon_pos else 0.0

    current_date = birth_date
    periods = []
    for i, (si, group) in enumerate(sequence):
        years = max(1.0, float(planet_count[si] + 1))
        if i == 0:
            elapsed = nak_frac * years
            current_date = birth_date + timedelta(days=-int(elapsed * 365.25))
        end = current_date + timedelta(days=int(years * 365.25))
        periods.append(LagnaKendradiPeriod(
            sign=_SIGN_NAMES[si], sign_index=si,
            group=group, years=years,
            start_date=current_date, end_date=end,
        ))
        current_date = end

    return periods
