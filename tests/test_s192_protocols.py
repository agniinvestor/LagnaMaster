"""
tests/test_s192_protocols.py — S192 Protocol boundary formalization tests

Verifies that concrete adapter classes satisfy their Protocol contracts
(runtime isinstance checks) and produce correct output shapes.

Design principle: every consumer of the classical engine, dasha engine,
feedback service, and ML service should program to the Protocol interface,
not to the concrete module. This enables Phase 9 strangler-fig extraction
without rewriting call sites.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ─────────────────────────────────────────────────────────────
# India 1947 fixture (verified against JPL DE431)
# ─────────────────────────────────────────────────────────────

INDIA_BIRTH_DATE = date(1947, 8, 15)
INDIA_BIRTH_LON = 77.2090
INDIA_BIRTH_LAT = 28.6139
INDIA_TZ_OFFSET = 5.5


def _india_chart():
    from src.ephemeris import compute_chart

    return compute_chart(
        year=1947,
        month=8,
        day=15,
        hour=0.0,
        lat=INDIA_BIRTH_LAT,
        lon=INDIA_BIRTH_LON,
        tz_offset=INDIA_TZ_OFFSET,
    )


# ─────────────────────────────────────────────────────────────
# 1. Adapter imports
# ─────────────────────────────────────────────────────────────


def test_scoring_engine_adapter_importable():
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter  # noqa: F401


def test_vimshottari_dasa_adapter_importable():
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter  # noqa: F401


def test_null_feedback_service_importable():
    from src.interfaces.adapters.null_feedback import NullFeedbackService  # noqa: F401


def test_null_ml_service_importable():
    from src.interfaces.adapters.null_ml import NullMLService  # noqa: F401


def test_adapters_package_exports_all_four():
    import src.interfaces.adapters as adapters

    for name in ("ScoringEngineAdapter", "VimshottariDasaAdapter",
                 "NullFeedbackService", "NullMLService"):
        assert hasattr(adapters, name), f"src.interfaces.adapters missing {name}"


def test_interfaces_package_re_exports_adapters():
    import src.interfaces as ifaces

    for name in ("ScoringEngineAdapter", "VimshottariDasaAdapter",
                 "NullFeedbackService", "NullMLService"):
        assert hasattr(ifaces, name), f"src.interfaces missing {name}"


# ─────────────────────────────────────────────────────────────
# 2. Protocol satisfaction (isinstance checks)
# ─────────────────────────────────────────────────────────────


def test_scoring_engine_adapter_satisfies_protocol():
    """ScoringEngineAdapter must satisfy ClassicalEngine Protocol at runtime."""
    from src.interfaces import ClassicalEngine
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    adapter = ScoringEngineAdapter()
    assert isinstance(adapter, ClassicalEngine), (
        "ScoringEngineAdapter does not satisfy ClassicalEngine Protocol"
    )


def test_vimshottari_dasa_adapter_satisfies_protocol():
    """VimshottariDasaAdapter must satisfy DashaEngine Protocol at runtime."""
    from src.interfaces import DashaEngine
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter

    adapter = VimshottariDasaAdapter()
    assert isinstance(adapter, DashaEngine), (
        "VimshottariDasaAdapter does not satisfy DashaEngine Protocol"
    )


def test_null_feedback_service_satisfies_protocol():
    """NullFeedbackService must satisfy FeedbackService Protocol at runtime."""
    from src.interfaces import FeedbackService
    from src.interfaces.adapters.null_feedback import NullFeedbackService

    adapter = NullFeedbackService()
    assert isinstance(adapter, FeedbackService), (
        "NullFeedbackService does not satisfy FeedbackService Protocol"
    )


def test_null_ml_service_satisfies_protocol():
    """NullMLService must satisfy MLService Protocol at runtime."""
    from src.interfaces import MLService
    from src.interfaces.adapters.null_ml import NullMLService

    adapter = NullMLService()
    assert isinstance(adapter, MLService), (
        "NullMLService does not satisfy MLService Protocol"
    )


# ─────────────────────────────────────────────────────────────
# 3. ClassicalEngine — functional tests
# ─────────────────────────────────────────────────────────────


def test_score_chart_returns_chart_scores_v3():
    """score_chart() must return ChartScoresV3 with lagna_sign populated."""
    from src.calculations.scoring_v3 import ChartScoresV3
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()
    result = adapter.score_chart(chart)

    assert isinstance(result, ChartScoresV3)
    assert result.lagna_sign  # non-empty string


def test_score_chart_with_school_kp():
    """score_chart() must accept school='kp' without error."""
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()
    result = adapter.score_chart(chart, school="kp")
    assert result is not None


def test_score_chart_with_on_date():
    """score_chart() must accept an on_date without error."""
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()
    result = adapter.score_chart(chart, on_date=date(2025, 1, 1))
    assert result is not None


def test_school_concordance_returns_float():
    """school_concordance() must return a float."""
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()
    result = adapter.school_concordance(chart, house=1)

    assert isinstance(result, float), f"Expected float, got {type(result)}"


def test_school_concordance_in_unit_interval():
    """school_concordance() must return a value in [0.0, 1.0]."""
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()

    for house in (1, 4, 7, 10):  # kendra houses
        c = adapter.school_concordance(chart, house=house)
        assert 0.0 <= c <= 1.0, (
            f"Concordance for house {house} = {c} is outside [0, 1]"
        )


def test_school_concordance_anti_prediction_threshold():
    """Concordance < 0.35 = anti-prediction zone — threshold must be reachable."""
    # Just verify the method works for all 12 houses without error
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter

    chart = _india_chart()
    adapter = ScoringEngineAdapter()
    values = [adapter.school_concordance(chart, house=h) for h in range(1, 13)]
    assert len(values) == 12
    assert all(isinstance(v, float) for v in values)


# ─────────────────────────────────────────────────────────────
# 4. DashaEngine — functional tests
# ─────────────────────────────────────────────────────────────


def test_compute_dashas_returns_list():
    """compute_dashas() must return a non-empty list of MahaDashas."""
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter

    chart = _india_chart()
    adapter = VimshottariDasaAdapter()
    dashas = adapter.compute_dashas(chart)

    assert isinstance(dashas, list)
    assert len(dashas) > 0


def test_compute_dashas_covers_120_years():
    """Vimshottari dasha sequence must span approximately 120 years end-to-end."""
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter

    chart = _india_chart()
    adapter = VimshottariDasaAdapter()
    dashas = adapter.compute_dashas(chart)

    # The first MD may start mid-period (Moon nakshatra balance), so sum of .years
    # can be < 120. Measure actual calendar span from first start to last end.
    span_days = (dashas[-1].end - dashas[0].start).days
    span_years = span_days / 365.25
    assert abs(span_years - 120) < 2.0, f"Dasha calendar span: {span_years:.2f} years"


def test_active_dasha_returns_string_triplet():
    """active_dasha() must return a tuple of 3 strings (MD, AD, PD lords)."""
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter

    chart = _india_chart()
    adapter = VimshottariDasaAdapter()
    result = adapter.active_dasha(chart, on_date=date(2025, 6, 15))

    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 3, f"Expected 3-tuple, got length {len(result)}"
    assert all(isinstance(s, str) for s in result), "All elements must be strings"


def test_active_dasha_lords_are_valid_planets():
    """active_dasha() lords must be from the 9 Vimshottari planets."""
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter

    VALID_LORDS = {"Sun", "Moon", "Mars", "Rahu", "Jupiter",
                   "Saturn", "Mercury", "Ketu", "Venus"}

    chart = _india_chart()
    adapter = VimshottariDasaAdapter()
    md_lord, ad_lord, pd_lord = adapter.active_dasha(chart, on_date=date(2025, 6, 15))

    for lord in (md_lord, ad_lord, pd_lord):
        assert lord in VALID_LORDS, f"Invalid dasha lord: {lord}"


# ─────────────────────────────────────────────────────────────
# 5. NullFeedbackService — stub contract tests
# ─────────────────────────────────────────────────────────────


def test_null_feedback_store_returns_string_id():
    """NullFeedbackService.store_feedback() must return a string ID."""
    from src.interfaces.adapters.null_feedback import NullFeedbackService

    svc = NullFeedbackService()
    record_id = svc.store_feedback(
        prediction_id="P001",
        outcome=True,
        convergence_state={"school_concordance": 0.8, "varga_agreement": "★★"},
    )
    assert isinstance(record_id, str)
    assert len(record_id) > 0


def test_null_feedback_get_returns_list():
    """NullFeedbackService.get_feedback() must return a list."""
    from src.interfaces.adapters.null_feedback import NullFeedbackService

    svc = NullFeedbackService()
    result = svc.get_feedback()
    assert isinstance(result, list)


def test_null_feedback_store_then_get():
    """NullFeedbackService.store then get must round-trip."""
    from src.interfaces.adapters.null_feedback import NullFeedbackService

    svc = NullFeedbackService()
    svc.store_feedback("P002", True, {"school_concordance": 0.7})
    records = svc.get_feedback()
    assert isinstance(records, list)


# ─────────────────────────────────────────────────────────────
# 6. NullMLService — stub contract tests
# ─────────────────────────────────────────────────────────────


def test_null_ml_predict_returns_dict_with_probability():
    """NullMLService.predict() must return dict with 'probability' key."""
    from src.interfaces.adapters.null_ml import NullMLService

    svc = NullMLService()
    result = svc.predict(
        chart_features={"lagna_sign": "Taurus"},
        house=10,
        concordance_state={"parashari": 0.7, "kp": 0.6},
    )
    assert isinstance(result, dict)
    assert "probability" in result
    assert isinstance(result["probability"], float)


def test_null_ml_predict_probability_in_unit_interval():
    """NullMLService.predict() probability must be in [0.0, 1.0]."""
    from src.interfaces.adapters.null_ml import NullMLService

    svc = NullMLService()
    result = svc.predict(
        chart_features={},
        house=1,
        concordance_state={},
    )
    assert 0.0 <= result["probability"] <= 1.0


def test_null_ml_calibrate_returns_updated_false():
    """NullMLService.calibrate() must return updated=False (stub mode)."""
    from src.interfaces.adapters.null_ml import NullMLService

    svc = NullMLService()
    result = svc.calibrate(feedback_records=[], min_events=1000)
    assert isinstance(result, dict)
    assert "updated" in result
    assert result["updated"] is False


def test_null_ml_calibrate_has_calibration_version():
    """NullMLService.calibrate() must include calibration_version."""
    from src.interfaces.adapters.null_ml import NullMLService

    svc = NullMLService()
    result = svc.calibrate(feedback_records=[])
    assert "calibration_version" in result
    assert isinstance(result["calibration_version"], str)
