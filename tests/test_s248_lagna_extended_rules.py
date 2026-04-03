"""tests/test_s248_lagna_extended_rules.py — S248: Lagna extended rules."""
from __future__ import annotations


def test_lagna_extended_count():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    assert LAGNA_EXTENDED_RULES_REGISTRY.count() == 30


def test_all_lge_rules_present():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    ids = {r.rule_id for r in LAGNA_EXTENDED_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"LGE{i:03d}" in ids, f"LGE{i:03d} missing"


def test_lagna_category():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    for rule in LAGNA_EXTENDED_RULES_REGISTRY.all():
        assert rule.category == "lagna", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    for rule in LAGNA_EXTENDED_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "varahamihira", "mantreswara"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_all_12_lagna_signs_covered():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    lagna_tags = [
        "aries_lagna", "taurus_lagna", "gemini_lagna", "cancer_lagna",
        "leo_lagna", "virgo_lagna", "libra_lagna", "scorpio_lagna",
        "sagittarius_lagna", "capricorn_lagna", "aquarius_lagna", "pisces_lagna",
    ]
    all_tags = set()
    for rule in LAGNA_EXTENDED_RULES_REGISTRY.all():
        all_tags.update(rule.keyword_tags)
    for tag in lagna_tags:
        assert tag in all_tags, f"Missing lagna tag: {tag}"


def test_yogakaraka_rules():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    yogakaraka_rules = [r for r in LAGNA_EXTENDED_RULES_REGISTRY.all() if "yogakaraka" in r.keyword_tags]
    assert len(yogakaraka_rules) >= 4


def test_kendra_adhipati_dosha():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    rule = LAGNA_EXTENDED_RULES_REGISTRY.get("LGE017")
    assert rule is not None
    assert "kendra_adhipati_dosha" in rule.keyword_tags
    assert "benefic_kendra_lord" in rule.keyword_tags


def test_vargottama_lagna():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    rule = LAGNA_EXTENDED_RULES_REGISTRY.get("LGE028")
    assert rule is not None
    assert "vargottama_lagna" in rule.keyword_tags
    assert "exceptional_strength" in rule.keyword_tags


def test_chandra_surya_lagna():
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY
    chandra = LAGNA_EXTENDED_RULES_REGISTRY.get("LGE019")
    surya = LAGNA_EXTENDED_RULES_REGISTRY.get("LGE020")
    assert chandra is not None and "chandra_lagna" in chandra.keyword_tags
    assert surya is not None and "surya_lagna" in surya.keyword_tags


def test_combined_corpus_includes_lge():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1016  # 986 + 30 = 1016
