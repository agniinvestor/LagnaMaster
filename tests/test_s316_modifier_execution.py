"""Tests for modifier execution: gate eval, ordering, 3-tier negation, context scaling."""
from src.calculations.inference import apply_modifiers
from src.calculations.rule_firing import FiredRule


def _fired(rule_id="T001", direction="favorable", confidence=0.7):
    return FiredRule(
        rule_id=rule_id, source="BPHS", planet="Sun", house=1,
        outcome_direction=direction, outcome_domains=["wealth"],
        confidence=confidence, concordance_count=0,
    )


class _Rule:
    def __init__(self, modifiers=None, predictions=None, primary_domain="wealth"):
        self.modifiers = modifiers or []
        self.predictions = predictions or [{"magnitude": 0.7, "domain": "wealth"}]
        self.primary_domain = primary_domain


class _MockPlanet:
    def __init__(self, sign_index, degree_in_sign=15.0, name="Sun"):
        self.sign_index = sign_index
        self.degree_in_sign = degree_in_sign
        self.name = name
        self.sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                      "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][sign_index]


class _MockChart:
    def __init__(self, lagna_sign_index=0, planets=None):
        self.lagna_sign_index = lagna_sign_index
        self.lagna_sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][lagna_sign_index]
        self.planets = planets or {}


def _make_chart(sun_house=1, lagna_si=0):
    sun_si = (lagna_si + sun_house - 1) % 12
    return _MockChart(lagna_sign_index=lagna_si, planets={"Sun": _MockPlanet(sun_si, name="Sun")})


# --- Gate tests ---

def test_structured_gate_passes():
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 1}],
    }])
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert not result.gated_out


def test_structured_gate_fails():
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 7}],
    }])
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert result.gated_out
    assert result.gate_reason != ""


def test_string_gate_unevaluated():
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": "other_six_planets_endowed_with_strength",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert not result.gated_out
    assert len(result.unevaluated_gates) == 1
    assert result.unevaluated_gates[0]["severity"] == "blocking"


# --- Negation 3-tier ---

def test_strong_negation_flips():
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "strong",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "unfavorable"


def test_medium_negation_weakens():
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "medium",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "favorable"  # NOT flipped
    assert result.magnitude < 0.7


def test_weak_negation_negligible():
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "weak",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "favorable"
    assert result.magnitude == 0.7


# --- Ordering ---

def test_gates_before_amplifies():
    fired = _fired()
    rule = _Rule(modifiers=[
        {"effect": "amplifies", "target": "prediction", "strength": "strong",
         "scope": "local", "condition": "test"},
        {"effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
         "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 7}]},
    ])
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert result.gated_out


# --- Context scaling ---

def test_context_aware_amplification():
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "amplifies", "target": "prediction", "strength": "medium",
        "scope": "local", "condition": "test",
    }])
    ctx = {"conditions": {}, "aggregates": {"argala_strength_total": 0.8}, "gates": {}}
    result = apply_modifiers(fired, rule, chart=None, condition_context=ctx)
    # effective_weight = 0.30 * (1 + 0.5 * 0.8) = 0.42
    # magnitude = 0.7 * (1 + 0.42) = 0.994
    assert result.magnitude > 0.9


# --- ModifiedRule fields ---

def test_modified_rule_new_fields():
    fired = _fired()
    rule = _Rule()
    result = apply_modifiers(fired, rule, chart=None)
    assert hasattr(result, "gate_reason")
    assert hasattr(result, "unevaluated_gates")
    assert hasattr(result, "context")


# --- Backward compat: no modifiers ---

def test_no_modifiers_unchanged():
    fired = _fired()
    rule = _Rule()
    result = apply_modifiers(fired, rule, chart=None)
    assert result.magnitude == 0.7
    assert result.direction == "favorable"
    assert not result.gated_out


# --- Conflict resolution in aggregate_domains ---

from src.calculations.inference import aggregate_domains, ModifiedRule


def _modified(rule_id, domain, direction, magnitude, confidence=0.7, signal_group=""):
    fired = _fired(rule_id=rule_id, direction=direction, confidence=confidence)
    fired.signal_group = signal_group
    return ModifiedRule(
        rule_id=rule_id, primary_domain=domain, direction=direction,
        magnitude=magnitude, source_rule=fired,
    )


def test_confidence_weighted_scoring():
    rules = [_modified("R1", "wealth", "favorable", 0.8, confidence=0.5)]
    scores = aggregate_domains(rules)
    assert scores["wealth"].favorable_score == 0.4  # 0.8 * 0.5


def test_contrary_mirror_cancellation():
    r1 = _modified("R1", "wealth", "favorable", 0.8)
    r2 = _modified("R2", "wealth", "unfavorable", 0.6)
    scores = aggregate_domains([r1, r2], contrary_mirrors={("R1", "R2")})
    assert scores["wealth"].net_score == 0.0
    assert scores["wealth"].rule_count == 0  # both cancelled


def test_same_signal_group_strongest_wins():
    r1 = _modified("R1", "wealth", "favorable", 0.8, signal_group="sig_1")
    r2 = _modified("R2", "wealth", "unfavorable", 0.5, signal_group="sig_1")
    scores = aggregate_domains([r1, r2])
    assert scores["wealth"].favorable_score > 0
    assert scores["wealth"].unfavorable_score == 0.0


def test_no_conflict_resolution_without_signal_group():
    """Rules without signal groups are independent — both contribute."""
    r1 = _modified("R1", "wealth", "favorable", 0.8)
    r2 = _modified("R2", "wealth", "unfavorable", 0.5)
    scores = aggregate_domains([r1, r2])
    assert scores["wealth"].favorable_score > 0
    assert scores["wealth"].unfavorable_score > 0
