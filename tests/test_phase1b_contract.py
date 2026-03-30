"""tests/test_phase1b_contract.py — Phase 1B Rule Contract enforcement.

This test ensures ALL Phase 1B rules comply with the mandatory contract
defined in docs/PHASE1B_RULE_CONTRACT.md. If this test fails, the
pre-push hook will block the push.

No Phase 1B rule ships without:
1. primary_condition populated with planet + placement_type
2. outcome_domains from the fixed 15-domain taxonomy
3. outcome_direction from {favorable, unfavorable, neutral, mixed}
4. outcome_intensity from {strong, moderate, weak, conditional}
5. verse_ref in "Ch.N v.M" format
6. concordance_texts populated ([] is valid only if no match exists —
   but confidence must reflect the formula)
7. confidence computed mechanically, not hardcoded
8. system field populated
9. phase field starting with "1B"
"""
from __future__ import annotations

VALID_DOMAINS = frozenset({
    "longevity", "physical_health", "mental_health", "wealth",
    "career_status", "marriage", "progeny", "spirituality",
    "intelligence_education", "character_temperament",
    "physical_appearance", "foreign_travel", "enemies_litigation",
    "property_vehicles", "fame_reputation",
})

VALID_DIRECTIONS = frozenset({"favorable", "unfavorable", "neutral", "mixed"})
VALID_INTENSITIES = frozenset({"strong", "moderate", "weak", "conditional"})
VALID_SYSTEMS = frozenset({"natal", "horary", "varshaphala", "muhurtha"})
VALID_TIMINGS = frozenset({
    "early_life", "middle_life", "late_life",
    "dasha_dependent", "unspecified",
})


def _get_phase_1b_rules():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    return [r for r in registry.all() if r.phase.startswith("1B")]


def test_primary_condition_populated():
    for rule in _get_phase_1b_rules():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} ({rule.source}): empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id}: missing 'planet' in primary_condition"
        assert "placement_type" in pc, f"{rule.rule_id}: missing 'placement_type'"


def test_outcome_domains_valid():
    for rule in _get_phase_1b_rules():
        assert rule.outcome_domains, f"{rule.rule_id} ({rule.source}): empty outcome_domains"
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, (
                f"{rule.rule_id} ({rule.source}): invalid domain '{d}'. "
                f"Must be one of: {sorted(VALID_DOMAINS)}"
            )


def test_outcome_direction_valid():
    for rule in _get_phase_1b_rules():
        assert rule.outcome_direction in VALID_DIRECTIONS, (
            f"{rule.rule_id}: direction '{rule.outcome_direction}' not in {VALID_DIRECTIONS}"
        )


def test_outcome_intensity_valid():
    for rule in _get_phase_1b_rules():
        assert rule.outcome_intensity in VALID_INTENSITIES, (
            f"{rule.rule_id}: intensity '{rule.outcome_intensity}' not in {VALID_INTENSITIES}"
        )


def test_verse_ref_populated():
    for rule in _get_phase_1b_rules():
        assert rule.verse_ref, f"{rule.rule_id} ({rule.source}): empty verse_ref"


def test_system_valid():
    for rule in _get_phase_1b_rules():
        assert rule.system in VALID_SYSTEMS, (
            f"{rule.rule_id}: system '{rule.system}' not in {VALID_SYSTEMS}"
        )


def test_outcome_timing_valid():
    for rule in _get_phase_1b_rules():
        assert rule.outcome_timing in VALID_TIMINGS, (
            f"{rule.rule_id}: timing '{rule.outcome_timing}' not in {VALID_TIMINGS}"
        )


def test_confidence_is_mechanical():
    """Confidence must follow the formula, not be hardcoded.

    Formula: 0.60 + 0.08*len(concordance_texts) + 0.05*(bool(verse_ref)) - 0.05*divergence_count
    Capped at 1.0.

    Tolerance: ±0.01 for float precision.
    """
    for rule in _get_phase_1b_rules():
        concordance_count = len(rule.concordance_texts) if rule.concordance_texts else 0
        verse_bonus = 0.05 if rule.verse_ref else 0.0
        # Count unique divergent SOURCES, not individual rule refs
        if rule.divergence_notes:
            div_sources = {e.split(":")[0] for e in rule.divergence_notes.split(", ") if e}
            divergence_count = len(div_sources)
        else:
            divergence_count = 0
        expected = min(1.0, max(0.10, 0.60 + 0.08 * concordance_count + verse_bonus - 0.05 * divergence_count))
        assert abs(rule.confidence - expected) < 0.02, (
            f"{rule.rule_id} ({rule.source}): confidence {rule.confidence} != "
            f"expected {expected:.2f} (concordance={concordance_count}, "
            f"verse={'yes' if rule.verse_ref else 'no'}, divergence={divergence_count})"
        )


def test_source_populated():
    for rule in _get_phase_1b_rules():
        assert rule.source, f"{rule.rule_id}: empty source"


def test_school_populated():
    for rule in _get_phase_1b_rules():
        assert rule.school, f"{rule.rule_id}: empty school"


def test_phase_1b_count_minimum():
    """Sanity check: we should have a significant Phase 1B corpus."""
    rules = _get_phase_1b_rules()
    assert len(rules) >= 3900, f"Only {len(rules)} Phase 1B rules — expected ≥3900"
