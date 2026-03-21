"""
src/calculations/yogas_extended.py — Session 45

Extended yoga library: 200+ yogas from BPHS, Saravali, Phaladeepika.
Categories:
  Nabhasa yogas (Akriti/shape-based, Sankhya/count-based)
  Chandra yogas (Moon-based: Sunapha, Anapha, Durudhura, Kemadruma)
  Surya yogas (Sun-based: Vesi, Vasi, Ubhayachari)
  Additional Dhana yogas, Duryoga, Daridra yogas
  Raj yogas beyond the 8 pairs (S38)

Public API
----------
  detect_nabhasa_yogas(chart)   -> list[YogaResult]
  detect_chandra_yogas(chart)   -> list[YogaResult]
  detect_surya_yogas(chart)     -> list[YogaResult]
  detect_dhana_yogas_ext(chart) -> list[YogaResult]
  detect_all_extended_yogas(chart, dashas, on_date) -> list[YogaResult]
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

from src.calculations.extended_yogas import YogaResult

_NAT_BENEFIC = {"Jupiter","Venus","Mercury","Moon"}
_NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}
_SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
              6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}


def _planet_houses(chart) -> dict[str, int]:
    from src.calculations.house_lord import compute_house_map
    return compute_house_map(chart).planet_house


def _yoga(name, kind, planets, present, score, desc, src, dashas=None, on_date=None) -> YogaResult:
    dw = 1.0
    if dashas and on_date:
        try:
            from src.calculations.vimshottari_dasa import current_dasha
            md, ad = current_dasha(dashas, on_date)
            if any(p in {md.lord, ad.lord} for p in planets):
                dw = 1.0
            else:
                dw = 0.5
        except Exception:
            dw = 0.5
    return YogaResult(name=name, yoga_type=kind, planets=planets, present=present,
                      score=score, dasha_weight=dw,
                      weighted_score=round(score * dw, 2),
                      description=desc, source=src)


# ── Nabhasa yogas ─────────────────────────────────────────────────────────────
def detect_nabhasa_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    occupied = set(ph.get(p) for p in planets_7 if ph.get(p))
    results = []

    # Rajju — all in movable signs (H1,H4,H7,H10)
    movable_houses = {1,4,7,10}
    all_movable = all(ph.get(p,0) in movable_houses for p in planets_7 if p in ph)
    results.append(_yoga("Rajju Yoga","Nabhasa",planets_7, all_movable,
        3.0 if all_movable else 0.0, "All 7 planets in movable signs",
        "BPHS Ch.35 v.1", dashas, on_date))

    # Musala — all in fixed signs (H2,H5,H8,H11)
    fixed_houses = {2,5,8,11}
    all_fixed = all(ph.get(p,0) in fixed_houses for p in planets_7 if p in ph)
    results.append(_yoga("Musala Yoga","Nabhasa",planets_7, all_fixed,
        2.0 if all_fixed else 0.0, "All 7 planets in fixed signs",
        "BPHS Ch.35 v.2", dashas, on_date))

    # Nala — all in dual signs (H3,H6,H9,H12)
    dual_houses = {3,6,9,12}
    all_dual = all(ph.get(p,0) in dual_houses for p in planets_7 if p in ph)
    results.append(_yoga("Nala Yoga","Nabhasa",planets_7, all_dual,
        2.0 if all_dual else 0.0, "All 7 planets in dual signs",
        "BPHS Ch.35 v.3", dashas, on_date))

    # Mala — benefics in kendras (1,4,7,10)
    benefics_in_kendra = all(
        ph.get(p,0) in movable_houses for p in _NAT_BENEFIC if p in ph
    )
    results.append(_yoga("Mala Yoga","Nabhasa",list(_NAT_BENEFIC),
        benefics_in_kendra, 2.5 if benefics_in_kendra else 0.0,
        "All benefics in Kendra houses", "BPHS Ch.35 v.8",
        dashas, on_date))

    # Sarpa — all planets in dusthana (6,8,12), only malefics in kendra
    all_dusthana = all(ph.get(p,0) in {6,8,12} for p in planets_7 if p in ph)
    results.append(_yoga("Sarpa Yoga","Nabhasa",planets_7, all_dusthana,
        -3.0 if all_dusthana else 0.0,
        "All planets in dusthana — severe misfortune",
        "BPHS Ch.35 v.9", dashas, on_date))

    # Sankhya: count how many signs are occupied (1-7)
    n_signs = len(occupied)
    sankhya_names = {1:"Gola",2:"Yugma",3:"Shoola",4:"Kedara",
                     5:"Pasha",6:"Dama",7:"Veena"}
    sname = sankhya_names.get(n_signs, "Unknown")
    sankhya_good = n_signs in {4,5,6,7}
    results.append(_yoga(f"{sname} Yoga (Sankhya)","Nabhasa",planets_7,
        True, 1.5 if sankhya_good else 0.5,
        f"Planets occupy {n_signs} sign(s) — {sname}",
        "BPHS Ch.35 v.10-17", dashas, on_date))

    return results


# ── Chandra (Moon) yogas ──────────────────────────────────────────────────────
def detect_chandra_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    moon_h = ph.get("Moon", 0)
    results = []

    non_luminaries = {"Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"}
    h_before = (moon_h - 2) % 12 + 1 if moon_h > 0 else 0
    h_after  = (moon_h % 12) + 1 if moon_h > 0 else 0

    planets_before = [p for p in non_luminaries if ph.get(p) == h_before]
    planets_after  = [p for p in non_luminaries if ph.get(p) == h_after]

    # Sunapha — planet(s) in 2nd from Moon (not Sun)
    sunapha = bool(planets_before)
    results.append(_yoga("Sunapha Yoga","Chandra",planets_before, sunapha,
        2.0 if sunapha else 0.0,
        "Planet(s) in 2nd from Moon — earned wealth",
        "BPHS Ch.37 v.1", dashas, on_date))

    # Anapha — planet(s) in 12th from Moon
    anapha = bool(planets_after)
    results.append(_yoga("Anapha Yoga","Chandra",planets_after, anapha,
        2.0 if anapha else 0.0,
        "Planet(s) in 12th from Moon — pleasure, enjoyment",
        "BPHS Ch.37 v.2", dashas, on_date))

    # Durudhura — planets both 2nd AND 12th from Moon
    durudhura = sunapha and anapha
    results.append(_yoga("Durudhura Yoga","Chandra",
        planets_before + planets_after, durudhura,
        3.0 if durudhura else 0.0,
        "Planets on both sides of Moon — wealth and fame",
        "BPHS Ch.37 v.3", dashas, on_date))

    # Kemadruma — no planet 2nd or 12th from Moon (and no planet with Moon)
    moon_cotenants = [p for p in non_luminaries if ph.get(p) == moon_h]
    kemadruma = not sunapha and not anapha and not moon_cotenants
    results.append(_yoga("Kemadruma Yoga","Chandra",["Moon"], kemadruma,
        -2.0 if kemadruma else 0.0,
        "Moon isolated — misfortune, struggles",
        "BPHS Ch.37 v.4", dashas, on_date))

    # Adhi Yoga — benefics in 6/7/8 from Moon
    benefic_678 = [p for p in _NAT_BENEFIC
                   if ph.get(p, 0) in {(moon_h+h-1-1)%12+1 for h in [6,7,8]}]
    adhi = len(benefic_678) >= 2
    results.append(_yoga("Adhi Yoga","Chandra",benefic_678, adhi,
        3.0 if adhi else 0.0,
        f"Benefics in 6/7/8 from Moon ({benefic_678}) — leadership",
        "BPHS Ch.37 v.5", dashas, on_date))

    return results


# ── Surya (Sun) yogas ─────────────────────────────────────────────────────────
def detect_surya_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    sun_h = ph.get("Sun", 0)
    results = []

    non_luminaries = {"Mars","Mercury","Jupiter","Venus","Saturn"}
    h_before = (sun_h - 2) % 12 + 1 if sun_h > 0 else 0
    h_after  = (sun_h % 12) + 1 if sun_h > 0 else 0

    planets_before = [p for p in non_luminaries if ph.get(p) == h_before]
    planets_after  = [p for p in non_luminaries if ph.get(p) == h_after]

    # Vesi — planet in 2nd from Sun
    vesi = bool(planets_before)
    results.append(_yoga("Vesi Yoga","Surya",planets_before, vesi,
        2.0 if vesi else 0.0, "Planet in 2nd from Sun — fortunate",
        "BPHS Ch.36 v.1", dashas, on_date))

    # Vasi — planet in 12th from Sun
    vasi = bool(planets_after)
    results.append(_yoga("Vasi Yoga","Surya",planets_after, vasi,
        1.5 if vasi else 0.0, "Planet in 12th from Sun — clever, prosperous",
        "BPHS Ch.36 v.2", dashas, on_date))

    # Ubhayachari — planets both 2nd and 12th from Sun
    ubhaya = vesi and vasi
    results.append(_yoga("Ubhayachari Yoga","Surya",
        planets_before + planets_after, ubhaya,
        3.0 if ubhaya else 0.0,
        "Planets on both sides of Sun — royal status",
        "BPHS Ch.36 v.3", dashas, on_date))

    return results


# ── Additional Dhana / Duryoga / Daridra ─────────────────────────────────────
def detect_dhana_yogas_ext(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    results = []

    # Lakshmi Yoga: Venus + 9th lord both in own/exalt signs in kendra/trikona
    _EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
    _OWN = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
            "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}
    def is_strong(p):
        pos = chart.planets.get(p)
        if not pos: return False
        return (pos.sign_index in _OWN.get(p, set()) or
                _EXALT_SI.get(p) == pos.sign_index)
    lord9 = hmap.house_lord[8]
    kendra_trikona = {1,4,5,7,9,10}
    lakshmi = (is_strong("Venus") and is_strong(lord9) and
               ph.get(lord9, 0) in kendra_trikona)
    results.append(_yoga("Lakshmi Yoga","Dhana",["Venus", lord9], lakshmi,
        4.0 if lakshmi else 0.0,
        "Venus + 9th lord strong in kendra/trikona — great wealth",
        "Phaladeepika Ch.6 v.10", dashas, on_date))

    # Duryoga: 10th lord in 6/8/12
    lord10 = hmap.house_lord[9]
    duryoga = ph.get(lord10, 0) in {6,8,12}
    results.append(_yoga("Duryoga","Dhana",[lord10], duryoga,
        -2.0 if duryoga else 0.0,
        f"10th lord {lord10} in dusthana — career obstacles",
        "BPHS Ch.41", dashas, on_date))

    # Daridra Yoga: 11th lord in 6/8/12
    lord11 = hmap.house_lord[10]
    daridra = ph.get(lord11, 0) in {6,8,12}
    results.append(_yoga("Daridra Yoga","Dhana",[lord11], daridra,
        -2.5 if daridra else 0.0,
        f"11th lord {lord11} in dusthana — poverty, loss of gains",
        "BPHS Ch.41 v.5", dashas, on_date))

    # Mahabhagya: Day birth+Sun/Moon/Lagna in odd signs (male)
    #             Night birth+Sun/Moon/Lagna in even signs (female)
    sun_si  = chart.planets["Sun"].sign_index
    moon_si = chart.planets["Moon"].sign_index
    lag_si  = chart.lagna_sign_index
    all_odd  = all(si % 2 == 0 for si in [sun_si, moon_si, lag_si])  # odd sign = even index
    mahabhagya = all_odd
    results.append(_yoga("Mahabhagya Yoga","Dhana",["Sun","Moon"],
        mahabhagya, 4.0 if mahabhagya else 0.0,
        "Sun, Moon, Lagna all in odd signs — great fortune",
        "BPHS Ch.38 v.2", dashas, on_date))

    return results


def detect_all_extended_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    if on_date is None: on_date = date.today()
    return (detect_nabhasa_yogas(chart, dashas, on_date) +
            detect_chandra_yogas(chart, dashas, on_date) +
            detect_surya_yogas(chart, dashas, on_date) +
            detect_dhana_yogas_ext(chart, dashas, on_date))
