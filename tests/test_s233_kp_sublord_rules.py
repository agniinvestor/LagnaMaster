"""tests/test_s233_kp_sublord_rules.py — S233: KP Sublord Rules."""
from __future__ import annotations


def test_kp_sublord_rules_count():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    assert KP_SUBLORD_RULES_REGISTRY.count() == 30


def test_all_kp_rules_present():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    ids = {r.rule_id for r in KP_SUBLORD_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"KPS{i:03d}" in ids, f"KPS{i:03d} missing"


def test_fundamental_structure_rules():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS001")
    assert rule is not None
    assert "vimshottari_proportion" in rule.tags
    assert rule.school == "kp"


def test_sublord_decisive_rule():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS002")
    assert rule is not None
    assert "sublord_decisive" in rule.tags
    assert "hierarchy" in rule.tags


def test_marriage_rule():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS007")
    assert rule is not None
    assert "kp_marriage" in rule.tags
    assert "7th_house" in rule.tags


def test_career_rule():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS015")
    assert rule is not None
    assert "kp_career" in rule.tags
    assert "10th_cusp" in rule.tags


def test_disease_rule():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS019")
    assert rule is not None
    assert "kp_disease" in rule.tags
    assert "6_8_12_triangle" in rule.tags


def test_horary_rule():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    rule = KP_SUBLORD_RULES_REGISTRY.get("KPS027")
    assert rule is not None
    assert "kp_horary" in rule.tags
    assert "prashna" in rule.tags


def test_all_kp_category():
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY
    for rule in KP_SUBLORD_RULES_REGISTRY.all():
        assert rule.category == "kp_sublord", f"{rule.rule_id} wrong category"
        assert rule.school == "kp", f"{rule.rule_id} wrong school"


def test_combined_corpus_includes_kp_sublord():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 572  # 542 + 30
