"""tests/test_s250_graha_phala_rules.py — S250: Graha Phala (planets in houses) rules."""
from __future__ import annotations


def test_graha_phala_count():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    assert GRAHA_PHALA_RULES_REGISTRY.count() == 30


def test_all_gph_rules_present():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    ids = {r.rule_id for r in GRAHA_PHALA_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"GPH{i:03d}" in ids, f"GPH{i:03d} missing"


def test_graha_phala_category():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    for rule in GRAHA_PHALA_RULES_REGISTRY.all():
        assert rule.category == "graha_phala", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    for rule in GRAHA_PHALA_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "mantreswara", "varahamihira"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_sun_house_rules():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    sun_rules = [r for r in GRAHA_PHALA_RULES_REGISTRY.all() if "sun_house" in r.keyword_tags]
    assert len(sun_rules) >= 4


def test_mangal_dosha():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    rule = GRAHA_PHALA_RULES_REGISTRY.get("GPH009")
    assert rule is not None
    assert "mangal_dosha" in rule.keyword_tags
    assert "1_4_7" in rule.keyword_tags


def test_saturn_upachaya():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    rule = GRAHA_PHALA_RULES_REGISTRY.get("GPH021")
    assert rule is not None
    assert "upachaya_3_6_11" in rule.keyword_tags
    assert "steady_gains" in rule.keyword_tags


def test_ketu_moksha():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    rule = GRAHA_PHALA_RULES_REGISTRY.get("GPH026")
    assert rule is not None
    assert "moksha_12th" in rule.keyword_tags


def test_combust_planets():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    rule = GRAHA_PHALA_RULES_REGISTRY.get("GPH027")
    assert rule is not None
    assert "combust" in rule.keyword_tags
    assert "asta" in rule.keyword_tags


def test_swakshetra():
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY
    rule = GRAHA_PHALA_RULES_REGISTRY.get("GPH030")
    assert rule is not None
    assert "swakshetra" in rule.keyword_tags
    assert "maximum_expression" in rule.keyword_tags


def test_combined_corpus_includes_gph():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1076  # 1046 + 30 = 1076
