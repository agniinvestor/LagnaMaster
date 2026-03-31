"""tests/test_s311_bphs_v2_ch18.py — S311: BPHS Ch.18 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch18 import BPHS_V2_CH18_REGISTRY
from src.corpus.corpus_audit import CorpusAudit, VALID_ENTITY_TARGETS, VALID_TIMING_TYPES

RULES = BPHS_V2_CH18_REGISTRY.all()


def test_total_rule_count():
    assert len(RULES) >= 20


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


def test_marriage_timing_rules():
    """Ch.18 has 13+ marriage timing rules with specific ages."""
    timed = [r for r in RULES if r.timing_window.get("type") in ("age", "age_range")
             and "marriage" in r.signal_group]
    assert len(timed) >= 10


def test_wife_death_timing_rules():
    """Ch.18 has 4+ wife death timing rules."""
    death = [r for r in RULES if "wife_death" in r.signal_group or "wife_short" in r.signal_group]
    assert len(death) >= 4


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_v2_audit_zero_errors():
    audit = CorpusAudit(BPHS_V2_CH18_REGISTRY)
    assert audit.run()["v2_errors"] == []
