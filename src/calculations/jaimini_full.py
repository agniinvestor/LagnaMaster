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


    # ── Bandhu Yoga (4th lord in kendra from AK) ─────────────────────────────
    lord4 = hmap.house_lord[3]
    ak_h = ph.get(ak_planet, 0)
    lord4_h = ph.get(lord4, 0)
    if ak_h > 0 and lord4_h > 0:
        diff_bandhu = abs(lord4_h - ak_h) % 12
        bandhu = diff_bandhu in {0, 3, 6, 9}
    else:
        bandhu = False
    yogas.append(JaiminiYoga(
        name="Bandhu Yoga",
        present=bandhu,
        score=1.5 if bandhu else 0.0,
        description=f"4th lord {lord4} in kendra from AK {ak_planet} — comfort and homeland",
        source="Jaimini Sutra 4.2",
    ))

    return yogas


def compute_karakamsha_scores(chart) -> dict[int, float]:
    """Score all 12 houses from Karakamsha lagna (soul axis)."""
    from src.calculations.multi_lagna import compute_karakamsha
    from src.calculations.multi_axis_scoring import score_axis
    try:
        kk = compute_karakamsha(chart)
        ax = score_axis(chart, kk.ak_d9_sign_index, "Karakamsha", "jaimini")
        return ax.scores
    except Exception:
        return {h: 0.0 for h in range(1, 13)}


@dataclass
class JaiminiLongevity:
    brahma: str        # planet
    maheshvara: str    # planet
    rudra: str         # planet
    span: str          # "Short"/"Medium"/"Long"
    years_estimate: float
    method: str = "Jaimini Brahma-Maheshvara-Rudra"


def compute_jaimini_longevity(chart) -> JaiminiLongevity:
    """
    Jaimini longevity via Brahma, Maheshvara, Rudra method.
    Brahma: strongest planet in odd houses (1,3,5,7,9,11)
    Maheshvara: 8th lord from AK
    Rudra: stronger of 8th and 12th lords
    """
    from src.calculations.house_lord import compute_house_map
    from src.calculations.chara_karak import compute_chara_karakas

    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    # Brahma: planet occupying or ruling odd houses with most strength
    odd_houses = {1,3,5,7,9,11}
    odd_planets = [p for p in chart.planets if ph.get(p,0) in odd_houses
                   and p not in {"Rahu","Ketu"}]
    brahma = odd_planets[0] if odd_planets else "Jupiter"

    # Maheshvara: lord of 8th from Atmakaraka
    try:
        karakas_raw = compute_chara_karakas(chart)
        if hasattr(karakas_raw, 'items'):
            ak = next((p for p, r in karakas_raw.items() if r == "AK"), "Sun")
        else:
            ak = next((p for p, r in karakas_raw if r == "AK"), "Sun")
    except Exception:
        ak = "Sun"
    ak_si = chart.planets[ak].sign_index
    h8_from_ak_si = (ak_si + 7) % 12
    maheshvara = _SIGN_LORD[h8_from_ak_si]

    # Rudra: stronger of H8 lord and H12 lord (by house position)
    lord8  = hmap.house_lord[7]
    lord12 = hmap.house_lord[11]
    h8_lord_house  = ph.get(lord8, 1)
    h12_lord_house = ph.get(lord12, 1)
    _HOUSE_STRENGTH = {1:4,4:4,7:4,10:4, 2:2,5:2,8:2,11:2, 3:1,6:1,9:1,12:1}
    rudra = lord8 if _HOUSE_STRENGTH.get(h8_lord_house,1) >= _HOUSE_STRENGTH.get(h12_lord_house,1) else lord12

    # Span estimate from combination
    strong_count = sum(1 for p in [brahma, maheshvara, rudra]
                       if ph.get(p,0) in {1,4,7,10})
    if strong_count >= 2:
        span, years = "Long", 75.0
    elif strong_count == 1:
        span, years = "Medium", 55.0
    else:
        span, years = "Short", 35.0

    return JaiminiLongevity(brahma=brahma, maheshvara=maheshvara, rudra=rudra,
                             span=span, years_estimate=years)


def pada_relationship_score(chart, h1: int, h2: int) -> float:
    """
    Score the relationship between two Arudha Padas.
    Positive: compatible signs (trine/sextile), benefics between them.
    Negative: 6/8 relationship between the padas (shad-ashtaka).
    """
    from src.calculations.multi_lagna import compute_all_arudha_padas
    ap = compute_all_arudha_padas(chart)
    p1 = ap.padas.get(h1)
    p2 = ap.padas.get(h2)
    if not p1 or not p2:
        return 0.0

    diff = abs(p1.sign_index - p2.sign_index) % 12
    if diff in {2, 10}:   # trine (5th/9th = 4,8 but from sign: 0,4,8)
        return 1.0
    if diff in {4, 8}:    # trine positions
        return 1.5
    if diff in {0}:        # same sign
        return 2.0
    if diff in {5, 7}:    # 6/8 relationship — challenging
        return -1.5
    if diff in {6}:        # 7th — opposition, neutral
        return 0.5
    return 0.0
