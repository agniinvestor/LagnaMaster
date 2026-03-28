"""tests/test_s240_uttara_kalamrita_ext.py — S240: Uttara Kalamrita extended rules."""
from __future__ import annotations


def test_uttara_kalamrita_ext_count():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    assert UTTARA_KALAMRITA_EXT_REGISTRY.count() == 30


def test_all_uke_rules_present():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    ids = {r.rule_id for r in UTTARA_KALAMRITA_EXT_REGISTRY.all()}
    for i in range(1, 31):
        assert f"UKE{i:03d}" in ids, f"UKE{i:03d} missing"


def test_kalidasa_school():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    for rule in UTTARA_KALAMRITA_EXT_REGISTRY.all():
        assert rule.school == "kalidasa", f"{rule.rule_id} wrong school"
        assert "kalidasa" in rule.tags


def test_12_house_significations():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    house_rules = [r for r in UTTARA_KALAMRITA_EXT_REGISTRY.all()
                   if r.rule_id in {f"UKE{i:03d}" for i in range(1, 13)}]
    assert len(house_rules) == 12


def test_9_planetary_significations():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    planet_rules = [r for r in UTTARA_KALAMRITA_EXT_REGISTRY.all()
                    if r.rule_id in {f"UKE{i:03d}" for i in range(13, 22)}]
    assert len(planet_rules) == 9


def test_bhavat_bhavam_rule():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    rule = UTTARA_KALAMRITA_EXT_REGISTRY.get("UKE023")
    assert rule is not None
    assert "bhavat_bhavam" in rule.tags


def test_kartari_rule():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    rule = UTTARA_KALAMRITA_EXT_REGISTRY.get("UKE025")
    assert rule is not None
    assert "kartari" in rule.tags
    assert "papa_kartari" in rule.tags


def test_temporal_malefic_benefic():
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY
    rule = UTTARA_KALAMRITA_EXT_REGISTRY.get("UKE028")
    assert rule is not None
    assert "temporal_malefic" in rule.tags
    assert "temporal_benefic" in rule.tags


def test_combined_corpus_includes_uke():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 776  # 746 + 30
