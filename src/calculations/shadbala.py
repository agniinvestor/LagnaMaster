"""
src/calculations/shadbala.py
==============================
Simplified Shadbala — 6 components of planetary strength in Virupas.
Source: CALC_Shadbala (Excel), BPHS Ch.27, Saravali.

Implements: Uchcha, Kendradi, Ojha-Yugma, Dig Bala, Naisargika, Paksha.
Chesta Bala computed from pyswisseph speed (S-2 bug noted in comments).
Saptavargaja deferred to Phase 2 (requires divisional charts D2/D3/D7/D9/D12/D30).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from src.ephemeris import BirthChart, SIGNS
from src.calculations.dignity import DignityLevel, compute_all_dignities
from src.calculations.house_lord import compute_house_map


# ---------------------------------------------------------------------------
# Minimum Shadbala thresholds (BPHS Ch.27)
# ---------------------------------------------------------------------------

SHADBALA_MIN: dict[str, float] = {
    "Sun":     390.0,
    "Moon":    360.0,
    "Mars":    300.0,
    "Mercury": 420.0,
    "Jupiter": 390.0,
    "Venus":   330.0,
    "Saturn":  300.0,
}


# ---------------------------------------------------------------------------
# Naisargika Bala (permanent natural strength constants)
# BPHS Ch.27 — fixed values, never change
# ---------------------------------------------------------------------------

NAISARGIKA_BALA: dict[str, float] = {
    "Sun":     60.00,
    "Moon":    51.43,
    "Venus":   42.86,
    "Jupiter": 34.29,
    "Mercury": 25.71,
    "Mars":    17.14,
    "Saturn":   8.57,
    # Rahu/Ketu not included in classical Shadbala
}

# Mean daily motions (degrees/day) for Chesta Bala calculation
_MEAN_DAILY_MOTION: dict[str, float] = {
    "Sun":     0.9856,
    "Moon":   13.1763,
    "Mars":    0.5240,
    "Mercury": 1.3833,
    "Jupiter": 0.0831,
    "Venus":   1.2000,
    "Saturn":  0.0335,
}


@dataclass
class ShadbalaPlanet:
    planet: str
    uchcha: float        # dignity / exaltation strength
    kendradi: float      # house position strength
    ojha_yugma: float    # odd/even sign gender affinity
    dig_bala: float      # directional strength
    naisargika: float    # permanent natural strength
    paksha: float        # lunar phase strength
    chesta: float        # motional strength (from pyswisseph speed)
    total: float         # sum of above
    minimum: float       # BPHS minimum threshold
    ishta_pct: float     # total / minimum * 100
    meets_minimum: bool


@dataclass
class ShadbalaResult:
    planets: dict[str, ShadbalaPlanet] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [f"{'Planet':<10} {'Total':>7} {'Min':>7} {'Ishta%':>8} {'OK':>4}"]
        lines.append("-" * 42)
        for p in self.planets.values():
            ok = "✓" if p.meets_minimum else "✗"
            lines.append(
                f"{p.planet:<10} {p.total:>7.1f} {p.minimum:>7.0f} "
                f"{p.ishta_pct:>7.1f}% {ok:>4}"
            )
        return "\n".join(lines)


def compute_shadbala(chart: BirthChart) -> ShadbalaResult:
    """
    Compute simplified Shadbala for all 7 classical planets.
    Rahu and Ketu are excluded (no classical Shadbala).
    """
    dignities = compute_all_dignities(chart)
    house_map = compute_house_map(chart)
    sun_lon = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude

    result = ShadbalaResult()
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    for planet in classical:
        p = chart.planets[planet]

        # --- Uchcha Bala (0-60 Virupas): based on distance from exaltation/debilitation ---
        uchcha = _uchcha_bala(planet, p.longitude)

        # --- Kendradi Bala ---
        house = house_map.planet_house[planet]
        kendradi = _kendradi_bala(house)

        # --- Ojha-Yugma Bala ---
        ojha = _ojha_yugma_bala(planet, p.sign_index)

        # --- Dig Bala ---
        dig = _dig_bala_virupas(planet, house)

        # --- Naisargika Bala ---
        naisargika = NAISARGIKA_BALA.get(planet, 0.0)

        # --- Paksha Bala (lunar phase) ---
        paksha = _paksha_bala(planet, sun_lon, moon_lon)

        # --- Chesta Bala (motional strength from speed) ---
        # S-2 note: CALC_Shadbala cell J14 had a formula error (=3851).
        # We compute correctly: min(60, mean_motion / |actual_speed| * 60)
        # Retrograde = 60 Virupas (Saravali: Rx planet = full Chesta)
        chesta = _chesta_bala(planet, p.speed, p.is_retrograde)

        total = uchcha + kendradi + ojha + dig + naisargika + paksha + chesta
        minimum = SHADBALA_MIN.get(planet, 300.0)
        ishta_pct = (total / minimum * 100) if minimum > 0 else 0.0

        result.planets[planet] = ShadbalaPlanet(
            planet=planet,
            uchcha=uchcha,
            kendradi=kendradi,
            ojha_yugma=ojha,
            dig_bala=dig,
            naisargika=naisargika,
            paksha=paksha,
            chesta=chesta,
            total=total,
            minimum=minimum,
            ishta_pct=ishta_pct,
            meets_minimum=(total >= minimum),
        )
    return result


# ---------------------------------------------------------------------------
# Component calculations
# ---------------------------------------------------------------------------

# Exaltation + debilitation longitudes for Uchcha Bala
_EXALT_LON = {
    "Sun":     10.0,    # 10° Aries
    "Moon":    33.0,    # 3° Taurus  (30+3)
    "Mars":   298.0,    # 28° Capricorn (270+28)
    "Mercury":165.0,    # 15° Virgo  (150+15)
    "Jupiter":  95.0,   # 5° Cancer  (90+5)
    "Venus":   357.0,   # 27° Pisces (330+27)
    "Saturn":  200.0,   # 20° Libra  (180+20)
}

def _uchcha_bala(planet: str, longitude: float) -> float:
    """
    Uchcha Bala (0-60 Virupas):
    60 at exact exaltation, 0 at exact debilitation, linear in between.
    """
    exalt = _EXALT_LON.get(planet)
    if exalt is None:
        return 30.0   # default
    debil = (exalt + 180.0) % 360.0
    lon = longitude % 360.0

    # Distance from exaltation (shorter arc)
    d_exalt = abs(lon - exalt) % 360
    d_exalt = min(d_exalt, 360 - d_exalt)
    # Uchcha Bala = 60 * (180 - d_exalt) / 180   (BPHS Ch.27)
    return 60.0 * (180.0 - d_exalt) / 180.0


def _kendradi_bala(house: int) -> float:
    """Kendradi Bala: Kendra=60, Panapara=30, Apoklima=15."""
    if house in (1, 4, 7, 10):
        return 60.0
    elif house in (2, 5, 8, 11):
        return 30.0
    else:
        return 15.0


# Odd/even sign affinity (REF_Zodiac row 16)
_MALE_PLANETS = {"Sun", "Mars", "Jupiter"}
_FEMALE_PLANETS = {"Moon", "Venus"}
# Mercury and Saturn are neutral (=15 always)

def _ojha_yugma_bala(planet: str, sign_idx: int) -> float:
    """
    Ojha-Yugma Bala:
    Male planets strong in odd signs (30V), female in even signs (30V); neutral=15V.
    """
    is_odd = (sign_idx % 2 == 0)  # 0-indexed: Aries=0 is odd sign (#1)
    if planet in _MALE_PLANETS:
        return 30.0 if is_odd else 0.0
    elif planet in _FEMALE_PLANETS:
        return 30.0 if not is_odd else 0.0
    else:
        return 15.0   # Mercury, Saturn neutral


# Dig Bala peak houses (CALC_DigBala col B)
_DIG_BALA_PEAK: dict[str, list[int]] = {
    "Sun":     [10],
    "Moon":    [4],
    "Mars":    [10, 3],
    "Mercury": [1],
    "Jupiter": [1, 9],
    "Venus":   [4],
    "Saturn":  [7],
}

def _dig_bala_virupas(planet: str, house: int) -> float:
    """
    Dig Bala (0-60 Virupas): 60 in peak house, linear interpolation to 0 at opposite.
    """
    peaks = _DIG_BALA_PEAK.get(planet, [1])
    # Distance from nearest peak (in house count, wrapping 1-12)
    min_dist = min(
        min(abs(house - pk), 12 - abs(house - pk)) for pk in peaks
    )
    # 60 at dist=0, 0 at dist=6
    return max(0.0, 60.0 * (1.0 - min_dist / 6.0))


_BENEFIC_PLANETS = {"Moon", "Mercury", "Jupiter", "Venus"}
_MALEFIC_PLANETS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

def _paksha_bala(planet: str, sun_lon: float, moon_lon: float) -> float:
    """
    Paksha Bala (0-60 Virupas):
    Benefics strong in waxing (Shukla) phase; malefics in waning (Krishna) phase.
    Moon-Sun angle: 0°=new moon, 180°=full moon.
    Sun itself = always 30 (Paksha has no effect per BPHS).
    """
    if planet == "Sun":
        return 30.0   # constant

    # Moon-Sun angular separation (0=new, 180=full)
    angle = (moon_lon - sun_lon) % 360.0
    is_waxing = angle <= 180.0
    # Normalised phase 0.0 (new moon) → 1.0 (full moon)
    phase = angle / 180.0 if is_waxing else (360.0 - angle) / 180.0

    if planet in _BENEFIC_PLANETS:
        return 60.0 * phase if is_waxing else 60.0 * (1.0 - phase)
    elif planet in _MALEFIC_PLANETS:
        return 60.0 * (1.0 - phase) if is_waxing else 60.0 * phase
    return 30.0


def _chesta_bala(planet: str, speed: float, is_retrograde: bool) -> float:
    """
    Chesta Bala (0-60 Virupas):
    Retrograde = 60 (Saravali: Rx = max Chesta).
    Direct: min(60, mean_daily_motion / |actual_speed| * 60).

    S-2 note: CALC_Shadbala J14 had formula error (computed 3851 instead of ~15.9
    for Saturn). Correct formula: min(60, mean / |speed| * 60).
    """
    if is_retrograde:
        return 60.0   # Rx = full Chesta (Saravali Ch.3)

    mean = _MEAN_DAILY_MOTION.get(planet, 1.0)
    actual_speed = abs(speed)
    if actual_speed < 1e-6:
        return 30.0   # stationary — moderate strength

    return min(60.0, mean / actual_speed * 60.0)
