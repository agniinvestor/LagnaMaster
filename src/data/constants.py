"""src/data/constants.py — Canonical astrological constants.

GOLDEN SOURCE: Every astrological constant in LagnaMaster is defined here
and ONLY here. All other modules import from this file.

Each constant cites its BPHS source. If a constant comes from a different
text, that text is cited instead. If values differ between texts, BPHS is
authoritative unless noted.

Verified against: R. Santhanam, BPHS Vol 1, Ranjan Publications.
"""

from __future__ import annotations

# ─── A. Planet classifications ───────────────────────────────────────────────
# BPHS Ch.3 v.11 (p.27-28)
# Moon and Mercury are CONDITIONALLY benefic/malefic:
#   Moon: malefic when waning (Krishna Paksha), benefic when waxing
#   Mercury: malefic when conjunct malefics
# For static lookups (no chart context), classify both as benefic.
NATURAL_BENEFICS: frozenset[str] = frozenset({"Jupiter", "Venus", "Mercury", "Moon"})
NATURAL_MALEFICS: frozenset[str] = frozenset({"Sun", "Mars", "Saturn", "Rahu", "Ketu"})

# All 9 grahas in standard order
PLANETS: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
)
SEVEN_PLANETS: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
)

# ─── B. Sign lords ───────────────────────────────────────────────────────────
# BPHS Ch.3 v.49-51 — Planetary Rulership
# sign_index (0=Aries) → ruling planet
SIGN_LORDS: dict[int, str] = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# ─── C. Sign classifications ────────────────────────────────────────────────
# BPHS — even-numbered signs (0-indexed) are feminine/gentle
# Taurus(1), Cancer(3), Virgo(5), Scorpio(7), Capricorn(9), Pisces(11)
GENTLE_SIGNS: frozenset[int] = frozenset({1, 3, 5, 7, 9, 11})
CRUEL_SIGNS: frozenset[int] = frozenset({0, 2, 4, 6, 8, 10})

SIGN_NAMES: tuple[str, ...] = (
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
)

# ─── D. House classifications ───────────────────────────────────────────────
# BPHS Ch.11 — Bhava Characteristics
KENDRA_HOUSES: frozenset[int] = frozenset({1, 4, 7, 10})
TRIKONA_HOUSES: frozenset[int] = frozenset({1, 5, 9})
DUSTHANA_HOUSES: frozenset[int] = frozenset({6, 8, 12})
UPACHAYA_HOUSES: frozenset[int] = frozenset({3, 6, 10, 11})
MARAKA_HOUSES: frozenset[int] = frozenset({2, 7})
PANAPHARA_HOUSES: frozenset[int] = frozenset({2, 5, 8, 11})
APOKLIMA_HOUSES: frozenset[int] = frozenset({3, 6, 9, 12})

# ─── E. Special aspects ─────────────────────────────────────────────────────
# BPHS Ch.26 v.9-12 — Graha Drishti (special planetary aspects)
# Offset from aspecting planet's house position. All planets also have
# 7th aspect (offset=6) which is universal, not listed here.
SPECIAL_ASPECTS: dict[str, frozenset[int]] = {
    "Mars": frozenset({4, 8}),      # 4th and 8th house aspects
    "Jupiter": frozenset({5, 9}),   # 5th and 9th house aspects
    "Saturn": frozenset({3, 10}),   # 3rd and 10th house aspects
}

# ─── F. Dig Bala ────────────────────────────────────────────────────────────
# BPHS Ch.27 — Directional Strength (peak houses)
DIG_BALA_PEAK: dict[str, int] = {
    "Sun": 10, "Moon": 4, "Mars": 10, "Mercury": 1,
    "Jupiter": 1, "Venus": 4, "Saturn": 7,
}

# ─── G. Sthira Karaka ───────────────────────────────────────────────────────
# BPHS Ch.32 v.34 — Naisargika (Fixed) Significators per house
STHIRA_KARAKA: dict[int, tuple[str, ...]] = {
    1: ("Sun",),
    2: ("Jupiter",),
    3: ("Mars",),
    4: ("Moon", "Venus"),       # BUG-052 fix: Venus = vehicles/comforts
    5: ("Jupiter",),
    6: ("Mars", "Saturn"),
    7: ("Venus",),
    8: ("Saturn",),
    9: ("Jupiter", "Sun"),      # BUG-053 fix: Sun = father karaka
    10: ("Sun", "Mercury", "Saturn"),  # BUG-054 fix: removed Jupiter
    11: ("Jupiter",),
    12: ("Saturn",),
}

# ─── H. Exaltation / Debilitation ───────────────────────────────────────────
# BPHS Ch.3 v.49-51 — Exaltation signs (0-indexed)
EXALTATION_SIGN: dict[str, int] = {
    "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
    "Jupiter": 3, "Venus": 11, "Saturn": 6,
}
DEBILITATION_SIGN: dict[str, int] = {
    "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
    "Jupiter": 9, "Venus": 5, "Saturn": 0,
}
# Exaltation degrees — BPHS Ch.3 v.49-51
EXALTATION_DEGREE: dict[str, float] = {
    "Sun": 10.0, "Moon": 3.0, "Mars": 28.0, "Mercury": 15.0,
    "Jupiter": 5.0, "Venus": 27.0, "Saturn": 20.0,
}

