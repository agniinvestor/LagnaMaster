"""
src/calculations/monte_carlo.py — LagnaMaster Session 27
Monte Carlo birth-time sensitivity analysis with Celery chord parallelism.

Two execution modes
-------------------
  sync   runs all samples in the calling thread (Streamlit / tests)
  async  dispatches samples as a Celery chord, returns AsyncResult

The module re-exports the original `run_monte_carlo` from pushkara_navamsha
for backward compatibility, and adds:

  run_monte_carlo_parallel(...)  → MonteCarloResult  (sync, multi-process via Celery eager)
  run_monte_carlo_async(...)     → AsyncResult        (truly async via Celery chord)
  chord_status(task_id)          → dict               (poll result)

Celery chord architecture
--------------------------
  header : N individual `_sample_task` tasks (one per birth-time sample)
  callback: `_aggregate_task` collects all N score dicts → MonteCarloResult

This keeps each individual task tiny (<1s) so they spread across all workers.
The callback runs on whichever worker finishes last. Total wall time ≈ max(sample)
instead of sum(samples), giving near-linear speedup with worker count.

Public API
----------
    run_monte_carlo_parallel(year, month, day, hour, lat, lon,
                             tz_offset, ayanamsha, samples, window_minutes)
        → MonteCarloResult

    run_monte_carlo_async(year, month, day, hour, lat, lon,
                          tz_offset, ayanamsha, samples, window_minutes)
        → celery.result.AsyncResult

    chord_status(task_id: str) → dict  {"state", "result"?, "error"?}
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Optional

# Re-export for backward compat
from src.calculations.pushkara_navamsha import (
    MonteCarloResult,
    run_monte_carlo,
)

try:
    from src.worker import celery_app
    from celery import chord as celery_chord
    _CELERY = True
except ImportError:
    _CELERY = False


# ── Celery tasks ──────────────────────────────────────────────────────────────

if _CELERY:
    @celery_app.task(name="src.calculations.monte_carlo._sample_task", serializer="json")
    def _sample_task(
        year: int, month: int, day: int, hour: float,
        lat: float, lon: float, tz_offset: float, ayanamsha: str,
    ) -> dict[str, float]:
        """Compute scores for a single birth-time sample. Returns {str(house): score}."""
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        chart = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
        scores = score_chart(chart)
        return {str(h): hs.final_score for h, hs in scores.houses.items()}

    @celery_app.task(name="src.calculations.monte_carlo._aggregate_task", serializer="json")
    def _aggregate_task(
        sample_results: list[dict[str, float]],
        base_scores: dict[str, float],
    ) -> dict:
        """Aggregate N sample score dicts into a MonteCarloResult-compatible dict."""
        import statistics
        houses = list(base_scores.keys())
        mean_scores: dict[str, float] = {}
        std_scores: dict[str, float] = {}
        sensitivity: dict[str, str] = {}

        for h in houses:
            vals = [r[h] for r in sample_results if h in r]
            if not vals:
                vals = [base_scores[h]]
            mean_scores[h] = statistics.mean(vals)
            std = statistics.stdev(vals) if len(vals) > 1 else 0.0
            std_scores[h] = std
            if std < 0.5:
                sensitivity[h] = "Stable"
            elif std < 1.5:
                sensitivity[h] = "Sensitive"
            else:
                sensitivity[h] = "High"

        return {
            "base_scores": base_scores,
            "mean_scores": mean_scores,
            "std_scores": std_scores,
            "sensitivity": sensitivity,
            "sample_count": len(sample_results),
        }


# ── public functions ──────────────────────────────────────────────────────────

def run_monte_carlo_parallel(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
    samples: int = 100,
    window_minutes: float = 30.0,
) -> MonteCarloResult:
    """
    Run Monte Carlo using Celery chord parallelism.
    In eager mode (tests) this runs synchronously; in production
    tasks are distributed across workers.

    Falls back to the synchronous `run_monte_carlo` if Celery is unavailable.
    """
    if not _CELERY:
        return run_monte_carlo(
            year, month, day, hour, lat, lon, tz_offset, ayanamsha,
            samples=samples, window_minutes=window_minutes,
        )

    from src.ephemeris import compute_chart
    from src.scoring import score_chart

    half = window_minutes / 60.0 / 2.0
    base_chart = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
    base_scores = {str(h): hs.final_score for h, hs in score_chart(base_chart).houses.items()}

    # Build N perturbed hours
    rng = random.Random(42)
    sample_hours = [
        max(0.0, min(23.9999, hour + rng.uniform(-half, half)))
        for _ in range(samples)
    ]

    # Celery chord: N header tasks + 1 aggregating callback
    header = [
        _sample_task.s(year, month, day, h, lat, lon, tz_offset, ayanamsha)
        for h in sample_hours
    ]
    callback = _aggregate_task.s(base_scores)
    result_dict = celery_chord(header)(callback).get(timeout=120)

    return MonteCarloResult(
        base_scores={int(k): v for k, v in result_dict["base_scores"].items()},
        mean_scores={int(k): v for k, v in result_dict["mean_scores"].items()},
        std_scores={int(k): v for k, v in result_dict["std_scores"].items()},
        sensitivity={int(k): v for k, v in result_dict["sensitivity"].items()},
        sample_count=result_dict["sample_count"],
    )


def run_monte_carlo_async(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
    samples: int = 100,
    window_minutes: float = 30.0,
):
    """
    Fire-and-forget: dispatch the chord and return the AsyncResult immediately.
    Poll with chord_status(result.id).
    """
    if not _CELERY:
        raise RuntimeError("Celery is not available")

    from src.ephemeris import compute_chart
    from src.scoring import score_chart

    half = window_minutes / 60.0 / 2.0
    base_chart = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
    base_scores = {str(h): hs.final_score for h, hs in score_chart(base_chart).houses.items()}

    rng = random.Random(42)
    sample_hours = [
        max(0.0, min(23.9999, hour + rng.uniform(-half, half)))
        for _ in range(samples)
    ]

    header = [
        _sample_task.s(year, month, day, h, lat, lon, tz_offset, ayanamsha)
        for h in sample_hours
    ]
    callback = _aggregate_task.s(base_scores)
    return celery_chord(header)(callback)


def chord_status(task_id: str) -> dict:
    """Poll a previously dispatched chord callback task."""
    if not _CELERY:
        return {"state": "UNAVAILABLE", "error": "Celery not configured"}
    result = celery_app.AsyncResult(task_id)
    state = result.state
    if state == "SUCCESS":
        return {"state": "SUCCESS", "result": result.result}
    if state == "FAILURE":
        return {"state": "FAILURE", "error": str(result.result)}
    return {"state": state}


# ── Stub references so imports don't NameError when Celery is unavailable ──────
if not _CELERY:
    class _TaskStub:
        """Placeholder when Celery is not configured."""
        def delay(self, *a, **kw):
            raise RuntimeError("Celery not available")
        def s(self, *a, **kw):
            raise RuntimeError("Celery not available")
    _sample_task    = _TaskStub()   # noqa: F811
    _aggregate_task = _TaskStub()   # noqa: F811
    _sample_task_stub = True
