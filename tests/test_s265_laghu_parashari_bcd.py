"""tests/test_s265_laghu_parashari_bcd.py — S265: LP Sections B (Yogakaraka), C (Kendradhipati), D (Dasha)."""
from __future__ import annotations


# ── Section B — Yogakaraka ────────────────────────────────────────────────────

def test_lpy_count():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    assert LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.count() == 12


def test_all_lpy_ids_present():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.all()}
    for i in range(1, 13):
        assert f"LPY{i:03d}" in ids, f"LPY{i:03d} missing"


def test_lpy_all_12_lagnas_covered():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    lagnas = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
    ]
    covered = {lg for r in LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.all() for lg in r.lagna_scope}
    for lagna in lagnas:
        assert lagna in covered, f"{lagna} not covered in Section B"


def test_lpy_yogakaraka_6_lagnas():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    yk = [r for r in LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.all() if "yogakaraka" in r.keyword_tags]
    assert len(yk) == 6, f"Expected 6 yogakaraka rules, got {len(yk)}"


def test_lpy_no_yogakaraka_6_lagnas():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    no_yk = [r for r in LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.all() if "no_yogakaraka" in r.keyword_tags]
    assert len(no_yk) == 6, f"Expected 6 no_yogakaraka rules, got {len(no_yk)}"


def test_lpy002_taurus_saturn_yogakaraka():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    rule = LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.get("LPY002")
    assert rule is not None
    assert "taurus" in rule.lagna_scope
    assert "saturn" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpy004_cancer_mars_yogakaraka():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    rule = LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.get("LPY004")
    assert rule is not None
    assert "cancer" in rule.lagna_scope
    assert "mars" in rule.keyword_tags
    assert "yogakaraka" in rule.keyword_tags


def test_lpy_phase_school_source():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_YOGAKARAKA_REGISTRY
    for rule in LAGHU_PARASHARI_YOGAKARAKA_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"
        assert rule.school == "parashari"
        assert rule.source == "LaghuParashari"
        assert rule.system == "natal"


# ── Section C — Kendradhipati ─────────────────────────────────────────────────

def test_lpk_count():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    assert LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.count() >= 20


def test_all_lpk_ids_sequential():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all()}
    n = LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"LPK{i:03d}" in ids, f"LPK{i:03d} missing"


def test_lpk_lagna_scope_populated():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    for rule in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all():
        assert len(rule.lagna_scope) >= 1, f"{rule.rule_id} has empty lagna_scope"


def test_lpk_phase_1b_conditional():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    for rule in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all():
        assert rule.phase == "1B_conditional", f"{rule.rule_id} wrong phase"


def test_lpk_aries_moon():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    aries_moon = [r for r in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all()
                  if "aries" in r.lagna_scope and "moon" in r.keyword_tags]
    assert len(aries_moon) >= 1, "Aries Moon KD rule missing"


def test_lpk_gemini_jupiter():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    gmj = [r for r in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all()
           if "gemini" in r.lagna_scope and "jupiter" in r.keyword_tags]
    assert len(gmj) >= 1, "Gemini Jupiter KD rule missing"


def test_lpk_virgo_jupiter():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    vj = [r for r in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all()
          if "virgo" in r.lagna_scope and "jupiter" in r.keyword_tags]
    assert len(vj) >= 1, "Virgo Jupiter KD rule missing"


def test_lpk_primary_condition_populated():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY
    for rule in LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY.all():
        assert rule.primary_condition, f"{rule.rule_id} primary_condition empty"
        assert "planet" in rule.primary_condition


# ── Section D — Dasha Results ─────────────────────────────────────────────────

def test_lpd_count():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    assert LAGHU_PARASHARI_DASHA_REGISTRY.count() >= 42


def test_all_lpd_ids_sequential():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    ids = {r.rule_id for r in LAGHU_PARASHARI_DASHA_REGISTRY.all()}
    n = LAGHU_PARASHARI_DASHA_REGISTRY.count()
    for i in range(1, n + 1):
        assert f"LPD{i:03d}" in ids, f"LPD{i:03d} missing"


def test_lpd_phase_matrix_or_conditional():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    valid = {"1B_matrix", "1B_conditional"}
    for rule in LAGHU_PARASHARI_DASHA_REGISTRY.all():
        assert rule.phase in valid, f"{rule.rule_id} has phase={rule.phase}"


def test_lpd_all_12_houses_covered():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    all_pv = []
    for r in LAGHU_PARASHARI_DASHA_REGISTRY.all():
        pv = r.primary_condition.get("placement_value") or []
        all_pv.extend(pv)
    for house in range(1, 13):
        assert house in all_pv, f"H{house} not covered in Section D"


def test_lpd_yogakaraka_present():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    yk = [r for r in LAGHU_PARASHARI_DASHA_REGISTRY.all() if "yogakaraka" in r.keyword_tags]
    assert len(yk) >= 1, "No yogakaraka dasha rule found"


def test_lpd_maraka_present():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    mk = [r for r in LAGHU_PARASHARI_DASHA_REGISTRY.all() if "maraka" in r.keyword_tags]
    assert len(mk) >= 1, "No maraka dasha rule found"


def test_lpd_source_school():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    for rule in LAGHU_PARASHARI_DASHA_REGISTRY.all():
        assert rule.school == "parashari"
        assert rule.source == "LaghuParashari"


def test_lpd_outcome_direction_valid():
    from src.corpus.laghu_parashari_bcd import LAGHU_PARASHARI_DASHA_REGISTRY
    valid = {"favorable", "unfavorable", "neutral", "mixed"}
    for rule in LAGHU_PARASHARI_DASHA_REGISTRY.all():
        assert rule.outcome_direction in valid, f"{rule.rule_id} bad direction"


# ── Combined corpus ───────────────────────────────────────────────────────────

def test_combined_includes_bcd():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    # 2742 + min(12 + 20 + 42) = 2742 + 74 = 2816
    assert registry.count() >= 2816
