"""
tests/test_s200_g22_integration.py — S200: G22 wiring + ChartScoresV3 integration

Validates that ChartScoresV3 carries a feature_vector field and that
the full Phase 0 feature decomposition pipeline is end-to-end accessible.
"""

from __future__ import annotations


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


# ── ChartScoresV3 integration ─────────────────────────────────────────────────

def test_chart_scores_v3_has_feature_vector():
    """score_chart_v3 must populate feature_vector on ChartScoresV3."""
    from src.calculations.scoring_v3 import score_chart_v3
    result = score_chart_v3(_india_chart())
    assert result.feature_vector is not None, "feature_vector should not be None"


def test_feature_vector_in_scores_v3_is_chart_feature_vector():
    """The feature_vector field must be a ChartFeatureVector instance."""
    from src.calculations.scoring_v3 import score_chart_v3
    from src.calculations.feature_decomp import ChartFeatureVector
    result = score_chart_v3(_india_chart())
    assert isinstance(result.feature_vector, ChartFeatureVector)


def test_feature_vector_count_in_scores_v3():
    """feature_vector in ChartScoresV3 must have ≥150 features."""
    from src.calculations.scoring_v3 import score_chart_v3
    result = score_chart_v3(_india_chart())
    assert result.feature_vector.feature_count() >= 150, (
        f"ChartScoresV3.feature_vector only has {result.feature_vector.feature_count()} features"
    )


# ── G22 compliance note ───────────────────────────────────────────────────────

def test_g22_note_in_feature_vector_docstring():
    """G22 guardrail note must appear in ChartFeatureVector docstring."""
    from src.calculations.feature_decomp import ChartFeatureVector
    doc = ChartFeatureVector.__doc__ or ""
    assert "G22" in doc, "ChartFeatureVector docstring must reference G22 guardrail"


def test_extract_features_module_docstring_has_g22():
    """feature_decomp module docstring must reference G22."""
    import src.calculations.feature_decomp as mod
    assert "G22" in (mod.__doc__ or ""), "feature_decomp module must reference G22 guardrail"
