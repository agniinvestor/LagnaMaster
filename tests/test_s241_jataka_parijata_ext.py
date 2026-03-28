"""tests/test_s241_jataka_parijata_ext.py — S241: Jataka Parijata extended rules."""
from __future__ import annotations


def test_jataka_parijata_ext_count():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    assert JATAKA_PARIJATA_EXT_REGISTRY.count() == 30


def test_all_jpe_rules_present():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    ids = {r.rule_id for r in JATAKA_PARIJATA_EXT_REGISTRY.all()}
    for i in range(1, 31):
        assert f"JPE{i:03d}" in ids, f"JPE{i:03d} missing"


def test_vaidyanatha_school():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    for rule in JATAKA_PARIJATA_EXT_REGISTRY.all():
        assert rule.school == "vaidyanatha", f"{rule.rule_id} wrong school"
        assert "vaidyanatha" in rule.tags


def test_parivartana_classifications():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    rule = JATAKA_PARIJATA_EXT_REGISTRY.get("JPE011")
    assert rule is not None
    assert "maha_parivartana" in rule.tags
    assert "dainya_parivartana" in rule.tags


def test_neecha_bhanga_rule():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    rule = JATAKA_PARIJATA_EXT_REGISTRY.get("JPE012")
    assert rule is not None
    assert "neecha_bhanga" in rule.tags
    assert "debilitation_cancelled" in rule.tags


def test_kemadruma_yoga():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    rule = JATAKA_PARIJATA_EXT_REGISTRY.get("JPE019")
    assert rule is not None
    assert "kemadruma" in rule.tags
    assert "moon_alone" in rule.tags


def test_all_9_mahadashas_present():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    dasha_rules = [r for r in JATAKA_PARIJATA_EXT_REGISTRY.all()
                   if r.category == "dasha"]
    assert len(dasha_rules) == 10  # JPE021-030


def test_venus_dasha_20_years():
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY
    rule = JATAKA_PARIJATA_EXT_REGISTRY.get("JPE030")
    assert rule is not None
    assert "20_years" in rule.tags
    assert "venus_dasha" in rule.tags


def test_combined_corpus_includes_jpe():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 806  # 776 + 30 = 806, crossing 800!
