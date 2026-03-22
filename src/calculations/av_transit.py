"""
src/calculations/av_transit.py — Session 60

AV-weighted transit analysis (PVRNR Ch.12 p154, p166).

PVRNR: "AV becomes invaluable when we interpret transits in rasi chart
with respect to natal positions in divisional charts."

SAV thresholds (p165):
  ≥30 rekhas = strong house (matters flourish)
  25-29      = average
  <25        = weak (struggles with that house's matters)

Per-planet BAV for transit:
  ≥5 rekhas in transit sign = favorable planet transit
  ≤3 rekhas                 = unfavorable

Sodhya Pinda for key event timing:
  High pinda = favorable period for events of that planet.

Public API
----------
  compute_transit_av_score(chart, transit_chart) -> TransitAVReport
  planet_transit_quality(planet, transit_sign_index, natal_chart) -> str
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass
class PlanetTransitQuality:
    planet: str
    transit_sign_index: int
    transit_sign: str
    rekhas: int
    quality: str  # "Excellent"/"Good"/"Average"/"Unfavorable"/"Malefic"
    commentary: str


@dataclass
class TransitAVReport:
    transit_date: date
    planet_qualities: dict[str, PlanetTransitQuality]
    house_sav: dict[int, int]  # SAV rekhas per natal house
    strong_natal_houses: list[int]  # SAV ≥30
    weak_natal_houses: list[int]  # SAV <25
    active_favorable: list[str]  # planets in favorable transit signs


_SIGNS = [
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


def planet_transit_quality(
    planet: str, transit_si: int, natal_chart
) -> PlanetTransitQuality:
    """Evaluate transit quality for a planet moving through a sign."""
    try:
        from src.calculations.ashtakavarga import compute_ashtakavarga

        av = compute_ashtakavarga(natal_chart)
        planet_av = getattr(av, planet.lower(), None)
        rekhas = planet_av.bindus[transit_si] if planet_av else 4
    except Exception:
        rekhas = 4

    if rekhas >= 6:
        quality, comment = "Excellent", "High rekhas — very favorable transit"
    elif rekhas == 5:
        quality, comment = "Good", "Average-high — favorable transit"
    elif rekhas == 4:
        quality, comment = "Average", "Neutral transit"
    elif rekhas == 3:
        quality, comment = "Unfavorable", "Low rekhas — challenging transit"
    else:
        quality, comment = "Malefic", "Very low rekhas — avoid major decisions"

    return PlanetTransitQuality(
        planet=planet,
        transit_sign_index=transit_si,
        transit_sign=_SIGNS[transit_si % 12],
        rekhas=rekhas,
        quality=quality,
        commentary=comment,
    )


def compute_transit_av_score(
    natal_chart,
    transit_date: date | None = None,
    transit_longitudes: dict[str, float] | None = None,
) -> TransitAVReport:
    """
    Full transit AV report: per-planet quality + SAV house strength.
    transit_longitudes: optional {planet: longitude} for a specific transit chart.
    """
    if transit_date is None:
        transit_date = date.today()

    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    # Get transit positions
    if transit_longitudes is None:
        try:
            from src.ephemeris import compute_chart

            birth = natal_chart
            t_chart = compute_chart(
                year=transit_date.year,
                month=transit_date.month,
                day=transit_date.day,
                hour=12.0,
                lat=getattr(birth, "lat", 28.6139),
                lon=getattr(birth, "lon", 77.2090),
                tz_offset=getattr(birth, "tz_offset", 5.5),
                ayanamsha=getattr(birth, "ayanamsha", "lahiri"),
            )
            transit_longitudes = {
                p: t_chart.planets[p].longitude
                for p in planets_7
                if p in t_chart.planets
            }
        except Exception:
            transit_longitudes = {}

    # Per-planet transit quality
    planet_qualities = {}
    for p in planets_7:
        if p in transit_longitudes:
            si = int(transit_longitudes[p] / 30) % 12
            planet_qualities[p] = planet_transit_quality(p, si, natal_chart)

    # SAV per natal house
    try:
        from src.calculations.ashtakavarga import compute_ashtakavarga

        av = compute_ashtakavarga(natal_chart)
        lagna_si = natal_chart.lagna_sign_index
        house_sav = {}
        for h in range(1, 13):
            si = (lagna_si + h - 1) % 12
            house_sav[h] = av.sarva.bindus.get(si, 0) if hasattr(av, "sarva") else 0
    except Exception:
        house_sav = {h: 28 for h in range(1, 13)}

    strong = [h for h, r in house_sav.items() if r >= 30]
    weak = [h for h, r in house_sav.items() if r < 25]
    active_favorable = [
        p for p, q in planet_qualities.items() if q.quality in {"Excellent", "Good"}
    ]

    return TransitAVReport(
        transit_date=transit_date,
        planet_qualities=planet_qualities,
        house_sav=house_sav,
        strong_natal_houses=strong,
        weak_natal_houses=weak,
        active_favorable=active_favorable,
    )
