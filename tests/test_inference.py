"""Tests for inference engine — modifier application + domain aggregation."""
import pytest
from src.calculations.inference import (
    apply_modifiers, aggregate_domains, ModifiedRule,
)
from src.calculations.rule_firing import FiredRule


def _make_fired(rule_id="TEST001", direction="favorable", confidence=0.7):
    return FiredRule(
        rule_id=rule_id, source="BPHS", planet="Sun", house=1,
        outcome_direction=direction, outcome_domains=["wealth"],
        confidence=confidence, concordance_count=0,
    )


class _FakeRule:
    def __init__(self, predictions=None, modifiers=None, primary_domain="wealth"):
        self.predictions = predictions or [{"magnitude": 0.7, "domain": "wealth"}]
        self.modifiers = modifiers or []
        self.primary_domain = primary_domain


def test_apply_modifiers_no_modifiers():
    fired = _make_fired()
    rule = _FakeRule()
    result = apply_modifiers(fired, rule)
    assert result.magnitude == 0.7
    assert result.direction == "favorable"


def test_apply_modifiers_amplifies():
    fired = _make_fired()
    rule = _FakeRule(modifiers=[
        {"effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local", "condition": "test"}
    ])
    result = apply_modifiers(fired, rule)
    assert result.magnitude > 0.7  # amplified


def test_apply_modifiers_attenuates():
    fired = _make_fired()
    rule = _FakeRule(modifiers=[
        {"effect": "attenuates", "target": "prediction", "strength": "strong", "scope": "local", "condition": "test"}
    ])
    result = apply_modifiers(fired, rule)
    assert result.magnitude < 0.7  # weakened


def test_apply_modifiers_negates():
    fired = _make_fired(direction="favorable")
    rule = _FakeRule(modifiers=[
        {"effect": "negates", "target": "prediction", "strength": "strong", "scope": "local", "condition": "test"}
    ])
    result = apply_modifiers(fired, rule)
    assert result.direction == "unfavorable"  # flipped


def test_apply_modifiers_qualifies():
    fired = _make_fired()
    rule = _FakeRule(modifiers=[
        {"effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local", "condition": "more_daughters"}
    ])
    result = apply_modifiers(fired, rule)
    assert "more_daughters" in result.qualifications
    assert result.magnitude == 0.7  # unchanged


def test_aggregate_domains():
    rules = [
        ModifiedRule(rule_id="R1", primary_domain="wealth", direction="favorable", magnitude=0.8, source_rule=_make_fired()),
        ModifiedRule(rule_id="R2", primary_domain="wealth", direction="unfavorable", magnitude=0.5, source_rule=_make_fired()),
        ModifiedRule(rule_id="R3", primary_domain="health", direction="favorable", magnitude=0.6, source_rule=_make_fired()),
    ]
    scores = aggregate_domains(rules)
    # Confidence-weighted: magnitude * confidence (0.7 default)
    assert scores["wealth"].favorable_score == pytest.approx(0.8 * 0.7)
    assert scores["wealth"].unfavorable_score == pytest.approx(0.5 * 0.7)
    assert scores["wealth"].net_score == pytest.approx(round(0.8 * 0.7 - 0.5 * 0.7, 3))
    assert scores["wealth"].rule_count == 2
    assert scores["health"].favorable_score == pytest.approx(0.6 * 0.7)
    assert scores["health"].rule_count == 1
