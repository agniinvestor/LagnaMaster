"""tests/test_s273_saravali_conjunctions_1.py — S273: Saravali Sun-Moon/Sun-Mars/Sun-Mercury."""
from __future__ import annotations


def test_sav1_count():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    assert SARAVALI_CONJUNCTIONS_1_REGISTRY.count() >= 130


def test_all_sav1_ids_sequential():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    ids = {r.rule_id for r in SARAVALI_CONJUNCTIONS_1_REGISTRY.all()}
    n = SARAVALI_CONJUNCTIONS_1_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"SAV{i:03d}" in ids, f"SAV{i:03d} missing"


def test_sav1_sun_moon_rules():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    sun_moon = [r for r in SARAVALI_CONJUNCTIONS_1_REGISTRY.all()
                if r.primary_condition.get("planet") == "sun_moon"]
    assert len(sun_moon) >= 40, f"Sun-Moon has {len(sun_moon)} rules, expected ≥40"


def test_sav1_sun_mars_rules():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    sun_mars = [r for r in SARAVALI_CONJUNCTIONS_1_REGISTRY.all()
                if r.primary_condition.get("planet") == "sun_mars"]
    assert len(sun_mars) >= 40, f"Sun-Mars has {len(sun_mars)} rules, expected ≥40"


def test_sav1_sun_mercury_rules():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    sun_merc = [r for r in SARAVALI_CONJUNCTIONS_1_REGISTRY.all()
                if r.primary_condition.get("planet") == "sun_mercury"]
    assert len(sun_merc) >= 40, f"Sun-Mercury has {len(sun_merc)} rules, expected ≥40"


def test_sav1_phase_compound():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.phase == "1B_compound", f"{rule.rule_id} wrong phase"


def test_sav1_source_school():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.source == "Saravali", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_sav1_primary_condition_has_planets():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet"
        assert "placement_type" in pc, f"{rule.rule_id} missing placement_type"


def test_sav1_outcome_direction_valid():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_sav1_outcome_intensity_valid():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_sav1_verse_ref_set():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_sav1_outcome_domains_valid():
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    valid_domains = {
        "longevity", "physical_health", "mental_health", "wealth",
        "career_status", "marriage", "progeny", "spirituality",
        "intelligence_education", "character_temperament",
        "physical_appearance", "foreign_travel", "enemies_litigation",
        "property_vehicles", "fame_reputation",
    }
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.outcome_domains, f"{rule.rule_id} empty outcome_domains"
        for d in rule.outcome_domains:
            assert d in valid_domains, f"{rule.rule_id} invalid domain '{d}'"


def test_sav1_lagna_scope_empty():
    """Conjunction rules are universal — not lagna-specific."""
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY
    for rule in SARAVALI_CONJUNCTIONS_1_REGISTRY.all():
        assert rule.lagna_scope == [], f"{rule.rule_id} should have empty lagna_scope"


def test_combined_includes_sav1():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3687 + 130
