"""tests/test_s223_bphs_raja_yoga.py — S223: BPHS raja yoga rules."""
from __future__ import annotations


def test_bphs_raja_yoga_count():
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY
    assert BPHS_RAJA_YOGA_REGISTRY.count() == 25


def test_core_raja_yoga_present():
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY
    rule = BPHS_RAJA_YOGA_REGISTRY.get("RY001")
    assert rule is not None
    assert "raja_yoga" in rule.tags


def test_yogakaraka_rule_present():
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY
    rule = BPHS_RAJA_YOGA_REGISTRY.get("RY003")
    assert rule is not None
    assert "yogakaraka" in rule.tags


def test_dharma_karma_adhipati_in_raja_yoga():
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY
    rule = BPHS_RAJA_YOGA_REGISTRY.get("RY011")
    assert rule is not None
    assert "dharma_karma_adhipati" in rule.tags


def test_saturn_yogakaraka_taurus_libra():
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY
    rule = BPHS_RAJA_YOGA_REGISTRY.get("RY017")
    assert rule is not None
    assert "taurus_lagna" in rule.tags or "libra_lagna" in rule.tags
