"""tests/test_s311_bphs_v2_ch12.py — S311: BPHS Ch.12 V2 contract tests.

Validates EVERY V2 dimension for Ch.12 (1st House Effects) re-encode.
This is the V2 test template — all future V2 encoding sessions must
have an equivalent test file.
"""
from __future__ import annotations

import pytest

from src.corpus.bphs_v2_ch12 import BPHS_V2_CH12_REGISTRY
from src.corpus.corpus_audit import (
    CorpusAudit,
    VALID_ENTITY_TARGETS,
    VALID_TIMING_TYPES,
    VALID_RELATIONSHIP_TYPES,
)

RULES = BPHS_V2_CH12_REGISTRY.all()

VALID_DIRECTIONS = {"favorable", "unfavorable", "neutral", "mixed"}
VALID_INTENSITIES = {"strong", "moderate", "weak", "conditional"}
VALID_PHASES = {"1B_matrix", "1B_conditional", "1B_compound"}
VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth", "career_status",
    "marriage", "progeny", "spirituality", "intelligence_education",
    "character_temperament", "physical_appearance", "foreign_travel",
    "enemies_litigation", "property_vehicles", "fame_reputation",
}


# ── Basic counts ──────────────────────────────────────────────────────────────

def test_total_rule_count():
    assert len(RULES) >= 15, f"Ch.12 has 15 slokas, got {len(RULES)} rules"


def test_no_duplicate_rule_ids():
    ids = [r.rule_id for r in RULES]
    assert len(ids) == len(set(ids))


# ── Legacy contract (backward compat) ─────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_rule_id_format(rule):
    assert rule.rule_id.startswith("BPHS")
    assert len(rule.rule_id) == 8


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_source_is_bphs(rule):
    assert rule.source == "BPHS"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_school_parashari(rule):
    assert rule.school == "parashari"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_verse_ref_format(rule):
    assert rule.verse_ref
    assert "Ch.12" in rule.verse_ref
    assert "v." in rule.verse_ref


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_domains_from_taxonomy(rule):
    assert len(rule.outcome_domains) >= 1
    for domain in rule.outcome_domains:
        assert domain in VALID_DOMAINS, f"{rule.rule_id}: invalid '{domain}'"


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_outcome_direction(rule):
    assert rule.outcome_direction in VALID_DIRECTIONS


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_description_non_empty(rule):
    assert len(rule.description) >= 50


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_confidence_in_range(rule):
    assert 0.60 <= rule.confidence <= 1.0


# ── V2 PREDICTIONS (Protocol A: one-claim-one-rule) ──────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_non_empty(rule):
    """Every V2 rule must have at least 1 atomic prediction."""
    assert len(rule.predictions) >= 1, (
        f"{rule.rule_id}: predictions is empty — Protocol A requires at least 1"
    )


@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_predictions_structure(rule):
    """Each prediction must have entity, claim, domain, direction."""
    for i, pred in enumerate(rule.predictions):
        assert isinstance(pred, dict), f"{rule.rule_id}: predictions[{i}] not a dict"
        for key in ("entity", "claim", "domain", "direction"):
            assert key in pred, (
                f"{rule.rule_id}: predictions[{i}] missing '{key}'"
            )
        assert pred["entity"] in VALID_ENTITY_TARGETS, (
            f"{rule.rule_id}: predictions[{i}].entity='{pred['entity']}' invalid"
        )


def test_no_over_stuffed_predictions():
    """No rule should have >3 predictions (potential summarization)."""
    for r in RULES:
        assert len(r.predictions) <= 3, (
            f"{r.rule_id}: {len(r.predictions)} predictions — likely summarization, "
            f"split into separate rules (Protocol A)"
        )


# ── V2 ENTITY TARGET (Protocol C) ────────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_entity_target_valid(rule):
    assert rule.entity_target in VALID_ENTITY_TARGETS, (
        f"{rule.rule_id}: entity_target='{rule.entity_target}' not valid"
    )


# ── V2 SIGNAL GROUP (Gap 4) ──────────────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_signal_group_non_empty(rule):
    assert rule.signal_group, (
        f"{rule.rule_id}: signal_group is empty — must group rules from same signal"
    )


# ── V2 TIMING (Protocol F) ───────────────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_timing_window_checked(rule):
    """timing_window must NOT be bare {} (unchecked). Must have 'type' key."""
    tw = rule.timing_window
    assert tw, (
        f"{rule.rule_id}: timing_window is {{}} (unchecked) — set "
        f"{{\"type\": \"unspecified\"}} if text states no timing (Protocol F)"
    )
    assert "type" in tw, f"{rule.rule_id}: timing_window missing 'type' key"
    assert tw["type"] in VALID_TIMING_TYPES, (
        f"{rule.rule_id}: timing_window type='{tw['type']}' invalid"
    )


# ── V2 COMPUTABLE CONDITIONS (Protocol E) ────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_primary_condition_has_planet(rule):
    """Every rule must have 'planet' in primary_condition (backward compat)."""
    assert "planet" in rule.primary_condition, (
        f"{rule.rule_id}: missing 'planet' in primary_condition"
    )


# ── V2 COMMENTARY (Protocol D) ───────────────────────────────────────────────

def test_commentary_coverage():
    """At least 60% of rules should have commentary from Santhanam's notes."""
    with_commentary = [r for r in RULES if r.commentary_context]
    ratio = len(with_commentary) / len(RULES)
    assert ratio >= 0.60, (
        f"Commentary coverage {ratio:.0%} < 60% — read Santhanam's notes"
    )


# ── V2 CONCORDANCE ────────────────────────────────────────────────────────────

def test_concordance_coverage():
    """At least 50% of rules should have concordance texts."""
    with_conc = [r for r in RULES if r.concordance_texts]
    ratio = len(with_conc) / len(RULES)
    assert ratio >= 0.50, f"Concordance coverage {ratio:.0%} < 50%"


# ── V2 RULE RELATIONSHIPS (Protocol B: contrary mirrors) ─────────────────────

def test_contrary_mirrors_exist():
    """Ch.12 has explicit contrary-situation verses — mirrors must exist."""
    mirrors = [r for r in RULES if r.rule_relationship.get("type") == "contrary_mirror"]
    assert len(mirrors) >= 1, "No contrary mirrors found — Protocol B"


def test_rule_relationships_valid():
    """All rule_relationship entries must have valid type."""
    for r in RULES:
        rr = r.rule_relationship
        if rr:
            assert "type" in rr, f"{r.rule_id}: rule_relationship missing 'type'"
            assert rr["type"] in VALID_RELATIONSHIP_TYPES, (
                f"{r.rule_id}: relationship type '{rr['type']}' invalid"
            )


# ── V2 AUDIT GATE ─────────────────────────────────────────────────────────────

def test_v2_audit_zero_errors():
    """All Ch.12 V2 rules must pass the corpus_audit V2 compliance check."""
    audit = CorpusAudit(BPHS_V2_CH12_REGISTRY)
    report = audit.run()
    assert report["v2_errors"] == [], (
        f"V2 audit errors: {report['v2_errors'][:5]}"
    )


# ── V2 LAST MODIFIED ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("rule", RULES, ids=lambda r: r.rule_id)
def test_last_modified_session(rule):
    assert rule.last_modified_session == "S311"
