"""
src/calculations/shadbala.py
Planetary strength in Virupas (Shadbala) — complete implementation.

Session 111 changes (Phase 0 classical correctness):
  - Dig Bala: degree-arc formula (was house-number distance — dimensionally wrong)
  - Kala Bala: all 8 sub-components (was only Paksha Bala)
  - Drik Bala: aspect-sum from all planet pairs (was always 0)
  - Naisargika Bala: verified exact values from BPHS Ch.27
  - Saptavargaja Bala: uses vargas.py (requires D1/D2/D3/D7/D9/D12/D30)
  - Ishta/Kashta Bala: sqrt(Uchcha*Chesta) / sqrt((60-U)*(60-C))

Sources:
  BPHS Ch.27 v.1-75 (all Shadbala components)
  Phaladeepika Ch.2 (combustion and dignity)
  Saravali Ch.3 (Chesta Bala)
"""

from __future__ import annotations  # noqa: F401
from dataclasses import dataclass  # noqa: F401
from math import sqrt  # noqa: F401
from datetime import datetime  # noqa: F401
from typing import Optional  # noqa: F401

# ─── Constants ───────────────────────────────────────────────────────────────

# Naisargika (Natural) Bala — fixed hierarchy, never changes
# Source: BPHS Ch.27
NAISARGIKA_BALA: dict[str, float] = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Venus": 42.86,
    "Jupiter": 34.29,
    "Mercury": 25.71,
    "Mars": 17.14,
    "Saturn": 8.57,
}

# Dig Bala peak house for each planet
# Source: BPHS Ch.27 v.12-15
DIG_BALA_PEAK_HOUSE: dict[str, int] = {
    "Sun": 10,  # H10 = 10th house
    "Mars": 10,
    "Moon": 4,
    "Venus": 4,
    "Mercury": 1,
    "Jupiter": 1,
    "Saturn": 7,
}

# Saptavargaja Bala Virupas — BPHS Ch.27 v.2-4 (p.265, Santhanam Vol 1)
# Uses 7-level compound (Panchadha) relationship, NOT simple dignity.
# "Moolatrikona Rasi 45, own Rasi 30, extreme friend 20, friend 15,
#  neutral 10, enemy 4, extreme enemy 2 Virupas"
SAPTAVARGAJA_VIRUPAS_BPHS: dict[str, float] = {
    "Moolatrikona": 45.0,
    "Own": 30.0,
    "Adhi Mitra": 20.0,
    "Mitra": 15.0,
    "Sama": 10.0,
    "Shatru": 4.0,
    "Adhi Shatru": 2.0,
}

# Legacy lookup (kept for backward compat with shodashavarga_bala.py)
SAPTAVARGAJA_VIRUPAS: dict[str, float] = {
    "DEEP_EXALT": 30.0,
    "EXALT": 30.0,
    "MOOLTRIKONA": 45.0,  # corrected: was 30.0
    "OWN_SIGN": 30.0,  # corrected: was 22.5
    "FRIEND_SIGN": 15.0,
    "NEUTRAL": 10.0,  # corrected: was 7.5
    "ENEMY_SIGN": 4.0,  # corrected: was 3.75
    "DEBIL": 2.0,  # corrected: was 1.875
    "NEECHA_BHANGA_RAJA": 30.0,
    "NEECHA_BHANGA": 10.0,
}

# 7 vargas used for Saptavargaja Bala
SAPTAVARGA_LIST = [1, 2, 3, 7, 9, 12, 30]

# Ojha-Yugma Bala — male planets in odd signs, female in even signs = 30 Virupas
MALE_PLANETS = {"Sun", "Mars", "Jupiter"}
FEMALE_PLANETS = {"Moon", "Venus"}
# Mercury, Saturn: neutral — get 15 Virupas regardless

# Kendradi Bala
KENDRADI_VIRUPAS: dict[str, float] = {
    "kendra": 60.0,  # H1/H4/H7/H10
    "panapara": 30.0,  # H2/H5/H8/H11
    "apoklima": 15.0,  # H3/H6/H9/H12
}

