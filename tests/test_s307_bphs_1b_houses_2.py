"""tests/test_s307_bphs_1b_houses_2.py — S307: BPHS Phase 1B Houses 2 tests.

Validates Phase 1B contract compliance for BPHS Ch.16-19 re-encode.
"""
from __future__ import annotations

import pytest

from src.corpus.bphs_1b_houses_2 import BPHS_1B_HOUSES_2_REGISTRY

RULES = BPHS_1B_HOUSES_2_REGISTRY.all()

VALID_DIRECTIONS = {"favorable", "unfavorable", "neutral", "mixed"}
VALID_INTENSITIES = {"strong", "moderate", "weak", "conditional"}
VALID_PHASES = {"1B_matrix", "1B_conditional", "1B_compound"}
VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
}


def test_total_rule_count():
    assert len(RULES) >= 60


def test_chapter_distribution():
    ch16 = [r for r in RULES if r.chapter == "Ch.16"]
    ch17 = [r for r in RULES if r.chapter == "Ch.17"]
    ch18 = [r for r in RULES if r.chapter == "Ch.18"]
    ch19 = [r for r in RULES if r.chapter == "Ch.19"]
    assert len(ch16) >= 20, f"Ch.16: {len(ch16)}"
    assert len(ch17) >= 12, f"Ch.17: {len(ch17)}"
    assert len(ch18) >= 15, f"Ch.18: {len(ch18)}"
    assert len(ch19) >= 15, f"Ch.19: {len(ch19)}"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    assert rule.rule_id.startswith("BPHS")
    assert len(rule.rule_id) == 8


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_primary_condition_populated(rule):
    assert isinstance(rule.primary_condition, dict)
    assert len(rule.primary_condition) >= 2
    assert "planet" in rule.primary_condition
    assert "placement_type" in rule.primary_condition


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_domains_from_taxonomy(rule):
    assert len(rule.outcome_domains) >= 1
    for domain in rule.outcome_domains:
        assert domain in VALID_DOMAINS, f"{rule.rule_id}: invalid '{domain}'"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_direction(rule):
    assert rule.outcome_direction in VALID_DIRECTIONS


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_intensity(rule):
    assert rule.outcome_intensity in VALID_INTENSITIES


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_verse_ref_format(rule):
    assert rule.verse_ref
    assert "Ch." in rule.verse_ref
    assert "v." in rule.verse_ref


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_phase_value(rule):
    assert rule.phase in VALID_PHASES


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_system_natal(rule):
    assert rule.system == "natal"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_is_bphs(rule):
    assert rule.source == "BPHS"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_confidence_in_range(rule):
    assert 0.60 <= rule.confidence <= 1.0


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_description_non_empty(rule):
    assert len(rule.description) >= 50


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_modifiers_structured(rule):
    assert isinstance(rule.modifiers, list)
    for mod in rule.modifiers:
        assert isinstance(mod, dict)
        assert "condition" in mod
        assert "effect" in mod
        assert mod["effect"] in ("amplifies", "negates", "conditionalizes", "modifies")


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_exceptions_are_strings(rule):
    assert isinstance(rule.exceptions, list)
    for exc in rule.exceptions:
        assert isinstance(exc, str)


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_no_modifier_redundancy(rule):
    """Modifiers must not restate the primary condition."""
    pc_type = rule.primary_condition.get("placement_type", "")
    for mod in rule.modifiers:
        cond = mod["condition"]
        # Modifier should not contain the placement type + value
        assert pc_type not in cond or "placement" not in cond, (
            f"{rule.rule_id}: modifier '{cond}' may duplicate primary_condition"
        )


def test_concordance_coverage():
    with_conc = [r for r in RULES if r.concordance_texts]
    ratio = len(with_conc) / len(RULES)
    assert ratio >= 0.35


def test_high_confidence_mechanical():
    for r in RULES:
        if len(r.concordance_texts) >= 3:
            assert r.confidence >= 0.84, f"{r.rule_id}: {r.confidence}"


def test_no_duplicate_rule_ids():
    ids = [r.rule_id for r in RULES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S307"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_school_parashari(rule):
    assert rule.school == "parashari"
