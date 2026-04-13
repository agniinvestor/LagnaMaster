"""Tests for convergence layer (G5)."""

from __future__ import annotations

from datetime import date

import pytest

from src.ephemeris import compute_chart, BirthChart
from src.calculations.chart_context import build_chart_context, ChartContext
from src.calculations.unified_engine import evaluate_all_rules, EvalResult
from src.calculations.convergence import (
    ConvergedPrediction,
    converge,
    _classify_channel,
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


@pytest.fixture
def india_1947_results(india_1947_ctx: ChartContext) -> list[EvalResult]:
    return evaluate_all_rules(india_1947_ctx).results


class TestConvergedPredictionStructure:
    def test_returns_list_of_converged(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        assert isinstance(preds, list)
        assert all(isinstance(p, ConvergedPrediction) for p in preds)

    def test_predictions_have_required_fields(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        for p in preds:
            assert 1 <= p.house <= 12
            assert p.direction in ("favorable", "unfavorable")
            assert p.convergence_score >= 1
            assert isinstance(p.confirmation_sources, list)
            assert isinstance(p.contra_indicators, list)

    def test_sorted_by_convergence_desc(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        scores = [p.convergence_score for p in preds]
        assert scores == sorted(scores, reverse=True)


class TestIndependentChannels:
    def test_max_one_per_channel(self, india_1947_results, india_1947_ctx):
        """Each channel contributes at most once to convergence_score."""
        preds = converge(india_1947_results, india_1947_ctx)
        for p in preds:
            channels = [c.channel for c in p.confirmation_sources]
            assert len(channels) == len(set(channels)), \
                f"H{p.house} {p.direction}: duplicate channels {channels}"

    def test_contra_max_one_per_channel(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        for p in preds:
            channels = [c.channel for c in p.contra_indicators]
            assert len(channels) == len(set(channels)), \
                f"H{p.house} {p.direction}: duplicate contra channels {channels}"

    def test_convergence_score_equals_channel_count(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        for p in preds:
            assert p.convergence_score == len(p.confirmation_sources)
            assert p.contra_score == len(p.contra_indicators)


class TestContraIndicators:
    def test_contras_tracked_separately(self, india_1947_results, india_1947_ctx):
        """Contra-indicators are NOT netted against confirmations."""
        preds = converge(india_1947_results, india_1947_ctx)
        # Find a house with both favorable and unfavorable predictions
        houses_with_both = set()
        for p in preds:
            if p.direction == "favorable":
                for q in preds:
                    if q.house == p.house and q.direction == "unfavorable":
                        houses_with_both.add(p.house)
        assert len(houses_with_both) > 0, "Expected at least one house with both directions"

        for house in houses_with_both:
            fav = [p for p in preds if p.house == house and p.direction == "favorable"][0]
            unfav = [p for p in preds if p.house == house and p.direction == "unfavorable"][0]
            # Favorable's contras should match unfavorable's confirmations
            assert fav.contra_score == unfav.convergence_score
            assert unfav.contra_score == fav.convergence_score

    def test_contra_magnitude_positive(self, india_1947_results, india_1947_ctx):
        preds = converge(india_1947_results, india_1947_ctx)
        for p in preds:
            if p.contra_indicators:
                assert p.total_contra_magnitude > 0


class TestStrengthLabels:
    def test_strength_thresholds(self):
        p = ConvergedPrediction(house=1, direction="favorable", convergence_score=4)
        assert p.strength_label == "very_strong"
        p = ConvergedPrediction(house=1, direction="favorable", convergence_score=3)
        assert p.strength_label == "strong"
        p = ConvergedPrediction(house=1, direction="favorable", convergence_score=2)
        assert p.strength_label == "moderate"
        p = ConvergedPrediction(house=1, direction="favorable", convergence_score=1)
        assert p.strength_label == "weak"


class TestChannelClassification:
    def test_scoring_channel(self):
        r = EvalResult(rule_id="SCORING_R01", source="SCORING", house=1,
                       direction="favorable", magnitude=0.5, confidence=1.0,
                       verse="", rule_category="scoring_rule")
        assert _classify_channel(r) == "scoring"

    def test_bphs_channel(self):
        r = EvalResult(rule_id="BPHS1200", source="BPHS", house=1,
                       direction="favorable", magnitude=0.65, confidence=0.65,
                       verse="Ch.12 v.1", rule_category="corpus_rule")
        assert _classify_channel(r) == "bphs"

    def test_saravali_channel(self):
        r = EvalResult(rule_id="SAR001", source="Saravali", house=1,
                       direction="favorable", magnitude=0.6, confidence=0.6,
                       verse="", rule_category="corpus_rule")
        assert _classify_channel(r) == "saravali"


class TestDeterminism:
    def test_two_runs_identical(self, india_1947_results, india_1947_ctx):
        p1 = converge(india_1947_results, india_1947_ctx)
        p2 = converge(india_1947_results, india_1947_ctx)
        assert len(p1) == len(p2)
        for a, b in zip(p1, p2):
            assert a.house == b.house
            assert a.direction == b.direction
            assert a.convergence_score == b.convergence_score
            assert a.contra_score == b.contra_score
