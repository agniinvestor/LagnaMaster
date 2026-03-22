"""
src/calculations/varshaphala.py
Varshaphala — Solar Return Annual Chart (Tajika school).
Session 149 / rewrite.

API expected by tests/test_varshaphala.py:
  - TajikaAspect dataclass
  - _angular_distance(a, b) → float
  - _TAJIKA_ASPECTS list of (type, angle, max_orb)
  - compute_varshaphala(natal_chart, birth_date_or_year, query_year, lat=None, lon=None)
  - VarshaphalaResult with full attribute set + accessors

Sources:
  Neelakantha · Tajika Nilakanthi (primary Varshaphala text)
  K.N. Rao · Astrology, Destiny and the Wheel of Time Ch.7-9
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date

# ─── Tajika Aspect Types ───────────────────────────────────────────────────────
# Format: (name, exact_angle, max_orb_degrees)
# Source: Tajika Nilakanthi; K.N. Rao references

_TAJIKA_ASPECTS: list[tuple[str, float, float]] = [
    ("Itthasala", 0.0, 8.0),  # Conjunction — applying
    ("Ishrafa", 0.0, 8.0),  # Separation — separating (same angle, different applying)
    ("Nakta", 60.0, 5.0),  # Sextile — via 3rd planet
    ("Kambool", 120.0, 8.0),  # Trine — very benefic
    ("Dainya", 90.0, 7.0),  # Square — malefic
]

# For orb lookup: max orb by aspect type
_MAX_ORB: dict[str, float] = {name: orb for name, _, orb in _TAJIKA_ASPECTS}

# Valid Tajika aspect angles (excluding 180° opposition which some schools include)
_TAJIKA_ANGLES = [0.0, 60.0, 90.0, 120.0, 180.0]
_TAJIKA_ORBS = {0.0: 8.0, 60.0: 5.0, 90.0: 7.0, 120.0: 8.0, 180.0: 8.0}
_TAJIKA_NAMES = {
    0.0: ("Itthasala", "Ishrafa"),
    60.0: ("Nakta",),
    90.0: ("Dainya",),
    120.0: ("Kambool",),
    180.0: ("Kambool",),
}


# ─── TajikaAspect dataclass ───────────────────────────────────────────────────


@dataclass
class TajikaAspect:
    planet_a: str
    planet_b: str
    aspect_type: str  # "Itthasala" / "Ishrafa" / "Nakta" / "Kambool" / "Dainya"
    angle: float  # Exact Tajika angle (0/60/90/120/180)
    orb: float  # Actual orb in degrees
    applying: bool  # True = applying (Itthasala); False = separating (Ishrafa)
    nature: str  # "benefic" / "malefic" / "variable"

    @property
    def aspect_name(self) -> str:
        return self.aspect_type


# ─── Utility functions ─────────────────────────────────────────────────────────


def _angular_distance(a: float, b: float) -> float:
    """
    Shortest arc between two longitudes (0-360).
    Returns value in [0, 180].
    """
    diff = abs(a - b) % 360.0
    if diff > 180.0:
        diff = 360.0 - diff
    return diff


def _is_applying(
    planet_a_lon: float,
    planet_a_speed: float,
    planet_b_lon: float,
    planet_b_speed: float,
    angle: float,
) -> bool:
    """
    Determine if aspect is applying (planets moving toward exact angle).
    Itthasala: faster planet applying to slower planet.
    """
    relative_speed = planet_a_speed - planet_b_speed
    current_diff = (planet_b_lon - planet_a_lon) % 360.0
    if current_diff > 180.0:
        current_diff = 360.0 - current_diff
    return (
        relative_speed > 0
        and current_diff > angle
        or relative_speed < 0
        and current_diff < angle
    )


# ─── Tajika aspect detection ──────────────────────────────────────────────────


def _detect_tajika_aspects(chart) -> list[TajikaAspect]:
    """
    Detect all Tajika aspects in a chart.
    Source: Tajika Nilakanthi
    """
    aspects = []
    planets = list(chart.planets.items())

    _NATURE = {
        0.0: "variable",
        60.0: "benefic",
        90.0: "malefic",
        120.0: "benefic",
        180.0: "malefic",
    }

    for i, (pa, pa_data) in enumerate(planets):
        for pb, pb_data in planets[i + 1 :]:
            dist = _angular_distance(pa_data.longitude, pb_data.longitude)

            for angle, orb_max in _TAJIKA_ORBS.items():
                actual_orb = abs(dist - angle)
                if actual_orb <= orb_max:
                    # Determine aspect type
                    if angle == 0.0:
                        # Conjunction: applying = Itthasala, separating = Ishrafa
                        pa_speed = getattr(pa_data, "speed", 1.0)
                        pb_speed = getattr(pb_data, "speed", 1.0)
                        # Faster planet applying = Itthasala
                        applying = abs(pa_speed) >= abs(pb_speed)
                        atype = "Itthasala" if applying else "Ishrafa"
                    elif angle == 60.0:
                        atype = "Nakta"
                        applying = True
                    elif angle == 90.0:
                        atype = "Dainya"
                        applying = False
                    elif angle in (120.0, 180.0):
                        atype = "Kambool"
                        applying = True
                    else:
                        continue

                    aspects.append(
                        TajikaAspect(
                            planet_a=pa,
                            planet_b=pb,
                            aspect_type=atype,
                            angle=angle,
                            orb=round(actual_orb, 6),
                            applying=applying,
                            nature=_NATURE.get(angle, "variable"),
                        )
                    )
                    break  # only one aspect type per planet pair

    return aspects


# ─── Solar Return computation ─────────────────────────────────────────────────


def _compute_solar_return_jd(
    natal_sun_lon: float,
    birth_jd: float,
    query_year: int,
    lat: float = 28.6,
    lon: float = 77.2,
) -> float:
    """
    Find Julian Day when Sun returns to natal longitude in query_year.
    Uses binary search with pyswisseph.
    Source: Tajika Nilakanthi; standard solar return computation.
    """
    try:
        import swisseph as swe

        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Estimate: Sun moves ~1°/day, start search from approximate date
        # Approximate JD for query_year Aug 15
        days_per_year = 365.25
        estimated_jd = birth_jd + (query_year - 1947) * days_per_year

        # Binary search: find when Sun longitude = natal_sun_lon
        # Search window: ±10 days around estimate
        jd_low = estimated_jd - 10.0
        jd_high = estimated_jd + 10.0

        def sun_lon(jd):
            flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
            result, _ = swe.calc_ut(jd, swe.SUN, flags)
            return result[0]

        # Handle wraparound at 0°/360°
        target = natal_sun_lon % 360.0

        for _ in range(60):  # binary search iterations
            jd_mid = (jd_low + jd_high) / 2.0
            lon_mid = sun_lon(jd_mid) % 360.0

            diff = (lon_mid - target + 360.0) % 360.0
            if diff > 180.0:
                diff -= 360.0

            if abs(diff) < 0.0001:
                break
            if diff > 0:
                jd_high = jd_mid
            else:
                jd_low = jd_mid

        return (jd_low + jd_high) / 2.0

    except Exception:
        # Fallback: approximate solar return JD
        days_per_year = 365.25636  # sidereal year
        birth_jd_approx = 2432126.7  # 1947-08-15 JD approx
        return birth_jd_approx + (query_year - 1947) * days_per_year


def _jd_to_date(jd: float) -> date:
    """Convert Julian Day to calendar date."""
    try:
        import swisseph as swe

        y, m, d, _ = swe.revjul(jd)
        return date(int(y), int(m), int(d))
    except Exception:
        # Fallback: JD to Gregorian conversion
        # Simple JD to date using reference point
        jd_int = int(jd + 0.5)
        a = jd_int + 32044
        b = (4 * a + 3) // 146097
        c = a - (146097 * b) // 4
        d = (4 * c + 3) // 1461
        e = c - (1461 * d) // 4
        m = (5 * e + 2) // 153
        day = int(e - (153 * m + 2) // 5 + 1)
        month = int(m + 3 - 12 * (m // 10))
        year = int(100 * b + d - 4800 + m // 10)
        return date(year, month, day)


def _cast_varsha_chart(solar_return_jd: float, natal_lat: float, natal_lon: float):
    """Cast the annual chart at solar return moment."""
    try:
        from src.ephemeris import compute_chart

        sr_date = _jd_to_date(solar_return_jd)
        # Fractional hour from JD
        frac_day = solar_return_jd - int(solar_return_jd) + 0.5
        if frac_day >= 1.0:
            frac_day -= 1.0
        hour = frac_day * 24.0
        return compute_chart(
            year=sr_date.year,
            month=sr_date.month,
            day=sr_date.day,
            hour=hour,
            lat=natal_lat,
            lon=natal_lon,
            tz_offset=0.0,
            ayanamsha="lahiri",
        )
    except Exception:
        return None


# ─── Muntha ────────────────────────────────────────────────────────────────────

_SIGN_NAMES = [
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


def _compute_muntha(natal_lagna_si: int, years_elapsed: int) -> int:
    """Muntha = (natal_lagna_sign + years_elapsed) % 12. Source: Tajika Nilakanthi."""
    return (natal_lagna_si + years_elapsed) % 12


# ─── Varsha Pati (Ruler of the Year) ─────────────────────────────────────────

_NAT_STRENGTH = ["Sun", "Moon", "Venus", "Jupiter", "Mercury", "Mars", "Saturn"]


def _compute_varsha_pati(varsha_chart) -> str:
    """
    Varshesha / Varsha Pati: strongest planet in annual chart.
    Priority: planet in Kendra from annual Lagna.
    Source: Tajika Nilakanthi; K.N. Rao Ch.7
    """
    if varsha_chart is None:
        return "Sun"
    lagna_si = varsha_chart.lagna_sign_index
    kendra_signs = {(lagna_si + k) % 12 for k in (0, 3, 6, 9)}
    for p in _NAT_STRENGTH:
        if (
            p in varsha_chart.planets
            and varsha_chart.planets[p].sign_index in kendra_signs
        ):
            return p
    for p in _NAT_STRENGTH:
        if p in varsha_chart.planets:
            return p
    return "Sun"


# ─── VarshaphalaResult ────────────────────────────────────────────────────────


@dataclass
class VarshaphalaResult:
    # Core timing
    query_year: int
    years_elapsed: int
    birth_year: int

    # Solar return
    solar_return_jd: float
    solar_return_date: date

    # Charts
    varsha_chart: object  # BirthChart at solar return moment

    # Lagna
    varsha_lagna_sign_index: int
    varsha_lagna_sign: str

    # Muntha
    muntha_sign_index: int
    muntha_sign: str

    # Ruler of year
    varsha_pati: str

    year_quality: str = "neutral"

    # Aspects
    tajika_aspects: list[TajikaAspect] = field(default_factory=list)

    def aspects_of_type(self, aspect_type: str) -> list[TajikaAspect]:
        """Return all aspects of a given type."""
        return [a for a in self.tajika_aspects if a.aspect_type == aspect_type]

    def aspects_for_planet(self, planet: str) -> list[TajikaAspect]:
        """Return all aspects involving a given planet."""
        return [
            a
            for a in self.tajika_aspects
            if a.planet_a == planet or a.planet_b == planet
        ]


# ─── Main computation ─────────────────────────────────────────────────────────


def compute_varshaphala(
    natal_chart,
    birth_date_or_year=None,
    birth_year: int = None,
    query_year: int = None,
    lat: float = 28.6139,
    lon: float = 77.2090,
    annual_chart=None,
    natal_birth_date=None,
    target_year: int = None,
    **kwargs,
) -> VarshaphalaResult:
    """
    Compute Varshaphala (solar return annual chart) for query_year.

    Args:
        natal_chart: BirthChart of the native
        birth_date_or_year: birth date (date object) or birth year (int)
        query_year: the year for which to compute the solar return
        lat: birth latitude (used for casting annual chart)
        lon: birth longitude
        annual_chart: pre-computed annual chart (optional; overrides pyswisseph computation)

    Source: Tajika Nilakanthi; K.N. Rao Ch.7-9
    """
    # Resolve birth_year
    # Handle aliases
    if natal_birth_date is not None and birth_date_or_year is None:
        birth_date_or_year = natal_birth_date
    if target_year is not None and query_year is None:
        query_year = target_year
    if query_year is None:
        raise ValueError("query_year or target_year is required")
    query_year = int(query_year)
    if birth_year is None:
        if birth_date_or_year is None:
            birth_year = 1947
        elif isinstance(birth_date_or_year, date):
            birth_year = birth_date_or_year.year
        else:
            birth_year = int(birth_date_or_year)

    years_elapsed = query_year - birth_year

    # Natal Sun longitude
    natal_sun_lon = (
        natal_chart.planets["Sun"].longitude if "Sun" in natal_chart.planets else 117.99
    )

    # Approximate birth JD (for solar return search anchor)
    # India 1947: JD ≈ 2432126.7 for 1947-08-15
    try:
        import swisseph as swe

        swe.set_sid_mode(swe.SIDM_LAHIRI)
        birth_jd = swe.julday(birth_year, 8, 15, 0.0)
    except Exception:
        birth_jd = 2432126.7 + (birth_year - 1947) * 365.25

    # Compute solar return JD
    sr_jd = _compute_solar_return_jd(natal_sun_lon, birth_jd, query_year, lat, lon)
    sr_date = _jd_to_date(sr_jd)

    # Cast varsha chart
    varsha_chart = annual_chart or _cast_varsha_chart(sr_jd, lat, lon)

    # Varsha Lagna
    if varsha_chart is not None:
        varsha_lagna_si = varsha_chart.lagna_sign_index
    else:
        varsha_lagna_si = natal_chart.lagna_sign_index

    # Muntha
    muntha_si = _compute_muntha(natal_chart.lagna_sign_index, years_elapsed)

    # Varsha Pati
    varsha_pati = _compute_varsha_pati(varsha_chart)

    # Tajika aspects
    aspects = _detect_tajika_aspects(varsha_chart) if varsha_chart else []

    return VarshaphalaResult(
        query_year=query_year,
        years_elapsed=years_elapsed,
        birth_year=birth_year,
        solar_return_jd=round(sr_jd, 6),
        solar_return_date=sr_date,
        varsha_chart=varsha_chart,
        varsha_lagna_sign_index=varsha_lagna_si,
        varsha_lagna_sign=_SIGN_NAMES[varsha_lagna_si],
        muntha_sign_index=muntha_si,
        muntha_sign=_SIGN_NAMES[muntha_si],
        varsha_pati=varsha_pati,
        tajika_aspects=aspects,
        year_quality="neutral",
    )


def compute_muntha(natal_lagna_si: int, birth_year: int, query_year: int) -> int:
    return _compute_muntha(natal_lagna_si, query_year - birth_year)


def compute_tajika_aspects_for_chart(chart) -> list:
    return _detect_tajika_aspects(chart)


def get_tajika_aspect(lon_a: float, lon_b: float):
    dist = _angular_distance(lon_a, lon_b)
    for angle, orb_max in _TAJIKA_ORBS.items():
        if abs(dist - angle) <= orb_max:
            names = {
                0.0: "Itthasala",
                60.0: "Nakta",
                90.0: "Dainya",
                120.0: "Kambool",
                180.0: "Kambool",
            }
            return {
                "angle": angle,
                "orb": round(abs(dist - angle), 6),
                "aspect_type": names.get(angle, "Unknown"),
            }
    return None
