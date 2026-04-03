"""tests/test_s259_jaimini_sutras_exhaustive.py — S259: Jaimini Sutras Exhaustive (150 rules)."""
from __future__ import annotations


def test_jmx_count():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    assert JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.count() == 150


def test_all_jmx_rules_present():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 151):
        assert f"JMX{i:03d}" in ids, f"JMX{i:03d} missing"


def test_school_jaimini():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    for rule in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "jaimini", f"{rule.rule_id} wrong school"


def test_source_jaimini_sutras():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    for rule in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "JaiminiSutras", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    for rule in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_jmx_tag_on_all_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    for rule in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all():
        assert "jmx" in rule.keyword_tags, f"{rule.rule_id} missing 'jmx' tag"


def test_jaimini_tag_on_all_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    for rule in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all():
        assert "jaimini" in rule.keyword_tags, f"{rule.rule_id} missing 'jaimini' tag"


def test_chara_karaka_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    ck = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "chara_karaka" in r.keyword_tags]
    assert len(ck) >= 5


def test_atmakaraka_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    ak = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "atmakaraka" in r.keyword_tags]
    assert len(ak) >= 10


def test_rashi_drishti_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rd = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "rashi_drishti" in r.keyword_tags]
    assert len(rd) >= 8


def test_arudha_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    arudha = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "arudha" in r.keyword_tags]
    assert len(arudha) >= 8


def test_upapada_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    ul = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "upapada" in r.keyword_tags]
    assert len(ul) >= 4


def test_karakamsha_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    km = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "karakamsha" in r.keyword_tags]
    assert len(km) >= 10


def test_chara_dasha_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    cd = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "chara_dasha" in r.keyword_tags]
    assert len(cd) >= 8


def test_raja_yoga_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    raja = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "raja_yoga" in r.keyword_tags]
    assert len(raja) >= 5


def test_moksha_rules():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    moksha = [r for r in JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.all() if "moksha" in r.keyword_tags]
    assert len(moksha) >= 3


def test_jmx001_atmakaraka():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX001")
    assert rule is not None
    assert "atmakaraka" in rule.keyword_tags


def test_jmx013_rashi_drishti():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX013")
    assert rule is not None
    assert "rashi_drishti" in rule.keyword_tags


def test_jmx021_arudha_lagna():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX021")
    assert rule is not None
    assert "arudha_lagna" in rule.keyword_tags


def test_jmx023_upapada():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX023")
    assert rule is not None
    assert "upapada" in rule.keyword_tags


def test_jmx036_chara_dasha():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX036")
    assert rule is not None
    assert "chara_dasha" in rule.keyword_tags


def test_jmx056_raja_yoga():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX056")
    assert rule is not None
    assert "raja_yoga" in rule.keyword_tags


def test_jmx087_ishta_devata():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX087")
    assert rule is not None
    assert "ishta_devata" in rule.keyword_tags


def test_jmx140_soul_philosophy():
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY
    rule = JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY.get("JMX140")
    assert rule is not None
    assert "soul" in rule.keyword_tags


def test_combined_corpus_includes_jmx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2274  # 2124 + 150 = 2274
