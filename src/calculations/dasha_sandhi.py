"""
src/calculations/dasha_sandhi.py
Dasha Sandhi alerting — junction periods between Mahadashas.
Session 131 (Phase 2).

Source: K.N. Rao, Astrology Destiny and the Wheel of Time Ch.3
'The transition period between two Mahadashas correlates with major life disruptions.'
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta


SANDHI_MONTHS = 6  # last/first N months of each MD constitute the Sandhi zone


@dataclass
class DashaSandhi:
    ending_lord: str
    starting_lord: str
    sandhi_start: date  # 6 months before end of ending MD
    md_transition: date  # actual MD transition
    sandhi_end: date  # 6 months after start of new MD
    is_active_today: bool


def compute_sandhi_periods(mahadashas: list, on_date: date = None) -> list[DashaSandhi]:
    """
    Compute Sandhi periods for all MD transitions.
    Source: K.N. Rao, Astrology Destiny Ch.3
    """
    today = on_date or date.today()
    results = []

    for i in range(len(mahadashas) - 1):
        md_current = mahadashas[i]
        md_next = mahadashas[i + 1]

        transition = md_current.end
        sandhi_start = transition - relativedelta(months=SANDHI_MONTHS)
        sandhi_end = transition + relativedelta(months=SANDHI_MONTHS)

        is_active = sandhi_start <= today <= sandhi_end

        results.append(
            DashaSandhi(
                ending_lord=md_current.lord,
                starting_lord=md_next.lord,
                sandhi_start=sandhi_start,
                md_transition=transition,
                sandhi_end=sandhi_end,
                is_active_today=is_active,
            )
        )

    return results


def current_sandhi(
    sandhi_list: list[DashaSandhi], on_date: date = None
) -> DashaSandhi | None:
    """Return the active Sandhi period if any."""
    today = on_date or date.today()
    for s in sandhi_list:
        if s.sandhi_start <= today <= s.sandhi_end:
            return s
    return None
