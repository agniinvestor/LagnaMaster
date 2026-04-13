"""
src/calculations/multi_axis_scoring.py — Canonical Scoring Engine

Runs the 26-rule scoring engine (R01–R24 + D6 Avastha + WL War Loser)
against all 5 lagna axes:
  D1  Natal Rashi lagna   (35% weight in LPI)
  CL  Chandra Lagna       (15% weight)
  SL  Surya Lagna         (10% weight)
  D9  Navamsha            (15% weight)
  D10 Dashamsha           (10% weight)

Uses functional benefic/malefic classification per BPHS Ch.34.
School-specific rule weights (REF_SchoolConfig, fully implemented).
Yogakaraka multiplier: Parashari/KP=1.5×, Jaimini=1.25×.

Public API
----------
  score_axis(chart, frame, school) -> AxisScores
  score_all_axes(chart, school)    -> MultiAxisScores  [deprecated]
  evaluate_house_detailed(...)     -> (float, list[tuple])
"""

from __future__ import annotations
import warnings
from dataclasses import dataclass
from typing import Optional
from src.data.constants import DIG_BALA_PEAK, DUSTHANA_HOUSES, KENDRA_HOUSES, SIGN_LORDS, SIGN_NAMES, STHIRA_KARAKA, TRIKONA_HOUSES

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
        "R10": -1.0,
        "R11": -1.25,
        "R12": -0.75,
        "R13": -1.0,
        "R14": -0.5,
        "R15": -2.0,
        "R16": -0.75,
        "R17": 0.5,
        "R18": -0.5,
        "R19": -1.0,
        "R20": 0.5,
        "R21": 0.5,
        "R22": 0.25,
        "R23": 0.5,
        "R24": 1.0,
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
        "R10": -1.0,
        "R11": -1.25,
        "R12": -0.75,
        "R13": -1.0,
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
        "R24": 1.0,
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
        "R10": -1.0,
        "R11": -1.0,
        "R12": -0.5,
        "R13": -1.0,
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
        "R24": 1.0,
    },
}
_YK_MULT = {"parashari": 1.5, "kp": 1.5, "jaimini": 1.25}
_WC_RULES = {"R03", "R05", "R07", "R14"}

_GENTLE_SIGNS = {3, 1, 6, 11, 8}  # Cancer, Taurus, Libra, Pisces, Sagittarius


# D10 formula: sign = (si*10 + floor(deg/3)) % 12  for odd sign
# D9 uses varga._d9_sign_index (canonical implementation)


def _d10_sign(longitude: float) -> int:
    si = int(longitude / 30) % 12
    div = int((longitude % 30) / 3)
    if si % 2 == 0:  # odd sign (0-indexed even = 1st, 3rd...)
        return (si * 10 + div) % 12
    else:
        return (si * 10 + (9 - div)) % 12


def _aspects(planet: str, p_house: int, t_house: int) -> bool:
    """Binary aspect check: does planet in p_house aspect t_house?

    Uses the simple Parashari model: 7th for all, plus Mars 4th/8th,
    Jupiter 5th/9th, Saturn 3rd/10th (BPHS Ch.26 v.5).
    For graded aspect strength, use sputa_drishti.get_aspect_strength().
    """
    diff = (t_house - p_house) % 12
    if diff == 6:  # 7th house (0-indexed)
        return True
    _SPECIAL = {"Mars": {3, 7}, "Jupiter": {4, 8}, "Saturn": {2, 9}}
    return diff in _SPECIAL.get(planet, set())


def _kartari(house_si: int, sign_planets: dict, chart=None) -> tuple[bool, bool]:
    """Shubha/Paapa Kartari. Uses chart-conditional BPHS Ch.3 v.11 classification
    when chart is provided (waning Moon = malefic, combust Mercury = malefic)."""
    from src.calculations.dignity import is_natural_benefic, is_natural_malefic
    prev_si = (house_si - 1) % 12
    next_si = (house_si + 1) % 12
    prev_pl = sign_planets.get(prev_si, [])
    next_pl = sign_planets.get(next_si, [])
    shubh = any(is_natural_benefic(p, chart) for p in prev_pl) and any(
        is_natural_benefic(p, chart) for p in next_pl
    )
    paap = any(is_natural_malefic(p, chart) for p in prev_pl) and any(
        is_natural_malefic(p, chart) for p in next_pl
    )
    return shubh, paap


