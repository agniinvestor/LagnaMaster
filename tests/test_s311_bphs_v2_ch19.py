"""tests/test_s311_bphs_v2_ch19.py — S311: BPHS Ch.19 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch19 import BPHS_V2_CH19_REGISTRY
from src.corpus.corpus_audit import CorpusAudit, VALID_ENTITY_TARGETS, VALID_TIMING_TYPES

RULES = BPHS_V2_CH19_REGISTRY.all()


def test_total_rule_count():
    assert len(RULES) >= 4


def test_no_duplicate_rule_ids():
    assert len([r.rule_id for r in RULES]) == len(set(r.rule_id for r in RULES))


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_non_empty(rule):
    assert len(rule.predictions) >= 1


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


def test_longevity_domain():
    """Ch.19 is about longevity — all rules should have longevity domain."""
    longevity = [r for r in RULES if "longevity" in r.outcome_domains]
    assert len(longevity) == len(RULES)


def test_contrary_mirror():
    assert any(r.rule_relationship.get("type") == "contrary_mirror" for r in RULES)


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_v2_audit_zero_errors():
    assert CorpusAudit(BPHS_V2_CH19_REGISTRY).run()["v2_errors"] == []
