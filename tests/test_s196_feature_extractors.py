"""
tests/test_s196_feature_extractors.py — S196: kartari, combust, retrograde,
bhavesh_house_type extractors

All four produce well-ranged continuous values. Cumulative: 8 × 12 = 96 features.
"""

from __future__ import annotations


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


# ─── kartari_score (R08 + R12) ────────────────────────────────────────────────

def test_kartari_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_kartari_score"]
        assert -1.0 <= val <= 1.0, f"H{h} kartari_score={val}"


def test_kartari_score_three_values():
    """kartari_score must be in {-1.0, 0.0, 1.0} — paap / none / shubh."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    valid = {-1.0, 0.0, 1.0}
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_kartari_score"]
        assert val in valid, f"H{h} kartari_score={val} not in {valid}"


# ─── combust_score (R19) ──────────────────────────────────────────────────────

def test_combust_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_combust_score"]
        assert -1.0 <= val <= 0.5, f"H{h} combust_score={val}"


def test_combust_score_fine_is_zero():
    """A non-combust bhavesh must have combust_score=0.0."""
    from src.calculations.feature_decomp import extract_features
    # Find any house whose bhavesh is not combust (should exist in India 1947)
    cfv = extract_features(_india_chart())
    fine_vals = [hfv.to_dict()[f"h{h:02d}_combust_score"]
                 for h, hfv in cfv.houses.items()]
    assert 0.0 in fine_vals, "Expected at least one non-combust bhavesh"


# ─── retrograde_score (R22) ───────────────────────────────────────────────────

def test_retrograde_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_retrograde_score"]
        assert -1.0 <= val <= 1.0, f"H{h} retrograde_score={val}"


# ─── bhavesh_house_type (R04 house placement) ─────────────────────────────────

def test_bhavesh_house_type_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_bhavesh_house_type"]
        assert 0.0 <= val <= 1.0, f"H{h} bhavesh_house_type={val}"


# ─── Feature count grows to 8 per house ───────────────────────────────────────

def test_feature_count_is_96():
    """After S196: 8 features × 12 houses = 96 total features."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert cfv.feature_count() == 96, (
        f"Expected 96 features (8×12), got {cfv.feature_count()}"
    )


def test_all_8_feature_names_present_per_house():
    from src.calculations.feature_decomp import extract_features
    EXPECTED = {
        "gentle_sign", "bhavesh_dignity", "dig_bala", "sav_bindus_norm",
        "kartari_score", "combust_score", "retrograde_score", "bhavesh_house_type",
    }
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        names_short = {rf.name for rf in hfv.features}
        assert names_short == EXPECTED, (
            f"H{h} features mismatch: {names_short ^ EXPECTED}"
        )
