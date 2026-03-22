"""tests/test_session27.py — Session 27 Monte Carlo Celery scaling tests."""

from __future__ import annotations
import pytest

INDIA = dict(
    year=1947,
    month=8,
    day=15,
    hour=0.0,
    lat=28.6139,
    lon=77.2090,
    tz_offset=5.5,
    ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA)


class TestMCImports:
    def test_run_monte_carlo_importable(self):
        from src.calculations.monte_carlo import run_monte_carlo

        assert callable(run_monte_carlo)

    def test_run_monte_carlo_parallel_importable(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel

        assert callable(run_monte_carlo_parallel)

    def test_run_monte_carlo_async_importable(self):
        from src.calculations.monte_carlo import run_monte_carlo_async

        assert callable(run_monte_carlo_async)

    def test_chord_status_importable(self):
        from src.calculations.monte_carlo import chord_status

        assert callable(chord_status)

    def test_monte_carlo_result_reexported(self):
        from src.calculations.monte_carlo import MonteCarloResult

        assert MonteCarloResult is not None


class TestMCParallelEager:
    """Run parallel MC in Celery eager mode — no broker needed."""

    @pytest.fixture(autouse=True)
    def eager(self):
        try:
            from src.worker import celery_app

            celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
            yield
            celery_app.conf.update(task_always_eager=False)
        except ImportError:
            yield

    def test_parallel_returns_monte_carlo_result(self):
        from src.calculations.monte_carlo import (
            run_monte_carlo_parallel,
            MonteCarloResult,
        )

        result = run_monte_carlo_parallel(**INDIA, samples=5, window_minutes=10.0)
        assert isinstance(result, MonteCarloResult)

    def test_parallel_has_12_houses(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel

        result = run_monte_carlo_parallel(**INDIA, samples=5, window_minutes=10.0)
        assert len(result.base_scores) == 12
        assert len(result.mean_scores) == 12
        assert len(result.std_scores) == 12

    def test_parallel_sample_count(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel

        result = run_monte_carlo_parallel(**INDIA, samples=8, window_minutes=15.0)
        assert result.sample_count == 8

    def test_parallel_sensitivity_labels_valid(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel

        result = run_monte_carlo_parallel(**INDIA, samples=5, window_minutes=10.0)
        valid = {"Stable", "Sensitive", "High"}
        for h in range(1, 13):
            assert result.sensitivity[h] in valid

    def test_parallel_base_scores_match_direct(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel
        from src.ephemeris import compute_chart
        from src.scoring import score_chart

        result = run_monte_carlo_parallel(**INDIA, samples=3, window_minutes=5.0)
        chart = compute_chart(**INDIA)
        scores = score_chart(chart)
        for h in range(1, 13):
            assert abs(result.base_scores[h] - scores.houses[h].final_score) < 0.001

    def test_parallel_deterministic(self):
        from src.calculations.monte_carlo import run_monte_carlo_parallel

        r1 = run_monte_carlo_parallel(**INDIA, samples=5, window_minutes=10.0)
        r2 = run_monte_carlo_parallel(**INDIA, samples=5, window_minutes=10.0)
        assert r1.mean_scores == r2.mean_scores

    def test_sample_task_returns_12_scores(self):
        """Individual sample task produces correct shape."""
        from src.calculations.monte_carlo import _sample_task

        try:
            from src.worker import celery_app

            celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
            result = _sample_task.delay(**INDIA).get(timeout=30)
            assert len(result) == 12
        except (ImportError, AttributeError):
            pytest.skip("Celery tasks not available")

    def test_aggregate_task_correct_labels(self):
        """Aggregator produces correct sensitivity labels."""
        from src.calculations.monte_carlo import _aggregate_task

        try:
            from src.worker import celery_app

            celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
            samples = [{"1": 2.0, "2": -1.0} for _ in range(3)]
            base = {"1": 2.0, "2": -1.0}
            result = _aggregate_task.delay(samples, base).get(timeout=10)
            assert "sensitivity" in result
            assert result["sample_count"] == 3
        except (ImportError, AttributeError):
            pytest.skip("Celery tasks not available")


class TestChordStatus:
    def test_status_unavailable_without_celery(self, monkeypatch):
        from src.calculations import monte_carlo as mc_mod

        monkeypatch.setattr(mc_mod, "_CELERY", False)
        status = mc_mod.chord_status("fake-task-id")
        assert status["state"] == "UNAVAILABLE"


class TestMCBackwardCompat:
    """Ensure original run_monte_carlo still works unchanged."""

    def test_original_sync_still_works(self):
        from src.calculations.monte_carlo import run_monte_carlo

        result = run_monte_carlo(**INDIA, samples=3, window_minutes=5.0)
        assert result.sample_count == 3
        assert len(result.base_scores) == 12

    def test_pushkara_run_monte_carlo_still_importable(self):
        from src.calculations.pushkara_navamsha import run_monte_carlo

        assert callable(run_monte_carlo)
