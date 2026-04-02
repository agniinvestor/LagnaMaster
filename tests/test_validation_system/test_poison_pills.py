"""Poison pill tests — deliberately bad inputs that must be caught."""
import math

import pytest

from tools.diff_engine_core import diff_charts, diff_field
from tools.normalize_outputs import normalize_chart_output, normalize_longitude


class TestPoisonLongitude:
    def test_999_degree_normalization(self):
        """999° must normalize to 279°, not silently pass."""
        result = normalize_longitude(999.0)
        assert result == pytest.approx(279.0)

    def test_nan_longitude_diff_flags(self):
        v = diff_field("lagna", math.nan, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status != "agreement"

    def test_none_value_diff_flags(self):
        v = diff_field("lagna", None, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status != "agreement"
        assert "missing" in (v.note or "")


class TestPoisonMissingField:
    def test_field_in_one_engine_only(self):
        lm = {"lagna_degree": 100.0}
        pjh = {"lagna_degree": 100.0, "extra_field": 50.0}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "extra_field": {"field_type": "longitude", "tolerance": 0.1},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert verdicts["extra_field"].status != "agreement"


class TestPoisonNormalization:
    def test_empty_chart_no_crash(self):
        """normalize_chart_output on empty dict should not crash."""
        result = normalize_chart_output({}, source="lm")
        assert result.get("planets") == {}
