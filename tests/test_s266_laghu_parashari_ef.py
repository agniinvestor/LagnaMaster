"""tests/test_s266_laghu_parashari_ef.py — S266: LP Sections E (Antardasha), F (Maraka)."""
from __future__ import annotations


# ── Section E — Antardasha ────────────────────────────────────────────────────

def test_lpa_count():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    assert LAGHU_PARASHARI_ANTARDASHA_REGISTRY.count() >= 60


def test_all_lpa_ids_sequential():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all()}
    n = LAGHU_PARASHARI_ANTARDASHA_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"LPA{i:03d}" in ids, f"LPA{i:03d} missing"


def test_lpa_phase_conditional_or_matrix():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    valid = {"1B_conditional", "1B_matrix"}
    for rule in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all():
        assert rule.phase in valid, f"{rule.rule_id} has phase={rule.phase}"


def test_lpa_primary_condition_has_md_ad():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    for rule in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all():
        pc = rule.primary_condition
        assert "md_type" in pc or "placement_type" in pc, (
            f"{rule.rule_id} missing md_type/placement_type in primary_condition"
        )


def test_lpa_outcome_direction_valid():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


def test_lpa_trikona_trikona_present():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    tt = [r for r in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all()
          if "trikona_md" in r.tags and "trikona_ad" in r.tags]
    assert len(tt) >= 1, "No trikona-MD + trikona-AD rule found"


def test_lpa_maraka_maraka_present():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    mm = [r for r in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all()
          if "maraka_md" in r.tags and "maraka_ad" in r.tags]
    assert len(mm) >= 1, "No maraka-MD + maraka-AD rule found"


def test_lpa_yogakaraka_combinations_present():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    yk = [r for r in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all() if "yogakaraka" in r.tags]
    assert len(yk) >= 3, f"Expected ≥3 yogakaraka antardasha rules, got {len(yk)}"


def test_lpa_source_school():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_ANTARDASHA_REGISTRY
    for rule in LAGHU_PARASHARI_ANTARDASHA_REGISTRY.all():
        assert rule.source == "LaghuParashari"
        assert rule.school == "parashari"


# ── Section F — Maraka ────────────────────────────────────────────────────────

def test_lpm_count():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    assert LAGHU_PARASHARI_MARAKA_REGISTRY.count() >= 24


def test_all_lpm_ids_sequential():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_MARAKA_REGISTRY.all()}
    n = LAGHU_PARASHARI_MARAKA_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"LPM{i:03d}" in ids, f"LPM{i:03d} missing"


def test_lpm_all_12_lagnas_covered():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    lagnas = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    covered = {lg for r in LAGHU_PARASHARI_MARAKA_REGISTRY.all() for lg in r.lagna_scope}
    for lagna in lagnas:
        assert lagna in covered, f"{lagna} not covered in Section F"


def test_lpm_lagna_scope_populated():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    for rule in LAGHU_PARASHARI_MARAKA_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_lpm_maraka_tag_present():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    for rule in LAGHU_PARASHARI_MARAKA_REGISTRY.all():
        assert "maraka" in rule.tags, f"{rule.rule_id} missing maraka tag"


def test_lpm_phase_conditional():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    for rule in LAGHU_PARASHARI_MARAKA_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_lpm_aries_venus_double_maraka():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    aries_venus = [r for r in LAGHU_PARASHARI_MARAKA_REGISTRY.all()
                   if "aries" in r.lagna_scope and "venus" in r.tags]
    assert len(aries_venus) >= 1, "Aries Venus double-maraka rule missing"


def test_lpm_libra_mars_double_maraka():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    libra_mars = [r for r in LAGHU_PARASHARI_MARAKA_REGISTRY.all()
                  if "libra" in r.lagna_scope and "mars" in r.tags]
    assert len(libra_mars) >= 1, "Libra Mars double-maraka rule missing"


def test_lpm_outcome_direction_valid():
    from src.corpus.laghu_parashari_ef import LAGHU_PARASHARI_MARAKA_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in LAGHU_PARASHARI_MARAKA_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


# ── Combined corpus ───────────────────────────────────────────────────────────

def test_combined_includes_ef():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # After S265: 2742 + 12 + 24 + 45 = 2823; + min(60 + 24) = 2907
    assert registry.count() >= 2907


def test_full_lp_coverage_map_progress():
    """Verify Laghu Parashari sections A-F are all present in combined corpus."""
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    lp_rules = [r for r in registry.all() if r.source == "LaghuParashari"]
    # A=108, B=12, C=24, D=45, E≥60, F≥24 → minimum 273
    assert len(lp_rules) >= 273, f"LP rules: {len(lp_rules)}"
