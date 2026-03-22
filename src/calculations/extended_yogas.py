"""
src/calculations/extended_yogas.py — Session 38

Raja + Dhana Yogas, Viparita Raja Yoga, Neecha Bhanga Raja Yoga.
All with dasha-weighted scoring (dormant=0.5×, active=1.0×).
Also: Rasi Drishti (12×12 sign-aspect matrix) and Bhavat Bhavam.

Public API
----------
  detect_raja_dhana_yogas(chart, dashas, on_date) -> list[YogaResult]
  detect_viparita_yogas(chart, dashas, on_date)   -> list[YogaResult]
  detect_neecha_bhanga(chart, dashas, on_date)    -> list[YogaResult]
  compute_rasi_drishti(chart)  -> RasiDrishtiMap
  compute_bhavat_bhavam(chart) -> dict[int, int]
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_SIGN_LORD = {
    0: "Mars",
    1: "Venus",
    2: "Mercury",
    3: "Moon",
    4: "Sun",
    5: "Mercury",
    6: "Venus",
    7: "Mars",
    8: "Jupiter",
    9: "Saturn",
    10: "Saturn",
    11: "Jupiter",
}
_EXALT = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
}
_DEBIL = {
    "Sun": 6,
    "Moon": 7,
    "Mars": 3,
    "Mercury": 11,
    "Jupiter": 9,
    "Venus": 5,
    "Saturn": 0,
}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}


@dataclass
class YogaResult:
    name: str
    yoga_type: str  # "Raja","Dhana","Viparita","NeechaBhanga"
    planets: list[str]
    present: bool
    score: float  # base score
    dasha_weight: float  # 0.5 dormant / 1.0 active
    weighted_score: float
    description: str
    source: str


def _is_dasha_active(planet: str, dashas, on_date) -> bool:
    try:
        from src.calculations.vimshottari_dasa import current_dasha

        md, ad = current_dasha(dashas, on_date)
        return planet in {md.lord, ad.lord}
    except Exception:
        return False


def _planet_sign_index(chart, planet: str) -> int:
    pos = chart.planets.get(planet)
    return pos.sign_index if pos else -1


def _same_sign(chart, p1: str, p2: str) -> bool:
    return (
        _planet_sign_index(chart, p1) == _planet_sign_index(chart, p2)
        and _planet_sign_index(chart, p1) >= 0
    )


def detect_raja_dhana_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    if on_date is None:
        on_date = date.today()
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    results = []

    # 8 Raja Yoga pairs: each non-H1 kendra (4,7,10) × each trikona (5,9)
    # + H1 × each trikona (5,9)
    raja_pairs = [
        (1, 5, "H1+H5"),
        (1, 9, "H1+H9"),
        (4, 5, "H4+H5"),
        (4, 9, "H4+H9"),
        (7, 5, "H7+H5"),
        (7, 9, "H7+H9"),
        (10, 5, "H10+H5"),
        (10, 9, "H10+H9"),
    ]
    for h_kendra, h_trikona, label in raja_pairs:
        lord_k = hmap.house_lord[h_kendra - 1]
        lord_t = hmap.house_lord[h_trikona - 1]
        present = _same_sign(chart, lord_k, lord_t)
        active_p = (
            lord_k
            if _is_dasha_active(lord_k, dashas, on_date)
            else (lord_t if _is_dasha_active(lord_t, dashas, on_date) else None)
        )
        dw = 1.0 if active_p else 0.5
        score = 2.0 if present else 0.0
        results.append(
            YogaResult(
                name=f"RY: {label}",
                yoga_type="Raja",
                planets=[lord_k, lord_t],
                present=present,  # noqa: F841
                score=score,
                dasha_weight=dw,
                weighted_score=round(score * dw, 2),
                description="Kendra+Trikona lord contact → status elevation",
                source="BPHS Ch.34-39",
            )
        )

    # 5 Dhana Yoga pairs
    dhana_pairs = [
        (2, 11, "DY: H2+H11"),
        (2, 9, "DY: H2+H9"),
        (2, 5, "DY: H2+H5"),
        (11, 9, "DY: H11+H9"),
        (11, 5, "DY: H11+H5"),
    ]
    for ha, hb, label in dhana_pairs:
        la = hmap.house_lord[ha - 1]
        lb = hmap.house_lord[hb - 1]
        present = _same_sign(chart, la, lb)
        dw = (
            1.0
            if (
                _is_dasha_active(la, dashas, on_date)
                or _is_dasha_active(lb, dashas, on_date)
            )
            else 0.5
        )
        score = 2.0 if present else 0.0
        _desc = {
            "DY: H2+H11": "Classic Dhana Yoga",
            "DY: H2+H9": "Wealth via fortune",
            "DY: H2+H5": "Wealth via intellect",
            "DY: H11+H9": "Gains via dharma",
            "DY: H11+H5": "Gains via creativity",
        }.get(label, "Dhana Yoga")
        results.append(
            YogaResult(
                name=label,
                yoga_type="Dhana",
                planets=[la, lb],
                present=present,  # noqa: F841
                score=score,
                dasha_weight=dw,
                weighted_score=round(score * dw, 2),
                description=_desc,
                source="BPHS Ch.35-36",
            )
        )
    return results


def detect_viparita_yogas(chart, dashas=None, on_date=None) -> list[YogaResult]:
    if on_date is None:
        on_date = date.today()
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    results = []

    # Viparita types: dusthana lord in another dusthana
    viparita = [
        (
            "Harsha Yoga",
            6,
            "H6 lord in H6/H8/H12 → victory over enemies",
            "BPHS Ch.42 v.3-4",
        ),
        (
            "Sarala Yoga",
            8,
            "H8 lord in H6/H8/H12 → long life, prosperous",
            "BPHS Ch.42 v.5-6",
        ),
        (
            "Vimala Yoga",
            12,
            "H12 lord in H6/H8/H12 → virtuous, free enemies",
            "BPHS Ch.42 v.7-8",
        ),
    ]
    for name, src_house, desc, src in viparita:
        lord = hmap.house_lord[src_house - 1]
        lord_house = hmap.planet_house.get(lord, 0)
        present = lord_house in DUSTHANA
        dw = 1.0 if _is_dasha_active(lord, dashas, on_date) else 0.5
        score = 2.0 if present else 0.0
        results.append(
            YogaResult(
                name=name,
                yoga_type="Viparita",
                planets=[lord],
                present=present,
                score=score,
                dasha_weight=dw,
                weighted_score=round(score * dw, 2),
                description=desc,
                source=src,
            )
        )

    # Dainya Yoga: H6+H8 lords in parivartana
    l6 = hmap.house_lord[5]
    l8 = hmap.house_lord[7]
    l6_h = hmap.planet_house.get(l6, 0)
    l8_h = hmap.planet_house.get(l8, 0)
    dainya = l6_h == 8 and l8_h == 6
    dw = (
        1.0
        if (
            _is_dasha_active(l6, dashas, on_date)
            or _is_dasha_active(l8, dashas, on_date)
        )
        else 0.5
    )
    results.append(
        YogaResult(
            name="Dainya Yoga",
            yoga_type="Viparita",
            planets=[l6, l8],
            present=dainya,  # noqa: F841
            score=-1.0 if dainya else 0.0,
            dasha_weight=dw,
            weighted_score=round((-1.0 if dainya else 0.0) * dw, 2),
            description="H6+H8 lords in mutual exchange — difficult obstacles",
            source="BPHS Ch.42 v.9-12",
        )
    )
    return results


DUSTHANA = {6, 8, 12}


def detect_neecha_bhanga(chart, dashas=None, on_date=None) -> list[YogaResult]:
    if on_date is None:
        on_date = date.today()
    from src.calculations.house_lord import compute_house_map, is_kendra

    hmap = compute_house_map(chart)
    results = []
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    for p in planets_7:
        pos = chart.planets.get(p)
        if not pos:
            continue
        debil_si = _DEBIL.get(p)
        if pos.sign_index != debil_si:
            results.append(
                YogaResult(
                    name=f"NB: {p}",
                    yoga_type="NeechaBhanga",
                    planets=[p],
                    present=False,
                    score=0.0,
                    dasha_weight=0.5,
                    weighted_score=0.0,
                    description=f"{p} not debilitated",
                    source="BPHS Ch.30",
                )
            )
            continue
        # Check 3 cancellation conditions
        dispositor = _SIGN_LORD[debil_si]
        disp_house = hmap.planet_house.get(dispositor, 0)
        exalt_lord = _SIGN_LORD[_EXALT.get(p, debil_si)]
        exalt_lord_house = hmap.planet_house.get(exalt_lord, 0)
        from src.calculations.panchanga import compute_navamsha_chart

        d9_map = compute_navamsha_chart(chart)
        p_d9_si = d9_map.get(p, -1)
        exalt_in_d9 = p_d9_si == _EXALT.get(p, -1)

        cond1 = is_kendra(disp_house)
        cond2 = is_kendra(exalt_lord_house)
        cond3 = exalt_in_d9
        present = cond1 or cond2 or cond3
        dw = 1.0 if _is_dasha_active(p, dashas, on_date) else 0.5
        score = 3.0 if present else 0.0
        results.append(
            YogaResult(
                name=f"NB: {p}",
                yoga_type="NeechaBhanga",
                planets=[p],
                present=present,  # noqa: F841
                score=score,
                dasha_weight=dw,
                weighted_score=round(score * dw, 2),
                description=(
                    f"Neecha Bhanga: cond1={cond1} cond2={cond2} d9={cond3}"
                    if present
                    else f"{p} debilitated, no cancellation"
                ),
                source="BPHS Ch.30; Uttara Kalamrita Ch.4",
            )
        )
    return results


# ── Rasi Drishti (12×12 lookup matrix from CALC_RasiDrishti) ─────────────────
# From sign (row) → aspects which signs (Y=True)
_RASI_DRISHTI = {
    0: {4, 7, 10},  # Aries  → Leo, Scorpio, Aquarius
    1: {3, 6, 9},  # Taurus → Cancer, Libra, Capricorn
    2: {5, 8, 11},  # Gemini → Virgo, Sagittarius, Pisces
    3: {1, 7, 10},  # Cancer → Taurus, Scorpio, Aquarius
    4: {0, 6, 9},  # Leo    → Aries, Libra, Capricorn
    5: {2, 8, 11},  # Virgo  → Gemini, Sagittarius, Pisces
    6: {1, 4, 10},  # Libra  → Taurus, Leo, Aquarius
    7: {0, 3, 9},  # Scorpio → Aries, Cancer, Capricorn
    8: {2, 5, 11},  # Sagittarius → Gemini, Virgo, Pisces
    9: {1, 4, 7},  # Capricorn → Taurus, Leo, Scorpio
    10: {0, 3, 6},  # Aquarius → Aries, Cancer, Libra
    11: {2, 5, 8},  # Pisces → Gemini, Virgo, Sagittarius
}


@dataclass
class RasiDrishtiMap:
    """Per-house Rasi Drishti aspecting signs and planets."""

    house_aspects: dict[
        int, dict
    ]  # house -> {aspecting_signs, benefic_planets, malefic_planets, net}

    def net_modifier(self, house: int) -> float:
        return self.house_aspects.get(house, {}).get("net", 0.0)


_NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


def compute_rasi_drishti(chart) -> RasiDrishtiMap:
    from src.calculations.house_lord import compute_house_map

    compute_house_map(chart)
    lsi = chart.lagna_sign_index

    # Build sign → planets map
    sign_pl: dict[int, list[str]] = {}
    for p, pos in chart.planets.items():
        sign_pl.setdefault(pos.sign_index, []).append(p)

    result = {}
    for h in range(1, 13):
        house_si = (lsi + h - 1) % 12
        aspecting_signs = [
            si for si in range(12) if house_si in _RASI_DRISHTI.get(si, set())
        ]
        benefics = []
        malefics = []
        for asi in aspecting_signs:
            for p in sign_pl.get(asi, []):
                if p in _NAT_BENEFIC:
                    benefics.append(p)
                if p in _NAT_MALEFIC:
                    malefics.append(p)
        net = len(benefics) * 0.5 - len(malefics) * 0.5
        result[h] = {
            "aspecting_signs": aspecting_signs,
            "benefic_planets": benefics,
            "malefic_planets": malefics,
            "net": round(net, 2),
        }
    return RasiDrishtiMap(house_aspects=result)


def compute_bhavat_bhavam(chart) -> dict[int, int]:
    """
    Bhavat Bhavam: for house H, secondary house = (H + H - 1) mod 12.
    H2 → H3, H3 → H5, H4 → H7, H5 → H9, H6 → H11, H7 → H1, etc.
    Returns {house: bhavat_bhavam_house}.
    """
    return {h: ((2 * h - 1) % 12 or 12) for h in range(1, 13)}
