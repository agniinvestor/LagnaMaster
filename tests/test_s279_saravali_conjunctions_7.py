"""tests/test_s279_saravali_conjunctions_7.py — S279: Jupiter-Venus/Jupiter-Saturn/Venus-Saturn."""
from __future__ import annotations


def test_sav7_count():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    assert SARAVALI_CONJUNCTIONS_7_REGISTRY.count() >= 130


def test_all_sav7_ids_sequential():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_7_REGISTRY.all()}
    for i in range(781, 781 + SARAVALI_CONJUNCTIONS_7_REGISTRY.count()):
        assert f"SAV{i:03d}" in ids, f"SAV{i:03d} missing"


def test_sav7_phase_source():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_7_REGISTRY.all():
        assert rule.phase == "1B_compound"
        assert rule.source == "Saravali"


def test_sav7_primary_condition():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_7_REGISTRY.all():
        pc = rule.primary_condition
        assert pc and "planet" in pc and "placement_type" in pc


def test_sav7_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_CONJUNCTIONS_7_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_sav7_verse_ref():
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_7_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_sav7():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 4467 + 130
