"""
src/calculations/functional_dignity.py
Functional benefic/malefic classification by Lagna + Badhakesh + Yogakaraka.
Session 137.

Natural (Naisargika) classification is useful for Drik Bala.
Functional (Tatkaliika) classification by Lagna is required for:
  - Scoring rule R02/R09 (benefic/malefic in house)
  - Drik Bala (functional benefic aspect = positive)
  - Yoga detection (functional vs natural Kendra/Trikona lords)
  - Upachaya interpretation

Sources:
  V.K. Choudhry · Systems Approach for Interpreting Horoscopes Ch.3
  PVRNR · BPHS Ch.34 (Yogakaraka)
  Mantreswara · Phaladeepika Ch.3 v.5-12
  Traditional: BPHS Ch.37 (Badhaka)
"""
from __future__ import annotations
from dataclasses import dataclass

_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
    5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
    9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

_KENDRA  = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_UPACHAYA = {3, 6, 10, 11}

# Movable/Fixed/Dual Lagnas for Badhaka
_MOVABLE_LAGNAS = {0, 3, 6, 9}   # Aries, Cancer, Libra, Capricorn
_FIXED_LAGNAS   = {1, 4, 7, 10}  # Taurus, Leo, Scorpio, Aquarius
_DUAL_LAGNAS    = {2, 5, 8, 11}  # Gemini, Virgo, Sag, Pisces


def _house_lords(lagna_si: int) -> dict[int, str]:
    """Map {house_number: lord} for a given Lagna sign."""
    return {h: _SIGN_LORDS[(lagna_si + h - 1) % 12] for h in range(1, 13)}


def _houses_ruled_by(planet: str, lagna_si: int) -> list[int]:
    """List of house numbers ruled by a planet for a given Lagna."""
    houses = []
    for h in range(1, 13):
        sign = (lagna_si + h - 1) % 12
        if _SIGN_LORDS[sign] == planet:
            houses.append(h)
    return houses


@dataclass
class FunctionalClassification:
    planet: str
    houses_ruled: list[int]          # 1-12
    is_functional_benefic: bool
    is_functional_malefic: bool
    is_yogakaraka: bool              # rules both Kendra AND Trikona
    is_maraka: bool                  # rules H2 or H7 (death-inflicting)
    is_badhaka: bool                 # is the Badhaka lord
    classification: str              # 'benefic' / 'malefic' / 'neutral' / 'yogakaraka'
    note: str                        # brief explanation


def compute_functional_classifications(lagna_sign_index: int) -> dict[str, FunctionalClassification]:
    """
    Compute functional benefic/malefic for all planets given a Lagna.
    Source: V.K. Choudhry Systems Approach Ch.3; PVRNR BPHS Ch.34
    """
    lagna_si = lagna_sign_index % 12
    badhaka_lord = _get_badhaka_lord(lagna_si)
    results = {}

    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    for planet in planets:
        houses = _houses_ruled_by(planet, lagna_si)
        if not houses:
            results[planet] = FunctionalClassification(
                planet=planet, houses_ruled=[], is_functional_benefic=False,
                is_functional_malefic=False, is_yogakaraka=False,
                is_maraka=False, is_badhaka=False, classification='neutral', note='No house ruled'
            )
            continue

        rules_kendra  = any(h in _KENDRA  for h in houses)
        rules_trikona = any(h in _TRIKONA for h in houses)
        rules_dusthana = any(h in _DUSTHANA for h in houses)
        rules_maraka  = any(h in {2, 7}   for h in houses)
        is_badhaka    = (planet == badhaka_lord)

        # Yogakaraka: rules BOTH a Kendra AND a Trikona (most powerful benefic)
        is_yogakaraka = rules_kendra and rules_trikona

        # Functional benefic: Trikona lord (H1/H5/H9) or Yogakaraka
        # Note: H1 lord is simultaneously Kendra+Trikona → always benefic
        is_functional_benefic = (
            rules_trikona and not (rules_dusthana and not rules_trikona)
        )

        # Functional malefic: rules only Kendra without Trikona, or rules dusthana only
        # H1 lord is exception — always benefic regardless
        is_functional_malefic = (
            (rules_dusthana and not rules_trikona) or
            (rules_kendra and not rules_trikona and not rules_dusthana and 1 not in houses)
        )

        # Exceptions
        if 1 in houses:  # Lagna lord is always functionally benefic
            is_functional_benefic = True
            is_functional_malefic = False

        if is_yogakaraka:
            is_functional_malefic = False  # Yogakaraka overrides malefic tendency

        if is_badhaka and not rules_trikona:
            is_functional_malefic = True

        # Determine classification string
        if is_yogakaraka:
            classification = 'yogakaraka'
        elif is_functional_benefic and not is_functional_malefic:
            classification = 'benefic'
        elif is_functional_malefic and not is_functional_benefic:
            classification = 'malefic'
        else:
            classification = 'neutral'

        note = f"Rules H{','.join(str(h) for h in houses)}"
        if is_yogakaraka: note += " — Yogakaraka"
        if is_badhaka: note += " — Badhaka lord"
        if rules_maraka: note += " — Maraka"

        results[planet] = FunctionalClassification(
            planet=planet,
            houses_ruled=houses,
            is_functional_benefic=is_functional_benefic,
            is_functional_malefic=is_functional_malefic,
            is_yogakaraka=is_yogakaraka,
            is_maraka=rules_maraka,
            is_badhaka=is_badhaka,
            classification=classification,
            note=note,
        )

    # Rahu and Ketu: adopt the characteristics of their sign lords
    for node in ["Rahu", "Ketu"]:
        results[node] = FunctionalClassification(
            planet=node, houses_ruled=[], is_functional_benefic=False,
            is_functional_malefic=True, is_yogakaraka=False,
            is_maraka=False, is_badhaka=False, classification='malefic',
            note='Nodes adopt their sign lord\'s nature'
        )

    return results


