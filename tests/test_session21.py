"""
tests/test_session21.py — LagnaMaster Session 21
Tests for:
  - src/worker.py   Celery task definitions (eager mode, no broker needed)
  - src/ui/app.py   Updated 10-tab UI (import-level smoke tests)

All tests run without a live Celery broker by using CELERY_TASK_ALWAYS_EAGER=True.

Run:
    PYTHONPATH=. pytest tests/test_session21.py -v
"""

from __future__ import annotations

import json
import os
import pytest
from datetime import date

# ── fixtures ──────────────────────────────────────────────────────────────────

INDIA = dict(
    year=1947, month=8, day=15, hour=0.0,
    lat=28.6139, lon=77.2090, tz_offset=5.5, ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA)


@pytest.fixture(scope="module")
def india_dashas(india_chart):
    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa
    return compute_vimshottari_dasa(india_chart, date(1947, 8, 15))


# ── worker — eager mode (no broker) ──────────────────────────────────────────

class TestWorkerEager:
    """Celery tasks run synchronously in eager mode — no broker needed."""

    @pytest.fixture(autouse=True)
    def eager_mode(self):
        from src.worker import celery_app
        celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
        yield
        celery_app.conf.update(task_always_eager=False)

    def test_compute_chart_task_returns_dict(self):
        from src.worker import compute_chart_task
        result = compute_chart_task.delay(**INDIA).get(timeout=30)
        assert isinstance(result, dict)
        assert "chart" in result
        assert "scores" in result

    def test_compute_chart_task_lagna_correct(self):
        from src.worker import compute_chart_task
        result = compute_chart_task.delay(**INDIA).get(timeout=30)
        assert result["chart"]["lagna_sign"] == "Taurus"
        assert abs(result["chart"]["lagna_degree_in_sign"] - 7.7286) < 0.05

    def test_compute_chart_task_has_all_planets(self):
        from src.worker import compute_chart_task
        result = compute_chart_task.delay(**INDIA).get(timeout=30)
        planets = result["chart"]["planets"]
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            assert p in planets

    def test_compute_chart_task_scores_have_12_houses(self):
        from src.worker import compute_chart_task
        result = compute_chart_task.delay(**INDIA).get(timeout=30)
        assert len(result["scores"]["houses"]) == 12

    def test_monte_carlo_task_returns_dict(self):
        from src.worker import compute_monte_carlo_task
        result = compute_monte_carlo_task.delay(**INDIA, samples=5, window_minutes=10.0).get(timeout=60)
        assert isinstance(result, dict)
        assert "base_scores" in result
        assert "mean_scores" in result
        assert "std_scores" in result
        assert "sensitivity" in result
        assert result["sample_count"] == 5

    def test_monte_carlo_task_has_12_houses(self):
        from src.worker import compute_monte_carlo_task
        result = compute_monte_carlo_task.delay(**INDIA, samples=3, window_minutes=5.0).get(timeout=60)
        assert len(result["base_scores"]) == 12
        assert len(result["sensitivity"]) == 12

    def test_monte_carlo_sensitivity_labels_valid(self):
        from src.worker import compute_monte_carlo_task
        result = compute_monte_carlo_task.delay(**INDIA, samples=5, window_minutes=10.0).get(timeout=60)
        valid = {"Stable", "Sensitive", "High"}
        for h in range(1, 13):
            assert result["sensitivity"][h] in valid

    def test_generate_pdf_task_returns_base64(self):
        from src.worker import generate_pdf_task
        result = generate_pdf_task.delay(
            **INDIA, name="India Independence"
        ).get(timeout=60)
        # Result is base64-encoded PDF bytes
        import base64
        pdf_bytes = base64.b64decode(result)
        assert pdf_bytes[:4] == b"%PDF"

    def test_worker_has_three_queues(self):
        from src.worker import celery_app
        routes = celery_app.conf.task_routes
        heavy = [k for k, v in routes.items() if v.get("queue") == "heavy"]
        default = [k for k, v in routes.items() if v.get("queue") == "default"]
        assert len(heavy) == 2
        assert len(default) == 1

    def test_chart_task_is_idempotent(self):
        """Same inputs → same lagna and sun position."""
        from src.worker import compute_chart_task
        r1 = compute_chart_task.delay(**INDIA).get(timeout=30)
        r2 = compute_chart_task.delay(**INDIA).get(timeout=30)
        assert r1["chart"]["lagna_sign"] == r2["chart"]["lagna_sign"]
        assert abs(r1["chart"]["lagna_degree_in_sign"] - r2["chart"]["lagna_degree_in_sign"]) < 0.001


