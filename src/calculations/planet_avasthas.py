"""
src/calculations/planet_avasthas.py
Planetary Avasthas (States) — age-based and element-based.
Session 138.

Bala Avastha: 5 age states by degree in sign (BPHS Ch.45)
Jagradadi Avastha: Awake/Dreaming/Sleeping by element compatibility (Saravali Ch.5)
Deeptadi Avastha: 9-state system including exaltation states (Phaladeepika Ch.8)

Sources:
  PVRNR · BPHS Ch.45 v.1-8 (Bala Avastha)
  Saravali · Kalyanarma Ch.5 v.8-14 (Jagradadi)
  Mantreswara · Phaladeepika Ch.8 v.5-12 (Deeptadi with Deepta)
  Jataka Parijata · Vaidyanatha Dikshita Ch.4 (Jagradadi + interpretive)
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

# ─── Bala Avastha ─────────────────────────────────────────────────────────────

class BalaAvastha(str, Enum):
    BALA    = "Bala"     # Infant (0°-6°): erratic, weak results
    KUMARA  = "Kumara"   # Youth (6°-12°): some strength, inconsistent
    YUVA    = "Yuva"     # Adult (12°-18°): full strength, best results
    VRIDDHA = "Vriddha"  # Old (18°-24°): declining, delayed results
    MRITA   = "Mrita"    # Dead (24°-30°): very weak, extreme delays

# Scoring modifiers per Bala Avastha (multiplier on planet's effectiveness)
BALA_AVASTHA_MODIFIER: dict[BalaAvastha, float] = {
    BalaAvastha.BALA:    0.65,
    BalaAvastha.KUMARA:  0.85,
    BalaAvastha.YUVA:    1.20,
    BalaAvastha.VRIDDHA: 0.80,
    BalaAvastha.MRITA:   0.60,
}

def bala_avastha(degree_in_sign: float) -> BalaAvastha:
    """
    Returns the Bala Avastha for a planet's degree within its sign.
    Source: PVRNR · BPHS Ch.45 v.1-8
    """
    d = degree_in_sign % 30
    if d < 6:   return BalaAvastha.BALA
    if d < 12:  return BalaAvastha.KUMARA
    if d < 18:  return BalaAvastha.YUVA
    if d < 24:  return BalaAvastha.VRIDDHA
    return BalaAvastha.MRITA


# ─── Jagradadi Avastha (Awake/Dreaming/Sleeping) ─────────────────────────────

class JagradadiAvastha(str, Enum):
    JAGRAT   = "Jagrat"   # Awake — fully operative
    SVAPNA   = "Svapna"   # Dreaming — partially operative
    SUSHUPTI = "Sushupti" # Deep Sleep — dormant

# Element compatibility table
# Fire: Aries(0), Leo(4), Sagittarius(8)
# Earth: Taurus(1), Virgo(5), Capricorn(9)
# Air: Gemini(2), Libra(6), Aquarius(10)
# Water: Cancer(3), Scorpio(7), Pisces(11)
_SIGN_ELEMENT: dict[int, str] = {
    0: "fire", 1: "earth", 2: "air",   3: "water",
    4: "fire", 5: "earth", 6: "air",   7: "water",
    8: "fire", 9: "earth", 10: "air",  11: "water",
}

# Planet's natural element
_PLANET_ELEMENT: dict[str, str] = {
    "Sun":     "fire",
    "Moon":    "water",
    "Mars":    "fire",
    "Mercury": "earth",    # Mercury is variable; traditionally earth per Phaladeepika
    "Jupiter": "ether",    # Akasha — compatible with all except pure earth
    "Venus":   "water",
    "Saturn":  "air",
    "Rahu":    "air",
    "Ketu":    "fire",
}

# Element compatibility matrix: {planet_element: {sign_element: avastha}}
_COMPATIBILITY: dict[str, dict[str, JagradadiAvastha]] = {
    "fire":  {"fire": JagradadiAvastha.JAGRAT, "air": JagradadiAvastha.SVAPNA,
              "earth": JagradadiAvastha.SUSHUPTI, "water": JagradadiAvastha.SUSHUPTI},
    "earth": {"earth": JagradadiAvastha.JAGRAT, "water": JagradadiAvastha.SVAPNA,
              "fire": JagradadiAvastha.SUSHUPTI, "air": JagradadiAvastha.SUSHUPTI},
    "air":   {"air": JagradadiAvastha.JAGRAT, "fire": JagradadiAvastha.SVAPNA,
              "water": JagradadiAvastha.SUSHUPTI, "earth": JagradadiAvastha.SUSHUPTI},
    "water": {"water": JagradadiAvastha.JAGRAT, "earth": JagradadiAvastha.SVAPNA,
              "air": JagradadiAvastha.SUSHUPTI, "fire": JagradadiAvastha.SUSHUPTI},
    "ether": {"fire": JagradadiAvastha.JAGRAT, "air": JagradadiAvastha.JAGRAT,
              "water": JagradadiAvastha.SVAPNA, "earth": JagradadiAvastha.SVAPNA},
}

JAGRADADI_MODIFIER: dict[JagradadiAvastha, float] = {
    JagradadiAvastha.JAGRAT:   1.0,
    JagradadiAvastha.SVAPNA:   0.7,
    JagradadiAvastha.SUSHUPTI: 0.5,
}

def jagradadi_avastha(planet: str, sign_index: int) -> JagradadiAvastha:
    """
    Returns Jagradadi Avastha based on element compatibility.
    Source: Saravali Ch.5 v.8-14; Jataka Parijata Ch.4
    """
    planet_elem = _PLANET_ELEMENT.get(planet, "air")
    sign_elem   = _SIGN_ELEMENT.get(sign_index % 12, "fire")
    return _COMPATIBILITY.get(planet_elem, {}).get(sign_elem, JagradadiAvastha.SVAPNA)


# ─── Deeptadi Avastha (9-state system) ───────────────────────────────────────

class DeeptadiAvastha(str, Enum):
    DEEPTA   = "Deepta"    # Exalted/own sign: brilliant, gives excellent results
    SWASTHA  = "Swastha"   # Own sign (healthy): good results
    MUDITA   = "Mudita"    # Friend's sign: happy, moderate results
    SHANTA   = "Shanta"    # Neutral sign: calm, average results
    DINA     = "Dina"      # Weak/enemy sign: miserable, poor results
    DUKHITA  = "Dukhita"   # Debilitated: sorrowful, bad results
    VIKALA   = "Vikala"    # Combust: lame/crippled, erratic
    KHALA    = "Khala"     # Retro+enemy: harsh/cruel tendencies
    KOPA     = "Kopa"      # Retrograde + debilitation: angry, extreme results

def deeptadi_avastha(planet: str, chart) -> DeeptadiAvastha:
    """
    9-state Deeptadi Avastha from Phaladeepika Ch.8.
    """
    if planet not in chart.planets:
        return DeeptadiAvastha.SHANTA

    from src.calculations.dignity import compute_dignity, DignityLevel
    d = compute_dignity(planet, chart)
    pdata = chart.planets[planet]
    is_rx = pdata.is_retrograde

    if d.combust and not d.cazimi:
        return DeeptadiAvastha.VIKALA

    if d.dignity == DignityLevel.DEEP_EXALT or d.dignity == DignityLevel.EXALT:
        return DeeptadiAvastha.DEEPTA

    if d.dignity in (DignityLevel.MOOLTRIKONA, DignityLevel.OWN_SIGN):
        return DeeptadiAvastha.SWASTHA

    if d.dignity == DignityLevel.FRIEND_SIGN:
        return DeeptadiAvastha.MUDITA

    if d.dignity == DignityLevel.NEUTRAL:
        return DeeptadiAvastha.SHANTA

    if d.dignity == DignityLevel.DEBIL:
        if is_rx:
            return DeeptadiAvastha.KOPA
        return DeeptadiAvastha.DUKHITA

    if d.dignity == DignityLevel.ENEMY_SIGN:
        if is_rx:
            return DeeptadiAvastha.KHALA
        return DeeptadiAvastha.DINA

    return DeeptadiAvastha.SHANTA


# ─── Combined Avastha Result ──────────────────────────────────────────────────

@dataclass
class AvasthaResult:
    planet: str
    bala_avastha: BalaAvastha
    jagradadi: JagradadiAvastha
    deeptadi: DeeptadiAvastha
    combined_modifier: float    # product of all modifiers (capped 0.4-1.3)
    summary: str


def compute_avasthas(planet: str, chart) -> AvasthaResult:
    """Compute all avasthas for a planet."""
    if planet not in chart.planets:
        return AvasthaResult(planet, BalaAvastha.YUVA, JagradadiAvastha.JAGRAT,
                             DeeptadiAvastha.SHANTA, 1.0, "Planet not in chart")

    deg = chart.planets[planet].degree_in_sign
    si  = chart.planets[planet].sign_index

    bala = bala_avastha(deg)
    jagra = jagradadi_avastha(planet, si)
    deepta = deeptadi_avastha(planet, chart)

    # Combined modifier
    mod = BALA_AVASTHA_MODIFIER[bala] * JAGRADADI_MODIFIER[jagra]
    mod = max(0.4, min(1.3, mod))

    # summary removed (Ruff F841 — unused variable)

    return AvasthaResult(
        planet=planet,
        bala_avastha=bala,
        jagradadi=jagra,
        deeptadi=deepta,
        combined_modifier=round(mod, 3),
        summary=f"{bala.value} | {jagra.value} | {deepta.value} | mod={mod:.2f}",
    )


def compute_all_avasthas(chart) -> dict[str, AvasthaResult]:
    """Compute all avasthas for all planets in chart."""
    return {p: compute_avasthas(p, chart) for p in chart.planets}
