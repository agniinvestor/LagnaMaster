"""
src/worker.py — LagnaMaster Session 21
Celery async worker configuration and task definitions.

Tasks
-----
compute_monte_carlo_task   Run 100-sample Monte Carlo in background
generate_pdf_task          Generate PDF chart report in background
compute_chart_task         Compute ephemeris + scores asynchronously

Environment variables
---------------------
CELERY_BROKER_URL   Redis broker  (default redis://localhost:6379/1)
CELERY_RESULT_URL   Redis backend (default redis://localhost:6379/2)

Usage
-----
    # Start workers
    celery -A src.worker worker --loglevel=info --concurrency=4

    # In application code
    from src.worker import compute_monte_carlo_task
    result = compute_monte_carlo_task.delay(year, month, day, hour, lat, lon, tz, ayanamsha)
    mc = result.get(timeout=30)   # blocks until done

    # Non-blocking (fire and forget, poll later)
    task = compute_monte_carlo_task.apply_async(
        args=[year, month, day, hour, lat, lon, tz, ayanamsha],
        countdown=0,
    )
    status = task.status   # "PENDING" | "STARTED" | "SUCCESS" | "FAILURE"
    if status == "SUCCESS":
        mc = task.result
"""

from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any

from celery import Celery

# ── app factory ───────────────────────────────────────────────────────────────

BROKER = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
BACKEND = os.environ.get("CELERY_RESULT_URL", "redis://localhost:6379/2")

celery_app = Celery(
    "lagnamaster",
    broker=BROKER,
    backend=BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    # Retry policy
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # Result TTL: keep for 1 hour
    result_expires=3600,
    # Route heavy tasks to dedicated queue
    task_routes={
        "src.worker.compute_monte_carlo_task": {"queue": "heavy"},
        "src.worker.generate_pdf_task": {"queue": "heavy"},
        "src.worker.compute_chart_task": {"queue": "default"},
    },
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _mc_to_dict(mc) -> dict:
    """Serialise MonteCarloResult to a plain JSON-safe dict."""
    return {
        "base_scores": mc.base_scores,
        "mean_scores": mc.mean_scores,
        "std_scores": mc.std_scores,
        "sensitivity": mc.sensitivity,
        "sample_count": mc.sample_count,
    }


def _chart_to_dict(chart) -> dict:
    return {
        "jd_ut": chart.jd_ut,
        "ayanamsha_name": chart.ayanamsha_name,
        "ayanamsha_value": chart.ayanamsha_value,
        "lagna": chart.lagna,
        "lagna_sign": chart.lagna_sign,
        "lagna_sign_index": chart.lagna_sign_index,
        "lagna_degree_in_sign": chart.lagna_degree_in_sign,
        "planets": {
            name: {
                "name": p.name,
                "longitude": p.longitude,
                "sign": p.sign,
                "sign_index": p.sign_index,
                "degree_in_sign": p.degree_in_sign,
                "is_retrograde": p.is_retrograde,
                "speed": p.speed,
            }
            for name, p in chart.planets.items()
        },
    }


def _scores_to_dict(scores) -> dict:
    return {
        "lagna_sign": scores.lagna_sign,
        "houses": {
            str(h): {
                "house": hs.house,
                "domain": hs.domain,
                "bhavesh": hs.bhavesh,
                "bhavesh_house": hs.bhavesh_house,
                "raw_score": hs.raw_score,
                "final_score": hs.final_score,
                "rating": hs.rating,
            }
            for h, hs in scores.houses.items()
        },
    }


# ── tasks ─────────────────────────────────────────────────────────────────────

@celery_app.task(
    name="src.worker.compute_monte_carlo_task",
    bind=True,
    max_retries=2,
    default_retry_delay=5,
)
def compute_monte_carlo_task(
    self,
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
) -> dict:
    """Run Monte Carlo birth-time sensitivity analysis asynchronously.

    Returns a JSON-safe dict matching MonteCarloResult fields.
    """
    try:
        from src.calculations.pushkara_navamsha import run_monte_carlo
        mc = run_monte_carlo(
            year, month, day, hour, lat, lon, tz_offset, ayanamsha,
            samples=samples, window_minutes=window_minutes,
        )
        return _mc_to_dict(mc)
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(
    name="src.worker.generate_pdf_task",
    bind=True,
    max_retries=2,
    default_retry_delay=10,
)
def generate_pdf_task(
    self,
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
    name: str = "",
) -> bytes:
    """Generate a PDF chart report asynchronously.

    Returns raw PDF bytes (base64-encoded when serialised through Celery JSON).
    """
    import base64
    from datetime import date as _date
    try:
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        from src.calculations.vimshottari_dasa import compute_vimshottari_dasa
        from src.calculations.yogas import detect_yogas
        from src.calculations.panchanga import compute_panchanga
        from src.report import generate_pdf_report

        birth_date = _date(year, month, day)
        chart = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
        scores = score_chart(chart)
        dashas = compute_vimshottari_dasa(chart, birth_date)
        yogas = detect_yogas(chart)
        panchanga = compute_panchanga(chart, birth_date)

        pdf_bytes = generate_pdf_report(
            chart, scores, dashas, yogas, panchanga, name=name, birth_date=birth_date
        )
        # JSON serialises as base64 string
        return base64.b64encode(pdf_bytes).decode("ascii")
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(
    name="src.worker.compute_chart_task",
    bind=True,
    max_retries=3,
    default_retry_delay=2,
)
def compute_chart_task(
    self,
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
) -> dict:
    """Compute ephemeris + scores asynchronously.

    Returns JSON-safe dict with 'chart' and 'scores' keys.
    """
    try:
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        chart = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
        scores = score_chart(chart)
        return {
            "chart": _chart_to_dict(chart),
            "scores": _scores_to_dict(scores),
        }
    except Exception as exc:
        raise self.retry(exc=exc)
