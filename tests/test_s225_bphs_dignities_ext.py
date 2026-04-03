"""tests/test_s225_bphs_dignities_ext.py — S225: BPHS extended dignity rules."""
from __future__ import annotations


def test_bphs_dignities_ext_count():
    from src.corpus.bphs_dignities_ext import BPHS_DIGNITIES_EXT_REGISTRY
    assert BPHS_DIGNITIES_EXT_REGISTRY.count() == 20


def test_vargottama_present():
    from src.corpus.bphs_dignities_ext import BPHS_DIGNITIES_EXT_REGISTRY
    rule = BPHS_DIGNITIES_EXT_REGISTRY.get("DIG013")
    assert rule is not None
    assert "vargottama" in rule.keyword_tags


def test_digbala_present():
    from src.corpus.bphs_dignities_ext import BPHS_DIGNITIES_EXT_REGISTRY
    rule = BPHS_DIGNITIES_EXT_REGISTRY.get("DIG019")
    assert rule is not None
    assert "digbala" in rule.keyword_tags


def test_strength_hierarchy_in_own_sign_rule():
    from src.corpus.bphs_dignities_ext import BPHS_DIGNITIES_EXT_REGISTRY
    rule = BPHS_DIGNITIES_EXT_REGISTRY.get("DIG010")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags
