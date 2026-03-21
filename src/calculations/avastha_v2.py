"""
src/calculations/avastha_v2.py — Session 39 (fixed)
Corrected Baaladi (even-sign reversal) and Sayanadi avastha systems.
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
_NAT_ENEMY = {
    "Sun":   {"Venus","Saturn"},
    "Moon":  set(),
    "Mars":  {"Mercury"},
    "Mercury":{"Moon"},
    "Jupiter":{"Mercury","Venus"},
    "Venus": {"Sun","Moon"},
    "Saturn":{"Sun","Moon","Mars"},
}
_SIGN_LORD = {
    0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
    6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter",
}
_WATERY = {3,7,11}
_NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}


def compute_baaladi(planet: str, chart) -> tuple[str, float]:
    pos = chart.planets.get(planet)
    if not pos:
        return "Yuva", 1.0
    deg = pos.degree_in_sign
    table = _BAALADI_EVEN if pos.sign_index % 2 == 1 else _BAALADI_ODD
    for lo, hi, name, eff in table:
        if lo <= deg < hi:
            return name, eff
    return "Bala", 0.25


def compute_sayanadi(planet: str, chart) -> tuple[str, float]:
    pos = chart.planets.get(planet)
    if not pos:
        return "Prakrita", 1.0

    # Kopa: combust
    try:
        from src.calculations.dignity import compute_all_dignities, DignityLevel
        dig = compute_all_dignities(chart).get(planet)
        if dig and dig.combust:
            return "Kopa", 0.5
        if dig and dig.dignity in {DignityLevel.EXALT, DignityLevel.OWN_SIGN, DignityLevel.MOOLTRIKONA}:
            return "Sthira", 1.25
    except Exception:
        pass

    # Friendly sign → Mudita
    lord = _SIGN_LORD[pos.sign_index]
    if lord in _NAT_FRIEND.get(planet, set()):
        return "Mudita", 1.25

    # Enemy sign → Kshuditha
    if lord in _NAT_ENEMY.get(planet, set()):
        return "Kshuditha", 0.75

    # Watery sign + malefic aspect → Trashita
    if pos.sign_index in _WATERY:
        for p2, p2pos in chart.planets.items():
            if p2 in _NAT_MALEFIC and p2 != planet:
                diff = (pos.sign_index - p2pos.sign_index) % 12
                if diff == 6:
                    return "Trashita", 0.75

    return "Prakrita", 1.0


@dataclass
class AvasthaV2:
    planet: str
    sign: str
    degree: float
    baaladi_state: str
    baaladi_pct: float
    sayanadi_state: str
    sayanadi_modifier: float
    combined_modifier: float


@dataclass
class AvasthaReportV2:
    planets: dict

    def modifier_for(self, planet: str) -> float:
        av = self.planets.get(planet)
        return av.combined_modifier if av else 1.0


def compute_avasthas_v2(chart) -> AvasthaReportV2:
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    result = {}
    for p in planets_7:
        pos = chart.planets.get(p)
        if not pos:
            continue
        ba_state, ba_pct = compute_baaladi(p, chart)
        sa_state, sa_mod = compute_sayanadi(p, chart)
        result[p] = AvasthaV2(
            planet=p, sign=pos.sign, degree=round(pos.degree_in_sign, 4),
            baaladi_state=ba_state, baaladi_pct=ba_pct,
            sayanadi_state=sa_state, sayanadi_modifier=sa_mod,
            combined_modifier=round(ba_pct * sa_mod, 3),
        )
    return AvasthaReportV2(planets=result)
