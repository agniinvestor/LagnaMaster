"""tests/test_s311_bphs_v2_ch17.py — S311: BPHS Ch.17 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch17 import BPHS_V2_CH17_REGISTRY
from src.corpus.corpus_audit import CorpusAudit, VALID_ENTITY_TARGETS, VALID_TIMING_TYPES

RULES = BPHS_V2_CH17_REGISTRY.all()
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


def test_timing_rich_chapter():
    """Ch.17 is extremely timing-rich — at least 10 rules with specific ages."""
    timed = [r for r in RULES if r.timing_window.get("type") in ("age", "age_range")]
    assert len(timed) >= 10


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_v2_audit_zero_errors():
    audit = CorpusAudit(BPHS_V2_CH17_REGISTRY)
    assert audit.run()["v2_errors"] == []
