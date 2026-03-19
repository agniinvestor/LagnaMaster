"""
src/calculations/varshaphala.py
================================
Varshaphala (Annual Solar Return Chart) — Session 18.

Varshaphala ("fruit of the year") is a Jyotish technique that computes the
chart for the moment the Sun returns to its exact natal longitude each year.
That moment becomes the Varsha Lagna (annual ascendant), and the resulting
chart governs events for that 12-month cycle.

Key concepts implemented
------------------------
  Solar Return   — exact Julian Day when Sun reaches natal longitude
  Varsha Lagna   — ascendant of the solar return moment
  Muntha         — "annual significator"; progresses 1 sign per year from H1
                   Muntha sign index = (natal_lagna_si + years_elapsed) % 12
  Varsha Pati    — lord of the Muntha sign (Year Lord)
  Tajika Aspects — five Tajika aspects used in annual chart analysis:
                     Itthasala (60°/Sextile), Ishrafa (120°/Trine),
                     Nakta (90°/Square), Kambool (180°/Opposition),
                     Dainya (30°/Semi-sextile)

Algorithm
---------
  1. At the start of `target_year` (Jan 1, noon UTC), compute Sun longitude.
  2. Binary-search for the Julian Day when Sun longitude matches natal Sun
     longitude (accounting for the 360° wrap at Pisces→Aries).
  3. Call ephemeris.compute_chart() at that JD to get the Varsha chart.
  4. Muntha = (natal_lagna_si + years_elapsed) % 12
  5. Varsha Pati = sign lord of Muntha sign.
  6. Detect Tajika aspects between pairs of Varsha chart planets.

Public API
----------
    compute_varshaphala(
        natal_chart: BirthChart,
        natal_birth_date: date,
        target_year: int,
        lat: float, lon: float,
        tz_offset: float = 5.5,
        ayanamsha: str = "lahiri",
    ) -> VarshaphalaReport

Data classes
------------
    TajikaAspect  — planet_a, planet_b, aspect_type, orb, applying
    VarshaphalaReport — solar_return_jd, solar_return_date, varsha_chart,
                        muntha_sign_index, muntha_sign, varsha_pati,
                        years_elapsed, tajika_aspects
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.ephemeris import BirthChart

# ── constants ─────────────────────────────────────────────────────────────────

_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

# Tajika aspect angles and default orbs (degrees)
_TAJIKA_ASPECTS = [
    ("Itthasala", 60.0,  3.0),   # Sextile  — applying positive
    ("Ishrafa",   120.0, 4.0),   # Trine    — strong positive
    ("Nakta",     90.0,  3.0),   # Square   — tension
    ("Kambool",   180.0, 5.0),   # Opposition — full
    ("Dainya",    30.0,  2.0),   # Semi-sextile — mild
]

_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury",
    "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]


# ── Tajika aspect ─────────────────────────────────────────────────────────────

@dataclass
class TajikaAspect:
    """A Tajika aspect between two planets in the Varsha chart."""
    planet_a: str
    planet_b: str
    aspect_type: str       # "Itthasala" / "Ishrafa" / "Nakta" / "Kambool" / "Dainya"
    angle: float           # nominal aspect angle (60, 120, 90, 180, 30)
    orb: float             # actual separation minus nominal angle (degrees)
    applying: bool         # True if faster planet is approaching aspect


def _angular_distance(lon_a: float, lon_b: float) -> float:
    """Shortest angular distance between two longitudes (0–180°)."""
    diff = abs(lon_a - lon_b) % 360.0
    return diff if diff <= 180.0 else 360.0 - diff


def _detect_tajika_aspects(chart) -> list[TajikaAspect]:   # chart: BirthChart
    """Detect all Tajika aspects among the 9 planets of a Varsha chart."""
    aspects: list[TajikaAspect] = []
    planet_names = [p for p in _PLANETS if p in chart.planets]

    for i, pa in enumerate(planet_names):
        for pb in planet_names[i + 1:]:
            lon_a = chart.planets[pa].longitude
            lon_b = chart.planets[pb].longitude
            sep = _angular_distance(lon_a, lon_b)

            for atype, angle, max_orb in _TAJIKA_ASPECTS:
                orb = abs(sep - angle)
                if orb <= max_orb:
                    # Applying = faster planet approaching slower
                    speed_a = abs(chart.planets[pa].speed)
                    speed_b = abs(chart.planets[pb].speed)
                    faster, slower = (pa, pb) if speed_a >= speed_b else (pb, pa)
                    lon_faster = chart.planets[faster].longitude
                    lon_slower = chart.planets[slower].longitude
                    # Applying if faster is behind slower (direct motion)
                    diff = (lon_slower - lon_faster) % 360.0
                    applying = diff < 180.0
                    aspects.append(TajikaAspect(
                        planet_a=pa, planet_b=pb,
                        aspect_type=atype, angle=angle,
                        orb=round(orb, 4), applying=applying,
                    ))
    return aspects


# ── VarshaphalaReport ─────────────────────────────────────────────────────────

@dataclass
class VarshaphalaReport:
    """Complete Varshaphala (annual solar return) analysis."""
    # Solar return timing
    solar_return_jd: float          # Julian Day (UT) of solar return
    solar_return_date: date         # calendar date of solar return
    # Annual chart
    varsha_chart: object            # BirthChart at solar return moment
    varsha_lagna_sign: str
    varsha_lagna_sign_index: int
    # Annual significators
    years_elapsed: int              # target_year − birth_year
    muntha_sign_index: int          # (natal_lagna_si + years_elapsed) % 12
    muntha_sign: str
    varsha_pati: str                # Year Lord = sign lord of Muntha
    # Tajika aspects
    tajika_aspects: list[TajikaAspect] = field(default_factory=list)

    def aspects_of_type(self, atype: str) -> list[TajikaAspect]:
        return [a for a in self.tajika_aspects if a.aspect_type == atype]

    def aspects_for_planet(self, planet: str) -> list[TajikaAspect]:
        return [a for a in self.tajika_aspects
                if a.planet_a == planet or a.planet_b == planet]


# ── solar return binary search ────────────────────────────────────────────────

def _sun_longitude_at_jd(jd_ut: float) -> float:
    """Return sidereal Sun longitude (Lahiri) at a given Julian Day."""
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    result, _ = swe.calc_ut(jd_ut, swe.SUN, flags)
    return result[0] % 360.0


def _find_solar_return_jd(
    natal_sun_lon: float,
    start_jd: float,
    end_jd: float,
    tolerance_deg: float = 1e-6,
) -> float:
    """
    Binary search for the JD within [start_jd, end_jd] when Sun longitude
    equals natal_sun_lon.  Handles the 359°→0° wrap.
    """
    def signed_diff(jd: float) -> float:
        cur = _sun_longitude_at_jd(jd)
        d = (cur - natal_sun_lon + 360.0) % 360.0
        return d if d <= 180.0 else d - 360.0

    lo, hi = start_jd, end_jd
    for _ in range(60):   # 60 iterations → sub-arcsecond precision
        mid = (lo + hi) / 2.0
        if signed_diff(mid) < 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tolerance_deg / 360.0:
            break
    return (lo + hi) / 2.0


def _jd_to_date(jd_ut: float) -> date:
    """Convert Julian Day (UT) to a calendar date."""
    import swisseph as swe
    y, m, d, _ = swe.revjul(jd_ut, swe.GREG_CAL)
    return date(y, m, int(d))


def _year_bounds_jd(year: int) -> tuple[float, float]:
    """Return (start_jd, end_jd) for a calendar year (UTC noon)."""
    import swisseph as swe
    start = swe.julday(year, 1, 1, 12.0, swe.GREG_CAL)
    end   = swe.julday(year, 12, 31, 12.0, swe.GREG_CAL)
    return start, end


# ── main public function ──────────────────────────────────────────────────────

def compute_varshaphala(
    natal_chart,            # BirthChart
    natal_birth_date: date,
    target_year: int,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
) -> VarshaphalaReport:
    """
    Compute the Varshaphala (Annual Solar Return Chart) for `target_year`.

    Parameters
    ----------
    natal_chart : BirthChart
        The natal BirthChart (output of ephemeris.compute_chart).
    natal_birth_date : date
        The native's date of birth (used to compute years_elapsed).
    target_year : int
        The calendar year for which the annual chart is desired.
    lat, lon : float
        Geographic coordinates for the annual ascendant calculation.
    tz_offset : float
        UTC offset in hours (default 5.5 = IST).
    ayanamsha : str
        Ayanamsha name (default "lahiri").

    Returns
    -------
    VarshaphalaReport
    """
    from src.ephemeris import compute_chart

    natal_sun_lon = natal_chart.planets["Sun"].longitude
    natal_lagna_si = natal_chart.lagna_sign_index

    # Find the JD of the solar return within target_year
    start_jd, end_jd = _year_bounds_jd(target_year)
    sr_jd = _find_solar_return_jd(natal_sun_lon, start_jd, end_jd)

    # Convert JD to local time for compute_chart
    # sr_jd is in UT; convert to local hour
    import swisseph as swe
    y, m, d, hour_ut = swe.revjul(sr_jd, swe.GREG_CAL)
    local_hour = (hour_ut + tz_offset) % 24.0
    # If local hour crosses midnight, adjust date
    sr_local_date = _jd_to_date(sr_jd + tz_offset / 24.0)

    varsha_chart = compute_chart(
        year=sr_local_date.year,
        month=sr_local_date.month,
        day=sr_local_date.day,
        hour=local_hour,
        lat=lat,
        lon=lon,
        tz_offset=tz_offset,
        ayanamsha=ayanamsha,
    )

    sr_date = _jd_to_date(sr_jd)

    # Muntha
    years_elapsed = target_year - natal_birth_date.year
    muntha_si = (natal_lagna_si + years_elapsed) % 12
    muntha_sign = _SIGNS[muntha_si]
    varsha_pati = _SIGN_LORDS[muntha_si]

    # Tajika aspects
    aspects = _detect_tajika_aspects(varsha_chart)

    return VarshaphalaReport(
        solar_return_jd=round(sr_jd, 6),
        solar_return_date=sr_date,
        varsha_chart=varsha_chart,
        varsha_lagna_sign=varsha_chart.lagna_sign,
        varsha_lagna_sign_index=varsha_chart.lagna_sign_index,
        years_elapsed=years_elapsed,
        muntha_sign_index=muntha_si,
        muntha_sign=muntha_sign,
        varsha_pati=varsha_pati,
        tajika_aspects=aspects,
    )
