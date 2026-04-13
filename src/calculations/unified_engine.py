"""src/calculations/unified_engine.py — Unified rule evaluation engine.

Architecture gap G3 + quality criterion Q4 (traceability).

ONE engine evaluates ALL rules from ALL sources.  Output is a single
``list[EvalResult]`` with full traceability from prediction back to verse.

Public API
----------
  evaluate_all_rules(ctx, weights=None) → list[EvalResult]
  EvalResult — one evaluated rule with traceability

This replaces the two parallel paths:
  - scoring engine (multi_axis_scoring → scoring_rule_eval) — 26 rules
  - corpus engine  (rule_firing → inference) — 6,500+ V2 rules

Both now produce EvalResult objects through a single entry point.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.calculations.chart_context import ChartContext
from src.calculations.weight_store import VersionInfo

_VERIFICATION = {"level": "architecture_spec", "reference": "ARCHITECTURE_CURRENT_VS_TARGET.md G3+Q4", "session": "S328"}


# ---------------------------------------------------------------------------
# EvalResult — the single output type for all rules (Q4 traceability)
# ---------------------------------------------------------------------------

@dataclass
class ConditionMet:
    """One evaluated condition within a rule — Q4 traceability primitive."""
    primitive: str        # condition type (e.g., "planet_in_house", "sign_in_set")
    args: dict            # the arguments checked
    result: bool          # whether it matched


@dataclass
class EvalResult:
    """One evaluated rule with full traceability.

    Every prediction traces from output → rule_id → verse → conditions.

    Trace depths:
      Minimal:  rule_id + verse + direction
      Standard: + conditions_met (planet positions, dignity levels)
      Full:     + every intermediate computation (from ChartContext)
    """
    # Identity
    rule_id: str
    source: str                          # "BPHS", "Saravali", "SCORING", etc.

    # House context
    house: int                           # 1-12, or 0 if not house-specific

    # Outcome
    direction: str                       # favorable|unfavorable|neutral|mixed
    magnitude: float                     # weight × condition score
    confidence: float                    # 0.0-1.0

    # Traceability (Q4)
    verse: str                           # "BPHS Ch.25 v.3" or ""
    predictions: list[dict] = field(default_factory=list)
    conditions_met: list[ConditionMet] = field(default_factory=list)

    # Metadata
    entity_target: str = "native"
    outcome_domains: list[str] = field(default_factory=list)
    signal_group: str = ""
    concordance_count: int = 0
    rule_category: str = ""              # "scoring_rule" | "corpus_rule"


# ---------------------------------------------------------------------------
# Scoring rule adapter — wraps 26 scoring rules as EvalResult
# ---------------------------------------------------------------------------

def _evaluate_scoring_rules(
    ctx: ChartContext,
    school: str = "parashari",
    *,
    frame_lagna_si: int | None = None,
    source_label: str = "SCORING",
    category_label: str = "scoring_rule",
) -> list[EvalResult]:
    """Evaluate the 26 house-scoring rules for all 12 houses.

    Uses the data-driven evaluator from scoring_rule_eval.py and wraps
    results as EvalResult objects.

    Parameters
    ----------
    frame_lagna_si : int, optional
        Override the lagna sign index (for varga evaluation: D9, D10).
        Defaults to the chart's D1 lagna.
    source_label : str
        Source tag for EvalResult (e.g., "SCORING", "SCORING_D9").
    category_label : str
        Category tag for EvalResult.
    """
    from src.calculations.multi_axis_scoring import (
        _prepare_frame_context,
        _aspects,
        _kartari,
    )
    from src.calculations.scoring_rule_eval import evaluate_all_scoring_rules
    from src.corpus.scoring_rules import SCORING_RULES_BY_ID, SCHOOL_WEIGHTS
    from src.data.constants import SIGN_LORDS

    chart = ctx.chart
    if frame_lagna_si is None:
        frame_lagna_si = chart.lagna_sign_index

    if school not in SCHOOL_WEIGHTS:
        school = "parashari"

    yogakaraka, dusthana_lords, kendra_lords, trikona_lords, is_fb, is_fm, av_bindus = \
        _prepare_frame_context(chart, frame_lagna_si, school, ctx=ctx)

    results: list[EvalResult] = []

    for house in range(1, 13):
        house_si = (frame_lagna_si + house - 1) % 12
        bhavesh = SIGN_LORDS[house_si]

        p_house = {
            p: (pos.sign_index - frame_lagna_si) % 12 + 1
            for p, pos in chart.planets.items()
        }
        bh_house = p_house.get(bhavesh, house)

        sign_pl: dict[int, list[str]] = {}
        for p, pos in chart.planets.items():
            sign_pl.setdefault(pos.sign_index, []).append(p)

        in_house = sign_pl.get(house_si, [])
        bh_si = chart.planets[bhavesh].sign_index if bhavesh in chart.planets else house_si
        bh_cotenants = [p for p in sign_pl.get(bh_si, []) if p != bhavesh]

        bh_combust = bh_cazimi = bh_rx = False
        bh_dignity = None
        if bhavesh in chart.planets:
            dig = ctx.dignities.get(bhavesh)
            if dig:
                bh_combust = dig.combust
                bh_cazimi = dig.cazimi
                bh_dignity = dig.dignity
            bh_rx = chart.planets[bhavesh].is_retrograde

        bh_war_loser = bhavesh in getattr(chart, "planetary_war_losers", set())
        shubh_k, paap_k = _kartari(house_si, sign_pl, chart)

        fb_ah = [p for p in chart.planets if is_fb(p) and p not in in_house and _aspects(p, p_house.get(p, 0), house)]
        fm_ah = [p for p in chart.planets if is_fm(p) and p not in in_house and _aspects(p, p_house.get(p, 0), house)]
        fb_abh = [p for p in chart.planets if is_fb(p) and _aspects(p, p_house.get(p, 0), bh_house)]
        fm_abh = [p for p in chart.planets if is_fm(p) and _aspects(p, p_house.get(p, 0), bh_house)]

        rule_tuples = evaluate_all_scoring_rules(
            house=house, house_si=house_si, frame_lagna_si=frame_lagna_si,
            bhavesh=bhavesh, bh_house=bh_house, chart=chart, school=school,
            av_bindus=av_bindus, yogakaraka=yogakaraka,
            dusthana_lords=dusthana_lords, kendra_lords=kendra_lords,
            trikona_lords=trikona_lords,
            is_func_benefic_fn=is_fb, is_func_malefic_fn=is_fm,
            in_house=in_house, bh_cotenants=bh_cotenants,
            p_house=p_house, sign_pl=sign_pl,
            shubh_k=shubh_k, paap_k=paap_k,
            fb_aspects_house=fb_ah, fm_aspects_house=fm_ah,
            fb_aspects_bh=fb_abh, fm_aspects_bh=fm_abh,
            bh_combust=bh_combust, bh_cazimi=bh_cazimi,
            bh_rx=bh_rx, bh_dignity=bh_dignity,
            bh_war_loser=bh_war_loser, ctx=ctx,
        )

        for rule_id, name, score, is_wc, triggered in rule_tuples:
            if not triggered:
                continue
            spec = SCORING_RULES_BY_ID.get(rule_id)
            direction = "favorable" if score > 0 else ("unfavorable" if score < 0 else "neutral")
            effective_mag = score * (0.5 if is_wc else 1.0)

            results.append(EvalResult(
                rule_id=f"{source_label}_{rule_id}",
                source=source_label,
                house=house,
                direction=direction,
                magnitude=effective_mag,
                confidence=1.0,
                verse=spec.verse_ref if spec else "",
                predictions=[],
                conditions_met=[
                    ConditionMet(
                        primitive=spec.condition_type if spec else rule_id,
                        args={"house": house, "bhavesh": bhavesh, "school": school},
                        result=True,
                    ),
                ],
                entity_target="native",
                outcome_domains=[],
                rule_category=category_label,
            ))

    return results


# ---------------------------------------------------------------------------
# Corpus rule adapter — wraps FiredRule objects as EvalResult
# ---------------------------------------------------------------------------

def _evaluate_corpus_rules(
    ctx: ChartContext,
) -> list[EvalResult]:
    """Evaluate all corpus rules and wrap as EvalResult objects.

    D1: Looks up verse_ref from the corpus RuleRecord.
    D4: Populates conditions_met from primary_condition for legacy rules.
    """
    from src.calculations.rule_firing import evaluate_chart
    from src.corpus.combined_corpus import build_corpus

    firing_result = evaluate_chart(ctx.chart, ctx=ctx)

    # D1: Build rule lookup for verse_ref + primary_condition
    corpus = build_corpus()
    rule_lookup: dict[str, object] = {r.rule_id: r for r in corpus.all()}

    results: list[EvalResult] = []
    for fired in firing_result.fired_rules:
        direction = fired.outcome_direction or "neutral"

        # D1: Lookup verse_ref from corpus record
        record = rule_lookup.get(fired.rule_id)
        verse = getattr(record, "verse_ref", "") if record else ""

        # D4: Extract conditions from firing context OR primary_condition
        conditions_met: list[ConditionMet] = []
        if fired.context and isinstance(fired.context, dict):
            cond_data = fired.context.get("conditions", {})
            for cond_name, cond_val in cond_data.items():
                conditions_met.append(ConditionMet(
                    primitive=cond_name,
                    args=cond_val if isinstance(cond_val, dict) else {"value": cond_val},
                    result=True,
                ))

        # D4: If no conditions from firing context, extract from primary_condition
        if not conditions_met and record:
            pc = getattr(record, "primary_condition", None)
            if pc and isinstance(pc, dict):
                # V2 structured conditions
                conds = pc.get("conditions", [])
                if isinstance(conds, list):
                    for c in conds:
                        if isinstance(c, dict) and "type" in c:
                            conditions_met.append(ConditionMet(
                                primitive=c["type"],
                                args={k: v for k, v in c.items() if k != "type"},
                                result=True,
                            ))
                # Legacy placement-based conditions
                if not conditions_met:
                    planet = pc.get("planet", "")
                    ptype = pc.get("placement_type", "")
                    pval = pc.get("placement_value", [])
                    if planet or ptype:
                        conditions_met.append(ConditionMet(
                            primitive=ptype or "placement",
                            args={"planet": planet, "value": pval},
                            result=True,
                        ))

        results.append(EvalResult(
            rule_id=fired.rule_id,
            source=fired.source,
            house=fired.house,
            direction=direction,
            magnitude=fired.confidence,
            confidence=fired.confidence,
            verse=verse,
            predictions=fired.predictions,
            conditions_met=conditions_met,
            entity_target=fired.entity_target,
            outcome_domains=fired.outcome_domains,
            signal_group=fired.signal_group,
            concordance_count=fired.concordance_count,
            rule_category="corpus_rule",
        ))

    return results


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

@dataclass
class UnifiedResult:
    """Complete output from the unified engine with version info (Q6).

    Carries both the evaluated rules and the three version axes needed
    for reproducibility.
    """
    results: list[EvalResult]
    version: "VersionInfo"

    @property
    def scoring_results(self) -> list[EvalResult]:
        return [r for r in self.results if r.rule_category in ("scoring_rule", "scoring_d9", "scoring_d10")]

    @property
    def corpus_results(self) -> list[EvalResult]:
        return [r for r in self.results if r.rule_category == "corpus_rule"]


def evaluate_all_rules(
    ctx: ChartContext,
    *,
    school: str = "parashari",
    include_scoring: bool = True,
    include_corpus: bool = True,
) -> UnifiedResult:
    """Evaluate ALL rules against a chart — single entry point.

    Runs both the scoring engine (26 house-scoring rules) and the corpus
    engine (6,500+ V2 rules), producing a unified ``UnifiedResult``
    with full traceability (Q4) and version info (Q6).

    Parameters
    ----------
    ctx : ChartContext
        Pre-computed chart context (from build_chart_context).
    school : str
        School for scoring rules (parashari/kp/jaimini).
    include_scoring : bool
        If True, evaluate the 26 house-scoring rules.
    include_corpus : bool
        If True, evaluate the V2 corpus rules.

    Returns
    -------
    UnifiedResult
        Every fired rule with traceability + three version axes.
    """
    from src.calculations.weight_store import get_weight_store

    store = get_weight_store()
    results: list[EvalResult] = []

    if include_scoring:
        # D1 natal (primary lagna)
        results.extend(_evaluate_scoring_rules(ctx, school=school))

        # D2: D9/D10 varga natal channels
        d9 = ctx.vargas.tables.get("D9")
        if d9:
            results.extend(_evaluate_scoring_rules(
                ctx, school=school,
                frame_lagna_si=d9.varga_lagna_sign_index,
                source_label="SCORING_D9",
                category_label="scoring_d9",
            ))
        d10 = ctx.vargas.tables.get("D10")
        if d10:
            results.extend(_evaluate_scoring_rules(
                ctx, school=school,
                frame_lagna_si=d10.varga_lagna_sign_index,
                source_label="SCORING_D10",
                category_label="scoring_d10",
            ))

    if include_corpus:
        results.extend(_evaluate_corpus_rules(ctx))

    return UnifiedResult(
        results=results,
        version=store.version_info,
    )
