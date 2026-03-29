"""tests/test_s244_jaimini_sutras_rules.py — S244: Jaimini Sutras + Upagraha rules."""
from __future__ import annotations


def test_jaimini_count():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    assert JAIMINI_SUTRAS_RULES_REGISTRY.count() == 30


def test_all_jms_rules_present():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    ids = {r.rule_id for r in JAIMINI_SUTRAS_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"JMS{i:03d}" in ids, f"JMS{i:03d} missing"


def test_schools():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    for rule in JAIMINI_SUTRAS_RULES_REGISTRY.all():
        assert rule.school in {"jaimini", "parashari"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_chara_karaka_system():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS001")
    assert rule is not None
    assert "chara_karaka" in rule.tags
    assert "atmakaraka" in rule.tags
    assert "darakaraka" in rule.tags


def test_7_karakas_rule():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS002")
    assert rule is not None
    assert "7_karakas" in rule.tags
    assert "ak_amk_bk_mk_pk_gk_dk" in rule.tags


def test_rashi_drishti():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS009")
    assert rule is not None
    assert "rashi_drishti" in rule.tags
    assert "movable_fixed_dual" in rule.tags


def test_arudha_lagna():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS012")
    assert rule is not None
    assert "arudha_lagna" in rule.tags
    assert "perception" in rule.tags


def test_chara_dasha():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    dasha_rules = [r for r in JAIMINI_SUTRAS_RULES_REGISTRY.all() if "chara_dasha" in r.tags]
    assert len(dasha_rules) >= 3


def test_gulika_upagraha():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS027")
    assert rule is not None
    assert "gulika" in rule.tags
    assert rule.category == "upagraha"


def test_karakamsha():
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY
    rule = JAIMINI_SUTRAS_RULES_REGISTRY.get("JMS003")
    assert rule is not None
    assert "karakamsha" in rule.tags
    assert "soul_purpose" in rule.tags


def test_combined_corpus_includes_jms():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 896  # 866 + 30 = 896
