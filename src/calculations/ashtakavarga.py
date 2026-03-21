"""
src/calculations/ashtakavarga.py
Parashari Ashtakavarga — 8-source bindu tables + both Shodhana reductions.

Session 112 changes (Phase 0):
  - Trikona Shodhana: mandatory reduction per PVRNR AV System Ch.4
  - Ekadhipatya Shodhana: dual-lordship reduction per PVRNR AV System Ch.5
  - Sarva: computed from reduced tables (not raw)
  - Raw bindus still exposed as .raw_bindus for reference/debugging

Sources:
  PVRNR, Ashtakavarga System of Prediction Ch.4 (Trikona Shodhana)
  PVRNR, Ashtakavarga System of Prediction Ch.5 (Ekadhipatya Shodhana)
  BV Raman, Ashtakavarga System of Prediction (1966) — worked example
  BPHS Ch.66-68 — base bindu house tables
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_SIGN_NAMES = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

# ─── Dual-ruled sign pairs (for Ekadhipatya Shodhana) ───────────────────────
# {planet: (sign_index_1, sign_index_2)}
_DUAL_RULED: dict[str, tuple[int, int]] = {
    "Mars":    (0, 7),    # Aries, Scorpio
    "Mercury": (2, 5),    # Gemini, Virgo
    "Jupiter": (8, 11),   # Sagittarius, Pisces
    "Venus":   (1, 6),    # Taurus, Libra
    "Saturn":  (9, 10),   # Capricorn, Aquarius
}

# ─── BPHS bindu house tables ─────────────────────────────────────────────────
# _BENEFIC_HOUSES[target_planet][contributor] = list of house offsets that donate a bindu
# House offsets are counted from the contributor's sign position

_BENEFIC_HOUSES: dict[str, dict[str, list[int]]] = {
    "Sun": {
        "Sun":     [1,2,4,7,8,9,10,11],
        "Moon":    [3,6,10,11],
        "Mars":    [1,2,4,7,8,9,10,11],
        "Mercury": [3,5,6,9,10,11,12],
        "Jupiter": [5,6,9,11],
        "Venus":   [6,7,12],
        "Saturn":  [1,2,4,7,8,9,10,11],
        "Lagna":   [3,4,6,10,11,12],
    },
    "Moon": {
        "Sun":     [3,6,7,8,10,11],
        "Moon":    [1,3,6,7,10,11],
        "Mars":    [2,3,5,6,9,10,11],
        "Mercury": [1,3,4,5,7,8,10,11],
        "Jupiter": [1,4,7,8,10,11,12],
        "Venus":   [3,4,5,7,9,10,11],
        "Saturn":  [3,5,6,11],
        "Lagna":   [3,6,10,11],
    },
    "Mars": {
        "Sun":     [3,5,6,10,11],
        "Moon":    [3,6,11],
        "Mars":    [1,2,4,7,8,10,11],
        "Mercury": [3,5,6,11],
        "Jupiter": [6,10,11,12],
        "Venus":   [6,8,11,12],
        "Saturn":  [1,4,7,8,9,10,11],
        "Lagna":   [1,3,6,10,11],
    },
    "Mercury": {
        "Sun":     [5,6,9,11,12],
        "Moon":    [2,4,6,8,10,11],
        "Mars":    [1,2,4,7,8,9,10,11],
        "Mercury": [1,3,5,6,9,10,11,12],
        "Jupiter": [6,8,11,12],
        "Venus":   [1,2,3,4,5,8,9,11],
        "Saturn":  [1,2,4,7,8,9,10,11],
        "Lagna":   [1,2,4,6,8,10,11],
    },
    "Jupiter": {
        "Sun":     [1,2,3,4,7,8,9,10,11],
        "Moon":    [2,5,7,9,11],
        "Mars":    [1,2,4,7,8,10,11],
        "Mercury": [1,2,4,5,6,9,10,11],
        "Jupiter": [1,2,3,4,7,8,10,11],
        "Venus":   [2,5,6,9,10,11],
        "Saturn":  [3,5,6,12],
        "Lagna":   [1,2,4,5,6,7,9,10,11],
    },
    "Venus": {
        "Sun":     [8,11,12],
        "Moon":    [1,2,3,4,5,8,9,11,12],
        "Mars":    [3,4,6,9,11,12],
        "Mercury": [3,5,6,9,11],
        "Jupiter": [5,8,9,10,11],
        "Venus":   [1,2,3,4,5,8,9,10,11],
        "Saturn":  [3,4,5,8,9,10,11],
        "Lagna":   [1,2,3,4,5,8,9,11],
    },
    "Saturn": {
        "Sun":     [1,2,4,7,8,10,11],
        "Moon":    [3,6,11],
        "Mars":    [3,5,6,10,11,12],
        "Mercury": [6,8,9,10,11,12],
        "Jupiter": [5,6,11,12],
        "Venus":   [6,11,12],
        "Saturn":  [3,5,6,11],
        "Lagna":   [1,3,4,6,10,11],
    },
}

# Fixed totals (chart-independent, pre-Shodhana)
FIXED_TOTALS_RAW: dict[str, int] = {
    "Sun": 48, "Moon": 48, "Mars": 42, "Mercury": 54,
    "Jupiter": 56, "Venus": 52, "Saturn": 40,
}


# ─── Result dataclasses ──────────────────────────────────────────────────────

@dataclass
class AshtakavargaTable:
    planet: str
    raw_bindus: list[int]    # pre-Shodhana, index 0=Aries
    bindus: list[int]        # post-Shodhana (use this for interpretation)
    total: int               # sum of reduced bindus

    def bindu_for_sign(self, sign_index: int) -> int:
        return self.bindus[sign_index % 12]

    def bindu_for_sign_name(self, sign_name: str) -> int:
        idx = _SIGN_NAMES.index(sign_name)
        return self.bindus[idx]

    def strength(self, sign_index: int) -> str:
        b = self.raw_bindus[sign_index % 12]
        if b >= 5: return "Strong"
        if b == 4: return "Average"
        return "Weak"


@dataclass
class AshtakavargaChart:
    planet_av: dict[str, AshtakavargaTable]  # 7 planets (post-Shodhana)
    sarva: AshtakavargaTable                  # sum of all 7 reduced, then re-reduced

    def for_planet(self, planet: str) -> AshtakavargaTable:
        return self.planet_av[planet]


# ─── Shodhana reductions ─────────────────────────────────────────────────────

def trikona_shodhana(bindus: list[int]) -> list[int]:
    """
    Trikona Shodhana: for each trine group subtract the minimum.
    Groups: (0,4,8), (1,5,9), (2,6,10), (3,7,11)
    Source: PVRNR, Ashtakavarga System Ch.4
    """
    result = list(bindus)
    for group in [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]:
        m = min(result[i] for i in group)
        for i in group:
            result[i] -= m
    return result


def ekadhipatya_shodhana(bindus: list[int], planet: str, chart) -> list[int]:
    """
    Ekadhipatya Shodhana: reduce dual-ruled sign pairs.
    Source: PVRNR, Ashtakavarga System Ch.5

    Rules:
    - If the planet occupies one of its two signs: apply conditional reduction
      (the occupied sign retains its bindus; the unoccupied sign is reduced by
      the occupied sign's value, floored at 0)
    - If the planet is in a third sign: reduce the lower-bindu sign to zero
      and retain the higher
    """
    if planet not in _DUAL_RULED:
        return bindus  # Sun, Moon, Lagna have no dual sign

    result = list(bindus)
    si1, si2 = _DUAL_RULED[planet]
    planet_sign = chart.planets[planet].sign_index if planet in chart.planets else -1

    if planet_sign in (si1, si2):
        # Planet occupies one of its signs — occupied retains, other reduces
        occupied = planet_sign
        other = si2 if occupied == si1 else si1
        result[other] = max(0, result[other] - result[occupied])
    else:
        # Planet in third sign — reduce lower to zero
        if result[si1] >= result[si2]:
            result[si2] = 0
        else:
            result[si1] = 0

    return result


# ─── Bindu computation ───────────────────────────────────────────────────────

def _compute_raw_bindus(target_planet: str, chart) -> list[int]:
    """Compute raw (pre-Shodhana) bindus for target_planet from all 8 contributors."""
    bindus = [0] * 12
    contributor_positions = {}

    for planet in _PLANETS:
        if planet in chart.planets:
            contributor_positions[planet] = chart.planets[planet].sign_index
    contributor_positions["Lagna"] = chart.lagna_sign_index

    house_table = _BENEFIC_HOUSES.get(target_planet, {})

    for contributor, contrib_sign in contributor_positions.items():
        good_houses = house_table.get(contributor, [])
        for h in good_houses:
            target_sign = (contrib_sign + h - 1) % 12
            bindus[target_sign] += 1

    return bindus


# ─── Main computation ─────────────────────────────────────────────────────────

def compute_ashtakavarga(chart) -> AshtakavargaChart:
    """
    Compute full Ashtakavarga chart with both Shodhana reductions applied.
    Source: BPHS Ch.66-68; PVRNR, Ashtakavarga System Ch.4-5
    """
    planet_tables: dict[str, AshtakavargaTable] = {}

    for planet in _PLANETS:
        # Step 1: raw bindus
        raw = _compute_raw_bindus(planet, chart)

        # Step 2: Trikona Shodhana
        after_trikona = trikona_shodhana(raw)

        # Step 3: Ekadhipatya Shodhana
        reduced = ekadhipatya_shodhana(after_trikona, planet, chart)

        planet_tables[planet] = AshtakavargaTable(
            planet=planet,
            raw_bindus=raw,
            bindus=reduced,
            total=sum(reduced),
        )

    # Sarva: sum of all 7 reduced tables, then re-reduce
    sarva_raw = [
        sum(planet_tables[p].bindus[i] for p in _PLANETS)
        for i in range(12)
    ]
    sarva_after_trikona = trikona_shodhana(sarva_raw)
    # Ekadhipatya on Sarva — all dual-ruled pairs
    sarva_reduced = list(sarva_after_trikona)
    for planet in _DUAL_RULED:
        si1, si2 = _DUAL_RULED[planet]
        if sarva_reduced[si1] >= sarva_reduced[si2]:
            sarva_reduced[si2] = 0
        else:
            sarva_reduced[si1] = 0

    sarva_table = AshtakavargaTable(
        planet="Sarva",
        raw_bindus=sarva_raw,   # = sum of all 7 planet reduced bindus per sign
        bindus=sarva_reduced,   # after Trikona+Ekadhipatya Shodhana on Sarva
        total=sum(sarva_reduced),
    )

    return AshtakavargaChart(planet_av=planet_tables, sarva=sarva_table)


# ─── Kakshya analysis (Phase 2) ─────────────────────────────────────────────
# Source: BV Raman, Ashtakavarga System Ch.9
# Each sign divided into 8 Kakshyas of 3°45' each

_KAKSHYA_ORDER = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]

def kakshya_lord(longitude: float) -> str:
    """Return the Kakshya lord for a given longitude (0-360)."""
    deg_in_sign = longitude % 30
    idx = int(deg_in_sign / 3.75)
    return _KAKSHYA_ORDER[idx % 8]


def kakshya_has_bindu(
    transit_lon: float,
    natal_planet: str,
    av_chart: AshtakavargaChart,
    natal_chart,
) -> bool:
    """
    Check if the Kakshya lord at transit_lon donated a bindu in natal AV
    for the given planet's table.
    Source: BV Raman, Ashtakavarga System Ch.9
    """
    kak_lord = kakshya_lord(transit_lon)
    transit_sign = int(transit_lon / 30) % 12

    if kak_lord == "Lagna":
        contrib_sign = natal_chart.lagna_sign_index
    elif kak_lord in natal_chart.planets:
        contrib_sign = natal_chart.planets[kak_lord].sign_index
    else:
        return False

    # Check if this contributor donated a bindu to transit_sign
    house_table = _BENEFIC_HOUSES.get(natal_planet, {})
    good_houses = house_table.get(kak_lord, [])
    for h in good_houses:
        target = (contrib_sign + h - 1) % 12
        if target == transit_sign:
            return True
    return False
FIXED_TOTALS = FIXED_TOTALS_RAW


# ── Backward-compatibility: old tests expect pre-Shodhana totals ──
def compute_ashtakavarga_raw(chart) -> dict:
    """Returns pre-Shodhana bindu totals keyed by planet name.
    Use compute_ashtakavarga() for the correct post-Shodhana values."""
    result = {}
    for planet in _PLANETS:
        raw = _compute_raw_bindus(planet, chart)
        result[planet] = {"bindus": raw, "total": sum(raw)}
    sarva = [sum(result[p]["bindus"][i] for p in _PLANETS) for i in range(12)]
    result["Sarva"] = {"bindus": sarva, "total": sum(sarva)}
    return result
