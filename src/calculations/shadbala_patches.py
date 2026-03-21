"""
src/calculations/shadbala_patches.py
Shadbala minimum thresholds + 5-fold Panchadhyayee Maitri friendship.
Graha Yuddha loser persistence + NBRY surfacing in yoga list.
Sessions 141, 144, 147, C-2.

Sources:
  PVRNR · BPHS Ch.27 v.76-80 (minimum Shadbala thresholds)
  PVRNR · BPHS Ch.15 v.1-12 (Panchadhyayee Maitri / 5-fold friendship)
  BV Raman · Hindu Predictive Astrology Ch.3 (5-fold friendship matrix)
  Saravali · Ch.4 v.18-22 (Graha Yuddha — loser = debilitated throughout life)
"""
from __future__ import annotations
from typing import Optional

# ─── Shadbala Minimum Thresholds ─────────────────────────────────────────────
# Source: PVRNR · BPHS Ch.27 v.76-80

SHADBALA_MIN_VIRUPAS: dict[str, float] = {
    "Sun":     390.0,
    "Moon":    360.0,
    "Mars":    300.0,
    "Mercury": 420.0,
    "Jupiter": 390.0,
    "Venus":   330.0,
    "Saturn":  300.0,
}


def is_shadbala_strong(planet: str, total_virupas: float) -> bool:
    """Returns True if planet meets BPHS minimum Shadbala threshold."""
    return total_virupas >= SHADBALA_MIN_VIRUPAS.get(planet, 300.0)


def shadbala_strength_label(planet: str, total_virupas: float) -> str:
    """Returns 'Strong' / 'Moderate' / 'Weak' relative to BPHS threshold."""
    threshold = SHADBALA_MIN_VIRUPAS.get(planet, 300.0)
    ratio = total_virupas / threshold if threshold > 0 else 0
    if ratio >= 1.0:   return "Strong"
    if ratio >= 0.75:  return "Moderate"
    return "Weak"


# ─── Panchadhyayee Maitri (5-fold Friendship) ────────────────────────────────
# Source: PVRNR · BPHS Ch.15; BV Raman · Hindu Predictive Astrology Ch.3
#
# Permanent (Naisargika) friendship:
_NAISARGIKA: dict[tuple[str, str], str] = {
    ("Sun","Moon"): "Friend", ("Sun","Mars"): "Friend", ("Sun","Jupiter"): "Friend",
    ("Sun","Mercury"): "Neutral", ("Sun","Venus"): "Enemy", ("Sun","Saturn"): "Enemy",
    ("Moon","Sun"): "Friend", ("Moon","Mercury"): "Friend",
    ("Moon","Mars"): "Neutral", ("Moon","Jupiter"): "Neutral",
    ("Moon","Venus"): "Neutral", ("Moon","Saturn"): "Neutral",
    ("Mars","Sun"): "Friend", ("Mars","Moon"): "Friend", ("Mars","Jupiter"): "Friend",
    ("Mars","Mercury"): "Enemy", ("Mars","Venus"): "Neutral", ("Mars","Saturn"): "Neutral",
    ("Mercury","Sun"): "Friend", ("Mercury","Venus"): "Friend",
    ("Mercury","Moon"): "Enemy", ("Mercury","Mars"): "Neutral",
    ("Mercury","Jupiter"): "Neutral", ("Mercury","Saturn"): "Neutral",
    ("Jupiter","Sun"): "Friend", ("Jupiter","Moon"): "Friend", ("Jupiter","Mars"): "Friend",
    ("Jupiter","Mercury"): "Enemy", ("Jupiter","Saturn"): "Enemy", ("Jupiter","Venus"): "Neutral",
    ("Venus","Mercury"): "Friend", ("Venus","Saturn"): "Friend",
    ("Venus","Sun"): "Enemy", ("Venus","Moon"): "Neutral",
    ("Venus","Mars"): "Neutral", ("Venus","Jupiter"): "Neutral",
    ("Saturn","Mercury"): "Friend", ("Saturn","Venus"): "Friend",
    ("Saturn","Sun"): "Enemy", ("Saturn","Moon"): "Enemy",
    ("Saturn","Mars"): "Neutral", ("Saturn","Jupiter"): "Neutral",
}

# Tatkalika friendship: planets in signs 2/3/4/10/11/12 from given planet = temporary friend
_TEMP_FRIEND_POSITIONS = {2, 3, 4, 10, 11, 12}
_TEMP_ENEMY_POSITIONS  = {1, 5, 6, 7, 8, 9}

