"""Diverse pipeline tests — verify G1-G6 pipeline across golden_50 charts.

Uses the golden_50 subset (50 edge-case-dense charts across all 12 lagnas)
for structural correctness. Tests types, counts, and invariants — NOT
chart-specific values.
"""

from __future__ import annotations

from datetime import date

import pytest

from src.ephemeris import compute_chart
from src.calculations.chart_context import build_chart_context, ChartContext
from src.calculations.unified_engine import evaluate_all_rules, UnifiedResult
from src.calculations.convergence import converge
from src.calculations.temporal_projection import time_project


@pytest.fixture
def chart_and_bd(golden_chart):
    """Compute BirthChart + birth_date from a golden_chart fixture."""
    bd = golden_chart["birth_data"]
    chart = compute_chart(
        year=bd["year"], month=bd["month"], day=bd["day"],
        hour=bd["hour"], lat=bd["lat"], lon=bd["lon"],
        tz_offset=bd["tz_offset"],
    )
    return chart, date(bd["year"], bd["month"], bd["day"])


@pytest.fixture
def ctx(chart_and_bd) -> ChartContext:
    chart, birth_date = chart_and_bd
    return build_chart_context(chart, birth_date=birth_date)


# ---------------------------------------------------------------------------
# G1: ChartContext builds for all charts
# ---------------------------------------------------------------------------

class TestChartContextDiverse:
    def test_builds_without_error(self, chart_and_bd):
        chart, birth_date = chart_and_bd
        ctx = build_chart_context(chart, birth_date=birth_date)
        assert ctx is not None

    def test_house_map_has_12_houses(self, ctx):
        assert len(ctx.house_map.house_sign) == 12
        assert len(ctx.house_map.house_lord) == 12

    def test_dignities_computed_for_all_planets(self, ctx):
        assert len(ctx.dignities) >= 7

    def test_shadbala_computed(self, ctx):
        assert len(ctx.shadbala) >= 7

    def test_ashtakavarga_total(self, ctx):
        assert ctx.ashtakavarga.sarva.total > 0

    def test_dashas_computed(self, ctx):
        assert ctx.dashas is not None
        assert len(ctx.dashas) == 9


# ---------------------------------------------------------------------------
# G3: Unified engine runs for all charts
# ---------------------------------------------------------------------------

class TestUnifiedEngineDiverse:
    def test_evaluates_without_error(self, ctx):
        ur = evaluate_all_rules(ctx)
        assert isinstance(ur, UnifiedResult)

    def test_scoring_results_present(self, ctx):
        ur = evaluate_all_rules(ctx, include_corpus=False)
        assert len(ur.scoring_results) > 0

    def test_all_12_houses_scored(self, ctx):
        ur = evaluate_all_rules(ctx, include_corpus=False)
        d1_results = [r for r in ur.results if r.rule_category == "scoring_rule"]
        houses = {r.house for r in d1_results}
        assert houses == set(range(1, 13))

    def test_version_info_present(self, ctx):
        ur = evaluate_all_rules(ctx)
        assert ur.version.corpus_version
        assert ur.version.schema_version >= 1


# ---------------------------------------------------------------------------
# G5: Convergence works for all charts
# ---------------------------------------------------------------------------

class TestConvergenceDiverse:
    def test_converges_without_error(self, ctx):
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        assert isinstance(conv, list)

    def test_predictions_have_valid_houses(self, ctx):
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        for p in conv:
            assert 1 <= p.house <= 12
            assert p.direction in ("favorable", "unfavorable")
            assert p.convergence_score >= 1

    def test_contra_not_negative(self, ctx):
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        for p in conv:
            assert p.contra_score >= 0


# ---------------------------------------------------------------------------
# G6: Temporal projection works for all charts
# ---------------------------------------------------------------------------

class TestTemporalDiverse:
    def test_projects_without_error(self, ctx, chart_and_bd):
        _, birth_date = chart_and_bd
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        timed = time_project(conv, ctx, birth_date=birth_date)
        assert isinstance(timed, list)

    def test_probabilities_in_range(self, ctx, chart_and_bd):
        _, birth_date = chart_and_bd
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        timed = time_project(conv, ctx, birth_date=birth_date)
        for t in timed:
            for y, p in t.probability_by_year.items():
                assert 0.0 <= p <= 1.0, f"P({y})={p} out of range"

    def test_total_confirmations_non_negative(self, ctx, chart_and_bd):
        _, birth_date = chart_and_bd
        ur = evaluate_all_rules(ctx)
        conv = converge(ur.results, ctx)
        timed = time_project(conv, ctx, birth_date=birth_date)
        for t in timed:
            assert t.total_confirmations >= 1
            assert t.temporal_confirmations >= 0
