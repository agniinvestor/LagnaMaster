"""src/calculations/temporal_projection.py — Temporal probability layer.

Architecture gap G6.

For each converged prediction, overlays independent timing systems:
  - Vimshottari Mahadasha + Antardasha
  - Yogini Dasha
  - Chara Dasha (sign-based)

When multiple systems point to the same year window = high confidence.
When they scatter across decades = low confidence.

Public API
----------
  time_project(converged, ctx) → list[TimedPrediction]
  TimedPrediction — one house prediction with timing probability
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from src.calculations.chart_context import ChartContext
from src.calculations.convergence import ConvergedPrediction

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G6", "session": "S328"}


@dataclass
class TimingWindow:
    """A period during which a timing system activates a house."""
    system: str       # "vimshottari_md"|"vimshottari_ad"|"yogini"|"chara"|"gochara"|"varshaphala"|"pad"
    lord: str         # planet or sign name
    start_year: int
    end_year: int
    start_month: int = 1   # D10: month-level precision (1-12)
    end_month: int = 12    # D10: defaults to full-year if not specified


@dataclass
class TimedPrediction:
    """A converged prediction with temporal probability.

    Carries the original convergence data PLUS timing from independent
    timing systems.  P(event|year) counts how many systems are active
    in each year.

    The unified confirmation count (architecture Layer 4) combines:
      natal_confirmations  — from convergence layer (text source channels)
      temporal_confirmations — timing systems active during peak window
      contra_indicators    — from convergence layer (opposing channels)
    """
    # From convergence layer (natal promise)
    house: int
    direction: str
    convergence_score: int    # natal channel count
    contra_score: int

    # Timing
    probability_by_year: dict[int, float] = field(default_factory=dict)
    peak_window: tuple[int, int] = (0, 0)
    timing_confidence: float = 0.0
    contributing_systems: list[TimingWindow] = field(default_factory=list)

    # Unified confirmation count (D0b: natal + temporal combined)
    temporal_confirmations: int = 0   # timing systems active during peak
    temporal_systems: list[str] = field(default_factory=list)

    # Metadata
    outcome_domains: list[str] = field(default_factory=list)
    strength_label: str = ""

    @property
    def total_confirmations(self) -> int:
        """Unified count: natal channels + temporal systems (architecture Layer 4)."""
        return self.convergence_score + self.temporal_confirmations

    @property
    def unified_label(self) -> str:
        """Human-readable unified strength."""
        tc = self.total_confirmations
        if tc >= 6:
            return "very_strong"
        if tc >= 4:
            return "strong"
        if tc >= 2:
            return "moderate"
        return "weak"

    @property
    def peak_years(self) -> list[int]:
        """Years with maximum probability."""
        if not self.probability_by_year:
            return []
        max_p = max(self.probability_by_year.values())
        return [y for y, p in sorted(self.probability_by_year.items()) if p == max_p]


# ---------------------------------------------------------------------------
# Timing system scanners
# ---------------------------------------------------------------------------

def _house_lords(ctx: ChartContext, house: int) -> set[str]:
    """Get the planet(s) that lord the given house."""
    lord = ctx.house_map.house_lord[house - 1]
    return {lord}


def _vimshottari_windows(
    ctx: ChartContext,
    house_lords: set[str],
) -> list[TimingWindow]:
    """Find Vimshottari MD and AD periods ruled by house lords."""
    if ctx.dashas is None:
        return []

    windows: list[TimingWindow] = []
    for md in ctx.dashas:
        if md.lord in house_lords:
            windows.append(TimingWindow(
                system="vimshottari_md",
                lord=md.lord,
                start_year=md.start.year,
                end_year=md.end.year,
                start_month=md.start.month,
                end_month=md.end.month,
            ))
        for ad in md.antardashas:
            if ad.lord in house_lords:
                windows.append(TimingWindow(
                    system="vimshottari_ad",
                    lord=ad.lord,
                    start_year=ad.start.year,
                    end_year=ad.end.year,
                    start_month=ad.start.month,
                    end_month=ad.end.month,
                ))
    return windows


def _yogini_windows(
    ctx: ChartContext,
    house_lords: set[str],
    birth_date: Optional[date],
) -> list[TimingWindow]:
    """Find Yogini dasha periods ruled by house lords."""
    if birth_date is None:
        return []
    try:
        from src.calculations.yogini_dasha import compute_yogini_dasha
        periods = compute_yogini_dasha(ctx.chart, birth_date)
    except (ImportError, Exception):
        return []

    windows: list[TimingWindow] = []
    for p in periods:
        if p.lord in house_lords:
            windows.append(TimingWindow(
                system="yogini",
                lord=p.lord,
                start_year=p.start_date.year,
                end_year=p.end_date.year,
            ))
    return windows


def _chara_windows(
    ctx: ChartContext,
    house: int,
    birth_date: Optional[date],
) -> list[TimingWindow]:
    """Find Chara dasha periods for the sign of this house."""
    if birth_date is None:
        return []
    try:
        from src.calculations.chara_dasha import compute_chara_dasha
        entries = compute_chara_dasha(ctx.chart, birth_date)
    except (ImportError, Exception):
        return []

    house_sign_idx = ctx.house_map.house_sign[house - 1]
    windows: list[TimingWindow] = []
    for e in entries:
        if e.sign_index == house_sign_idx:
            windows.append(TimingWindow(
                system="chara",
                lord=e.sign,
                start_year=e.start.year,
                end_year=e.end.year,
            ))
    return windows


# ---------------------------------------------------------------------------
# D6: Gochara (transit) windows
# ---------------------------------------------------------------------------

# Jupiter takes ~12 years for full zodiac, ~1 year per sign
# Saturn takes ~29.5 years, ~2.5 years per sign
_JUPITER_PERIOD = 11.86  # years per full cycle
_SATURN_PERIOD = 29.46


def _gochara_windows(
    ctx: ChartContext,
    house: int,
    birth_date: Optional[date],
) -> list[TimingWindow]:
    """D6: Find years when Jupiter or Saturn transits the house sign.

    Uses orbital period approximation from the natal transit position.
    For each slow planet, computes when it will be in the house sign.
    """
    if birth_date is None:
        return []

    house_sign_idx = ctx.house_map.house_sign[house - 1]
    windows: list[TimingWindow] = []
    birth_year = birth_date.year

    for planet, period in [("Jupiter", _JUPITER_PERIOD), ("Saturn", _SATURN_PERIOD)]:
        if planet not in ctx.chart.planets:
            continue
        natal_si = ctx.chart.planets[planet].sign_index
        # How many signs from natal to house sign (forward in zodiac)
        signs_ahead = (house_sign_idx - natal_si) % 12
        # First transit over house sign
        years_to_first = signs_ahead * (period / 12)
        time_in_sign = period / 12  # ~1yr for Jupiter, ~2.5yr for Saturn

        # Generate all transits within 120 years
        year = birth_year + years_to_first
        while year < birth_year + 120:
            start_y = int(year)
            end_y = int(year + time_in_sign)
            if start_y >= birth_year:
                windows.append(TimingWindow(
                    system="gochara",
                    lord=planet,
                    start_year=start_y,
                    end_year=max(start_y, end_y),
                ))
            year += period

    return windows


# ---------------------------------------------------------------------------
# D7: Varshaphala (solar return) windows
# ---------------------------------------------------------------------------

def _varshaphala_windows(
    ctx: ChartContext,
    house_lords: set[str],
    birth_date: Optional[date],
) -> list[TimingWindow]:
    """D7: Find years where varsha_pati lords the target house.

    Computes varshaphala for a sample of years (every 3rd year across
    the dasha span) to avoid computing 120 solar returns.
    """
    if birth_date is None:
        return []

    windows: list[TimingWindow] = []
    birth_year = birth_date.year

    try:
        from src.calculations.varshaphala import compute_varshaphala
    except ImportError:
        return []

    # Sample every 3rd year across 120-year span
    for query_year in range(birth_year + 1, birth_year + 121, 3):
        try:
            v = compute_varshaphala(
                ctx.chart,
                birth_date_or_year=birth_date,
                query_year=query_year,
            )
            if v.varsha_pati in house_lords:
                windows.append(TimingWindow(
                    system="varshaphala",
                    lord=v.varsha_pati,
                    start_year=query_year,
                    end_year=query_year,
                ))
        except (ValueError, TypeError, AttributeError, KeyError):
            continue

    return windows


# ---------------------------------------------------------------------------
# D8: Pratyantardasha windows (computed proportionally from AD)
# ---------------------------------------------------------------------------

# Vimshottari dasha years per planet
_DASHA_YEARS = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16,
    "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20,
}
_TOTAL_DASHA = 120


def _pad_windows(
    ctx: ChartContext,
    house_lords: set[str],
) -> list[TimingWindow]:
    """D8: Compute Pratyantardasha windows from Vimshottari MD/AD.

    PAD is not stored in the dasha structure, so we compute it
    proportionally: within each AD, each PAD lord gets a fraction
    of the AD duration proportional to its dasha years / 120.
    We only emit PADs where the lord rules the target house.
    """
    if ctx.dashas is None:
        return []

    windows: list[TimingWindow] = []
    pad_lords = ["Sun", "Moon", "Mars", "Rahu", "Jupiter",
                 "Saturn", "Mercury", "Ketu", "Venus"]

    for md in ctx.dashas:
        for ad in md.antardashas:
            ad_days = (ad.end - ad.start).days
            if ad_days <= 0:
                continue

            # PAD sequence starts from AD lord
            try:
                start_idx = pad_lords.index(ad.lord)
            except ValueError:
                continue

            current_date = ad.start
            for i in range(9):
                pad_lord = pad_lords[(start_idx + i) % 9]
                pad_fraction = _DASHA_YEARS.get(pad_lord, 7) / _TOTAL_DASHA
                pad_days = int(ad_days * pad_fraction)
                pad_end = current_date + __import__("datetime").timedelta(days=pad_days)

                if pad_lord in house_lords and pad_days > 0:
                    windows.append(TimingWindow(
                        system="pad",
                        lord=pad_lord,
                        start_year=current_date.year,
                        end_year=pad_end.year,
                    ))
                current_date = pad_end

    return windows


# ---------------------------------------------------------------------------
# Probability distribution builder
# ---------------------------------------------------------------------------

def _build_probability(
    windows: list[TimingWindow],
    birth_year: int,
) -> dict[int, float]:
    """Build P(activation|year) from timing windows.

    Each year gets +1.0 for each independent SYSTEM active in that year.
    The same system counts at most once per year.

    D9: Narrower systems (AD, PAD, gochara) are weighted 1.5× vs broad
    systems (MD) to prefer specific timing over general periods.

    D11: Normalized to [0, 1] by dividing by weighted system count.
    This is a counting heuristic, not Bayesian — proper probabilistic
    combination requires calibration data (Phase B / G10).
    """
    # D9: System weights — narrower systems count more
    _SYSTEM_WEIGHT = {
        "vimshottari_md": 1.0,
        "vimshottari_ad": 1.5,
        "yogini": 1.0,
        "chara": 1.0,
        "gochara": 1.5,
        "varshaphala": 1.5,
        "pad": 2.0,
    }

    year_score: dict[int, float] = defaultdict(float)
    year_systems: dict[int, set[str]] = defaultdict(set)
    systems_present: set[str] = set()

    for w in windows:
        systems_present.add(w.system)
        sw = _SYSTEM_WEIGHT.get(w.system, 1.0)
        for y in range(w.start_year, w.end_year + 1):
            if y >= birth_year and w.system not in year_systems[y]:
                year_systems[y].add(w.system)
                year_score[y] += sw

    if not systems_present:
        return {}

    max_possible = sum(_SYSTEM_WEIGHT.get(s, 1.0) for s in systems_present)
    return {
        y: min(1.0, score / max_possible)
        for y, score in sorted(year_score.items())
    }


def _peak_window(prob: dict[int, float]) -> tuple[int, int]:
    """Find the contiguous window of peak probability years.

    D9: Uses 0.85 threshold (tighter than original 0.75) to produce
    narrower, more actionable peak windows.
    """
    if not prob:
        return (0, 0)
    max_p = max(prob.values())
    peak_years = sorted(y for y, p in prob.items() if p >= max_p * 0.85)
    if not peak_years:
        return (0, 0)

    # Find the longest contiguous run within peak_years
    best_start = best_end = peak_years[0]
    curr_start = curr_end = peak_years[0]
    for y in peak_years[1:]:
        if y == curr_end + 1:
            curr_end = y
        else:
            if (curr_end - curr_start) > (best_end - best_start):
                best_start, best_end = curr_start, curr_end
            curr_start = curr_end = y
    if (curr_end - curr_start) > (best_end - best_start):
        best_start, best_end = curr_start, curr_end

    return (best_start, best_end)


def _timing_confidence(
    windows: list[TimingWindow],
    peak: tuple[int, int],
) -> float:
    """Compute timing confidence as fraction of systems confirming the peak.

    0.0 = no timing data. 1.0 = all systems converge on peak window.
    """
    if not windows or peak == (0, 0):
        return 0.0

    systems = {w.system for w in windows}
    confirming = set()
    for w in windows:
        if w.start_year <= peak[1] and w.end_year >= peak[0]:
            confirming.add(w.system)

    return len(confirming) / len(systems) if systems else 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def time_project(
    converged: list[ConvergedPrediction],
    ctx: ChartContext,
    *,
    birth_date: Optional[date] = None,
) -> list[TimedPrediction]:
    """Project temporal probability onto converged predictions.

    For each converged prediction, overlays Vimshottari (MD+AD), Yogini,
    and Chara dasha systems.  Computes P(event|year) as the fraction of
    independent timing systems active per year.

    Parameters
    ----------
    converged : list[ConvergedPrediction]
        From converge().
    ctx : ChartContext
        Pre-computed chart context (must include dashas if birth_date given).
    birth_date : date, optional
        Calendar birth date.  Required for Yogini and Chara dashas.

    Returns
    -------
    list[TimedPrediction]
        Converged predictions enriched with timing probability.
    """
    birth_year = birth_date.year if birth_date else 1900

    results: list[TimedPrediction] = []
    for cp in converged:
        lords = _house_lords(ctx, cp.house)

        # Collect timing windows from independent systems
        windows: list[TimingWindow] = []
        windows.extend(_vimshottari_windows(ctx, lords))
        windows.extend(_yogini_windows(ctx, lords, birth_date))
        windows.extend(_chara_windows(ctx, cp.house, birth_date))
        windows.extend(_gochara_windows(ctx, cp.house, birth_date))  # D6
        windows.extend(_varshaphala_windows(ctx, lords, birth_date))  # D7
        windows.extend(_pad_windows(ctx, lords))  # D8

        # Build probability distribution
        prob = _build_probability(windows, birth_year)
        peak = _peak_window(prob)
        confidence = _timing_confidence(windows, peak)

        # D0b: count temporal systems active during peak window
        peak_systems: set[str] = set()
        if peak != (0, 0):
            for w in windows:
                if w.start_year <= peak[1] and w.end_year >= peak[0]:
                    peak_systems.add(w.system)

        results.append(TimedPrediction(
            house=cp.house,
            direction=cp.direction,
            convergence_score=cp.convergence_score,
            contra_score=cp.contra_score,
            probability_by_year=prob,
            peak_window=peak,
            timing_confidence=confidence,
            contributing_systems=windows,
            temporal_confirmations=len(peak_systems),
            temporal_systems=sorted(peak_systems),
            outcome_domains=cp.outcome_domains,
            strength_label=cp.strength_label,
        ))

    return results
