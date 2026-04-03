"""tests/test_s258_sarvartha_chintamani_exhaustive.py — S258: Sarvartha Chintamani Exhaustive (150 rules)."""
from __future__ import annotations


def test_scx_count():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    assert SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.count() == 150


def test_all_scx_rules_present():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 151):
        assert f"SCX{i:03d}" in ids, f"SCX{i:03d} missing"


def test_school_parashari():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    for rule in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_source_sarvartha_chintamani():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    for rule in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "SarvarthaChintamani", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    for rule in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_sc_tag_on_all_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    for rule in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all():
        assert "sc" in rule.keyword_tags, f"{rule.rule_id} missing 'sc' tag"


def test_all_12_lagnas_covered():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    lagnas = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    for lagna in lagnas:
        rules = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if lagna in r.keyword_tags]
        assert len(rules) >= 1, f"{lagna} not covered"


def test_planets_covered():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    # SC focuses on combinations; at least 7 of 9 planets should appear as tags
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    covered = [p for p in planets
               if any(p in r.keyword_tags for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all())]
    assert len(covered) >= 7, f"Only {len(covered)} planets covered: {covered}"


def test_raja_yoga_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    raja = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all()
            if any("raja_yoga" in t for t in r.keyword_tags)]
    assert len(raja) >= 2


def test_scx025_raja_yoga_tiers():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    rule = SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.get("SCX025")
    assert rule is not None
    assert "raja_yoga" in rule.keyword_tags


def test_scx031_neecha_bhanga():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    rule = SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.get("SCX031")
    assert rule is not None
    assert any("neecha_bhanga" in t for t in rule.keyword_tags)


def test_sade_sati_rule():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    rules = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "sade_sati" in r.keyword_tags]
    assert len(rules) >= 1


def test_marana_karaka_sthana():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    rules = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "marana_karaka_sthana" in r.keyword_tags]
    assert len(rules) >= 1


def test_scx118_dharmakarmadhipati():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    rule = SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.get("SCX118")
    assert rule is not None
    assert "dharmakarmadhipati" in rule.keyword_tags


def test_yoga_count():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    yogas = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "yoga" in r.keyword_tags]
    assert len(yogas) >= 20


def test_longevity_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    longevity = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "longevity" in r.keyword_tags]
    assert len(longevity) >= 2


def test_medical_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    medical = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "medical" in r.keyword_tags]
    assert len(medical) >= 2


def test_transit_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    transit = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "transit" in r.keyword_tags]
    assert len(transit) >= 2


def test_dasha_rules():
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY
    dasha = [r for r in SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY.all() if "dasha" in r.keyword_tags]
    assert len(dasha) >= 2


def test_combined_corpus_includes_scx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2124  # 1974 + 150 = 2124
