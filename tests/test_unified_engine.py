"""Tests for unified evaluation engine (G3+Q4) and weight store (G4+Q6)."""

from __future__ import annotations

from datetime import date

import pytest

from src.ephemeris import compute_chart, BirthChart
from src.calculations.chart_context import build_chart_context, ChartContext
from src.calculations.unified_engine import (
    EvalResult,
    ConditionMet,
    UnifiedResult,
    evaluate_all_rules,
)


@pytest.fixture
def india_1947_chart() -> BirthChart:
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


@pytest.fixture
def india_1947_ctx(india_1947_chart: BirthChart) -> ChartContext:
    return build_chart_context(india_1947_chart, birth_date=date(1947, 8, 15))


class TestEvalResultStructure:
    def test_returns_unified_result(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        assert isinstance(ur, UnifiedResult)
        assert isinstance(ur.results, list)
        assert all(isinstance(r, EvalResult) for r in ur.results)

    def test_both_categories_present(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        categories = {r.rule_category for r in ur.results}
        assert "scoring_rule" in categories
        assert "corpus_rule" in categories

    def test_scoring_only(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        scoring_cats = {"scoring_rule", "scoring_d9", "scoring_d10"}
        assert all(r.rule_category in scoring_cats for r in ur.results)
        assert len(ur.results) > 0

    def test_corpus_only(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_scoring=False)
        assert all(r.rule_category == "corpus_rule" for r in ur.results)
        assert len(ur.results) > 0

    def test_convenience_properties(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        assert len(ur.scoring_results) > 0
        assert len(ur.corpus_results) > 0
        assert len(ur.scoring_results) + len(ur.corpus_results) == len(ur.results)


class TestTraceability:
    """Q4: Every prediction traces from output to verse citation."""

    def test_scoring_rules_have_verse(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        for r in ur.results:
            assert r.verse != "", f"{r.rule_id} missing verse"

    def test_scoring_rules_have_conditions_met(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        for r in ur.results:
            assert len(r.conditions_met) > 0, f"{r.rule_id} missing conditions_met"
            assert all(isinstance(c, ConditionMet) for c in r.conditions_met)

    def test_eval_result_has_required_fields(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        for r in ur.results[:20]:
            assert r.rule_id
            assert r.source
            assert r.direction in ("favorable", "unfavorable", "neutral", "mixed")
            assert isinstance(r.magnitude, (int, float))
            assert isinstance(r.confidence, (int, float))
            assert 0.0 <= r.confidence <= 1.0


class TestScoringRuleResults:
    def test_houses_covered(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        houses = {r.house for r in ur.results}
        assert houses == set(range(1, 13)), "Not all 12 houses covered"

    def test_scoring_rule_ids_prefixed(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        for r in ur.results:
            assert r.rule_id.startswith("SCORING"), f"Bad prefix: {r.rule_id}"

    def test_scoring_magnitude_matches_old_engine(self, india_1947_ctx: ChartContext):
        """Verify unified engine D1 scoring matches the old score_chart output."""
        from src.scoring import score_chart

        old_scores = score_chart(india_1947_ctx.chart, ctx=india_1947_ctx)
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)

        # Sum magnitudes per house — D1 scoring only (exclude D9/D10 varga)
        new_house_scores: dict[int, float] = {}
        for r in ur.results:
            if r.rule_category == "scoring_rule":  # D1 only
                new_house_scores[r.house] = new_house_scores.get(r.house, 0.0) + r.magnitude

        for h in range(1, 13):
            old_score = old_scores.houses[h].final_score
            new_score = max(-10.0, min(10.0, new_house_scores.get(h, 0.0)))
            assert new_score == pytest.approx(old_score, abs=0.01), \
                f"House {h}: old={old_score:.3f} vs unified={new_score:.3f}"

    def test_d9_d10_channels_present(self, india_1947_ctx: ChartContext):
        """D2: Verify D9 and D10 varga channels are evaluated."""
        ur = evaluate_all_rules(india_1947_ctx, include_corpus=False)
        categories = {r.rule_category for r in ur.results}
        assert "scoring_d9" in categories, "D9 varga channel missing"
        assert "scoring_d10" in categories, "D10 varga channel missing"


class TestCorpusRuleResults:
    def test_corpus_rule_count_matches_firing(self, india_1947_ctx: ChartContext):
        from src.calculations.rule_firing import evaluate_chart

        old = evaluate_chart(india_1947_ctx.chart, ctx=india_1947_ctx)
        ur = evaluate_all_rules(india_1947_ctx, include_scoring=False)
        assert len(ur.results) == old.total_fired

    def test_corpus_rule_ids_match(self, india_1947_ctx: ChartContext):
        from src.calculations.rule_firing import evaluate_chart

        old = evaluate_chart(india_1947_ctx.chart, ctx=india_1947_ctx)
        old_ids = {r.rule_id for r in old.fired_rules}
        new_ids = {r.rule_id for r in evaluate_all_rules(india_1947_ctx, include_scoring=False).results}
        assert new_ids == old_ids


class TestVersionAxes:
    """Q6: Three version axes in output."""

    def test_version_info_present(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        v = ur.version
        assert v.corpus_version  # non-empty hash
        assert v.schema_version >= 1
        assert v.weight_version >= 1

    def test_corpus_version_is_hash(self, india_1947_ctx: ChartContext):
        ur = evaluate_all_rules(india_1947_ctx)
        assert len(ur.version.corpus_version) >= 8  # hex hash

    def test_version_deterministic(self, india_1947_ctx: ChartContext):
        v1 = evaluate_all_rules(india_1947_ctx).version
        v2 = evaluate_all_rules(india_1947_ctx).version
        assert v1.corpus_version == v2.corpus_version
        assert v1.schema_version == v2.schema_version
        assert v1.weight_version == v2.weight_version


class TestWeightStore:
    """G4: Weight store API tests."""

    def test_build_weight_store(self):
        from src.calculations.weight_store import build_weight_store
        store = build_weight_store()
        assert store.rule_count > 0
        assert "parashari" in store.schools

    def test_scoring_weights_match_old(self):
        from src.calculations.weight_store import build_weight_store
        from src.corpus.scoring_rules import SCHOOL_WEIGHTS

        store = build_weight_store()
        for school, weights in SCHOOL_WEIGHTS.items():
            for rule_id, expected in weights.items():
                actual = store.get(rule_id, school)
                assert actual == expected, f"{school}/{rule_id}: {actual} != {expected}"

    def test_corpus_weight_is_confidence(self):
        from src.calculations.weight_store import build_weight_store
        store = build_weight_store()
        entry = store.get_entry("BPHS1200")
        assert entry is not None
        assert entry.base_weight == entry.empirical_weight
        assert entry.n == 0  # no observations yet

    def test_version_info(self):
        from src.calculations.weight_store import build_weight_store
        store = build_weight_store()
        v = store.version_info
        assert v.corpus_version
        assert v.schema_version == 1
        assert v.weight_version == 1


class TestDeterminism:
    """Q10: Same chart + same config = identical output."""

    def test_two_runs_identical(self, india_1947_ctx: ChartContext):
        r1 = evaluate_all_rules(india_1947_ctx)
        r2 = evaluate_all_rules(india_1947_ctx)
        assert len(r1.results) == len(r2.results)
        for a, b in zip(r1.results, r2.results):
            assert a.rule_id == b.rule_id
            assert a.house == b.house
            assert a.magnitude == b.magnitude
            assert a.direction == b.direction
