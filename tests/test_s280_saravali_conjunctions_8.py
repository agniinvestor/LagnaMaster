"""tests/test_s280_saravali_conjunctions_8.py — S280: Three+ planet conjunctions."""
from __future__ import annotations


def test_sav8_count():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    assert SARAVALI_CONJUNCTIONS_8_REGISTRY.count() >= 130


def test_all_sav8_ids_sequential():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_8_REGISTRY.all()}
    for i in range(911, 911 + SARAVALI_CONJUNCTIONS_8_REGISTRY.count()):
        rid = f"SAV{i:03d}" if i < 1000 else f"SAV{i}"
        assert rid in ids, f"{rid} missing"


def test_sav8_phase_source():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_8_REGISTRY.all():
        assert rule.phase == "1B_compound"
        assert rule.source == "Saravali"


def test_sav8_has_multi_planet():
    """Should have three+ planet conjunction rules."""
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    multi = [r for r in SARAVALI_CONJUNCTIONS_8_REGISTRY.all()
             if r.primary_condition.get("placement_type") == "multi_conjunction"]
    assert len(multi) >= 80, f"Expected ≥80 multi-conjunction rules, got {len(multi)}"


def test_sav8_primary_condition():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_8_REGISTRY.all():
        pc = rule.primary_condition
        assert pc and "planet" in pc and "placement_type" in pc


def test_sav8_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_CONJUNCTIONS_8_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_sav8_verse_ref():
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_8_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_sav8():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 4467 + 130 + 130
