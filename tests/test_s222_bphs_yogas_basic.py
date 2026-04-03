"""tests/test_s222_bphs_yogas_basic.py — S222: BPHS basic yogas (Pancha Mahapurusha, Gajakesari, etc.)."""
from __future__ import annotations


def test_bphs_yogas_basic_count():
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY
    assert BPHS_YOGAS_BASIC_REGISTRY.count() == 25


def test_pancha_mahapurusha_yogas_present():
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY
    mahapurusha_ids = {"YB001", "YB002", "YB003", "YB004", "YB005"}
    ids = {r.rule_id for r in BPHS_YOGAS_BASIC_REGISTRY.all()}
    assert mahapurusha_ids.issubset(ids)


def test_gajakesari_yoga_present():
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY
    rule = BPHS_YOGAS_BASIC_REGISTRY.get("YB006")
    assert rule is not None
    assert "gajakesari" in rule.description.lower()


def test_neecha_bhanga_present():
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY
    rule = BPHS_YOGAS_BASIC_REGISTRY.get("YB012")
    assert rule is not None
    assert "neecha_bhanga" in rule.keyword_tags


def test_viparita_yoga_present():
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY
    rule = BPHS_YOGAS_BASIC_REGISTRY.get("YB014")
    assert rule is not None
    assert "viparita_raja_yoga" in rule.keyword_tags