# Aspect partial strengths (Phase 0 fix: BPHS Ch.26 v.3-5)
# Used for Drik Bala computation
ASPECT_STRENGTH: dict[tuple[str, int], float] = {
    ("Mars", 4): 0.75,
    ("Mars", 8): 0.75,
    ("Jupiter", 5): 0.75,
    ("Jupiter", 9): 0.75,
    ("Saturn", 3): 0.75,
    ("Saturn", 10): 0.75,
}

# Hora sequence for Kala Bala (weekday lord order)
_HORA_SEQUENCE = ["Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter", "Mars"]
_WEEKDAY_LORDS = [
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Sun",
]  # Mon=0

# Vara Bala: each weekday's ruling planet gets 45 Virupas
# Hora Bala: birth hora lord gets 60 Virupas
# Masa Bala: month lord gets 30 Virupas
# Abda Bala: year lord gets 15 Virupas
# Tribhaga Bala: 20 Virupas each
# Nathonnata Bala: 60 Virupas
# Ayana Bala: 0-60 Virupas


# ─── Result dataclass ────────────────────────────────────────────────────────


@dataclass
class ShadbalResult:
    planet: str

    # Sthana Bala components
    uchcha_bala: float = 0.0  # 0-60 (from dignity.py)
    saptavargaja_bala: float = 0.0  # 0-175 (7 vargas × dignity)
    ojha_yugma_bala: float = 0.0  # 15 or 30
    kendradi_bala: float = 0.0  # 15/30/60
    drekkana_bala: float = 0.0  # 15 (male in 1st/female in 3rd drekkana)
    # sthana total
    sthana_bala: float = 0.0

    # Dig Bala
    dig_bala: float = 0.0  # 0-60

    # Kala Bala components
    nathonnata_bala: float = 0.0
    paksha_bala: float = 0.0
    tribhaga_bala: float = 0.0
    vara_bala: float = 0.0
    hora_bala: float = 0.0
    masa_bala: float = 0.0
    abda_bala: float = 0.0
    ayana_bala: float = 0.0
    # kala total
    kala_bala: float = 0.0

    # Chesta Bala
    chesta_bala: float = 0.0  # 0-60

    # Naisargika Bala
    naisargika_bala: float = 0.0  # fixed

    # Drik Bala
    drik_bala: float = 0.0  # signed sum of aspects received

    # Totals
    total: float = 0.0  # sum of all components

    # Derived
    ishta_bala: float = 0.0  # sqrt(uchcha * chesta)
    kashta_bala: float = 0.0  # sqrt((60-uchcha) * (60-chesta))

    @property
    def is_strong(self) -> bool:
        """Minimum Shadbala threshold per BPHS."""
        thresholds = {
            "Sun": 390,
            "Moon": 360,
            "Mars": 300,
            "Mercury": 420,
            "Jupiter": 390,
            "Venus": 330,
            "Saturn": 300,
        }
        return self.total >= thresholds.get(self.planet, 300)


# ─── Dig Bala ────────────────────────────────────────────────────────────────


def compute_dig_bala(planet: str, chart) -> float:
    """
    Dig Bala using degree-arc formula.
    Formula: 60 * (180 - arc_distance_from_peak_cusp) / 180
    Source: BPHS Ch.27 v.12-15
    """
    if planet not in DIG_BALA_PEAK_HOUSE:
        return 0.0

    peak_house = DIG_BALA_PEAK_HOUSE[planet]
    lagna_lon = chart.lagna

    # Cusp longitude of peak house (whole-sign: house N starts at lagna + (N-1)*30)
    peak_cusp_lon = (lagna_lon + (peak_house - 1) * 30) % 360

    planet_lon = chart.planets[planet].longitude
    arc_dist = min(
        abs(planet_lon - peak_cusp_lon) % 360,
        360 - abs(planet_lon - peak_cusp_lon) % 360,
    )
    return max(0.0, round(60.0 * (180.0 - arc_dist) / 180.0, 3))


