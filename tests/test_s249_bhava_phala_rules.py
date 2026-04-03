"""tests/test_s249_bhava_phala_rules.py — S249: Bhava Phala (house results) rules."""
from __future__ import annotations


def test_bhava_phala_count():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    assert BHAVA_PHALA_RULES_REGISTRY.count() == 30


def test_all_bph_rules_present():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    ids = {r.rule_id for r in BHAVA_PHALA_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"BPH{i:03d}" in ids, f"BPH{i:03d} missing"


def test_bhava_category():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    for rule in BHAVA_PHALA_RULES_REGISTRY.all():
        assert rule.category == "bhava", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    for rule in BHAVA_PHALA_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "kalidasa", "mantreswara"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_all_12_houses_covered():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    # Check at least 12 different house tags present
    all_tags = set()
    for rule in BHAVA_PHALA_RULES_REGISTRY.all():
        all_tags.update(rule.keyword_tags)
    for tag in ["1st_house", "2nd_house", "3rd_house", "4th_house", "5th_house",
                "6th_house", "7th_house", "8th_house", "9th_house", "10th_house",
                "11th_house", "12th_house"]:
        assert tag in all_tags, f"Missing house tag: {tag}"


def test_dusthana_houses():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    rule = BHAVA_PHALA_RULES_REGISTRY.get("BPH015")
    assert rule is not None
    assert "dusthana" in rule.keyword_tags
    assert "6_8_12" in rule.keyword_tags


def test_trikona_houses():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    rule = BHAVA_PHALA_RULES_REGISTRY.get("BPH016")
    assert rule is not None
    assert "trikona" in rule.keyword_tags
    assert "1_5_9" in rule.keyword_tags


def test_bhavat_bhavam():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    rule = BHAVA_PHALA_RULES_REGISTRY.get("BPH013")
    assert rule is not None
    assert "bhavat_bhavam" in rule.keyword_tags
    assert "5th_from_5th" in rule.keyword_tags


def test_maraka_principle():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    maraka_rules = [r for r in BHAVA_PHALA_RULES_REGISTRY.all() if "maraka" in r.keyword_tags]
    assert len(maraka_rules) >= 2


def test_health_body_parts():
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY
    rule = BHAVA_PHALA_RULES_REGISTRY.get("BPH030")
    assert rule is not None
    assert "12_houses_anatomy" in rule.keyword_tags
    assert "health_body_parts" in rule.keyword_tags


def test_combined_corpus_includes_bph():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1046  # 1016 + 30 = 1046
