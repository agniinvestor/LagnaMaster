"""src/calculations/scoring_rule_eval.py — Data-driven scoring rule evaluator.

Architecture gap G2: replaces the hardcoded if/else chain in
evaluate_house_detailed() with a dispatch evaluator that reads from
ScoringRule data records.

Each condition_type maps to a small evaluator function.  Adding a new
scoring rule = adding a data record in scoring_rules.py, not writing Python.
"""

from __future__ import annotations

from typing import Optional

from src.corpus.scoring_rules import (
    ScoringRule,
    SCORING_RULES,
    YOGAKARAKA_MULTIPLIER,
)
from src.data.constants import (
    DIG_BALA_PEAK,
    DUSTHANA_HOUSES,
    KENDRA_HOUSES,
    STHIRA_KARAKA,
    TRIKONA_HOUSES,
)

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G2", "session": "S328"}


def evaluate_rule(
    rule: ScoringRule,
    *,
    house: int,
    house_si: int,
    frame_lagna_si: int,
    bhavesh: str,
    bh_house: int,
    chart,
    school: str,
    av_bindus: Optional[dict],
    yogakaraka: Optional[str],
    dusthana_lords: set[str],
    kendra_lords: set[str],
    trikona_lords: set[str],
    is_func_benefic_fn,
    is_func_malefic_fn,
    in_house: list[str],
    bh_cotenants: list[str],
    p_house: dict[str, int],
    sign_pl: dict[int, list[str]],
    shubh_k: bool,
    paap_k: bool,
    fb_aspects_house: list[str],
    fm_aspects_house: list[str],
    fb_aspects_bh: list[str],
    fm_aspects_bh: list[str],
    bh_combust: bool,
    bh_cazimi: bool,
    bh_rx: bool,
    bh_dignity,
    bh_war_loser: bool,
    ctx=None,
) -> float:
    """Evaluate one scoring rule for one house. Returns raw score (before WC multiplier)."""
    from src.calculations.weight_store import get_weight_store
    store = get_weight_store()
    W = store.school_weights(school)
    YKM = YOGAKARAKA_MULTIPLIER.get(school, 1.5)
    w = W.get(rule.weight_key, 0.0)
    ct = rule.condition_type

    if ct == "sign_in_set":
        return w if house_si in rule.params["sign_set"] else 0.0

    if ct == "func_benefic_in_house":
        total = 0.0
        for p in [p for p in in_house if is_func_benefic_fn(p)]:
            mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
            total += w * mult
        return total

    if ct == "func_benefic_aspects_house":
        return w if fb_aspects_house else 0.0

    if ct == "bhavesh_in_house_set":
        hs = rule.params.get("house_set", "")
        exclude = rule.params.get("exclude", "")
        if hs == "kendra_trikona":
            match = bh_house in KENDRA_HOUSES or bh_house in TRIKONA_HOUSES
            if exclude == "dusthana" and bh_house in DUSTHANA_HOUSES:
                match = False
            return w if match else 0.0
        if hs == "dusthana":
            return w if bh_house in DUSTHANA_HOUSES else 0.0
        return 0.0

    if ct == "bhavesh_conjunct_lord_type":
        kt_lords = kendra_lords | trikona_lords
        return w if any(p in kt_lords for p in bh_cotenants) else 0.0

    if ct == "bhavesh_conjunct_func_benefic":
        total = 0.0
        for p in bh_cotenants:
            if is_func_benefic_fn(p):
                mult = YKM if (yogakaraka and p == yogakaraka) else 1.0
                total += w * mult
        return total

    if ct == "func_benefic_aspects_bhavesh":
        return w if fb_aspects_bh else 0.0

    if ct == "shubh_kartari":
        return w if shubh_k else 0.0

    if ct == "func_malefic_in_house":
        malefics_in = [p for p in in_house if is_func_malefic_fn(p)]
        return w * len(malefics_in)

    if ct == "func_malefic_aspects_house":
        return w if fm_aspects_house else 0.0

    if ct == "dusthana_lord_in_house":
        return w if any(p in dusthana_lords for p in in_house) else 0.0

    if ct == "paap_kartari":
        return w if paap_k else 0.0

    if ct == "bhavesh_conjunct_func_malefic":
        malefic_cotenants = [p for p in bh_cotenants if is_func_malefic_fn(p)]
        if not malefic_cotenants:
            return 0.0
        mitigated = False
        if rule.params.get("mitigation_check", False):
            for mc in malefic_cotenants:
                mc_si = chart.planets[mc].sign_index if mc in chart.planets else -1
                from src.calculations.dignity import _NAISARGIKA, EXALT_SIGN
                is_friendly = _NAISARGIKA.get((mc, bhavesh), "Neutral") == "Friend"
                is_exalted = EXALT_SIGN.get(mc) == mc_si
                in_good_house = p_house.get(mc, 0) in KENDRA_HOUSES or p_house.get(mc, 0) in TRIKONA_HOUSES
                if is_friendly or is_exalted or in_good_house:
                    mitigated = True
                    break
        mitigation_factor = rule.params.get("mitigation_factor", 0.5)
        return w * (mitigation_factor if mitigated else 1.0)

    if ct == "func_malefic_aspects_bhavesh":
        return w if fm_aspects_bh else 0.0

    if ct == "bhavesh_conjunct_dusthana_lord":
        if not any(p in dusthana_lords for p in bh_cotenants):
            return 0.0
        bhavesh_is_dusthana = bhavesh in dusthana_lords
        return w * (0.5 if bhavesh_is_dusthana else 1.0)

    if ct == "sthira_karaka_support":
        from src.calculations.multi_axis_scoring import _aspects
        total = 0.0
        for karak in STHIRA_KARAKA.get(house, set()):
            if karak not in chart.planets:
                continue
            karak_si = chart.planets[karak].sign_index
            karak_house = (karak_si - frame_lagna_si) % 12 + 1
            if karak_house == house or _aspects(karak, karak_house, house):
                total += w
        return total

    if ct == "sthira_karaka_dusthana":
        total = 0.0
        for karak in STHIRA_KARAKA.get(house, set()):
            if karak not in chart.planets:
                continue
            karak_si = chart.planets[karak].sign_index
            karak_house = (karak_si - frame_lagna_si) % 12 + 1
            dist = (house - karak_house) % 12 + 1
            if dist in DUSTHANA_HOUSES:
                total += w
        return total

    if ct == "bhavesh_combust":
        if bh_cazimi:
            return rule.params.get("cazimi_score", +0.5)
        if bh_combust and bh_rx:
            return rule.params.get("asta_vakri_score", -0.5)
        if bh_combust:
            return w
        return 0.0

    if ct == "bhavesh_dig_bala":
        return w if DIG_BALA_PEAK.get(bhavesh) == bh_house else 0.0

    if ct == "bhavesh_pushkara":
        try:
            from src.calculations.pushkara_navamsha import is_pushkara_navamsha as is_pushkara
            if bhavesh in chart.planets and is_pushkara(
                chart.planets[bhavesh].sign_index,
                chart.planets[bhavesh].degree_in_sign,
            ):
                return w
        except (ImportError, AttributeError):
            pass
        return 0.0

    if ct == "bhavesh_retrograde":
        return w if bh_rx else 0.0

    if ct == "ashtakavarga_threshold":
        if av_bindus:
            bindus = av_bindus.get(house_si, 0)
            if bindus >= rule.params.get("threshold", 5):
                return w
        return 0.0

    if ct == "bhavesh_dignity_score":
        if bh_dignity is not None:
            from src.calculations.dignity import DIGNITY_SCORE
            return DIGNITY_SCORE.get(bh_dignity, 0.0) * w
        return 0.0

    if ct == "bhavesh_avastha":
        try:
            from src.calculations.avasthas import compute_baaladi, BaaladiAvastha
            if bhavesh in chart.planets:
                baaladi = compute_baaladi(
                    chart.planets[bhavesh].sign_index,
                    chart.planets[bhavesh].degree_in_sign,
                )
                if baaladi == BaaladiAvastha.MRITA:
                    return rule.params.get("mrita_score", -1.5)
                if baaladi == BaaladiAvastha.VRIDDHA:
                    return rule.params.get("vriddha_score", -0.75)
                if baaladi == BaaladiAvastha.BAALA:
                    return rule.params.get("baala_score", -0.25)
        except ImportError:
            pass
        return 0.0

    if ct == "bhavesh_war_loser":
        return rule.params.get("penalty", -1.5) if bh_war_loser else 0.0

    return 0.0


