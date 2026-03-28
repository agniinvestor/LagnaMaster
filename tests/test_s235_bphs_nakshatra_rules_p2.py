"""tests/test_s235_bphs_nakshatra_rules_p2.py — S235: BPHS nakshatra rules p2."""
from __future__ import annotations


def test_bphs_nakshatra_rules_p2_count():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    assert BPHS_NAKSHATRA_RULES_P2_REGISTRY.count() == 26


def test_all_13_nakshatras_15_to_27():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    ids = {r.rule_id for r in BPHS_NAKSHATRA_RULES_P2_REGISTRY.all()}
    for i in range(29, 42):
        assert f"NAK{i:03d}" in ids, f"NAK{i:03d} missing"


def test_all_13_moon_in_nakshatra_rules_p2():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    ids = {r.rule_id for r in BPHS_NAKSHATRA_RULES_P2_REGISTRY.all()}
    for i in range(42, 55):
        assert f"NAK{i:03d}" in ids, f"NAK{i:03d} missing"


def test_revati_last_nakshatra():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P2_REGISTRY.get("NAK041")
    assert rule is not None
    assert "last_nakshatra" in rule.tags
    assert "revati" in rule.tags


def test_pushya_nakshatra_lord():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    # NAK029 = Swati, Rahu-ruled
    rule = BPHS_NAKSHATRA_RULES_P2_REGISTRY.get("NAK029")
    assert rule is not None
    assert "rahu" in rule.tags


def test_mula_liberation_tags():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P2_REGISTRY.get("NAK033")
    assert rule is not None
    assert "liberation" in rule.tags
    assert "ketu" in rule.tags


def test_all_nakshatra_categories():
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY
    for rule in BPHS_NAKSHATRA_RULES_P2_REGISTRY.all():
        assert rule.category == "nakshatra", f"{rule.rule_id} wrong category"


def test_combined_corpus_includes_nakshatra_p2():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 626  # 600 + 26
