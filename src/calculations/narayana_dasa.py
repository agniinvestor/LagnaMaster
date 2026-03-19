"""
src/calculations/narayana_dasa.py
===================================
Narayana Dasha — Rasi (sign-based) predictive cycle.
Source: CALC_NarayanaDasa + REF_NarayanaDasaRules (Excel), BPHS Ch.4, PVRNR.

N-1 BUG FIX: Taurus was 4 years in the Excel; correct PVRNR value is 7 years.
The Excel REF_NarayanaDasaRules sheet says "Count from Taurus to lord Venus in
Pisces (exalt) = 11, adj to 4" — this adjustment formula is wrong; PVRNR Ch.1
explicitly gives Taurus = 7 years.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from src.ephemeris import SIGNS


# ---------------------------------------------------------------------------
# Narayana Dasha period table  (PVRNR corrected)
# N-1 FIX: Taurus = 7 (was 4 in Excel bug)
# Total = 6+7+2+10+9+8+1+11+5+7+12+3 = 81 years per cycle
# ---------------------------------------------------------------------------

NARAYANA_DASHA_YEARS: dict[str, int] = {
    "Aries":       6,
    "Taurus":      7,   # N-1 FIX: was 4 in Excel, correct is 7 (PVRNR Ch.1)
    "Gemini":      2,
    "Cancer":      10,
    "Leo":         9,
    "Virgo":       8,
    "Libra":       1,
    "Scorpio":     11,
    "Sagittarius": 5,
    "Capricorn":   7,
    "Aquarius":    12,
    "Pisces":      3,
}

_ODD_SIGNS = {0, 2, 4, 6, 8, 10}   # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius


@dataclass
class NarayanaPeriod:
    sequence: int       # 1-12
    sign: str
    sign_index: int
    years: int
    start_date: date
    end_date: date
    is_active: bool
    remaining_years: float | None   # if active


def _sign_sequence(lagna_sign_idx: int, direction: str) -> list[str]:
    """Return 12-sign Narayana Dasha sequence starting from Lagna sign."""
    signs = list(SIGNS)
    seq = []
    idx = lagna_sign_idx
    for _ in range(12):
        seq.append(signs[idx])
        if direction == "forward":
            idx = (idx + 1) % 12
        else:
            idx = (idx - 1) % 12
    return seq


def compute_narayana_dasha(
    lagna_sign_idx: int,
    birth_date: date,
    query_date: date | None = None,
) -> list[NarayanaPeriod]:
    """
    Compute the 12-period Narayana Dasha sequence.

    Parameters
    ----------
    lagna_sign_idx : Ascendant sign index (0=Aries)
    birth_date     : birth date
    query_date     : date to check active period (defaults to today)

    Returns
    -------
    List of 12 NarayanaPeriod objects.
    """
    if query_date is None:
        query_date = date.today()

    # Direction: odd Lagna sign → forward; even → backward
    direction = "forward" if lagna_sign_idx in _ODD_SIGNS else "backward"
    sequence = _sign_sequence(lagna_sign_idx, direction)

    periods: list[NarayanaPeriod] = []
    current = birth_date

    for i, sign in enumerate(sequence):
        years = NARAYANA_DASHA_YEARS[sign]
        # Use 365.25 days/year for fractional year calculation
        days = int(years * 365.25)
        end = current + timedelta(days=days)

        is_active = current <= query_date < end
        remaining = None
        if is_active:
            remaining_days = (end - query_date).days
            remaining = remaining_days / 365.25

        sign_idx = SIGNS.index(sign)
        periods.append(NarayanaPeriod(
            sequence=i + 1,
            sign=sign,
            sign_index=sign_idx,
            years=years,
            start_date=current,
            end_date=end,
            is_active=is_active,
            remaining_years=remaining,
        ))
        current = end

    return periods


def active_narayana_period(
    lagna_sign_idx: int,
    birth_date: date,
    query_date: date | None = None,
) -> NarayanaPeriod | None:
    """Return the currently active Narayana Dasha period, or None."""
    for p in compute_narayana_dasha(lagna_sign_idx, birth_date, query_date):
        if p.is_active:
            return p
    return None