def evaluate_all_scoring_rules(
    *,
    house: int,
    house_si: int,
    frame_lagna_si: int,
    bhavesh: str,
    bh_house: int,
    chart,
    school: str,
    av_bindus: Optional[dict],
    yogakaraka: Optional[str],
    dusthana_lords: set[str],
    kendra_lords: set[str],
    trikona_lords: set[str],
    is_func_benefic_fn,
    is_func_malefic_fn,
    in_house: list[str],
    bh_cotenants: list[str],
    p_house: dict[str, int],
    sign_pl: dict[int, list[str]],
    shubh_k: bool,
    paap_k: bool,
    fb_aspects_house: list[str],
    fm_aspects_house: list[str],
    fb_aspects_bh: list[str],
    fm_aspects_bh: list[str],
    bh_combust: bool,
    bh_cazimi: bool,
    bh_rx: bool,
    bh_dignity,
    bh_war_loser: bool,
    ctx=None,
) -> list[tuple[str, str, float, bool, bool]]:
    """Evaluate all 26 scoring rules for one house.

    Returns list of (rule_id, name, score, is_wide_card, triggered) tuples —
    same format as the old evaluate_house_detailed output.
    """
    results = []
    kwargs = dict(
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
    for rule in SCORING_RULES:
        score = evaluate_rule(rule, **kwargs)
        results.append((rule.rule_id, rule.name, score, rule.is_wide_card, score != 0.0))
    return results
