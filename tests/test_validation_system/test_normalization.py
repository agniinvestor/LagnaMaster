"""Tests for the normalization layer — proves the watchers work."""
import math

import pytest

from tools.normalize_outputs import (
    normalize_longitude,
    normalize_sign,
    normalize_nakshatra,
    normalize_house_index,
    normalize_chart_output,
)


# --- Longitude wrapping ---

class TestNormalizeLongitude:
    def test_normal_value(self):
        assert normalize_longitude(180.0) == 180.0

    def test_wrap_above_360(self):
        assert normalize_longitude(361.0) == pytest.approx(1.0)

    def test_wrap_negative(self):
        assert normalize_longitude(-1.0) == pytest.approx(359.0)

    def test_zero(self):
        assert normalize_longitude(0.0) == 0.0

    def test_exact_360_wraps_to_0(self):
        assert normalize_longitude(360.0) == 0.0

    def test_large_value(self):
        assert normalize_longitude(725.5) == pytest.approx(5.5)

    def test_nan_raises(self):
        with pytest.raises(ValueError, match="NaN"):
            normalize_longitude(math.nan)


# --- Sign normalization ---

class TestNormalizeSign:
    def test_canonical_name(self):
        assert normalize_sign("Aries") == "Aries"

    def test_lowercase(self):
        assert normalize_sign("aries") == "Aries"

    def test_index_to_name(self):
        assert normalize_sign(0) == "Aries"
        assert normalize_sign(11) == "Pisces"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            normalize_sign("NotASign")

    def test_index_out_of_range_raises(self):
        with pytest.raises(ValueError):
            normalize_sign(12)


# --- Nakshatra normalization ---

class TestNormalizeNakshatra:
    def test_canonical(self):
        assert normalize_nakshatra("Ashwini") == "Ashwini"

    def test_variant_spelling(self):
        assert normalize_nakshatra("Ashvini") == "Ashwini"

    def test_pushya(self):
        assert normalize_nakshatra("Pushya") == "Pushya"
        assert normalize_nakshatra("Pushyami") == "Pushya"

    def test_index(self):
        assert normalize_nakshatra(0) == "Ashwini"
        assert normalize_nakshatra(26) == "Revati"


# --- House index normalization ---

class TestNormalizeHouseIndex:
    def test_already_1_indexed(self):
        assert normalize_house_index(1) == 1
        assert normalize_house_index(12) == 12

    def test_0_indexed_converts(self):
        assert normalize_house_index(0, zero_indexed=True) == 1
        assert normalize_house_index(11, zero_indexed=True) == 12

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            normalize_house_index(13)

    def test_zero_without_flag_raises(self):
        with pytest.raises(ValueError):
            normalize_house_index(0)


# --- Chart output normalization ---

class TestNormalizeChartOutput:
    def test_empty_chart(self):
        result = normalize_chart_output({}, source="lm")
        assert result.get("planets") == {}

    def test_basic_chart(self):
        data = {
            "lagna_degree": 370.5,
            "lagna_sign": "aries",
            "planets": {
                "Sun": {"longitude": 100.0, "sign": "Cancer"},
            },
        }
        result = normalize_chart_output(data, source="lm")
        assert result["lagna_degree"] == pytest.approx(10.5)
        assert result["lagna_sign"] == "Aries"
        assert result["planets"]["Sun"]["longitude"] == 100.0
        assert result["planets"]["Sun"]["sign"] == "Cancer"
