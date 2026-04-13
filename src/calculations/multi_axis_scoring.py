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
from typing import TYPE_CHECKING, Optional
from src.data.constants import DUSTHANA_HOUSES, KENDRA_HOUSES, SIGN_LORDS, SIGN_NAMES, TRIKONA_HOUSES

if TYPE_CHECKING:
    pass

# Weight tables and rule definitions are now in src/corpus/scoring_rules.py (G2).
# Evaluation logic is in src/calculations/scoring_rule_eval.py.


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
    *,
    ctx=None,
) -> tuple[float, list[tuple]]:
    """Evaluate all scoring rules for one house.

    Returns (clamped_total, rule_details) where each rule detail is a tuple:
        (rule_id, name, score, is_wc, triggered)

    Rules are defined as DATA in src/corpus/scoring_rules.py and evaluated
    by the dispatch engine in src/calculations/scoring_rule_eval.py.
    No rule logic lives in this function — it only prepares context.
    """
    from src.calculations.scoring_rule_eval import evaluate_all_scoring_rules

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

    bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
    bh_cotenants = [p for p in sign_pl.get(bh_si, []) if p != bhavesh]

    # Dignity/combustion data
    bh_combust = False
    bh_cazimi = False
    bh_rx = False
    bh_dignity = None
    if bhavesh in chart.planets:
        if ctx is not None:
            dignities = ctx.dignities
        else:
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

    # ── Delegate to data-driven evaluator ──
    rules = evaluate_all_scoring_rules(
        house=house, house_si=house_si, frame_lagna_si=frame_lagna_si,
        bhavesh=bhavesh, bh_house=bh_house, chart=chart, school=school,
        av_bindus=av_bindus, yogakaraka=yogakaraka,
        dusthana_lords=dusthana_lords, kendra_lords=kendra_lords,
        trikona_lords=trikona_lords,
        is_func_benefic_fn=is_func_benefic_fn,
        is_func_malefic_fn=is_func_malefic_fn,
        in_house=in_house, bh_cotenants=bh_cotenants,
        p_house=p_house, sign_pl=sign_pl,
        shubh_k=shubh_k, paap_k=paap_k,
        fb_aspects_house=fb_aspects_house,
        fm_aspects_house=fm_aspects_house,
        fb_aspects_bh=fb_aspects_bh,
        fm_aspects_bh=fm_aspects_bh,
        bh_combust=bh_combust, bh_cazimi=bh_cazimi,
        bh_rx=bh_rx, bh_dignity=bh_dignity,
        bh_war_loser=bh_war_loser, ctx=ctx,
    )

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
    *,
    ctx=None,
) -> float:
    """Score one house, returning only the clamped total."""
    total, _ = evaluate_house_detailed(
        house, frame_lagna_si, chart, school,
        av_bindus, yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
        is_func_benefic_fn, is_func_malefic_fn,
        ctx=ctx,
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


def _prepare_frame_context(chart, frame_lagna_si: int, school: str, *, ctx=None):
    """Pre-compute context needed for scoring all 12 houses in a frame.

    Returns (yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
             is_fb, is_fm, av_bindus).

    If *ctx* (ChartContext) is provided, ashtakavarga is read from it
    instead of recomputed.
    """
    from src.calculations.multi_lagna import yogakaraka_for_lagna

    yogakaraka = yogakaraka_for_lagna(frame_lagna_si)
    dusthana_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in DUSTHANA_HOUSES}
    kendra_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in KENDRA_HOUSES}
    trikona_lords = {SIGN_LORDS[(frame_lagna_si + h - 1) % 12] for h in TRIKONA_HOUSES}
    is_fb, is_fm = _make_frame_funcs(frame_lagna_si, chart, school)

    try:
        if ctx is not None:
            av = ctx.ashtakavarga
        else:
            from src.calculations.ashtakavarga import compute_ashtakavarga
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
    *,
    ctx=None,
) -> AxisScores:
    """Score 12 houses for a given lagna reference sign.

    If *ctx* (ChartContext) is provided, pre-computed derived facts are
    used instead of recomputing per house.
    """
    school = school.lower()
    from src.corpus.scoring_rules import SCHOOL_WEIGHTS
    if school not in SCHOOL_WEIGHTS:
        school = "parashari"

    yogakaraka, dusthana_lords, kendra_lords, trikona_lords, is_fb, is_fm, av_bindus = \
        _prepare_frame_context(chart, frame_lagna_si, school, ctx=ctx)

    scores = {}
    for h in range(1, 13):
        scores[h] = _score_one_house(
            h, frame_lagna_si, chart, school,
            av_bindus, yogakaraka, dusthana_lords, kendra_lords, trikona_lords,
            is_fb, is_fm,
            ctx=ctx,
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