# Absolute zodiac longitudes for exaltation/debilitation (= sign*30 + degree)
# Used by Uchcha Bala (ishta_kashta.py) and Pindayu (longevity.py)
EXALTATION_LON: dict[str, int] = {
    "Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165,
    "Jupiter": 95, "Venus": 357, "Saturn": 200,
}
DEBILITATION_LON: dict[str, int] = {
    "Sun": 190, "Moon": 213, "Mars": 118, "Mercury": 345,
    "Jupiter": 275, "Venus": 177, "Saturn": 20,
}

# ─── I. Moolatrikona ranges ─────────────────────────────────────────────────
# Re-exported from dignity.py which has the degree-bounded ranges.
# Format: (sign_index, start_degree, end_degree)
# Imported lazily to avoid circular imports — consumers should use:
#   from src.calculations.dignity import MOOLTRIKONA_RANGES

# ─── J. Nakshatra names ─────────────────────────────────────────────────────
# 27 Nakshatras in order (Ashwini=0 to Revati=26)
NAKSHATRA_NAMES: tuple[str, ...] = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishtha", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
)

# ─── K. Vimshottari Dasha data ──────────────────────────────────────────────
# BPHS Ch.46 — Vimshottari Dasha years and sequence
VIMSHOTTARI_YEARS: dict[str, int] = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Mercury": 17, "Jupiter": 16,
    "Venus": 20, "Saturn": 19, "Rahu": 18, "Ketu": 7,
}  # Total: 120 years

# Dasha sequence (starting from Ketu)
VIMSHOTTARI_SEQUENCE: tuple[str, ...] = (
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
)

# ─── L. Own signs ────────────────────────────────────────────────────────────
# BPHS Ch.3 v.49-51 — each planet's own signs (sign indices)
OWN_SIGNS: dict[str, tuple[int, ...]] = {
    "Sun": (4,), "Moon": (3,), "Mars": (0, 7), "Mercury": (2, 5),
    "Jupiter": (8, 11), "Venus": (1, 6), "Saturn": (9, 10),
}

# ─── M. Combustion orbs ─────────────────────────────────────────────────────
# BPHS Ch.3 (Santhanam notes p.28)
# Degrees from Sun at which a planet becomes combust (direct, retrograde)
# For full multi-school combustion logic, see dignity.py COMBUSTION_ORBS
COMBUSTION_ORBS_BPHS: dict[str, tuple[float, float]] = {
    "Moon": (12.0, 12.0),
    "Mars": (17.0, 17.0),
    "Mercury": (14.0, 12.0),
    "Jupiter": (11.0, 11.0),
    "Venus": (10.0, 8.0),
    "Saturn": (15.0, 15.0),
}

# ─── N. Naisargika Bala ─────────────────────────────────────────────────────
# BPHS Ch.27 — Natural strength (Shashtiamsha units)
NAISARGIKA_BALA: dict[str, float] = {
    "Sun": 60.0, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
    "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57,
}

# ─── O. Weekday and Hora lords ──────────────────────────────────────────────
# Standard weekday sequence (Sunday=0)
WEEKDAY_LORDS: tuple[str, ...] = (
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
)

# Hora sequence (planetary hours)
HORA_SEQUENCE: tuple[str, ...] = (
    "Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon",
)

# ─── P. Zodiac elements and qualities ───────────────────────────────────────
# Fire/Earth/Air/Water by sign index
FIRE_SIGNS: frozenset[int] = frozenset({0, 4, 8})      # Aries, Leo, Sagittarius
EARTH_SIGNS: frozenset[int] = frozenset({1, 5, 9})     # Taurus, Virgo, Capricorn
AIR_SIGNS: frozenset[int] = frozenset({2, 6, 10})      # Gemini, Libra, Aquarius
WATER_SIGNS: frozenset[int] = frozenset({3, 7, 11})    # Cancer, Scorpio, Pisces

# Cardinal/Fixed/Mutable (Chara/Sthira/Dwiswabhava)
CARDINAL_SIGNS: frozenset[int] = frozenset({0, 3, 6, 9})   # Aries, Cancer, Libra, Capricorn
FIXED_SIGNS: frozenset[int] = frozenset({1, 4, 7, 10})     # Taurus, Leo, Scorpio, Aquarius
MUTABLE_SIGNS: frozenset[int] = frozenset({2, 5, 8, 11})   # Gemini, Virgo, Sagittarius, Pisces

# ─── Q. Naisargika friendship ───────────────────────────────────────────────
# Re-exported from panchadha_maitri.py which has the full friendship logic.
# Consumers should use: from src.calculations.panchadha_maitri import ...
