"""tests/test_s309_rule_record_v2.py — S309: RuleRecord v2 schema contract tests.

Validates the 10 new S309 fields (Corpus Standard Upgrade):
  predictions, entity_target, signal_group, commentary_context,
  cross_chapter_refs, timing_window, functional_modulation,
  derived_house_chains, convergence_signals, rule_relationship

Tests confirm:
  1. Backward compatibility (existing rules unaffected)
  2. Correct defaults (all empty/falsy)
  3. New fields accept proper values
  4. Total field count is 45
"""
from __future__ import annotations

from src.corpus.rule_record import RuleRecord


def _minimal_rule(**overrides) -> RuleRecord:
    """Create a minimal valid RuleRecord with optional overrides."""
    defaults = {
        "rule_id": "TEST001",
        "source": "TEST",
        "chapter": "Ch.1",
        "school": "parashari",
        "category": "test",
        "description": "Test rule for contract validation with enough length",
        "confidence": 0.65,
        "verse_ref": "Ch.1 v.1",
    }
    defaults.update(overrides)
    return RuleRecord(**defaults)


# ── Backward compatibility ────────────────────────────────────────────────────

def test_total_field_count():
    """RuleRecord field count — 53 (S311) + 3 maker-checker fields."""
    assert len(RuleRecord.__dataclass_fields__) == 56


def test_minimal_rule_creates_without_new_fields():
    """Existing Phase 1A constructor still works — no new required args."""
    r = _minimal_rule()
    assert r.rule_id == "TEST001"
    assert r.confidence == 0.65


def test_existing_phase1b_constructor_still_works():
    """Phase 1B constructor with all pre-S309 fields still works."""
    r = RuleRecord(
        rule_id="PH1B", source="BPHS", chapter="Ch.12", school="parashari",
        category="test", description="Phase 1B test", confidence=0.8,
        primary_condition={"planet": "jupiter", "placement_type": "house",
                           "placement_value": [7]},
        modifiers=[{"condition": "exalted", "effect": "amplifies", "strength": "strong"}],
        outcome_domains=["marriage"], outcome_direction="favorable",
        outcome_intensity="strong", verse_ref="Ch.12 v.1",
        phase="1B_matrix", system="natal",
    )
    assert r.outcome_direction == "favorable"
    # S309 fields all at defaults:
    assert r.predictions == []
    assert r.entity_target == "native"
    assert r.signal_group == ""


# ── Default values ────────────────────────────────────────────────────────────

def test_predictions_default_empty():
    assert _minimal_rule().predictions == []


def test_entity_target_default_native():
    assert _minimal_rule().entity_target == "native"


def test_signal_group_default_empty():
    assert _minimal_rule().signal_group == ""


def test_commentary_context_default_empty():
    assert _minimal_rule().commentary_context == ""


def test_cross_chapter_refs_default_empty():
    assert _minimal_rule().cross_chapter_refs == []


def test_timing_window_default_empty():
    assert _minimal_rule().timing_window == {}


def test_functional_modulation_default_empty():
    assert _minimal_rule().functional_modulation == {}


def test_derived_house_chains_default_empty():
    assert _minimal_rule().derived_house_chains == []


def test_convergence_signals_default_empty():
    assert _minimal_rule().convergence_signals == []


def test_rule_relationship_default_empty():
    assert _minimal_rule().rule_relationship == {}


# ── Field population ──────────────────────────────────────────────────────────

VALID_ENTITY_TARGETS = {"native", "father", "mother", "spouse", "children",
                        "siblings", "general"}

VALID_TIMING_TYPES = {"age", "age_range", "after_event", "dasha_period",
                      "unspecified"}

VALID_RELATIONSHIP_TYPES = {"alternative", "addition", "override",
                            "contrary_mirror"}


