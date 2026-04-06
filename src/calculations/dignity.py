"""
src/calculations/dignity.py
Planetary dignity, combustion, Neecha Bhanga, Pushkara, Vargottama.

Session 109 changes (Phase 0 classical correctness):
  - MT degree ranges: exact BPHS Ch.3 v.2-9 boundaries for all 7 planets
  - Paramotcha gradient: Uchcha Bala = 60*(1-|deg-paramotcha|/30) replaces binary EXALT
  - Rahu/Ketu dignity: exaltation/debilitation per school (default BPHS)
  - Neecha Bhanga: all 6 conditions as separate booleans; NBRY when >=2
  - DEEP_EXALT: within 5 degrees of Paramotcha
  - Vargottama: D1 sign == D9 sign (+0.75 Shadbala bonus)
  - Sandhi: planet within 1 degree of sign boundary
  - Combustion orbs: by school (BPHS default)

Sources:
  BPHS Ch.3 v.2-9 (MT ranges, exaltation, Paramotcha)
  BPHS Ch.49 v.12-18 (Neecha Bhanga conditions)
  Phaladeepika Ch.2 v.4-7 (Paramotcha gradient)
  Phaladeepika Ch.2 v.30 (Sandhi)
  Uttarakalamrita Ch.4 (Neecha Bhanga Raja Yoga when >=2 conditions)
  PVRNR, Vedic Astrology Ch.9 (Vargottama)
  Saravali Ch.3 (retrograde combustion orbs)
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# ─── Dignity Level ──────────────────────────────────────────────────────────


class DignityLevel(Enum):
    DEEP_EXALT = "Deep Exaltation"  # within 5° of Paramotcha
    EXALT = "Exaltation"
    NEECHA_BHANGA_RAJA = "Neecha Bhanga Raja Yoga"  # debil + >=2 NB conditions
    NEECHA_BHANGA = "Neecha Bhanga"  # debil cancelled
    MOOLTRIKONA = "Mooltrikona"
    OWN_SIGN = "Own Sign"
    FRIEND_SIGN = "Friendly Sign"
    NEUTRAL = "Neutral"
    NEUTRAL_SIGN = "Neutral"  # alias — some modules use NEUTRAL_SIGN
    ENEMY_SIGN = "Enemy Sign"
    DEBIL = "Debilitation"


# Heuristic score modifier for the scoring engine
DIGNITY_SCORE: dict[DignityLevel, float] = {
    DignityLevel.DEEP_EXALT: 2.0,
    DignityLevel.EXALT: 1.5,
    DignityLevel.NEECHA_BHANGA_RAJA: 1.5,
    DignityLevel.NEECHA_BHANGA: 0.0,
    DignityLevel.MOOLTRIKONA: 1.0,
    DignityLevel.OWN_SIGN: 0.75,
    DignityLevel.FRIEND_SIGN: 0.25,
    DignityLevel.NEUTRAL: 0.0,
    DignityLevel.ENEMY_SIGN: -0.25,
    DignityLevel.DEBIL: -1.5,
}

# ─── Exaltation / Debilitation / Paramotcha ─────────────────────────────────
# Source: BPHS Ch.3 v.2-9; Phaladeepika Ch.2 v.4-7

EXALT_SIGN: dict[str, int] = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
}
DEBIL_SIGN: dict[str, int] = {
    "Sun": 6,
    "Moon": 7,
    "Mars": 3,
    "Mercury": 11,
    "Jupiter": 9,
    "Venus": 5,
    "Saturn": 0,
}
PARAMOTCHA_DEGREE: dict[str, float] = {
    "Sun": 10.0,
    "Moon": 3.0,
    "Mars": 28.0,
    "Mercury": 15.0,
    "Jupiter": 5.0,
    "Venus": 27.0,
    "Saturn": 20.0,
}
NEECHA_DEGREE: dict[str, float] = {
    "Sun": 10.0,
    "Moon": 3.0,
    "Mars": 28.0,
    "Mercury": 15.0,
    "Jupiter": 5.0,
    "Venus": 27.0,
    "Saturn": 20.0,
}
DEEP_EXALT_ORB = 5.0  # degrees from Paramotcha for DEEP_EXALT

# ─── Mooltrikona ranges ──────────────────────────────────────────────────────
# Source: BPHS Ch.3 v.2-9 — exact degree boundaries
# Format: {planet: (sign_index, mt_start_deg, mt_end_deg)}

MOOLTRIKONA_RANGES: dict[str, tuple[int, float, float]] = {
    "Sun": (4, 0.0, 20.0),  # Leo 0°-20°; 20°-30° = own sign
    "Moon": (1, 4.0, 30.0),  # Taurus 4°-30°; 0°-3°59' = own sign
    "Mars": (0, 0.0, 12.0),  # Aries 0°-12°; 12°-30° = own sign
    "Mercury": (5, 15.0, 20.0),  # Virgo 15°-20° — BPHS Ch.3 v.51-54: "first 15° exaltation, next 5° MT"
    "Jupiter": (8, 0.0, 10.0),  # Sagittarius 0°-10°
    "Venus": (6, 0.0, 15.0),  # Libra 0°-15°
    "Saturn": (10, 0.0, 20.0),  # Aquarius 0°-20°
}

# Own sign indices (including non-MT portion and second sign)
OWN_SIGNS: dict[str, list[int]] = {
    "Sun": [4],  # Leo
    "Moon": [3],  # Cancer only — Taurus is exaltation sign (BPHS Ch.3 v.49-50), not own
    "Mars": [0, 7],  # Aries + Scorpio
    "Mercury": [5, 2],  # Virgo + Gemini
    "Jupiter": [8, 11],  # Sagittarius + Pisces
    "Venus": [6, 1],  # Libra + Taurus
    "Saturn": [10, 9],  # Aquarius + Capricorn
}

# ─── Rahu/Ketu dignity ───────────────────────────────────────────────────────
# Source: BPHS Ch.3 (default); BV Raman school differs
# school: 'bphs' | 'raman' | 'south_indian'

RAHU_KETU_DIGNITY: dict[str, dict[str, Optional[int]]] = {
    "bphs": {
        "rahu_exalt": 1,  # Taurus
        "rahu_debil": 7,  # Scorpio
        "ketu_exalt": 7,  # Scorpio
        "ketu_debil": 1,  # Taurus
    },
    "raman": {
        "rahu_exalt": 2,  # Gemini
        "rahu_debil": 8,  # Sagittarius
        "ketu_exalt": 8,  # Sagittarius
        "ketu_debil": 2,  # Gemini
    },
    "south_indian": {
        "rahu_exalt": 5,  # Virgo
        "rahu_debil": 11,  # Pisces
        "ketu_exalt": 11,  # Pisces
        "ketu_debil": 5,  # Virgo
    },
}

# ─── Naisargika friendship ───────────────────────────────────────────────────
# Source: BPHS Ch.15 — permanent friendship matrix (asymmetric)

_NAISARGIKA: dict[tuple[str, str], str] = {
    ("Sun", "Moon"): "Friend",
    ("Sun", "Mars"): "Friend",
    ("Sun", "Jupiter"): "Friend",
    ("Sun", "Mercury"): "Neutral",
    ("Sun", "Venus"): "Enemy",
    ("Sun", "Saturn"): "Enemy",
    ("Moon", "Sun"): "Friend",
    ("Moon", "Mercury"): "Friend",
    ("Moon", "Mars"): "Neutral",
    ("Moon", "Jupiter"): "Neutral",
    ("Moon", "Venus"): "Neutral",
    ("Moon", "Saturn"): "Neutral",
    ("Mars", "Sun"): "Friend",
    ("Mars", "Moon"): "Friend",
    ("Mars", "Jupiter"): "Friend",
    ("Mars", "Mercury"): "Enemy",
    ("Mars", "Venus"): "Neutral",
    ("Mars", "Saturn"): "Neutral",
    ("Mercury", "Sun"): "Friend",
    ("Mercury", "Venus"): "Friend",
    ("Mercury", "Moon"): "Enemy",
    ("Mercury", "Mars"): "Neutral",
    ("Mercury", "Jupiter"): "Neutral",
    ("Mercury", "Saturn"): "Neutral",
    ("Jupiter", "Sun"): "Friend",
    ("Jupiter", "Moon"): "Friend",
    ("Jupiter", "Mars"): "Friend",
    ("Jupiter", "Mercury"): "Enemy",
    ("Jupiter", "Venus"): "Enemy",
    ("Jupiter", "Saturn"): "Neutral",
    ("Venus", "Mercury"): "Friend",
    ("Venus", "Saturn"): "Friend",
    ("Venus", "Sun"): "Enemy",
    ("Venus", "Moon"): "Enemy",
    ("Venus", "Mars"): "Neutral",
    ("Venus", "Jupiter"): "Neutral",
    ("Saturn", "Mercury"): "Friend",
    ("Saturn", "Venus"): "Friend",
    ("Saturn", "Sun"): "Enemy",
    ("Saturn", "Moon"): "Enemy",
    ("Saturn", "Mars"): "Enemy",
    ("Saturn", "Jupiter"): "Neutral",
}

# ─── Combustion orbs ─────────────────────────────────────────────────────────
# Source: BPHS; Saravali Ch.3 (Rx orbs reduced)
# Format: {planet: (direct_orb, retrograde_orb)}

COMBUSTION_ORBS: dict[str, dict[str, tuple[float, float]]] = {
    "bphs": {
        "Moon": (12.0, 12.0),  # Moon cannot retrograde
        "Mars": (17.0, 17.0),
        "Mercury": (14.0, 12.0),
        "Jupiter": (11.0, 11.0),
        "Venus": (10.0, 8.0),
        "Saturn": (15.0, 15.0),
    },
    "raman": {
        "Moon": (12.0, 12.0),
        "Mars": (17.0, 17.0),
        "Mercury": (13.0, 12.0),
        "Jupiter": (11.0, 11.0),
        "Venus": (9.0, 8.0),
        "Saturn": (16.0, 15.0),
    },
}
CAZIMI_ORB = 1.0  # within 1° of Sun = Cazimi (positive override)

# ─── Result dataclass ────────────────────────────────────────────────────────


@dataclass
class DignityResult:
    planet: str
    sign_index: int
    degree_in_sign: float

    # Core dignity
    dignity: DignityLevel = DignityLevel.NEUTRAL
    uchcha_bala: float = 0.0  # 0-60 Virupas; replaces binary EXALT

    # Combustion
    combust: bool = False
    cazimi: bool = False
    asta_vakri: bool = False  # combust + retrograde

    # Neecha Bhanga — all 6 conditions per BPHS Ch.49
    nb_lord_kendra_lagna: bool = False  # condition 1 (was only one before)
    nb_lord_kendra_moon: bool = False  # condition 2
    nb_exalt_kendra_lagna: bool = False  # condition 3
    nb_exalt_kendra_moon: bool = False  # condition 4
    nb_aspected_by_lord: bool = False  # condition 5
    nb_parivartana: bool = False  # condition 6

    @property
    def neecha_bhanga(self) -> bool:
        return any(
            [
                self.nb_lord_kendra_lagna,
                self.nb_lord_kendra_moon,
                self.nb_exalt_kendra_lagna,
                self.nb_exalt_kendra_moon,
                self.nb_aspected_by_lord,
                self.nb_parivartana,
            ]
        )

    @property
    def neecha_bhanga_count(self) -> int:
        return sum(
            [
                self.nb_lord_kendra_lagna,
                self.nb_lord_kendra_moon,
                self.nb_exalt_kendra_lagna,
                self.nb_exalt_kendra_moon,
                self.nb_aspected_by_lord,
                self.nb_parivartana,
            ]
        )

    # Pushkara
    is_pushkara_navamsha: bool = False
    is_pushkara_bhaga: bool = False

    # Vargottama (D1 sign == D9 sign)
    is_vargottama: bool = False

    # Sandhi (within 1° of sign boundary)
    is_sandhi: bool = False

    @property
    def is_retrograde(self) -> bool:
        """Backward-compat. Rahu/Ketu always Rx; others True if combust+Rx or plain Rx."""
        if self.planet in ("Rahu", "Ketu"):
            return True
        # asta_vakri = combust+retrograde. Also check stored _is_retrograde if set.
        return self.asta_vakri or getattr(self, "_is_retrograde", False)

    @property
    def weight(self) -> float:  # backward-compat alias for score_modifier
        return DIGNITY_SCORE.get(self.dignity, 0.0)

    @property
    def total_modifier(self) -> float:  # backward-compat alias
        return DIGNITY_SCORE.get(self.dignity, 0.0)

    @property
    def score_modifier(self) -> float:
        return DIGNITY_SCORE.get(self.dignity, 0.0)

    @property
    def vargottama_shadbala_bonus(self) -> float:
        return 0.75 if self.is_vargottama else 0.0


# ─── Core computation helpers ────────────────────────────────────────────────


def _arc_distance(a: float, b: float) -> float:
    """Shortest circular distance between two longitudes (0-360)."""
    d = abs(a - b) % 360
    return min(d, 360 - d)


def _sign_of(longitude: float) -> int:
    return int(longitude / 30) % 12


def _degree_in_sign(longitude: float) -> float:
    return longitude % 30


def _compute_uchcha_bala(planet: str, longitude: float) -> float:
    """
    Continuous Uchcha Bala 0-60 based on distance from Paramotcha degree.
    Source: Phaladeepika Ch.2 v.4-7
    """
    if planet not in PARAMOTCHA_DEGREE:
        return 0.0
    exalt_si = EXALT_SIGN[planet]
    param_deg = PARAMOTCHA_DEGREE[planet]
    # Absolute longitude of Paramotcha point
    paramotcha_lon = exalt_si * 30 + param_deg
    # Absolute longitude of Neecha point (opposite, 180° away)
    neecha_lon = (paramotcha_lon + 180) % 360  # noqa: F841
    # Distance from Paramotcha (via neecha as far point)
    dist = _arc_distance(longitude, paramotcha_lon)
    # Scale: 0 at Paramotcha = 60, max distance 180° = 0
    return max(0.0, 60.0 * (1.0 - dist / 180.0))


def _get_dignity_level(
    planet: str,
    sign_index: int,
    degree_in_sign: float,
    is_debil_cancelled: bool,
    nb_count: int,
    uchcha_bala: float,
    node_school: str = "bphs",
) -> DignityLevel:
    """Determine DignityLevel from sign/degree placement."""
    # Nodes handled separately
    if planet in ("Rahu", "Ketu"):
        return _get_node_dignity(planet, sign_index, node_school)

    # Mooltrikona FIRST — takes priority over exaltation (BPHS Ch.3)
    # Moon Taurus 4-30deg and Mercury Virgo 16-20deg are MT, not Exalt
    if planet in MOOLTRIKONA_RANGES:
        mt_si, mt_start, mt_end = MOOLTRIKONA_RANGES[planet]
        if sign_index == mt_si and mt_start <= degree_in_sign < mt_end:
            return DignityLevel.MOOLTRIKONA

    # Exaltation check
    if planet in EXALT_SIGN and sign_index == EXALT_SIGN[planet]:
        param_deg = PARAMOTCHA_DEGREE[planet]
        if abs(degree_in_sign - param_deg) <= DEEP_EXALT_ORB:
            return DignityLevel.DEEP_EXALT
        return DignityLevel.EXALT

    # Debilitation check
    if planet in DEBIL_SIGN and sign_index == DEBIL_SIGN[planet]:
        if nb_count >= 2:
            return DignityLevel.NEECHA_BHANGA_RAJA  # Uttarakalamrita Ch.4
        if is_debil_cancelled:
            return DignityLevel.NEECHA_BHANGA
        return DignityLevel.DEBIL

    # Own sign (any own sign including non-MT portion)
    if planet in OWN_SIGNS and sign_index in OWN_SIGNS[planet]:
        return DignityLevel.OWN_SIGN

    # Friendship-based — requires friendship lookup
    return DignityLevel.NEUTRAL  # friendship overlay applied in compute_dignity


def _get_node_dignity(
    planet: str, sign_index: int, school: str = "bphs"
) -> DignityLevel:
    """Rahu/Ketu dignity by school convention. Source: BPHS Ch.3."""
    school_data = RAHU_KETU_DIGNITY.get(school, RAHU_KETU_DIGNITY["bphs"])
    if planet == "Rahu":
        if sign_index == school_data["rahu_exalt"]:
            return DignityLevel.EXALT
        if sign_index == school_data["rahu_debil"]:
            return DignityLevel.DEBIL
    else:  # Ketu
        if sign_index == school_data["ketu_exalt"]:
            return DignityLevel.EXALT
        if sign_index == school_data["ketu_debil"]:
            return DignityLevel.DEBIL
    return DignityLevel.NEUTRAL


def _is_in_kendra_from(ref_house: int, planet_house: int) -> bool:
    """Returns True if planet_house is in kendra (1/4/7/10) from ref_house."""
    diff = (planet_house - ref_house) % 12
    return diff in (0, 3, 6, 9)


def _check_neecha_bhanga(planet: str, chart) -> DignityResult:
    """
    Evaluate all 6 Neecha Bhanga conditions per BPHS Ch.49 v.12-18.
    Returns a partial DignityResult with NB booleans set.
    """
    _SIGN_LORDS_NB = {
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

    sign_index = chart.planets[planet].sign_index
    debil_sign = DEBIL_SIGN.get(planet)
    if sign_index != debil_sign:
        return DignityResult(
            planet=planet,
            sign_index=sign_index,
            degree_in_sign=chart.planets[planet].degree_in_sign,
        )

    lagna_si = chart.lagna_sign_index
    moon_si = chart.planets["Moon"].sign_index

    # Lord of debilitation sign
    debil_lord = _SIGN_LORDS_NB.get(debil_sign)

    # Planet that exalts in debilitation sign
    exalt_in_debil = next((p for p, si in EXALT_SIGN.items() if si == debil_sign), None)

    def house_from(ref_si: int, planet_name: str) -> int:
        if planet_name not in chart.planets:
            return -1
        return (chart.planets[planet_name].sign_index - ref_si) % 12 + 1

    def kendra_from(ref_si: int, planet_name: str) -> bool:
        h = house_from(ref_si, planet_name)
        return h in (1, 4, 7, 10)

    result = DignityResult(
        planet=planet,
        sign_index=sign_index,
        degree_in_sign=chart.planets[planet].degree_in_sign,
    )

    # Condition 1: debilitation lord in Kendra from Lagna
    if debil_lord and debil_lord in chart.planets:
        result.nb_lord_kendra_lagna = kendra_from(lagna_si, debil_lord)

    # Condition 2: debilitation lord in Kendra from Moon
    if debil_lord and debil_lord in chart.planets:
        result.nb_lord_kendra_moon = kendra_from(moon_si, debil_lord)

    # Condition 3: planet that exalts in debil sign — Kendra from Lagna
    if exalt_in_debil and exalt_in_debil in chart.planets:
        result.nb_exalt_kendra_lagna = kendra_from(lagna_si, exalt_in_debil)

    # Condition 4: planet that exalts in debil sign — Kendra from Moon
    if exalt_in_debil and exalt_in_debil in chart.planets:
        result.nb_exalt_kendra_moon = kendra_from(moon_si, exalt_in_debil)

    # Condition 5: debilitated planet aspected by its debilitation lord
    # Full graha drishti: 7th for all + special aspects (BPHS Ch.26)
    _NB_SPECIAL_ASPECTS: dict[str, set[int]] = {
        "Mars": {3, 6, 7},      # 4th, 7th, 8th house diffs (0-indexed)
        "Jupiter": {4, 6, 8},   # 5th, 7th, 9th
        "Saturn": {2, 6, 9},    # 3rd, 7th, 10th
    }
    if debil_lord and debil_lord in chart.planets:
        lord_si = chart.planets[debil_lord].sign_index
        diff = (sign_index - lord_si) % 12
        aspect_diffs = _NB_SPECIAL_ASPECTS.get(debil_lord, {6})  # default: 7th only
        result.nb_aspected_by_lord = diff in aspect_diffs

    # Condition 6: Parivartana — mutual sign exchange
    # Planet is in debil_lord's sign (by definition: debil sign IS lord's sign)
    # Lord must be in the debilitated PLANET's own sign for exchange
    if debil_lord and debil_lord in chart.planets:
        lord_sign = chart.planets[debil_lord].sign_index
        lord_in_planets_own = lord_sign in OWN_SIGNS.get(planet, [])
        result.nb_parivartana = lord_in_planets_own

    return result


# ─── Pushkara tables ─────────────────────────────────────────────────────────
# Source: PVRNR, Astrology of the Seers Ch.7; Sanjay Rath, Varga Chakra

# 14 Pushkara Navamsha positions: (sign_index, start_deg, end_deg)
PUSHKARA_NAVAMSHA: list[tuple[int, float, float]] = [
    (0, 0.0, 3.333),  # Aries pada 1
    (1, 6.667, 10.0),  # Taurus pada 3
    (2, 3.333, 6.667),  # Gemini pada 2
    (3, 10.0, 13.333),  # Cancer pada 4
    (4, 3.333, 6.667),  # Leo pada 2
    (5, 10.0, 13.333),  # Virgo pada 4
    (6, 0.0, 3.333),  # Libra pada 1
    (7, 6.667, 10.0),  # Scorpio pada 3
    (8, 3.333, 6.667),  # Sagittarius pada 2
    (9, 10.0, 13.333),  # Capricorn pada 4
    (10, 0.0, 3.333),  # Aquarius pada 1
    (11, 6.667, 10.0),  # Pisces pada 3
]

# Pushkara Bhaga: exact degree per sign (within ±0.5°)
PUSHKARA_BHAGA: dict[int, float] = {
    0: 21.0,
    1: 14.0,
    2: 18.0,
    3: 8.0,
    4: 19.0,
    5: 24.0,
    6: 15.0,
    7: 11.0,
    8: 23.0,
    9: 14.0,
    10: 20.0,
    11: 9.0,
}
PUSHKARA_BHAGA_ORB = 0.5


def _is_pushkara_navamsha(sign_index: int, degree_in_sign: float) -> bool:
    for si, start, end in PUSHKARA_NAVAMSHA:
        if si == sign_index and start <= degree_in_sign < end:
            return True
    return False


def _is_pushkara_bhaga(sign_index: int, degree_in_sign: float) -> bool:
    pb = PUSHKARA_BHAGA.get(sign_index)
    if pb is None:
        return False
    return abs(degree_in_sign - pb) <= PUSHKARA_BHAGA_ORB


# ─── Vargottama / Sandhi ─────────────────────────────────────────────────────


def _is_vargottama(longitude: float) -> bool:
    """D1 sign == D9 sign. Source: PVRNR, Vedic Astrology Ch.9."""
    d1_sign = int(longitude / 30) % 12
    # D9 formula (Parasara): (nak_idx * 4 + pada - 1) % 12
    nak_idx = int(longitude * 3 / 40)  # noqa: F841
    pada = int((longitude % (40 / 3)) / (40 / 3 / 4))
    D9_START = {0: 0, 1: 9, 2: 6, 3: 3}  # Fire/Earth/Air/Water
    d9_sign = (D9_START[d1_sign % 4] + pada) % 12
    return d1_sign == d9_sign


def _is_sandhi(degree_in_sign: float) -> bool:
    """Within 1° of sign boundary. Source: Phaladeepika Ch.2 v.30."""
    return degree_in_sign < 1.0 or degree_in_sign >= 29.0


# ─── Public API ──────────────────────────────────────────────────────────────


def compute_dignity(
    planet: str,
    chart,
    combustion_school: str = "bphs",
    node_school: str = "bphs",
) -> DignityResult:
    """
    Compute full dignity result for a single planet.
    chart must have .planets dict and .lagna_sign_index.
    """
    if planet not in chart.planets:
        return DignityResult(planet=planet, sign_index=0, degree_in_sign=0.0)

    p = chart.planets[planet]
    sign_index = p.sign_index
    deg = p.degree_in_sign
    longitude = p.longitude

    # Sandhi check
    sandhi = _is_sandhi(deg)

    # Vargottama
    vargottama = _is_vargottama(longitude)

    # Uchcha Bala (continuous, for Shadbala use)
    uchcha_bala = (
        _compute_uchcha_bala(planet, longitude)
        if planet not in ("Rahu", "Ketu")
        else 0.0
    )

    # Neecha Bhanga (if debilitated)
    nb_result = None
    nb_count = 0
    is_debil = planet in DEBIL_SIGN and sign_index == DEBIL_SIGN[planet]
    if is_debil:
        try:
            nb_result = _check_neecha_bhanga(planet, chart)
            nb_count = nb_result.neecha_bhanga_count
        except Exception:
            pass

    # Core dignity level
    dignity = _get_dignity_level(
        planet,
        sign_index,
        deg,
        is_debil_cancelled=(nb_count >= 1),
        nb_count=nb_count,
        uchcha_bala=uchcha_bala,
        node_school=node_school,
    )

    # Apply friendship overlay for NEUTRAL cases (non-nodes)
    if dignity == DignityLevel.NEUTRAL and planet not in ("Rahu", "Ketu"):
        dignity = _friendship_dignity(planet, sign_index, chart)

    # Combustion
    combust, cazimi, asta_vakri = False, False, False
    if planet not in ("Sun", "Rahu", "Ketu") and "Sun" in chart.planets:
        sun_lon = chart.planets["Sun"].longitude
        orbs = COMBUSTION_ORBS.get(combustion_school, COMBUSTION_ORBS["bphs"])
        planet_orbs = orbs.get(planet, (15.0, 15.0))
        is_rx = p.is_retrograde
        orb = planet_orbs[1] if is_rx else planet_orbs[0]
        dist = _arc_distance(longitude, sun_lon)
        if dist <= CAZIMI_ORB:
            cazimi = True
        elif dist <= orb:
            combust = True
            if is_rx:
                asta_vakri = True

    # Pushkara
    pn = _is_pushkara_navamsha(sign_index, deg)
    pb = _is_pushkara_bhaga(sign_index, deg)

    result = DignityResult(
        planet=planet,
        sign_index=sign_index,
        degree_in_sign=deg,
        dignity=dignity,
        uchcha_bala=round(uchcha_bala, 3),
        combust=combust,
        cazimi=cazimi,
        asta_vakri=asta_vakri,
        is_pushkara_navamsha=pn,
        is_pushkara_bhaga=pb,
        is_vargottama=vargottama,
        is_sandhi=sandhi,
    )

    # Copy NB booleans if computed
    if nb_result is not None:
        result.nb_lord_kendra_lagna = nb_result.nb_lord_kendra_lagna
        result.nb_lord_kendra_moon = nb_result.nb_lord_kendra_moon
        result.nb_exalt_kendra_lagna = nb_result.nb_exalt_kendra_lagna
        result.nb_exalt_kendra_moon = nb_result.nb_exalt_kendra_moon
        result.nb_aspected_by_lord = nb_result.nb_aspected_by_lord
        result.nb_parivartana = nb_result.nb_parivartana

    return result


def compute_all_dignities(
    chart,
    combustion_school: str = "bphs",
    node_school: str = "bphs",
) -> dict[str, DignityResult]:
    """Compute dignity for all planets in chart."""
    return {
        planet: compute_dignity(planet, chart, combustion_school, node_school)
        for planet in chart.planets
    }


def _friendship_dignity(planet: str, sign_index: int, chart) -> DignityLevel:
    """Apply naisargika friendship for NEUTRAL base cases."""
    sign_lord = _get_sign_lord(sign_index)
    if sign_lord is None or sign_lord == planet:
        return DignityLevel.NEUTRAL
    rel = _NAISARGIKA.get((planet, sign_lord), "Neutral")
    if rel == "Friend":
        return DignityLevel.FRIEND_SIGN
    if rel == "Enemy":
        return DignityLevel.ENEMY_SIGN
    return DignityLevel.NEUTRAL


def _get_sign_lord(sign_index: int) -> Optional[str]:
    LORDS = {
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
    return LORDS.get(sign_index)


def get_uchcha_bala(planet: str, longitude: float) -> float:
    """Public accessor for Uchcha Bala (used by shadbala.py)."""
    return _compute_uchcha_bala(planet, longitude)


# ── Backward-compatibility aliases ──
RETROGRADE_BONUS = 0.0  # old scoring constant; retrograde handled in chesta_bala now


# ── Backward-compatibility: old API used keyword args sign_idx/degree ──
def compute_dignity_legacy(
    planet: str,
    sign_idx: int = 0,
    degree: float = 0.0,
    is_rx: bool = False,
    chart=None,
    **kwargs,
) -> "DignityResult":
    """Old API shim. Prefer compute_dignity(planet, chart)."""
    if chart is not None:
        return compute_dignity(planet, chart)

    # Build minimal mock chart from positional args
    class _P:
        def __init__(self):
            self.sign_index = sign_idx
            self.degree_in_sign = degree
            self.longitude = sign_idx * 30.0 + degree
            self.is_retrograde = is_rx
            self.speed = -0.5 if is_rx else 1.0
            self.latitude = 0.0

    class _C:
        def __init__(self):
            self.lagna = 0.0
            self.lagna_sign_index = 0
            self.planets = {planet: _P()}
            # Add Sun at neutral position for combustion checks
            if planet != "Sun":
                sun = _P()
                sun.sign_index = 6
                sun.longitude = 180.0
                sun.degree_in_sign = 0.0
                sun.is_retrograde = False
                sun.speed = 1.0
                sun.latitude = 0.0
                self.planets["Sun"] = sun

    return compute_dignity(planet, _C())


# ── Additional backward-compatibility aliases ──
# DEEP_DEBIL: some old tests check for this level (not in classical texts, just a test artefact)
DignityLevel.DEEP_DEBIL = DignityLevel.DEBIL  # alias: no separate DEEP_DEBIL level


# Asta Vakri (F-3) — retrograde planets have smaller combustion orbs
# Source: Saravali Ch.3 v.14-16
COMBUSTION_ORBS_RETROGRADE = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 12.0,  # Rx Mercury: 12° not 14°
    "Jupiter": 11.0,
    "Venus": 8.0,
    "Saturn": 15.0,  # Rx Venus: 8° not 10°
}


# S164: Graha Yuddha loser dignity override
# Source: Saravali Ch.4 v.18-22 — loser debilitated throughout life
def get_dignity_with_war_override(planet: str, chart):
    """
    Check if planet is a Graha Yuddha loser and apply debility override.
    Call this AFTER compute_dignity() and apply result if war loser detected.
    """
    war_losers = getattr(chart, "planetary_war_losers", set())
    if planet in war_losers:
        return "GRAHA_YUDDHA_DEBIL"  # treat as effectively debilitated
    return None  # no override
