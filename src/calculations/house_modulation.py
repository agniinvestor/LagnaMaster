"""
src/calculations/house_modulation.py — Session 68

House-type modulation — houses behave differently by type (GAP 5+6).

Classical doctrine:
  UPACHAYAS (3,6,10,11): improve with age/time; malefics do WELL here
    (BPHS: malefics in 3rd/6th = overcomes enemies)
  KENDRAS (1,4,7,10): stabilizing houses — strength is stable over time
  TRIKONAS (1,5,9): benefic promise — benefics here give lasting results
  DUSTHANAS (6,8,12): challenging — but 8th shows longevity potential,
    12th shows moksha/losses; Viparita if lords exchange
  MARAKAS (2,7): maraka potential must be considered for longevity

Age/time modifier for upachayas:
  Young (0-35 yrs): upachaya at 50% potential
  Middle (35-60 yrs): 80%
  Elder (60+): full 100% (upachayas mature fully)

Public API
----------
  house_type_modifier(house, chart, age_years) -> HouseModulation
  apply_house_modulation(scores, chart, age_years) -> dict[int, float]
"""
from __future__ import annotations
from dataclasses import dataclass

_UPACHAYA  = {3, 6, 10, 11}
_KENDRA    = {1, 4, 7, 10}
_TRIKONA   = {1, 5, 9}
_DUSTHANA  = {6, 8, 12}
_MARAKA    = {2, 7}
_NAT_MALEF = {"Sun","Mars","Saturn","Rahu","Ketu"}
_NAT_BENEF = {"Jupiter","Venus","Mercury","Moon"}


@dataclass
class HouseModulation:
    house: int
    house_type: str           # "Upachaya"/"Kendra"/"Trikona"/"Dusthana"/"Maraka"/"Neutral"
    malefic_beneficial: bool  # malefics are beneficial in this house type
    age_modifier: float       # 0.5–1.0 for upachayas; 1.0 for others
    time_improves: bool       # True for upachayas
    modulated_score: float
    raw_score: float
    commentary: str


def house_type_modifier(house: int, chart, age_years: float = 35.0,
                        raw_score: float = 0.0) -> HouseModulation:
    """Apply house-type modulation to a score."""
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    # Determine house type
    if house in _UPACHAYA:
        htype = "Upachaya"
    elif house in _KENDRA:
        htype = "Kendra"
    elif house in _TRIKONA - {1}:
        htype = "Trikona"
    elif house in _DUSTHANA:
        htype = "Dusthana"
    elif house in _MARAKA:
        htype = "Maraka"
    else:
        htype = "Neutral"

    # Age modifier for upachayas
    if htype == "Upachaya":
        if age_years < 35:
            age_mod = 0.5 + 0.3 * (age_years / 35)
        elif age_years < 60:
            age_mod = 0.8 + 0.2 * ((age_years - 35) / 25)
        else:
            age_mod = 1.0
        time_improves = True
    else:
        age_mod = 1.0
        time_improves = False

    # Malefics in 3/6/11 are actually beneficial (BPHS)
    in_house = [p for p, h in ph.items() if h == house]
    house_malefics = [p for p in in_house if p in _NAT_MALEF]
    malefic_beneficial = house in {3, 6, 11} and bool(house_malefics)

    # Modulated score
    if htype == "Upachaya":
        # Upachaya: malefics add to score (they improve outcomes here)
        malefic_bonus = len(house_malefics) * 0.5 if malefic_beneficial else 0
        modulated = round((raw_score + malefic_bonus) * age_mod, 3)
    elif htype == "Dusthana":
        # Dusthanas: slightly dampen positive scores (unless Viparita)
        modulated = round(raw_score * 0.9, 3)
    else:
        modulated = round(raw_score * age_mod, 3)

    # Commentary
    parts = [f"H{house} ({htype})"]
    if time_improves:
        parts.append(f"age modifier {age_mod:.2f} (matures with time)")
    if malefic_beneficial:
        parts.append(f"malefics {house_malefics} beneficial here")
    commentary = "; ".join(parts)

    return HouseModulation(
        house=house, house_type=htype,
        malefic_beneficial=malefic_beneficial,
        age_modifier=round(age_mod, 3),
        time_improves=time_improves,
        modulated_score=modulated,
        raw_score=raw_score,
        commentary=commentary,
    )


def apply_house_modulation(scores: dict[int, float], chart,
                            age_years: float = 35.0) -> dict[int, float]:
    """Apply house-type modulation to all 12 house scores."""
    return {h: house_type_modifier(h, chart, age_years, scores.get(h, 0.0)).modulated_score
            for h in range(1, 13)}
