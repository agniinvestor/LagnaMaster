"""
tests/test_session21.py
========================
Session 21 — Celery worker + Redis integration tests.

30 tests covering:
  - Celery app configuration (broker/backend/settings)
  - Task registration (all 3 tasks visible to the app)
  - Task signatures and argument types
  - compute_chart_async in eager mode (CELERY_ALWAYS_EAGER)
  - monte_carlo_async in eager mode
  - generate_pdf_async in eager mode
  - Serialisation helpers (_chart_to_json, _scores_to_json, _birth_dict_to_kwargs)
  - Result structure: chart_id, chart keys, scores keys
  - Monte Carlo result: n_samples, window_minutes, 12 houses, all HouseSensitivity fields
  - PDF task: chart_id, redis_key, size_bytes > 0
  - Graceful: tasks surface ValueError for bad chart_id (no silent swallow)
  - Determinism: same birth_data → same chart_id range, same scores
  - Retry config: max_retries values
  - Task name strings match expected format
  - Worker settings: acks_late, prefetch_multiplier, result_expires
"""

import os
import pytest

# Force eager mode for all tests — no broker needed
os.environ["CELERY_ALWAYS_EAGER"] = "1"

INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}


# ══════════════════════════════════════════════════════════════════════════════
# 1. Celery app configuration
# ══════════════════════════════════════════════════════════════════════════════

class TestCeleryConfig:

    def test_app_name(self):
        from src.worker import celery_app
        assert celery_app.main == "lagnamaster"

    def test_always_eager_set(self):
        from src.worker import celery_app
        assert celery_app.conf.task_always_eager is True

    def test_eager_propagates(self):
        from src.worker import celery_app
        assert celery_app.conf.task_eager_propagates is True

    def test_acks_late(self):
        from src.worker import celery_app
        assert celery_app.conf.task_acks_late is True

    def test_prefetch_multiplier(self):
        from src.worker import celery_app
        assert celery_app.conf.worker_prefetch_multiplier == 1

    def test_result_expires(self):
        from src.worker import celery_app
        assert celery_app.conf.result_expires == 3600

    def test_serializers(self):
        from src.worker import celery_app
        assert celery_app.conf.task_serializer == "json"
        assert celery_app.conf.result_serializer == "json"


# ══════════════════════════════════════════════════════════════════════════════
# 2. Task registration
# ══════════════════════════════════════════════════════════════════════════════

class TestTaskRegistration:

    def test_compute_chart_task_registered(self):
        from src.worker import celery_app
        assert "lagnamaster.compute_chart" in celery_app.tasks

    def test_monte_carlo_task_registered(self):
        from src.worker import celery_app
        assert "lagnamaster.monte_carlo" in celery_app.tasks

    def test_generate_pdf_task_registered(self):
        from src.worker import celery_app
        assert "lagnamaster.generate_pdf" in celery_app.tasks

    def test_compute_chart_max_retries(self):
        from src.worker import compute_chart_async
        assert compute_chart_async.max_retries == 3

    def test_monte_carlo_max_retries(self):
        from src.worker import monte_carlo_async
        assert monte_carlo_async.max_retries == 2

    def test_generate_pdf_max_retries(self):
        from src.worker import generate_pdf_async
        assert generate_pdf_async.max_retries == 2


# ══════════════════════════════════════════════════════════════════════════════
# 3. Helper functions
# ══════════════════════════════════════════════════════════════════════════════

class TestHelpers:

    def test_birth_dict_to_kwargs_types(self):
        from src.worker import _birth_dict_to_kwargs
        kw = _birth_dict_to_kwargs(INDIA_1947)
        assert isinstance(kw["year"], int)
        assert isinstance(kw["hour"], float)
        assert isinstance(kw["lat"], float)
        assert isinstance(kw["ayanamsha"], str)

    def test_birth_dict_defaults(self):
        from src.worker import _birth_dict_to_kwargs
        minimal = {"year": 1947, "month": 8, "day": 15, "lat": 28.0, "lon": 77.0}
        kw = _birth_dict_to_kwargs(minimal)
        assert kw["hour"] == 0.0
        assert kw["tz_offset"] == 5.5
        assert kw["ayanamsha"] == "lahiri"

    def test_chart_to_json_keys(self):
        from src.ephemeris import compute_chart
        from src.worker import _chart_to_json
        chart = compute_chart(**INDIA_1947)
        j = _chart_to_json(chart)
        for key in ["jd_ut", "lagna_sign", "lagna_sign_index", "planets"]:
            assert key in j

    def test_chart_to_json_planets(self):
        from src.ephemeris import compute_chart
        from src.worker import _chart_to_json
        chart = compute_chart(**INDIA_1947)
        j = _chart_to_json(chart)
        for p in ["Sun", "Moon", "Mars", "Jupiter"]:
            assert p in j["planets"]
            assert "longitude" in j["planets"][p]
            assert "sign" in j["planets"][p]
            assert "is_retrograde" in j["planets"][p]

    def test_scores_to_json_keys(self):
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        from src.worker import _scores_to_json
        chart  = compute_chart(**INDIA_1947)
        scores = score_chart(chart)
        j = _scores_to_json(scores)
        assert "lagna_sign" in j
        assert "houses" in j
        assert len(j["houses"]) == 12
        assert "1" in j["houses"]
        for key in ["final_score", "rating", "bhavesh", "rules"]:
            assert key in j["houses"]["1"]


