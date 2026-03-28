"""
tests/test_s198_pushkara_warlost_features.py — S198: pushkara_nav, war_loser

Two more extractors; cumulative 13 × 12 = 156 features (crosses 150 threshold).
"""

from __future__ import annotations


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


def test_pushkara_nav_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_pushkara_nav"]
        assert val in {0.0, 1.0}, f"H{h} pushkara_nav={val} not binary"


def test_war_loser_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_war_loser"]
        assert val in {0.0, -1.0}, f"H{h} war_loser={val} not in {{0.0, -1.0}}"


def test_feature_count_is_156():
    """After S198: 13 features × 12 houses = 156 total — crosses 150 threshold."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert cfv.feature_count() == 156, f"Expected 156, got {cfv.feature_count()}"


def test_all_13_feature_names_present():
    from src.calculations.feature_decomp import extract_features
    EXPECTED = {
        "gentle_sign", "bhavesh_dignity", "dig_bala", "sav_bindus_norm",
        "kartari_score", "combust_score", "retrograde_score", "bhavesh_house_type",
        "benefic_net_score", "malefic_net_score", "karak_score",
        "pushkara_nav", "war_loser",
    }
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        names = {rf.name for rf in hfv.features}
        assert names == EXPECTED, f"H{h}: {names ^ EXPECTED}"


def test_feature_count_exceeds_150():
    """G22 contract: feature space must be ≥ 150 before Phase 6."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert cfv.feature_count() >= 150, (
        f"Phase 6 requires ≥150 features; got {cfv.feature_count()}"
    )