# ─── Kendradi Bala ────────────────────────────────────────────────────────────


def compute_kendradi_bala(planet: str, chart) -> float:
    from src.calculations.house_lord import compute_house_map  # noqa: F401

    hmap = compute_house_map(chart)
    h = hmap.planet_house.get(planet, 1)
    if h in (1, 4, 7, 10):
        return KENDRADI_VIRUPAS["kendra"]
    if h in (2, 5, 8, 11):
        return KENDRADI_VIRUPAS["panapara"]
    return KENDRADI_VIRUPAS["apoklima"]


# ─── Ojha-Yugma Bala ─────────────────────────────────────────────────────────


def compute_ojha_yugma_bala(planet: str, chart) -> float:
    if planet not in chart.planets:
        return 15.0
    si = chart.planets[planet].sign_index
    is_odd_sign = si % 2 == 0  # Aries=0 is odd
    if planet in MALE_PLANETS:
        return 30.0 if is_odd_sign else 0.0
    if planet in FEMALE_PLANETS:
        return 30.0 if not is_odd_sign else 0.0
    return 15.0  # neutral planets (Mercury, Saturn)


# ─── Kala Bala — all 8 sub-components ───────────────────────────────────────


def compute_kala_bala(
    planet: str, chart, birth_dt: Optional[datetime] = None
) -> tuple[float, dict[str, float]]:
    """
    Compute Kala Bala with all 8 sub-components.
    Returns (total_kala_bala, component_dict)
    Source: BPHS Ch.27 v.30-62
    """
    components: dict[str, float] = {}

    # 1. Nathonnata Bala (day/night strength)
    # Sun/Jupiter/Venus: strong by day (Natha)
    # Moon/Mars/Saturn: strong by night (Unnata)
    # Mercury: strong both day and night
    if birth_dt is not None:
        hour = birth_dt.hour + birth_dt.minute / 60.0
        is_day = 6.0 <= hour < 18.0  # simplified; ideally use sunrise
    else:
        # Default: use Sun's position (above horizon = day)
        sun_lon = chart.planets["Sun"].longitude if "Sun" in chart.planets else 270.0
        is_day = not (90 <= sun_lon % 360 < 270)

    day_planets = {"Sun", "Jupiter", "Venus"}
    night_planets = {"Moon", "Mars", "Saturn"}
    if planet == "Mercury":
        components["nathonnata"] = 60.0
    elif planet in day_planets:
        components["nathonnata"] = 60.0 if is_day else 0.0
    elif planet in night_planets:
        components["nathonnata"] = 0.0 if is_day else 60.0
    else:
        components["nathonnata"] = 30.0

    # 2. Paksha Bala (lunar phase)
    if "Moon" in chart.planets and "Sun" in chart.planets:
        moon_lon = chart.planets["Moon"].longitude
        sun_lon = chart.planets["Sun"].longitude
        elongation = (moon_lon - sun_lon) % 360
        paksha_frac = (
            elongation / 180.0 if elongation <= 180 else (360 - elongation) / 180.0
        )
        # Benefics strong in waxing (Shukla), malefics in waning (Krishna)
        malefics = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
        if planet in malefics:
            paksha_frac = 1.0 - paksha_frac
        components["paksha"] = round(60.0 * paksha_frac, 3)
    else:
        components["paksha"] = 30.0

    # 3. Tribhaga Bala (day/night thirds)
    if birth_dt is not None:
        hour = birth_dt.hour + birth_dt.minute / 60.0
        if is_day:
            watch = int((hour - 6) / 4) % 3
            tribhaga_lords = {0: "Jupiter", 1: "Sun", 2: "Saturn"}
        else:
            night_hour = hour if hour < 6 else hour - 18
            watch = int(night_hour / 4) % 3
            tribhaga_lords = {0: "Moon", 1: "Venus", 2: "Mars"}
        components["tribhaga"] = 20.0 if planet == tribhaga_lords.get(watch) else 0.0
    else:
        components["tribhaga"] = 0.0

    # 4. Vara Bala (weekday lord)
    if birth_dt is not None:
        weekday = birth_dt.weekday()  # 0=Mon
        vara_lord = _WEEKDAY_LORDS[weekday]
        components["vara"] = 45.0 if planet == vara_lord else 0.0
    else:
        components["vara"] = 0.0

    # 5. Hora Bala (planetary hour)
    if birth_dt is not None:
        weekday = birth_dt.weekday()
        hour = birth_dt.hour + birth_dt.minute / 60.0
        hora_num = int(hour)  # 0-23
        (
            _WEEKDAY_LORDS.index("Sun") if "Sun" in _WEEKDAY_LORDS else 6
        )  # noqa: F841
        # Sequence starts from weekday lord at sunrise (hour 0 of that day)
        weekday_lord_idx = _HORA_SEQUENCE.index(_WEEKDAY_LORDS[weekday])
        hora_lord_idx = (weekday_lord_idx + hora_num) % 7
        hora_lord = _HORA_SEQUENCE[hora_lord_idx]
        components["hora"] = 60.0 if planet == hora_lord else 0.0
    else:
        components["hora"] = 0.0

    # 6. Masa Bala (month lord — simplified: use Sun's sign for solar month)
    if birth_dt is not None:
        sun_sign = chart.planets["Sun"].sign_index if "Sun" in chart.planets else 0
        # Solar month lords cycle: Aries=Mars, Taurus=Venus, etc.
        month_lords = [
            "Mars",
            "Venus",
            "Mercury",
            "Moon",
            "Sun",
            "Mercury",
            "Venus",
            "Mars",
            "Jupiter",
            "Saturn",
            "Saturn",
            "Jupiter",
        ]
        masa_lord = month_lords[sun_sign % 12]
        components["masa"] = 30.0 if planet == masa_lord else 0.0
    else:
        components["masa"] = 0.0

    # 7. Abda Bala (year lord — use weekday of January 1 of birth year)
    if birth_dt is not None:
        jan1 = datetime(birth_dt.year, 1, 1)
        year_lord = _WEEKDAY_LORDS[jan1.weekday()]
        components["abda"] = 15.0 if planet == year_lord else 0.0
    else:
        components["abda"] = 0.0

    # 8. Ayana Bala (Sun's declination effect)
    # Simplified: Sun in Uttarayana (Capricorn-Gemini = signs 9-2) benefits solar planets
    if "Sun" in chart.planets:
        sun_si = chart.planets["Sun"].sign_index
        uttarayana = sun_si in (9, 10, 11, 0, 1, 2)
        sun_benefited = {"Sun", "Mars", "Jupiter"}
        moon_benefited = {"Moon", "Venus", "Saturn"}
        if planet in sun_benefited:
            components["ayana"] = 48.0 if uttarayana else 12.0
        elif planet in moon_benefited:
            components["ayana"] = 12.0 if uttarayana else 48.0
        else:
            components["ayana"] = 30.0
    else:
        components["ayana"] = 30.0

    total = sum(components.values())
    return round(total, 3), components


