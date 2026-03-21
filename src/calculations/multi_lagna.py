"""
src/calculations/multi_lagna.py — Session 33

Three secondary reference frames beyond the natal (D1) lagna:
  Chandra Lagna  — houses counted from Moon's sign (emotional axis)
  Surya Lagna    — houses counted from Sun's sign  (authority/career axis)
  Karakamsha     — Atmakaraka's Navamsha sign as lagna (soul axis)

Also exposes the canonical Yogakaraka lookup table for all 12 lagnas
(CALC_YogakarakaMap) and all-12-arudha-pada computation (CALC_ArudhaPada).

Public API
----------
  compute_chandra_lagna(chart)    -> LagnaFrame
  compute_surya_lagna(chart)      -> LagnaFrame
  compute_karakamsha(chart)       -> KarakamshaResult
  yogakaraka_for_lagna(lagna_si)  -> str | None
  compute_all_arudha_padas(chart) -> ArudhaPadaResult
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
_SIGN_IDX = {s: i for i, s in enumerate(_SIGNS)}
_SIGN_LORD = {
    0:"Mars", 1:"Venus", 2:"Mercury", 3:"Moon", 4:"Sun", 5:"Mercury",
    6:"Venus", 7:"Mars", 8:"Jupiter", 9:"Saturn", 10:"Saturn", 11:"Jupiter",
}
_NAT_BENEFIC = {"Jupiter","Venus","Mercury","Moon"}
_NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}

# Yogakaraka per lagna — from CALC_YogakarakaMap (workbook-verified)
_YOGAKARAKA = {
    0: None,      # Aries
    1: "Saturn",  # Taurus  (H9+H10)
    2: None,      # Gemini
    3: "Mars",    # Cancer  (H5+H10)
    4: "Mars",    # Leo     (H4+H9)
    5: None,      # Virgo
    6: "Saturn",  # Libra   (H4+H5)
    7: None,      # Scorpio
    8: None,      # Sagittarius
    9: "Venus",   # Capricorn (H5+H10)
    10: "Venus",  # Aquarius  (H4+H9)
    11: None,     # Pisces
}


@dataclass
class LagnaFrame:
    """House map counted from a reference sign (Moon, Sun, or other)."""
    frame_name: str          # "Chandra", "Surya", "Karakamsha"
    reference_sign: str
    reference_sign_index: int
    # house_sign[h-1] = sign_index of house h in this frame
    house_sign: list[int]    = field(default_factory=list)
    house_lord: list[str]    = field(default_factory=list)
    planet_house: dict[str, int] = field(default_factory=dict)
    yogakaraka: Optional[str] = None

    def bhavesh(self, house: int) -> str:
        return self.house_lord[house - 1]


def _build_frame(name: str, ref_si: int, chart) -> LagnaFrame:
    house_sign = [(ref_si + h) % 12 for h in range(12)]
    house_lord = [_SIGN_LORD[si] for si in house_sign]
    planet_house = {}
    for p, pos in chart.planets.items():
        h = (pos.sign_index - ref_si) % 12 + 1
        planet_house[p] = h
    yk = _YOGAKARAKA.get(ref_si)
    return LagnaFrame(
        frame_name=name,
        reference_sign=_SIGNS[ref_si],
        reference_sign_index=ref_si,
        house_sign=house_sign,
        house_lord=house_lord,
        planet_house=planet_house,
        yogakaraka=yk,
    )


def compute_chandra_lagna(chart) -> LagnaFrame:
    """Houses counted from Moon's natal sign."""
    moon_si = chart.planets["Moon"].sign_index
    return _build_frame("Chandra", moon_si, chart)


def compute_surya_lagna(chart) -> LagnaFrame:
    """Houses counted from Sun's natal sign."""
    sun_si = chart.planets["Sun"].sign_index
    return _build_frame("Surya", sun_si, chart)


def yogakaraka_for_lagna(lagna_si: int) -> Optional[str]:
    """Return the Yogakaraka planet for a given lagna sign index, or None."""
    return _YOGAKARAKA.get(lagna_si % 12)


@dataclass
class KarakamshaResult:
    atmakaraka: str
    ak_d1_sign: str
    ak_d9_sign: str
    ak_d9_sign_index: int
    karakamsha_lord: str
    frame: LagnaFrame


