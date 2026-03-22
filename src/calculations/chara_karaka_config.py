"""
src/calculations/chara_karaka_config.py
Chara Karaka computation — 7-planet and 8-planet (Rahu) variants.
Session 129 (Phase 2).

Chara Karakas are determined by the speed of planets in the chart.
The planet with the highest longitude degree in its sign = Atma Karaka (AK).

Sources:
  Jaimini Sutras Adhyaya 1, Pada 1 (7-karaka system)
  BPHS Ch.32 (8-karaka system including Rahu)
  Sanjay Rath, Crux of Vedic Astrology Ch.6 (both systems with reconciliation)
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

# ─── Karaka names and order (by descending degree in sign) ───────────────────

KARAKA_NAMES_7 = [
    "AtmaKaraka",  # AK  — soul, self
    "AmatyaKaraka",  # AmK — career, counsel
    "BhratriKaraka",  # BK  — siblings, courage
    "MatriKaraka",  # MK  — mother, mind
    "PutraKaraka",  # PiK — children, intelligence
    "GnatiKaraka",  # GK  — obstacles, disease
    "DaraKaraka",  # DK  — spouse, partnerships
]

KARAKA_NAMES_8 = KARAKA_NAMES_7[:-1] + [
    "PitraKaraka",  # PK  — father (8-karaka system only)
    "DaraKaraka",  # DK  — spouse (shifted to 8th position)
]

# 7-karaka: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn
# 8-karaka: adds Rahu (uses 360 - Rahu's longitude to get degree in sign)
PLANETS_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
PLANETS_8 = PLANETS_7 + ["Rahu"]


class KarakaSystem(str, Enum):
    SEVEN = "7"  # Standard Parashari/Jaimini — 7 planets
    EIGHT = "8"  # BPHS Ch.32 variant — includes Rahu as Pitru Karaka


@dataclass
class CharaKarakaResult:
    system: str  # "7" or "8"
    assignments: dict[str, str]  # {karaka_name: planet_name}
    degrees: dict[str, float]  # {planet: degree_in_sign used for ranking}
    atma_karaka: str  # Convenience — the AK planet
    dara_karaka: str  # Convenience — the DK planet

    @property
    def atmakaraka(self) -> str:
        """Alias for atma_karaka."""
        return self.atma_karaka


def _degree_for_ranking(planet: str, chart) -> float:
    """
    Degree within sign used for Chara Karaka ranking.
    For Rahu: use (30 - degree_in_sign) because Rahu moves retrograde.
    Source: BPHS Ch.32; Sanjay Rath, Crux Ch.6
    """
    if planet not in chart.planets:
        return 0.0
    deg = chart.planets[planet].degree_in_sign % 30
    if planet == "Rahu":
        return 30.0 - deg  # Rahu's effective degree for ranking
    return deg


def compute_chara_karakas(
    chart,
    system: str = KarakaSystem.SEVEN,
) -> CharaKarakaResult:
    """
    Compute Chara Karakas for a chart.

    7-planet system (Jaimini Sutras): Sun through Saturn
    8-planet system (BPHS Ch.32): adds Rahu as Pitru Karaka

    Source: Jaimini Sutras Adhyaya 1 Pada 1; BPHS Ch.32
    """
    if system == KarakaSystem.EIGHT:
        planets = PLANETS_8
        names = KARAKA_NAMES_8
    else:
        planets = PLANETS_7
        names = KARAKA_NAMES_7

    # Get degree in sign for each planet
    degrees = {p: _degree_for_ranking(p, chart) for p in planets}

    # Sort by descending degree — highest degree = most advanced = first karaka
    ranked = sorted(
        [p for p in planets if p in chart.planets],
        key=lambda p: degrees[p],
        reverse=True,
    )

    # Assign karaka names in order
    assignments = {}
    for i, planet in enumerate(ranked):
        if i < len(names):
            assignments[names[i]] = planet

    return CharaKarakaResult(
        system=str(system),
        assignments=assignments,
        degrees=degrees,
        atma_karaka=assignments.get("AtmaKaraka", ""),
        dara_karaka=assignments.get("DaraKaraka", ""),
    )


# ─── Karakamsha ───────────────────────────────────────────────────────────────


def compute_karakamsha(chart, chara_result: CharaKarakaResult) -> int:
    """
    Karakamsha Lagna: the D9 (navamsha) sign of the Atma Karaka.
    Source: Jaimini Sutras Adhyaya 1 Pada 2
    """
    ak = chara_result.atma_karaka
    if not ak or ak not in chart.planets:
        return chart.lagna_sign_index

    ak_lon = chart.planets[ak].longitude
    try:
        from src.calculations.vargas import compute_varga_sign

        return compute_varga_sign(ak_lon, 9)
    except Exception:
        # Fallback
        si = int(ak_lon / 30) % 12
        pada = int((ak_lon % 30) * 9 / 30)
        D9_START = {0: 0, 1: 9, 2: 6, 3: 3}
        return (D9_START[si % 4] + pada) % 12


# ─── Swamsha ─────────────────────────────────────────────────────────────────


def is_swamsha(chart, chara_result: CharaKarakaResult) -> bool:
    """
    Swamsha: AK in its own sign or exaltation in D9.
    A very powerful placement — native is spiritually advanced.
    Source: Jaimini Sutras; Sanjay Rath commentary
    """
    ak = chara_result.atma_karaka
    if not ak or ak not in chart.planets:
        return False

    ak_lon = chart.planets[ak].longitude
    try:
        from src.calculations.vargas import compute_varga_sign

        d9_si = compute_varga_sign(ak_lon, 9)
    except Exception:
        return False

    from src.calculations.dignity import EXALT_SIGN, OWN_SIGNS

    if d9_si in OWN_SIGNS.get(ak, []):
        return True
    if d9_si == EXALT_SIGN.get(ak):
        return True
    return False
