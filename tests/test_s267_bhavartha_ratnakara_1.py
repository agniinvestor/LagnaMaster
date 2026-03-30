"""tests/test_s267_bhavartha_ratnakara_1.py — S267: Bhavartha Ratnakara Aries + Taurus."""
from __future__ import annotations


def test_bvr1_count():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    assert BHAVARTHA_RATNAKARA_1_REGISTRY.count() >= 130


def test_all_bvr1_ids_sequential():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_1_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_1_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr1_aries_rules():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    aries = [r for r in BHAVARTHA_RATNAKARA_1_REGISTRY.all() if "aries" in r.lagna_scope]
    assert len(aries) >= 65, f"Aries has {len(aries)} rules, expected ≥65"


def test_bvr1_taurus_rules():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    taurus = [r for r in BHAVARTHA_RATNAKARA_1_REGISTRY.all() if "taurus" in r.lagna_scope]
    assert len(taurus) >= 65, f"Taurus has {len(taurus)} rules, expected ≥65"


def test_bvr1_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr1_phase_conditional():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr1_source_school():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr1_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr1_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr1_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr1_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_1_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr1_all_7_planets_covered_aries():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    aries_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_1_REGISTRY.all()
        if "aries" in r.lagna_scope
    }
    for planet in planets:
        assert planet in aries_planets, f"Aries missing rules for {planet}"


def test_bvr1_all_7_planets_covered_taurus():
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    taurus_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_1_REGISTRY.all()
        if "taurus" in r.lagna_scope
    }
    for planet in planets:
        assert planet in taurus_planets, f"Taurus missing rules for {planet}"


def test_combined_includes_bvr1():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2907 + 130
