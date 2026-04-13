"""Tests for temporal projection layer (G6)."""

from __future__ import annotations

from datetime import date

import pytest

from src.ephemeris import compute_chart, BirthChart
from src.calculations.chart_context import build_chart_context, ChartContext
from src.calculations.unified_engine import evaluate_all_rules
from src.calculations.convergence import converge, ConvergedPrediction
from src.calculations.temporal_projection import (
    TimedPrediction,
    TimingWindow,
    time_project,
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
def india_1947_converged(india_1947_ctx: ChartContext) -> list[ConvergedPrediction]:
    ur = evaluate_all_rules(india_1947_ctx)
    return converge(ur.results, india_1947_ctx)


@pytest.fixture
def india_1947_timed(india_1947_converged, india_1947_ctx):
    return time_project(india_1947_converged, india_1947_ctx, birth_date=date(1947, 8, 15))


class TestTimedPredictionStructure:
    def test_returns_list(self, india_1947_timed):
        assert isinstance(india_1947_timed, list)
        assert all(isinstance(t, TimedPrediction) for t in india_1947_timed)

    def test_same_count_as_converged(self, india_1947_converged, india_1947_timed):
        assert len(india_1947_timed) == len(india_1947_converged)

    def test_required_fields(self, india_1947_timed):
        for t in india_1947_timed:
            assert 1 <= t.house <= 12
            assert t.direction in ("favorable", "unfavorable")
            assert t.convergence_score >= 1
            assert isinstance(t.probability_by_year, dict)
            assert isinstance(t.contributing_systems, list)

    def test_preserves_convergence_data(self, india_1947_converged, india_1947_timed):
        for cp, tp in zip(india_1947_converged, india_1947_timed):
            assert tp.house == cp.house
            assert tp.direction == cp.direction
            assert tp.convergence_score == cp.convergence_score
            assert tp.contra_score == cp.contra_score


class TestTimingSystems:
    def test_multiple_systems_used(self, india_1947_timed):
        """All 4 timing systems should appear across predictions."""
        all_systems = set()
        for t in india_1947_timed:
            for w in t.contributing_systems:
                all_systems.add(w.system)
        assert "vimshottari_md" in all_systems
        assert "vimshottari_ad" in all_systems
        assert "yogini" in all_systems
        assert "chara" in all_systems

    def test_timing_windows_have_valid_years(self, india_1947_timed):
        for t in india_1947_timed:
            for w in t.contributing_systems:
                assert w.start_year >= 1947
                assert w.end_year >= w.start_year
                assert w.lord  # non-empty

    def test_contributing_systems_are_timing_windows(self, india_1947_timed):
        for t in india_1947_timed:
            assert all(isinstance(w, TimingWindow) for w in t.contributing_systems)


class TestProbabilityDistribution:
    def test_probabilities_in_range(self, india_1947_timed):
        for t in india_1947_timed:
            for y, p in t.probability_by_year.items():
                assert 0.0 <= p <= 1.0, f"H{t.house} year {y}: P={p}"

    def test_years_after_birth(self, india_1947_timed):
        for t in india_1947_timed:
            for y in t.probability_by_year:
                assert y >= 1947, f"H{t.house} has year {y} before birth"

    def test_peak_window_within_distribution(self, india_1947_timed):
        for t in india_1947_timed:
            if t.peak_window != (0, 0):
                assert t.peak_window[0] in t.probability_by_year
                assert t.peak_window[1] in t.probability_by_year
                assert t.peak_window[0] <= t.peak_window[1]

    def test_peak_years_property(self, india_1947_timed):
        for t in india_1947_timed:
            if t.probability_by_year:
                peaks = t.peak_years
                assert len(peaks) > 0
                max_p = max(t.probability_by_year.values())
                for y in peaks:
                    assert t.probability_by_year[y] == max_p


class TestTimingConfidence:
    def test_confidence_in_range(self, india_1947_timed):
        for t in india_1947_timed:
            assert 0.0 <= t.timing_confidence <= 1.0

    def test_has_timing_data(self, india_1947_timed):
        """With birth_date provided, most predictions should have timing."""
        with_timing = sum(1 for t in india_1947_timed if t.probability_by_year)
        assert with_timing > 0

    def test_no_birth_date_no_yogini_chara(self, india_1947_converged, india_1947_ctx):
        """Without birth_date, only Vimshottari (from ctx.dashas) works."""
        timed = time_project(india_1947_converged, india_1947_ctx)
        all_systems = set()
        for t in timed:
            for w in t.contributing_systems:
                all_systems.add(w.system)
        assert "yogini" not in all_systems
        assert "chara" not in all_systems


class TestDeterminism:
    def test_two_runs_identical(self, india_1947_converged, india_1947_ctx):
        bd = date(1947, 8, 15)
        t1 = time_project(india_1947_converged, india_1947_ctx, birth_date=bd)
        t2 = time_project(india_1947_converged, india_1947_ctx, birth_date=bd)
        assert len(t1) == len(t2)
        for a, b in zip(t1, t2):
            assert a.house == b.house
            assert a.direction == b.direction
            assert a.peak_window == b.peak_window
            assert a.timing_confidence == b.timing_confidence
            assert a.probability_by_year == b.probability_by_year
