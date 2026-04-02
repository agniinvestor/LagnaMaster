"""tests/test_condition_modifier_audit.py — Tests for condition/modifier audit."""
from __future__ import annotations

from tools.condition_modifier_audit import classify_modifier, scan_commentary_for_missing_exceptions


def test_classify_must_keyword_high():
    result = classify_modifier(
        modifier={"condition": "2nd_lord_must_be_in_10th", "effect": "conditionalizes"},
        commentary="Santhanam: Eight sons if Jupiter in 5th/9th + 5th lord strong + 2nd lord in 10th.",
    )
    assert result["confidence"] == "high"
    assert result["type"] == "modifier_should_be_condition"


def test_classify_required_keyword_high():
    result = classify_modifier(
        modifier={"condition": "moon_rahu_conjunction_required", "effect": "amplifies"},
        commentary="Three conditions required: (a) Saturn in 5th (b) lord in movable (c) Moon with Rahu.",
    )
    assert result["confidence"] == "high"


def test_classify_enumeration_pattern_high():
    result = classify_modifier(
        modifier={"condition": "h5_lord_in_movable_sign", "effect": "conditionalizes"},
        commentary="Santhanam notes: 3 conditions — (a) 5th lord in movable sign, (b) Saturn in 5th, (c) Moon with Rahu.",
    )
    assert result["confidence"] == "high"


def test_classify_placement_pattern_medium():
    result = classify_modifier(
        modifier={"condition": "benefic_in_12th", "effect": "amplifies"},
        commentary="No separate Santhanam note.",
    )
    assert result["confidence"] == "medium"


def test_classify_amplifier_low():
    result = classify_modifier(
        modifier={"condition": "aspected_by_benefic_more_favorable", "effect": "amplifies"},
        commentary="Benefic aspect makes results more favorable.",
    )
    assert result["confidence"] == "low"


def test_missing_exception_detected():
    flags = scan_commentary_for_missing_exceptions(
        commentary="The combinations get nullified if Jupiter aspects the 5th house.",
        exceptions=[],
    )
    assert len(flags) == 1
    assert "nullified" in flags[0]["evidence"].lower()


def test_no_false_positive_exception():
    flags = scan_commentary_for_missing_exceptions(
        commentary="No separate Santhanam note.",
        exceptions=[],
    )
    assert len(flags) == 0
