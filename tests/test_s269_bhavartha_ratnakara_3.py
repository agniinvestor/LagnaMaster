"""tests/test_s269_bhavartha_ratnakara_3.py — S269: Bhavartha Ratnakara Leo + Virgo."""
from __future__ import annotations


def test_bvr3_count():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    assert BHAVARTHA_RATNAKARA_3_REGISTRY.count() >= 130


def test_all_bvr3_ids_sequential():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_3_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_3_REGISTRY.count()
    start = 261
    for i in range(start, start + n):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr3_leo_rules():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    leo = [r for r in BHAVARTHA_RATNAKARA_3_REGISTRY.all() if "leo" in r.lagna_scope]
    assert len(leo) >= 65, f"Leo has {len(leo)} rules, expected ≥65"


def test_bvr3_virgo_rules():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    virgo = [r for r in BHAVARTHA_RATNAKARA_3_REGISTRY.all() if "virgo" in r.lagna_scope]
    assert len(virgo) >= 65, f"Virgo has {len(virgo)} rules, expected ≥65"


def test_bvr3_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr3_phase_conditional():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr3_source_school():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr3_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr3_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr3_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr3_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_3_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr3_all_7_planets_covered_leo():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    leo_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_3_REGISTRY.all()
        if "leo" in r.lagna_scope
    }
    for planet in planets:
        assert planet in leo_planets, f"Leo missing rules for {planet}"


def test_bvr3_all_7_planets_covered_virgo():
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    virgo_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_3_REGISTRY.all()
        if "virgo" in r.lagna_scope
    }
    for planet in planets:
        assert planet in virgo_planets, f"Virgo missing rules for {planet}"


def test_combined_includes_bvr3():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3167 + 130