# ─── Chesta Bala ─────────────────────────────────────────────────────────────


def compute_chesta_bala(planet: str, chart) -> float:
    """
    Chesta Bala from planet's speed relative to mean motion.
    Source: Saravali Ch.3; BPHS Ch.27
    """
    if planet not in chart.planets:
        return 30.0

    # Mean motions in degrees/day
    MEAN_MOTION: dict[str, float] = {
        "Sun": 0.9856,
        "Moon": 13.176,
        "Mars": 0.524,
        "Mercury": 1.383,
        "Jupiter": 0.083,
        "Venus": 1.2,
        "Saturn": 0.033,
    }
    if planet not in MEAN_MOTION:
        return 30.0

    speed = abs(chart.planets[planet].speed)
    mean = MEAN_MOTION[planet]
    is_rx = chart.planets[planet].is_retrograde

    if is_rx:
        # Retrograde: Chesta Bala from how far from stationary
        chesta = 60.0 * min(speed / mean, 1.0)
    else:
        chesta = 60.0 * min(speed / mean, 1.0) if mean > 0 else 30.0

    return round(min(60.0, max(0.0, chesta)), 3)


# ─── Drik Bala ───────────────────────────────────────────────────────────────


def compute_drik_bala(planet: str, chart) -> float:
    """
    Drik Bala: signed sum of aspectual strength received from all other planets.
    Source: BPHS Ch.27 v.22-29, using continuous drishti from Ch.26 v.6-8.

    Benefic aspects add virupas, malefic aspects subtract.
    Uses degree-based BPHS drishti (speculum table) instead of house-based binary.
    """
    if planet not in chart.planets:
        return 0.0

    from src.calculations.sputa_drishti import bphs_drishti_with_specials

    planet_lon = chart.planets[planet].longitude
    total = 0.0

    natural_benefics = {"Moon", "Mercury", "Jupiter", "Venus"}
    natural_malefics = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

    for aspector, aspector_pos in chart.planets.items():
        if aspector == planet:
            continue
        # Arc from aspector to aspected planet
        arc = (planet_lon - aspector_pos.longitude) % 360.0
        virupas = bphs_drishti_with_specials(aspector, arc)

        if virupas > 0:
            rupa_fraction = virupas / 60.0
            # BPHS Ch.27 v.19 (p.284): "Reduce one fourth if malefic aspects,
            # add a fourth if benefic. Super add entire aspect of Mercury and Jupiter."
            if aspector in ("Mercury", "Jupiter"):
                # Full aspect added (special rule for Mercury/Jupiter)
                total += rupa_fraction
            elif aspector in natural_benefics:
                total += rupa_fraction * 0.25
            elif aspector in natural_malefics:
                total -= rupa_fraction * 0.25

    return round(total * 60.0, 3)  # convert Rupas to Virupas


