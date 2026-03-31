"""tests/test_s311_bphs_v2_ch16.py — S311: BPHS Ch.16 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch16 import BPHS_V2_CH16_REGISTRY
from src.corpus.corpus_audit import CorpusAudit, VALID_ENTITY_TARGETS, VALID_TIMING_TYPES

RULES = BPHS_V2_CH16_REGISTRY.all()
VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
}


def test_total_rule_count():
    assert len(RULES) >= 15


def test_no_duplicate_rule_ids():
    assert len([r.rule_id for r in RULES]) == len(set(r.rule_id for r in RULES))


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    assert rule.rule_id.startswith("BPHS") and len(rule.rule_id) == 8


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_and_chapter(rule):
    assert rule.source == "BPHS" and "Ch.16" in rule.verse_ref


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_non_empty(rule):
    assert len(rule.predictions) >= 1


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_structure(rule):
    for i, pred in enumerate(rule.predictions):
        for key in ("entity", "claim", "domain", "direction"):
            assert key in pred


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_entity_target_valid(rule):
    assert rule.entity_target in VALID_ENTITY_TARGETS


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_signal_group_non_empty(rule):
    assert rule.signal_group


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_timing_window_checked(rule):
    tw = rule.timing_window
    assert tw and "type" in tw and tw["type"] in VALID_TIMING_TYPES


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_primary_condition_has_planet(rule):
    assert "planet" in rule.primary_condition


def test_specific_timing_rules():
    """Ch.16 has rules with specific ages (30, 32, 33, 36, 40, 56)."""
    timed = [r for r in RULES if r.timing_window.get("type") in ("age", "age_range")]
    assert len(timed) >= 5


def test_children_entity_dominant():
    """Ch.16 is about children — majority should target children."""
    children = [r for r in RULES if r.entity_target == "children"]
    assert len(children) / len(RULES) >= 0.50


def test_contrary_mirrors_exist():
    assert any(r.rule_relationship.get("type") == "contrary_mirror" for r in RULES)


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_v2_audit_zero_errors():
    audit = CorpusAudit(BPHS_V2_CH16_REGISTRY)
    assert audit.run()["v2_errors"] == []
