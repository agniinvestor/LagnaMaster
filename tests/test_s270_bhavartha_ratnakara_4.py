"""tests/test_s270_bhavartha_ratnakara_4.py — S270: Bhavartha Ratnakara Libra + Scorpio."""
from __future__ import annotations


def test_bvr4_count():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    assert BHAVARTHA_RATNAKARA_4_REGISTRY.count() >= 130


def test_all_bvr4_ids_sequential():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    ids = {r.rule_id for r in BHAVARTHA_RATNAKARA_4_REGISTRY.all()}
    n = BHAVARTHA_RATNAKARA_4_REGISTRY.count()
    start = 391
    for i in range(start, start + n):
        assert f"BVR{i:03d}" in ids, f"BVR{i:03d} missing"


def test_bvr4_libra_rules():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    libra = [r for r in BHAVARTHA_RATNAKARA_4_REGISTRY.all() if "libra" in r.lagna_scope]
    assert len(libra) >= 65, f"Libra has {len(libra)} rules, expected ≥65"


def test_bvr4_scorpio_rules():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    scorpio = [r for r in BHAVARTHA_RATNAKARA_4_REGISTRY.all() if "scorpio" in r.lagna_scope]
    assert len(scorpio) >= 65, f"Scorpio has {len(scorpio)} rules, expected ≥65"


def test_bvr4_all_lagna_scope_populated():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_bvr4_phase_conditional():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_bvr4_source_school():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert rule.source == "BhavarthaRatnakara", f"{rule.rule_id} wrong source"
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bvr4_primary_condition_populated():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        pc = rule.primary_condition
        assert pc, f"{rule.rule_id} empty primary_condition"
        assert "planet" in pc, f"{rule.rule_id} missing planet in primary_condition"
        assert "placement_type" in pc


def test_bvr4_outcome_direction_valid():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_bvr4_outcome_intensity_valid():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert rule.outcome_intensity in valid, f"{rule.rule_id} bad intensity"


def test_bvr4_verse_ref_set():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    for rule in BHAVARTHA_RATNAKARA_4_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} missing verse_ref"


def test_bvr4_all_7_planets_covered_libra():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    libra_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_4_REGISTRY.all()
        if "libra" in r.lagna_scope
    }
    for planet in planets:
        assert planet in libra_planets, f"Libra missing rules for {planet}"


def test_bvr4_all_7_planets_covered_scorpio():
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY
    planets = {"sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"}
    scorpio_planets = {
        r.primary_condition.get("planet")
        for r in BHAVARTHA_RATNAKARA_4_REGISTRY.all()
        if "scorpio" in r.lagna_scope
    }
    for planet in planets:
        assert planet in scorpio_planets, f"Scorpio missing rules for {planet}"


def test_combined_includes_bvr4():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 3297 + 130