# ---------------------------------------------------------------------------
# Core rule evaluation — single implementation for all scoring paths
# ---------------------------------------------------------------------------


def evaluate_house_detailed(
    house: int,
    frame_lagna_si: int,
    chart,
    school: str,
    av_bindus: Optional[dict],
    yogakaraka: Optional[str],
    dusthana_lords: set[str],
    kendra_lords: set[str],
    trikona_lords: set[str],
    is_func_benefic_fn,
    is_func_malefic_fn,
) -> tuple[float, list[tuple]]:
    """Evaluate all rules for one house.

    Returns (clamped_total, rule_details) where each rule detail is a tuple:
        (name, description, score, is_wc, triggered)

    The score field stores the FULL rule value. For WC rules (R03, R05, R07, R14),
    the aggregation applies a 0.5 multiplier — the caller handles this.
    """
    W = _WEIGHTS[school]
    YKM = _YK_MULT[school]
    house_si = (frame_lagna_si + house - 1) % 12
    bhavesh = SIGN_LORDS[house_si]

    # Planet → house mapping in this frame
    p_house = {
        p: (pos.sign_index - frame_lagna_si) % 12 + 1
        for p, pos in chart.planets.items()
    }
    bh_house = p_house.get(bhavesh, house)

    # Sign → planets list
    sign_pl: dict[int, list[str]] = {}
    for p, pos in chart.planets.items():
        sign_pl.setdefault(pos.sign_index, []).append(p)

    in_house = sign_pl.get(house_si, [])
    benefics_in = [p for p in in_house if is_func_benefic_fn(p)]
    malefics_in = [p for p in in_house if is_func_malefic_fn(p)]

    bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
    bh_cotenants = [p for p in sign_pl.get(bh_si, []) if p != bhavesh]

    # Dignity/combustion data (computed once for R19 + R24)
    bh_combust = False
    bh_cazimi = False
    bh_rx = False
    bh_dignity = None
    if bhavesh in chart.planets:
        from src.calculations.dignity import compute_all_dignities
        dignities = compute_all_dignities(chart)
        dig = dignities.get(bhavesh)
        if dig:
            bh_combust = dig.combust
            bh_cazimi = dig.cazimi
            bh_dignity = dig.dignity
        bh_rx = chart.planets[bhavesh].is_retrograde

    bh_war_loser = bhavesh in getattr(chart, "planetary_war_losers", set())
    shubh_k, paap_k = _kartari(house_si, sign_pl, chart)

    # Aspect helpers
    fb_aspects_house = [
        p for p in chart.planets
        if is_func_benefic_fn(p) and p not in in_house
        and _aspects(p, p_house.get(p, 0), house)
    ]
    fm_aspects_house = [
        p for p in chart.planets
        if is_func_malefic_fn(p) and p not in in_house
        and _aspects(p, p_house.get(p, 0), house)
    ]
    fb_aspects_bh = [
        p for p in chart.planets
        if is_func_benefic_fn(p) and _aspects(p, p_house.get(p, 0), bh_house)
    ]
    fm_aspects_bh = [
        p for p in chart.planets
        if is_func_malefic_fn(p) and _aspects(p, p_house.get(p, 0), bh_house)
    ]

    rules: list[tuple] = []
    kt_lords = kendra_lords | trikona_lords

    # ── R01: Gentle sign in house ──
    r01 = W["R01"] if house_si in _GENTLE_SIGNS else 0.0
    rules.append(("R01", "Gentle sign in house", r01, False, r01 != 0))

    # ── R02: Functional benefic in house (Yogakaraka bonus) ──
    r02 = 0.0
    for p in benefics_in:
        mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
        r02 += W["R02"] * mult
    rules.append(("R02", "Benefic in house", r02, False, r02 != 0))

    # ── R03: Benefic aspects house (WC — binary) ──
    r03 = W["R03"] if fb_aspects_house else 0.0
    rules.append(("R03", "Benefic aspects house", r03, True, r03 != 0))

    # ── R04: Bhavesh in Kendra or Trikona (not Dusthana) ──
    r04 = W["R04"] if (bh_house in KENDRA_HOUSES or bh_house in TRIKONA_HOUSES) and bh_house not in DUSTHANA_HOUSES else 0.0
    rules.append(("R04", "Bhavesh in Kendra/Trikon", r04, False, r04 != 0))

    # ── R05: Bhavesh with Kendra/Trikona lord (WC — binary) ──
    r05 = W["R05"] if any(p in kt_lords for p in bh_cotenants) else 0.0
    rules.append(("R05", "Bhavesh with Kendra/Trikon lord", r05, True, r05 != 0))

    # ── R06: Bhavesh with functional benefic (Yogakaraka bonus) ──
    r06 = 0.0
    for p in bh_cotenants:
        if is_func_benefic_fn(p):
            mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
            r06 += W["R06"] * mult
    rules.append(("R06", "Bhavesh with benefic", r06, False, r06 != 0))

    # ── R07: Benefic aspects Bhavesh sign (WC — binary) ──
    r07 = W["R07"] if fb_aspects_bh else 0.0
    rules.append(("R07", "Benefic aspects Bhavesh sign", r07, True, r07 != 0))

    # ── R08: Bhavesh in Shubh Kartari ──
    r08 = W["R08"] if shubh_k else 0.0
    rules.append(("R08", "Bhavesh in Shubh Kartari", r08, False, r08 != 0))

    # ── R09: Functional malefic in house (per-planet accumulation) ──
    r09 = W["R09"] * len(malefics_in)
    rules.append(("R09", "Malefic in house", r09, False, r09 != 0))

    # ── R10: Malefic aspects house (binary) ──
    r10 = W["R10"] if fm_aspects_house else 0.0
    rules.append(("R10", "Malefic aspects house", r10, False, r10 != 0))

    # ── R11: Dusthana lord in house (binary) ──
    r11 = W["R11"] if any(p in dusthana_lords for p in in_house) else 0.0
    rules.append(("R11", "Dusthana lord in house", r11, False, r11 != 0))

    # ── R12: House in Paap Kartari ──
    r12 = W["R12"] if paap_k else 0.0
    rules.append(("R12", "House in Paap Kartari", r12, False, r12 != 0))

    # ── R13: Bhavesh with functional malefic — BPHS Ch.11 note (b), p.125 ──
    # Mitigated if malefic is (a) friendly, (b) exalted, (c) in kendra/trikona
    r13 = 0.0
    malefic_cotenants = [p for p in bh_cotenants if is_func_malefic_fn(p)]
    if malefic_cotenants:
        mitigated = False
        for mc in malefic_cotenants:
            mc_si = chart.planets[mc].sign_index if mc in chart.planets else -1
            from src.calculations.dignity import _NAISARGIKA, EXALT_SIGN
            is_friendly = _NAISARGIKA.get((mc, bhavesh), "Neutral") == "Friend"
            is_exalted = EXALT_SIGN.get(mc) == mc_si
            in_good_house = p_house.get(mc, 0) in KENDRA_HOUSES or p_house.get(mc, 0) in TRIKONA_HOUSES
            if is_friendly or is_exalted or in_good_house:
                mitigated = True
                break
        r13 = W["R13"] * (0.5 if mitigated else 1.0)
    rules.append(("R13", "Bhavesh with malefic", r13, False, r13 != 0))

    # ── R14: Malefic aspects Bhavesh sign (WC — binary) ──
    r14 = W["R14"] if fm_aspects_bh else 0.0
    rules.append(("R14", "Malefic aspects Bhavesh", r14, True, r14 != 0))

    # ── R15: Bhavesh in Dusthana ──
    r15 = W["R15"] if bh_house in DUSTHANA_HOUSES else 0.0
    rules.append(("R15", "Bhavesh in Dusthana", r15, False, r15 != 0))

    # ── R16: Bhavesh with Dusthana lord — BPHS Ch.11 note (c), p.125 ──
    # Exemption: "If he himself is an evil lord, then some relief can be expected"
    r16 = 0.0
    if any(p in dusthana_lords for p in bh_cotenants):
        bhavesh_is_dusthana_lord = bhavesh in dusthana_lords
        r16 = W["R16"] * (0.5 if bhavesh_is_dusthana_lord else 1.0)
    rules.append(("R16", "Bhavesh with Dusthana lord", r16, False, r16 != 0))

    # ── R17/R18: Sthir Karak — BPHS Ch.32 ──
    # R17: Karak in or aspecting its signified house
    # R18: Karak in dusthana FROM its signified house
    r17 = 0.0
    r18 = 0.0
    for karak in STHIRA_KARAKA.get(house, set()):
        if karak not in chart.planets:
            continue
        karak_si = chart.planets[karak].sign_index
        karak_house = (karak_si - frame_lagna_si) % 12 + 1
        if karak_house == house or _aspects(karak, karak_house, house):
            r17 += W["R17"]
        else:
            dist = (house - karak_house) % 12 + 1
            if dist in DUSTHANA_HOUSES:
                r18 += W["R18"]
    rules.append(("R17", "Sthir Karak in Kendra/Trikon", r17, False, r17 != 0))
    rules.append(("R18", "Sthir Karak in Dusthana", r18, False, r18 != 0))

    # ── R19: Bhavesh combust ──
    r19 = 0.0
    if bh_cazimi:
        r19 = +0.5
    elif bh_combust and bh_rx:
        r19 = -0.5  # Asta Vakri (reduced effect)
    elif bh_combust:
        r19 = W["R19"]
    rules.append(("R19", "Bhavesh combust", r19, False, r19 != 0))

    # ── R20: Bhavesh in Dig Bala house ──
    r20 = W["R20"] if DIG_BALA_PEAK.get(bhavesh) == bh_house else 0.0
    rules.append(("R20", "Bhavesh in Dig Bala house", r20, False, r20 != 0))

    # ── R21: Bhavesh in Pushkara Navamsha ──
    r21 = 0.0
    try:
        from src.calculations.pushkara_navamsha import is_pushkara_navamsha as is_pushkara
        if bhavesh in chart.planets and is_pushkara(
            chart.planets[bhavesh].sign_index, chart.planets[bhavesh].degree_in_sign
        ):
            r21 = W["R21"]
    except (ImportError, AttributeError):
        pass
    rules.append(("R21", "Bhavesh Pada in Pushkara Navamsha", r21, False, r21 != 0))

    # ── R22: Bhavesh retrograde — Phaladeepika Ch.2 v.9 ──
    # Classical texts treat ALL retrograde planets as strong, no inner/outer distinction
    r22 = W["R22"] if bh_rx else 0.0
    rules.append(("R22", "Bhavesh retrograde", r22, False, r22 != 0))

    # ── R23: Ashtakavarga SAV ──
    r23 = 0.0
    if av_bindus:
        bindus = av_bindus.get(house_si, 0)
        if bindus >= 5:
            r23 = W["R23"]
    rules.append(("R23", "Ashtakavarga SAV", r23, False, r23 != 0))

    # ── R24: Bhavesh dignity modifier ──
    r24 = 0.0
    if bh_dignity is not None:
        from src.calculations.dignity import DIGNITY_SCORE
        r24 = DIGNITY_SCORE.get(bh_dignity, 0.0) * W["R24"]
    rules.append(("R24", f"Bhavesh {bhavesh} dignity modifier", r24, False, r24 != 0))

    # ── D6: Avastha-based evaluation — BPHS Ch.11 v.14-16 (pp.123-126) ──
    d6 = 0.0
    try:
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha
        if bhavesh in chart.planets:
            baaladi = compute_baaladi(
                chart.planets[bhavesh].sign_index,
                chart.planets[bhavesh].degree_in_sign,
            )
            if baaladi == BaaladiAvastha.MRITA:
                d6 = -1.5  # "bhava will be destroyed" (Ch.11 p.126)
            elif baaladi == BaaladiAvastha.VRIDDHA:
                d6 = -0.75  # "ineffective from the view point of good results"
            elif baaladi == BaaladiAvastha.BAALA:
                d6 = -0.25  # 1/4 effect — reduced but not destroyed
    except ImportError:
        pass
    rules.append(("D6", "Bhavesh avastha modifier", d6, False, d6 != 0))

    # ── WL: War loser penalty — Saravali Ch.4 v.18-22 ──
    wl = -1.5 if bh_war_loser else 0.0
    rules.append(("WL", "Bhavesh war loser penalty", wl, False, wl != 0))

    # ── Aggregate ──
    total = sum(score * (0.5 if is_wc else 1.0) for _, _, score, is_wc, _ in rules)
    clamped = max(-10.0, min(10.0, total))

    return clamped, rules


