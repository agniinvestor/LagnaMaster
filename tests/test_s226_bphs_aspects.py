"""tests/test_s226_bphs_aspects.py — S226: BPHS aspect rules."""
from __future__ import annotations


def test_bphs_aspects_count():
    from src.corpus.bphs_aspects import BPHS_ASPECTS_REGISTRY
    assert BPHS_ASPECTS_REGISTRY.count() == 20


def test_special_aspects_present():
    from src.corpus.bphs_aspects import BPHS_ASPECTS_REGISTRY
    ids = {r.rule_id for r in BPHS_ASPECTS_REGISTRY.all()}
    assert {"ASP002", "ASP003", "ASP004"}.issubset(ids)


def test_jupiter_aspect_moon_rule():
    from src.corpus.bphs_aspects import BPHS_ASPECTS_REGISTRY
    rule = BPHS_ASPECTS_REGISTRY.get("ASP007")
    assert rule is not None
    assert "jupiter" in rule.keyword_tags and "moon" in rule.keyword_tags


def test_mangal_dosha_aspect_present():
    from src.corpus.bphs_aspects import BPHS_ASPECTS_REGISTRY
    rule = BPHS_ASPECTS_REGISTRY.get("ASP010")
    assert rule is not None
    assert "mangal_dosha" in rule.keyword_tags
