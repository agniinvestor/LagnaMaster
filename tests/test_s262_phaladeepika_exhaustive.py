"""tests/test_s262_phaladeepika_exhaustive.py — S262: Phaladeepika Exhaustive (120 rules)."""
from __future__ import annotations


def test_phx_count():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    assert PHALADEEPIKA_EXHAUSTIVE_REGISTRY.count() == 120


def test_all_phx_rules_present():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 121):
        assert f"PHX{i:03d}" in ids, f"PHX{i:03d} missing"


def test_school_parashari():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    for rule in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_source_phaladeepika():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    for rule in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "Phaladeepika", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    for rule in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_phx_tag_on_all_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    for rule in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all():
        assert "phx" in rule.keyword_tags, f"{rule.rule_id} missing 'phx' tag"


def test_parashari_tag_on_all_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    for rule in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all():
        assert "parashari" in rule.keyword_tags, f"{rule.rule_id} missing 'parashari' tag"


def test_all_12_rashis_covered():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rashis = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    for rashi in rashis:
        rules = [r for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all() if rashi in r.keyword_tags]
        assert len(rules) >= 1, f"{rashi} not covered"


def test_planets_covered():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    covered = [
        p for p in planets
        if any(p in r.keyword_tags for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all())
    ]
    assert len(covered) >= 7


def test_yoga_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    yoga = [r for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all() if "yoga" in r.keyword_tags]
    assert len(yoga) >= 10


def test_dignity_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    dignity = [r for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all() if "dignity" in r.keyword_tags]
    assert len(dignity) >= 5


def test_house_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    house_tags = [
        "1st_house", "2nd_house", "3rd_house", "4th_house", "5th_house", "6th_house",
        "7th_house", "8th_house", "9th_house", "10th_house", "11th_house", "12th_house",
    ]
    covered = [
        t for t in house_tags
        if any(t in r.keyword_tags for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all())
    ]
    assert len(covered) >= 12


def test_dasha_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    dasha = [r for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all() if "dasha" in r.keyword_tags]
    assert len(dasha) >= 5


def test_divisional_chart_rules():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    div = [r for r in PHALADEEPIKA_EXHAUSTIVE_REGISTRY.all() if "varga" in r.keyword_tags]
    assert len(div) >= 5


def test_phx022_exaltation():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX022")
    assert rule is not None
    assert "exaltation" in rule.keyword_tags


def test_phx026_neecha_bhanga():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX026")
    assert rule is not None
    assert any("neecha_bhanga" in t for t in rule.keyword_tags)


def test_phx046_pancha_mahapurusha():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX046")
    assert rule is not None
    assert "pancha_mahapurusha" in rule.keyword_tags


def test_phx047_gaja_kesari():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX047")
    assert rule is not None
    assert any("gaja_kesari" in t for t in rule.keyword_tags)


def test_phx087_sade_sati():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX087")
    assert rule is not None
    assert "sade_sati" in rule.keyword_tags


def test_phx103_shadbala():
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY
    rule = PHALADEEPIKA_EXHAUSTIVE_REGISTRY.get("PHX103")
    assert rule is not None
    assert "shadbala" in rule.keyword_tags


def test_combined_corpus_includes_phx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2634  # 2514 + 120 = 2634
