"""
tests/test_s197_net_karak_features.py — S197: benefic_net_score, malefic_net_score, karak_score

Three more extractors; cumulative 11 × 12 = 132 features.
"""

from __future__ import annotations


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(year=1947, month=8, day=15, hour=0.0,
                         lat=28.6139, lon=77.2090, tz_offset=5.5)


def test_benefic_net_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_benefic_net_score"]
        assert 0.0 <= val <= 1.0, f"H{h} benefic_net_score={val}"


def test_malefic_net_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_malefic_net_score"]
        assert 0.0 <= val <= 1.0, f"H{h} malefic_net_score={val}"


def test_karak_score_in_range():
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        val = hfv.to_dict()[f"h{h:02d}_karak_score"]
        assert -1.0 <= val <= 1.0, f"H{h} karak_score={val}"


def test_feature_count_is_132():
    """After S197: 11 features × 12 houses = 132 total."""
    from src.calculations.feature_decomp import extract_features
    cfv = extract_features(_india_chart())
    assert cfv.feature_count() == 132, f"Expected 132, got {cfv.feature_count()}"


def test_all_11_feature_names_present():
    from src.calculations.feature_decomp import extract_features
    EXPECTED = {
        "gentle_sign", "bhavesh_dignity", "dig_bala", "sav_bindus_norm",
        "kartari_score", "combust_score", "retrograde_score", "bhavesh_house_type",
        "benefic_net_score", "malefic_net_score", "karak_score",
    }
    cfv = extract_features(_india_chart())
    for h, hfv in cfv.houses.items():
        names = {rf.name for rf in hfv.features}
        assert names == EXPECTED, f"H{h}: {names ^ EXPECTED}"
