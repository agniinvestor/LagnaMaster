"""tests/test_s246_dasha_systems_rules.py — S246: Dasha systems rules."""
from __future__ import annotations


def test_dasha_systems_count():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    assert DASHA_SYSTEMS_RULES_REGISTRY.count() == 30


def test_all_dsy_rules_present():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    ids = {r.rule_id for r in DASHA_SYSTEMS_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"DSY{i:03d}" in ids, f"DSY{i:03d} missing"


def test_dasha_category():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    for rule in DASHA_SYSTEMS_RULES_REGISTRY.all():
        assert rule.category == "dasha", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    for rule in DASHA_SYSTEMS_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "sarvartha", "kalidasa", "jaimini"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_vimshottari_primary():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    rule = DASHA_SYSTEMS_RULES_REGISTRY.get("DSY001")
    assert rule is not None
    assert "vimshottari" in rule.keyword_tags
    assert "primary_dasha" in rule.keyword_tags
    assert "120_years" in rule.keyword_tags


def test_ashtottari_dasha():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    rule = DASHA_SYSTEMS_RULES_REGISTRY.get("DSY007")
    assert rule is not None
    assert "ashtottari" in rule.keyword_tags
    assert "108_years" in rule.keyword_tags


def test_yogini_dasha():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    rule = DASHA_SYSTEMS_RULES_REGISTRY.get("DSY010")
    assert rule is not None
    assert "yogini_dasha" in rule.keyword_tags
    assert "36_years" in rule.keyword_tags


def test_maraka_dasha():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    rule = DASHA_SYSTEMS_RULES_REGISTRY.get("DSY025")
    assert rule is not None
    assert "maraka" in rule.keyword_tags
    assert "2nd_7th_lord" in rule.keyword_tags


def test_transit_confirmation():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    rule = DASHA_SYSTEMS_RULES_REGISTRY.get("DSY022")
    assert rule is not None
    assert "transit_confirmation" in rule.keyword_tags
    assert "dasha_transit" in rule.keyword_tags


def test_planet_dashas_present():
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY
    for rule_id in ["DSY026", "DSY027", "DSY028", "DSY029", "DSY030"]:
        rule = DASHA_SYSTEMS_RULES_REGISTRY.get(rule_id)
        assert rule is not None, f"{rule_id} missing"


def test_combined_corpus_includes_dsy():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 956  # 926 + 30 = 956
