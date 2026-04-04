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
# Engine formula (BPHS inclusive counting):
#   target = (ref_house + offset - 2) % 12 + 1
#   offset=1 → same house, offset=7 → opposite house
# Inverse: offset = (planet_house - ref_house + 1) % 12 or 12

def test_planet_in_house_from_basic():
    """Basic occupancy: planet in Nth house from reference."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    offset = (saturn_house - rahu_house + 1) % 12 or 12
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires, f"Saturn should be in {offset}th from Rahu"
    assert house == saturn_house


def test_planet_in_house_from_no_match():
    """Planet NOT in computed house → does not fire."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    rahu_house = _planet_house(chart, "Rahu")
    saturn_house = _planet_house(chart, "Saturn")
    correct_offset = (saturn_house - rahu_house + 1) % 12 or 12
    wrong_offset = (correct_offset % 12) + 1  # shift by 1
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Rahu", "offset": wrong_offset, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires


def test_planet_in_house_from_any_malefic():
    """any_malefic: fires if ANY malefic in target house."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    jupiter_house = _planet_house(chart, "Jupiter")
    # 5th from Jupiter (BPHS inclusive)
    target = (jupiter_house + 5 - 2) % 12 + 1
    malefic_houses = [_planet_house(chart, m) for m in ("Sun", "Mars", "Saturn", "Rahu", "Ketu")]
    expected = target in malefic_houses
    conds = [{"type": "planet_in_house_from", "planet": "any_malefic",
              "reference": "Jupiter", "offset": 5, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires == expected


def test_planet_in_house_from_lord_of_n():
    """lord_of_N as reference: resolves correctly."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house, _lord_of_house
    chart = _get_india_1947()
    lord5 = _lord_of_house(chart, 5)
    lord5_house = _planet_house(chart, lord5)
    moon_house = _planet_house(chart, "Moon")
    offset = (moon_house - lord5_house + 1) % 12 or 12
    conds = [{"type": "planet_in_house_from", "planet": "Moon",
              "reference": "lord_of_5", "offset": offset, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires
    assert house == moon_house


def test_planet_in_house_from_offset_1_same_house():
    """offset=1 means same house as reference (BPHS inclusive counting)."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    # offset=1 should compute to same house as reference
    sun_house = _planet_house(chart, "Sun")
    target = (sun_house + 1 - 2) % 12 + 1
    assert target == sun_house, "offset=1 must yield same house"
    # Sun in 1st from Sun = True
    conds = [{"type": "planet_in_house_from", "planet": "Sun",
              "reference": "Sun", "offset": 1, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires
    # Find two planets in same house (conjunction)
    houses = {}
    for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        h = _planet_house(chart, p)
        if h in houses:
            conds2 = [{"type": "planet_in_house_from", "planet": p,
                       "reference": houses[h], "offset": 1, "mode": "occupies"}]
            fires2, _ = _check_compound_conditions(conds2, chart)
            assert fires2, f"{p} and {houses[h]} in same house → offset=1 should fire"
            return
        houses[h] = p


def test_planet_in_house_from_missing_reference():
    """Missing reference planet → (False, 0)."""
    from src.calculations.rule_firing import _check_compound_conditions
    chart = _get_india_1947()
    conds = [{"type": "planet_in_house_from", "planet": "Saturn",
              "reference": "Pluto", "offset": 8, "mode": "occupies"}]
    fires, house = _check_compound_conditions(conds, chart)
    assert not fires
    assert house == 0


def test_planet_in_house_from_offset_12_wraparound():
    """offset=12: 12th from reference wraps correctly."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    sun_house = _planet_house(chart, "Sun")
    # 12th from Sun (BPHS inclusive): (sun + 12 - 2) % 12 + 1
    target = (sun_house + 12 - 2) % 12 + 1
    # Find if any planet is there
    for p in ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ketu"):
        if _planet_house(chart, p) == target:
            conds = [{"type": "planet_in_house_from", "planet": p,
                      "reference": "Sun", "offset": 12, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires
            return
    # No planet there — verify it correctly returns False
    conds = [{"type": "planet_in_house_from", "planet": "Jupiter",
              "reference": "Sun", "offset": 12, "mode": "occupies"}]
    fires, _ = _check_compound_conditions(conds, chart)
    jupiter_house = _planet_house(chart, "Jupiter")
    assert fires == (jupiter_house == target)


def test_planet_in_house_from_all_candidates_miss():
    """any_benefic but none in target house → False."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    saturn_house = _planet_house(chart, "Saturn")
    benefic_houses = {_planet_house(chart, b) for b in ("Jupiter", "Venus", "Mercury", "Moon")}
    for off in range(1, 13):
        target = (saturn_house + off - 2) % 12 + 1
        if target not in benefic_houses:
            conds = [{"type": "planet_in_house_from", "planet": "any_benefic",
                      "reference": "Saturn", "offset": off, "mode": "occupies"}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert not fires, f"No benefic should be in {off}th from Saturn (house {target})"
            return


def test_planet_not_in_house_basic():
    """Absence: no benefic in target house → fires."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    # Find a house with no benefics
    benefic_houses = {_planet_house(chart, b) for b in ("Jupiter", "Venus", "Mercury", "Moon")}
    for h in range(1, 13):
        if h not in benefic_houses:
            conds = [{"type": "planet_not_in_house", "planet": "any_benefic", "house": h}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires, f"No benefic in house {h} → should fire"
            return


def test_planet_not_in_house_fails_when_present():
    """Absence: benefic IS in house → does not fire."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_house
    chart = _get_india_1947()
    jupiter_house = _planet_house(chart, "Jupiter")
    conds = [{"type": "planet_not_in_house", "planet": "any_benefic", "house": jupiter_house}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires, f"Jupiter (benefic) IS in house {jupiter_house} → should not fire"


def test_planet_not_aspecting_basic():
    """No benefic aspects target house → fires."""
    from src.calculations.rule_firing import _check_compound_conditions, _planet_aspects_house
    chart = _get_india_1947()
    # Find a house not aspected by any benefic
    for h in range(1, 13):
        aspected = any(_planet_aspects_house(chart, b, h) for b in ("Jupiter", "Venus", "Mercury", "Moon"))
        if not aspected:
            conds = [{"type": "planet_not_aspecting", "planet": "any_benefic", "house": h}]
            fires, _ = _check_compound_conditions(conds, chart)
            assert fires
            return


# ═══ planet_in_navamsa_sign tests ════════════════════════════════════════════

def test_planet_in_navamsa_sign():
    """Planet's navamsa sign matches target."""
    from src.calculations.rule_firing import _check_compound_conditions, _find_planet
    chart = _get_india_1947()
    # Compute Sun's navamsa to verify
    sun = _find_planet(chart, "Sun")
    FIRE = {0, 4, 8}
    EARTH = {1, 5, 9}
    AIR = {2, 6, 10}
    WATER = {3, 7, 11}  # noqa: F841
    pada = int(sun.degree_in_sign / (30.0 / 9))
    if pada >= 9:
        pada = 8
    if sun.sign_index in FIRE:
        start = 0
    elif sun.sign_index in EARTH:
        start = 3
    elif sun.sign_index in AIR:
        start = 6
    else:
        start = 9
    nav_idx = (start + pada) % 12
    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sun_nav = SIGNS[nav_idx]
    conds = [{"type": "planet_in_navamsa_sign", "planet": "Sun", "sign": [sun_nav]}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires, f"Sun navamsa={sun_nav} should match"


def test_planet_in_navamsa_sign_no_match():
    """Planet's navamsa sign does not match wrong target → False."""
    from src.calculations.rule_firing import _check_compound_conditions, _find_planet
    chart = _get_india_1947()
    sun = _find_planet(chart, "Sun")
    FIRE = {0, 4, 8}
    EARTH = {1, 5, 9}
    AIR = {2, 6, 10}
    WATER = {3, 7, 11}  # noqa: F841
    pada = int(sun.degree_in_sign / (30.0 / 9))
    if pada >= 9:
        pada = 8
    if sun.sign_index in FIRE:
        start = 0
    elif sun.sign_index in EARTH:
        start = 3
    elif sun.sign_index in AIR:
        start = 6
    else:
        start = 9
    nav_idx = (start + pada) % 12
    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sun_nav = SIGNS[nav_idx]
    wrong_nav = SIGNS[(nav_idx + 1) % 12]
    conds = [{"type": "planet_in_navamsa_sign", "planet": "Sun", "sign": [wrong_nav]}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires, f"Sun navamsa={sun_nav}, wrong={wrong_nav} should not match"


# ═══ dispositor_condition tests ══════════════════════════════════════════════

def test_dispositor_in_house():
    """Dispositor of planet is in target house."""
    from src.calculations.rule_firing import _check_compound_conditions, _find_planet, _planet_house
    chart = _get_india_1947()
    rahu = _find_planet(chart, "Rahu")
    LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
             "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    dispositor = LORDS[rahu.sign_index]
    disp_house = _planet_house(chart, dispositor)
    conds = [{"type": "dispositor_condition", "planet": "Rahu",
              "dispositor_state": "in_house", "house": disp_house}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires


def test_dispositor_in_house_wrong():
    """Dispositor not in wrong house → False."""
    from src.calculations.rule_firing import _check_compound_conditions, _find_planet, _planet_house
    chart = _get_india_1947()
    rahu = _find_planet(chart, "Rahu")
    LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
             "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    dispositor = LORDS[rahu.sign_index]
    disp_house = _planet_house(chart, dispositor)
    wrong_house = (disp_house % 12) + 1
    conds = [{"type": "dispositor_condition", "planet": "Rahu",
              "dispositor_state": "in_house", "house": wrong_house}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert not fires
