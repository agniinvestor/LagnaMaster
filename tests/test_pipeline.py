"""Tests for the production pipeline entry point (D0)."""

from __future__ import annotations

import pytest

from src.pipeline import PipelineResult, run_pipeline


@pytest.fixture
def india_1947_result() -> PipelineResult:
    return run_pipeline(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


class TestPipelineResult:
    def test_returns_pipeline_result(self, india_1947_result):
        assert isinstance(india_1947_result, PipelineResult)

    def test_chart_present(self, india_1947_result):
        assert india_1947_result.chart.lagna_sign == "Taurus"

    def test_ctx_present(self, india_1947_result):
        assert india_1947_result.ctx is not None
        assert india_1947_result.ctx.house_map is not None

    def test_scores_present(self, india_1947_result):
        assert len(india_1947_result.scores.houses) == 12

    def test_unified_present(self, india_1947_result):
        assert len(india_1947_result.unified.results) > 0
        assert len(india_1947_result.unified.scoring_results) > 0
        assert len(india_1947_result.unified.corpus_results) > 0

    def test_predictions_present(self, india_1947_result):
        assert len(india_1947_result.predictions) > 0

    def test_version_present(self, india_1947_result):
        v = india_1947_result.version
        assert v.corpus_version
        assert v.schema_version >= 1
        assert v.weight_version >= 1


class TestPipelineScoresMatch:
    """Verify pipeline scores match standalone score_chart."""

    def test_scores_identical_to_standalone(self, india_1947_result):
        from src.scoring import score_chart

        standalone = score_chart(india_1947_result.chart)
        for h in range(1, 13):
            assert india_1947_result.scores.houses[h].final_score == pytest.approx(
                standalone.houses[h].final_score, abs=1e-6,
            ), f"House {h} score mismatch"


class TestPipelineEndToEnd:
    """Verify the full chain produces meaningful results."""

    def test_predictions_have_timing(self, india_1947_result):
        with_timing = sum(1 for p in india_1947_result.predictions if p.probability_by_year)
        assert with_timing > 0

    def test_predictions_have_convergence(self, india_1947_result):
        max_conv = max(p.convergence_score for p in india_1947_result.predictions)
        assert max_conv >= 2, "Expected at least one prediction with 2+ channel convergence"

    def test_converged_property(self, india_1947_result):
        conv = india_1947_result.converged
        assert len(conv) > 0
        assert all(c.convergence_score >= 1 for c in conv)
