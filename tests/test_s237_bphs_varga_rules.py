"""tests/test_s237_bphs_varga_rules.py — S237: BPHS Varga chart rules."""
from __future__ import annotations


def test_bphs_varga_rules_count():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    assert BPHS_VARGA_RULES_REGISTRY.count() == 30


def test_all_var_rules_present():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    ids = {r.rule_id for r in BPHS_VARGA_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"VAR{i:03d}" in ids, f"VAR{i:03d} missing"


def test_navamsha_most_important():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    rule = BPHS_VARGA_RULES_REGISTRY.get("VAR001")
    assert rule is not None
    assert "most_important_varga" in rule.keyword_tags


def test_vargottama_rule():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    rule = BPHS_VARGA_RULES_REGISTRY.get("VAR002")
    assert rule is not None
    assert "vargottama" in rule.keyword_tags
    assert "peak_strength" in rule.keyword_tags


def test_dashamsha_career():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    rule = BPHS_VARGA_RULES_REGISTRY.get("VAR011")
    assert rule is not None
    assert "dashamsha" in rule.keyword_tags
    assert "career" in rule.keyword_tags


def test_karakamsha_rule():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    rule = BPHS_VARGA_RULES_REGISTRY.get("VAR009")
    assert rule is not None
    assert "karakamsha" in rule.keyword_tags
    assert "atmakaraka" in rule.keyword_tags


def test_d12_parents():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    rule = BPHS_VARGA_RULES_REGISTRY.get("VAR020")
    assert rule is not None
    assert "parents" in rule.keyword_tags
    assert "dwadashamsha" in rule.keyword_tags


def test_all_varga_category():
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY
    for rule in BPHS_VARGA_RULES_REGISTRY.all():
        assert rule.category == "varga", f"{rule.rule_id} wrong category"


def test_combined_corpus_includes_varga_rules():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 686  # 656 + 30
