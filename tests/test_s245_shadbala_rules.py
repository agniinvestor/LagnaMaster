"""tests/test_s245_shadbala_rules.py — S245: Shadbala rules."""
from __future__ import annotations


def test_shadbala_count():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    assert SHADBALA_RULES_REGISTRY.count() == 30


def test_all_sdb_rules_present():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    ids = {r.rule_id for r in SHADBALA_RULES_REGISTRY.all()}
    for i in range(1, 31):
        assert f"SDB{i:03d}" in ids, f"SDB{i:03d} missing"


def test_shadbala_category():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    for rule in SHADBALA_RULES_REGISTRY.all():
        assert rule.category == "shadbala", f"{rule.rule_id} wrong category"


def test_schools():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    for rule in SHADBALA_RULES_REGISTRY.all():
        assert rule.school in {"parashari", "sarvartha", "varahamihira"}, (
            f"{rule.rule_id} unexpected school: {rule.school}"
        )


def test_six_strengths_overview():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    rule = SHADBALA_RULES_REGISTRY.get("SDB001")
    assert rule is not None
    assert "6_strengths" in rule.tags
    assert "rupas" in rule.tags


def test_minimum_thresholds():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    rule = SHADBALA_RULES_REGISTRY.get("SDB002")
    assert rule is not None
    assert "minimum_threshold" in rule.tags
    assert "ishta_shadbala" in rule.tags


def test_dig_bala():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    rule = SHADBALA_RULES_REGISTRY.get("SDB009")
    assert rule is not None
    assert "dig_bala" in rule.tags
    assert "directional_strength" in rule.tags


def test_naisargika_bala():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    rule = SHADBALA_RULES_REGISTRY.get("SDB019")
    assert rule is not None
    assert "naisargika_bala" in rule.tags
    assert "sun_60_saturn_8" in rule.tags


def test_retrograde_strength():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    rule = SHADBALA_RULES_REGISTRY.get("SDB017")
    assert rule is not None
    assert "retrograde" in rule.tags
    assert "maximum_strength" in rule.tags


def test_vimshopaka_bala():
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY
    vimsh_rules = [r for r in SHADBALA_RULES_REGISTRY.all() if "vimshopaka_bala" in r.tags]
    assert len(vimsh_rules) == 2


def test_combined_corpus_includes_sdb():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 926  # 896 + 30 = 926
