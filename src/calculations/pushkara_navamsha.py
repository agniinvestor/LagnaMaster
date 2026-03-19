"""Pushkara Navamsha — 24 auspicious navamsha zones (Session 11)."""
from __future__ import annotations
_NAVAMSHA_WIDTH: float = 10.0 / 3.0
_PUSHKARA_STARTS: dict[int, tuple[float, float]] = {
    0:(18+20/60,25.0),1:(3+20/60,28+20/60),2:(13+20/60,25.0),
    3:(1+40/60,25.0),4:(11+40/60,19+10/60),5:(23+20/60,28+20/60),
    6:(0.0,23+20/60),7:(19+10/60,28+20/60),8:(5.0,23+20/60),
    9:(10.0,28+20/60),10:(6+40/60,25.0),11:(13+20/60,25.0),
}
def is_pushkara_navamsha(sign_index:int,degree_in_sign:float)->bool:
    if not(0<=sign_index<=11): return False
    for s in _PUSHKARA_STARTS[sign_index]:
        if s<=degree_in_sign<s+_NAVAMSHA_WIDTH: return True
    return False
def pushkara_navamsha_planets(chart)->list:
    return[n for n,p in chart.planets.items() if is_pushkara_navamsha(p.sign_index,p.degree_in_sign)]
def pushkara_navamsha_zones(sign_index:int)->list:
    return[(s,s+_NAVAMSHA_WIDTH) for s in _PUSHKARA_STARTS.get(sign_index,(0.0,0.0))]
def pushkara_strength_label(sign_index:int,degree_in_sign:float)->str:
    return "Pushkara Navamsha" if is_pushkara_navamsha(sign_index,degree_in_sign) else ""
