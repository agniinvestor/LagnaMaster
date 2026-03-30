"""tests/test_s275_saravali_conjunctions_3.py — S275: Saravali Moon-Mars/Moon-Mercury/Moon-Jupiter."""
from __future__ import annotations


def test_sav3_count():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    assert SARAVALI_CONJUNCTIONS_3_REGISTRY.count() >= 130


def test_all_sav3_ids_sequential():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_3_REGISTRY.all()}
    for i in range(261, 261 + SARAVALI_CONJUNCTIONS_3_REGISTRY.count()):
        assert f"SAV{i:03d}" in ids, f"SAV{i:03d} missing"


def test_sav3_moon_mars():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_3_REGISTRY.all()
             if r.primary_condition.get("planet") == "moon_mars"]
    assert len(rules) >= 40


def test_sav3_moon_mercury():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_3_REGISTRY.all()
             if r.primary_condition.get("planet") == "moon_mercury"]
    assert len(rules) >= 40


def test_sav3_moon_jupiter():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_3_REGISTRY.all()
             if r.primary_condition.get("planet") == "moon_jupiter"]
    assert len(rules) >= 40


def test_sav3_phase_source():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_3_REGISTRY.all():
        assert rule.phase == "1B_compound"
        assert rule.source == "Saravali"
        assert rule.school == "parashari"


def test_sav3_primary_condition():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_3_REGISTRY.all():
        pc = rule.primary_condition
        assert pc and "planet" in pc and "placement_type" in pc


def test_sav3_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_CONJUNCTIONS_3_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_sav3_verse_ref():
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_3_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_sav3():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3817 + 130 + 130
