"""tests/test_s230_bphs_graha_rashis_p2.py — S230: BPHS graha in rashis part 2."""
from __future__ import annotations


def test_bphs_graha_rashis_p2_count():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    assert BPHS_GRAHA_RASHIS_P2_REGISTRY.count() == 24


def test_mars_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P2_REGISTRY.all()}
    for i in range(1, 13):
        assert f"MAR{i:03d}" in ids, f"MAR{i:03d} missing"


def test_mercury_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P2_REGISTRY.all()}
    for i in range(1, 13):
        assert f"BUR{i:03d}" in ids, f"BUR{i:03d} missing"


def test_mars_own_sign_aries():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("MAR001")
    assert rule is not None
    assert "own_sign" in rule.tags
    assert "moolatrikona" in rule.tags


def test_mars_debilitation_cancer():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("MAR004")
    assert rule is not None
    assert "debilitation" in rule.tags
    assert "neecha" in rule.tags


def test_mars_own_sign_scorpio():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("MAR008")
    assert rule is not None
    assert "own_sign" in rule.tags


def test_mars_exaltation_capricorn():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("MAR010")
    assert rule is not None
    assert "exaltation" in rule.tags


def test_mercury_own_sign_gemini():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("BUR003")
    assert rule is not None
    assert "own_sign" in rule.tags
    assert "moolatrikona" in rule.tags


def test_mercury_exaltation_virgo():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("BUR006")
    assert rule is not None
    assert "exaltation" in rule.tags
    assert "own_sign" in rule.tags


def test_mercury_debilitation_sagittarius():
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P2_REGISTRY.get("BUR009")
    assert rule is not None
    assert "debilitation" in rule.tags
    assert "neecha" in rule.tags


def test_combined_corpus_includes_graha_rashis_p2():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 482  # 458 + 24
