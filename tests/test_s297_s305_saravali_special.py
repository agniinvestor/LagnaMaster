"""tests/test_s297_s305_saravali_special.py — S297-S305: Block D Special Topics."""
from __future__ import annotations

VALID_DOMAINS = {
    "longevity", "physical_health", "mental_health", "wealth",
    "career_status", "marriage", "progeny", "spirituality",
    "intelligence_education", "character_temperament",
    "physical_appearance", "foreign_travel", "enemies_litigation",
    "property_vehicles", "fame_reputation",
}


def _check(registry, min_count):
    assert registry.count() >= min_count, f"Expected ≥{min_count}, got {registry.count()}"
    for rule in registry.all():
        assert rule.source == "Saravali"
        assert rule.school == "parashari"
        assert rule.phase == "1B_matrix"
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"
        assert rule.outcome_domains, f"{rule.rule_id} empty outcome_domains"
        for d in rule.outcome_domains:
            assert d in VALID_DOMAINS, f"{rule.rule_id} invalid domain '{d}'"


def test_d1_planet_natures():
    from src.corpus.saravali_special_1 import SARAVALI_SPECIAL_1_REGISTRY
    _check(SARAVALI_SPECIAL_1_REGISTRY, 40)


def test_d2_longevity():
    from src.corpus.saravali_special_2 import SARAVALI_SPECIAL_2_REGISTRY
    _check(SARAVALI_SPECIAL_2_REGISTRY, 25)


def test_d3_raja_yogas():
    from src.corpus.saravali_special_3 import SARAVALI_SPECIAL_3_REGISTRY
    _check(SARAVALI_SPECIAL_3_REGISTRY, 25)


def test_d4_nabhasa_yogas():
    from src.corpus.saravali_special_4 import SARAVALI_SPECIAL_4_REGISTRY
    _check(SARAVALI_SPECIAL_4_REGISTRY, 30)


def test_d5_bhava_effects():
    from src.corpus.saravali_special_5 import SARAVALI_SPECIAL_5_REGISTRY
    _check(SARAVALI_SPECIAL_5_REGISTRY, 25)


def test_d6_female_horoscopy():
    from src.corpus.saravali_special_6 import SARAVALI_SPECIAL_6_REGISTRY
    _check(SARAVALI_SPECIAL_6_REGISTRY, 25)


def test_d7_dasha_transit():
    from src.corpus.saravali_special_7 import SARAVALI_SPECIAL_7_REGISTRY
    _check(SARAVALI_SPECIAL_7_REGISTRY, 20)


def test_d8_death_drekkana():
    from src.corpus.saravali_special_8 import SARAVALI_SPECIAL_8_REGISTRY
    _check(SARAVALI_SPECIAL_8_REGISTRY, 15)


def test_d9_nimitta_summary():
    from src.corpus.saravali_special_9 import SARAVALI_SPECIAL_9_REGISTRY
    _check(SARAVALI_SPECIAL_9_REGISTRY, 20)


def test_combined_includes_block_d():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # 6315 (through S296) + 270 (Block D) = 6585
    assert registry.count() >= 6315 + 270
