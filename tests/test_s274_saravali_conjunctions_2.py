"""tests/test_s274_saravali_conjunctions_2.py — S274: Saravali Sun-Jupiter/Sun-Venus/Sun-Saturn."""
from __future__ import annotations


def test_sav2_count():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    assert SARAVALI_CONJUNCTIONS_2_REGISTRY.count() >= 130


def test_all_sav2_ids_sequential():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_2_REGISTRY.all()}
    for i in range(131, 131 + SARAVALI_CONJUNCTIONS_2_REGISTRY.count()):
        assert f"SAV{i:03d}" in ids, f"SAV{i:03d} missing"


def test_sav2_sun_jupiter():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_2_REGISTRY.all()
             if r.primary_condition.get("planet") == "sun_jupiter"]
    assert len(rules) >= 40


def test_sav2_sun_venus():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_2_REGISTRY.all()
             if r.primary_condition.get("planet") == "sun_venus"]
    assert len(rules) >= 40


def test_sav2_sun_saturn():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    rules = [r for r in SARAVALI_CONJUNCTIONS_2_REGISTRY.all()
             if r.primary_condition.get("planet") == "sun_saturn"]
    assert len(rules) >= 40


def test_sav2_phase_source():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_2_REGISTRY.all():
        assert rule.phase == "1B_compound"
        assert rule.source == "Saravali"
        assert rule.school == "parashari"


def test_sav2_primary_condition():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_2_REGISTRY.all():
        pc = rule.primary_condition
        assert pc and "planet" in pc and "placement_type" in pc


def test_sav2_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_CONJUNCTIONS_2_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_sav2_verse_ref():
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_2_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_sav2():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3817 + 130