def test_predictions_populated():
    r = _minimal_rule(predictions=[
        {"entity": "native", "claim": "wealthy_through_career",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
        {"entity": "father", "claim": "father_prosperous",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ])
    assert len(r.predictions) == 2
    assert r.predictions[0]["entity"] == "native"
    assert r.predictions[1]["entity"] == "father"


def test_entity_target_valid_values():
    for entity in VALID_ENTITY_TARGETS:
        r = _minimal_rule(entity_target=entity)
        assert r.entity_target == entity


def test_signal_group_populated():
    r = _minimal_rule(signal_group="jupiter_h7_marriage")
    assert r.signal_group == "jupiter_h7_marriage"


def test_commentary_context_populated():
    r = _minimal_rule(
        commentary_context="Santhanam notes: the 10th house in astrology "
        "actually denotes one's profession, job, livelihood etc."
    )
    assert "Santhanam" in r.commentary_context


def test_cross_chapter_refs_populated():
    r = _minimal_rule(cross_chapter_refs=["Ch.44 Maraka", "Ch.83 Curses"])
    assert len(r.cross_chapter_refs) == 2


def test_timing_window_age():
    r = _minimal_rule(timing_window={
        "type": "age", "value": 32, "precision": "exact",
    })
    assert r.timing_window["type"] == "age"
    assert r.timing_window["value"] == 32


def test_timing_window_age_range():
    r = _minimal_rule(timing_window={
        "type": "age_range", "value": [16, 18], "precision": "approximate",
    })
    assert r.timing_window["type"] == "age_range"
    assert r.timing_window["value"] == [16, 18]


def test_timing_window_dasha():
    r = _minimal_rule(timing_window={
        "type": "dasha_period", "value": "jupiter",
        "precision": "approximate",
    })
    assert r.timing_window["type"] == "dasha_period"


def test_functional_modulation_populated():
    r = _minimal_rule(functional_modulation={
        "yogakaraka": "strongly_favorable_delayed_but_excellent",
        "malefic": "unfavorable_quarrelsome_health_issues",
        "neutral": "moderate_practical_partnership",
    })
    assert "yogakaraka" in r.functional_modulation


def test_derived_house_chains_populated():
    r = _minimal_rule(derived_house_chains=[{
        "base_house": 9, "derivative": "2nd_from",
        "effective_house": 10, "entity": "father", "domain": "wealth",
    }])
    assert r.derived_house_chains[0]["entity"] == "father"
    assert r.derived_house_chains[0]["base_house"] == 9


def test_convergence_signals_populated():
    r = _minimal_rule(convergence_signals=[
        "d9_7th_lord_in_jupiter_sign",
        "venus_aspecting_7th",
        "7th_house_ashtakavarga_above_28",
    ])
    assert len(r.convergence_signals) == 3


def test_rule_relationship_alternative():
    r = _minimal_rule(rule_relationship={
        "type": "alternative",
        "related_rules": ["BPHS0803", "BPHS0804"],
    })
    assert r.rule_relationship["type"] == "alternative"


def test_rule_relationship_contrary_mirror():
    r = _minimal_rule(rule_relationship={
        "type": "contrary_mirror",
        "related_rules": ["BPHS0800"],
    })
    assert r.rule_relationship["type"] == "contrary_mirror"


# ── to_dict includes new fields ───────────────────────────────────────────────

def test_to_dict_includes_s309_fields():
    r = _minimal_rule(entity_target="father", signal_group="h9_lord_fortune")
    d = r.to_dict()
    assert d["entity_target"] == "father"
    assert d["signal_group"] == "h9_lord_fortune"
    assert "predictions" in d
    assert "timing_window" in d
    assert "functional_modulation" in d
    assert "derived_house_chains" in d
    assert "convergence_signals" in d
    assert "rule_relationship" in d
    assert "commentary_context" in d
    assert "cross_chapter_refs" in d


# ── Corpus-wide check: existing rules unaffected ──────────────────────────────

def test_combined_corpus_loads_with_new_fields():
    """All 6,812 rules load without error with 10 new fields."""
    from src.corpus.combined_corpus import COMBINED_CORPUS
    rules = COMBINED_CORPUS.all()
    assert len(rules) >= 6000
    # Spot check: every rule has the new fields at defaults
    for rule in rules[:100]:
        assert isinstance(rule.predictions, list)
        assert rule.entity_target in VALID_ENTITY_TARGETS or rule.entity_target == "native"
        assert isinstance(rule.timing_window, dict)


# ── V2 Audit Enforcement Tests ────────────────────────────────────────────────

def test_audit_rejects_s310_rule_with_empty_predictions():
    """A rule from S310+ with empty predictions MUST fail audit."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S310",
        phase="1B_matrix",
        predictions=[],  # EMPTY — should fail
        signal_group="test_group",
        timing_window={"type": "unspecified"},
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert any("predictions is empty" in e for e in errors)


def test_audit_rejects_s310_rule_with_empty_signal_group():
    """A rule from S310+ with empty signal_group MUST fail audit."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S310",
        phase="1B_matrix",
        predictions=[{"entity": "native", "claim": "test_prediction_claim", "domain": "wealth",
                      "direction": "favorable"}],
        signal_group="",  # EMPTY — should fail
        timing_window={"type": "unspecified"},
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert any("signal_group is empty" in e for e in errors)


def test_audit_rejects_s310_rule_with_bare_empty_timing():
    """timing_window={} means unchecked — MUST fail. {"type":"unspecified"} is ok."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S310",
        phase="1B_matrix",
        predictions=[{"entity": "native", "claim": "test_prediction_claim", "domain": "wealth",
                      "direction": "favorable"}],
        signal_group="test_group",
        timing_window={},  # UNCHECKED — should fail
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert any("timing_window is empty dict" in e for e in errors)


def test_audit_accepts_s310_rule_with_unspecified_timing():
    """timing_window={"type":"unspecified"} means checked, no timing — should pass."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S310",
        phase="1B_matrix",
        predictions=[{"entity": "native", "claim": "test_prediction_claim", "domain": "wealth",
                      "direction": "favorable"}],
        signal_group="test_group",
        timing_window={"type": "unspecified"},
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert len(errors) == 0


def test_audit_skips_pre_s310_rules():
    """Rules from S308 and earlier are grandfathered — no V2 checks."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S308",
        phase="1B_matrix",
        predictions=[],  # empty but should pass (pre-S310)
        signal_group="",
        timing_window={},
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert len(errors) == 0


def test_audit_rejects_bad_prediction_structure():
    """Predictions list items must have required keys."""
    from src.corpus.corpus_audit import CorpusAudit
    r = _minimal_rule(
        last_modified_session="S310",
        phase="1B_matrix",
        predictions=[{"entity": "native"}],  # missing claim, domain, direction
        signal_group="test_group",
        timing_window={"type": "unspecified"},
    )
    errors = CorpusAudit(None).audit_v2_compliance(r)
    assert any("missing required key 'claim'" in e for e in errors)
    assert any("missing required key 'domain'" in e for e in errors)
    assert any("missing required key 'direction'" in e for e in errors)


def test_audit_full_corpus_no_v2_errors_for_existing():
    """All existing rules (pre-S310) should produce 0 V2 errors."""
    from src.corpus.combined_corpus import COMBINED_CORPUS
    from src.corpus.corpus_audit import CorpusAudit
    audit = CorpusAudit(COMBINED_CORPUS)
    report = audit.run()
    assert report["v2_errors"] == [], (
        f"Expected 0 V2 errors for pre-S310 rules, got {len(report['v2_errors'])}: "
        f"{report['v2_errors'][:5]}"
    )
