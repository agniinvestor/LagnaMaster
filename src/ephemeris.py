"""
src/ephemeris.py
================
pyswisseph wrapper for Jyotish birth chart calculation.

Returns sidereal planet positions (Lahiri ayanamsha) and Lagna (ascendant)
for any birth date, time, and geographic location.

Regression fixture (validates all future changes):
    1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
    → Lagna: 7.7286° Taurus
    → Sun:   27.989° Cancer
    → Ayanamsha: Lahiri (~23.15° in 1947)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import swisseph as swe

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_EPHE_PATH = str(Path(__file__).parent.parent / "ephe")

SIGNS = [
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

# Jyotish Navagrahas (9 planets). Ketu derived from Rahu.
_PLANET_IDS: dict[str, int] = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # mean North Node (Rahu)
}

_AYANAMSHA_MAP = {
    "lahiri": swe.SIDM_LAHIRI,
    "raman": swe.SIDM_RAMAN,
    "krishnamurti": swe.SIDM_KRISHNAMURTI,
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class PlanetPosition:
    name: str
    longitude: float  # sidereal, 0–360°
    sign: str  # e.g. "Taurus"
    sign_index: int  # 0=Aries … 11=Pisces
    degree_in_sign: float  # 0–30°
    is_retrograde: bool
    speed: float  # degrees/day (negative = retrograde)


@dataclass
class BirthChart:
    # Metadata
    jd_ut: float  # Julian Day (UT)
    ayanamsha_name: str  # e.g. "lahiri"
    ayanamsha_value: float  # degrees (e.g. ~23.15° in 1947)

    # Lagna (ascendant)
    lagna: float  # sidereal longitude, 0–360°
    lagna_sign: str
    lagna_sign_index: int
    lagna_degree_in_sign: float

    # Navagrahas
    planets: dict[str, PlanetPosition] = field(default_factory=dict)

    def planet(self, name: str) -> PlanetPosition:
        """Convenience accessor with a clear error."""
        if name not in self.planets:
            raise KeyError(
                f"Planet {name!r} not in chart. Available: {list(self.planets)}"
            )
        return self.planets[name]

    def summary(self) -> str:
        """Human-readable one-liner per planet for debugging."""
        lines = [
            f"Lagna : {self.lagna_degree_in_sign:.4f}° {self.lagna_sign}  "
            f"(ayanamsha {self.ayanamsha_name} = {self.ayanamsha_value:.4f}°)"
        ]
        for name, p in self.planets.items():
            retro = " ℞" if p.is_retrograde else ""
            lines.append(f"  {name:8s}: {p.degree_in_sign:.4f}° {p.sign}{retro}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _sign_from_lon(lon: float) -> tuple[str, int, float]:
    """Return (sign_name, sign_index 0–11, degree_in_sign 0–30) for a longitude."""
    lon = lon % 360
    idx = int(lon / 30)
    deg = lon - idx * 30
    return SIGNS[idx], idx, deg


def _local_to_jd(
    year: int, month: int, day: int, hour: float, tz_offset: float
) -> float:
    """
    Convert local date/time to Julian Day (UT).

    P-1 fix: `hour` may be 0.0 for midnight — caller must not test `if not hour`.
    We accept None and treat it as 0.0.
    """
    if hour is None:
        hour = 0.0
    ut_hour = hour - tz_offset
    # swe.julday handles day/month rollover correctly for Gregorian dates
    return swe.julday(year, month, day, ut_hour, swe.GREG_CAL)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def compute_chart(
    year: int,
    month: int,
    day: int,
    hour: float,  # local time as decimal hours (0.0 = midnight)
    lat: float,  # degrees N (positive north)
    lon: float,  # degrees E (positive east)
    tz_offset: float = 5.5,  # UTC offset in hours; IST = +5.5
    ayanamsha: str = "lahiri",
    ephe_path: Optional[str] = None,
) -> BirthChart:
    """
    Compute a sidereal Jyotish birth chart.

    Parameters
    ----------
    year, month, day : birth date (Gregorian)
    hour             : local civil time as decimal hours (midnight = 0.0)
    lat, lon         : geographic coordinates (decimal degrees)
    tz_offset        : UTC offset in hours (IST = 5.5)
    ayanamsha        : "lahiri" (default), "raman", or "krishnamurti"
    ephe_path        : path to Swiss Ephemeris data files;
                       None → uses built-in Moshier (accurate to ~1 arcsec)

    Returns
    -------
    BirthChart dataclass with lagna + all 9 Navagrahas (sidereal).
    """
    # --- Ayanamsha validation (P-4 fix: raise on unknown, never silently pass) ---
    ayanamsha_key = ayanamsha.lower().strip()
    if ayanamsha_key not in _AYANAMSHA_MAP:
        raise ValueError(
            f"Unknown ayanamsha {ayanamsha!r}. Supported: {list(_AYANAMSHA_MAP.keys())}"
        )

    # --- Ephemeris setup ---
    if ephe_path:
        swe.set_ephe_path(ephe_path)
    elif Path(_EPHE_PATH).exists():
        swe.set_ephe_path(_EPHE_PATH)
    # If neither, pyswisseph falls back to Moshier (built-in, no files needed)

    swe.set_sid_mode(_AYANAMSHA_MAP[ayanamsha_key])

    # --- Julian Day (UT) ---
    jd_ut = _local_to_jd(year, month, day, hour, tz_offset)

    # --- Ayanamsha value ---
    ayanamsha_val = swe.get_ayanamsa_ut(jd_ut)

    # --- Lagna (Ascendant) ---
    # swe.houses returns tropical cusps; we subtract ayanamsha for sidereal lagna.
    # Use 'P' (Placidus) to get the ascendant degree — house system doesn't matter
    # for Lagna in whole-sign Jyotish; only the ASC degree matters.
    cusps, ascmc = swe.houses(jd_ut, lat, lon, b"P")
    tropical_asc = ascmc[0]
    sidereal_asc = (tropical_asc - ayanamsha_val) % 360
    lagna_sign, lagna_idx, lagna_deg = _sign_from_lon(sidereal_asc)

    # --- Planet positions ---
    # FLG_SIDEREAL applies the ayanamsha correction automatically.
    # FLG_SPEED returns daily motion (negative = retrograde).
    # FLG_MOSEPH falls back gracefully if SE files are absent.
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    planets_out: dict[str, PlanetPosition] = {}

    swe.set_topo(lon, lat, 0)  # S161: topocentric Moon (Swiss Ephemeris Manual §2.3)
    for name, planet_id in _PLANET_IDS.items():
        # Moon requires FLG_TOPOCTR — set_topo() alone is not sufficient (SE Manual §2.3)
        planet_flags = flags | swe.FLG_TOPOCTR if name == "Moon" else flags
        result, _ = swe.calc_ut(jd_ut, planet_id, planet_flags)
        lon_sid = result[0] % 360
        speed = result[3]  # longitude speed, deg/day
        sign, sign_idx, deg_in_sign = _sign_from_lon(lon_sid)
        planets_out[name] = PlanetPosition(
            name=name,
            longitude=lon_sid,
            sign=sign,
            sign_index=sign_idx,
            degree_in_sign=deg_in_sign,
            is_retrograde=(speed < 0),
            speed=speed,
        )

    # Ketu = Rahu + 180° (always "retrograde" — moves opposite to direct motion)
    rahu = planets_out["Rahu"]
    ketu_lon = (rahu.longitude + 180.0) % 360
    ketu_sign, ketu_idx, ketu_deg = _sign_from_lon(ketu_lon)
    planets_out["Ketu"] = PlanetPosition(
        name="Ketu",
        longitude=ketu_lon,
        sign=ketu_sign,
        sign_index=ketu_idx,
        degree_in_sign=ketu_deg,
        is_retrograde=True,
        speed=-abs(rahu.speed),
    )

    return BirthChart(
        jd_ut=jd_ut,
        ayanamsha_name=ayanamsha_key,
        ayanamsha_value=ayanamsha_val,
        lagna=sidereal_asc,
        lagna_sign=lagna_sign,
        lagna_sign_index=lagna_idx,
        lagna_degree_in_sign=lagna_deg,
        planets=planets_out,  # noqa: F841
    )


# Topocentric Moon correction S136
TOPOCENTRIC_MOON_NOTE = "swe.set_topo(lat,lon,0) + SEFLG_TOPOCTR for Moon"


# Topocentric Moon (F-1 S136)
# swe.set_topo(lat,lon,0) before Moon calc; SEFLG_TOPOCTR flag
TOPOCENTRIC_MOON_ENABLED = True  # Active: swe.set_topo() called before Moon