# ─── Saptavargaja Bala ────────────────────────────────────────────────────────


def compute_saptavargaja_bala(planet: str, chart) -> float:
    """
    Saptavargaja Bala: dignity across 7 divisional charts.
    Requires vargas.py to provide D1/D2/D3/D7/D9/D12/D30.
    Source: BPHS Ch.27 v.1-20
    """
    try:
        from src.calculations.vargas import compute_varga_sign  # noqa: F401
    except ImportError:
        return 0.0

    if planet not in chart.planets:
        return 0.0

    longitude = chart.planets[planet].longitude
    total = 0.0

    for varga_n in SAPTAVARGA_LIST:
        try:
            varga_sign = compute_varga_sign(longitude, varga_n)
        except Exception:
            continue

        # Determine relationship-based virupas in this varga (BPHS Ch.27 v.2-4)
        virupas = _get_saptavargaja_virupas(
            planet, varga_sign, longitude, varga_n, chart=chart,
        )
        total += virupas

    return round(total, 3)


def _get_saptavargaja_virupas(
    planet: str, sign_index: int, longitude: float, varga_n: int,
    chart=None,
) -> float:
    """Determine Virupas for a planet in a given varga sign.

    BPHS Ch.27 v.2-4: uses compound (Panchadha) relationship with sign lord.
    Exaltation/debilitation are NOT Saptavargaja categories — those are
    handled by Uchcha Bala. Saptavargaja uses: MT, Own, and 5-fold relationship.

    Note on compound relationships (p.265 notes): "compound relationships of
    two given planets be seen in the Rasi chart only and not in the concerned
    divisional chart."
    """
    from src.calculations.dignity import MOOLTRIKONA_RANGES

    V = SAPTAVARGAJA_VIRUPAS_BPHS

    if planet in ("Rahu", "Ketu"):
        return V["Sama"]

    lord = _simple_sign_lord(sign_index)
    if not lord or lord == planet:
        # Planet is in its own sign
        # Check if MT (D1: degree range; other vargas: sign match only)
        if planet in MOOLTRIKONA_RANGES:
            mt_si, mt_s, mt_e = MOOLTRIKONA_RANGES[planet]
            if sign_index == mt_si:
                if varga_n == 1:
                    deg = longitude % 30
                    if mt_s <= deg < mt_e:
                        return V["Moolatrikona"]
                    return V["Own"]  # own sign portion of MT sign
                return V["Moolatrikona"]  # in other vargas, MT sign = MT
        return V["Own"]

    # Planet is in another planet's sign — use compound relationship
    if chart is not None:
        try:
            from src.calculations.panchadha_maitri import panchadha_relation
            rel = panchadha_relation(planet, lord, chart)
            return V.get(rel, V["Sama"])
        except Exception:
            pass

    # Fallback: simple Naisargika if chart not available
    from src.calculations.dignity import _NAISARGIKA
    nai = _NAISARGIKA.get((planet, lord), "Neutral")
    if nai == "Friend":
        return V["Mitra"]
    if nai == "Enemy":
        return V["Shatru"]
    return V["Sama"]


