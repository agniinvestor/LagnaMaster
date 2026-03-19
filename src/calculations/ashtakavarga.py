"""
src/calculations/ashtakavarga.py
=================================
Classical Parashari Ashtakavarga (8-source bindu system).

For each of the 7 planets (Sun through Saturn), a table of 12 bindus
(one per sign) is computed by asking: do any of the 8 contributors
(Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Lagna) fall in a
position that donates a bindu to that sign?

Benefic house lists from BPHS (Santhanam translation), Chapter 66.
Houses are counted from the contributor's sign (inclusive, 1-based).

Sarvashtakavarga (Sarva = "total") is the sum of all 7 planet tables.
Classical fixed totals: Sun=50, Moon=49, Mars=39, Mercury=54,
                        Jupiter=56, Venus=52, Saturn=39 (Σ=339)

Usage:
    from src.calculations.ashtakavarga import compute_ashtakavarga
    av = compute_ashtakavarga(chart)
    # av.sarva.bindus[si] → total bindus for sign index si
    # av.planet_av["Sun"].bindus[3] → Sun's bindus in Cancer
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.ephemeris import BirthChart, SIGNS

# ---------------------------------------------------------------------------
# Classical benefic-house tables (BPHS, Santhanam translation)
# Keys: target planet whose table is being built
# Sub-keys: the 8 contributors (planets + "Lagna")
# Values: list of house numbers (1-12) counted FROM the contributor's sign
#         A bindu is placed in sign (contributor_sign + h - 1) % 12
# ---------------------------------------------------------------------------

_BENEFIC_HOUSES: dict[str, dict[str, list[int]]] = {
    "Sun": {
        "Sun":     [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon":    [3, 6, 10, 11],
        "Mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus":   [6, 7, 12],
        "Saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna":   [1, 2, 4, 7, 8, 9, 10, 11],
    },
    "Moon": {
        "Sun":     [3, 6, 7, 8, 10, 11],
        "Moon":    [1, 3, 6, 7, 10, 11],
        "Mars":    [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11],
        "Venus":   [3, 4, 5, 7, 9, 10, 11],
        "Saturn":  [3, 5, 6, 11],
        "Lagna":   [3, 6, 10, 11],
    },
    "Mars": {
        "Sun":     [3, 5, 6, 10, 11],
        "Moon":    [3, 6, 11],
        "Mars":    [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus":   [6, 8, 11, 12],
        "Saturn":  [1, 4, 7, 8, 9, 10, 11],
        "Lagna":   [1, 2, 4, 7, 8, 9, 10, 11],
    },
    "Mercury": {
        "Sun":     [5, 6, 9, 11, 12],
        "Moon":    [2, 4, 6, 8, 10, 11],
        "Mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus":   [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna":   [1, 2, 4, 7, 8, 9, 10, 11],
    },
    "Jupiter": {
        "Sun":     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon":    [2, 5, 7, 9, 11],
        "Mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus":   [2, 5, 6, 9, 10, 11],
        "Saturn":  [3, 5, 6, 12],
        "Lagna":   [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun":     [8, 11, 12],
        "Moon":    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars":    [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus":   [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Saturn":  [3, 4, 5, 8, 9, 10, 11],
        "Lagna":   [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun":     [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon":    [3, 6, 11],
        "Mars":    [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus":   [6, 11, 12],
        "Saturn":  [3, 5, 6, 11],
        "Lagna":   [1, 3, 4, 6, 10, 11],
    },
}

# Planets in computation order (Rahu/Ketu excluded — no AV tables in Parashari)
_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Pre-computed fixed totals per planet (sum of all benefic-house list lengths)
# These are chart-independent and can be used for validation.
FIXED_TOTALS: dict[str, int] = {
    planet: sum(len(h) for h in contributors.values())
    for planet, contributors in _BENEFIC_HOUSES.items()
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AshtakavargaTable:
    """Ashtakavarga bindus for one planet (or Sarva) across 12 signs."""
    planet: str                  # e.g. "Sun", "Moon", …, "Sarva"
    bindus: list[int]            # 12 values; index 0 = Aries, 11 = Pisces
    total: int                   # sum(bindus) — fixed per planet, chart-independent

    def bindu_for_sign(self, sign_index: int) -> int:
        """Return bindu count for a sign by index (0 = Aries)."""
        return self.bindus[sign_index % 12]

    def bindu_for_sign_name(self, sign_name: str) -> int:
        """Return bindu count for a sign by name (e.g. 'Cancer')."""
        return self.bindus[SIGNS.index(sign_name)]

    def strength(self, sign_index: int) -> str:
        """
        Classical strength rating for a sign's bindu count:
          ≥ 5 : Strong (beneficial transits; auspicious periods)
          4   : Average
          ≤ 3 : Weak (inauspicious transits)
        For Sarva (max 56 per sign): use proportional thresholds.
        """
        b = self.bindus[sign_index % 12]
        if self.planet == "Sarva":
            if b >= 30:
                return "Strong"
            elif b >= 25:
                return "Average"
            else:
                return "Weak"
        else:
            if b >= 5:
                return "Strong"
            elif b == 4:
                return "Average"
            else:
                return "Weak"


@dataclass
class AshtakavargaChart:
    """Complete Ashtakavarga for a birth chart: 7 planet tables + Sarva."""
    planet_av: dict[str, AshtakavargaTable]  # keyed by planet name
    sarva: AshtakavargaTable                  # Sarvashtakavarga total

    def for_planet(self, planet: str) -> AshtakavargaTable:
        return self.planet_av[planet]


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def compute_ashtakavarga(chart: BirthChart) -> AshtakavargaChart:
    """
    Compute classical Parashari Ashtakavarga for all 7 planets.

    Algorithm for each target planet P:
      For each contributor C (7 planets + Lagna):
        contributor_sign = C's sign_index (or lagna_sign_index for Lagna)
        For each benefic_house h in _BENEFIC_HOUSES[P][C]:
          sign_idx = (contributor_sign + h - 1) % 12
          bindus[P][sign_idx] += 1

    Sarvashtakavarga = element-wise sum of all 7 planet bindu arrays.
    """
    lagna_si = chart.lagna_sign_index

    planet_avs: dict[str, AshtakavargaTable] = {}

    for target_planet in _PLANETS:
        bindus = [0] * 12
        contributor_table = _BENEFIC_HOUSES[target_planet]

        for contributor, benefic_houses in contributor_table.items():
            if contributor == "Lagna":
                contributor_si = lagna_si
            else:
                contributor_si = chart.planets[contributor].sign_index

            for h in benefic_houses:
                sign_idx = (contributor_si + h - 1) % 12
                bindus[sign_idx] += 1

        planet_avs[target_planet] = AshtakavargaTable(
            planet=target_planet,
            bindus=bindus,
            total=sum(bindus),
        )

    # Sarvashtakavarga: sum each sign across all 7 planet tables
    sarva_bindus = [0] * 12
    for table in planet_avs.values():
        for i, b in enumerate(table.bindus):
            sarva_bindus[i] += b

    sarva = AshtakavargaTable(
        planet="Sarva",
        bindus=sarva_bindus,
        total=sum(sarva_bindus),
    )

    return AshtakavargaChart(planet_av=planet_avs, sarva=sarva)
