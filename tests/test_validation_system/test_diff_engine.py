"""Tests for the diff engine — proves diffing detects real differences."""
import math

import pytest

from tools.diff_engine_core import (
    _circular_diff,
    diff_charts,
    diff_field,
    validate_schema,
)


class TestCircularDiff:
    def test_normal_diff(self):
        assert _circular_diff(100, 102) == pytest.approx(2.0)

    def test_wrap_around_boundary(self):
        assert _circular_diff(359, 1) == pytest.approx(2.0)

    def test_wrap_around_large(self):
        assert _circular_diff(1, 359) == pytest.approx(2.0)

    def test_identical(self):
        assert _circular_diff(180, 180) == pytest.approx(0.0)

    def test_opposite(self):
        assert _circular_diff(0, 180) == pytest.approx(180.0)


class TestSchemaValidation:
    def test_longitude_requires_tolerance(self):
        with pytest.raises(ValueError, match="tolerance"):
            validate_schema({"f": {"field_type": "longitude"}})

    def test_degree_requires_tolerance(self):
        with pytest.raises(ValueError, match="tolerance"):
            validate_schema({"f": {"field_type": "degree"}})

    def test_valid_schema_passes(self):
        validate_schema({"f": {"field_type": "longitude", "tolerance": 0.1}})
        validate_schema({"g": {"field_type": "categorical"}})

    def test_missing_field_type_raises(self):
        with pytest.raises(ValueError, match="field_type"):
            validate_schema({"f": {"tolerance": 0.1}})


class TestDiffField:
    def test_identical_longitude_agrees(self):
        v = diff_field("lagna_degree", 100.5, 100.5, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"
        assert v.diff == pytest.approx(0.0)

    def test_within_tolerance_agrees(self):
        v = diff_field("lagna_degree", 100.5, 100.55, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"

    def test_at_tolerance_boundary_agrees(self):
        v = diff_field("lagna_degree", 100.0, 100.1, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"

    def test_beyond_tolerance_disagrees(self):
        v = diff_field("lagna_degree", 100.0, 100.2, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "unclassified_disagreement"

    def test_wrap_around_agrees(self):
        v = diff_field("lagna_degree", 359.95, 0.03, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"
        assert v.diff == pytest.approx(0.08)

    def test_categorical_match(self):
        v = diff_field("moon_nakshatra", "Pushya", "Pushya",
                       field_type="categorical")
        assert v.status == "agreement"

    def test_categorical_mismatch(self):
        v = diff_field("moon_nakshatra", "Pushya", "Ashlesha",
                       field_type="categorical")
        assert v.status == "unclassified_disagreement"

    def test_integer_exact_match(self):
        v = diff_field("av_sun_aries", 4, 4, field_type="integer")
        assert v.status == "agreement"

    def test_integer_mismatch(self):
        v = diff_field("av_sun_aries", 4, 5, field_type="integer")
        assert v.status == "unclassified_disagreement"

    def test_nan_lm_value_flags(self):
        v = diff_field("lagna_degree", math.nan, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status == "unclassified_disagreement"

    def test_missing_field_flags(self):
        v = diff_field("lagna_degree", None, 100.0, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "unclassified_disagreement"
        assert "missing" in (v.note or "")


class TestDiffCharts:
    def test_fully_identical(self):
        lm = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        pjh = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "lagna_sign": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert all(v.status == "agreement" for v in verdicts.values())

    def test_mixed_verdicts(self):
        lm = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        pjh = {"lagna_degree": 105.0, "lagna_sign": "Cancer"}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "lagna_sign": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert verdicts["lagna_degree"].status == "unclassified_disagreement"
        assert verdicts["lagna_sign"].status == "agreement"

    def test_summary_counts(self):
        lm = {"a": 1.0, "b": 2.0, "c": "X"}
        pjh = {"a": 1.0, "b": 9.0, "c": "X"}
        schema = {
            "a": {"field_type": "longitude", "tolerance": 0.1},
            "b": {"field_type": "longitude", "tolerance": 0.1},
            "c": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        agreement = sum(1 for v in verdicts.values() if v.status == "agreement")
        assert agreement == 2
