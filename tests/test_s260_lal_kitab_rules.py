"""tests/test_s260_lal_kitab_rules.py — S260: Lal Kitab Exhaustive (120 rules)."""
from __future__ import annotations


def test_lkx_count():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    assert LAL_KITAB_RULES_REGISTRY.count() == 120


def test_all_lkx_rules_present():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    ids = {r.rule_id for r in LAL_KITAB_RULES_REGISTRY.all()}
    for i in range(1, 121):
        assert f"LKX{i:03d}" in ids, f"LKX{i:03d} missing"


def test_school_lal_kitab():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    for rule in LAL_KITAB_RULES_REGISTRY.all():
        assert rule.school == "lal_kitab", f"{rule.rule_id} wrong school"


def test_source_lal_kitab():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    for rule in LAL_KITAB_RULES_REGISTRY.all():
        assert rule.source == "LalKitab", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    for rule in LAL_KITAB_RULES_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_lkx_tag_on_all_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    for rule in LAL_KITAB_RULES_REGISTRY.all():
        assert "lkx" in rule.tags, f"{rule.rule_id} missing 'lkx' tag"


def test_lal_kitab_tag_on_all_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    for rule in LAL_KITAB_RULES_REGISTRY.all():
        assert "lal_kitab" in rule.tags, f"{rule.rule_id} missing 'lal_kitab' tag"


def test_pakka_ghar_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    pg = [r for r in LAL_KITAB_RULES_REGISTRY.all() if "pakka_ghar" in r.tags]
    assert len(pg) >= 7


def test_all_9_planets_covered():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    for p in planets:
        rules = [r for r in LAL_KITAB_RULES_REGISTRY.all() if p in r.tags]
        assert len(rules) >= 2, f"{p} has fewer than 2 rules"


def test_andha_planet_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    andha = [r for r in LAL_KITAB_RULES_REGISTRY.all() if "andha" in r.tags]
    assert len(andha) >= 5


def test_rin_karma_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rin = [r for r in LAL_KITAB_RULES_REGISTRY.all() if "rin_karma" in r.tags]
    assert len(rin) >= 5


def test_remedy_rules():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    remedy = [r for r in LAL_KITAB_RULES_REGISTRY.all() if "remedy" in r.tags]
    assert len(remedy) >= 10


def test_all_12_houses_covered():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    houses = [f"{i}th_house" if i != 1 else "1st_house" for i in range(1, 13)]
    houses[1] = "2nd_house"
    houses[2] = "3rd_house"
    houses[3] = "4th_house"
    houses[4] = "5th_house"
    houses[5] = "6th_house"
    houses[6] = "7th_house"
    houses[7] = "8th_house"
    houses[8] = "9th_house"
    houses[9] = "10th_house"
    houses[10] = "11th_house"
    houses[11] = "12th_house"
    for house in houses:
        rules = [r for r in LAL_KITAB_RULES_REGISTRY.all() if house in r.tags]
        assert len(rules) >= 1, f"{house} not covered"


def test_lkx001_sun_pakka_ghar():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rule = LAL_KITAB_RULES_REGISTRY.get("LKX001")
    assert rule is not None
    assert "pakka_ghar" in rule.tags
    assert "sun" in rule.tags


def test_lkx019_rin_karma():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rule = LAL_KITAB_RULES_REGISTRY.get("LKX019")
    assert rule is not None
    assert "rin_karma" in rule.tags


def test_lkx056_empty_house():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rule = LAL_KITAB_RULES_REGISTRY.get("LKX056")
    assert rule is not None
    assert "empty_house" in rule.tags


def test_lkx111_vish_yoga():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rule = LAL_KITAB_RULES_REGISTRY.get("LKX111")
    assert rule is not None
    assert "vish_yoga" in rule.tags


def test_lkx110_yoga():
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY
    rule = LAL_KITAB_RULES_REGISTRY.get("LKX110")
    assert rule is not None
    assert "yoga" in rule.tags


def test_combined_corpus_includes_lkx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2394  # 2274 + 120 = 2394
