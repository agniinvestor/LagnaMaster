"""tests/test_s272_bhavartha_ratnakara_6.py — S272: Bhavartha Ratnakara Aquarius + Pisces."""
from __future__ import annotations


def test_bvr6_count():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    assert BHAVARTHA_RATNAKARA_6_REGISTRY.count() >= 130


def test_all_bvr6_ids_sequential():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_6_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_6_REGISTRY.count()
    start = 651
    for i in range(start, start + n):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr6_aquarius_rules():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    aqu = [r for r in BHAVARTHA_RATNAKARA_6_REGISTRY.all() if "aquarius" in r.lagna_scope]
    assert len(aqu) >= 65, f"Aquarius has {len(aqu)} rules, expected ≥65"


def test_bvr6_pisces_rules():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    pisces = [r for r in BHAVARTHA_RATNAKARA_6_REGISTRY.all() if "pisces" in r.lagna_scope]
    assert len(pisces) >= 65, f"Pisces has {len(pisces)} rules, expected ≥65"


def test_bvr6_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr6_phase_conditional():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr6_source_school():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr6_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr6_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr6_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr6_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_6_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr6_all_7_planets_covered_aquarius():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    aqu_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_6_REGISTRY.all()
        if "aquarius" in r.lagna_scope
    }
    for planet in planets:
        assert planet in aqu_planets, f"Aquarius missing rules for {planet}"


def test_bvr6_all_7_planets_covered_pisces():
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    pis_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_6_REGISTRY.all()
        if "pisces" in r.lagna_scope
    }
    for planet in planets:
        assert planet in pis_planets, f"Pisces missing rules for {planet}"


def test_combined_includes_bvr6():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3427 + 130 + 130
