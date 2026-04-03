"""tests/test_s231_bphs_graha_rashis_p3.py — S231: BPHS graha in rashis part 3."""
from __future__ import annotations


def test_bphs_graha_rashis_p3_count():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    assert BPHS_GRAHA_RASHIS_P3_REGISTRY.count() == 24


def test_jupiter_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P3_REGISTRY.all()}
    for i in range(1, 13):
        assert f"JUR{i:03d}" in ids, f"JUR{i:03d} missing"


def test_venus_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P3_REGISTRY.all()}
    for i in range(1, 13):
        assert f"VER{i:03d}" in ids, f"VER{i:03d} missing"


def test_jupiter_exaltation_cancer():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("JUR004")
    assert rule is not None
    assert "exaltation" in rule.keyword_tags
    assert "cancer" in rule.keyword_tags


def test_jupiter_own_sign_sagittarius():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("JUR009")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags
    assert "moolatrikona" in rule.keyword_tags


def test_jupiter_debilitation_capricorn():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("JUR010")
    assert rule is not None
    assert "debilitation" in rule.keyword_tags
    assert "neecha" in rule.keyword_tags


def test_jupiter_own_sign_pisces():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("JUR012")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags


def test_venus_own_sign_taurus():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("VER002")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags
    assert "moolatrikona" in rule.keyword_tags


def test_venus_debilitation_virgo():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("VER006")
    assert rule is not None
    assert "debilitation" in rule.keyword_tags
    assert "neecha" in rule.keyword_tags


def test_venus_own_sign_libra():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("VER007")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags


def test_venus_exaltation_pisces():
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P3_REGISTRY.get("VER012")
    assert rule is not None
    assert "exaltation" in rule.keyword_tags
    assert "pisces" in rule.keyword_tags


def test_combined_corpus_includes_graha_rashis_p3():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 506  # 482 + 24
