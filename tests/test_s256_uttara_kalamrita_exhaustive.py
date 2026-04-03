"""tests/test_s256_uttara_kalamrita_exhaustive.py — S256: Uttara Kalamrita Exhaustive (150 rules)."""
from __future__ import annotations


def test_ukx_count():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    assert UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.count() == 150


def test_all_ukx_rules_present():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    ids = {r.rule_id for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all()}
    for i in range(1, 151):
        assert f"UKX{i:03d}" in ids, f"UKX{i:03d} missing"


def test_school_kalidasa():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    for rule in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all():
        assert rule.school == "kalidasa", f"{rule.rule_id} wrong school"


def test_source_uttara_kalamrita():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    for rule in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all():
        assert rule.source == "UttaraKalamrita", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    for rule in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_uk_tag_on_all_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    for rule in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all():
        assert "uk" in rule.keyword_tags, f"{rule.rule_id} missing 'uk' tag"


def test_all_12_houses_covered():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    ordinals = {
        1: "1st_house", 2: "2nd_house", 3: "3rd_house", 4: "4th_house",
        5: "5th_house", 6: "6th_house", 7: "7th_house", 8: "8th_house",
        9: "9th_house", 10: "10th_house", 11: "11th_house", 12: "12th_house",
    }
    for h, tag in ordinals.items():
        rules = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if tag in r.keyword_tags]
        assert len(rules) >= 1, f"House {h} ({tag}) not covered"


def test_special_lagnas_covered():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    special = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "special_lagna" in r.keyword_tags]
    assert len(special) >= 5


def test_argala_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    argala = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "argala" in r.keyword_tags]
    assert len(argala) >= 4


def test_arudha_all_12():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    arudha = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "arudha" in r.keyword_tags]
    assert len(arudha) >= 12


def test_hora_lagna():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    rule = UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.get("UKX001")
    assert rule is not None
    assert "hora_lagna" in rule.keyword_tags


def test_ghati_lagna():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    rule = UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.get("UKX002")
    assert rule is not None
    assert "ghati_lagna" in rule.keyword_tags


def test_upapada_lagna():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    rule = UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.get("UKX023")
    assert rule is not None
    assert "upapada_lagna" in rule.keyword_tags or "ul" in rule.keyword_tags


def test_gulika_rule():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    rule = UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.get("UKX052")
    assert rule is not None
    assert "gulika" in rule.keyword_tags


def test_all_9_planets_karakatva():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]
    for p in planets:
        rules = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all()
                 if p in r.keyword_tags and "karakatva" in r.keyword_tags]
        assert len(rules) >= 1, f"{p} karakatva not covered"


def test_yoga_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    yogas = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "yoga" in r.keyword_tags]
    assert len(yogas) >= 10


def test_karakamsha_covered():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    kl = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "karakamsha" in r.keyword_tags]
    assert len(kl) >= 4


def test_chara_karakas():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    ck = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "chara_karaka" in r.keyword_tags]
    assert len(ck) >= 3


def test_dasha_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    dasha = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "dasha" in r.keyword_tags]
    assert len(dasha) >= 5


def test_transit_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    transit = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "transit" in r.keyword_tags]
    assert len(transit) >= 4


def test_sade_sati():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    rule = UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.get("UKX135")
    assert rule is not None
    assert "sade_sati" in rule.keyword_tags


def test_varga_rules():
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY
    varga = [r for r in UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY.all() if "varga" in r.keyword_tags]
    assert len(varga) >= 3


def test_combined_corpus_includes_ukx():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1824  # 1674 + 150 = 1824
