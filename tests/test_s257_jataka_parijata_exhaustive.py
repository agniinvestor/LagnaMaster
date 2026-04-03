"""tests/test_s257_jataka_parijata_exhaustive.py — S257: Jataka Parijata Exhaustive (150 rules)."""
from __future__ import annotations


def test_jpx_count():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    assert JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.count() == 150


def test_all_jpx_rules_present():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 151):
        assert f"JPX{i:03d}" in ids, f"JPX{i:03d} missing"


def test_school_parashari():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    for rule in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_source_jataka_parijata():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    for rule in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "JatakaParijata", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    for rule in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_jp_tag_on_all_rules():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    for rule in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all():
        assert "jp" in rule.keyword_tags, f"{rule.rule_id} missing 'jp' tag"


def test_all_12_rashis_covered():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rashis = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    for rashi in rashis:
        rules = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if rashi in r.keyword_tags]
        assert len(rules) >= 1, f"{rashi} not covered"


def test_all_9_planets_covered():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    for p in planets:
        rules = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if p in r.keyword_tags]
        assert len(rules) >= 2, f"{p} has fewer than 2 rules"


def test_raja_yoga_rules():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    raja = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if "raja_yoga" in r.keyword_tags]
    assert len(raja) >= 3


def test_mahapurusha_yoga():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX042")
    assert rule is not None
    assert "mahapurusha" in rule.keyword_tags


def test_viparita_raja_yoga():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX041")
    assert rule is not None
    assert "harsha" in rule.keyword_tags
    assert "sarala" in rule.keyword_tags
    assert "vimala" in rule.keyword_tags


def test_yoga_karaka():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX040")
    assert rule is not None
    assert "yoga_karaka" in rule.keyword_tags


def test_neecha_bhanga():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX022")
    assert rule is not None
    assert "neecha_bhanga" in rule.keyword_tags


def test_mangal_dosha():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX050")
    assert rule is not None
    assert "mangal_dosha" in rule.keyword_tags


def test_dig_bala():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX024")
    assert rule is not None
    assert "dig_bala" in rule.keyword_tags


def test_sade_sati():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX074")
    assert rule is not None
    assert "sade_sati" in rule.keyword_tags


def test_vargottama():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX025")
    assert rule is not None
    assert "vargottama" in rule.keyword_tags


def test_longevity_rules():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    longevity = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if "longevity" in r.keyword_tags]
    assert len(longevity) >= 3


def test_yoga_count():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    yogas = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if "yoga" in r.keyword_tags]
    assert len(yogas) >= 20


def test_varga_rules():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    varga = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if "varga" in r.keyword_tags]
    assert len(varga) >= 4


def test_medical_rules():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    medical = [r for r in JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.all() if "medical" in r.keyword_tags]
    assert len(medical) >= 4


def test_parijata_yoga():
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY
    rule = JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY.get("JPX093")
    assert rule is not None
    assert "parijata_yoga" in rule.keyword_tags


def test_combined_corpus_includes_jpx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1974  # 1824 + 150 = 1974
