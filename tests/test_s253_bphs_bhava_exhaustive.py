"""tests/test_s253_bphs_bhava_exhaustive.py — S253: BPHS Bhava Exhaustive (120 rules)."""
from __future__ import annotations


def test_bvx_count():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    assert BPHS_BHAVA_EXHAUSTIVE_REGISTRY.count() == 120


def test_all_bvx_rules_present():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 121):
        assert f"BVX{i:03d}" in ids, f"BVX{i:03d} missing"


def test_bvx_category():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all():
        assert rule.category == "bhava_signification", f"{rule.rule_id} wrong category"


def test_bvx_school_parashari():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} unexpected school"


def test_bvx_source_bphs():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "BPHS", f"{rule.rule_id} wrong source"


def test_all_12_houses_covered():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    ordinals = {
        1: "1st_house", 2: "2nd_house", 3: "3rd_house", 4: "4th_house",
        5: "5th_house", 6: "6th_house", 7: "7th_house", 8: "8th_house",
        9: "9th_house", 10: "10th_house", 11: "11th_house", 12: "12th_house",
    }
    for h, suffix in ordinals.items():
        house_rules = [r for r in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all() if suffix in r.keyword_tags]
        assert len(house_rules) >= 3, f"House {h} ({suffix}) has fewer than 3 rules"


def test_marana_karaka_rules():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    marana = [
        r for r in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all()
        if any("marana" in t for t in r.keyword_tags)
    ]
    assert len(marana) >= 4  # Saturn/Moon/Jupiter/Sun/Venus/Mars each have Marana placements


def test_maraka_rules():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    maraka = [r for r in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all() if "maraka" in r.keyword_tags]
    assert len(maraka) >= 2


def test_dig_bala_rule():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    rule = BPHS_BHAVA_EXHAUSTIVE_REGISTRY.get("BVX068")
    assert rule is not None
    assert "dig_bala" in rule.keyword_tags


def test_bhavat_bhavam():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    rule = BPHS_BHAVA_EXHAUSTIVE_REGISTRY.get("BVX061")
    assert rule is not None
    assert "bhavat_bhavam" in rule.keyword_tags


def test_body_anatomy_rule():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    rule = BPHS_BHAVA_EXHAUSTIVE_REGISTRY.get("BVX081")
    assert rule is not None
    assert "body_anatomy" in rule.keyword_tags


def test_longevity_classification():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    rule = BPHS_BHAVA_EXHAUSTIVE_REGISTRY.get("BVX066")
    assert rule is not None
    assert "alpayu" in rule.keyword_tags
    assert "purnayu" in rule.keyword_tags


def test_implemented_false():
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY
    for rule in BPHS_BHAVA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_combined_corpus_includes_bvx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1454  # 1334 + 120 = 1454
