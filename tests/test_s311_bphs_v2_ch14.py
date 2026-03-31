"""tests/test_s311_bphs_v2_ch14.py — S311: BPHS Ch.14 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch14 import BPHS_V2_CH14_REGISTRY
from src.corpus.corpus_audit import CorpusAudit, VALID_ENTITY_TARGETS, VALID_TIMING_TYPES

RULES = BPHS_V2_CH14_REGISTRY.all()
VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
}


def test_total_rule_count():
    assert len(RULES) >= 12


def test_no_duplicate_rule_ids():
    assert len([r.rule_id for r in RULES]) == len(set(r.rule_id for r in RULES))


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    assert rule.rule_id.startswith("BPHS") and len(rule.rule_id) == 8


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_and_chapter(rule):
    assert rule.source == "BPHS"
    assert "Ch.14" in rule.verse_ref


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_domains_valid(rule):
    assert len(rule.outcome_domains) >= 1
    for d in rule.outcome_domains:
        assert d in VALID_DOMAINS


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_non_empty(rule):
    assert len(rule.predictions) >= 1


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_structure(rule):
    for i, pred in enumerate(rule.predictions):
        for key in ("entity", "claim", "domain", "direction"):
            assert key in pred, f"{rule.rule_id}: predictions[{i}] missing '{key}'"
        assert pred["entity"] in VALID_ENTITY_TARGETS


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


def test_commentary_coverage():
    assert len([r for r in RULES if r.commentary_context]) / len(RULES) >= 0.60


def test_concordance_coverage():
    assert len([r for r in RULES if r.concordance_texts]) / len(RULES) >= 0.30


def test_contrary_mirrors_exist():
    assert any(r.rule_relationship.get("type") == "contrary_mirror" for r in RULES)


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_entity_target_is_siblings():
    """Ch.14 is a siblings chapter — all rules should target siblings."""
    sibling_rules = [r for r in RULES if r.entity_target == "siblings"]
    assert len(sibling_rules) / len(RULES) >= 0.90


def test_v2_audit_zero_errors():
    audit = CorpusAudit(BPHS_V2_CH14_REGISTRY)
    report = audit.run()
    assert report["v2_errors"] == []