def _score_one_house(
    house: int,
    frame_lagna_si: int,
    chart,
    school: str,
    av_bindus: Optional[dict],
    yogakaraka: Optional[str],
    dusthana_lords: set[str],
    kendra_lords: set[str],
    trikona_lords: set[str],
    is_func_benefic_fn,
    is_func_malefic_fn,
) -> float:
    """Score one house, returning only the clamped total."""
    total, _ = evaluate_house_detailed(
        house, frame_lagna_si, chart, school,
        av_bindus, yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
        is_func_benefic_fn, is_func_malefic_fn,
    )
    return total


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


_SIGNS = list(SIGN_NAMES)


def _make_frame_funcs(frame_lagna_si: int, chart, school: str):
    """Return is_func_benefic / is_func_malefic for any frame.

    Uses KNOWN_FUNCTIONAL_MALEFICS (BPHS Ch.34 verse-verified table) as the
    canonical source for both benefic and malefic classification. This ensures
    consistency — the same data drives both checks.
    """
    from src.calculations.functional_dignity import (
        KNOWN_FUNCTIONAL_MALEFICS,
        KNOWN_YOGAKARAKAS,
    )

    malefic_set = set(KNOWN_FUNCTIONAL_MALEFICS.get(frame_lagna_si, []))
    yogakaraka_list = KNOWN_YOGAKARAKAS.get(frame_lagna_si, [])

    def is_func_benefic(planet: str) -> bool:
        if planet in yogakaraka_list:
            return True
        return planet not in malefic_set and planet not in ("Rahu", "Ketu")

    def is_func_malefic(planet: str) -> bool:
        return planet in malefic_set

    return is_func_benefic, is_func_malefic


