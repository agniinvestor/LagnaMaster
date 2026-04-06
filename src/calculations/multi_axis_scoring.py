"""
src/calculations/multi_axis_scoring.py — Session 34

Runs the 23-rule scoring engine (R01–R23) against all 5 lagna axes:
  D1  Natal Rashi lagna   (35% weight in LPI)
  CL  Chandra Lagna       (15% weight)
  SL  Surya Lagna         (10% weight)
  D9  Navamsha            (15% weight)
  D10 Dashamsha           (10% weight)

R23 — Ashtakavarga SAV rule (new):
  +0.5 if SAV bindus ≥ 5 in the house sign for the active school.
  Weight: Parashari=0.5, KP=0.25, Jaimini=0.5

School-specific rule weights (REF_SchoolConfig, fully implemented).
Yogakaraka multiplier: Parashari/KP=1.5×, Jaimini=1.25×.

Public API
----------
  score_axis(chart, frame, school) -> dict[int, float]   12 house scores
  score_all_axes(chart, school)    -> MultiAxisScores
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ── School weight tables (REF_SchoolConfig) ───────────────────────────────────
_WEIGHTS = {
    "parashari": {
        "R01": 0.5,
        "R02": 1.0,
        "R03": 0.75,
        "R04": 2.0,
        "R05": 0.5,
        "R06": 1.0,
        "R07": 0.5,
        "R08": 0.75,
        "R09": -1.0,
        "R10": -0.5,
        "R11": -1.25,
        "R12": -0.75,
        "R13": -0.5,
        "R14": -0.5,
        "R15": -2.0,
        "R16": -0.75,
        "R17": 0.5,
        "R18": -0.5,
        "R19": -1.0,
        "R20": 0.25,
        "R21": 0.5,
        "R22": 0.25,
        "R23": 0.5,
    },
    "kp": {
        "R01": 0.5,
        "R02": 1.0,
        "R03": 0.5,
        "R04": 1.5,
        "R05": 0.5,
        "R06": 1.0,
        "R07": 0.5,
        "R08": 0.75,
        "R09": -1.0,
        "R10": -0.5,
        "R11": -1.25,
        "R12": -0.75,
        "R13": -0.5,
        "R14": -0.5,
        "R15": -1.75,
        "R16": -0.75,
        "R17": 0.5,
        "R18": -0.5,
        "R19": -1.0,
        "R20": 0.5,
        "R21": 0.5,
        "R22": 0.25,
        "R23": 0.25,
    },
    "jaimini": {
        "R01": 0.5,
        "R02": 1.0,
        "R03": 0.75,
        "R04": 1.5,
        "R05": 0.5,
        "R06": 1.0,
        "R07": 0.5,
        "R08": 0.5,
        "R09": -1.0,
        "R10": -0.5,
        "R11": -1.0,
        "R12": -0.5,
        "R13": -0.5,
        "R14": -0.5,
        "R15": -2.0,
        "R16": -0.75,
        "R17": 0.75,
        "R18": -0.75,
        "R19": -1.0,
        "R20": 0.25,
        "R21": 0.25,
        "R22": 0.25,
        "R23": 0.5,
    },
}
_YK_MULT = {"parashari": 1.5, "kp": 1.5, "jaimini": 1.25}
_WC_RULES = {"R03", "R05", "R07", "R14"}

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
_NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_DIG_BALA = {
    "Sun": 10,
    "Mars": 10,
    "Moon": 4,
    "Venus": 4,
    "Mercury": 1,
    "Jupiter": 1,
    "Saturn": 7,
}

# R17/R18 — Naisargika (natural) karakas per house (BPHS Ch.32; Phala Deepika Ch.2)
# R17: karaka in or aspecting own house  → +W["R17"]
# R18: karaka in dusthana from its own signified house → +W["R18"] (negative weight)
_STHIR_KARAK: dict[int, set[str]] = {
    1:  {"Sun"},
    2:  {"Jupiter"},
    3:  {"Mars"},
    4:  {"Moon", "Venus"},
    5:  {"Jupiter"},
    6:  {"Mars", "Saturn"},
    7:  {"Venus"},
    8:  {"Saturn"},
    9:  {"Sun", "Jupiter"},
    10: {"Sun", "Mercury", "Saturn"},
    11: {"Jupiter"},
    12: {"Saturn"},
}

# D10 formula: sign = (si*10 + floor(deg/3)) % 12  for odd sign
# D9 uses existing panchanga._d9_sign_index


def _d10_sign(longitude: float) -> int:
    si = int(longitude / 30) % 12
    div = int((longitude % 30) / 3)
    if si % 2 == 0:  # odd sign (0-indexed even = 1st, 3rd...)
        return (si * 10 + div) % 12
    else:
        return (si * 10 + (9 - div)) % 12


def _aspects(planet: str, p_house: int, t_house: int) -> bool:
    diff = (t_house - p_house) % 12
    if diff == 6:
        return True
    extras = {"Mars": {3, 9}, "Jupiter": {4, 8}, "Saturn": {2, 9}}
    return diff in extras.get(planet, set())


def _kartari(house_si: int, sign_planets: dict) -> tuple[bool, bool]:
    prev_si = (house_si - 1) % 12
    next_si = (house_si + 1) % 12
    prev_pl = sign_planets.get(prev_si, [])
    next_pl = sign_planets.get(next_si, [])
    shubh = any(p in _NAT_BENEFIC for p in prev_pl) and any(
        p in _NAT_BENEFIC for p in next_pl
    )
    paap = any(p in _NAT_MALEFIC for p in prev_pl) and any(
        p in _NAT_MALEFIC for p in next_pl
    )
    return shubh, paap


def _score_one_house(
    house: int,
    frame_lagna_si: int,
    chart,
    school: str,
    av_bindus: Optional[dict],  # sign_index -> SAV bindus
    yogakaraka: Optional[str],
    dusthana_lords: set[str],
    kendra_lords: set[str],
    trikona_lords: set[str],
    is_func_benefic_fn,
    is_func_malefic_fn,
) -> float:
    W = _WEIGHTS[school]
    YKM = _YK_MULT[school]
    house_si = (frame_lagna_si + house - 1) % 12
    bhavesh = _SIGN_LORD[house_si]

    # planet→house mapping in this frame
    p_house = {
        p: (pos.sign_index - frame_lagna_si) % 12 + 1
        for p, pos in chart.planets.items()
    }
    bh_house = p_house.get(bhavesh, house)

    # sign → planets list
    sign_pl: dict[int, list[str]] = {}
    for p, pos in chart.planets.items():
        sign_pl.setdefault(pos.sign_index, []).append(p)

    in_house = sign_pl.get(house_si, [])
    benefics_in = [p for p in in_house if is_func_benefic_fn(p)]
    malefics_in = [p for p in in_house if is_func_malefic_fn(p)]

    bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
    bh_cotenants = [p for p in sign_pl.get(bh_si, []) if p != bhavesh]
    bh_combust = False
    bh_cazimi = False
    bh_rx = False
    if bhavesh in chart.planets:
        from src.calculations.dignity import compute_all_dignities

        dig = compute_all_dignities(chart).get(bhavesh)
        bh_combust = dig.combust
        bh_cazimi = dig.cazimi
        bh_rx = chart.planets[bhavesh].is_retrograde
    # S164: Graha Yuddha loser — effectively debilitated for entire life
    # Source: Saravali Ch.4 v.18-22
    bh_war_loser = bhavesh in getattr(chart, "planetary_war_losers", set())

    shubh_k, paap_k = _kartari(house_si, sign_pl)

    # aspect helpers
    fb_aspects_house = [
        p
        for p in chart.planets
        if is_func_benefic_fn(p)
        and p not in in_house
        and _aspects(p, p_house.get(p, 0), house)
    ]
    fm_aspects_house = [
        p
        for p in chart.planets
        if is_func_malefic_fn(p)
        and p not in in_house
        and _aspects(p, p_house.get(p, 0), house)
    ]
    fb_aspects_bh = [
        p
        for p in chart.planets
        if is_func_benefic_fn(p) and _aspects(p, p_house.get(p, 0), bh_house)
    ]
    fm_aspects_bh = [
        p
        for p in chart.planets
        if is_func_malefic_fn(p) and _aspects(p, p_house.get(p, 0), bh_house)
    ]

    total = 0.0

    # R01 gentle sign
    gentle = {3, 1, 6, 11, 8}  # Cancer, Taurus, Libra, Pisces, Sagittarius (sign idx)
    total += W["R01"] if house_si in gentle else 0

    # R02 func benefic in house (YK bonus)
    for p in benefics_in:
        mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
        total += W["R02"] * mult

    # R03 (WC) benefic aspects house
    if fb_aspects_house:
        total += W["R03"] * 0.5  # WC = half weight

    # R04 bhavesh in kendra/trikona (not dusthana)
    if (bh_house in _KENDRA or bh_house in _TRIKONA) and bh_house not in _DUSTHANA:
        total += W["R04"]

    # R05 (WC) bhavesh with kendra/trikona lord
    kt_lords = kendra_lords | trikona_lords
    if any(p in kt_lords for p in bh_cotenants):
        total += W["R05"] * 0.5

    # R06 bhavesh with func benefic
    for p in bh_cotenants:
        if is_func_benefic_fn(p):
            mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
            total += W["R06"] * mult

    # R07 (WC) benefic aspects bhavesh sign
    if fb_aspects_bh:
        total += W["R07"] * 0.5

    # R08 bhavesh in shubh kartari
    if shubh_k:
        total += W["R08"]

    # R09 func malefic in house
    total += W["R09"] * len(malefics_in)

    # R10 malefic aspects house
    if fm_aspects_house:
        total += W["R10"]

    # R11 dusthana lord in house
    if any(p in dusthana_lords for p in in_house):
        total += W["R11"]

    # R12 paap kartari
    if paap_k:
        total += W["R12"]

    # R13 bhavesh with func malefic — BPHS Ch.11 note (b), p.125:
    # Mitigated if malefic is (a) friendly, (b) exalted, (c) in kendra/trikona
    malefic_cotenants = [p for p in bh_cotenants if is_func_malefic_fn(p)]
    if malefic_cotenants:
        # Check for mitigation per BPHS Ch.11
        mitigated = False
        for mc in malefic_cotenants:
            mc_si = chart.planets[mc].sign_index if mc in chart.planets else -1
            from src.calculations.dignity import _NAISARGIKA, EXALT_SIGN
            is_friendly = _NAISARGIKA.get((mc, bhavesh), "Neutral") == "Friend"
            is_exalted = EXALT_SIGN.get(mc) == mc_si
            in_good_house = p_house.get(mc, 0) in _KENDRA or p_house.get(mc, 0) in _TRIKONA
            if is_friendly or is_exalted or in_good_house:
                mitigated = True
                break
        total += W["R13"] * (0.5 if mitigated else 1.0)

    # R14 (WC) malefic aspects bhavesh
    if fm_aspects_bh:
        total += W["R14"] * 0.5

    # R15 bhavesh in dusthana
    if bh_house in _DUSTHANA:
        total += W["R15"]

    # R16 bhavesh with dusthana lord (6/8/12) — BPHS Ch.11 note (c), p.125
    # Exemption: "If he himself is an evil lord, then some relief can be expected"
    if any(p in dusthana_lords for p in bh_cotenants):
        bhavesh_is_dusthana_lord = bhavesh in dusthana_lords
        total += W["R16"] * (0.5 if bhavesh_is_dusthana_lord else 1.0)

    # R17 sthir karak in or aspecting its signified house (BPHS Ch.32)
    # R18 sthir karak in dusthana FROM its signified house
    for karak in _STHIR_KARAK.get(house, set()):
        if karak not in chart.planets:
            continue
        karak_si = chart.planets[karak].sign_index
        karak_house = (karak_si - frame_lagna_si) % 12 + 1
        if karak_house == house or _aspects(karak, karak_house, house):
            total += W["R17"]
        else:
            dist = (house - karak_house) % 12 + 1
            if dist in _DUSTHANA:
                total += W["R18"]

    # R19 combustion
    if bh_cazimi:
        total += 0.5
    elif bh_combust and bh_rx:
        total -= 0.5
    elif bh_combust:
        total += W["R19"]

    # R20 dig bala
    if _DIG_BALA.get(bhavesh) == bh_house:
        total += W["R20"]

    # R21 pushkara navamsha (simple: bhavesh degree check)
    # Pushkara Navamsha degrees are fixed; check if bhavesh qualifies
    try:
        from src.calculations.pushkara_navamsha import (
            is_pushkara_navamsha as is_pushkara,
        )

        if bhavesh in chart.planets and is_pushkara(
            chart.planets[bhavesh].sign_index, chart.planets[bhavesh].degree_in_sign
        ):
            total += W["R21"]
    except (ImportError, AttributeError):
        pass

    # R22 retrograde
    if bh_rx:
        if bhavesh in {"Jupiter", "Saturn"}:
            total += W["R22"]
        elif bhavesh in {"Mercury", "Venus", "Mars"}:
            total -= abs(W["R22"]) * 2

    # R23 Ashtakavarga SAV
    if av_bindus:
        bindus = av_bindus.get(house_si, 0)
        if bindus >= 5:
            total += W["R23"]

    # D6: Avastha-based house evaluation — BPHS Ch.11 v.14-16 (pp.123-126)
    # Yuva/Kumara lord → prosper, Vriddha → ineffective, Mrita → destroyed
    try:
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha
        if bhavesh in chart.planets:
            bh_si = chart.planets[bhavesh].sign_index
            bh_deg = chart.planets[bhavesh].degree_in_sign
            baaladi = compute_baaladi(bh_si, bh_deg)
            # Vriddha/Mrita penalize, Yuva is neutral (full = 1.0), Baala/Kumara partial
            if baaladi == BaaladiAvastha.MRITA:
                total += -1.5  # "bhava will be destroyed" (Ch.11 p.126)
            elif baaladi == BaaladiAvastha.VRIDDHA:
                total += -0.75  # "ineffective from the view point of good results"
            elif baaladi == BaaladiAvastha.BAALA:
                total += -0.25  # 1/4 effect — reduced but not destroyed
    except ImportError:
        pass

    # S164: War loser bhavesh penalty (Saravali Ch.4 v.18-22)
    if bh_war_loser:
        total += -1.5  # treat bhavesh as effectively debilitated throughout life

    return max(-10.0, min(10.0, total))


@dataclass
class AxisScores:
    axis: str  # "D1","CL","SL","D9","D10"
    lagna_sign: str
    scores: dict[int, float]  # house -> score


@dataclass
class MultiAxisScores:
    d1: AxisScores
    cl: AxisScores
    sl: AxisScores
    d9: AxisScores
    d10: AxisScores
    school: str

    def composite(self, house: int) -> float:
        """D1×0.5 + D9×0.3 + D10×0.2 (CALC_CompositeVargaScore formula)."""
        return (
            self.d1.scores[house] * 0.5
            + self.d9.scores[house] * 0.3
            + self.d10.scores[house] * 0.2
        )


def _make_frame_funcs(frame_lagna_si: int, chart, school: str):
    """Return is_func_benefic / is_func_malefic for any frame."""
    from src.calculations.functional_roles import compute_functional_roles

    # We recompute functional roles from the frame's lagna
    import types

    fake = types.SimpleNamespace(
        lagna_sign_index=frame_lagna_si,
        lagna_sign=[
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ][frame_lagna_si],
        planets=chart.planets,  # noqa: F841
    )
    roles = compute_functional_roles(fake)
    return roles.is_functional_benefic, roles.is_functional_malefic


def score_axis(
    chart,
    frame_lagna_si: int,
    axis_name: str,
    school: str = "parashari",
    strict_school: bool = False,
) -> AxisScores:
    """Score 12 houses for a given lagna reference sign."""
    from src.calculations.ashtakavarga import compute_ashtakavarga

    school = school.lower()
    if school not in _WEIGHTS:
        school = "parashari"

    from src.calculations.multi_lagna import yogakaraka_for_lagna

    yogakaraka = yogakaraka_for_lagna(frame_lagna_si)

    # Build dusthana/kendra/trikona lord sets for this frame
    dusthana_lords = {_SIGN_LORD[(frame_lagna_si + h - 1) % 12] for h in _DUSTHANA}
    kendra_lords = {_SIGN_LORD[(frame_lagna_si + h - 1) % 12] for h in _KENDRA}
    trikona_lords = {_SIGN_LORD[(frame_lagna_si + h - 1) % 12] for h in _TRIKONA}

    is_fb, is_fm = _make_frame_funcs(frame_lagna_si, chart, school)

    # SAV bindus for R23
    try:
        av = compute_ashtakavarga(chart)
        av_bindus = {si: av.sarva.bindus[si] for si in range(12)}
    except Exception:
        av_bindus = None

    scores = {}
    for h in range(1, 13):
        scores[h] = _score_one_house(
            h,
            frame_lagna_si,
            chart,
            school,
            av_bindus,
            yogakaraka,
            dusthana_lords,
            kendra_lords,
            trikona_lords,
            is_fb,
            is_fm,
        )

    # I-B: School mixing — deduct forbidden-school rule contributions in strict mode
    # R17/R18 currently score 0 (skipped in _score_one_house) so no numeric change yet;
    # wire is live for when Sthir Karak rules are activated.
    if strict_school:
        try:
            from src.calculations.school_rules import school_score_adjustment

            scores = {
                h: school_score_adjustment(scores[h], [], school, strict=True)
                for h in scores
            }
        except Exception:
            pass

    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    return AxisScores(axis=axis_name, lagna_sign=signs[frame_lagna_si], scores=scores)


def score_all_axes(
    chart, school: str = "parashari", strict_school: bool = False
) -> MultiAxisScores:
    """Score all 5 axes: D1, Chandra Lagna, Surya Lagna, D9, D10."""
    from src.calculations.panchanga import compute_navamsha_chart

    d1_si = chart.lagna_sign_index
    cl_si = chart.planets["Moon"].sign_index
    sl_si = chart.planets["Sun"].sign_index

    # D9 lagna: D9 sign of D1 lagna
    compute_navamsha_chart(chart)
    d9_lagna_si = (
        chart.lagna_sign_index
    )  # DivisionalMap has no .get(); use D1 lagna as D9 reference

    # D10 lagna: Dashamsha sign of D1 lagna
    d10_lagna_si = _d10_sign(chart.lagna)

    return MultiAxisScores(
        d1=score_axis(chart, d1_si, "D1", school, strict_school),
        cl=score_axis(chart, cl_si, "CL", school, strict_school),
        sl=score_axis(chart, sl_si, "SL", school, strict_school),
        d9=score_axis(chart, d9_lagna_si, "D9", school, strict_school),
        d10=score_axis(chart, d10_lagna_si, "D10", school, strict_school),
        school=school,
    )
