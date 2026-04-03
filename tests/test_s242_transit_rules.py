"""tests/test_s242_transit_rules.py — S242: Classical transit (Gochara) rules."""
from __future__ import annotations


def test_transit_rules_count():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    assert TRANSIT_RULES_REGISTRY.count() == 30


def test_all_trn_rules_present():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    ids = {r.rule_id for r in TRANSIT_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"TRN{i:03d}" in ids, f"TRN{i:03d} missing"


def test_transit_schools():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    for rule in TRANSIT_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "sarvartha", "kp"}, (
            f"{rule.rule_id} has unexpected school: {rule.school}"
        )


def test_transit_category():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    for rule in TRANSIT_RULES_REGISTRY.all():
        assert rule.category == "transit", f"{rule.rule_id} wrong category"


def test_fundamental_gochara_from_moon():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    rule = TRANSIT_RULES_REGISTRY.get("TRN001")
    assert rule is not None
    assert "from_moon" in rule.keyword_tags
    assert "janma_rashi" in rule.keyword_tags
    assert "fundamental" in rule.keyword_tags


def test_vedha_principle():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    rule = TRANSIT_RULES_REGISTRY.get("TRN004")
    assert rule is not None
    assert "vedha" in rule.keyword_tags
    assert "obstruction" in rule.keyword_tags


def test_sade_sati_rule():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    sade_sati_rules = [
        r for r in TRANSIT_RULES_REGISTRY.all()
        if "sade_sati" in r.keyword_tags
    ]
    assert len(sade_sati_rules) >= 1
    rule = sade_sati_rules[0]
    assert "saturn_7_5_years" in rule.keyword_tags


def test_ashtakavarga_rule():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    rule = TRANSIT_RULES_REGISTRY.get("TRN005")
    assert rule is not None
    assert "ashtakavarga" in rule.keyword_tags
    assert "bindus" in rule.keyword_tags


def test_double_transit_rule():
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY
    double_transit = [
        r for r in TRANSIT_RULES_REGISTRY.all()
        if "double_transit" in r.keyword_tags
    ]
    assert len(double_transit) >= 1


def test_combined_corpus_includes_trn():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 836  # 806 + 30 = 836
