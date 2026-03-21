"""
src/calculations/kp.py
=======================
KP (Krishnamurti Paddhati) Sub-lord System — Session 17.

KP divides each of the 27 nakshatras into 9 sub-lords proportional to
the Vimshottari Dasha periods (totalling 120 years).  A further
sub-sub-lord division (sometimes called "sub-sub") is also provided.

Structure of KP cusps within one nakshatra (span = 800 arcminutes = 13°20'):
─────────────────────────────────────────────────────────────────────────────
  Planet    Dasha yrs   Sub-span (arcmin)   Sub-span (degrees)
  ─────────────────────────────────────────────────────────────
  Ketu          7        46.6667             0.7778°
  Venus         20       133.3333            2.2222°
  Sun           6        40.0000             0.6667°
  Moon          10       66.6667             1.1111°
  Mars          7        46.6667             0.7778°
  Rahu          18       120.0000            2.0000°
  Jupiter       16       106.6667            1.7778°
  Saturn        19       126.6667            2.1111°
  Mercury       17       113.3333            1.8889°
  ──────────────────────────────────────────────────
  Total         120      800.0000            13.3333°

The sequence repeats across all 27 nakshatras (243 sub-lords total).
The sub-sub division applies the same proportional split within each sub.

House Significators (KP):
  Each KP house cusp is defined by the Sub-lord that governs that cusp.
  The cusp position is the sidereal longitude of the house cusp.
  (This module uses the whole-sign cusp as the cusp longitude for
  the pilot — i.e. each house begins at 0° of its sign.)

Key terms:
  Star Lord  (SL)  — nakshatra lord of the planet's longitude
  Sub Lord   (SubL) — KP sub-lord at the planet's longitude
  Sub-Sub    (SS)   — further subdivision (optional fine analysis)

Public API
----------
    compute_kp(chart: BirthChart) -> KPChart
    kp_sub_at(longitude: float) -> KPPosition

Data classes
------------
    KPPosition — star_lord, sub_lord, sub_sub_lord, longitude
    KPPlanet   — wraps KPPosition for a planet
    KPChart    — all 9 planets + Lagna KP positions + house significators
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ephemeris import BirthChart

# ── Vimshottari sequence and periods ─────────────────────────────────────────

_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury",
]

_VIMSH_YEARS: dict[str, int] = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
_TOTAL_YEARS = 120

# Nakshatra span in degrees
_NAK_SPAN = 360.0 / 27          # 13.333...°
_NAK_SPAN_MIN = _NAK_SPAN * 60  # 800' arcminutes

# Sub-span for each planet within one nakshatra (in degrees)
_SUB_SPAN: dict[str, float] = {
    p: _VIMSH_YEARS[p] / _TOTAL_YEARS * _NAK_SPAN
    for p in _SEQUENCE
}
# Verify total ≈ _NAK_SPAN
assert abs(sum(_SUB_SPAN.values()) - _NAK_SPAN) < 1e-9

# Nakshatra names and their lords (27 entries = _SEQUENCE × 3)
_NAK_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
_NAK_LORDS = (_SEQUENCE * 3)[:27]  # Ketu→Venus→Sun→Moon→Mars→Rahu→Jup→Sat→Mer × 3


# ── KP position lookup ────────────────────────────────────────────────────────

@dataclass
class KPPosition:
    """KP cuspal analysis for a single longitude."""
    longitude: float       # sidereal, 0–360°
    nakshatra: str
    nakshatra_index: int   # 0–26
    star_lord: str         # nakshatra lord
    sub_lord: str          # KP sub-lord
    sub_sub_lord: str      # KP sub-sub-lord (optional finer analysis)
    sub_degree_start: float  # longitude where this sub begins
    sub_degree_end: float    # longitude where this sub ends


def kp_sub_at(longitude: float) -> KPPosition:
    """
    Compute the KP Star Lord, Sub Lord, and Sub-Sub Lord for any sidereal
    longitude (0–360°).

    Algorithm
    ---------
    1. Find nakshatra index: `nak_idx = int(longitude / _NAK_SPAN)`
    2. Star lord = _NAK_LORDS[nak_idx]
    3. Within the nakshatra, the subs are laid out sequentially starting
       from the nakshatra lord's sub (not always Ketu).
       Starting planet index = position of star_lord in _SEQUENCE.
    4. Walk through sub-spans until the longitude is enclosed.
    5. Apply the same logic recursively within the sub for sub-sub.

    This correctly handles the fact that subs within a nakshatra start
    from the *nakshatra's own lord*, not from Ketu.
    """
    lon = longitude % 360.0
    nak_idx = min(int(lon / _NAK_SPAN), 26)
    nak_start = nak_idx * _NAK_SPAN
    pos_in_nak = lon - nak_start     # 0 … _NAK_SPAN

    star_lord = _NAK_LORDS[nak_idx]
    start_idx = _SEQUENCE.index(star_lord)

    # Walk subs within nakshatra
    cursor = 0.0
    sub_lord = star_lord
    sub_start = 0.0
    sub_end = _NAK_SPAN
    for i in range(9):
        planet = _SEQUENCE[(start_idx + i) % 9]
        span = _SUB_SPAN[planet]
        if cursor + span > pos_in_nak or i == 8:
            sub_lord = planet
            sub_start = nak_start + cursor
            sub_end = nak_start + cursor + span
            break
        cursor += span

    # Sub-sub: same pattern within the sub
    pos_in_sub = lon - sub_start
    sub_span_total = sub_end - sub_start
    sub2_start_idx = _SEQUENCE.index(sub_lord)
    cursor2 = 0.0
    sub_sub_lord = sub_lord
    for i in range(9):
        planet = _SEQUENCE[(sub2_start_idx + i) % 9]
        frac = _VIMSH_YEARS[planet] / _TOTAL_YEARS
        span2 = frac * sub_span_total
        if cursor2 + span2 > pos_in_sub or i == 8:
            sub_sub_lord = planet
            break
        cursor2 += span2

    return KPPosition(
        longitude=lon,
        nakshatra=_NAK_NAMES[nak_idx],
        nakshatra_index=nak_idx,
        star_lord=star_lord,
        sub_lord=sub_lord,
        sub_sub_lord=sub_sub_lord,
        sub_degree_start=sub_start,
        sub_degree_end=sub_end,
    )


# ── KP Planet ─────────────────────────────────────────────────────────────────

@dataclass
class KPPlanet:
    """KP analysis for a single planet in the birth chart."""
    planet: str
    longitude: float
    sign: str
    sign_index: int
    is_retrograde: bool
    kp: KPPosition

    @property
    def star_lord(self) -> str:
        return self.kp.star_lord

    @property
    def sub_lord(self) -> str:
        return self.kp.sub_lord

    @property
    def sub_sub_lord(self) -> str:
        return self.kp.sub_sub_lord

    @property
    def nakshatra(self) -> str:
        return self.kp.nakshatra


# ── House Significators ───────────────────────────────────────────────────────

@dataclass
class KPHouseSignificator:
    """
    KP significator analysis for one house (1–12).

    In KP, a house's "sub-lord" is the planet that governs the KP sub at
    the house cusp longitude.  This pilot uses whole-sign cusps (0° of
    each house sign).

    Significators of a house are planets that:
      (a) occupy the house (direct significators)
      (b) are the house lord
      (c) are star lords of planets in the house
    """
    house: int
    cusp_longitude: float
    cusp_star_lord: str
    cusp_sub_lord: str       # "House Sub Lord" — key KP concept
    occupants: list[str]     # planets in this house
    house_lord: str
    significators: list[str]  # ranked: occupants → star lords → house lord


_SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_ALL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


# ── KPChart ───────────────────────────────────────────────────────────────────

@dataclass
class KPChart:
    """Complete KP analysis for a birth chart."""
    lagna_kp: KPPosition
    planets: dict[str, KPPlanet]            # 9 planets
    houses: dict[int, KPHouseSignificator]  # 1–12

    def for_planet(self, planet: str) -> KPPlanet:
        return self.planets[planet]

    def house_sub_lord(self, house: int) -> str:
        return self.houses[house].cusp_sub_lord

    def significators_of(self, house: int) -> list[str]:
        return self.houses[house].significators


# ── main public function ──────────────────────────────────────────────────────

def compute_kp(chart) -> KPChart:           # chart: BirthChart
    """
    Compute the full KP chart analysis for a BirthChart.

    Covers:
      - Star Lord / Sub Lord / Sub-Sub Lord for every planet and the Lagna
      - House Cusp Sub Lords (whole-sign cusps, pilot version)
      - Significators per house (occupants + lord + star-lords of occupants)

    Parameters
    ----------
    chart : BirthChart
        Output of src.ephemeris.compute_chart().

    Returns
    -------
    KPChart
    """
    # ── Lagna ──────────────────────────────────────────────────────────────
    lagna_kp = kp_sub_at(chart.lagna)

    # ── Planets ────────────────────────────────────────────────────────────
    kp_planets: dict[str, KPPlanet] = {}
    for pname in _ALL_PLANETS:
        pp = chart.planets.get(pname)
        if pp is None:
            continue
        kp_pos = kp_sub_at(pp.longitude)
        kp_planets[pname] = KPPlanet(
            planet=pname,
            longitude=pp.longitude,
            sign=pp.sign,
            sign_index=pp.sign_index,
            is_retrograde=pp.is_retrograde,
            kp=kp_pos,
        )

    # ── Houses (whole-sign pilot) ──────────────────────────────────────────
    lagna_si = chart.lagna_sign_index
    houses: dict[int, KPHouseSignificator] = {}

    # Precompute which house each planet is in (whole-sign)
    planet_house: dict[str, int] = {}
    for pname, pp in chart.planets.items():
        h = (pp.sign_index - lagna_si) % 12 + 1
        planet_house[pname] = h

    for h in range(1, 13):
        house_si = (lagna_si + h - 1) % 12
        # Whole-sign cusp = start of the sign (0° of that sign)
        cusp_lon = house_si * 30.0
        cusp_kp = kp_sub_at(cusp_lon)
        lord = _SIGN_LORDS[house_si]
        occupants = [p for p, hh in planet_house.items() if hh == h]

        # Significators:
        # Level 1: planets occupying the house
        # Level 2: star lords of those occupants (planets whose nakshatra lord is in the house)
        # Level 3: house lord (bhavesh)
        sigs: list[str] = []
        seen: set[str] = set()

        # Level 1 — occupants
        for p in occupants:
            if p not in seen:
                sigs.append(p)
                seen.add(p)

        # Level 2 — star lords whose signified planet is an occupant
        for p in _ALL_PLANETS:
            if p in seen:
                continue
            pp = chart.planets.get(p)
            if pp is None:
                continue
            if kp_planets[p].star_lord in occupants or \
               kp_planets[p].sub_lord in occupants:
                sigs.append(p)
                seen.add(p)

        # Level 3 — house lord
        if lord not in seen:
            sigs.append(lord)
            seen.add(lord)

        houses[h] = KPHouseSignificator(
            house=h,
            cusp_longitude=cusp_lon,
            cusp_star_lord=cusp_kp.star_lord,
            cusp_sub_lord=cusp_kp.sub_lord,
            occupants=occupants,
            house_lord=lord,
            significators=sigs,
        )

    return KPChart(
        lagna_kp=lagna_kp,
        planets=kp_planets,  # noqa: F841
        houses=houses,
    )
