"""
src/calculations/sudarshana.py
Sudarshana Chakra (3-wheel predictive system) + Dasha Pravesh Charts.
Session 159 (Audit D-3, D-4).

Sudarshana Chakra: 3 concentric wheels from Lagna, Sun, and Moon.
When all 3 wheels agree on an effect, it is "certain to manifest."

Sources:
  PVRNR · BPHS Ch.67 (Sudarshana Chakra)
  K.N. Rao · Advanced Techniques of Prediction Vol.2 (Dasha Pravesh)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


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


# ─── Sudarshana Chakra ────────────────────────────────────────────────────────


@dataclass
class SudarshanWheel:
    """One wheel (Lagna/Sun/Moon) of the Sudarshana Chakra."""

    reference: str  # "Lagna" / "Sun" / "Moon"
    reference_sign: int  # 0-11
    house_signs: list[int]  # [12 sign indices, H1..H12]

    def house_sign(self, house: int) -> int:
        return self.house_signs[house - 1]


@dataclass
class SudarshanResult:
    """
    Sudarshana Chakra — 3-wheel concordance analysis.
    Source: PVRNR · BPHS Ch.67
    """

    lagna_wheel: SudarshanWheel
    sun_wheel: SudarshanWheel
    moon_wheel: SudarshanWheel
    concordance_by_house: dict[int, str]  # {house: "Triple"/"Double"/"Single"/"None"}
    activated_houses: list[int]  # Triple + Double concordance houses
    most_active_house: int

    def concordance_strength(self, house: int) -> str:
        return self.concordance_by_house.get(house, "None")


def _build_wheel(reference_si: int, reference: str) -> SudarshanWheel:
    """Build a wheel starting from a reference sign."""
    house_signs = [(reference_si + h) % 12 for h in range(12)]
    return SudarshanWheel(
        reference=reference, reference_sign=reference_si, house_signs=house_signs
    )


def _house_quality(sign: int, planets_in_signs: dict[int, list[str]]) -> str:
    """Simple quality: 'strong' if benefic planet present, else 'neutral'."""
    benefics = {"Jupiter", "Venus", "Moon", "Mercury"}
    malefics = {"Saturn", "Mars", "Sun", "Rahu", "Ketu"}
    planets = planets_in_signs.get(sign, [])
    if any(p in benefics for p in planets):
        return "benefic"
    if any(p in malefics for p in planets):
        return "malefic"
    return "neutral"


def compute_sudarshana_chakra(chart, transit_chart=None) -> SudarshanResult:
    """
    Compute Sudarshana Chakra — 3-wheel concordance.

    For each house: if transit planet activates that house in all 3 wheels,
    the effect is "certain to manifest" (BPHS Ch.67).

    Source: PVRNR · BPHS Ch.67
    """
    lagna_si = chart.lagna_sign_index
    sun_si = chart.planets["Sun"].sign_index if "Sun" in chart.planets else lagna_si
    moon_si = chart.planets["Moon"].sign_index if "Moon" in chart.planets else lagna_si

    lagna_wheel = _build_wheel(lagna_si, "Lagna")
    sun_wheel = _build_wheel(sun_si, "Sun")
    moon_wheel = _build_wheel(moon_si, "Moon")

    # Build planet-in-sign map (use transit if provided, else natal)
    ref_chart = transit_chart if transit_chart else chart
    planets_in_signs: dict[int, list[str]] = {}
    for p, pd in ref_chart.planets.items():
        planets_in_signs.setdefault(pd.sign_index, []).append(p)

    # For each house: check if a transit planet is present in that house
    # in each of the 3 wheels
    concordance = {}
    activated = []

    for house in range(1, 13):
        lagna_sign = lagna_wheel.house_sign(house)
        sun_sign = sun_wheel.house_sign(house)
        moon_sign = moon_wheel.house_sign(house)

        lagna_active = bool(planets_in_signs.get(lagna_sign))
        sun_active = bool(planets_in_signs.get(sun_sign))
        moon_active = bool(planets_in_signs.get(moon_sign))

        count = sum([lagna_active, sun_active, moon_active])
        if count == 3:
            concordance[house] = "Triple"
            activated.append((house, 3))
        elif count == 2:
            concordance[house] = "Double"
            activated.append((house, 2))
        elif count == 1:
            concordance[house] = "Single"
        else:
            concordance[house] = "None"

    most_active = sorted(activated, key=lambda x: x[1], reverse=True)
    most_active_house = most_active[0][0] if most_active else 1

    return SudarshanResult(
        lagna_wheel=lagna_wheel,
        sun_wheel=sun_wheel,
        moon_wheel=moon_wheel,
        concordance_by_house=concordance,
        activated_houses=[h for h, _ in activated],
        most_active_house=most_active_house,
    )


# ─── Dasha Pravesh Charts ─────────────────────────────────────────────────────


@dataclass
class DashaPraveshResult:
    """
    Dasha Pravesh Chakra — annual chart for a dasha year.
    Source: K.N. Rao · Advanced Techniques Vol.2 Ch.4
    """

    planet: str
    query_year: int
    natal_planet_longitude: float
    return_jd: Optional[float]
    return_date_approx: str
    note: str


def compute_dasha_pravesh(
    planet: str,
    natal_chart,
    query_year: int,
    lat: float = 28.6,
    lon: float = 77.2,
) -> DashaPraveshResult:
    """
    Compute when a dasha lord returns to its natal longitude in query_year.
    This is the Dasha Pravesh moment — the annual chart is cast for this instant.

    Source: K.N. Rao · Advanced Techniques of Prediction Vol.2 Ch.4
    """
    if planet not in natal_chart.planets:
        return DashaPraveshResult(
            planet=planet,
            query_year=query_year,
            natal_planet_longitude=0.0,
            return_jd=None,
            return_date_approx=f"{query_year}-??-??",
            note=f"{planet} not found in natal chart",
        )

    natal_lon = natal_chart.planets[planet].longitude

    try:
        import swisseph as swe

        swe.set_sid_mode(swe.SIDM_LAHIRI)

        # Planet orbital periods (approximate sidereal years)
        _PERIODS = {
            "Sun": 1.0,
            "Moon": 0.0748,
            "Mars": 1.881,
            "Mercury": 0.241,
            "Jupiter": 11.86,
            "Venus": 0.615,
            "Saturn": 29.46,
        }

        if planet not in _PERIODS:
            raise ValueError(f"No orbital period for {planet}")

        period = _PERIODS[planet]
        birth_jd = natal_chart.jd_ut if hasattr(natal_chart, "jd_ut") else 2432126.7
        target_jd = birth_jd + (query_year - 1947) * 365.25

        _SWISSEPH_PLANETS = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
        }

        swe_planet = _SWISSEPH_PLANETS.get(planet, swe.SUN)
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

        # Binary search for return
        jd_low = target_jd - period * 365.25 / 2
        jd_high = target_jd + period * 365.25 / 2

        for _ in range(50):
            jd_mid = (jd_low + jd_high) / 2
            res, _ = swe.calc_ut(jd_mid, swe_planet, flags)
            diff = (res[0] - natal_lon + 360) % 360
            if diff > 180:
                diff -= 360
            if abs(diff) < 0.001:
                break
            if diff > 0:
                jd_high = jd_mid
            else:
                jd_low = jd_mid

        return_jd = (jd_low + jd_high) / 2
        y, m, d, _ = swe.revjul(return_jd)
        date_str = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"

        return DashaPraveshResult(
            planet=planet,
            query_year=query_year,
            natal_planet_longitude=natal_lon,
            return_jd=round(return_jd, 4),
            return_date_approx=date_str,
            note=f"{planet} returns to natal longitude {natal_lon:.2f}° on {date_str}",
        )

    except Exception as e:
        return DashaPraveshResult(
            planet=planet,
            query_year=query_year,
            natal_planet_longitude=natal_lon,
            return_jd=None,
            return_date_approx=f"{query_year}-??-??",
            note=f"Computation requires pyswisseph: {e}",
        )
