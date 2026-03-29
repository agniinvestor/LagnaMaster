"""
tests/test_s199_feature_contracts.py — S199: contract tests for ChartFeatureVector

Validates internal consistency guarantees that must hold for any future
additions to feature_decomp.py. G22: these tests act as the Phase 6 gate.
"""

from __future__ import annotations


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


def _malawi_chart():
    """A different chart to test against India 1947 assumptions."""
    from src.ephemeris import compute_chart
    return compute_chart(year=1964, month=7, day=6, hour=0.0,
                         lat=-13.9626, lon=33.7741, tz_offset=2.0)


# ── Phase 6 gate ──────────────────────────────────────────────────────────────

def test_feature_count_exceeds_150_phase6_gate():
    """G22 contract: feature space must reach ≥150 before Phase 6."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert cfv.feature_count() >= 150, (
        f"Phase 6 gate FAILED: only {cfv.feature_count()} features (need ≥150)"
    )


# ── Internal consistency ──────────────────────────────────────────────────────

def test_to_array_length_equals_feature_count():
    """to_array() length must equal feature_count()."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert len(cfv.to_array()) == cfv.feature_count()


def test_to_dict_length_equals_feature_count():
    """to_dict() key count must equal feature_count()."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert len(cfv.to_dict()) == cfv.feature_count()


def test_feature_names_length_equals_feature_count():
    """feature_names() length must equal feature_count()."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert len(cfv.feature_names()) == cfv.feature_count()


def test_feature_names_unique():
    """All feature names must be unique (no duplicate keys)."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    names = cfv.feature_names()
    assert len(names) == len(set(names)), (
        f"Duplicate feature names: {[n for n in names if names.count(n) > 1][:5]}"
    )


def test_to_dict_to_array_order_consistent():
    """to_array() values must match to_dict() values in feature_names() order."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    d = cfv.to_dict()
    arr = cfv.to_array()
    names = cfv.feature_names()
    for i, name in enumerate(names):
        assert d[name] == arr[i], (
            f"Mismatch at index {i} ({name}): dict={d[name]}, array={arr[i]}"
        )


def test_all_features_are_float():
    """Every feature value must be a Python float."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for k, v in cfv.to_dict().items():
        assert isinstance(v, float), f"{k}={v!r} is {type(v).__name__}, expected float"


def test_12_houses_always_present():
    """ChartFeatureVector must always have exactly 12 house entries."""
    from src.calculations.feature_decomp import extract_features
    for chart in (_india_chart(), _malawi_chart()):
        cfv = extract_features(chart)
        assert set(cfv.houses.keys()) == set(range(1, 13)), (
            f"Expected houses 1-12, got {sorted(cfv.houses.keys())}"
        )


def test_feature_count_same_across_charts():
    """Feature count must be identical for any chart (no conditional features)."""
    from src.calculations.feature_decomp import extract_features
    c1 = extract_features(_india_chart())
    c2 = extract_features(_malawi_chart())
    assert c1.feature_count() == c2.feature_count(), (
        f"Feature count varies: India={c1.feature_count()}, Malawi={c2.feature_count()}"
    )


def test_all_values_finite():
    """No feature value may be NaN or Inf."""
    import math
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for k, v in cfv.to_dict().items():
        assert math.isfinite(v), f"{k}={v} is not finite"
