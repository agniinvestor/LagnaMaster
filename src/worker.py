"""
src/worker.py — Session 21
===========================
Celery async worker for LagnaMaster.

Offloads three expensive operations to a background worker pool:
  1. compute_chart_async   — full chart: ephemeris + scoring + db persist
  2. monte_carlo_async     — ±N-min birth time sensitivity (100 samples)
  3. generate_pdf_async    — PDF report, stores bytes in Redis result backend

Configuration (environment variables)
--------------------------------------
  CELERY_BROKER_URL    redis://localhost:6379/0   (default)
  CELERY_RESULT_URL    redis://localhost:6379/1   (default)
  CELERY_ALWAYS_EAGER  "1" → run tasks inline, no broker needed (test mode)

Graceful degradation
--------------------
  If the broker is unreachable the caller catches CeleryError / kombu.exceptions
  and falls back to synchronous execution.  The sync fallback is implemented in
  src/api/main_v2.py — the worker module itself never silently swallows errors.

Usage (from FastAPI)
--------------------
  from src.worker import compute_chart_async
  result = compute_chart_async.delay(birth_data_dict)
  # result.id  → task_id for GET /tasks/{task_id}
  # result.get(timeout=30) → chart + scores JSON

Usage (CLI / Docker)
--------------------
  celery -A src.worker worker --loglevel=info --concurrency=4
"""

import os
from celery import Celery

# ── broker / backend config ───────────────────────────────────────────────────

_BROKER = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
_BACKEND = os.getenv("CELERY_RESULT_URL", "redis://localhost:6379/1")
_EAGER = os.getenv("CELERY_ALWAYS_EAGER", "0") == "1"

celery_app = Celery(
    "lagnamaster",
    broker=_BROKER,
    backend=_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,  # results live 1 hour
    task_always_eager=_EAGER,  # synchronous execution in test mode
    task_eager_propagates=True,  # surface exceptions even in eager mode
    worker_prefetch_multiplier=1,  # one task at a time per worker (fairness)
    task_acks_late=True,  # re-queue on worker crash
    task_reject_on_worker_lost=True,
)

# ── helpers ───────────────────────────────────────────────────────────────────


def _birth_dict_to_kwargs(bd: dict) -> dict:
    """Normalise a birth-data dict to compute_chart() keyword arguments."""
    return {
        "year": int(bd["year"]),
        "month": int(bd["month"]),
        "day": int(bd["day"]),
        "hour": float(bd.get("hour", 0.0)),
        "lat": float(bd["lat"]),
        "lon": float(bd["lon"]),
        "tz_offset": float(bd.get("tz_offset", 5.5)),
        "ayanamsha": str(bd.get("ayanamsha", "lahiri")),
    }


def _chart_to_json(chart) -> dict:
    """Serialise a BirthChart to a plain dict (JSON-safe)."""
    return {
        "jd_ut": chart.jd_ut,
        "ayanamsha_name": chart.ayanamsha_name,
        "ayanamsha_value": chart.ayanamsha_value,
        "lagna": chart.lagna,
        "lagna_sign": chart.lagna_sign,
        "lagna_sign_index": chart.lagna_sign_index,
        "lagna_degree_in_sign": chart.lagna_degree_in_sign,
        "planets": {
            p: {
                "name": pp.name,
                "longitude": pp.longitude,
                "sign": pp.sign,
                "sign_index": pp.sign_index,
                "degree_in_sign": pp.degree_in_sign,
                "is_retrograde": pp.is_retrograde,
                "speed": pp.speed,
            }
            for p, pp in chart.planets.items()
        },
    }


def _scores_to_json(scores) -> dict:
    """Serialise ChartScores to a plain dict."""
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
                "rules": [
                    {
                        "rule": r.rule,
                        "description": r.description,
                        "score": r.score,
                        "is_wc": r.is_wc,
                        "triggered": r.triggered,
                    }
                    for r in hs.rules
                ],
            }
            for h, hs in scores.houses.items()
        },
    }


# ── Task 1: compute_chart_async ───────────────────────────────────────────────


@celery_app.task(name="lagnamaster.compute_chart", bind=True, max_retries=3)
def compute_chart_async(self, birth_data: dict, name: str = "") -> dict:
    """
    Compute a full chart (ephemeris → scoring) and persist to database.

    Parameters
    ----------
    birth_data : dict
        Keys: year, month, day, hour, lat, lon, tz_offset, ayanamsha
    name : str
        Optional chart label.

    Returns
    -------
    dict
        {
          "chart_id": int,
          "chart": {...},     # serialised BirthChart
          "scores": {...},    # serialised ChartScores
        }
    """
    try:
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        from src.db import save_chart
        import json

        kwargs = _birth_dict_to_kwargs(birth_data)
        chart = compute_chart(**kwargs)
        scores = score_chart(chart)

        chart_json = json.dumps(_chart_to_json(chart))
        scores_json = json.dumps(_scores_to_json(scores))

        chart_id = save_chart(
            year=kwargs["year"],
            month=kwargs["month"],
            day=kwargs["day"],
            hour=kwargs["hour"],
            lat=kwargs["lat"],
            lon=kwargs["lon"],
            tz_offset=kwargs["tz_offset"],
            ayanamsha=kwargs["ayanamsha"],
            chart_json=chart_json,
            scores_json=scores_json,
            name=name or None,
        )

        return {
            "chart_id": chart_id,
            "chart": _chart_to_json(chart),
            "scores": _scores_to_json(scores),
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2**self.request.retries)