# 5-fold combined friendship
_COMBINED: dict[tuple[str, str], str] = {
    ("Friend",  "Friend"):  "Adhimitra",    # Intimate Friend
    ("Friend",  "Neutral"): "Mitra",        # Friend
    ("Friend",  "Enemy"):   "Sama",         # Neutral
    ("Neutral", "Friend"):  "Mitra",
    ("Neutral", "Neutral"): "Sama",
    ("Neutral", "Enemy"):   "Shatru",       # Enemy
    ("Enemy",   "Friend"):  "Sama",
    ("Enemy",   "Neutral"): "Shatru",
    ("Enemy",   "Enemy"):   "Adhi-Shatru",  # Bitter Enemy
}

# Saptavargaja Virupas for 5-fold friendship
PANCHADHYAYEE_VIRUPAS: dict[str, float] = {
    "Adhimitra":  22.5,
    "Mitra":      15.0,
    "Sama":        7.5,
    "Shatru":      3.75,
    "Adhi-Shatru": 1.875,
    # Own sign and exaltation handled separately
}


def tatkalika_friendship(planet_a: str, planet_b: str, chart) -> str:
    """
    Temporary (Tatkalika) friendship: B is a temp friend of A if B is in
    2/3/4/10/11/12 from A's sign position.
    Source: PVRNR · BPHS Ch.15 v.1-5
    """
    if planet_a not in chart.planets or planet_b not in chart.planets:
        return "Neutral"
    a_si = chart.planets[planet_a].sign_index
    b_si = chart.planets[planet_b].sign_index
    house_b_from_a = ((b_si - a_si) % 12) + 1
    if house_b_from_a in _TEMP_FRIEND_POSITIONS:
        return "Friend"
    return "Enemy"


def panchadhyayee_maitri(planet_a: str, planet_b: str, chart) -> str:
    """
    Combined 5-fold friendship between two planets.
    Source: PVRNR · BPHS Ch.15; BV Raman Ch.3
    """
    naisargika = _NAISARGIKA.get((planet_a, planet_b), "Neutral")
    tatkalika  = tatkalika_friendship(planet_a, planet_b, chart)
    return _COMBINED.get((naisargika, tatkalika), "Sama")


def get_saptavargaja_virupas(relation: str) -> float:
    """Returns Virupa value for a 5-fold friendship relationship."""
    return PANCHADHYAYEE_VIRUPAS.get(relation, 7.5)


# ─── Graha Yuddha Loser Persistence ─────────────────────────────────────────

def apply_war_loser_dignity(chart, war_results: list) -> dict[str, str]:
    """
    Returns dignity overrides for war losers.
    War loser is treated as effectively DEBILITATED throughout life.
    Source: Saravali Ch.4 v.18-22; Varahamihira · Brihat Jataka Ch.3 v.11
    """
    overrides = {}
    for war in war_results:
        if hasattr(war, 'loser') and war.loser:
            overrides[war.loser] = "GRAHA_YUDDHA_DEBIL"
    return overrides


# ─── NBRY Surfacing in Yoga Pipeline ─────────────────────────────────────────

def extract_nbry_yogas(chart) -> list[dict]:
    """
    Extract Neecha Bhanga Raja Yogas from dignity results and surface as named yogas.
    Source: Uttarakalamrita Ch.4 v.11-14 (NBRY ranked among highest Raja Yogas)
    """
    from src.calculations.dignity import compute_all_dignities, DignityLevel

    dignities = compute_all_dignities(chart)
    nbry_yogas = []

    for planet, d in dignities.items():
        if d.dignity == DignityLevel.NEECHA_BHANGA_RAJA:
            conditions_met = []
            if d.nb_lord_kendra_lagna:   conditions_met.append("Debil lord in Kendra from Lagna")
            if d.nb_lord_kendra_moon:    conditions_met.append("Debil lord in Kendra from Moon")
            if d.nb_exalt_kendra_lagna:  conditions_met.append("Exalt lord of debil sign in Kendra from Lagna")
            if d.nb_exalt_kendra_moon:   conditions_met.append("Exalt lord in Kendra from Moon")
            if d.nb_aspected_by_lord:    conditions_met.append("Debil lord aspects planet")
            if d.nb_parivartana:         conditions_met.append("Parivartana with sign lord")

            nbry_yogas.append({
                "name": f"Neecha Bhanga Raja Yoga ({planet})",
                "planet": planet,
                "conditions_met": conditions_met,
                "conditions_count": d.neecha_bhanga_count,
                "description": (
                    f"{planet} is debilitated but {d.neecha_bhanga_count} cancellation conditions active — "
                    f"native overcomes obstacles that would defeat others; "
                    f"excels in {planet}'s significations during its dasha"
                ),
                "source": "Uttarakalamrita Ch.4 v.11-14; BPHS Ch.49 v.12-18",
                "scoring_bonus": 1.5,
            })

    return nbry_yogas