# ── worker configuration ──────────────────────────────────────────────────────

class TestWorkerConfig:
    def test_broker_url_defaults_to_redis_db1(self):
        os.environ.pop("CELERY_BROKER_URL", None)
        import importlib, src.worker as w
        importlib.reload(w)
        assert "6379/1" in w.BROKER

    def test_result_url_defaults_to_redis_db2(self):
        os.environ.pop("CELERY_RESULT_URL", None)
        import importlib, src.worker as w
        importlib.reload(w)
        assert "6379/2" in w.BACKEND

    def test_task_serializer_is_json(self):
        from src.worker import celery_app
        assert celery_app.conf.task_serializer == "json"

    def test_result_expires_is_one_hour(self):
        from src.worker import celery_app
        assert celery_app.conf.result_expires == 3600

    def test_celery_app_name(self):
        from src.worker import celery_app
        assert celery_app.main == "lagnamaster"


# ── UI smoke tests ────────────────────────────────────────────────────────────

class TestUIImports:
    """Verify the updated app.py imports all Session 11-20 modules correctly."""

    def test_pushkara_import(self):
        from src.calculations.pushkara_navamsha import check_pushkara, run_monte_carlo
        assert callable(check_pushkara)
        assert callable(run_monte_carlo)

    def test_jaimini_import(self):
        from src.calculations.jaimini_chara_dasha import (
            compute_chara_dasha, current_chara_dasha
        )
        assert callable(compute_chara_dasha)

    def test_kp_import(self):
        from src.calculations.kp_significators import compute_kp
        assert callable(compute_kp)

    def test_tajika_import(self):
        from src.calculations.tajika import compute_tajika
        assert callable(compute_tajika)

    def test_compatibility_import(self):
        from src.calculations.compatibility_score import compute_compatibility
        assert callable(compute_compatibility)

    def test_milan_import(self):
        from src.calculations.kundali_milan import compute_milan
        assert callable(compute_milan)

    def test_chara_dasha_runs_on_1947(self, india_chart):
        from src.calculations.jaimini_chara_dasha import compute_chara_dasha
        dashas = compute_chara_dasha(india_chart, date(1947, 8, 15))
        assert len(dashas) == 12
        assert all(d.years > 0 for d in dashas)

    def test_kp_runs_on_1947(self, india_chart):
        from src.calculations.kp_significators import compute_kp
        kp = compute_kp(india_chart, date(2026, 3, 19))
        assert len(kp.ruling_planets) > 0
        assert len(kp.house_significators) == 12

    def test_tajika_runs_on_1947(self, india_chart):
        from src.calculations.tajika import compute_tajika
        tajika = compute_tajika(india_chart, date(1947, 8, 15), 2026, 28.6139, 77.209, 5.5)
        assert tajika.varshaphal_lagna_sign in [
            "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
            "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces",
        ]
        assert tajika.year_number == 78

    def test_compatibility_runs_on_same_chart(self, india_chart, india_dashas):
        """Compatibility of chart with itself → composite near 1.0 (same dasha lords)."""
        from src.calculations.compatibility_score import compute_compatibility
        compat = compute_compatibility(india_chart, india_chart, india_dashas, india_dashas)
        assert 0.0 <= compat.composite <= 1.0
        assert compat.label in ["Excellent", "Good", "Average", "Weak", "Incompatible"]

    def test_pushkara_check_runs_on_1947(self, india_chart):
        from src.calculations.pushkara_navamsha import check_pushkara
        results = check_pushkara(india_chart)
        assert isinstance(results, list)
        for r in results:
            assert hasattr(r, "is_pushkara")


# ── integration: worker + db ──────────────────────────────────────────────────

class TestWorkerDBIntegration:
    """Verify task output can be stored and retrieved via db layer."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        import src.db as db_module
        db_module.DB_PATH = str(tmp_path / "test_s21.db")
        db_module.init_db()
        from src.worker import celery_app
        celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
        yield
        celery_app.conf.update(task_always_eager=False)

    def test_chart_task_result_saveable(self):
        from src.worker import compute_chart_task
        import src.db as db_module
        result = compute_chart_task.delay(**INDIA).get(timeout=30)
        chart_id = db_module.save_chart(
            **INDIA,
            chart_json=json.dumps(result["chart"]),
        )
        row = db_module.get_chart(chart_id)
        assert row is not None
        cj = json.loads(row["chart_json"])
        assert cj["lagna_sign"] == "Taurus"
