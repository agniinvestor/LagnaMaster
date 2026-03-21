"""
src/calculations/functional_roles.py — LagnaMaster Session 28

Per-lagna functional role matrix: the most critical and most commonly
under-modeled layer in Jyotish engines.

Every planet's benefic/malefic status is LAGNA-SPECIFIC, not universal.
Venus is universally benefic, but for Gemini lagna it rules H12 (dusthana)
making it functionally malefic. Saturn rules H9+H10 for Taurus lagna
making it a powerful Yogakaraka.

Computes for any lagna:
  - Functional benefics / neutrals / malefics (per BPHS Ch.34)
  - Yogakaraka planets (kendra+trikona dual rulership)
  - Badhaka house, sign and lord
  - Maraka lords (H2 and H7 lords)
  - Kendradhipati dosha (benefics weakened by owning kendras)
  - Dusthana lords (H6, H8, H12)
  - Trik lords (same as dusthana — H6/H8/H12)

Public API
----------
    compute_functional_roles(chart) -> FunctionalRoles
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# Sign lord map (0=Aries … 11=Pisces)
_SIGN_LORD = {
    0: "Mars",   1: "Venus",   2: "Mercury", 3: "Moon",
    4: "Sun",    5: "Mercury", 6: "Venus",   7: "Mars",
    8: "Jupiter",9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# Natural benefics and malefics
_NAT_BENEFIC  = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC  = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

# Badhaka house by lagna sign type
# Moveable (0,3,6,9): H11  Fixed (1,4,7,10): H9  Dual (2,5,8,11): H7
def _badhaka_house(lagna_si: int) -> int:
    if lagna_si in {0, 3, 6, 9}:  return 11   # moveable
    if lagna_si in {1, 4, 7, 10}: return 9    # fixed
    return 7                                    # dual


@dataclass
class FunctionalRoles:
    lagna_sign: str
    lagna_sign_index: int

    # Per-planet functional classification
    functional_benefics: list[str]  = field(default_factory=list)
    functional_malefics: list[str]  = field(default_factory=list)
    functional_neutrals: list[str]  = field(default_factory=list)

    # Special roles
    yogakaraka: Optional[str]       = None      # single strongest yogakaraka
    yogakarakas: list[str]          = field(default_factory=list)  # all
    maraka_lords: list[str]         = field(default_factory=list)  # H2, H7 lords
    dusthana_lords: list[str]       = field(default_factory=list)  # H6/H8/H12 lords
    kendradhipati_planets: list[str]= field(default_factory=list)  # nat. benefics with kendradhipati dosha

    # Badhaka
    badhaka_house: int              = 0
    badhaka_sign_index: int         = 0
    badhaka_sign: str               = ""
    badhaka_lord: str               = ""

    # House-lord lookup (1-indexed, house -> lord)
    house_lords: dict[int, str]     = field(default_factory=dict)

    def is_functional_benefic(self, planet: str) -> bool:
        return planet in self.functional_benefics

    def is_functional_malefic(self, planet: str) -> bool:
        return planet in self.functional_malefics

    def is_yogakaraka(self, planet: str) -> bool:
        return planet in self.yogakarakas

    def is_maraka(self, planet: str) -> bool:
        return planet in self.maraka_lords


_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]


def compute_functional_roles(chart) -> FunctionalRoles:
    """Compute the complete functional role matrix for the chart's lagna."""
    lsi = chart.lagna_sign_index

    # Build house-lord map (whole-sign)
    house_lords = {}
    for h in range(1, 13):
        sign_idx = (lsi + h - 1) % 12
        house_lords[h] = _SIGN_LORD[sign_idx]

    roles = FunctionalRoles(
        lagna_sign=chart.lagna_sign,
        lagna_sign_index=lsi,
        house_lords=house_lords,
    )

    # Dusthana lords (H6, H8, H12)
    roles.dusthana_lords = list({house_lords[6], house_lords[8], house_lords[12]})

    # Maraka lords (H2, H7)
    roles.maraka_lords = list({house_lords[2], house_lords[7]})

    # Yogakaraka: planet that simultaneously rules a kendra AND a trikona
    # (H1 counts as both; exclude H1-only lords)
    kendra_lords  = {house_lords[h] for h in [1, 4, 7, 10]}
    trikona_lords = {house_lords[h] for h in [1, 5, 9]}
    yk_set = (kendra_lords & trikona_lords) - {house_lords[1]}  # H1 excluded (always both)
    roles.yogakarakas = sorted(yk_set)
    roles.yogakaraka  = roles.yogakarakas[0] if len(roles.yogakarakas) == 1 else None

    # Kendradhipati dosha: natural benefics owning kendras (H4, H7, H10)
    # H1 lordship does not give KD dosha; H4/H7/H10 do for natural benefics
    kd_candidates = {house_lords[h] for h in [4, 7, 10]}
    roles.kendradhipati_planets = [p for p in kd_candidates if p in _NAT_BENEFIC]

    # Functional classification per planet (7 grahas)
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    for planet in planets_7:
        owned = [h for h, lord in house_lords.items() if lord == planet]
        dusthana_owned = [h for h in owned if h in {6, 8, 12}]
        kendra_owned   = [h for h in owned if h in {1, 4, 7, 10}]
        trikona_owned  = [h for h in owned if h in {1, 5, 9}]
        [h for h in owned if h in {3, 6, 10, 11}]

        # Yogakaraka — strongly benefic
        if planet in roles.yogakarakas:
            roles.functional_benefics.append(planet)
            continue

        # Primary dusthana lord (owns ONLY dusthanas) — malefic
        if dusthana_owned and not (set(owned) - {6, 8, 12}):
            roles.functional_malefics.append(planet)
            continue

        # Trikona lord (H5 or H9) without dusthana — benefic
        if any(h in {5, 9} for h in trikona_owned) and not dusthana_owned:
            roles.functional_benefics.append(planet)
            continue

        # Pure kendra lord (no trikona) — KD dosha for nat benefics
        if kendra_owned and not trikona_owned and not dusthana_owned:
            if planet in _NAT_BENEFIC:
                roles.functional_neutrals.append(planet)  # KD weakens but not malefic
            else:
                roles.functional_neutrals.append(planet)
            continue

        # Mixed ownership including dusthana — generally malefic
        if dusthana_owned:
            roles.functional_malefics.append(planet)
            continue

        # Default to natural classification
        if planet in _NAT_BENEFIC:
            roles.functional_benefics.append(planet)
        else:
            roles.functional_malefics.append(planet)

    # Badhaka
    bh = _badhaka_house(lsi)
    bsi = (lsi + bh - 1) % 12
    roles.badhaka_house       = bh
    roles.badhaka_sign_index  = bsi
    roles.badhaka_sign        = _SIGNS[bsi]
    roles.badhaka_lord        = _SIGN_LORD[bsi]

    return roles
