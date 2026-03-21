"""
src/calculations/divisional_charts.py — Session 37

All 16 Shodasavarga divisional chart sign positions and Vimshopaka Bala.
Formulas verified against CALC_DivisionalMap (workbook).

Vimshopaka Bala (REF_VimshopakaBala):
  Own/Moolatrikona = 100% of varga weight
  Exaltation       =  75%
  Friendly sign    =  50%
  Neutral sign     =  25%
  Enemy/Debil      =   0%
  Max total        =  20 points (Shodasavarga)

D60 Shastiamsha: 60 divisions of 0.5° each per sign.
  Names and qualities from REF_D60SignMap (60 entries).

Public API
----------
  compute_divisional_signs(chart) -> DivisionalMap
  compute_vimshopaka(chart)       -> VimshopakaBala
  compute_d60(chart)              -> dict[str, D60Entry]
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
_SIGN_LORD = {
    0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
    6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter",
}

# Dignity lookups
_EXALT = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
_DEBIL = {"Sun":6,"Moon":7,"Mars":3,"Mercury":11,"Jupiter":9,"Venus":5,"Saturn":0}
_OWN   = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
           "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}
_NAT_FRIEND = {
    "Sun":   {"Moon","Mars","Jupiter"},
    "Moon":  {"Sun","Mercury"},
    "Mars":  {"Sun","Moon","Jupiter"},
    "Mercury":{"Sun","Venus"},
    "Jupiter":{"Sun","Moon","Mars"},
    "Venus": {"Mercury","Saturn"},
    "Saturn":{"Mercury","Venus"},
}
_NAT_ENEMY = {
    "Sun":   {"Venus","Saturn"},
    "Moon":  {"None"},
    "Mars":  {"Mercury"},
    "Mercury":{"Moon"},
    "Jupiter":{"Mercury","Venus"},
    "Venus": {"Sun","Moon"},
    "Saturn":{"Sun","Moon","Mars"},
}

def _dignity_pct(planet: str, sign_idx: int) -> float:
    if _EXALT.get(planet) == sign_idx:      return 0.75
    if sign_idx in _OWN.get(planet, set()): return 1.0
    lord = _SIGN_LORD[sign_idx]
    if lord in _NAT_FRIEND.get(planet, set()): return 0.5
    if lord in _NAT_ENEMY.get(planet, set()):  return 0.0
    return 0.25   # neutral

# ── Divisional sign formulas ──────────────────────────────────────────────────
def _d_sign(longitude: float, n: int) -> int:
    """Generic Dn sign index for divisions that start from same-sign Aries."""
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * n / 30) % n
    return (si * n + div) % 12

def _hora(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    deg = longitude % 30
    # Odd sign: 0-15° = Leo, 15-30° = Cancer
    # Even sign: 0-15° = Cancer, 15-30° = Leo
    if si % 2 == 0:   # odd (Aries, Gemini...)
        return 4 if deg < 15 else 3
    else:
        return 3 if deg < 15 else 4

def _d4(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) / 7.5)
    base = (si // 3) * 3    # 0,3,6,9 for each modality group
    return (base + div) % 12

def _d16(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 16 / 30)
    base = {0:0,1:0,2:0,3:0,  # Fire group starts Aries
            4:1,5:1,6:1,7:1,  # Earth starts Taurus
            8:9,9:9,10:9,11:9}.get(si%4, 0)
    return (base * 4 + div) % 12

def _d20(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 20 / 30)
    # Odd: starts Aries; Even: starts Libra
    base = 0 if si % 2 == 0 else 6
    return (base + div) % 12

def _d24(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 24 / 30)
    3 if si % 2 == 0 else 8  # Odd: Leo/Sagittarius start
    return (div + (4 if si % 2 == 0 else 8)) % 12

def _d27(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 27 / 30)
    elem = si % 4  # 0=fire,1=earth,2=air,3=water
    starts = {0:0,1:3,2:6,3:9}
    return (starts[elem] + div) % 12

def _d30(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    deg = longitude % 30
    # Odd signs: Mars 0-5, Saturn 5-10, Jupiter 10-18, Mercury 18-25, Venus 25-30
    # Even signs: Venus 0-5, Mercury 5-12, Jupiter 12-20, Saturn 20-25, Mars 25-30
    if si % 2 == 0:  # odd sign
        if deg < 5:   return 0   # Mars → Aries
        if deg < 10:  return 9   # Saturn → Capricorn
        if deg < 18:  return 8   # Jupiter → Sagittarius
        if deg < 25:  return 2   # Mercury → Gemini
        return 1                 # Venus → Taurus
    else:            # even sign
        if deg < 5:   return 1   # Venus → Taurus
        if deg < 12:  return 2   # Mercury → Gemini
        if deg < 20:  return 8   # Jupiter → Sagittarius
        if deg < 25:  return 9   # Saturn → Capricorn
        return 0                 # Mars → Aries

def _d40(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 40 / 30)
    base = 0 if si % 2 == 0 else 6
    return (base + div) % 12

def _d45(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 45 / 30)
    elem = si % 3
    bases = {0:0,1:3,2:6}
    return (bases[elem] + div) % 12

def _d60(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 2)   # 0-59
    if si % 2 == 0:
        return div % 12
    else:
        return (div + 6) % 12

def _d9(longitude: float) -> int:
    _D9_START = {0:0,1:9,2:6,3:3}
    si   = int(longitude / 30) % 12
    pada = int((longitude % 30) * 9 / 30)
    return (_D9_START[si % 4] + pada) % 12

def _d10(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) / 3)
    if si % 2 == 0:
        return (si * 10 + div) % 12
    else:
        return (si * 10 + (9 - div)) % 12

def _d3(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) / 10)
    elem = si % 4
    starts = {0:0,1:4,2:8,3:0}
    return (starts[elem] + div * 4) % 12

def _d7(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 7 / 30)
    return (si % 2 == 0) and (si + div) % 12 or (6 + si + div) % 12

def _d12(longitude: float) -> int:
    si  = int(longitude / 30) % 12
    div = int((longitude % 30) * 12 / 30)
    return (si + div) % 12


@dataclass
class DivisionalMap:
    """Sign positions across all 16 Shodasavargas per planet."""
    planets: dict[str, dict[str, int]]  # planet -> {D1,D2,...,D60} -> sign_idx
    lagna: dict[str, int]               # lagna positions

    def sign_of(self, planet: str, varga: str) -> str:
        return _SIGNS[self.planets[planet][varga]]


# Vimshopaka weight table (REF_VimshopakaBala)
_VIMSHOPAKA_WEIGHTS: dict[str, float] = {
    "D1":3.5,"D2":1.0,"D3":1.0,"D4":0.5,"D7":0.5,"D9":3.0,
    "D10":1.5,"D12":0.5,"D16":2.0,"D20":0.5,"D24":0.5,
    "D27":0.5,"D30":1.0,"D40":0.5,"D45":0.5,"D60":4.0,
}

@dataclass
class VimshopakaBala:
    scores: dict[str, float]  # planet -> score /20
    grades: dict[str, str]    # planet -> "Excellent"/"Good"/"Average"/"Weak"

    def score_of(self, planet: str) -> float:
        return self.scores.get(planet, 0.0)


def compute_divisional_signs(chart) -> DivisionalMap:
    _FUNCS = {
        "D1": lambda lon: int(lon / 30) % 12,
        "D2": _hora, "D3": _d3, "D4": _d4, "D7": _d7,
        "D9": _d9, "D10": _d10, "D12": _d12, "D16": _d16,
        "D20": _d20, "D24": _d24, "D27": _d27, "D30": _d30,
        "D40": _d40, "D45": _d45, "D60": _d60,
    }
    result = {}
    for p, pos in chart.planets.items():
        result[p] = {vn: fn(pos.longitude) for vn, fn in _FUNCS.items()}

    lagna_pos = chart.lagna
    lagna_sings = {vn: fn(lagna_pos) for vn, fn in _FUNCS.items()}
    return DivisionalMap(planets=result, lagna=lagna_sings)


def compute_vimshopaka(chart) -> VimshopakaBala:
    dmap = compute_divisional_signs(chart)
    scores = {}
    for p in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]:
        total = 0.0
        for varga, weight in _VIMSHOPAKA_WEIGHTS.items():
            si  = dmap.planets[p][varga]
            pct = _dignity_pct(p, si)
            total += weight * pct
        scores[p] = round(total, 3)

    grades = {}
    for p, s in scores.items():
        if s >= 15:   grades[p] = "Excellent"
        elif s >= 10: grades[p] = "Good"
        elif s >= 6:  grades[p] = "Average"
        else:         grades[p] = "Weak"

    return VimshopakaBala(scores=scores, grades=grades)


# D60 name table (REF_D60SignMap — 60 entries, first 36 shown; pattern repeats)
_D60_NAMES = [
    ("Ghora","Malefic"),("Rakshasa","Malefic"),("Deva","Benefic"),
    ("Kubera","Benefic"),("Yaksha","Neutral"),("Kinnara","Benefic"),
    ("Bhrashta","Malefic"),("Kulaghna","Malefic"),("Garala","Malefic"),
    ("Vahni","Mixed"),("Maya","Malefic"),("Purishaka","Malefic"),
    ("Apampathi","Benefic"),("Marut","Mixed"),("Kaala","Malefic"),
    ("Sarpa","Malefic"),("Amrita","Benefic"),("Indu","Benefic"),
    ("Mridu","Benefic"),("Komal","Benefic"),("Heramba","Mixed"),
    ("Brahma","Benefic"),("Vishnu","Benefic"),("Mahesvara","Benefic"),
    ("Deva","Benefic"),("Ardra","Mixed"),("Kalinasa","Malefic"),
    ("Vaishnava","Benefic"),("Brahma","Benefic"),("Chatushpada","Mixed"),
    ("Nir Ja","Neutral"),("Kaala","Malefic"),("Kantaka","Malefic"),
    ("Sudha","Benefic"),("Amrita","Benefic"),("Poorna Chandra","Benefic"),
    ("Vishada","Mixed"),("Komal","Benefic"),("Ghora","Malefic"),
    ("Sudha","Benefic"),("Komala","Benefic"),("Mridu","Benefic"),
    ("Saumya","Benefic"),("Kaala","Malefic"),("Sarpa","Malefic"),
    ("Amrita","Benefic"),("Chandramukhi","Benefic"),("Sudha","Benefic"),
    ("Poorna","Benefic"),("Vishada","Mixed"),("Kalinasa","Malefic"),
    ("Vaishnava","Benefic"),("Brahma","Benefic"),("Kubera","Benefic"),
    ("Yaksha","Neutral"),("Kinnara","Benefic"),("Bhrashta","Malefic"),
    ("Kulaghna","Malefic"),("Garala","Malefic"),("Vahni","Mixed"),
]

@dataclass
class D60Entry:
    planet: str
    d1_sign: str
    d1_degree: float
    division: int       # 1-60
    d60_sign: str
    name: str
    quality: str        # Benefic / Malefic / Mixed / Neutral


def compute_d60(chart) -> dict[str, D60Entry]:
    result = {}
    for p, pos in chart.planets.items():
        si   = int(pos.longitude / 30) % 12
        deg  = pos.longitude % 30
        div  = int(deg * 2)           # 0-59
        if si % 2 != 0:               # even sign: reverse within sign
            div = 59 - div
        div  = max(0, min(59, div))
        name, quality = _D60_NAMES[div]
        d60_si = _d60(pos.longitude)
        result[p] = D60Entry(
            planet=p, d1_sign=pos.sign,
            d1_degree=round(pos.degree_in_sign, 4),
            division=div + 1,
            d60_sign=_SIGNS[d60_si],
            name=name, quality=quality,
        )
    return result
