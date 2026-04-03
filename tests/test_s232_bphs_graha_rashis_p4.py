"""tests/test_s232_bphs_graha_rashis_p4.py — S232: BPHS graha in rashis part 4."""
from __future__ import annotations


def test_bphs_graha_rashis_p4_count():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    assert BPHS_GRAHA_RASHIS_P4_REGISTRY.count() == 36


def test_saturn_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P4_REGISTRY.all()}
    for i in range(1, 13):
        assert f"SAR{i:03d}" in ids, f"SAR{i:03d} missing"


def test_rahu_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P4_REGISTRY.all()}
    for i in range(1, 13):
        assert f"RHR{i:03d}" in ids, f"RHR{i:03d} missing"


def test_ketu_in_all_12_rashis():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_RASHIS_P4_REGISTRY.all()}
    for i in range(1, 13):
        assert f"KTR{i:03d}" in ids, f"KTR{i:03d} missing"


def test_saturn_debilitation_aries():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("SAR001")
    assert rule is not None
    assert "debilitation" in rule.keyword_tags
    assert "neecha" in rule.keyword_tags


def test_saturn_exaltation_libra():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("SAR007")
    assert rule is not None
    assert "exaltation" in rule.keyword_tags
    assert "libra" in rule.keyword_tags


def test_saturn_own_sign_capricorn():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("SAR010")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags
    assert "moolatrikona" in rule.keyword_tags


def test_saturn_own_sign_aquarius():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("SAR011")
    assert rule is not None
    assert "own_sign" in rule.keyword_tags


def test_ketu_moksha_scorpio():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("KTR008")
    assert rule is not None
    assert "moksha" in rule.keyword_tags


def test_ketu_pisces_enlightenment():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    rule = BPHS_GRAHA_RASHIS_P4_REGISTRY.get("KTR012")
    assert rule is not None
    assert "moksha" in rule.keyword_tags
    assert "liberation" in rule.keyword_tags


def test_all_graha_in_rashi_category():
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY
    for rule in BPHS_GRAHA_RASHIS_P4_REGISTRY.all():
        assert rule.category == "graha_in_rashi", f"{rule.rule_id} wrong category"


def test_combined_corpus_includes_graha_rashis_p4():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 542  # 506 + 36
