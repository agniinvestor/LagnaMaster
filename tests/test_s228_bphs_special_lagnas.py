"""tests/test_s228_bphs_special_lagnas.py — S228: BPHS special lagna rules."""
from __future__ import annotations


def test_bphs_special_lagnas_count():
    from src.corpus.bphs_special_lagnas import BPHS_SPECIAL_LAGNAS_REGISTRY
    assert BPHS_SPECIAL_LAGNAS_REGISTRY.count() == 20


def test_chandra_lagna_present():
    from src.corpus.bphs_special_lagnas import BPHS_SPECIAL_LAGNAS_REGISTRY
    rule = BPHS_SPECIAL_LAGNAS_REGISTRY.get("SL001")
    assert rule is not None
    assert "chandra_lagna" in rule.keyword_tags


def test_arudha_lagna_present():
    from src.corpus.bphs_special_lagnas import BPHS_SPECIAL_LAGNAS_REGISTRY
    rule = BPHS_SPECIAL_LAGNAS_REGISTRY.get("SL003")
    assert rule is not None
    assert "arudha_lagna" in rule.keyword_tags


def test_upapada_lagna_present():
    from src.corpus.bphs_special_lagnas import BPHS_SPECIAL_LAGNAS_REGISTRY
    rule = BPHS_SPECIAL_LAGNAS_REGISTRY.get("SL007")
    assert rule is not None
    assert "upapada" in rule.keyword_tags


def test_combined_corpus_count_after_s228():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # 135 (phase 0) + 144 (lords) + 25+25+25+20+20+20+20 (yogas/etc) = 414
    assert registry.count() >= 400
