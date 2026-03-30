"""tests/test_s268_bhavartha_ratnakara_2.py — S268: Bhavartha Ratnakara Gemini + Cancer."""
from __future__ import annotations


def test_bvr2_count():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    assert BHAVARTHA_RATNAKARA_2_REGISTRY.count() >= 130


def test_all_bvr2_ids_sequential():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_2_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_2_REGISTRY.count()
    start = 131
    for i in range(start, start + n):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr2_gemini_rules():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    gemini = [r for r in BHAVARTHA_RATNAKARA_2_REGISTRY.all() if "gemini" in r.lagna_scope]
    assert len(gemini) >= 65, f"Gemini has {len(gemini)} rules, expected ≥65"


def test_bvr2_cancer_rules():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    cancer = [r for r in BHAVARTHA_RATNAKARA_2_REGISTRY.all() if "cancer" in r.lagna_scope]
    assert len(cancer) >= 65, f"Cancer has {len(cancer)} rules, expected ≥65"


def test_bvr2_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr2_phase_conditional():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr2_source_school():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr2_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr2_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr2_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr2_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_2_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr2_all_7_planets_covered_gemini():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    gemini_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_2_REGISTRY.all()
        if "gemini" in r.lagna_scope
    }
    for planet in planets:
        assert planet in gemini_planets, f"Gemini missing rules for {planet}"


def test_bvr2_all_7_planets_covered_cancer():
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    cancer_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_2_REGISTRY.all()
        if "cancer" in r.lagna_scope
    }
    for planet in planets:
        assert planet in cancer_planets, f"Cancer missing rules for {planet}"


def test_combined_includes_bvr2():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3037 + 130
