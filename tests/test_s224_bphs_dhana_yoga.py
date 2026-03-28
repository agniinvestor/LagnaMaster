"""tests/test_s224_bphs_dhana_yoga.py — S224: BPHS wealth yoga rules."""
from __future__ import annotations


def test_bphs_dhana_yoga_count():
    from src.corpus.bphs_dhana_yoga import BPHS_DHANA_YOGA_REGISTRY
    assert BPHS_DHANA_YOGA_REGISTRY.count() == 25


def test_primary_dhana_yoga_present():
    from src.corpus.bphs_dhana_yoga import BPHS_DHANA_YOGA_REGISTRY
    rule = BPHS_DHANA_YOGA_REGISTRY.get("DY001")
    assert rule is not None
    assert "dhana_yoga" in rule.tags


def test_daridra_yoga_present():
    from src.corpus.bphs_dhana_yoga import BPHS_DHANA_YOGA_REGISTRY
    rule = BPHS_DHANA_YOGA_REGISTRY.get("DY017")
    assert rule is not None
    assert "poverty" in rule.tags or "daridra" in rule.tags


def test_parivartana_dhana_present():
    from src.corpus.bphs_dhana_yoga import BPHS_DHANA_YOGA_REGISTRY
    rule = BPHS_DHANA_YOGA_REGISTRY.get("DY013")
    assert rule is not None
    assert "parivartana" in rule.tags
