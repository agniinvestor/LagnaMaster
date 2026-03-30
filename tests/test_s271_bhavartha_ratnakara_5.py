"""tests/test_s271_bhavartha_ratnakara_5.py — S271: Bhavartha Ratnakara Sagittarius + Capricorn."""
from __future__ import annotations


def test_bvr5_count():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    assert BHAVARTHA_RATNAKARA_5_REGISTRY.count() >= 130


def test_all_bvr5_ids_sequential():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_5_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_5_REGISTRY.count()
    start = 521
    for i in range(start, start + n):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr5_sagittarius_rules():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    sag = [r for r in BHAVARTHA_RATNAKARA_5_REGISTRY.all() if "sagittarius" in r.lagna_scope]
    assert len(sag) >= 65, f"Sagittarius has {len(sag)} rules, expected ≥65"


def test_bvr5_capricorn_rules():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    cap = [r for r in BHAVARTHA_RATNAKARA_5_REGISTRY.all() if "capricorn" in r.lagna_scope]
    assert len(cap) >= 65, f"Capricorn has {len(cap)} rules, expected ≥65"


def test_bvr5_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr5_phase_conditional():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr5_source_school():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr5_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr5_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr5_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr5_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_5_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr5_all_7_planets_covered_sagittarius():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    sag_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_5_REGISTRY.all()
        if "sagittarius" in r.lagna_scope
    }
    for planet in planets:
        assert planet in sag_planets, f"Sagittarius missing rules for {planet}"


def test_bvr5_all_7_planets_covered_capricorn():
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    cap_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_5_REGISTRY.all()
        if "capricorn" in r.lagna_scope
    }
    for planet in planets:
        assert planet in cap_planets, f"Capricorn missing rules for {planet}"


def test_combined_includes_bvr5():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3427 + 130