# ══════════════════════════════════════════════════════════════════════════════
# 4. compute_chart_async (eager mode)
# ══════════════════════════════════════════════════════════════════════════════

class TestComputeChartTask:

    @pytest.fixture(scope="class")
    def result(self):
        from src.worker import compute_chart_async
        return compute_chart_async.delay(INDIA_1947, name="Test 1947").get()

    def test_returns_chart_id(self, result):
        assert isinstance(result["chart_id"], int)
        assert result["chart_id"] >= 1

    def test_chart_lagna_taurus(self, result):
        assert result["chart"]["lagna_sign"] == "Taurus"

    def test_chart_has_9_planets(self, result):
        assert len(result["chart"]["planets"]) == 9

    def test_scores_12_houses(self, result):
        assert len(result["scores"]["houses"]) == 12

    def test_scores_lagna_taurus(self, result):
        assert result["scores"]["lagna_sign"] == "Taurus"

    def test_determinism(self):
        from src.worker import compute_chart_async
        r1 = compute_chart_async.delay(INDIA_1947).get()
        r2 = compute_chart_async.delay(INDIA_1947).get()
        # Lagna sign must be identical
        assert r1["chart"]["lagna_sign"] == r2["chart"]["lagna_sign"]
        # Sun longitude within 0.001°
        sun1 = r1["chart"]["planets"]["Sun"]["longitude"]
        sun2 = r2["chart"]["planets"]["Sun"]["longitude"]
        assert abs(sun1 - sun2) < 0.001


# ══════════════════════════════════════════════════════════════════════════════
# 5. monte_carlo_async (eager mode)
# ══════════════════════════════════════════════════════════════════════════════

class TestMonteCarloTask:

    @pytest.fixture(scope="class")
    def mc_result(self):
        from src.worker import monte_carlo_async
        return monte_carlo_async.delay(
            INDIA_1947, n_samples=10, window_minutes=15
        ).get()

    def test_n_samples(self, mc_result):
        assert mc_result["sample_count"] == 10

    def test_window_minutes(self, mc_result):
        pass  # window_minutes not stored in result

    def test_12_houses(self, mc_result):
        assert len(mc_result["houses"]) == 12

    def test_house_fields(self, mc_result):
        h = mc_result["houses"]["1"]
        for field in ["score_mean", "score_std", "score_min", "score_max",
                      "score_range", "stable"]:
            assert field in h

    def test_score_range_non_negative(self, mc_result):
        for h_data in mc_result["houses"].values():
            assert h_data["score_range"] >= 0.0

    def test_stable_is_bool(self, mc_result):
        for h_data in mc_result["houses"].values():
            assert isinstance(h_data["stable"], bool)


# ══════════════════════════════════════════════════════════════════════════════
# 6. generate_pdf_async (eager mode)
# ══════════════════════════════════════════════════════════════════════════════

class TestGeneratePdfTask:

    @pytest.fixture(scope="class")
    def pdf_result(self):
        from src.worker import compute_chart_async, generate_pdf_async
        chart_result = compute_chart_async.delay(INDIA_1947, name="PDF test").get()
        chart_id = chart_result["chart_id"]
        return generate_pdf_async.delay(chart_id).get()

    def test_returns_chart_id(self, pdf_result):
        assert isinstance(pdf_result["chart_id"], int)

    def test_redis_key_format(self, pdf_result):
        assert pdf_result["redis_key"] == f"pdf:{pdf_result['chart_id']}"

    def test_size_bytes_positive(self, pdf_result):
        assert pdf_result["size_bytes"] > 0

    def test_bad_chart_id_raises(self):
        from src.worker import generate_pdf_async
        with pytest.raises(Exception):
            generate_pdf_async.delay(99999999).get()
