"""tests/test_s284_saravali_signs_4.py — S284: Saravali Mercury in 12 signs."""
from __future__ import annotations


def test_signs4_count():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    assert SARAVALI_SIGNS_4_REGISTRY.count() >= 130


def test_signs4_ids_sequential():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    ids = {r.rule_id for r in SARAVALI_SIGNS_4_REGISTRY.all()}
    for i in range(1431, 1431 + SARAVALI_SIGNS_4_REGISTRY.count()):
        assert f"SAV{i}" in ids, f"SAV{i} missing"


def test_signs4_phase_source():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    for rule in SARAVALI_SIGNS_4_REGISTRY.all():
        assert rule.phase == "1B_matrix"
        assert rule.source == "Saravali"


def test_signs4_mercury_planet():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    for rule in SARAVALI_SIGNS_4_REGISTRY.all():
        assert rule.primary_condition.get("planet") == "mercury"


def test_signs4_outcome_domains_valid():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    valid = {"longevity", "physical_health", "mental_health", "wealth",
             "career_status", "marriage", "progeny", "spirituality",
             "intelligence_education", "character_temperament",
             "physical_appearance", "foreign_travel", "enemies_litigation",
             "property_vehicles", "fame_reputation"}
    for rule in SARAVALI_SIGNS_4_REGISTRY.all():
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in valid, f"{rule.rule_id} invalid domain '{d}'"


def test_signs4_verse_ref():
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY
    for rule in SARAVALI_SIGNS_4_REGISTRY.all():
        assert rule.verse_ref


def test_combined_includes_signs4():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 4727 + 520
