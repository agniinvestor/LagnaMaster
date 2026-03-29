"""tests/test_s254_bphs_graha_characteristics.py — S254: BPHS Graha Characteristics (100 rules)."""
from __future__ import annotations


def test_gch_count():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    assert BPHS_GRAHA_CHARACTERISTICS_REGISTRY.count() == 100


def test_all_gch_rules_present():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all()}
    for i in range(1, 101):
        assert f"GCH{i:03d}" in ids, f"GCH{i:03d} missing"


def test_gch_category():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    for rule in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all():
        assert rule.category == "graha_nature", f"{rule.rule_id} wrong category"


def test_gch_school_parashari():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    for rule in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} unexpected school"


def test_all_9_planets_covered():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    for planet in planets:
        planet_rules = [r for r in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all() if planet in r.tags]
        min_rules = 2 if planet in {"rahu", "ketu"} else 3
        assert len(planet_rules) >= min_rules, f"{planet} has fewer than {min_rules} rules"


def test_special_aspects_rule():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH035")
    assert rule is not None
    assert "saturn_3_10" in rule.tags
    assert "jupiter_5_9" in rule.tags
    assert "mars_4_8" in rule.tags


def test_combustion_degrees():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH038")
    assert rule is not None
    assert "combustion" in rule.tags
    assert "asta" in rule.tags


def test_vimshottari_periods():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH045")
    assert rule is not None
    assert "venus_20" in rule.tags
    assert "saturn_19" in rule.tags


def test_naisargika_bala():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH071")
    assert rule is not None
    assert "sun_60" in rule.tags
    assert "saturn_8.57" in rule.tags


def test_maturation_ages():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH098")
    assert rule is not None
    assert "saturn_36" in rule.tags
    assert "jupiter_16" in rule.tags


def test_graha_yuddha():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    rule = BPHS_GRAHA_CHARACTERISTICS_REGISTRY.get("GCH040")
    assert rule is not None
    assert "graha_yuddha" in rule.tags


def test_medical_astrology_covered():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    medical = [r for r in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all() if "medical_astrology" in r.tags]
    assert len(medical) >= 8


def test_gems_and_metals():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    gems = [r for r in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all() if "gem_ruby" in r.tags or "gem_pearl" in r.tags
            or "gem_emerald" in r.tags or "gem_yellow_sapphire" in r.tags or "gem_diamond" in r.tags
            or "gem_blue_sapphire" in r.tags or "gem_hessonite_catseye" in r.tags or "gem_red_coral" in r.tags]
    assert len(gems) == 8  # one per planet


def test_implemented_false():
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY
    for rule in BPHS_GRAHA_CHARACTERISTICS_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_combined_corpus_includes_gch():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1554  # 1454 + 100 = 1554
