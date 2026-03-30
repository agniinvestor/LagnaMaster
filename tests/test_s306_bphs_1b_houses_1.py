"""tests/test_s306_bphs_1b_houses_1.py — S306: BPHS Phase 1B Houses 1 tests.

Validates Phase 1B contract compliance for BPHS Ch.12-15 re-encode.
"""
from __future__ import annotations

import pytest

from src.corpus.bphs_1b_houses_1 import BPHS_1B_HOUSES_1_REGISTRY

RULES = BPHS_1B_HOUSES_1_REGISTRY.all()

# ── Rule count tests ─────────────────────────────────────────────────────────

def test_total_rule_count():
    """S306 encodes Ch.12-15: at least 70 rules from 76 predictive slokas."""
    assert len(RULES) >= 70


def test_chapter_distribution():
    """Each chapter must have rules proportional to its sloka count."""
    ch12 = [r for r in RULES if r.chapter == "Ch.12"]
    ch13 = [r for r in RULES if r.chapter == "Ch.13"]
    ch14 = [r for r in RULES if r.chapter == "Ch.14"]
    ch15 = [r for r in RULES if r.chapter == "Ch.15"]
    # Ch.12 has 16 slokas → at least 16 rules
    assert len(ch12) >= 16, f"Ch.12 has {len(ch12)} rules, expected >= 16"
    # Ch.13 has 12 slokas → at least 12 rules
    assert len(ch13) >= 12, f"Ch.13 has {len(ch13)} rules, expected >= 12"
    # Ch.14 has 20 predictive slokas → at least 15 rules
    assert len(ch14) >= 15, f"Ch.14 has {len(ch14)} rules, expected >= 15"
    # Ch.15 has 28 predictive slokas → at least 20 rules
    assert len(ch15) >= 20, f"Ch.15 has {len(ch15)} rules, expected >= 20"


# ── Phase 1B contract compliance ─────────────────────────────────────────────

VALID_DIRECTIONS = {"favorable", "unfavorable", "neutral", "mixed"}
VALID_INTENSITIES = {"strong", "moderate", "weak", "conditional"}
VALID_PHASES = {"1B_matrix", "1B_conditional", "1B_compound"}
VALID_SYSTEMS = {"natal", "horary", "varshaphala", "transit", "muhurtha"}
VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
}


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    """Rule IDs must start with BPHS and be 8 chars."""
    assert rule.rule_id.startswith("BPHS"), f"{rule.rule_id} bad prefix"
    assert len(rule.rule_id) == 8, f"{rule.rule_id} bad length"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_primary_condition_populated(rule):
    """primary_condition must be a non-empty dict."""
    assert isinstance(rule.primary_condition, dict)
    assert len(rule.primary_condition) >= 2, f"{rule.rule_id}: primary_condition too sparse"
    assert "planet" in rule.primary_condition, f"{rule.rule_id}: missing planet"
    assert "placement_type" in rule.primary_condition, f"{rule.rule_id}: missing placement_type"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_domains_from_taxonomy(rule):
    """outcome_domains must be non-empty and from the 15-domain taxonomy."""
    assert len(rule.outcome_domains) >= 1, f"{rule.rule_id}: empty outcome_domains"
    for domain in rule.outcome_domains:
        assert domain in VALID_DOMAINS, f"{rule.rule_id}: invalid domain '{domain}'"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_direction(rule):
    """outcome_direction must be one of 4 valid values."""
    assert rule.outcome_direction in VALID_DIRECTIONS, (
        f"{rule.rule_id}: invalid direction '{rule.outcome_direction}'"
    )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_intensity(rule):
    """outcome_intensity must be one of 4 valid values."""
    assert rule.outcome_intensity in VALID_INTENSITIES, (
        f"{rule.rule_id}: invalid intensity '{rule.outcome_intensity}'"
    )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_verse_ref_format(rule):
    """verse_ref must have chapter AND verse (Phase 1B requirement)."""
    assert rule.verse_ref, f"{rule.rule_id}: empty verse_ref"
    assert "Ch." in rule.verse_ref, f"{rule.rule_id}: missing 'Ch.' in verse_ref"
    assert "v." in rule.verse_ref, f"{rule.rule_id}: missing 'v.' in verse_ref"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_phase_value(rule):
    """phase must be one of the Phase 1B values."""
    assert rule.phase in VALID_PHASES, f"{rule.rule_id}: invalid phase '{rule.phase}'"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_system_value(rule):
    """system must be 'natal' for BPHS house-effect chapters."""
    assert rule.system in VALID_SYSTEMS, f"{rule.rule_id}: invalid system"
    # Ch.12-15 are all natal
    assert rule.system == "natal", f"{rule.rule_id}: expected natal"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_is_bphs(rule):
    """Source must be BPHS."""
    assert rule.source == "BPHS"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_confidence_in_range(rule):
    """Confidence must be mechanically calculated and in valid range."""
    assert 0.60 <= rule.confidence <= 1.0, (
        f"{rule.rule_id}: confidence {rule.confidence} out of range"
    )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_description_non_empty(rule):
    """Description must be substantial, not a placeholder."""
    assert len(rule.description) >= 50, (
        f"{rule.rule_id}: description too short ({len(rule.description)} chars)"
    )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_modifiers_are_structured(rule):
    """Modifiers must be a list of dicts with required keys."""
    assert isinstance(rule.modifiers, list)
    for mod in rule.modifiers:
        assert isinstance(mod, dict), f"{rule.rule_id}: modifier not a dict"
        assert "condition" in mod, f"{rule.rule_id}: modifier missing 'condition'"
        assert "effect" in mod, f"{rule.rule_id}: modifier missing 'effect'"
        assert mod["effect"] in ("amplifies", "negates", "conditionalizes", "modifies"), (
            f"{rule.rule_id}: invalid modifier effect '{mod['effect']}'"
        )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_exceptions_are_list_of_strings(rule):
    """Exceptions must be a list of strings."""
    assert isinstance(rule.exceptions, list)
    for exc in rule.exceptions:
        assert isinstance(exc, str), f"{rule.rule_id}: exception not a string"


# ── Concordance quality ──────────────────────────────────────────────────────

def test_concordance_coverage():
    """At least 40% of rules should have concordance texts (BPHS is anchor)."""
    with_conc = [r for r in RULES if r.concordance_texts]
    ratio = len(with_conc) / len(RULES)
    assert ratio >= 0.40, (
        f"Only {ratio:.0%} of rules have concordance, expected >= 40%"
    )


def test_high_confidence_rules_exist():
    """Rules with 3+ concordance texts should reach >=0.84 confidence."""
    high_conc = [r for r in RULES if len(r.concordance_texts) >= 3]
    if high_conc:
        for r in high_conc:
            assert r.confidence >= 0.84, (
                f"{r.rule_id}: 3+ concordance but confidence={r.confidence}"
            )


def test_no_duplicate_rule_ids():
    """All rule IDs must be unique."""
    ids = [r.rule_id for r in RULES]
    assert len(ids) == len(set(ids)), "Duplicate rule IDs found"


# ── S305 extension fields ───────────────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    """last_modified_session must be S306."""
    assert rule.last_modified_session == "S306"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_school_is_parashari(rule):
    """School must be parashari for BPHS rules."""
    assert rule.school == "parashari"
