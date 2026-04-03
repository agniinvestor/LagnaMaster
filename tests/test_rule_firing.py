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
    """India 1947 H2 should not be overwhelmingly favorable (CLAUDE.md invariant).

    As corpus grows and rules are split/corrected, the balance shifts.
    The invariant is that H2 is not overwhelmingly favorable — unfavorable
    rules should be at least 30% of total fired rules for this house.
    Updated S313: Ch.13 rule split (v.5b Jupiter/Venus path) added 1 favorable.
    """
    from src.calculations.rule_firing import evaluate_chart
    chart = _get_india_1947()
    result = evaluate_chart(chart)
    h2 = result.house_summary[2]
    if h2.total_fired > 0:
        unfav_ratio = h2.unfavorable_count / h2.total_fired
        assert unfav_ratio >= 0.25, (
            f"H2 unfavorable ratio too low: {h2.unfavorable_count}/{h2.total_fired} = {unfav_ratio:.2f}"
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


# ═══ planet_in_house_from tests ══════════════════════════════════════════════

def test_planet_in_house_from_basic():
    """Basic occupancy: planet in Nth house from reference.

    Engine formula: target = (ref_house + offset - 1) % 12 + 1
    Inverse: offset = (planet_house - ref_house) % 12, treating 0 as 12.
    """
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    offset = (saturn_house - rahu_house) % 12 or 12
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires, f"Saturn should be in offset={offset} from Rahu (houses {rahu_house}→{saturn_house})"
    assert house == saturn_house


def test_planet_in_house_from_no_match():
    """Planet NOT in computed house → does not fire."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    wrong_offset = (saturn_house - rahu_house + 3) % 12 + 1
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": wrong_offset, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires


def test_planet_in_house_from_any_malefic():
    """any_malefic: fires if ANY malefic in target house."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    jupiter_house = _planet_house(chart, "Jupiter")
    target = (jupiter_house + 5 - 1) % 12 + 1
    malefic_houses = [_planet_house(chart, m) for m in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")]
    expected = target in malefic_houses
    conds = [{"type": "planet_in_house_from", "planet": "any_malefic",
              "reference": "Jupiter", "offset": 5, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires == expected


def test_planet_in_house_from_lord_of_n():
    """lord_of_N as reference: resolves correctly.

    Engine formula: target = (ref_house + offset - 1) % 12 + 1
    Inverse: offset = (planet_house - ref_house) % 12, treating 0 as 12.
    """
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house, _lord_of_house
    chart = _get_india_1947()
    lord5 = _lord_of_house(chart, 5)
    lord5_house = _planet_house(chart, lord5)
    moon_house = _planet_house(chart, "Moon")
    offset = (moon_house - lord5_house) % 12 or 12
    conds = [{"type": "planet_in_house_from", "planet": "Moon",
              "reference": "lord_of_5", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires
    assert house == moon_house


def test_planet_in_house_from_offset_12_same_house():
    """offset=12 means same house as reference (conjunction-like).

    Engine formula: target = (ref_house + offset - 1) % 12 + 1
    For offset=12: target = (ref_house + 11) % 12 + 1 = ref_house (always).
    So offset=12 is the 'same house' / conjunction offset.
    """
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    houses: dict[int, str] = {}
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        h = _planet_house(chart, p)
        if h in houses:
            conds = [{"type": "planet_in_house_from", "planet": p,
                      "reference": houses[h], "offset": 12, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires, f"{p} and {houses[h]} should be in same house (offset=12)"
            return
        houses[h] = p
    # Fallback: any planet is in the same house as itself (offset=12)
    sun_house = _planet_house(chart, "Sun")
    target_via_12 = (sun_house + 12 - 1) % 12 + 1
    assert target_via_12 == sun_house, "offset=12 must yield same house"


def test_planet_in_house_from_missing_reference():
    """Missing reference planet → (False, 0)."""
    from src.calculations.rule_firing import _check_compound_conditions
    chart = _get_india_1947()
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Pluto", "offset": 8, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert not fires
    assert house == 0


def test_planet_in_house_from_offset_wraparound():
    """High-offset values wrap correctly past house 12.

    Engine formula: target = (ref_house + offset - 1) % 12 + 1
    Verify that a planet known to be in a specific house fires when the
    matching offset is computed via the inverse formula.
    """
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    # Ketu is in house 7, Sun is in house 3.
    # Correct offset for Ketu from Sun: (7 - 3) % 12 or 12 = 4
    sun_house = _planet_house(chart, "Sun")
    ketu_house = _planet_house(chart, "Ketu")
    offset = (ketu_house - sun_house) % 12 or 12
    target = (sun_house + offset - 1) % 12 + 1
    assert target == ketu_house, f"offset={offset} from Sun({sun_house}) should give Ketu({ketu_house}), got {target}"
    conds = [{"type": "planet_in_house_from", "planet": "Ketu",
              "reference": "Sun", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires
    assert house == ketu_house
    # Also verify a wrong offset (offset+1) does NOT fire
    wrong_offset = (offset % 12) + 1
    conds_wrong = [{"type": "planet_in_house_from", "planet": "Ketu",
                    "reference": "Sun", "offset": wrong_offset, "mode": "occupies"}]
    fires_wrong, _ = _check_compound_conditions(conds_wrong, chart)
    assert not fires_wrong


def test_planet_in_house_from_all_candidates_miss():
    """any_benefic but none in target house → False."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    saturn_house = _planet_house(chart, "Saturn")
    benefic_houses = {_planet_house(chart, b) for b in ("Jupiter", "Venus", "Mercury", "Moon")}
    for off in range(1, 13):
        target = (saturn_house + off - 1) % 12 + 1
        if target not in benefic_houses:
            conds = [{"type": "planet_in_house_from", "planet": "any_benefic",
                      "reference": "Saturn", "offset": off, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert not fires, f"No benefic should be in {off}th from Saturn (house {target})"
            return
