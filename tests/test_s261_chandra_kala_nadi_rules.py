"""tests/test_s261_chandra_kala_nadi_rules.py — S261: Chandra Kala Nadi Exhaustive (120 rules)."""
from __future__ import annotations


def test_ckn_count():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    assert CHANDRA_KALA_NADI_REGISTRY.count() == 120


def test_all_ckn_rules_present():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    ids = {r.rule_id for r in CHANDRA_KALA_NADI_REGISTRY.all()}
    for i in range(1, 121):
        assert f"CKN{i:03d}" in ids, f"CKN{i:03d} missing"


def test_school_nadi():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    for rule in CHANDRA_KALA_NADI_REGISTRY.all():
        assert rule.school == "nadi", f"{rule.rule_id} wrong school"


def test_source_chandra_kala_nadi():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    for rule in CHANDRA_KALA_NADI_REGISTRY.all():
        assert rule.source == "ChandraKalaNadi", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    for rule in CHANDRA_KALA_NADI_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_ckn_tag_on_all_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    for rule in CHANDRA_KALA_NADI_REGISTRY.all():
        assert "ckn" in rule.tags, f"{rule.rule_id} missing 'ckn' tag"


def test_nadi_tag_on_all_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    for rule in CHANDRA_KALA_NADI_REGISTRY.all():
        assert "nadi" in rule.tags, f"{rule.rule_id} missing 'nadi' tag"


def test_moon_nakshatra_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    mn = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "moon_nakshatra" in r.category]
    assert len(mn) >= 27


def test_all_27_nakshatras_covered():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    nakshatras = [
        "ashwini", "bharani", "krittika", "rohini", "mrigashira", "ardra",
        "punarvasu", "pushya", "ashlesha", "magha", "purva_phalguni", "uttara_phalguni",
        "hasta", "chitra", "swati", "vishakha", "anuradha", "jyeshtha",
        "mula", "purva_ashadha", "uttara_ashadha", "shravana", "dhanishtha",
        "shatabhisha", "purva_bhadrapada", "uttara_bhadrapada", "revati",
    ]
    for nak in nakshatras:
        rules = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if nak in r.tags]
        assert len(rules) >= 1, f"{nak} not covered"


def test_transit_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    transit = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "transit" in r.tags]
    assert len(transit) >= 8


def test_dasha_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    dasha = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "dasha" in r.tags]
    assert len(dasha) >= 8


def test_yoga_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    yoga = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "yoga" in r.tags]
    assert len(yoga) >= 5


def test_medical_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    medical = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "medical" in r.tags]
    assert len(medical) >= 3


def test_sade_sati_rule():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rules = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "sade_sati" in r.tags]
    assert len(rules) >= 1


def test_tara_rules():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    tara = [r for r in CHANDRA_KALA_NADI_REGISTRY.all() if "tara" in r.tags]
    assert len(tara) >= 3


def test_ckn001_ashwini():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rule = CHANDRA_KALA_NADI_REGISTRY.get("CKN001")
    assert rule is not None
    assert "ashwini" in rule.tags


def test_ckn028_gaja_kesari():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rule = CHANDRA_KALA_NADI_REGISTRY.get("CKN028")
    assert rule is not None
    assert "gaja_kesari_yoga" in rule.tags


def test_ckn041_sade_sati():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rule = CHANDRA_KALA_NADI_REGISTRY.get("CKN041")
    assert rule is not None
    assert "sade_sati" in rule.tags


def test_ckn064_nine_taras():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rule = CHANDRA_KALA_NADI_REGISTRY.get("CKN064")
    assert rule is not None
    assert "9_taras" in rule.tags


def test_ckn120_philosophy():
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY
    rule = CHANDRA_KALA_NADI_REGISTRY.get("CKN120")
    assert rule is not None
    assert "philosophy" in rule.tags


def test_combined_corpus_includes_ckn():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2514  # 2394 + 120 = 2514
