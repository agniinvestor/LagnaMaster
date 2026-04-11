"""tests/test_s321_primitives.py — S321: planet_aspecting lord-position targets.

Tests for the extended planet_aspecting primitive that resolves lord positions.
"""
from __future__ import annotations

import pytest

from src.calculations.rule_firing import (
    _check_compound_conditions,
    _lord_of_house,
    _planet_aspects_house,
    _planet_house,
)


def _get_india_1947():
    from src.ephemeris import compute_chart
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


# ═══ Primitive A: planet_aspecting with target="lord_of_N" ═══════════════════


def test_planet_aspecting_lord_target_hit():
    """Jupiter aspects house where lord_of_7 sits → fires.

    India 1947: lord_of_7=Mars in H2, Jupiter aspects H2 (from H6 via special 9th aspect → no,
    from H6: 7th aspect = H12; 5th aspect = H10; 9th aspect = H2 ✓).
    """
    chart = _get_india_1947()
    # Verify: lord_of_7 = Mars, Mars in H2, Jupiter aspects H2
    lord_7 = _lord_of_house(chart, 7)
    lord_7_house = _planet_house(chart, lord_7)
    assert _planet_aspects_house(chart, "Jupiter", lord_7_house), (
        f"Pre-check: Jupiter should aspect H{lord_7_house} (lord_of_7={lord_7})"
    )
    conds = [{"type": "planet_aspecting", "planet": "Jupiter", "target": "lord_of_7"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires, "Jupiter aspects lord_of_7's house but condition didn't fire"


def test_planet_aspecting_lord_target_miss():
    """Planet does NOT aspect lord_of_N's house → doesn't fire."""
    chart = _get_india_1947()
    lord_2 = _lord_of_house(chart, 2)
    lord_2_house = _planet_house(chart, lord_2)
    # Find a planet that does NOT aspect lord_2's house
    for planet in ("Sun", "Moon", "Mercury", "Venus", "Jupiter", "Mars", "Saturn"):
        if not _planet_aspects_house(chart, planet, lord_2_house):
            conds = [{"type": "planet_aspecting", "planet": planet, "target": "lord_of_2"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert not fires, f"{planet} should NOT aspect house {lord_2_house} but condition fired"
            return
    pytest.skip("All planets aspect lord_of_2's house in India 1947 fixture")


def test_planet_aspecting_house_still_works():
    """Existing numeric house path unchanged (regression)."""
    chart = _get_india_1947()
    # Jupiter in Libra (house 6 for Taurus lagna), aspects 7th from it = house 12
    jup_house = _planet_house(chart, "Jupiter")
    target = ((jup_house - 1 + 6) % 12) + 1  # 7th from Jupiter
    conds = [{"type": "planet_aspecting", "planet": "Jupiter", "house": target}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires, f"Jupiter in house {jup_house} should aspect house {target} via 7th aspect"


def test_planet_aspecting_lord_target_no_lord():
    """Edge case: target lord resolution works for all valid houses."""
    chart = _get_india_1947()
    # lord_of_1 should always resolve for any valid chart
    lord_1 = _lord_of_house(chart, 1)
    assert lord_1, "lord_of_1 should resolve"
    lord_1_house = _planet_house(chart, lord_1)
    assert lord_1_house > 0, "lord_of_1 should have a house position"
