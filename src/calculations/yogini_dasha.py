"""
src/calculations/yogini_dasha.py — Session 43

Yogini Dasha: 8-period cycle totalling 36 years.
Lords: Mangala(Moon,1yr) → Pingala(Sun,2) → Dhanya(Jupiter,3)
       → Bhramari(Mars,4) → Bhadrika(Mercury,5) → Ulka(Saturn,6)
       → Siddha(Venus,7) → Sankata(Rahu,8)

Starting Yogini determined by birth nakshatra:
  (nakshatra_index mod 8) → Yogini index

Public API
----------
  compute_yogini_dasha(chart, birth_date) -> list[YoginiPeriod]
  current_yogini(periods, on_date) -> YoginiPeriod
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta

# 8 Yogini lords in order
_YOGINIS = [
    ("Mangala", "Moon", 1),
    ("Pingala", "Sun", 2),
    ("Dhanya", "Jupiter", 3),
    ("Bhramari", "Mars", 4),
    ("Bhadrika", "Mercury", 5),
    ("Ulka", "Saturn", 6),
    ("Siddha", "Venus", 7),
    ("Sankata", "Rahu", 8),
]
# Total = 1+2+3+4+5+6+7+8 = 36 years

# Nakshatra → starting Yogini index (0-7)
# (nakshatra_number - 1) mod 8
# Ashwini=0 → Mangala, Bharani=1 → Pingala, etc.


@dataclass
class YoginiPeriod:
    yogini_name: str
    lord: str
    years: int
    start_date: date
    end_date: date
    is_current: bool = False

    def antara_periods(self) -> list[dict]:
        """Sub-periods within this Yogini Mahadasha (proportional)."""
        total_days = (self.end_date - self.start_date).days
        subs = []
        cursor = self.start_date
        for yname, yplanet, yyears in _YOGINIS:
            days = round(total_days * yyears / 36)
            end = cursor + timedelta(days=days)
            subs.append({"yogini": yname, "lord": yplanet, "start": cursor, "end": end})
            cursor = end
        return subs


def compute_yogini_dasha(chart, birth_date):
    """Compute full Yogini Dasha sequence from birth."""
    # Get Moon nakshatra index (0-based, 0=Ashwini)
    moon_lon = chart.planets["Moon"].longitude
    # Nakshatra index = floor(longitude * 27 / 360)
    nak_idx = int((moon_lon % 360) / (360 / 27))
    nak_fraction = ((moon_lon % 360) % (360 / 27)) / (360 / 27)

    start_yogini = nak_idx % 8
    first_years = _YOGINIS[start_yogini][2]
    elapsed_years = nak_fraction * first_years
    elapsed_days = int(elapsed_years * 365.25)

    periods = []
    cursor = birth_date - timedelta(days=elapsed_days)

    # Generate 3 complete cycles (108 years)
    for cycle in range(3):
        for i in range(8):
            idx = (start_yogini + i) % 8
            yname, yplanet, yyears = _YOGINIS[idx]
            if cycle == 0 and i == 0:
                days = int((first_years - elapsed_years) * 365.25)
            else:
                days = int(yyears * 365.25)
            end = cursor + timedelta(days=days)
            periods.append(
                YoginiPeriod(
                    yogini_name=yname,
                    lord=yplanet,
                    years=yyears,
                    start_date=cursor,
                    end_date=end,
                )
            )
            cursor = end

    return periods


def current_yogini(
    periods: list[YoginiPeriod], on_date: date | None = None
) -> YoginiPeriod | None:
    if on_date is None:
        on_date = date.today()
    for p in periods:
        if p.start_date <= on_date < p.end_date:
            p.is_current = True
            return p
    return None
