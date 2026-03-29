"""
tests/test_s195_feature_decomp.py — S195: Feature decomposition infrastructure

Verifies RuleFeature, HouseFeatureVector, ChartFeatureVector dataclasses
and the first 4 continuous extractors:
  gentle_sign      (R01)
  bhavesh_dignity  (R04 continuous)
  dig_bala         (R20)
  sav_bindus_norm  (R23 continuous)

G22: no SHAP analysis without OSF pre-registration — these features are
     infrastructure only; no statistical analysis in this module.
"""

from __future__ import annotations


INDIA_BIRTH_LAT = 28.6139
INDIA_BIRTH_LON = 77.2090
INDIA_TZ_OFFSET = 5.5


def _india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=INDIA_BIRTH_LAT, lon=INDIA_BIRTH_LON, tz_offset=INDIA_TZ_OFFSET,
    )


# ─── 1. RuleFeature dataclass ─────────────────────────────────────────────────

def test_rule_feature_fields():
    from src.calculations.feature_decomp import RuleFeature
    rf = RuleFeature(name="gentle_sign", value=1.0, rule_id="R01", house=1)
    assert rf.name == "gentle_sign"
    assert rf.value == 1.0
    assert rf.rule_id == "R01"
    assert rf.house == 1


def test_rule_feature_value_is_float():
    from src.calculations.feature_decomp import RuleFeature
    rf = RuleFeature(name="sav_bindus_norm", value=0.625, rule_id="R23", house=5)
    assert isinstance(rf.value, float)


# ─── 2. HouseFeatureVector dataclass ─────────────────────────────────────────

def test_house_feature_vector_fields():
    from src.calculations.feature_decomp import HouseFeatureVector, RuleFeature
    fv = HouseFeatureVector(
        house=1,
        features=[RuleFeature("gentle_sign", 1.0, "R01", 1)],
    )
    assert fv.house == 1
    assert len(fv.features) == 1


def test_house_feature_vector_to_dict():
    from src.calculations.feature_decomp import HouseFeatureVector, RuleFeature
    fv = HouseFeatureVector(
        house=3,
        features=[
            RuleFeature("gentle_sign", 0.0, "R01", 3),
            RuleFeature("dig_bala", 1.0, "R20", 3),
        ],
    )
    d = fv.to_dict()
    assert isinstance(d, dict)
    assert "h03_gentle_sign" in d
    assert "h03_dig_bala" in d
    assert d["h03_gentle_sign"] == 0.0


def test_house_feature_vector_to_array():
    from src.calculations.feature_decomp import HouseFeatureVector, RuleFeature
    fv = HouseFeatureVector(
        house=1,
        features=[
            RuleFeature("gentle_sign", 1.0, "R01", 1),
            RuleFeature("dig_bala", 0.0, "R20", 1),
        ],
    )
    arr = fv.to_array()
    assert isinstance(arr, list)
    assert len(arr) == 2
    assert all(isinstance(v, float) for v in arr)


# ─── 3. ChartFeatureVector dataclass ─────────────────────────────────────────

def test_chart_feature_vector_has_12_houses():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    assert set(cfv.houses.keys()) == set(range(1, 13))


def test_chart_feature_vector_to_dict_flat():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    d = cfv.to_dict()
    assert isinstance(d, dict)
    assert len(d) > 0
    # All keys should be prefixed h01_ through h12_
    for key in d:
        assert key[:1] == "h", f"Unexpected key prefix: {key}"


def test_chart_feature_vector_to_array_length():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    arr = cfv.to_array()
    assert len(arr) == cfv.feature_count()
    assert cfv.feature_count() > 0


def test_chart_feature_vector_feature_names_consistent():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    names = cfv.feature_names()
    d = cfv.to_dict()
    assert set(names) == set(d.keys()), "feature_names() must match to_dict() keys"


# ─── 4. gentle_sign extractor (R01) ──────────────────────────────────────────

def test_gentle_sign_is_binary():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    for h, hfv in cfv.houses.items():
        d = hfv.to_dict()
        key = f"h{h:02d}_gentle_sign"
        assert d[key] in (0.0, 1.0), f"gentle_sign must be 0.0 or 1.0, got {d[key]}"


# ─── 5. bhavesh_dignity extractor (continuous R04) ───────────────────────────

def test_bhavesh_dignity_in_range():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    for h, hfv in cfv.houses.items():
        d = hfv.to_dict()
        key = f"h{h:02d}_bhavesh_dignity"
        val = d[key]
        assert -1.0 <= val <= 1.0, f"H{h} bhavesh_dignity={val} out of [-1,1]"


# ─── 6. dig_bala extractor (R20) ─────────────────────────────────────────────

def test_dig_bala_is_binary():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    for h, hfv in cfv.houses.items():
        d = hfv.to_dict()
        key = f"h{h:02d}_dig_bala"
        assert d[key] in (0.0, 1.0), f"dig_bala must be 0/1, got {d[key]}"


# ─── 7. sav_bindus_norm extractor (R23 continuous) ───────────────────────────

def test_sav_bindus_norm_in_range():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    for h, hfv in cfv.houses.items():
        d = hfv.to_dict()
        key = f"h{h:02d}_sav_bindus_norm"
        val = d[key]
        assert 0.0 <= val <= 1.0, f"H{h} sav_bindus_norm={val} out of [0,1]"


# ─── 8. Feature values are all floats ────────────────────────────────────────

def test_all_feature_values_are_float():
    from src.calculations.feature_decomp import extract_features
    chart = _india_chart()
    cfv = extract_features(chart)
    for key, val in cfv.to_dict().items():
        assert isinstance(val, float), f"{key}={val!r} is not float"
