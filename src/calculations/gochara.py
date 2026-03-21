"""
src/calculations/gochara.py
============================
Gochara (Transit) Analysis.

Computes planetary positions for a given transit date and maps each
transiting planet against the natal chart:
  - Transit house (whole-sign, counted from natal lagna)
  - Ashtakavarga bindus for the transit sign from each planet's table
  - Sade Sati detection (Saturn within ±1 sign of natal Moon sign)

Usage:
    from src.calculations.gochara import compute_gochara
    report = compute_gochara(natal_chart, transit_date=date(2026, 3, 19))
    print(report.planets["Saturn"].natal_house)
    print(report.sade_sati_phase)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

import swisseph as swe

from src.ephemeris import BirthChart, PlanetPosition, SIGNS, _AYANAMSHA_MAP, _PLANET_IDS
from src.calculations.ashtakavarga import compute_ashtakavarga

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TransitPlanet:
    """Transit position of one planet relative to the natal chart."""
    planet: str
    longitude: float        # sidereal longitude 0–360°
    sign: str
    sign_index: int         # 0 = Aries
    degree_in_sign: float
    is_retrograde: bool
    speed: float            # deg/day (negative = retrograde)
    natal_house: int        # whole-sign house from natal lagna (1–12)
    av_bindus: int          # Ashtakavarga bindus for this sign (−1 if N/A)


@dataclass
class GocharaReport:
    """Full Gochara (transit) analysis for a given date."""
    transit_date: date
    natal_lagna_sign: str
    natal_moon_sign: str
    natal_moon_sign_index: int
    planets: dict[str, TransitPlanet]   # 9 planets (incl. Rahu/Ketu)

    # Sade Sati (Saturn's 7.5-year period)
    sade_sati: bool          # True if Saturn is in Sade Sati
    sade_sati_phase: str     # "Rising", "Peak", "Setting", or "None"

    # Jupiter transit over natal Moon
    guru_transit_house: int          # house number (from lagna) Jupiter is in
    guru_chandal_transit: bool       # Jupiter + Rahu in same sign in transit

    def transit_house(self, planet: str) -> int:
        """Return the natal house the transiting planet currently occupies."""
        return self.planets[planet].natal_house


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_transit_positions(
    transit_date: date,
    ayanamsha_key: str,
) -> dict[str, tuple[float, float]]:
    """
    Return {planet: (sidereal_longitude, speed)} for the given date.
    Uses noon UTC as the reference time (suitable for daily transit analysis).
    """
    # JD for noon UTC on transit_date
    jd_ut = swe.julday(
        transit_date.year, transit_date.month, transit_date.day,
        12.0,   # noon UTC
        swe.GREG_CAL,
    )
    swe.set_sid_mode(_AYANAMSHA_MAP[ayanamsha_key])
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    positions: dict[str, tuple[float, float]] = {}
    for name, planet_id in _PLANET_IDS.items():
        result, _ = swe.calc_ut(jd_ut, planet_id, flags)
        lon_sid = result[0] % 360
        speed   = result[3]
        positions[name] = (lon_sid, speed)

    # Ketu = Rahu + 180°
    rahu_lon, rahu_spd = positions["Rahu"]
    positions["Ketu"] = ((rahu_lon + 180.0) % 360, -abs(rahu_spd))

    return positions


def _whole_sign_house(planet_sign_index: int, lagna_sign_index: int) -> int:
    """Return the whole-sign house number (1–12) a planet occupies."""
    return (planet_sign_index - lagna_sign_index) % 12 + 1


def _sade_sati_phase(saturn_si: int, moon_si: int) -> tuple[bool, str]:
    """
    Sade Sati: Saturn transiting natal Moon sign ±1 sign.
    - Rising: Saturn in sign before natal Moon (moon_si - 1 mod 12)
    - Peak:   Saturn in natal Moon sign
    - Setting: Saturn in sign after natal Moon (moon_si + 1 mod 12)
    """
    prev_si = (moon_si - 1) % 12
    next_si = (moon_si + 1) % 12
    if saturn_si == moon_si:
        return True, "Peak"
    elif saturn_si == prev_si:
        return True, "Rising"
    elif saturn_si == next_si:
        return True, "Setting"
    return False, "None"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_gochara(
    natal_chart: BirthChart,
    transit_date: date | None = None,
) -> GocharaReport:
    """
    Compute Gochara (transit) analysis for natal_chart on transit_date.

    Parameters
    ----------
    natal_chart   : BirthChart from compute_chart()
    transit_date  : the date to analyse transits (default: today)

    Returns
    -------
    GocharaReport with all 9 planets' transit positions relative to natal chart.
    """
    if transit_date is None:
        transit_date = date.today()

    lagna_si   = natal_chart.lagna_sign_index
    moon_si    = natal_chart.planets["Moon"].sign_index
    moon_sign  = natal_chart.planets["Moon"].sign
    ayanamsha  = natal_chart.ayanamsha_name

    # Compute transit positions
    transit_pos = _compute_transit_positions(transit_date, ayanamsha)

    # Ashtakavarga for natal chart (used for AV bindus at transit sign)
    av = compute_ashtakavarga(natal_chart)
    # Only 7 planets have AV tables
    _AV_PLANETS = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}

    transit_planets: dict[str, TransitPlanet] = {}
    for planet_name, (lon, speed) in transit_pos.items():
        si  = int(lon / 30) % 12
        deg = lon - si * 30
        sign = SIGNS[si]
        natal_house = _whole_sign_house(si, lagna_si)

        av_bindus = -1  # Rahu/Ketu have no AV table
        if planet_name in _AV_PLANETS:
            av_bindus = av.planet_av[planet_name].bindus[si]

        transit_planets[planet_name] = TransitPlanet(
            planet=planet_name,
            longitude=lon,
            sign=sign,
            sign_index=si,
            degree_in_sign=deg,
            is_retrograde=(speed < 0),
            speed=speed,
            natal_house=natal_house,
            av_bindus=av_bindus,
        )

    # Sade Sati
    saturn_si = transit_planets["Saturn"].sign_index
    sade_sati, ss_phase = _sade_sati_phase(saturn_si, moon_si)

    # Jupiter transit
    guru_house = transit_planets["Jupiter"].natal_house
    guru_chandal = (
        transit_planets["Jupiter"].sign_index ==
        transit_planets["Rahu"].sign_index
    )

    return GocharaReport(
        transit_date=transit_date,
        natal_lagna_sign=natal_chart.lagna_sign,
        natal_moon_sign=moon_sign,
        natal_moon_sign_index=moon_si,
        planets=transit_planets,  # noqa: F841
        sade_sati=sade_sati,
        sade_sati_phase=ss_phase,
        guru_transit_house=guru_house,
        guru_chandal_transit=guru_chandal,
    )


# Guru Sade Sati modulation (XI-D)
def guru_modulates_sade_sati(natal_moon_si: int, jupiter_transit_si: int) -> bool:
    """Jupiter adjacent to or aspecting natal Moon during Sade Sati mitigates it.
    Source: Classical Gochara texts; K.N. Rao references"""
    house_from_moon = ((jupiter_transit_si - natal_moon_si) % 12) + 1
    return house_from_moon in {1, 2, 12, 5, 9}  # adjacent or trine
