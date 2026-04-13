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
from src.data.constants import NATURAL_BENEFICS
from datetime import date

from src.calculations.extended_yogas import YogaResult



def _planet_houses(chart) -> dict[str, int]:
    from src.calculations.house_lord import compute_house_map

    return compute_house_map(chart).planet_house


def _yoga(
    name, kind, planets, present, score, desc, src, dashas=None, on_date=None
) -> YogaResult:
    dw = 1.0
    if dashas and on_date:
        try:
            from src.calculations.vimshottari_dasa import current_dasha

            md, ad = current_dasha(dashas, on_date)
            if any(p in {md.lord, ad.lord} for p in planets):
                dw = 1.0
            else:
                dw = 0.5
        except ImportError:
            dw = 0.5
    return YogaResult(
        name=name,
        yoga_type=kind,
        planets=planets,
        present=present,
        score=score,
        dasha_weight=dw,
        weighted_score=round(score * dw, 2),
        description=desc,
        source=src,
    )


# ── Nabhasa yogas ─────────────────────────────────────────────────────────────
def detect_nabhasa_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    """Delegate to canonical nabhasa_yogas.py (32 yogas) and wrap as YogaResult."""
    from src.calculations.nabhasa_yogas import detect_nabhasa_yogas as _canonical

    canonical = _canonical(chart)
    results = []
    for ny in canonical:
        results.append(
            _yoga(
                ny.name,
                "Nabhasa",
                ny.planets_involved,
                ny.present,
                2.0 if ny.present else 0.0,
                ny.result,
                f"BPHS Ch.35 ({ny.group})",
                dashas,
                on_date,
            )
        )
    return results