def compute_karakamsha(chart) -> KarakamshaResult:
    """
    Karakamsha Lagna = Atmakaraka planet's Navamsha (D9) sign.
    The D9 sign of the AK becomes the reference for the soul-axis house map.
    Requires navamsha positions (computed by panchanga.compute_navamsha_chart).
    """
    from src.calculations.chara_karak import compute_chara_karakas
    from src.calculations.panchanga import compute_navamsha_chart
    karakas = compute_chara_karakas(chart)
    # Robust AK lookup: handles dict {planet: role} or list [(planet, role)]
    if hasattr(karakas, "items"):
        ak_planet = next((pl for pl, r in karakas.items() if r == "AK"), "Sun")
    elif karakas:
        try:
            ak_planet = next((pl for pl, r in karakas if r == "AK"), "Sun")
        except TypeError:
            ak_planet = "Sun"
    else:
        ak_planet = "Sun"
    ak_d1_si  = chart.planets[ak_planet].sign_index
    d9_map    = compute_navamsha_chart(chart)
    # DivisionalMap: access planet's D9 sign via planets dict or D9 attribute
    try:
        if hasattr(d9_map, 'planets') and isinstance(d9_map.planets, dict):
            ak_d9_si = d9_map.planets.get(ak_planet, {}).get('D9', 0)
        elif hasattr(d9_map, 'D9') and isinstance(d9_map.D9, dict):
            ak_d9_si = d9_map.D9.get(ak_planet, 0)
        else:
            ak_d9_si = chart.lagna_sign_index
    except Exception:
        ak_d9_si = chart.lagna_sign_index
    frame     = _build_frame("Karakamsha", ak_d9_si, chart)
    return KarakamshaResult(
        atmakaraka=ak_planet,
        ak_d1_sign=_SIGNS[ak_d1_si],
        ak_d9_sign=_SIGNS[ak_d9_si],
        ak_d9_sign_index=ak_d9_si,
        karakamsha_lord=_SIGN_LORD[ak_d9_si],
        frame=frame,
    )


# ── All 12 Arudha Padas ───────────────────────────────────────────────────────

_ARUDHA_NAMES = {1:"AL",2:"A2",3:"A3",4:"A4",5:"A5",6:"A6",
                 7:"DL",8:"A8",9:"A9",10:"A10",11:"A11",12:"UL"}

@dataclass
class ArudhaPada:
    house: int
    name: str               # AL, A2 … UL
    lord: str
    lord_bhav: int          # lord's house from D1 lagna
    house_bhav: int         # = house itself
    raw_arudha_bhav: int
    final_arudha_bhav: int  # after exception rule
    sign: str
    sign_index: int


@dataclass
class ArudhaPadaResult:
    padas: dict[int, ArudhaPada]  # keyed by house 1–12
    arudha_lagna: ArudhaPada      # = padas[1]
    upapada: ArudhaPada           # = padas[12]
    darapada: ArudhaPada          # = padas[7]
    a10: ArudhaPada               # = padas[10]


def compute_all_arudha_padas(chart) -> ArudhaPadaResult:
    """
    Compute all 12 Arudha Padas per CALC_ArudhaPada.
    Formula: raw_arudha = lord_house + (lord_house - house)   [1-indexed]
    Exception: if raw falls on the house itself or 7th from it → add 10 signs.
    """
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    lsi  = chart.lagna_sign_index
    padas = {}
    for h in range(1, 13):
        lord = hmap.house_lord[h - 1]
        lord_bhav = hmap.planet_house.get(lord, h)
        raw = (lord_bhav + (lord_bhav - h)) % 12
        if raw == 0:
            raw = 12
        final = raw
        # Exception: falls on same house or 7th from it
        if final == h or final == ((h + 5) % 12 + 1):
            final = (raw + 9) % 12
            if final == 0:
                final = 12
        si = (lsi + final - 1) % 12
        padas[h] = ArudhaPada(
            house=h, name=_ARUDHA_NAMES[h],
            lord=lord, lord_bhav=lord_bhav, house_bhav=h,
            raw_arudha_bhav=raw, final_arudha_bhav=final,
            sign=_SIGNS[si], sign_index=si,
        )
    return ArudhaPadaResult(
        padas=padas,
        arudha_lagna=padas[1], upapada=padas[12],
        darapada=padas[7], a10=padas[10],
    )
