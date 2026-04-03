"""tests/test_s239_phala_deepika_ext.py — S239: Phala Deepika extended rules."""
from __future__ import annotations


def test_phala_deepika_ext_count():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    assert PHALA_DEEPIKA_EXT_REGISTRY.count() == 30


def test_all_pde_rules_present():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    ids = {r.rule_id for r in PHALA_DEEPIKA_EXT_REGISTRY.all()}
    for i in range(1, 31):
        assert f"PDE{i:03d}" in ids, f"PDE{i:03d} missing"


def test_mantreswara_school():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    for rule in PHALA_DEEPIKA_EXT_REGISTRY.all():
        assert rule.school == "mantreswara", f"{rule.rule_id} wrong school"
        assert "mantreswara" in rule.keyword_tags


def test_pancha_mahapurusha_details():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    rule = PHALA_DEEPIKA_EXT_REGISTRY.get("PDE013")
    assert rule is not None
    assert "ruchaka" in rule.keyword_tags
    assert "pancha_mahapurusha" in rule.keyword_tags


def test_gajakesari_refined():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    rule = PHALA_DEEPIKA_EXT_REGISTRY.get("PDE018")
    assert rule is not None
    assert "gajakesari" in rule.keyword_tags
    assert "refined_condition" in rule.keyword_tags


def test_health_rules_present():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    health_rules = [r for r in PHALA_DEEPIKA_EXT_REGISTRY.all() if r.category == "health"]
    assert len(health_rules) == 4


def test_yoga_cancellation_rule():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    rule = PHALA_DEEPIKA_EXT_REGISTRY.get("PDE027")
    assert rule is not None
    assert "yoga_cancellation" in rule.keyword_tags


def test_graha_yuddha_rule():
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY
    rule = PHALA_DEEPIKA_EXT_REGISTRY.get("PDE030")
    assert rule is not None
    assert "graha_yuddha" in rule.keyword_tags
    assert "planetary_war" in rule.keyword_tags


def test_combined_corpus_includes_pde():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 746  # 716 + 30