def _simple_sign_lord(sign_index: int) -> Optional[str]:
    lords = {
        0: "Mars",
        1: "Venus",
        2: "Mercury",
        3: "Moon",
        4: "Sun",
        5: "Mercury",
        6: "Venus",
        7: "Mars",
        8: "Jupiter",
        9: "Saturn",
        10: "Saturn",
        11: "Jupiter",
    }
    return lords.get(sign_index)


# ─── Ishta / Kashta Bala ─────────────────────────────────────────────────────


def compute_ishta_kashta(uchcha_bala: float, chesta_bala: float) -> tuple[float, float]:
    """
    Ishta Bala = sqrt(uchcha * chesta)
    Kashta Bala = sqrt((60-uchcha) * (60-chesta))
    Source: BPHS Ch.27 v.70-75
    """
    uchcha = max(0.0, min(60.0, uchcha_bala))
    chesta = max(0.0, min(60.0, chesta_bala))
    ishta = round(sqrt(uchcha * chesta), 3)
    kashta = round(sqrt((60.0 - uchcha) * (60.0 - chesta)), 3)
    return ishta, kashta


# ─── Main computation ─────────────────────────────────────────────────────────


def compute_shadbala(
    planet: str,
    chart,
    birth_dt: Optional[datetime] = None,
) -> ShadbalResult:
    """
    Compute full Shadbala for a planet.
    birth_dt needed for Kala Bala sub-components (Vara, Hora, etc.).
    """
    result = ShadbalResult(planet=planet)

    if planet not in chart.planets:
        return result

    # Uchcha Bala
    from src.calculations.dignity import get_uchcha_bala  # noqa: F401

    result.uchcha_bala = get_uchcha_bala(planet, chart.planets[planet].longitude)

    # Saptavargaja Bala
    result.saptavargaja_bala = compute_saptavargaja_bala(planet, chart)

    # Ojha-Yugma Bala
    result.ojha_yugma_bala = compute_ojha_yugma_bala(planet, chart)

    # Kendradi Bala
    result.kendradi_bala = compute_kendradi_bala(planet, chart)

    # Drekkana Bala (simplified: male in 1st drekkana 0°-10°, female in 3rd 20°-30°)
    deg = chart.planets[planet].degree_in_sign
    if planet in MALE_PLANETS and deg < 10.0:
        result.drekkana_bala = 15.0
    elif planet in FEMALE_PLANETS and deg >= 20.0:
        result.drekkana_bala = 15.0
    else:
        result.drekkana_bala = 0.0

    result.sthana_bala = (
        result.uchcha_bala
        + result.saptavargaja_bala
        + result.ojha_yugma_bala
        + result.kendradi_bala
        + result.drekkana_bala
    )

    # Dig Bala
    result.dig_bala = compute_dig_bala(planet, chart)

    # Kala Bala (all 8 sub-components)
    kala_total, kala_components = compute_kala_bala(planet, chart, birth_dt)
    result.nathonnata_bala = kala_components.get("nathonnata", 0.0)
    result.paksha_bala = kala_components.get("paksha", 0.0)
    result.tribhaga_bala = kala_components.get("tribhaga", 0.0)
    result.vara_bala = kala_components.get("vara", 0.0)
    result.hora_bala = kala_components.get("hora", 0.0)
    result.masa_bala = kala_components.get("masa", 0.0)
    result.abda_bala = kala_components.get("abda", 0.0)
    result.ayana_bala = kala_components.get("ayana", 0.0)
    result.kala_bala = kala_total

    # Chesta Bala
    result.chesta_bala = compute_chesta_bala(planet, chart)

    # Naisargika Bala
    result.naisargika_bala = NAISARGIKA_BALA.get(planet, 0.0)

    # Drik Bala
    result.drik_bala = compute_drik_bala(planet, chart)

    # Total
    result.total = round(
        result.sthana_bala
        + result.dig_bala
        + result.kala_bala
        + result.chesta_bala
        + result.naisargika_bala
        + result.drik_bala,
        3,
    )

    # Ishta / Kashta
    result.ishta_bala, result.kashta_bala = compute_ishta_kashta(
        result.uchcha_bala, result.chesta_bala
    )

    return result


