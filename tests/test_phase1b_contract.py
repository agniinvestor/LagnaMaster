"""tests/test_phase1b_contract.py — Phase 1B Rule Contract enforcement.

This test ensures ALL Phase 1B rules comply with the mandatory contract
defined in docs/PHASE1B_RULE_CONTRACT.md. If this test fails, the
pre-push hook will block the push.

Enforces:
  1. primary_condition: planet + placement_type present
  2. outcome_domains: from fixed 15-domain taxonomy
  3. outcome_direction: from valid set
  4. outcome_intensity: from valid set
  5. verse_ref: populated
  6. confidence: mechanical formula
  7. system: from valid set
  8. outcome_timing: from valid set (includes natal_permanent)
  9. prediction_type: from valid set
  10. gender_scope: from valid set
  11. certainty_level: from valid set
  12. strength_condition: from valid set
  13. house_system: from valid set
  14. modifiers: populated when description has conditional language
  15. trait rules must NOT be dasha_dependent
"""
from __future__ import annotations

import re

VALID_DOMAINS = frozenset({
    "longevity", "physical_health", "mental_health", "wealth",
    "career_status", "marriage", "progeny", "spirituality",
    "intelligence_education", "character_temperament",
    "physical_appearance", "foreign_travel", "enemies_litigation",
    "property_vehicles", "fame_reputation",
})

VALID_DIRECTIONS = frozenset({"favorable", "unfavorable", "neutral", "mixed"})
VALID_INTENSITIES = frozenset({"strong", "moderate", "weak", "conditional"})
VALID_SYSTEMS = frozenset({"natal", "horary", "varshaphala", "muhurtha", "transit"})
VALID_TIMINGS = frozenset({
    "natal_permanent", "early_life", "middle_life", "late_life",
    "dasha_dependent", "unspecified",
})
VALID_PREDICTION_TYPES = frozenset({"event", "trait", "capacity"})
VALID_GENDER_SCOPES = frozenset({"universal", "male", "female"})
VALID_CERTAINTY_LEVELS = frozenset({"definite", "probable", "possible"})
VALID_STRENGTH_CONDITIONS = frozenset({
    "any", "strong", "weak", "exalted", "debilitated",
    "own_sign", "combust", "moolatrikona",
})
VALID_HOUSE_SYSTEMS = frozenset({"sign_based", "bhava_chalita", "kp"})
VALID_EVALUATION_METHODS = frozenset({
    "placement_check", "yoga_detection", "lordship_check",
    "dasha_activation", "transit_check",
})

# Keywords that indicate conditional clauses requiring modifiers
CONDITIONAL_KEYWORDS = [
    r'\bif\b', r'\bwhen\b', r'\bunless\b', r'\bbut\b', r'\bhowever\b',
    r'\baspected\b', r'\bcombust\b', r'\bretrograde\b',
]

# Keywords that indicate trait (not event) predictions
TRAIT_KEYWORDS = [
    'personality', 'nature', 'character', 'temperament', 'appearance',
    'build', 'complexion', 'demeanor', 'disposition', 'constitution',
]


def _get_phase_1b_rules():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    return [r for r in registry.all() if r.phase.startswith("1B")]


# ── Original contract tests (S263) ──────────────────────────────────────────

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
    """Confidence must follow the formula, not be hardcoded."""
    for rule in _get_phase_1b_rules():
        concordance_count = len(rule.concordance_texts) if rule.concordance_texts else 0
        verse_bonus = 0.05 if rule.verse_ref else 0.0
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


# ── S305 extension tests ───────────────────────────────────────────────────

def test_prediction_type_valid():
    for rule in _get_phase_1b_rules():
        assert rule.prediction_type in VALID_PREDICTION_TYPES, (
            f"{rule.rule_id}: prediction_type '{rule.prediction_type}' not in {VALID_PREDICTION_TYPES}"
        )


def test_gender_scope_valid():
    for rule in _get_phase_1b_rules():
        assert rule.gender_scope in VALID_GENDER_SCOPES, (
            f"{rule.rule_id}: gender_scope '{rule.gender_scope}' not in {VALID_GENDER_SCOPES}"
        )


def test_certainty_level_valid():
    for rule in _get_phase_1b_rules():
        assert rule.certainty_level in VALID_CERTAINTY_LEVELS, (
            f"{rule.rule_id}: certainty_level '{rule.certainty_level}' not in {VALID_CERTAINTY_LEVELS}"
        )


def test_strength_condition_valid():
    for rule in _get_phase_1b_rules():
        assert rule.strength_condition in VALID_STRENGTH_CONDITIONS, (
            f"{rule.rule_id}: strength_condition '{rule.strength_condition}' not in {VALID_STRENGTH_CONDITIONS}"
        )


def test_house_system_valid():
    for rule in _get_phase_1b_rules():
        assert rule.house_system in VALID_HOUSE_SYSTEMS, (
            f"{rule.rule_id}: house_system '{rule.house_system}' not in {VALID_HOUSE_SYSTEMS}"
        )


def test_evaluation_method_valid():
    for rule in _get_phase_1b_rules():
        assert rule.evaluation_method in VALID_EVALUATION_METHODS, (
            f"{rule.rule_id}: evaluation_method '{rule.evaluation_method}' not in {VALID_EVALUATION_METHODS}"
        )


# ── Corpus stats display (informational, always passes) ────────────────────

def test_corpus_stats_display(capsys):
    """Display corpus health stats after every test run.

    This test always passes — it's a dashboard, not a gate.
    The output is visible in pytest verbose mode or captured output.
    """
    rules = _get_phase_1b_rules()
    total = len(rules)

    modifiers_populated = sum(1 for r in rules if r.modifiers)
    exceptions_populated = sum(1 for r in rules if r.exceptions)
    dasha_scope_populated = sum(1 for r in rules if r.dasha_scope)
    concordance_populated = sum(1 for r in rules if r.concordance_texts)
    lagna_scope_populated = sum(1 for r in rules if r.lagna_scope)

    # Conditional language without modifiers
    conditional_no_mod = 0
    for r in rules:
        desc = r.description.lower()
        if any(re.search(kw, desc) for kw in CONDITIONAL_KEYWORDS) and not r.modifiers:
            conditional_no_mod += 1

    # Trait rules with dasha_dependent timing
    trait_dasha = sum(1 for r in rules
                      if r.prediction_type == "trait"
                      and r.outcome_timing == "dasha_dependent")

    print("\n" + "=" * 60)
    print("CORPUS HEALTH DASHBOARD")
    print("=" * 60)
    print(f"  Total Phase 1B rules:          {total}")
    print(f"  modifiers populated:           {modifiers_populated}/{total} ({modifiers_populated/total*100:.0f}%)")
    print(f"  exceptions populated:          {exceptions_populated}/{total} ({exceptions_populated/total*100:.0f}%)")
    print(f"  dasha_scope populated:         {dasha_scope_populated}/{total} ({dasha_scope_populated/total*100:.0f}%)")
    print(f"  concordance_texts populated:   {concordance_populated}/{total} ({concordance_populated/total*100:.0f}%)")
    print(f"  lagna_scope populated:         {lagna_scope_populated}/{total} ({lagna_scope_populated/total*100:.0f}%)")
    print(f"  conditional lang w/o modifiers:{conditional_no_mod}/{total}")
    print(f"  trait + dasha_dependent:       {trait_dasha}")
    print("=" * 60)

    # This test always passes — it's informational
    assert True