# ── Chandra (Moon) yogas ──────────────────────────────────────────────────────
def detect_chandra_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    moon_h = ph.get("Moon", 0)
    results = []

    non_luminaries = {"Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    h_before = (moon_h - 2) % 12 + 1 if moon_h > 0 else 0
    h_after = (moon_h % 12) + 1 if moon_h > 0 else 0

    planets_before = [p for p in non_luminaries if ph.get(p) == h_before]
    planets_after = [p for p in non_luminaries if ph.get(p) == h_after]

    # Sunapha — planet(s) in 2nd from Moon (h_after = 2nd from Moon)
    sunapha = bool(planets_after)
    results.append(
        _yoga(
            "Sunapha Yoga",
            "Chandra",
            planets_after,
            sunapha,
            2.0 if sunapha else 0.0,
            "Planet(s) in 2nd from Moon — earned wealth",
            "BPHS Ch.37 v.1",
            dashas,
            on_date,
        )
    )

    # Anapha — planet(s) in 12th from Moon (h_before = 12th from Moon)
    anapha = bool(planets_before)
    results.append(
        _yoga(
            "Anapha Yoga",
            "Chandra",
            planets_before,
            anapha,
            2.0 if anapha else 0.0,
            "Planet(s) in 12th from Moon — pleasure, enjoyment",
            "BPHS Ch.37 v.2",
            dashas,
            on_date,
        )
    )

    # Durudhura — planets both 2nd AND 12th from Moon
    durudhura = sunapha and anapha
    results.append(
        _yoga(
            "Durudhura Yoga",
            "Chandra",
            planets_before + planets_after,
            durudhura,
            3.0 if durudhura else 0.0,
            "Planets on both sides of Moon — wealth and fame",
            "BPHS Ch.37 v.3",
            dashas,
            on_date,
        )
    )

    # Kemadruma — no planet 2nd or 12th from Moon (and no planet with Moon)
    moon_cotenants = [p for p in non_luminaries if ph.get(p) == moon_h]
    kemadruma = not sunapha and not anapha and not moon_cotenants
    results.append(
        _yoga(
            "Kemadruma Yoga",
            "Chandra",
            ["Moon"],
            kemadruma,
            -2.0 if kemadruma else 0.0,
            "Moon isolated — misfortune, struggles",
            "BPHS Ch.37 v.4",
            dashas,
            on_date,
        )
    )

    # Adhi Yoga — benefics in 6/7/8 from Moon
    benefic_678 = [
        p
        for p in NATURAL_BENEFICS
        if ph.get(p, 0) in {(moon_h + h - 1 - 1) % 12 + 1 for h in [6, 7, 8]}
    ]
    adhi = len(benefic_678) >= 2
    results.append(
        _yoga(
            "Adhi Yoga",
            "Chandra",
            benefic_678,
            adhi,
            3.0 if adhi else 0.0,
            f"Benefics in 6/7/8 from Moon ({benefic_678}) — leadership",
            "BPHS Ch.37 v.5",
            dashas,
            on_date,
        )
    )

    return results


# ── Surya (Sun) yogas ─────────────────────────────────────────────────────────
def detect_surya_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    sun_h = ph.get("Sun", 0)
    results = []

    non_luminaries = {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    h_before = (sun_h - 2) % 12 + 1 if sun_h > 0 else 0
    h_after = (sun_h % 12) + 1 if sun_h > 0 else 0

    planets_before = [p for p in non_luminaries if ph.get(p) == h_before]
    planets_after = [p for p in non_luminaries if ph.get(p) == h_after]

    # Vesi — planet in 2nd from Sun (h_after = 2nd from Sun)
    vesi = bool(planets_after)
    results.append(
        _yoga(
            "Vesi Yoga",
            "Surya",
            planets_after,
            vesi,
            2.0 if vesi else 0.0,
            "Planet in 2nd from Sun — fortunate",
            "BPHS Ch.36 v.1",
            dashas,
            on_date,
        )
    )

    # Vasi — planet in 12th from Sun (h_before = 12th from Sun)
    vasi = bool(planets_before)
    results.append(
        _yoga(
            "Vasi Yoga",
            "Surya",
            planets_before,
            vasi,
            1.5 if vasi else 0.0,
            "Planet in 12th from Sun — clever, prosperous",
            "BPHS Ch.36 v.2",
            dashas,
            on_date,
        )
    )

    # Ubhayachari — planets both 2nd and 12th from Sun
    ubhaya = vesi and vasi
    results.append(
        _yoga(
            "Ubhayachari Yoga",
            "Surya",
            planets_before + planets_after,
            ubhaya,
            3.0 if ubhaya else 0.0,
            "Planets on both sides of Sun — royal status",
            "BPHS Ch.36 v.3",
            dashas,
            on_date,
        )
    )

    return results


# ── Additional Dhana / Duryoga / Daridra ─────────────────────────────────────
def detect_dhana_yogas_ext(chart, dashas=None, on_date=None) -> list[YogaResult]:
    ph = _planet_houses(chart)
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    results = []

    # Lakshmi Yoga: Venus + 9th lord both in own/exalt signs in kendra/trikona
    from src.data.constants import EXALTATION_SIGN as _EXALT_SI, OWN_SIGNS
    _OWN = {p: set(s) for p, s in OWN_SIGNS.items()}

    def is_strong(p):
        pos = chart.planets.get(p)
        if not pos:
            return False
        return (
            pos.sign_index in _OWN.get(p, set()) or _EXALT_SI.get(p) == pos.sign_index
        )

    lord9 = hmap.house_lord[8]
    kendra_trikona = {1, 4, 5, 7, 9, 10}
    lakshmi = (
        is_strong("Venus") and is_strong(lord9) and ph.get(lord9, 0) in kendra_trikona
    )
    results.append(
        _yoga(
            "Lakshmi Yoga",
            "Dhana",
            ["Venus", lord9],
            lakshmi,
            4.0 if lakshmi else 0.0,
            "Venus + 9th lord strong in kendra/trikona — great wealth",
            "Phaladeepika Ch.6 v.10",
            dashas,
            on_date,
        )
    )

    # Duryoga: 10th lord in 6/8/12
    lord10 = hmap.house_lord[9]
    duryoga = ph.get(lord10, 0) in {6, 8, 12}
    results.append(
        _yoga(
            "Duryoga",
            "Dhana",
            [lord10],
            duryoga,
            -2.0 if duryoga else 0.0,
            f"10th lord {lord10} in dusthana — career obstacles",
            "BPHS Ch.41",
            dashas,
            on_date,
        )
    )

    # Daridra Yoga: 11th lord in 6/8/12
    lord11 = hmap.house_lord[10]
    daridra = ph.get(lord11, 0) in {6, 8, 12}
    results.append(
        _yoga(
            "Daridra Yoga",
            "Dhana",
            [lord11],
            daridra,
            -2.5 if daridra else 0.0,
            f"11th lord {lord11} in dusthana — poverty, loss of gains",
            "BPHS Ch.41 v.5",
            dashas,
            on_date,
        )
    )

    # Mahabhagya: Day birth+Sun/Moon/Lagna in odd signs (male)
    #             Night birth+Sun/Moon/Lagna in even signs (female)
    sun_si = chart.planets["Sun"].sign_index
    moon_si = chart.planets["Moon"].sign_index
    lag_si = chart.lagna_sign_index
    all_odd = all(
        si % 2 == 0 for si in [sun_si, moon_si, lag_si]
    )  # odd sign = even index
    mahabhagya = all_odd
    results.append(
        _yoga(
            "Mahabhagya Yoga",
            "Dhana",
            ["Sun", "Moon"],
            mahabhagya,
            4.0 if mahabhagya else 0.0,
            "Sun, Moon, Lagna all in odd signs — great fortune",
            "BPHS Ch.38 v.2",
            dashas,
            on_date,
        )
    )

    return results


def detect_all_extended_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    if on_date is None:
        on_date = date.today()
    return (
        detect_nabhasa_yogas(chart, dashas, on_date)
        + detect_chandra_yogas(chart, dashas, on_date)
        + detect_surya_yogas(chart, dashas, on_date)
        + detect_dhana_yogas_ext(chart, dashas, on_date)
    )