def compute_all_shadbala(
    chart,
    birth_dt: Optional[datetime] = None,
) -> dict[str, ShadbalResult]:
    """Compute Shadbala for all 7 classical planets."""
    return {
        planet: compute_shadbala(planet, chart, birth_dt)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    }


# ── Backward-compatibility: old API positional args ──


# ── Backward-compatibility wrapper ──
class _ShadbalWrapper:
    """Wraps dict[str, ShadbalResult] to expose .planets and old field names."""

    def __init__(self, d: dict):
        self._d = d
        self.planets = {k: _ShadbalFieldProxy(v) for k, v in d.items()}

    def __getitem__(self, k):
        return self.planets[k]

    def items(self):
        return self.planets.items()

    def keys(self):
        return self.planets.keys()


class _ShadbalFieldProxy:
    """Exposes short field names (.naisargika, .chesta) from ShadbalResult."""

    def __init__(self, r: "ShadbalResult"):
        self._r = r

    def __getattr__(self, name):
        # Map short names to full names
        _map = {
            "naisargika": "naisargika_bala",
            "chesta": "chesta_bala",
            "uchcha": "uchcha_bala",
            "dig": "dig_bala",
            "kala": "kala_bala",
            "drik": "drik_bala",
            "sthana": "sthana_bala",
            "ishta": "ishta_bala",
            "kashta": "kashta_bala",
            "total": "total",
        }
        full = _map.get(name, name)
        return getattr(self._r, full)


def compute_shadbala_legacy(
    planet_or_chart=None,
    sign_idx: int = 0,
    degree: float = 0.0,
    chart=None,
    birth_dt=None,
    planet: str = None,
):
    """Old API shim. Handles compute_shadbala(chart) and compute_shadbala(planet, chart)."""
    if planet_or_chart is not None and hasattr(planet_or_chart, "planets"):
        return _ShadbalWrapper(compute_all_shadbala(planet_or_chart, birth_dt))
    _planet = planet_or_chart if isinstance(planet_or_chart, str) else planet
    if chart is not None and hasattr(chart, "planets"):
        return compute_shadbala(_planet, chart, birth_dt)

    # positional legacy: compute_shadbala(planet, sign_idx, degree)
    class _P:
        def __init__(self):
            self.sign_index = sign_idx
            self.degree_in_sign = degree
            self.longitude = sign_idx * 30.0 + degree
            self.is_retrograde = False
            self.speed = 1.0
            self.latitude = 0.0

    class _C:
        def __init__(self):
            self.lagna = 0.0
            self.lagna_sign_index = 0
            self.planets = {_planet: _P()}
            sun = _P()
            sun.sign_index = 0
            sun.longitude = 0.0
            self.planets["Sun"] = sun

    return compute_shadbala(_planet, _C(), birth_dt)


# S170: Drekkana variant declaration (Sanjay Rath Varga Chakra Ch.3)
# Options: parasara | jagannatha | somanatha
ACTIVE_DREKKANA_METHOD = "parasara"  # default Parashari
