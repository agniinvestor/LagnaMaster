"""tests/test_s311_bphs_v2_ch13.py — S311: BPHS Ch.13 V2 contract tests."""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch13 import BPHS_V2_CH13_REGISTRY
from src.corpus.corpus_audit import (
    CorpusAudit,
    VALID_ENTITY_TARGETS,
    VALID_TIMING_TYPES,
)

RULES = BPHS_V2_CH13_REGISTRY.all()

VALID_DIRECTIONS = {"favorable", "unfavorable", "neutral", "mixed"}
from src.corpus.taxonomy import VALID_OUTCOME_DOMAINS as VALID_DOMAINS  # includes both legacy and primary


def test_total_rule_count():
    assert len(RULES) >= 13, f"Ch.13 has 13 slokas, got {len(RULES)} rules"


def test_no_duplicate_rule_ids():
    ids = [r.rule_id for r in RULES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    assert rule.rule_id.startswith("BPHS")
    assert len(rule.rule_id) == 8


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_and_chapter(rule):
    assert rule.source == "BPHS"
    assert "Ch.13" in rule.verse_ref


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
        assert isinstance(pred, dict)
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
    assert tw, f"{rule.rule_id}: timing_window unchecked"
    assert "type" in tw
    assert tw["type"] in VALID_TIMING_TYPES


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_primary_condition_has_planet(rule):
    assert "planet" in rule.primary_condition


def test_commentary_coverage():
    with_c = [r for r in RULES if r.commentary_context]
    assert len(with_c) / len(RULES) >= 0.60


def test_concordance_coverage():
    with_c = [r for r in RULES if r.concordance_texts]
    assert len(with_c) / len(RULES) >= 0.30


def test_contrary_mirrors_exist():
    mirrors = [r for r in RULES if r.rule_relationship.get("type") == "contrary_mirror"]
    assert len(mirrors) >= 1


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"


def test_v2_audit_zero_errors():
    audit = CorpusAudit(BPHS_V2_CH13_REGISTRY)
    report = audit.run()
    assert report["v2_errors"] == [], f"V2 errors: {report['v2_errors'][:5]}"
