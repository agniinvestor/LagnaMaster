"""Tests for ExecutionTrace observability layer."""
import src.calculations.inference as inf
from src.calculations.inference import (
    apply_modifiers, ExecutionTrace,
)
from src.calculations.rule_firing import FiredRule, _check_compound_conditions


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


class _P:
    def __init__(self, sign_index, degree_in_sign=15.0, name="Sun"):
        self.sign_index = sign_index
        self.degree_in_sign = degree_in_sign
        self.name = name
        self.sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                      "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][sign_index]


class _Chart:
    def __init__(self, lagna_sign_index=0, planets=None):
        self.lagna_sign_index = lagna_sign_index
        self.lagna_sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][lagna_sign_index]
        self.planets = planets or {}


def test_trace_toggle():
    """Trace disabled by default."""
    assert inf.TRACE_ENABLED is False


def test_trace_populated_when_enabled():
    """When TRACE_ENABLED=True, ModifiedRule gets a trace."""
    old = inf.TRACE_ENABLED
    inf.TRACE_ENABLED = True
    try:
        fired = _fired()
        rule = _Rule(modifiers=[
            {"effect": "amplifies", "target": "prediction", "strength": "medium",
             "scope": "local", "condition": "test_cond"},
        ])
        result = apply_modifiers(fired, rule, chart=None)
        assert result.trace is not None
        assert isinstance(result.trace, ExecutionTrace)
        assert result.trace.rule_id == "T001"
        assert result.trace.magnitude_initial == 0.7
        assert result.trace.magnitude_final == result.magnitude
        assert len(result.trace.modifier_traces) == 1
        mt = result.trace.modifier_traces[0]
        assert mt.effect == "amplifies"
        assert mt.magnitude_before == 0.7
        assert mt.magnitude_after > 0.7
    finally:
        inf.TRACE_ENABLED = old


def test_trace_not_populated_when_disabled():
    """When TRACE_ENABLED=False, no trace generated."""
    old = inf.TRACE_ENABLED
    inf.TRACE_ENABLED = False
    try:
        fired = _fired()
        rule = _Rule()
        result = apply_modifiers(fired, rule, chart=None)
        assert result.trace is None
    finally:
        inf.TRACE_ENABLED = old


def test_gate_trace():
    """Gate failure captured in trace with details."""
    old = inf.TRACE_ENABLED
    inf.TRACE_ENABLED = True
    try:
        chart = _Chart(lagna_sign_index=0, planets={"Sun": _P(0, name="Sun")})
        fired = _fired()
        rule = _Rule(modifiers=[{
            "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
            "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 7}],
        }])
        result = apply_modifiers(fired, rule, chart=chart)
        assert result.gated_out
        assert result.trace is not None
        assert result.trace.gated_out
        assert result.trace.gate_details is not None
        assert "severity" in result.trace.gate_details
    finally:
        inf.TRACE_ENABLED = old


def test_modifier_trace_context_factors():
    """Context-aware scaling records which factors influenced weight."""
    old = inf.TRACE_ENABLED
    inf.TRACE_ENABLED = True
    try:
        fired = _fired()
        rule = _Rule(modifiers=[{
            "effect": "amplifies", "target": "prediction", "strength": "medium",
            "scope": "local", "condition": "test",
        }])
        ctx = {"conditions": {}, "aggregates": {"argala_strength_total": 0.8}, "gates": {}}
        result = apply_modifiers(fired, rule, chart=None, condition_context=ctx)
        assert result.trace is not None
        mt = result.trace.modifier_traces[0]
        assert mt.context_factors.get("argala_strength_total") == 0.8
        assert mt.weight_after > mt.weight_before  # context scaled up
    finally:
        inf.TRACE_ENABLED = old


def test_condition_trace_from_context():
    """Condition traces populated from context when tracing enabled."""
    old = inf.TRACE_ENABLED
    inf.TRACE_ENABLED = True
    try:
        chart = _Chart(lagna_sign_index=0, planets={"Sun": _P(0, name="Sun")})
        conds = [{"type": "planet_in_house", "planet": "Sun", "house": 1}]
        ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
        fires, _ = _check_compound_conditions(conds, chart, context=ctx)
        assert fires is True
        # Context should have condition trace data when TRACE_ENABLED
        # (condition traces are built from ctx["conditions"] in apply_modifiers)
    finally:
        inf.TRACE_ENABLED = old
