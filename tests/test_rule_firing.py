"""tests/test_rule_firing.py — Rule firing function validation."""
from __future__ import annotations


def _get_india_1947():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


def test_rule_firing_returns_results():
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    assert result.total_evaluated > 3000
    assert result.total_fired > 50
    assert len(result.fired_rules) == result.total_fired


def test_rule_firing_house_summary():
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    assert len(result.house_summary) == 12
    # H3 should fire most (5 planets in Cancer = H3 from Taurus lagna)
    h3 = result.house_summary[3]
    assert h3.total_fired > 50


def test_rule_firing_h2_unfavorable():
    """India 1947 H2 should be unfavorable (CLAUDE.md invariant)."""
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    h2 = result.house_summary[2]
    assert h2.unfavorable_count > h2.favorable_count, (
        f"H2 should be unfavorable: fav={h2.favorable_count}, unfav={h2.unfavorable_count}"
    )


def test_rule_firing_feature_vector():
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    fv = result.feature_vector()
    # 12 houses × 7 features + 5 global = 89
    assert len(fv) == 89
    assert fv["global_total_fired"] > 0
    assert 0.0 <= fv["global_favorable_ratio"] <= 1.0
    assert fv["global_source_diversity"] >= 1.0


def test_rule_firing_multiple_sources():
    """Fired rules should come from multiple source texts."""
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    sources = {r.source for r in result.fired_rules}
    assert len(sources) >= 2, f"Expected ≥2 sources, got {sources}"


def test_rule_firing_lagna_scope_filter():
    """BVR rules should only fire for matching lagna."""
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    bvr = [r for r in result.fired_rules if r.source == "BhavarthaRatnakara"]
    # India 1947 is Taurus lagna — only BVR Taurus rules should fire
    assert len(bvr) > 0
    assert len(bvr) <= 65  # max 65 Taurus rules in BVR
