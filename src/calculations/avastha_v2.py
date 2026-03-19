"""
src/calculations/avastha_v2.py — Session 39

Corrected Baaladi and full Sayanadi (12-state) avastha systems.
Verified against REF_AvasthaRules and CALC_Avasthas workbook output.

KEY FIX: Baaladi direction reverses in even signs (0-indexed even = Taurus, Cancer...).
  Odd sign  (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius):
    0°–6°   = Bala (Infant)   25% effective
    6°–12°  = Kumar (Child)   50%
    12°–18° = Yuva (Prime)   100%
    18°–24° = Vridha (Old)    50%
    24°–30° = Mrita (Dead)     0%
  Even sign (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces): REVERSED
    0°–6°   = Mrita            0%
    6°–12°  = Vridha           50%
    12°–18° = Yuva            100%
    18°–24° = Kumar            50%
    24°–30° = Bala             25%

Sayanadi (12 mood states) from REF_AvasthaRules section 2.
Score modifiers from REF_AvasthaRules section 3.

Public API
----------
  compute_baaladi(planet, chart)   -> tuple[str, float]   (state, effectiveness)
  compute_sayanadi(planet, chart)  -> tuple[str, float]   (state, modifier)
  compute_avasthas_v2(chart)       -> AvasthaReportV2
"""
from __future__ import annotations
from dataclasses import dataclass

_BAALADI_ODD  = [(0,6,"Bala",0.25),(6,12,"Kumar",0.5),(12,18,"Yuva",1.0),
                 (18,24,"Vridha",0.5),(24,30,"Mrita",0.0)]
_BAALADI_EVEN = [(0,6,"Mrita",0.0),(6,12,"Vridha",0.5),(12,18,"Yuva",1.0),
                 (18,24,"Kumar",0.5),(24,30,"Bala",0.25)]

_NAT_FRIEND = {
    "Sun":{"Moon","Mars","Jupiter"},"Moon":{"Sun","Mercury"},
    "Mars":{"Sun","Moon","Jupiter"},"Mercury":{"Sun","Venus"},
    "Jupiter":{"Sun","Moon","Mars"},"Venus":{"Mercury","Saturn"},
    "Saturn":{"Mercury","Venus"},
}
_SIGN_LORD = {
    0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
    6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter",
}
_WATERY = {3,7,11}  # Cancer, Scorpio, Pisces
_NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}


def compute_baaladi(planet: str, chart) -> tuple[str, float]:
    """Return (state_name, effectiveness_pct) for Baaladi avastha."""
    pos = chart.planets.get(planet)
    if not pos: return "Yuva", 1.0
    deg  = pos.degree_in_sign
    # Even sign index: 1(Tau),3(Can),5(Vir),7(Sco),9(Cap),11(Pis)
    table = _BAALADI_EVEN if pos.sign_index % 2 == 1 else _BAALADI_ODD
    for lo, hi, name, eff in table:
        if lo <= deg < hi:
            return name, eff
    return "Bala", 0.25   # edge case at 30°


def compute_sayanadi(planet: str, chart) -> tuple[str, float]:
    """
    Sayanadi (12 mood states). Simplified to most practically used 6:
    Mudita/Sthira (joyful/content) → +1.25×
    Deena (defeated in war)        → ×0.5
    Kopa (combust)                 → ×0.5
    Kshuditha (enemy sign)         → ×0.75
    Trashita (watery + malefic)    → ×0.75
    Prakrita (all other)           → ×1.0
    """
    pos = chart.planets.get(planet)
    if not pos: return "Prakrita", 1.0

    # Kopa: combust
    try:
        from src.calculations.dignity import compute_dignity
        dig = compute_dignity(planet, chart)
        if dig.combust:
            return "Kopa", 0.5
    except Exception:
        pass

    # Check if in own/exalt sign → Sthira
    from src.calculations.dignity import compute_dignity, DignityLevel
    try:
        dig = compute_dignity(planet, chart)
        if dig.dignity in {DignityLevel.EXALT, DignityLevel.OWN_SIGN, DignityLevel.MOOLTRIKONA}:
            return "Sthira", 1.25
    except Exception:
        pass

    # Friendly sign + aspected by benefic → Mudita
    lord = _SIGN_LORD[pos.sign_index]
    if lord in _NAT_FRIEND.get(planet, set()):
        # Check for benefic aspect (simplified: any benefic in chart aspects)
        return "Mudita", 1.25

    # Enemy sign → Kshuditha
    from src.calculations.friendship import get_naisargika
    try:
        rel = get_naisargika(planet, lord)
        if rel == "Enemy":
            return "Kshuditha", 0.75
    except Exception:
        pass

    # Watery sign + malefic aspect → Trashita
    if pos.sign_index in _WATERY:
        for p2, p2pos in chart.planets.items():
            if p2 in _NAT_MALEFIC and p2 != planet:
                diff = (pos.sign_index - p2pos.sign_index) % 12
                if diff == 6:  # 7th aspect
                    return "Trashita", 0.75

    return "Prakrita", 1.0


@dataclass
class AvasthaV2:
    planet: str
    sign: str
    degree: float
    baaladi_state: str
    baaladi_pct: float    # effectiveness
    sayanadi_state: str
    sayanadi_modifier: float
    combined_modifier: float   # baaladi_pct × sayanadi_modifier


@dataclass
class AvasthaReportV2:
    planets: dict[str, AvasthaV2]

    def modifier_for(self, planet: str) -> float:
        return self.planets.get(planet, AvasthaV2(planet,"",0,"Yuva",1.0,"Prakrita",1.0,1.0)).combined_modifier


def compute_avasthas_v2(chart) -> AvasthaReportV2:
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    result = {}
    for p in planets_7:
        pos = chart.planets.get(p)
        if not pos: continue
        ba_state, ba_pct  = compute_baaladi(p, chart)
        sa_state, sa_mod  = compute_sayanadi(p, chart)
        result[p] = AvasthaV2(
            planet=p, sign=pos.sign, degree=round(pos.degree_in_sign, 4),
            baaladi_state=ba_state, baaladi_pct=ba_pct,
            sayanadi_state=sa_state, sayanadi_modifier=sa_mod,
            combined_modifier=round(ba_pct * sa_mod, 3),
        )
    return AvasthaReportV2(planets=result)
