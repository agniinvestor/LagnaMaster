"""tests/test_s276_saravali_conjunctions_4.py — S276: Moon-Venus/Moon-Saturn/Mars-Mercury."""
from __future__ import annotations


def test_sav4_count():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    assert SARAVALI_CONJUNCTIONS_4_REGISTRY.count() >= 130


def test_all_sav4_ids_sequential():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_4_REGISTRY.all()}
    for i in range(391, 391 + SARAVALI_CONJUNCTIONS_4_REGISTRY.count()):
        assert f"SAV{i:03d}" in ids, f"SAV{i:03d} missing"


def test_sav4_phase_source():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_4_REGISTRY.all():
        assert rule.phase == "1B_compound"
        assert rule.source == "Saravali"
        assert rule.school == "parashari"


def test_sav4_primary_condition():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_4_REGISTRY.all():
        pc = rule.primary_condition
        assert pc and "planet" in pc and "placement_type" in pc


def test_sav4_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_CONJUNCTIONS_4_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_sav4_verse_ref():
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_4_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_sav4():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 4077 + 130
