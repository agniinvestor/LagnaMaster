"""
src/calculations/avastha.py — LagnaMaster Session 29

Three avastha (planetary state) systems from classical Parashari sources.
Each state modifies the effective strength and quality of a planet's results.

Systems implemented
-------------------
1. Deeptadi Avastha (6 states based on dignity)
2. Baladi Avastha (5 states based on degree within sign — age metaphor)
3. Lajjitadi Avastha (6 states for the 5th house lord — psychological burden)

Lajjitadi is the most pressure-relevant: Lajjita (ashamed) occurs when the
5th lord is conjunct a malefic, combust, or in a dusthana — correlates
strongly with psychological burden, creative/child grief, mental distress.

Public API
----------
    compute_deeptadi(planet, chart) -> str
    compute_baladi(planet, chart)   -> str
    compute_lajjitadi(chart)        -> LajjitadiResult
    compute_all_avasthas(chart)     -> AvasthaReport
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# ── Deeptadi (6 states) ───────────────────────────────────────────────────────
# Based on dignity — maps to effective output multiplier
DEEPTADI_STATES = {
    "Deepta":    {"description": "Exalted/Moolatrikona — fully illumined",  "multiplier": 1.5},
    "Swastha":   {"description": "Own sign — comfortable",                   "multiplier": 1.0},
    "Mudita":    {"description": "Friend's sign — pleased",                  "multiplier": 0.75},
    "Shanta":    {"description": "Neutral sign — calm",                      "multiplier": 0.5},
    "Dukha":     {"description": "Enemy sign — suffering",                   "multiplier": 0.25},
    "Kshobhita": {"description": "Debilitated/Combust — agitated",           "multiplier": 0.0},
}

def compute_deeptadi(planet: str, chart) -> str:
    """Return the Deeptadi state name for a planet."""
    from src.calculations.dignity import compute_dignity, DignityLevel
    d = compute_dignity(planet, chart)
    if d.dignity in {DignityLevel.EXALT, DignityLevel.MOOLTRIKONA}:
        return "Deepta"
    if d.dignity == DignityLevel.OWN_SIGN:
        return "Swastha"
    if d.dignity == DignityLevel.FRIEND_SIGN:
        return "Mudita"
    if d.dignity == DignityLevel.NEUTRAL:
        return "Shanta"
    if d.dignity == DignityLevel.ENEMY_SIGN:
        return "Dukha"
    # Debilitated or combust
    return "Kshobhita"


# ── Baladi (5 states — degree-based age metaphor) ─────────────────────────────
# Each sign is divided into 6° segments; planet's degree determines its "age"
# Bala=0–6°: infant (weak); Kumara=6–12°: adolescent; Yuva=12–18°: youth (strong)
# Vriddha=18–24°: old (declining); Mrita=24–30°: dead (very weak)
BALADI_STATES = {
    "Bala":     {"description": "Infant — weak and dependent",    "multiplier": 0.25},
    "Kumara":   {"description": "Adolescent — developing",        "multiplier": 0.5},
    "Yuva":     {"description": "Youth — full strength",          "multiplier": 1.0},
    "Vriddha":  {"description": "Old — declining",                "multiplier": 0.5},
    "Mrita":    {"description": "Dead — extremely weak results",  "multiplier": 0.1},
}

def compute_baladi(planet: str, chart) -> str:
    """Return the Baladi state for a planet based on degree within sign."""
    pos = chart.planets.get(planet)
    if pos is None:
        return "Yuva"
    d = pos.degree_in_sign
    if d < 6:   return "Bala"
    if d < 12:  return "Kumara"
    if d < 18:  return "Yuva"
    if d < 24:  return "Vriddha"
    return "Mrita"


# ── Lajjitadi (6 states for 5th house lord — stress-focused) ─────────────────
@dataclass
class LajjitadiResult:
    fifth_lord: str
    state: str          # Lajjita / Garvita / Kshudhita / Trushita / Mudita / Kshobhita
    description: str
    pressure_score: float   # 0.0 (no pressure) to 1.0 (maximum)
    triggers: list[str]     # what triggered this state

LAJJITADI_STATES = {
    "Lajjita":   ("Ashamed — 5th lord with malefic/combust in dusthana", 1.0),
    "Kshudhita": ("Hungry — 5th lord with enemy/neutral in dusthana",    0.7),
    "Trushita":  ("Thirsty — 5th lord with benefic in dusthana",         0.4),
    "Kshobhita": ("Agitated — 5th lord combust or with Rahu/Ketu",       0.8),
    "Garvita":   ("Proud — 5th lord exalted/own sign in kendra/trikona", 0.0),
    "Mudita":    ("Pleased — 5th lord with natural benefic",             0.0),
}

def compute_lajjitadi(chart) -> LajjitadiResult:
    """Compute Lajjitadi state for the 5th house lord (most pressure-relevant)."""
    from src.calculations.house_lord import compute_house_map
    from src.calculations.dignity import compute_dignity, DignityLevel

    hmap = compute_house_map(chart)
    fifth_lord = hmap.house_lord[4]   # 0-indexed: index 4 = H5
    pos = chart.planets.get(fifth_lord)

    if pos is None:
        return LajjitadiResult(fifth_lord, "Mudita", "Planet not found", 0.0, [])

    fifth_lord_house = hmap.planet_house.get(fifth_lord, 1)
    in_dusthana = fifth_lord_house in {6, 8, 12}
    in_kendra   = fifth_lord_house in {1, 4, 7, 10}
    in_trikona  = fifth_lord_house in {1, 5, 9}

    dig = compute_dignity(fifth_lord, chart)
    combust = dig.combust
    exalted = dig.dignity in {DignityLevel.EXALT, DignityLevel.MOOLTRIKONA}
    own_sign = dig.dignity == DignityLevel.OWN_SIGN

    # Co-tenants (planets in same sign)
    co_signs = [p for p, pp in chart.planets.items()
                if pp.sign_index == pos.sign_index and p != fifth_lord]
    nat_malefics   = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
    nodes_present  = bool({"Rahu", "Ketu"} & set(co_signs))
    malefic_present = bool(nat_malefics & set(co_signs))
    benefic_present = bool({"Jupiter", "Venus", "Mercury", "Moon"} & set(co_signs))

    triggers = []
    if in_dusthana: triggers.append(f"in H{fifth_lord_house} (dusthana)")
    if combust:     triggers.append("combust")
    if nodes_present: triggers.append("conjunct Rahu/Ketu")
    if malefic_present: triggers.append(f"conjunct malefic(s): {[p for p in co_signs if p in nat_malefics]}")

    # State determination
    if (in_dusthana and malefic_present) or (in_dusthana and combust):
        state = "Lajjita"
    elif nodes_present or combust:
        state = "Kshobhita"
    elif in_dusthana and not benefic_present:
        state = "Kshudhita"
    elif in_dusthana and benefic_present:
        state = "Trushita"
    elif (exalted or own_sign) and (in_kendra or in_trikona):
        state = "Garvita"
    else:
        state = "Mudita"

    desc, pressure = LAJJITADI_STATES[state]
    return LajjitadiResult(fifth_lord, state, desc, pressure, triggers)


# ── Combined report ───────────────────────────────────────────────────────────
@dataclass
class AvasthaReport:
    deeptadi:   dict[str, str]      # planet -> state
    baladi:     dict[str, str]      # planet -> state
    lajjitadi:  LajjitadiResult
    # Effective strength multipliers (product of deeptadi × baladi)
    effective_multipliers: dict[str, float] = field(default_factory=dict)

_PLANETS_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]

def compute_all_avasthas(chart) -> AvasthaReport:
    deeptadi = {p: compute_deeptadi(p, chart) for p in _PLANETS_7}
    baladi   = {p: compute_baladi(p, chart)   for p in _PLANETS_7}
    lajjitadi = compute_lajjitadi(chart)
    effective = {
        p: DEEPTADI_STATES[deeptadi[p]]["multiplier"] * BALADI_STATES[baladi[p]]["multiplier"]
        for p in _PLANETS_7
    }
    return AvasthaReport(deeptadi=deeptadi, baladi=baladi,
                         lajjitadi=lajjitadi, effective_multipliers=effective)
