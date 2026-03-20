"""
src/calculations/kalachakra_dasha.py — Session 94

Kalachakra Dasha — "most respectable dasha" per Parasara (PVRNR p8).
Based on the Navamsha (D9) position of Moon at birth.

The zodiac is divided into groups of nakshatras:
  Deha: Moon's nakshatra group (determines body/outer manifestation)
  Jeeva: alternate group (life force / inner nature)

Kalachakra cycles through signs in a specific sequence depending on
the pada (quarter) of the Moon's nakshatra.

BPHS canonical version used (avoids the version contradictions noted
in earlier documentation — the BPHS Ch.36-42 version is implemented here).

Structure:
  9 signs in each of 4 groups (Savya/Apasavya forward/reverse)
  Each sign has a dasha period (years)
  Total cycle = 100 years
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

# Kalachakra sign sequences and periods (BPHS Ch.36)
# Savya (forward) groups: padas 1 & 2 of each nakshatra
# Apasavya (reverse) groups: padas 3 & 4 of each nakshatra

_SAVYA_SEQ    = ["Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg"]
_APASAVYA_SEQ = ["Sg","Sc","Li","Vi","Le","Cn","Ge","Ta","Ar"]

# Dasha periods in years for each sign in the sequence
_KC_PERIODS = {
    "Ar":7, "Ta":16, "Ge":9, "Cn":21, "Le":5, "Vi":9, "Li":16, "Sc":7, "Sg":10,
    "Cp":4, "Aq":4, "Pi":1
}

_SIGN_ABBR = ["Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg","Cp","Aq","Pi"]

# Nakshatra group → which sequence applies, and which sign starts the cycle
_NAK_GROUP = {}
_groups = [
    (range(0,3),  "savya",    0),   # Ashwini-Bharani-Krittika → Ar-Ta-Ge...
    (range(3,6),  "apasavya", 3),   # Rohini-Mrigashira-Ardra → Cn-Le-Vi (reverse)
    (range(6,9),  "savya",    6),   # Punarvasu-Pushya-Ashlesha → Li-Sc-Sg...
    (range(9,12), "apasavya", 9),   # etc.
    (range(12,15),"savya",    0),
    (range(15,18),"apasavya", 3),
    (range(18,21),"savya",    6),
    (range(21,24),"apasavya", 9),
    (range(24,27),"savya",    0),
]
for _nak_range, _type, _start_sign in _groups:
    for _n in _nak_range:
        _NAK_GROUP[_n] = (_type, _start_sign)


@dataclass
class KalachakraPeriod:
    sign: str
    sign_index: int
    years: int
    start_date: date
    end_date: date
    is_deha: bool     # body sign (first in cycle)
    is_jeeva: bool    # life sign (5th in cycle)


def compute_kalachakra_dasha(chart, birth_date: date) -> list[KalachakraPeriod]:
    """
    Compute Kalachakra Dasha periods from birth.
    Returns list of KalachakraPeriod covering ~100 years.
    """
    moon_pos = chart.planets.get("Moon")
    if not moon_pos:
        return []

    moon_lon = moon_pos.longitude % 360
    nak_idx = int(moon_lon * 27 / 360) % 27
    pada = int((moon_lon * 27 / 360 - nak_idx) * 4)  # 0-3

    # Determine sequence type
    dasha_type, start_sign_idx = _NAK_GROUP.get(nak_idx, ("savya", 0))

    # Build full sign sequence for this cycle
    if dasha_type == "savya":
        base_seq = ["Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg",
                    "Cp","Aq","Pi","Pi","Aq","Cp","Sg","Sc","Li","Vi","Le","Cn","Ge","Ta","Ar"]
    else:
        base_seq = ["Sg","Sc","Li","Vi","Le","Cn","Ge","Ta","Ar",
                    "Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg","Sg","Sc","Li","Vi","Le","Cn"]

    # Find starting position based on pada
    start_offset = [0, 9, 9, 0][pada % 4]
    seq = base_seq[start_offset:] + base_seq[:start_offset]

    # Elapsed fraction in current nakshatra for proportional start
    nak_fraction = (moon_lon * 27 / 360) - int(moon_lon * 27 / 360)
    first_period_years = _KC_PERIODS.get(seq[0], 7)
    elapsed_years = nak_fraction * first_period_years
    elapsed_days = int(elapsed_years * 365.25)

    current_date = birth_date + timedelta(days=-elapsed_days)
    periods = []

    for i, sign in enumerate(seq[:24]):
        years = _KC_PERIODS.get(sign, 7)
        end = current_date + timedelta(days=int(years * 365.25))
        si = _SIGN_ABBR.index(sign) if sign in _SIGN_ABBR else 0
        periods.append(KalachakraPeriod(
            sign=sign, sign_index=si, years=years,
            start_date=current_date, end_date=end,
            is_deha=(i == 0), is_jeeva=(i == 4),
        ))
        current_date = end

    return periods


def current_kalachakra_period(chart, birth_date: date,
                               on_date: date | None = None) -> KalachakraPeriod | None:
    if on_date is None:
        on_date = date.today()
    periods = compute_kalachakra_dasha(chart, birth_date)
    return next((p for p in periods if p.start_date <= on_date < p.end_date), None)
