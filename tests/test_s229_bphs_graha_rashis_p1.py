"""tests/test_s229_bphs_graha_rashis_p1.py — S229: BPHS graha in rashis part 1."""
from __future__ import annotations


def test_bphs_graha_rashis_p1_count():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    assert BPHS_GRAHA_RASHIS_P1_REGISTRY.count() == 24


def test_sun_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P1_REGISTRY.all()}
    for i in range(1, 13):
        assert f"SUR{i:03d}" in ids, f"SUR{i:03d} missing"


def test_moon_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P1_REGISTRY.all()}
    for i in range(1, 13):
        assert f"MOR{i:03d}" in ids, f"MOR{i:03d} missing"


def test_sun_exaltation_aries():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("SUR001")
    assert rule is not None
    assert "aries" in rule.tags
    assert "exaltation_zone" in rule.tags


def test_sun_own_sign_leo():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("SUR005")
    assert rule is not None
    assert "own_sign" in rule.tags
    assert "leo" in rule.tags


def test_sun_debilitation_libra():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("SUR007")
    assert rule is not None
    assert "debilitation" in rule.tags
    assert "neecha" in rule.tags


def test_moon_exaltation_taurus():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("MOR002")
    assert rule is not None
    assert "exaltation" in rule.tags
    assert "taurus" in rule.tags


def test_moon_own_sign_cancer():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("MOR004")
    assert rule is not None
    assert "own_sign" in rule.tags
    assert "mother" in rule.tags


def test_moon_debilitation_scorpio():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P1_REGISTRY.get("MOR008")
    assert rule is not None
    assert "debilitation" in rule.tags
    assert "neecha" in rule.tags


def test_all_graha_in_rashi_category():
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY
    for rule in BPHS_GRAHA_RASHIS_P1_REGISTRY.all():
        assert rule.category == "graha_in_rashi", f"{rule.rule_id} has wrong category"


def test_combined_corpus_includes_graha_rashis_p1():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 458  # 434 + 24
