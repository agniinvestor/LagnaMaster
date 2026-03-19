"""
src/calculations/vimshottari_dasa.py
=====================================
Vimshottari Dasha — 120-year nakshatra-based predictive cycle.

The most commonly used dasha system in Jyotish.
Dasha lord is determined by Moon's nakshatra at birth.

Structure:
  9 MahaDashas (major periods) × 9 AntarDashas (sub-periods) = 81 entries per chart.
  Total span: 120 years.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from src.ephemeris import BirthChart


# ── Vimshottari constants ────────────────────────────────────────────────────

VIMSHOTTARI_YEARS: dict[str, int] = {
    "Ketu":    7,
    "Venus":   20,
    "Sun":     6,
    "Moon":    10,
    "Mars":    7,
    "Rahu":    18,
    "Jupiter": 16,
    "Saturn":  19,
    "Mercury": 17,
}

TOTAL_YEARS = 120  # sum of all periods

# Fixed order of the 9 dasha lords
_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury",
]

# 27 nakshatra lords (each group of 9 repeats 3 times)
_NAKSHATRA_LORDS: list[str] = _SEQUENCE * 3  # indices 0–26

_NAKSHATRA_NAMES: list[str] = [
    "Ashwini",        "Bharani",          "Krittika",
    "Rohini",         "Mrigashira",       "Ardra",
    "Punarvasu",      "Pushya",           "Ashlesha",
    "Magha",          "Purva Phalguni",   "Uttara Phalguni",
    "Hasta",          "Chitra",           "Swati",
    "Vishakha",       "Anuradha",         "Jyeshtha",
    "Mula",           "Purva Ashadha",    "Uttara Ashadha",
    "Shravana",       "Dhanishtha",       "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

_NAK_SPAN      = 360.0 / 27   # 13.3333...° per nakshatra
_DAYS_PER_YEAR = 365.25


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class AntarDasha:
    lord:  str
    start: date
    end:   date
    years: float    # actual duration

    @property
    def is_current(self) -> bool:
        return self.start <= date.today() < self.end


@dataclass
class MahaDasha:
    lord:       str
    start:      date
    end:        date
    years:      float    # actual duration (balance for first dasha)
    full_years: int      # nominal period for this lord
    nakshatra:  str      # Moon's birth nakshatra (non-empty only for first dasha)
    antardashas: list[AntarDasha] = field(default_factory=list)

    @property
    def is_current(self) -> bool:
        return self.start <= date.today() < self.end


# ── Internal helpers ──────────────────────────────────────────────────────────

def _antardashas(maha_lord: str, maha_start: date, maha_years: float) -> list[AntarDasha]:
    """Divide a mahadasha into 9 antardashas (sub-periods)."""
    start_idx = _SEQUENCE.index(maha_lord)
    ads: list[AntarDasha] = []
    current = maha_start
    for i in range(9):
        antar_lord = _SEQUENCE[(start_idx + i) % 9]
        # Antardasha duration = (maha_years × antar_full_years) / 120
        ad_years = maha_years * VIMSHOTTARI_YEARS[antar_lord] / TOTAL_YEARS
        end = current + timedelta(days=ad_years * _DAYS_PER_YEAR)
        ads.append(AntarDasha(lord=antar_lord, start=current, end=end, years=ad_years))
        current = end
    return ads


# ── Public API ────────────────────────────────────────────────────────────────

def compute_vimshottari_dasa(
    chart: BirthChart,
    birth_date: date,
) -> list[MahaDasha]:
    """
    Compute Vimshottari Dasha sequence from birth.

    Parameters
    ----------
    chart      : BirthChart (Moon's sidereal longitude is used)
    birth_date : calendar date of birth (date object)

    Returns
    -------
    List of 9 MahaDashas covering 120 years from birth.
    Each MahaDasha contains 9 AntarDashas.
    """
    moon_lon = chart.planets["Moon"].longitude   # sidereal 0–360°

    # Moon's nakshatra (0-indexed, 0=Ashwini … 26=Revati)
    nak_idx = min(int(moon_lon / _NAK_SPAN), 26)

    # Fraction of the nakshatra elapsed at birth
    elapsed_fraction = (moon_lon - nak_idx * _NAK_SPAN) / _NAK_SPAN

    # Birth dasha lord
    birth_lord = _NAKSHATRA_LORDS[nak_idx]
    birth_nak  = _NAKSHATRA_NAMES[nak_idx]
    full_years = VIMSHOTTARI_YEARS[birth_lord]
    balance    = full_years * (1.0 - elapsed_fraction)

    start_idx = _SEQUENCE.index(birth_lord)
    dashas: list[MahaDasha] = []
    current_date = birth_date

    for i in range(9):
        seq_idx = (start_idx + i) % 9
        lord    = _SEQUENCE[seq_idx]
        full    = VIMSHOTTARI_YEARS[lord]
        actual  = balance if i == 0 else float(full)
        end_dt  = current_date + timedelta(days=actual * _DAYS_PER_YEAR)

        dashas.append(MahaDasha(
            lord=lord,
            start=current_date,
            end=end_dt,
            years=actual,
            full_years=full,
            nakshatra=birth_nak if i == 0 else "",
            antardashas=_antardashas(lord, current_date, actual),
        ))
        current_date = end_dt

    return dashas


def current_dasha(
    dashas: list[MahaDasha],
    on_date: date | None = None,
) -> tuple[MahaDasha, AntarDasha]:
    """
    Return the (MahaDasha, AntarDasha) active on on_date (defaults to today).
    Returns the last available dasha if on_date is beyond the 120-year span.
    """
    d = on_date or date.today()
    for md in dashas:
        if md.start <= d < md.end:
            for ad in md.antardashas:
                if ad.start <= d < ad.end:
                    return md, ad
            return md, md.antardashas[-1]
    return dashas[-1], dashas[-1].antardashas[-1]


def nakshatra_of_moon(chart: BirthChart) -> tuple[str, str]:
    """Return (nakshatra_name, dasha_lord) for Moon's position."""
    moon_lon = chart.planets["Moon"].longitude
    nak_idx  = min(int(moon_lon / _NAK_SPAN), 26)
    return _NAKSHATRA_NAMES[nak_idx], _NAKSHATRA_LORDS[nak_idx]