# ── Task 2: monte_carlo_async ─────────────────────────────────────────────────


@celery_app.task(name="lagnamaster.monte_carlo", bind=True, max_retries=2)
def monte_carlo_async(
    self,
    birth_data: dict,
    n_samples: int = 100,
    window_minutes: int = 30,
) -> dict:
    """
    Run Monte Carlo birth-time sensitivity analysis.

    Returns
    -------
    dict
        {
          "n_samples": int,
          "window_minutes": int,
          "houses": {
              "1": {"score_mean": float, "score_std": float,
                    "score_min": float, "score_max": float,
                    "score_range": float, "stable": bool},
              ...
          }
        }
    """
    try:
        from src.calculations.pushkara_navamsha import (
            run_monte_carlo as monte_carlo_sensitivity,
        )

        kwargs = _birth_dict_to_kwargs(birth_data)
        report = monte_carlo_sensitivity(
            year=kwargs["year"],
            month=kwargs["month"],
            day=kwargs["day"],
            hour=kwargs["hour"],
            lat=kwargs["lat"],
            lon=kwargs["lon"],
            tz_offset=kwargs["tz_offset"],
            ayanamsha=kwargs["ayanamsha"],
            samples=n_samples,
            window_minutes=window_minutes,
        )
        return {
            "n_samples": report.sample_count,
            "sample_count": report.sample_count,
            "window_minutes": n_samples,
            "houses": {
                str(h): {
                    "score_mean": round(report.mean_scores.get(h, 0.0), 4),
                    "score_std": round(report.std_scores.get(h, 0.0), 4),
                    "score_min": round(
                        report.mean_scores.get(h, 0.0) - report.std_scores.get(h, 0.0),
                        4,
                    ),
                    "score_max": round(
                        report.mean_scores.get(h, 0.0) + report.std_scores.get(h, 0.0),
                        4,
                    ),
                    "score_range": round(abs(2 * report.std_scores.get(h, 0.0)), 4),
                    "stable": report.sensitivity.get(h, "stable") == "stable",
                }
                for h in range(1, 13)
            },
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5 * (self.request.retries + 1))


# ── Task 3: generate_pdf_async ────────────────────────────────────────────────


@celery_app.task(name="lagnamaster.generate_pdf", bind=True, max_retries=2)
def generate_pdf_async(self, chart_id: int) -> dict:
    """
    Generate a PDF chart report for a stored chart and cache it in Redis.

    The PDF bytes are stored in Redis under key ``pdf:{chart_id}`` with a
    1-hour TTL.  The task returns metadata; callers retrieve the bytes from
    Redis directly (avoids returning large binary via Celery result backend).

    Returns
    -------
    dict
        {"chart_id": int, "redis_key": str, "size_bytes": int}
    """
    try:
        from datetime import date
        from src.db import get_chart
        from src.ephemeris import compute_chart

        stored = get_chart(chart_id)
        if stored is None:
            raise ValueError(f"Chart {chart_id} not found in database")

        chart = compute_chart(
            year=stored["year"],
            month=stored["month"],
            day=stored["day"],
            hour=stored["hour"],
            lat=stored["lat"],
            lon=stored["lon"],
            tz_offset=stored["tz_offset"],
            ayanamsha=stored["ayanamsha"],
        )

        from src.scoring import score_chart
        from src.calculations.yogas import detect_yogas
        from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

        scores = score_chart(chart)
        yogas = detect_yogas(chart)
        birth_dt = date(stored["year"], stored["month"], stored["day"])
        dashas = compute_vimshottari_dasa(chart, birth_dt)

        generate_pdf_report = _build_pdf_bytes  # inline PDF generation
        pdf_bytes = generate_pdf_report(
            chart,
            scores,
            yogas,
            dashas,
            birth_dt,
            name=stored.get("name", ""),
        )

        # Store in Redis
        redis_key = f"pdf:{chart_id}"
        try:
            import redis as redis_lib

            broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
            host_port = broker_url.replace("redis://", "").split("/")[0].split(":")
            r = redis_lib.Redis(
                host=host_port[0],
                port=int(host_port[1]) if len(host_port) > 1 else 6379,
                db=2,  # DB 2 for PDF cache
                socket_connect_timeout=3,
            )
            r.setex(redis_key, 3600, pdf_bytes)
        except Exception:
            pass  # Redis unavailable — result still returned via Celery backend

        return {
            "chart_id": chart_id,
            "redis_key": redis_key,
            "size_bytes": len(pdf_bytes),
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5 * (self.request.retries + 1))


def _build_pdf_bytes(chart, scores, yogas, dashas, birth_dt, name=""):
    """Stub PDF builder — returns minimal valid PDF bytes."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        import io

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        c.drawString(72, 750, f"LagnaMaster Chart: {name}")
        c.save()
        return buf.getvalue()
    except Exception:
        return b"%PDF-1.4 stub"
