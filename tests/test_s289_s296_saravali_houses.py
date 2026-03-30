"""tests/test_s289_s296_saravali_houses.py — S289-S296: All planets in 12 houses."""
from __future__ import annotations

VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth",
    "career_status", "marriage", "progeny", "spirituality",
    "intelligence_education", "character_temperament",
    "physical_appearance", "foreign_travel", "enemies_litigation",
    "property_vehicles", "fame_reputation",
}


def _check_registry(registry, planet_name, min_count):
    assert registry.count() >= min_count, f"Expected ≥{min_count}, got {registry.count()}"
    for rule in registry.all():
        assert rule.source == "Saravali"
        assert rule.school == "parashari"
        assert rule.phase == "1B_matrix"
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"
        assert rule.outcome_domains, f"{rule.rule_id} empty outcome_domains"
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, f"{rule.rule_id} invalid domain '{d}'"


def test_houses1_sun():
    from src.corpus.saravali_houses_1 import SARAVALI_HOUSES_1_REGISTRY
    _check_registry(SARAVALI_HOUSES_1_REGISTRY, "sun", 50)


def test_houses2_moon():
    from src.corpus.saravali_houses_2 import SARAVALI_HOUSES_2_REGISTRY
    _check_registry(SARAVALI_HOUSES_2_REGISTRY, "moon", 50)


def test_houses3_mars():
    from src.corpus.saravali_houses_3 import SARAVALI_HOUSES_3_REGISTRY
    _check_registry(SARAVALI_HOUSES_3_REGISTRY, "mars", 50)


def test_houses4_mercury():
    from src.corpus.saravali_houses_4 import SARAVALI_HOUSES_4_REGISTRY
    _check_registry(SARAVALI_HOUSES_4_REGISTRY, "mercury", 50)


def test_houses5_jupiter():
    from src.corpus.saravali_houses_5 import SARAVALI_HOUSES_5_REGISTRY
    _check_registry(SARAVALI_HOUSES_5_REGISTRY, "jupiter", 50)


def test_houses6_venus():
    from src.corpus.saravali_houses_6 import SARAVALI_HOUSES_6_REGISTRY
    _check_registry(SARAVALI_HOUSES_6_REGISTRY, "venus", 50)


def test_houses7_saturn():
    from src.corpus.saravali_houses_7 import SARAVALI_HOUSES_7_REGISTRY
    _check_registry(SARAVALI_HOUSES_7_REGISTRY, "saturn", 50)


def test_houses8_rahu_ketu():
    from src.corpus.saravali_houses_8 import SARAVALI_HOUSES_8_REGISTRY
    assert SARAVALI_HOUSES_8_REGISTRY.count() >= 70
    rahu = [r for r in SARAVALI_HOUSES_8_REGISTRY.all()
            if r.primary_condition.get("planet") == "rahu"]
    ketu = [r for r in SARAVALI_HOUSES_8_REGISTRY.all()
            if r.primary_condition.get("planet") == "ketu"]
    assert len(rahu) >= 30
    assert len(ketu) >= 30
    for rule in SARAVALI_HOUSES_8_REGISTRY.all():
        assert rule.source == "Saravali"
        assert rule.phase == "1B_matrix"
        assert rule.verse_ref
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, f"{rule.rule_id} invalid domain '{d}'"


def test_combined_includes_all_houses():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # 5819 (through S288) + 68+60+57+57+60+56+57+81 = 5819 + 496
    assert registry.count() >= 5819 + 496
