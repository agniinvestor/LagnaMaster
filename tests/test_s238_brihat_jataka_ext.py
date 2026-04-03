"""tests/test_s238_brihat_jataka_ext.py — S238: Brihat Jataka extended rules."""
from __future__ import annotations


def test_brihat_jataka_ext_count():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    assert BRIHAT_JATAKA_EXT_REGISTRY.count() == 30


def test_all_bje_rules_present():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    ids = {r.rule_id for r in BRIHAT_JATAKA_EXT_REGISTRY.all()}
    for i in range(1, 31):
        assert f"BJE{i:03d}" in ids, f"BJE{i:03d} missing"


def test_9_planets_have_nature_rules():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    ids = {r.rule_id for r in BRIHAT_JATAKA_EXT_REGISTRY.all()}
    for i in range(1, 10):
        assert f"BJE{i:03d}" in ids, f"BJE{i:03d} planetary nature missing"


def test_varahamihira_school():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    for rule in BRIHAT_JATAKA_EXT_REGISTRY.all():
        assert rule.school == "varahamihira", f"{rule.rule_id} wrong school"
        assert "varahamihira" in rule.keyword_tags


def test_benefic_malefic_classification():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    rule = BRIHAT_JATAKA_EXT_REGISTRY.get("BJE018")
    assert rule is not None
    assert "benefic_malefic" in rule.keyword_tags
    assert "waning_moon" in rule.keyword_tags


def test_special_aspects_rule():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    rule = BRIHAT_JATAKA_EXT_REGISTRY.get("BJE021")
    assert rule is not None
    assert "special_aspects" in rule.keyword_tags


def test_dasha_bhukti_rule():
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY
    rule = BRIHAT_JATAKA_EXT_REGISTRY.get("BJE029")
    assert rule is not None
    assert "antardasha" in rule.keyword_tags


def test_combined_corpus_includes_bje():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 716  # 686 + 30
