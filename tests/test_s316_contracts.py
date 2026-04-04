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


from src.calculations.inference import aggregate_condition_metadata, CONSUMABLE_AGGREGATES


def test_aggregate_empty_conditions():
    result = aggregate_condition_metadata({})
    assert result["bb_strength"] == 0.0
    assert "argala_strength_total" not in result


def test_aggregate_argala_metadata():
    conditions = {
        "cond_0": {
            "type": "argala_condition",
            "metadata": {"argala_strength": 0.7},
        }
    }
    result = aggregate_condition_metadata(conditions)
    assert result["argala_strength_total"] == 0.7


def test_aggregate_caps_argala_at_1():
    conditions = {
        "cond_0": {"type": "argala_condition", "metadata": {"argala_strength": 0.6}},
        "cond_1": {"type": "argala_condition", "metadata": {"argala_strength": 0.7}},
    }
    result = aggregate_condition_metadata(conditions)
    assert result["argala_strength_total"] == 1.0


def test_consumable_aggregates_whitelist():
    assert "argala_strength_total" in CONSUMABLE_AGGREGATES
    assert "bb_strength" in CONSUMABLE_AGGREGATES
    assert "shadbala_normalized" in CONSUMABLE_AGGREGATES
    assert len(CONSUMABLE_AGGREGATES) == 3


from src.corpus.feature_registry import IMPLEMENTED_FEATURES, PENDING_FEATURES


def test_s316_features_implemented():
    s316 = {"argala_condition", "functional_benefic", "same_planet_constraint",
            "dynamic_karaka", "shadbala_strength", "navamsa_lagna",
            "modifier_execution", "bhavat_bhavam_execution",
            "modifier_condition_structured", "prediction_type_classification",
            "timing_activation"}
    for f in s316:
        assert f in IMPLEMENTED_FEATURES, f"{f} not in IMPLEMENTED_FEATURES"


def test_s316_features_not_pending():
    s316 = {"argala_condition", "functional_benefic", "same_planet_constraint",
            "dynamic_karaka", "shadbala_strength", "navamsa_lagna",
            "modifier_execution", "bhavat_bhavam_execution",
            "modifier_condition_structured", "prediction_type_classification"}
    for f in s316:
        assert f not in PENDING_FEATURES, f"{f} still in PENDING_FEATURES"
