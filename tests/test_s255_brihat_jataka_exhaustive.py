"""tests/test_s255_brihat_jataka_exhaustive.py — S255: Brihat Jataka Exhaustive (120 rules)."""
from __future__ import annotations


def test_bjx_count():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    assert BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.count() == 120


def test_all_bjx_rules_present():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 121):
        assert f"BJX{i:03d}" in ids, f"BJX{i:03d} missing"


def test_school_varahamihira():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    for rule in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "varahamihira", f"{rule.rule_id} wrong school"


def test_source_brihat_jataka():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    for rule in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "Brihat Jataka", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    for rule in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_all_12_rashis_covered():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rashis = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    for rashi in rashis:
        rules = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all() if rashi in r.tags]
        assert len(rules) >= 1, f"{rashi} not covered"


def test_bj_tag_on_all_rules():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    for rule in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all():
        assert "bj" in rule.tags, f"{rule.rule_id} missing 'bj' tag"


def test_aspect_rules():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rule = BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.get("BJX005")
    assert rule is not None
    assert "saturn_3_10" in rule.tags
    assert "jupiter_5_9" in rule.tags
    assert "mars_4_8" in rule.tags


def test_mahapurusha_yoga():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rule = BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.get("BJX036")
    assert rule is not None
    assert "mahapurusha" in rule.tags


def test_navamsha_rule():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rule = BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.get("BJX031")
    assert rule is not None
    assert "navamsha_d9" in rule.tags or "navamsha" in rule.tags or "d9" in rule.tags


def test_jupiter_transit_rule():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rule = BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.get("BJX077")
    assert rule is not None
    assert "transit" in rule.tags


def test_sade_sati_rule():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    rule = BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.get("BJX078")
    assert rule is not None
    assert "sade_sati" in rule.tags or "saturn_transit" in rule.tags


def test_avastha_rules():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    avastha = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all()
               if any("avastha" in t for t in r.tags)]
    assert len(avastha) >= 1


def test_longevity_rules():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    longevity = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all() if "longevity" in r.tags]
    assert len(longevity) >= 3


def test_nakshatra_rules():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    nakshatra = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all() if "nakshatra" in r.tags]
    assert len(nakshatra) >= 5


def test_yoga_rules_covered():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    yogas = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all() if "yoga" in r.tags]
    assert len(yogas) >= 5


def test_dasha_rules_covered():
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY
    dasha = [r for r in BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY.all() if "dasha" in r.tags]
    assert len(dasha) >= 3


def test_combined_corpus_includes_bjx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1674  # 1554 + 120 = 1674
