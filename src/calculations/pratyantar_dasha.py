"""
src/calculations/pratyantar_dasha.py
Pratyantar Dasha — 3rd level of Vimshottari (MD > AD > PD).

Session 120 (Phase 1):
  PD duration = MD_years * AD_years * PD_lord_years / (120 * 120) years
  Same 9-planet sequence as MD/AD.

Source: K.N. Rao, Timing Events Through Vimshottari Dasha
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Optional

_SEQUENCE = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
]

VIMSHOTTARI_YEARS: dict[str, float] = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}


@dataclass
class PratyantarDasha:
    lord: str
    start: date
    end: date
    years: float


@dataclass
class AntarDashaFull:
    """AntarDasha with embedded Pratyantar list."""

    lord: str
    start: date
    end: date
    years: float
    pratyantars: list[PratyantarDasha] = field(default_factory=list)


def compute_pratyantar_dashas(
    ad_lord: str,
    ad_start: date,
    ad_end: date,
    md_years: float,
    ad_years: float,
) -> list[PratyantarDasha]:
    """
    Compute all 9 Pratyantar Dashas within one Antardasha.
    PD_years = md_years * ad_years * pd_lord_years / (120 * 120)
    """
    # Start sequence from the AD lord
    start_idx = _SEQUENCE.index(ad_lord)
    pratyantars = []
    current_start = ad_start

    for i in range(9):
        pd_lord = _SEQUENCE[(start_idx + i) % 9]
        pd_lord_years = VIMSHOTTARI_YEARS[pd_lord]
        pd_years = ad_years * pd_lord_years / 120.0

        # Convert years to days
        pd_days = pd_years * 365.25
        pd_end_dt = current_start + relativedelta(days=round(pd_days))

        pratyantars.append(
            PratyantarDasha(
                lord=pd_lord,
                start=current_start,
                end=min(pd_end_dt, ad_end),
                years=round(pd_years, 6),
            )
        )
        current_start = pd_end_dt

    return pratyantars


def current_pratyantar(
    pratyantars: list[PratyantarDasha],
    on_date: Optional[date] = None,
) -> Optional[PratyantarDasha]:
    """Return the active Pratyantar Dasha on a given date."""
    today = on_date or date.today()
    for pd in pratyantars:
        if pd.start <= today < pd.end:
            return pd
    return pratyantars[-1] if pratyantars else None
