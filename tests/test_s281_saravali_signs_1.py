"""tests/test_s281_saravali_signs_1.py — S281: Saravali Sun in 12 signs."""
from __future__ import annotations


def test_signs1_count():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    assert SARAVALI_SIGNS_1_REGISTRY.count() >= 130


def test_signs1_ids_sequential():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    ids = {r.rule_id for r in SARAVALI_SIGNS_1_REGISTRY.all()}
    for i in range(1041, 1041 + SARAVALI_SIGNS_1_REGISTRY.count()):
        assert f"SAV{i}" in ids, f"SAV{i} missing"


def test_signs1_phase_source():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    for rule in SARAVALI_SIGNS_1_REGISTRY.all():
        assert rule.phase == "1B_matrix"
        assert rule.source == "Saravali"
        assert rule.school == "parashari"


def test_signs1_sun_planet():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    for rule in SARAVALI_SIGNS_1_REGISTRY.all():
        assert rule.primary_condition.get("planet") == "sun"


def test_signs1_outcome_domains_valid():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_SIGNS_1_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_signs1_verse_ref():
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY
    for rule in SARAVALI_SIGNS_1_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_combined_includes_signs1():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 4727 + 130
