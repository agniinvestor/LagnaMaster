"""tests/test_s243_ashtakavarga_rules.py — S243: Ashtakavarga rules."""
from __future__ import annotations


def test_ashtakavarga_count():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    assert ASHTAKAVARGA_RULES_REGISTRY.count() == 30


def test_all_ast_rules_present():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    ids = {r.rule_id for r in ASHTAKAVARGA_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"AST{i:03d}" in ids, f"AST{i:03d} missing"


def test_ashtakavarga_category():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    for rule in ASHTAKAVARGA_RULES_REGISTRY.all():
        assert rule.category == "ashtakavarga", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    for rule in ASHTAKAVARGA_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "sarvartha", "varahamihira"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_fundamental_structure():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    rule = ASHTAKAVARGA_RULES_REGISTRY.get("AST001")
    assert rule is not None
    assert "fundamental" in rule.keyword_tags
    assert "sarvashtakavarga" in rule.keyword_tags
    assert "bindus" in rule.keyword_tags


def test_trikona_shodhana():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    rule = ASHTAKAVARGA_RULES_REGISTRY.get("AST004")
    assert rule is not None
    assert "trikona_shodhana" in rule.keyword_tags
    assert "reduction" in rule.keyword_tags


def test_ekadhipatya_shodhana():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    rule = ASHTAKAVARGA_RULES_REGISTRY.get("AST005")
    assert rule is not None
    assert "ekadhipatya_shodhana" in rule.keyword_tags
    assert "mercury_venus_saturn" in rule.keyword_tags


def test_saturn_bav_sade_sati():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    rule = ASHTAKAVARGA_RULES_REGISTRY.get("AST012")
    assert rule is not None
    assert "saturn_bav" in rule.keyword_tags
    assert "sade_sati" in rule.keyword_tags


def test_kakshya_timing():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    kakshya_rules = [r for r in ASHTAKAVARGA_RULES_REGISTRY.all() if "kakshya" in r.keyword_tags]
    assert len(kakshya_rules) == 2


def test_compatibility_rule():
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY
    rule = ASHTAKAVARGA_RULES_REGISTRY.get("AST030")
    assert rule is not None
    assert "compatibility" in rule.keyword_tags
    assert "synastry" in rule.keyword_tags


def test_combined_corpus_includes_ast():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 866  # 836 + 30 = 866
