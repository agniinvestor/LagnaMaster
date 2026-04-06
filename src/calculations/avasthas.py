"""
src/calculations/avasthas.py — Planetary Avasthas (States)
S317 — BPHS Ch.45 v.2-18 (pp.449-452, Santhanam Vol 1)

Three avastha systems defined by Parasara:
1. Baaladi (5 states by degree position) — v.3-6
2. Jagradadi (3 states by dignity) — v.5-6
3. Lajjitadi (6 states by association) — v.11-18
4. Sayanadi (12 states by formula) — v.30-37 [not implemented yet]

Ch.11 references Baaladi + Jagradadi for house evaluation:
  Yuva/Kumara → house prospers
  Vriddha → ineffective, Mrita → destroyed, Supta → neutralized
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Baaladi Avasthas — BPHS Ch.45 v.3 (p.449)
# ═══════════════════════════════════════════════════════════════════════════════

class BaaladiAvastha(Enum):
    """Five states by degree in sign. Effect ratios from v.4."""
    BAALA = "Infant"        # 1/4 effect
    KUMARA = "Youthful"     # 1/2 effect
    YUVA = "Adolescent"     # FULL effect
    VRIDDHA = "Old"         # negligible effect
    MRITA = "Dead"          # nil effect


# Effect multiplier per Baaladi state — BPHS Ch.45 v.4
BAALADI_EFFECT: dict[BaaladiAvastha, float] = {
    BaaladiAvastha.BAALA: 0.25,
    BaaladiAvastha.KUMARA: 0.50,
    BaaladiAvastha.YUVA: 1.00,
    BaaladiAvastha.VRIDDHA: 0.125,  # "negligible"
    BaaladiAvastha.MRITA: 0.0,
}


def compute_baaladi(sign_index: int, degree_in_sign: float) -> BaaladiAvastha:
    """BPHS Ch.45 v.3: 6° intervals, reversed for even signs.

    Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius):
      0-6° = Baala, 6-12° = Kumara, 12-18° = Yuva, 18-24° = Vriddha, 24-30° = Mrita

    Even signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces):
      0-6° = Mrita, 6-12° = Vriddha, 12-18° = Yuva, 18-24° = Kumara, 24-30° = Baala
    """
    is_odd = sign_index % 2 == 0  # Aries=0 is odd
    d = degree_in_sign

    if is_odd:
        order = [
            BaaladiAvastha.BAALA, BaaladiAvastha.KUMARA, BaaladiAvastha.YUVA,
            BaaladiAvastha.VRIDDHA, BaaladiAvastha.MRITA,
        ]
    else:
        order = [
            BaaladiAvastha.MRITA, BaaladiAvastha.VRIDDHA, BaaladiAvastha.YUVA,
            BaaladiAvastha.KUMARA, BaaladiAvastha.BAALA,
        ]

    idx = min(int(d / 6.0), 4)
    return order[idx]


# ═══════════════════════════════════════════════════════════════════════════════
# 2. Jagradadi Avasthas — BPHS Ch.45 v.5-6 (pp.449-450)
# ═══════════════════════════════════════════════════════════════════════════════

class JagradadiAvastha(Enum):
    """Three states by dignity (sign relationship)."""
    JAGRAT = "Awakening"   # own sign or exaltation → full
    SWAPNA = "Dreaming"    # friend or neutral sign → medium
    SUPTA = "Sleeping"     # enemy sign or debilitation → nil


JAGRADADI_EFFECT: dict[JagradadiAvastha, float] = {
    JagradadiAvastha.JAGRAT: 1.0,
    JagradadiAvastha.SWAPNA: 0.5,
    JagradadiAvastha.SUPTA: 0.0,
}


def compute_jagradadi(planet: str, sign_index: int) -> JagradadiAvastha:
    """BPHS Ch.45 v.5: own/exalt = Jagrat, friend/neutral = Swapna, enemy/debil = Supta."""
    from src.calculations.dignity import EXALT_SIGN, OWN_SIGNS, _NAISARGIKA

    # Own sign or exaltation
    if sign_index in OWN_SIGNS.get(planet, []):
        return JagradadiAvastha.JAGRAT
    if EXALT_SIGN.get(planet) == sign_index:
        return JagradadiAvastha.JAGRAT

    # Check relationship with sign lord
    lords = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
        4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
        8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
    }
    lord = lords.get(sign_index)
    if lord and lord != planet:
        rel = _NAISARGIKA.get((planet, lord), "Neutral")
        if rel == "Enemy":
            return JagradadiAvastha.SUPTA

    # Check debilitation
    from src.calculations.dignity import DEBIL_SIGN
    if DEBIL_SIGN.get(planet) == sign_index:
        return JagradadiAvastha.SUPTA

    return JagradadiAvastha.SWAPNA


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Lajjitadi Avasthas — BPHS Ch.45 v.11-18 (pp.451-452)
# ═══════════════════════════════════════════════════════════════════════════════

class LajjitadiAvastha(Enum):
    """Six states by planetary association."""
    LAJJITA = "Ashamed"       # 5th house + Sun/Saturn/Mars/node
    GARVITA = "Proud"         # exaltation or Moolatrikona
    KSHUDITA = "Hungry"       # enemy sign or conjunct/aspected by enemy
    TRUSHITA = "Thirsty"      # watery sign + enemy aspect, no benefic
    MUDITA = "Delighted"      # friendly sign + benefic conjunction/aspect
    KSHOBHITA = "Agitated"    # conjunct Sun + malefic aspect/conjunction


def compute_lajjitadi(planet: str, chart) -> LajjitadiAvastha | None:
    """BPHS Ch.45 v.11-18. Returns the applicable avastha or None."""
    from src.calculations.dignity import (
        EXALT_SIGN, DEBIL_SIGN, MOOLTRIKONA_RANGES, _NAISARGIKA,
    )

    if planet not in chart.planets:
        return None

    si = chart.planets[planet].sign_index
    deg = chart.planets[planet].degree_in_sign
    house = (si - chart.lagna_sign_index) % 12 + 1

    # Sign lord
    lords = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
        4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
        8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
    }
    lord = lords.get(si, "")
    rel = _NAISARGIKA.get((planet, lord), "Neutral") if lord != planet else "Friend"

    # Cotenants
    cotenants = [p for p, pos in chart.planets.items()
                 if p != planet and pos.sign_index == si]

    # Check Garvita first (exaltation or MT) — positive state
    if EXALT_SIGN.get(planet) == si:
        return LajjitadiAvastha.GARVITA
    if planet in MOOLTRIKONA_RANGES:
        mt_si, mt_s, mt_e = MOOLTRIKONA_RANGES[planet]
        if si == mt_si and mt_s <= deg < mt_e:
            return LajjitadiAvastha.GARVITA

    # Lajjita: in 5th house + associated with Sun/Saturn/Mars/Rahu/Ketu
    if house == 5:
        bad_assoc = {"Sun", "Saturn", "Mars", "Rahu", "Ketu"}
        if any(p in bad_assoc for p in cotenants):
            return LajjitadiAvastha.LAJJITA

    # Mudita: friendly sign + benefic conjunction/aspect or conjunct Jupiter
    if rel == "Friend" or lord == planet:
        benefics = {"Jupiter", "Venus", "Mercury", "Moon"}
        if any(p in benefics for p in cotenants) or "Jupiter" in cotenants:
            return LajjitadiAvastha.MUDITA

    # Kshudita: enemy sign or conjunct enemy or with Saturn
    if rel == "Enemy" or DEBIL_SIGN.get(planet) == si:
        return LajjitadiAvastha.KSHUDITA
    if "Saturn" in cotenants and rel != "Friend":
        return LajjitadiAvastha.KSHUDITA

    # Trushita: watery sign + enemy aspect, no benefic
    watery_signs = {3, 7, 11}  # Cancer, Scorpio, Pisces
    if si in watery_signs:
        benefics = {"Jupiter", "Venus", "Mercury", "Moon"}
        has_benefic = any(p in benefics for p in cotenants)
        if not has_benefic:
            return LajjitadiAvastha.TRUSHITA

    # Kshobhita: conjunct Sun + malefic aspect/conjunction
    if "Sun" in cotenants:
        malefics = {"Mars", "Saturn", "Rahu", "Ketu"}
        if any(p in malefics for p in cotenants):
            return LajjitadiAvastha.KSHOBHITA

    return None  # no specific Lajjitadi triggered


# ═══════════════════════════════════════════════════════════════════════════════
# Combined Avastha Result
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Sayanadi Avasthas — BPHS Ch.45 v.30-37 (pp.454-456)
# ═══════════════════════════════════════════════════════════════════════════════

class SayandiAvastha(Enum):
    """12 states computed by formula. BPHS Ch.45 v.30-37."""
    SAYANA = "Lying Down"
    UPAVESANA = "Sitting"
    NETRAPANI = "Hands on Eyes"
    PRAKASANA = "Shining"
    GAMANA = "Going"
    AAGAMANA = "Coming"
    SABHA = "In Assembly"
    AGAMA = "Approaching"
    BHOJANA = "Eating"
    NRITYALIPSA = "Dancing"
    KAUTUKA = "Curious"
    NIDRA = "Sleeping"


# Planet multipliers for Sayanadi — BPHS Ch.45 v.30 (p.454)
_SAYANADI_PLANET_MULT: dict[str, int] = {
    "Sun": 5, "Moon": 2, "Mars": 2, "Mercury": 3,
    "Jupiter": 5, "Venus": 3, "Saturn": 3, "Rahu": 4, "Ketu": 4,
}

# Planet additaments for sub-state — v.30 (p.454)
_SAYANADI_PLANET_ADD: dict[str, int] = {
    "Sun": 5, "Moon": 2, "Mars": 2, "Mercury": 3,
    "Jupiter": 5, "Venus": 3, "Saturn": 3, "Rahu": 4, "Ketu": 4,
}

_SAYANADI_ORDER = list(SayandiAvastha)


def compute_sayanadi(
    planet: str, chart, birth_ghatis: float = 0.0,
) -> SayandiAvastha | None:
    """BPHS Ch.45 v.30-37: Sayanadi avastha from formula.

    Formula: ((s × p × n) + (a + g + r)) mod 12 = avastha index
    Where: s = planet's nakshatra (1-27), p = planet multiplier,
           n = navamsa (1-9), a = birth nakshatra, g = birth ghatis,
           r = lagna sign count from Aries + 1.

    Note: sub-state computation (v.36, p.456) requires native's name
    first syllable — not implementable without user input.
    """
    if planet not in chart.planets or planet not in _SAYANADI_PLANET_MULT:
        return None

    pos = chart.planets[planet]
    lon = pos.longitude

    # s: nakshatra number (1-27) from planet's longitude
    s = int(lon / (360 / 27)) + 1  # 13°20' per nakshatra

    # p: planet multiplier
    p = _SAYANADI_PLANET_MULT[planet]

    # n: navamsa position (1-9)
    try:
        from src.calculations.vargas import compute_varga_sign
        d9_si = compute_varga_sign(lon, 9)
        n = (d9_si % 9) + 1  # 1-9 within the navamsa cycle
    except Exception:
        n = int((lon % 30) / 3.333) + 1  # fallback

    # a: birth nakshatra (Moon's nakshatra)
    moon = chart.planets.get("Moon")
    a = int(moon.longitude / (360 / 27)) + 1 if moon else 1

    # g: birth ghatis (from midnight)
    g = int(birth_ghatis)

    # r: signs from Aries to ascendant + 1
    r = chart.lagna_sign_index + 1

    # Avastha = ((s × p × n) + (a + g + r)) mod 12
    total = (s * p * n) + (a + g + r)
    idx = total % 12

    return _SAYANADI_ORDER[idx]


@dataclass
class AvasthaSummary:
    planet: str
    baaladi: BaaladiAvastha
    baaladi_effect: float  # 0.0 to 1.0
    jagradadi: JagradadiAvastha
    jagradadi_effect: float  # 0.0 to 1.0
    combined_effect: float  # baaladi × jagradadi (Ch.45 v.6)
    lajjitadi: LajjitadiAvastha | None
    sayanadi: SayandiAvastha | None = None


def compute_avasthas(planet: str, chart, birth_ghatis: float = 0.0) -> AvasthaSummary:
    """Compute all avastha states for a planet."""
    if planet not in chart.planets:
        return AvasthaSummary(
            planet=planet,
            baaladi=BaaladiAvastha.YUVA,
            baaladi_effect=1.0,
            jagradadi=JagradadiAvastha.SWAPNA,
            jagradadi_effect=0.5,
            combined_effect=0.5,
            lajjitadi=None,
        )

    si = chart.planets[planet].sign_index
    deg = chart.planets[planet].degree_in_sign

    baaladi = compute_baaladi(si, deg)
    jagradadi = compute_jagradadi(planet, si)
    lajjitadi = compute_lajjitadi(planet, chart)
    sayanadi = compute_sayanadi(planet, chart, birth_ghatis)

    b_eff = BAALADI_EFFECT[baaladi]
    j_eff = JAGRADADI_EFFECT[jagradadi]

    return AvasthaSummary(
        planet=planet,
        baaladi=baaladi,
        baaladi_effect=b_eff,
        jagradadi=jagradadi,
        jagradadi_effect=j_eff,
        combined_effect=round(b_eff * j_eff, 4),
        lajjitadi=lajjitadi,
        sayanadi=sayanadi,
    )
