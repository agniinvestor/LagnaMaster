"""tests/test_s234_bphs_nakshatra_rules_p1.py — S234: BPHS nakshatra rules p1."""
from __future__ import annotations


def test_bphs_nakshatra_rules_p1_count():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    assert BPHS_NAKSHATRA_RULES_P1_REGISTRY.count() == 28


def test_all_14_nakshatras_present():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    ids = {r.rule_id for r in BPHS_NAKSHATRA_RULES_P1_REGISTRY.all()}
    for i in range(1, 15):
        assert f"NAK{i:03d}" in ids, f"NAK{i:03d} missing"


def test_all_14_moon_in_nakshatra_rules():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    ids = {r.rule_id for r in BPHS_NAKSHATRA_RULES_P1_REGISTRY.all()}
    for i in range(15, 29):
        assert f"NAK{i:03d}" in ids, f"NAK{i:03d} missing"


def test_rohini_most_favored():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK004")
    assert rule is not None
    assert "rohini" in rule.keyword_tags
    assert "moon_favorite" in rule.keyword_tags


def test_pushya_most_auspicious():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK008")
    assert rule is not None
    assert "most_auspicious" in rule.keyword_tags


def test_rohini_moon_most_favored():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK018")
    assert rule is not None
    assert "moon_favorite" in rule.keyword_tags


def test_pushya_moon_most_auspicious():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    rule = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK022")
    assert rule is not None
    assert "most_auspicious_moon" in rule.keyword_tags


def test_nakshatra_categories():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    for rule in BPHS_NAKSHATRA_RULES_P1_REGISTRY.all():
        assert rule.category == "nakshatra", f"{rule.rule_id} wrong category"


def test_nakshatra_rulers_present():
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY
    # Ashwini = Ketu, Bharani = Venus, Krittika = Sun
    nak1 = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK001")
    nak2 = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK002")
    nak3 = BPHS_NAKSHATRA_RULES_P1_REGISTRY.get("NAK003")
    assert "ketu" in nak1.keyword_tags
    assert "venus" in nak2.keyword_tags
    assert "sun" in nak3.keyword_tags


def test_combined_corpus_includes_nakshatra_p1():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 600  # 572 + 28
