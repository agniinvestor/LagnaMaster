"""
tests/test_s213_protocol_verification.py — S213: Protocol verification

Verifies that all Protocol interfaces defined in S192 are still
satisfied by their concrete adapter implementations using runtime
isinstance() checks (requires @runtime_checkable).

Covers: ClassicalEngine, DashaEngine, FeedbackService, MLService.
"""

from __future__ import annotations


# ── Protocol isinstance checks ────────────────────────────────────────────────

def test_scoring_adapter_satisfies_classical_engine_protocol():
    from src.interfaces.classical_engine import ClassicalEngine
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    assert isinstance(ScoringEngineAdapter(), ClassicalEngine)


def test_dasha_adapter_satisfies_dasha_engine_protocol():
    from src.interfaces.dasha_engine import DashaEngine
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter
    assert isinstance(VimshottariDasaAdapter(), DashaEngine)


def test_null_feedback_satisfies_feedback_service_protocol():
    from src.interfaces.feedback_service import FeedbackService
    from src.interfaces.adapters.null_feedback import NullFeedbackService
    assert isinstance(NullFeedbackService(), FeedbackService)


def test_null_ml_satisfies_ml_service_protocol():
    from src.interfaces.ml_service import MLService
    from src.interfaces.adapters.null_ml import NullMLService
    assert isinstance(NullMLService(), MLService)


# ── Protocol compliance module ────────────────────────────────────────────────

def test_protocol_compliance_module_importable():
    from src.ci.protocol_compliance import check_all_protocols  # noqa: F401


def test_check_all_protocols_returns_report():
    from src.ci.protocol_compliance import check_all_protocols
    report = check_all_protocols()
    assert isinstance(report, dict)


def test_check_all_protocols_covers_all_four_protocols():
    from src.ci.protocol_compliance import check_all_protocols
    report = check_all_protocols()
    assert "ClassicalEngine" in report
    assert "DashaEngine" in report
    assert "FeedbackService" in report
    assert "MLService" in report


def test_check_all_protocols_all_pass():
    from src.ci.protocol_compliance import check_all_protocols
    report = check_all_protocols()
    for protocol_name, result in report.items():
        assert result["compliant"] is True, (
            f"{protocol_name} protocol not satisfied: {result.get('error', '')}"
        )


def test_check_all_protocols_adapter_names_present():
    from src.ci.protocol_compliance import check_all_protocols
    report = check_all_protocols()
    for protocol_name, result in report.items():
        assert "adapter" in result, f"Missing 'adapter' key for {protocol_name}"
        assert isinstance(result["adapter"], str)


# ── ScoringEngineAdapter functional tests ─────────────────────────────────────

def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


def test_scoring_adapter_score_chart_returns_valid_result():
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    adapter = ScoringEngineAdapter()
    chart = _india_chart()
    result = adapter.score_chart(chart, school="parashari")
    assert result is not None


def test_scoring_adapter_school_concordance_in_unit_interval():
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    adapter = ScoringEngineAdapter()
    chart = _india_chart()
    for house in (1, 5, 9):
        c = adapter.school_concordance(chart, house=house)
        assert 0.0 <= c <= 1.0, f"Concordance {c} out of [0,1] for house {house}"


def test_scoring_adapter_concordance_all_houses():
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    adapter = ScoringEngineAdapter()
    chart = _india_chart()
    concordances = [adapter.school_concordance(chart, house=h) for h in range(1, 13)]
    assert len(concordances) == 12
    assert all(0.0 <= c <= 1.0 for c in concordances)


# ── DashaEngine adapter functional tests ──────────────────────────────────────

def test_dasha_adapter_compute_dashas_returns_nonempty_list():
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter
    adapter = VimshottariDasaAdapter()
    chart = _india_chart()
    dashas = adapter.compute_dashas(chart, system="vimshottari")
    assert isinstance(dashas, list)
    assert len(dashas) > 0


def test_dasha_adapter_active_dasha_returns_tuple():
    from datetime import date
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter
    adapter = VimshottariDasaAdapter()
    chart = _india_chart()
    result = adapter.active_dasha(chart, on_date=date(2024, 1, 1))
    assert isinstance(result, tuple)
    assert len(result) == 3  # (md_lord, ad_lord, pd_lord)


# ── Full pipeline integration ──────────────────────────────────────────────────

def test_full_protocol_pipeline_end_to_end():
    """Chart → scoring → dasha → feedback → ML pipeline all wire together."""
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter
    from src.interfaces.adapters.null_feedback import NullFeedbackService
    from src.interfaces.adapters.null_ml import NullMLService

    chart = _india_chart()

    scoring = ScoringEngineAdapter()
    scores = scoring.score_chart(chart, school="parashari")
    assert scores is not None

    dasha = VimshottariDasaAdapter()
    dashas = dasha.compute_dashas(chart)
    assert len(dashas) > 0

    feedback = NullFeedbackService()
    record_id = feedback.store_feedback(
        "pred-001", True,
        {"school_concordance": scoring.school_concordance(chart, 1)},
    )
    assert isinstance(record_id, str)

    ml = NullMLService()
    pred = ml.predict(
        chart_features={"lagna_sign": "Taurus"},
        house=1,
        concordance_state={"parashari": 0.7},
    )
    assert 0.0 <= pred["probability"] <= 1.0
