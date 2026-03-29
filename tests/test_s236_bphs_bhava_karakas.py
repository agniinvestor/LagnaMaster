"""tests/test_s236_bphs_bhava_karakas.py — S236: BPHS Bhava Karakas."""
from __future__ import annotations


def test_bphs_bhava_karakas_count():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    assert BPHS_BHAVA_KARAKAS_REGISTRY.count() == 30


def test_all_bhk_rules_present():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    ids = {r.rule_id for r in BPHS_BHAVA_KARAKAS_REGISTRY.all()}
    for i in range(1, 31):
        assert f"BHK{i:03d}" in ids, f"BHK{i:03d} missing"


def test_12_naisargika_karakas():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    naisargika_rules = [
        r for r in BPHS_BHAVA_KARAKAS_REGISTRY.all()
        if any(f"{n}th_house" in r.tags or f"{n}st_house" in r.tags or
               f"{n}nd_house" in r.tags or f"{n}rd_house" in r.tags
               for n in range(1, 13))
        and "jaimini" not in r.tags
        and r.rule_id.startswith("BHK0") and int(r.rule_id[3:]) <= 12
    ]
    assert len(naisargika_rules) == 12


def test_7th_house_venus_karaka():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    rule = BPHS_BHAVA_KARAKAS_REGISTRY.get("BHK007")
    assert rule is not None
    assert "venus" in rule.tags
    assert "spouse" in rule.tags


def test_karaka_bhava_nashta():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    rule = BPHS_BHAVA_KARAKAS_REGISTRY.get("BHK021")
    assert rule is not None
    assert "karaka_bhava_nashta" in rule.tags


def test_atmakaraka_rule():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    rule = BPHS_BHAVA_KARAKAS_REGISTRY.get("BHK014")
    assert rule is not None
    assert "atmakaraka" in rule.tags
    assert rule.school == "jaimini"


def test_jaimini_karakas_present():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    jaimini_rules = [r for r in BPHS_BHAVA_KARAKAS_REGISTRY.all() if r.school == "jaimini"]
    assert len(jaimini_rules) == 8  # BHK013-020


def test_all_bhava_karaka_category():
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY
    for rule in BPHS_BHAVA_KARAKAS_REGISTRY.all():
        assert rule.category == "bhava_karaka", f"{rule.rule_id} wrong category"


def test_combined_corpus_includes_bhava_karakas():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 656  # 626 + 30
