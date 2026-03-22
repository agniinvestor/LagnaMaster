"""
src/calculations/upapada_lagna.py — Session 104

Upapada Lagna (UL) — the Arudha of the 12th house.
Source: PVRNR Ch.9 p97-104; B.V. Raman "How to Judge a Horoscope".

UL = Count as many signs from the 12th lord as the 12th lord is from the 12th house.
     Exception: if UL falls in 1st or 7th from AL, shift by 10 signs.

UL signifies: marriage, spouse's quality, the public perception of one's marriage.

Key interpretive rules (PVRNR p102-104):
  UL lord in kendra/trikona = good marriage prospects
  UL lord in dusthana = challenges in marriage
  2nd from UL = sustenance of marriage (benefics = lasting, malefics = problematic)
  Malefics in 2nd from UL = separation/divorce tendency

Additional rules:
  Saturn in 2nd from UL = strong maraka effect on marriage
  Jupiter in UL or 2nd from UL = protective, good marriage
  Rahu/Ketu in UL = unusual/unconventional relationship patterns
"""

from __future__ import annotations
from dataclasses import dataclass

_SIGN_NAMES = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]
_DUSTHANA = {6, 8, 12}
_KENDRA_TRIKONA = {1, 4, 5, 7, 9, 10}
_NAT_BENEF = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEF = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


@dataclass
class UpapadaAnalysis:
    ul_sign: str
    ul_sign_index: int
    ul_house: int  # UL from Lagna
    ul_lord: str
    ul_lord_house: int
    ul_lord_strong: bool  # in kendra/trikona
    second_from_ul_sign: str
    second_from_ul_planets: list[str]
    second_from_ul_benefics: list[str]
    second_from_ul_malefics: list[str]
    marriage_quality: str  # "Favourable"/"Mixed"/"Challenging"
    marriage_longevity: str  # "Lasting"/"Possible challenges"/"Separation risk"
    notes: list[str]


def compute_upapada(chart) -> UpapadaAnalysis:
    """Compute Upapada Lagna and its analysis."""
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    lagna_si = chart.lagna_sign_index

    # 12th house sign
    twelfth_si = (lagna_si + 11) % 12
    twelfth_lord = hmap.house_lord[11]
    lord_pos = chart.planets.get(twelfth_lord)

    if lord_pos is None:
        # Fallback
        ul_si = (twelfth_si + 11) % 12
    else:
        lord_si = lord_pos.sign_index
        # Count from 12th house to 12th lord
        count = (lord_si - twelfth_si) % 12 + 1
        # UL = count same distance from 12th lord
        ul_si = (lord_si + count - 1) % 12

    # Exception: if UL is 1st or 7th from Lagna, add 10
    ul_from_lagna = (ul_si - lagna_si) % 12 + 1
    if ul_from_lagna in {1, 7}:
        ul_si = (ul_si + 9) % 12
        ul_from_lagna = (ul_si - lagna_si) % 12 + 1

    ul_lord = hmap.house_lord[(ul_si - lagna_si) % 12]
    ul_lord_house = ph.get(ul_lord, 0)
    ul_lord_strong = ul_lord_house in _KENDRA_TRIKONA

    # 2nd from UL
    second_ul_si = (ul_si + 1) % 12
    second_ul_sign = _SIGN_NAMES[second_ul_si]
    second_house = (second_ul_si - lagna_si) % 12 + 1
    planets_2nd = [p for p, h in ph.items() if h == second_house]
    bens_2nd = [p for p in planets_2nd if p in _NAT_BENEF]
    mals_2nd = [p for p in planets_2nd if p in _NAT_MALEF]

    notes = []
    if "Jupiter" in planets_2nd or "Jupiter" in [
        p for p, h in ph.items() if h == ul_from_lagna
    ]:
        notes.append("Jupiter's influence on UL — protective, expansive marriage")
    if "Saturn" in mals_2nd:
        notes.append(
            "Saturn in 2nd from UL — maraka effect, challenges to marriage longevity"
        )
    if "Rahu" in [p for p, h in ph.items() if h == ul_from_lagna]:
        notes.append("Rahu in UL — unconventional relationship patterns")

    # Marriage quality
    if ul_lord_strong and not mals_2nd:
        quality = "Favourable"
    elif not ul_lord_strong and mals_2nd:
        quality = "Challenging"
    else:
        quality = "Mixed"

    # Longevity
    if len(mals_2nd) >= 2 or "Saturn" in mals_2nd:
        longevity = "Separation risk — 2nd from UL has serious malefics"
    elif bens_2nd and not mals_2nd:
        longevity = "Lasting — benefics sustain the 2nd from UL"
    else:
        longevity = "Possible challenges — mixed signals in 2nd from UL"

    return UpapadaAnalysis(
        ul_sign=_SIGN_NAMES[ul_si],
        ul_sign_index=ul_si,
        ul_house=ul_from_lagna,
        ul_lord=ul_lord,
        ul_lord_house=ul_lord_house,
        ul_lord_strong=ul_lord_strong,
        second_from_ul_sign=second_ul_sign,
        second_from_ul_planets=planets_2nd,
        second_from_ul_benefics=bens_2nd,
        second_from_ul_malefics=mals_2nd,
        marriage_quality=quality,
        marriage_longevity=longevity,
        notes=notes,
    )