def _get_badhaka_lord(lagna_si: int) -> str:
    """
    Returns the Badhaka lord for a given Lagna.
    Movable Lagnas: H11 lord is Badhaka
    Fixed Lagnas: H9 lord is Badhaka
    Dual Lagnas: H7 lord is Badhaka
    Source: PVRNR · BPHS Ch.37; Sanjay Rath · Crux Ch.9
    """
    if lagna_si in _MOVABLE_LAGNAS:
        badhaka_house = 11
    elif lagna_si in _FIXED_LAGNAS:
        badhaka_house = 9
    else:
        badhaka_house = 7
    badhaka_sign = (lagna_si + badhaka_house - 1) % 12
    return _SIGN_LORDS[badhaka_sign]


def badhakesh(lagna_sign_index: int) -> str:
    """Returns the Badhaka lord planet name for a Lagna sign."""
    return _get_badhaka_lord(lagna_sign_index % 12)


def yogakaraka(lagna_sign_index: int) -> list[str]:
    """
    Returns list of Yogakaraka planets for a Lagna.
    Yogakaraka: simultaneously rules a Kendra AND a Trikona.
    Source: PVRNR · BPHS Ch.34
    """
    fc = compute_functional_classifications(lagna_sign_index)
    return [p for p, r in fc.items() if r.is_yogakaraka]


# ─── Precomputed tables for common use ────────────────────────────────────────

# Classic Yogakarakas by Lagna
KNOWN_YOGAKARAKAS: dict[int, list[str]] = {
    0:  ["Sun"],           # Aries: Sun (H5 lord = Trikona; H4 Kendra via rulership)
    1:  ["Saturn"],        # Taurus: Saturn rules H9+H10
    2:  [],                # Gemini: no single Yogakaraka
    3:  ["Mars"],          # Cancer: Mars rules H5+H10
    4:  ["Mars"],          # Leo: Mars rules H4+H9
    5:  ["Venus"],         # Virgo: Venus rules H2+H9... (partial)
    6:  ["Saturn"],        # Libra: Saturn rules H4+H5
    7:  ["Jupiter"],       # Scorpio: Jupiter rules H2+H5
    8:  [],                # Sagittarius: no clear Yogakaraka
    9:  ["Venus"],         # Capricorn: Venus rules H5+H10
    10: ["Venus"],         # Aquarius: Venus rules H4+H9
    11: [],                # Pisces: Mars partial (H2+H9)
}

# Functional malefic by Lagna (traditional summary)
KNOWN_FUNCTIONAL_MALEFICS: dict[int, list[str]] = {
    0: ["Mercury", "Saturn", "Rahu", "Ketu"],
    1: ["Jupiter", "Moon", "Rahu", "Ketu"],
    2: ["Mars", "Jupiter", "Rahu", "Ketu"],
    3: ["Jupiter", "Saturn", "Mercury", "Rahu", "Ketu"],
    4: ["Mercury", "Venus", "Saturn", "Rahu", "Ketu"],
    5: ["Mars", "Jupiter", "Moon", "Rahu", "Ketu"],
    6: ["Jupiter", "Mercury", "Rahu", "Ketu"],
    7: ["Venus", "Mercury", "Rahu", "Ketu"],
    8: ["Venus", "Saturn", "Rahu", "Ketu"],
    9: ["Mars", "Jupiter", "Moon", "Rahu", "Ketu"],
    10: ["Jupiter", "Moon", "Mars", "Rahu", "Ketu"],
    11: ["Saturn", "Venus", "Sun", "Rahu", "Ketu"],
}
