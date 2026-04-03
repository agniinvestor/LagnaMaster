"""tests/test_s251_bphs_graha_bhava_complete.py — S251: BPHS Graha-Bhava Complete (108 rules)."""
from __future__ import annotations


def test_gbc_count():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    assert BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.count() == 108


def test_all_gbc_rules_present():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    ids = {r.rule_id for r in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all()}
    for i in range(1, 109):
        assert f"GBC{i:03d}" in ids, f"GBC{i:03d} missing"


def test_gbc_category():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for rule in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all():
        assert rule.category == "graha_bhava", f"{rule.rule_id} wrong category"


def test_gbc_school_parashari():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for rule in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} unexpected school: {rule.school}"


def test_gbc_source_bphs():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for rule in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all():
        assert rule.source == "BPHS", f"{rule.rule_id} wrong source"


def test_nine_planets_twelve_houses_each():
    """Each of 9 planets must have exactly 12 rules (one per house)."""
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    planets = [
        "sun", "moon", "mars", "mercury",
        "jupiter", "venus", "saturn", "rahu", "ketu",
    ]
    for planet in planets:
        planet_rules = [
            r for r in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all()
            if any(t.startswith(f"{planet}_") for t in r.keyword_tags)
        ]
        assert len(planet_rules) == 12, (
            f"{planet} has {len(planet_rules)} rules, expected 12"
        )


def test_sun_block_gbc001_012():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for i in range(1, 13):
        rule = BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.get(f"GBC{i:03d}")
        assert rule is not None
        assert any(t.startswith("sun_") for t in rule.keyword_tags), f"GBC{i:03d} missing sun_ tag"


def test_moon_block_gbc013_024():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for i in range(13, 25):
        rule = BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.get(f"GBC{i:03d}")
        assert rule is not None
        assert any(t.startswith("moon_") for t in rule.keyword_tags), f"GBC{i:03d} missing moon_ tag"


def test_rahu_ketu_blocks():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for i in range(85, 97):
        rule = BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.get(f"GBC{i:03d}")
        assert rule is not None
        assert any(t.startswith("rahu_") for t in rule.keyword_tags), f"GBC{i:03d} missing rahu_ tag"
    for i in range(97, 109):
        rule = BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.get(f"GBC{i:03d}")
        assert rule is not None
        assert any(t.startswith("ketu_") for t in rule.keyword_tags), f"GBC{i:03d} missing ketu_ tag"


def test_implemented_false():
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY
    for rule in BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY.all():
        assert rule.implemented is False, f"{rule.rule_id} should be implemented=False"


def test_combined_corpus_includes_gbc():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 1184  # 1076 + 108 = 1184
