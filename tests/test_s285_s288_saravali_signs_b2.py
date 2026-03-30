"""tests/test_s285_s288_saravali_signs_b2.py — S285-S288: Jupiter/Venus/Saturn/Rahu-Ketu in signs."""
from __future__ import annotations

VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth",
    "career_status", "marriage", "progeny", "spirituality",
    "intelligence_education", "character_temperament",
    "physical_appearance", "foreign_travel", "enemies_litigation",
    "property_vehicles", "fame_reputation",
}


def _check_registry(registry, min_count, planet_name, start_id):
    assert registry.count() >= min_count, f"Expected ≥{min_count}, got {registry.count()}"
    for rule in registry.all():
        assert rule.source == "Saravali"
        assert rule.school == "parashari"
        assert rule.phase == "1B_matrix"
        assert rule.primary_condition.get("planet") == planet_name, (
            f"{rule.rule_id}: expected planet={planet_name}, got {rule.primary_condition.get('planet')}"
        )
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"
        assert rule.outcome_domains, f"{rule.rule_id} empty outcome_domains"
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, f"{rule.rule_id} invalid domain '{d}'"
    ids = {r.rule_id for r in registry.all()}
    for i in range(start_id, start_id + registry.count()):
        assert f"SAV{i}" in ids, f"SAV{i} missing"


def test_signs5_jupiter():
    from src.corpus.saravali_signs_5 import SARAVALI_SIGNS_5_REGISTRY
    _check_registry(SARAVALI_SIGNS_5_REGISTRY, 130, "jupiter", 1561)


def test_signs6_venus():
    from src.corpus.saravali_signs_6 import SARAVALI_SIGNS_6_REGISTRY
    _check_registry(SARAVALI_SIGNS_6_REGISTRY, 130, "venus", 1703)


def test_signs7_saturn():
    from src.corpus.saravali_signs_7 import SARAVALI_SIGNS_7_REGISTRY
    _check_registry(SARAVALI_SIGNS_7_REGISTRY, 130, "saturn", 1862)


def test_signs8_rahu_ketu():
    from src.corpus.saravali_signs_8 import SARAVALI_SIGNS_8_REGISTRY
    assert SARAVALI_SIGNS_8_REGISTRY.count() >= 120
    rahu = [r for r in SARAVALI_SIGNS_8_REGISTRY.all()
            if r.primary_condition.get("planet") == "rahu"]
    ketu = [r for r in SARAVALI_SIGNS_8_REGISTRY.all()
            if r.primary_condition.get("planet") == "ketu"]
    assert len(rahu) >= 55, f"Rahu has {len(rahu)} rules"
    assert len(ketu) >= 55, f"Ketu has {len(ketu)} rules"
    for rule in SARAVALI_SIGNS_8_REGISTRY.all():
        assert rule.source == "Saravali"
        assert rule.phase == "1B_matrix"
        assert rule.verse_ref
        assert rule.outcome_domains
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, f"{rule.rule_id} invalid domain '{d}'"


def test_combined_includes_all_signs():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # 5247 (through S284) + 142 + 159 + 141 + 130 = 5819
    assert registry.count() >= 5247 + 142 + 159 + 141 + 130
