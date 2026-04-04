"""Tests for Wave 0 contracts: context accumulator, aggregation, whitelist."""
from src.calculations.rule_firing import (
    _check_compound_conditions, FiredRule,
)


def test_context_param_accepted():
    """_check_compound_conditions accepts optional context dict."""
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    result = _check_compound_conditions([], None, context=ctx)
    assert result == (False, 0)


def test_context_param_optional():
    """Existing callers without context still work."""
    result = _check_compound_conditions([], None)
    assert result == (False, 0)


def test_fired_rule_has_context_field():
    """FiredRule dataclass has a context field."""
    fired = FiredRule(
        rule_id="TEST", source="BPHS", planet="Sun", house=1,
        outcome_direction="favorable", outcome_domains=["wealth"],
        confidence=0.7, concordance_count=0,
    )
    assert hasattr(fired, "context")
    assert fired.context is None
