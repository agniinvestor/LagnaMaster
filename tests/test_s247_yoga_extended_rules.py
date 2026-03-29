"""tests/test_s247_yoga_extended_rules.py — S247: Extended yoga rules."""
from __future__ import annotations


def test_yoga_extended_count():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    assert YOGA_EXTENDED_RULES_REGISTRY.count() == 30


def test_all_yge_rules_present():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    ids = {r.rule_id for r in YOGA_EXTENDED_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"YGE{i:03d}" in ids, f"YGE{i:03d} missing"


def test_yoga_category():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    for rule in YOGA_EXTENDED_RULES_REGISTRY.all():
        assert rule.category == "yoga", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    for rule in YOGA_EXTENDED_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "varahamihira", "mantreswara"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_pancha_mahapurusha_5_yogas():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    pmp = [r for r in YOGA_EXTENDED_RULES_REGISTRY.all() if "pancha_mahapurusha" in r.tags]
    assert len(pmp) == 5


def test_ruchaka_yoga():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    rule = YOGA_EXTENDED_RULES_REGISTRY.get("YGE001")
    assert rule is not None
    assert "ruchaka_yoga" in rule.tags
    assert "mars_kendra" in rule.tags


def test_hamsa_yoga():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    rule = YOGA_EXTENDED_RULES_REGISTRY.get("YGE003")
    assert rule is not None
    assert "hamsa_yoga" in rule.tags
    assert "jupiter_kendra" in rule.tags


def test_viparita_raja_yoga():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    rule = YOGA_EXTENDED_RULES_REGISTRY.get("YGE013")
    assert rule is not None
    assert "viparita_raja_yoga" in rule.tags
    assert "6_8_12_lords" in rule.tags


def test_kartari_yoga():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    rule = YOGA_EXTENDED_RULES_REGISTRY.get("YGE030")
    assert rule is not None
    assert "kartari_yoga" in rule.tags
    assert "paapa_kartari" in rule.tags
    assert "shubha_kartari" in rule.tags


def test_nabhasa_yogas():
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY
    nabhasa = [r for r in YOGA_EXTENDED_RULES_REGISTRY.all() if "nabhasa" in r.tags]
    assert len(nabhasa) >= 6


def test_combined_corpus_includes_yge():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 986  # 956 + 30 = 986
