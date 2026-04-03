"""tests/test_s264_laghu_parashari_functional.py — S264: Laghu Parashari Functional Nature Table."""
from __future__ import annotations


def test_lpf_count():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    assert LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.count() == 108


def test_all_lpf_ids_present():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all()}
    for i in range(1, 109):
        assert f"LPF{i:03d}" in ids, f"LPF{i:03d} missing"


def test_school_parashari():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_source_laghu_parashari():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.source == "LaghuParashari", f"{rule.rule_id} wrong source"


def test_implemented_false():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.implemented is False


def test_phase_1b_conditional():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} has phase={rule.phase}"


def test_lagna_scope_populated():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert len(rule.lagna_scope) == 1, f"{rule.rule_id} lagna_scope must have exactly 1 lagna"


def test_primary_condition_populated():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.primary_condition, f"{rule.rule_id} primary_condition is empty"
        assert "planet" in rule.primary_condition
        assert "placement_type" in rule.primary_condition


def test_outcome_direction_set():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.outcome_direction in valid, (
            f"{rule.rule_id} has outcome_direction='{rule.outcome_direction}'"
        )


def test_outcome_intensity_set():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    valid = {"strong", "moderate", "weak", "conditional"}
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.outcome_intensity in valid, (
            f"{rule.rule_id} has outcome_intensity='{rule.outcome_intensity}'"
        )


def test_verse_ref_set():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.verse_ref, f"{rule.rule_id} verse_ref is empty"
        assert "v." in rule.verse_ref, f"{rule.rule_id} verse_ref must include verse number"


def test_outcome_domains_from_taxonomy():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    valid_domains = {
        "longevity", "physical_health", "mental_health", "wealth", "career_status",
        "marriage", "progeny", "spirituality", "intelligence_education",
        "character_temperament", "physical_appearance", "foreign_travel",
        "enemies_litigation", "property_vehicles", "fame_reputation",
    }
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        for d in rule.outcome_domains:
            assert d in valid_domains, f"{rule.rule_id} has invalid domain '{d}'"


def test_all_12_lagnas_covered():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    lagnas = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    for lagna in lagnas:
        rules = [r for r in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all()
                 if lagna in r.lagna_scope]
        assert len(rules) == 9, f"{lagna} has {len(rules)} rules, expected 9"


def test_yogakaraka_count():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    yogakaraka_rules = [r for r in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all()
                        if "yogakaraka" in r.keyword_tags]
    assert len(yogakaraka_rules) == 6, f"Expected 6 yogakaraka rules, got {len(yogakaraka_rules)}"


def test_aries_no_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    aries_yks = [r for r in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all()
                 if "aries" in r.lagna_scope and "yogakaraka" in r.keyword_tags]
    assert len(aries_yks) == 0


def test_lpf016_taurus_saturn_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF016")
    assert rule is not None
    assert "taurus" in rule.lagna_scope
    assert "saturn" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpf030_cancer_mars_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF030")
    assert rule is not None
    assert "cancer" in rule.lagna_scope
    assert "mars" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpf039_leo_mars_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF039")
    assert rule is not None
    assert "leo" in rule.lagna_scope
    assert "yogakaraka" in rule.keyword_tags


def test_lpf061_libra_saturn_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF061")
    assert rule is not None
    assert "libra" in rule.lagna_scope
    assert "saturn" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpf087_capricorn_venus_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF087")
    assert rule is not None
    assert "capricorn" in rule.lagna_scope
    assert "venus" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpf096_aquarius_venus_yogakaraka():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    rule = LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.get("LPF096")
    assert rule is not None
    assert "aquarius" in rule.lagna_scope
    assert "yogakaraka" in rule.keyword_tags


def test_system_natal():
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY
    for rule in LAGHU_PARASHARI_FUNCTIONAL_REGISTRY.all():
        assert rule.system == "natal", f"{rule.rule_id} has system={rule.system}"


def test_combined_corpus_includes_lpf():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 2742  # 2634 + 108
