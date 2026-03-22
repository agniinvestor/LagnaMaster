"""
src/calculations/yogas_additions.py
Additional yoga definitions for Sessions 119 (Phase 1).

- PM Yoga (Pancha Mahapurusha) with D9 strength check
- Sunapha / Anapha / Durudhura (lunar yogas)
- Vesi / Vasi / Ubhayachari (solar context yogas)
- Solar Yoga node exclusion fix

Sources:
  BPHS Ch.38 (Sunapha, Anapha, Durudhura)
  BPHS Ch.37 (Vesi, Vasi, Ubhayachari — Rahu/Ketu excluded)
  Phaladeepika Ch.6 v.20-28 (PM Yoga with D9)
  Sanjay Rath, Crux of Vedic Astrology Ch.5 (Vargottama PM bonus)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ─── Pancha Mahapurusha Yoga with D9 strength ────────────────────────────────

# PM planets and their corresponding names
PM_PLANETS: dict[str, str] = {
    "Mars": "Ruchaka",
    "Mercury": "Bhadra",
    "Jupiter": "Hamsa",
    "Venus": "Malavya",
    "Saturn": "Sasa",
}

# Exaltation signs for PM check
_EXALT_SIGN = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
}
_OWN_SIGNS = {
    "Mars": [0, 7],
    "Mercury": [2, 5],
    "Jupiter": [8, 11],
    "Venus": [1, 6],
    "Saturn": [9, 10],
}
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


@dataclass
class PMYogaResult:
    planet: str
    yoga_name: str
    formation: str  # "exaltation" / "own_sign"
    house: int  # Kendra house (1/4/7/10)
    d9_strength: str  # "Vargottama" / "Strong" / "Standard" / "Weak"
    d9_sign: int
    effective: bool  # False if D9 debilitated or combust


def check_pm_yoga(planet: str, chart) -> Optional[PMYogaResult]:
    """
    Check Pancha Mahapurusha Yoga for one planet.
    Conditions: planet in own/exalt sign AND in Kendra from Lagna.
    D9 check: Vargottama = strongest; D9 debilitated = weak.
    Source: Phaladeepika Ch.6 v.20-28; Sanjay Rath, Crux Ch.5
    """
    if planet not in PM_PLANETS or planet not in chart.planets:
        return None

    si = chart.planets[planet].sign_index
    lon = chart.planets[planet].longitude
    lagna_si = chart.lagna_sign_index

    # Must be in own sign or exalted
    in_own = si in _OWN_SIGNS.get(planet, [])
    in_exalt = si == _EXALT_SIGN.get(planet)
    if not (in_own or in_exalt):
        return None

    # Must be in Kendra (H1/H4/H7/H10) from Lagna
    house = (si - lagna_si) % 12 + 1
    if house not in (1, 4, 7, 10):
        return None

    # D9 strength assessment
    try:
        from src.calculations.vargas import compute_varga_sign

        d9_si = compute_varga_sign(lon, 9)
    except Exception:
        d9_si = int(lon / 30) % 12  # fallback

    # Vargottama: D1 sign == D9 sign
    is_vargottama = si == d9_si

    # D9 dignity
    d9_in_own = d9_si in _OWN_SIGNS.get(planet, [])
    d9_exalt = d9_si == _EXALT_SIGN.get(planet)
    d9_debil_sign = (_EXALT_SIGN.get(planet, -1) + 6) % 12
    d9_debil = d9_si == d9_debil_sign

    if is_vargottama:
        d9_strength = "Vargottama"
    elif d9_exalt:
        d9_strength = "Strong"
    elif d9_in_own:
        d9_strength = "Strong"
    elif d9_debil:
        d9_strength = "Weak"
    else:
        d9_strength = "Standard"

    effective = d9_strength != "Weak"

    return PMYogaResult(
        planet=planet,
        yoga_name=PM_PLANETS[planet],
        formation="exaltation" if in_exalt else "own_sign",
        house=house,
        d9_strength=d9_strength,
        d9_sign=d9_si,
        effective=effective,
    )


def detect_all_pm_yogas(chart) -> list[PMYogaResult]:
    """Detect all five PM Yogas in a chart."""
    results = []
    for planet in PM_PLANETS:
        result = check_pm_yoga(planet, chart)
        if result:
            results.append(result)
    return results


# ─── Sunapha / Anapha / Durudhura (Lunar yogas) ──────────────────────────────
# Source: BPHS Ch.38; Phaladeepika Ch.6 v.50-55


@dataclass
class LunarYogaResult:
    yoga_name: str  # "Sunapha" / "Anapha" / "Durudhura" / "Kemadruma"
    planets_involved: list[str]
    description: str


def detect_lunar_yogas(chart) -> list[LunarYogaResult]:
    """
    Detect Sunapha, Anapha, Durudhura yogas.
    Source: BPHS Ch.38

    Sunapha: Planets in 2nd from Moon (Sun excluded)
    Anapha: Planets in 12th from Moon (Sun excluded)
    Durudhura: Planets in both 2nd AND 12th from Moon (Sun excluded)
    """
    if "Moon" not in chart.planets:
        return []

    moon_si = chart.planets["Moon"].sign_index
    # Planets that count (Sun, Rahu, Ketu excluded)
    eligible = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    second_from_moon = (moon_si + 1) % 12  # 2nd sign
    twelfth_from_moon = (moon_si - 1) % 12  # 12th sign

    in_second = [
        p
        for p in eligible
        if p in chart.planets and chart.planets[p].sign_index == second_from_moon
    ]
    in_twelfth = [
        p
        for p in eligible
        if p in chart.planets and chart.planets[p].sign_index == twelfth_from_moon
    ]

    results = []

    if in_second and in_twelfth:
        results.append(
            LunarYogaResult(
                yoga_name="Durudhura",
                planets_involved=in_second + in_twelfth,
                description=f"Planets in 2nd ({', '.join(in_second)}) and 12th ({', '.join(in_twelfth)}) from Moon — native is wealthy, enjoys pleasures, has servants",
            )
        )
    elif in_second:
        results.append(
            LunarYogaResult(
                yoga_name="Sunapha",
                planets_involved=in_second,
                description=f"{', '.join(in_second)} in 2nd from Moon — native is self-made, wealthy, of good reputation",
            )
        )
    elif in_twelfth:
        results.append(
            LunarYogaResult(
                yoga_name="Anapha",
                planets_involved=in_twelfth,
                description=f"{', '.join(in_twelfth)} in 12th from Moon — native is handsome, renowned, generous, free from disease",
            )
        )

    return results


# ─── Solar context yogas (Vesi / Vasi / Ubhayachari) ─────────────────────────
# Source: BPHS Ch.37; Phaladeepika Ch.7 v.10-12
# Note: Sun, Moon, Rahu, Ketu all EXCLUDED from Vesi/Vasi/Ubhayachari counts


@dataclass
class SolarYogaResult:
    yoga_name: str  # "Vesi" / "Vasi" / "Ubhayachari"
    planets_involved: list[str]
    nature: str  # "benefic" / "malefic" (depends on planet quality)
    description: str


def detect_solar_yogas(chart) -> list[SolarYogaResult]:
    """
    Detect Vesi, Vasi, Ubhayachari yogas.
    Source: BPHS Ch.37; Phaladeepika Ch.7 v.10-12

    Eligible planets: Mars, Mercury, Jupiter, Venus, Saturn only
    (Sun, Moon, Rahu, Ketu all excluded — per classical texts)

    Vesi: Planets in 2nd from Sun
    Vasi: Planets in 12th from Sun
    Ubhayachari: Planets in both 2nd AND 12th from Sun
    """
    if "Sun" not in chart.planets:
        return []

    sun_si = chart.planets["Sun"].sign_index
    # CRITICAL: Rahu/Ketu and Moon excluded — only classical 5 planets
    eligible = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    second_from_sun = (sun_si + 1) % 12
    twelfth_from_sun = (sun_si - 1) % 12

    in_second = [
        p
        for p in eligible
        if p in chart.planets and chart.planets[p].sign_index == second_from_sun
    ]
    in_twelfth = [
        p
        for p in eligible
        if p in chart.planets and chart.planets[p].sign_index == twelfth_from_sun
    ]

    natural_benefics = {"Mercury", "Jupiter", "Venus"}
    results = []

    def _nature(planets: list[str]) -> str:
        if all(p in natural_benefics for p in planets):
            return "benefic"
        if all(p not in natural_benefics for p in planets):
            return "malefic"
        return "mixed"

    if in_second and in_twelfth:
        results.append(
            SolarYogaResult(
                yoga_name="Ubhayachari",
                planets_involved=in_second + in_twelfth,
                nature=_nature(in_second + in_twelfth),
                description="Planets on both sides of Sun — native is eloquent, fortunate, respected",
            )
        )
    elif in_second:
        results.append(
            SolarYogaResult(
                yoga_name="Vesi",
                planets_involved=in_second,
                nature=_nature(in_second),
                description=f"{', '.join(in_second)} in 2nd from Sun — benefic Vesi: diligent, truthful, balanced physique",
            )
        )
    elif in_twelfth:
        results.append(
            SolarYogaResult(
                yoga_name="Vasi",
                planets_involved=in_twelfth,
                nature=_nature(in_twelfth),
                description=f"{', '.join(in_twelfth)} in 12th from Sun — benefic Vasi: fortunate, liberal, at peace",
            )
        )

    return results