def _prepare_frame_context(chart, frame_lagna_si: int, school: str):
    """Pre-compute context needed for scoring all 12 houses in a frame.

    Returns (yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
             is_fb, is_fm, av_bindus).
    """
    from src.calculations.ashtakavarga import compute_ashtakavarga
    from src.calculations.multi_lagna import yogakaraka_for_lagna

    yogakaraka = yogakaraka_for_lagna(frame_lagna_si)
    dusthana_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in DUSTHANA_HOUSES}
    kendra_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in KENDRA_HOUSES}
    trikona_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in TRIKONA_HOUSES}
    is_fb, is_fm = _make_frame_funcs(frame_lagna_si, chart, school)

    try:
        av = compute_ashtakavarga(chart)
        av_bindus = {si: av.sarva.bindus[si] for si in range(12)}
    except (ValueError, TypeError):
        av_bindus = None

    return yogakaraka, dusthana_lords, kendra_lords, trikona_lords, is_fb, is_fm, av_bindus


def score_axis(
    chart,
    frame_lagna_si: int,
    axis_name: str,
    school: str = "parashari",
    strict_school: bool = False,
) -> AxisScores:
    """Score 12 houses for a given lagna reference sign."""
    school = school.lower()
    if school not in _WEIGHTS:
        school = "parashari"

    yogakaraka, dusthana_lords, kendra_lords, trikona_lords, is_fb, is_fm, av_bindus = \
        _prepare_frame_context(chart, frame_lagna_si, school)

    scores = {}
    for h in range(1, 13):
        scores[h] = _score_one_house(
            h, frame_lagna_si, chart, school,
            av_bindus, yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
            is_fb, is_fm,
        )

    if strict_school:
        try:
            from src.calculations.school_rules import school_score_adjustment
            scores = {
                h: school_score_adjustment(scores[h], [], school, strict=True)
                for h in scores
            }
        except ImportError:
            pass

    return AxisScores(axis=axis_name, lagna_sign=_SIGNS[frame_lagna_si], scores=scores)


def score_all_axes(
    chart, school: str = "parashari", strict_school: bool = False
) -> MultiAxisScores:
    """Score all 5 axes: D1, Chandra Lagna, Surya Lagna, D9, D10."""
    warnings.warn("score_all_axes is deprecated, use score_chart", DeprecationWarning, stacklevel=2)
    from src.calculations.panchanga import compute_navamsha_chart

    d1_si = chart.lagna_sign_index
    cl_si = chart.planets["Moon"].sign_index
    sl_si = chart.planets["Sun"].sign_index

    d9_map = compute_navamsha_chart(chart)
    d9_lagna_si = d9_map["lagna"] if d9_map and "lagna" in d9_map else chart.lagna_sign_index

    d10_lagna_si = _d10_sign(chart.lagna)

    return MultiAxisScores(
        d1=score_axis(chart, d1_si, "D1", school, strict_school),
        cl=score_axis(chart, cl_si, "CL", school, strict_school),
        sl=score_axis(chart, sl_si, "SL", school, strict_school),
        d9=score_axis(chart, d9_lagna_si, "D9", school, strict_school),
        d10=score_axis(chart, d10_lagna_si, "D10", school, strict_school),
        school=school,
    )
