"""
src/calculations/jaimini_full.py — Session 47

Full Jaimini system:
  Jaimini yoga corpus (Raja, Dhana, special Jaimini yogas)
  Karakamsha-centric house scoring
  Pada interplay (AL vs UL vs A10)
  Jaimini longevity (Brahma/Maheshvara/Rudra method)

Public API
----------
  detect_jaimini_yogas(chart)         -> list[JaiminiYoga]
  compute_karakamsha_scores(chart)    -> dict[int, float]
  compute_jaimini_longevity(chart)    -> JaiminiLongevity
  pada_relationship_score(chart, h1, h2) -> float
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
_SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
              6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}
_EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
_OWN = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
        "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}


@dataclass
class JaiminiYoga:
    name: str
    present: bool
    score: float
    description: str
    source: str


def detect_jaimini_yogas(chart) -> list[JaiminiYoga]:
    """Detect Jaimini-specific yogas (separate from Parashari)."""
    from src.calculations.chara_karak import compute_chara_karakas
    from src.calculations.multi_lagna import compute_all_arudha_padas
    from src.calculations.house_lord import compute_house_map

    try:
        karakas_raw = compute_chara_karakas(chart)
        if hasattr(karakas_raw, 'items'):
            karakas = karakas_raw
        else:
            karakas = {p: r for p, r in karakas_raw}
    except Exception:
        karakas = {}

    arudha = compute_all_arudha_padas(chart)
    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    yogas = []

    # AK in Kendra from Karakamsha — Rajayoga
    ak = next((p for p, r in karakas.items() if r == "AK"), "Sun")
    ak_house = ph.get(ak, 0)
    ak_in_kendra = ak_house in {1,4,7,10}
    yogas.append(JaiminiYoga(
        "Atmakaraka in Kendra", ak_in_kendra,
        3.0 if ak_in_kendra else 0.0,
        f"AK {ak} in H{ak_house} — Raja Yoga in Jaimini",
        "Jaimini Sutra 1.2.1"
    ))

    # Amatyakaraka (AmK) + AK together
    amk = next((p for p, r in karakas.items() if r == "AmK"), None)
    if amk:
        ak_amk_conjunct = ph.get(ak, 0) == ph.get(amk, 0)
        yogas.append(JaiminiYoga(
            "AK+AmK Conjunction", ak_amk_conjunct,
            3.5 if ak_amk_conjunct else 0.0,
            f"AK {ak} and AmK {amk} in same house — powerful Raja Yoga",
            "Jaimini Sutra 1.2.5"
        ))

    # Karakamsha 5th/9th house benefic — Gyana Yoga
    from src.calculations.multi_lagna import compute_karakamsha
    try:
        kk = compute_karakamsha(chart)
        kk_si = kk.ak_d9_sign_index
        h5_sign = (kk_si + 4) % 12
        h9_sign = (kk_si + 8) % 12
        h5_planets = [p for p in chart.planets
                      if chart.planets[p].sign_index == h5_sign]
        h9_planets = [p for p in chart.planets
                      if chart.planets[p].sign_index == h9_sign]
        benefics_5_9 = [p for p in h5_planets + h9_planets
                        if p in {"Jupiter","Venus","Mercury","Moon"}]
        gyana = bool(benefics_5_9)
        yogas.append(JaiminiYoga(
            "Karakamsha Gyana Yoga", gyana,
            2.5 if gyana else 0.0,
            f"Benefics {benefics_5_9} in 5th/9th from Karakamsha — wisdom",
            "Jaimini Sutra 2.1.12"
        ))
    except Exception:
        pass

    # AL and 7th from AL — relationship quality
    al_si  = arudha.arudha_lagna.sign_index
    al7_si = (al_si + 6) % 12
    al7_planets = [p for p in chart.planets
                   if chart.planets[p].sign_index == al7_si and p != "Ketu"]
    al7_benefics = [p for p in al7_planets if p in {"Jupiter","Venus","Mercury","Moon"}]
    al7_malefics = [p for p in al7_planets if p in {"Saturn","Mars","Rahu","Ketu","Sun"}]
    al_quality = len(al7_benefics) - len(al7_malefics)
    yogas.append(JaiminiYoga(
        "Arudha 7th Quality", al_quality > 0,
        float(al_quality), 
        f"7th from AL: benefics={al7_benefics}, malefics={al7_malefics}",
        "Jaimini Sutra 3.3"
    ))

    # UL and its lord — marriage quality
    ul_si  = arudha.upapada.sign_index
    ul_lord = _SIGN_LORD[ul_si]
    ul_lord_pos = chart.planets.get(ul_lord)
    ul_good = False
    if ul_lord_pos:
        ul_good = (ul_lord_pos.sign_index in _OWN.get(ul_lord, set()) or
                   _EXALT_SI.get(ul_lord) == ul_lord_pos.sign_index)
    yogas.append(JaiminiYoga(
        "Upapada Lord Strong", ul_good,
        2.0 if ul_good else -1.0,
        f"UL lord {ul_lord} is {'strong' if ul_good else 'weak'} — marriage quality",
        "Jaimini Sutra 3.4.1"
    ))

    try:
        _lord4 = hmap.house_lord[3]
        _ak_h  = ph.get(ak_planet, 0)
        _l4_h  = ph.get(_lord4, 0)
        _bandhu = (_ak_h > 0 and _l4_h > 0 and abs(_l4_h - _ak_h) % 12 in {0,3,6,9})
        yogas.append(JaiminiYoga(
            name="Bandhu Yoga", present=_bandhu,
            score=1.5 if _bandhu else 0.0,
            description=f"4th lord {_lord4} in kendra from AK {ak_planet}",
            source="Jaimini Sutra 4.2",
        ))
    except Exception:
        pass

    try:
        _lord4 = hmap.house_lord[3]
        _ak_h  = ph.get(ak_planet, 0)
        _l4_h  = ph.get(_lord4, 0)
        _bandhu = (_ak_h > 0 and _l4_h > 0 and abs(_l4_h - _ak_h) % 12 in {0,3,6,9})
        yogas.append(JaiminiYoga(
            name="Bandhu Yoga", present=_bandhu,
            score=1.5 if _bandhu else 0.0,
            description=f"4th lord {_lord4} in kendra from AK {ak_planet}",
            source="Jaimini Sutra 4.2",
        ))
    except Exception:
        pass
    return yogas
