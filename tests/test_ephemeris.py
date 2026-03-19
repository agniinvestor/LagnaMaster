"""
tests/test_ephemeris.py
=======================
Regression tests for src/ephemeris.py.

Run:  pytest tests/test_ephemeris.py -v
"""

import pytest
from src.ephemeris import compute_chart, BirthChart
from tests.fixtures import INDIA_1947


class TestIndia1947:
    """Primary regression fixture: 1947 India Independence Chart."""

    TOL = 0.05  # degrees tolerance (≈ 3 arcminutes)

    @pytest.fixture(scope="class")
    def chart(self) -> BirthChart:
        f = INDIA_1947
        return compute_chart(
            year=f["year"], month=f["month"], day=f["day"],
            hour=f["hour"], lat=f["lat"], lon=f["lon"],
            tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
        )

    def test_lagna_sign(self, chart):
        assert chart.lagna_sign == "Taurus", (
            f"Lagna sign: expected Taurus, got {chart.lagna_sign}"
        )

    def test_lagna_degree(self, chart):
        expected = INDIA_1947["lagna_degree_in_sign"]
        actual = chart.lagna_degree_in_sign
        assert abs(actual - expected) < self.TOL, (
            f"Lagna degree: expected {expected:.4f}°, got {actual:.4f}° "
            f"(diff={abs(actual-expected):.4f}°, tol={self.TOL}°)"
        )

    def test_sun_sign(self, chart):
        sun = chart.planet("Sun")
        assert sun.sign == "Cancer", (
            f"Sun sign: expected Cancer, got {sun.sign}"
        )

    def test_sun_degree(self, chart):
        sun = chart.planet("Sun")
        expected = INDIA_1947["planets"]["Sun"]["degree"]
        actual = sun.degree_in_sign
        assert abs(actual - expected) < self.TOL, (
            f"Sun degree: expected {expected:.3f}°, got {actual:.4f}° "
            f"(diff={abs(actual-expected):.4f}°)"
        )

    def test_all_planet_signs(self, chart):
        """Check that all 9 planets land in the correct sign."""
        for planet_name, expected in INDIA_1947["planets"].items():
            actual_sign = chart.planet(planet_name).sign
            assert actual_sign == expected["sign"], (
                f"{planet_name}: expected {expected['sign']}, got {actual_sign}"
            )

    def test_ayanamsha_range(self, chart):
        """Lahiri ayanamsha in 1947 should be ~23.1–23.2°."""
        assert 23.0 < chart.ayanamsha_value < 23.3, (
            f"Ayanamsha out of expected range: {chart.ayanamsha_value:.4f}°"
        )

    def test_ketu_opposite_rahu(self, chart):
        rahu_lon = chart.planet("Rahu").longitude
        ketu_lon = chart.planet("Ketu").longitude
        diff = abs((rahu_lon - ketu_lon) % 360)
        assert abs(diff - 180.0) < 0.001, (
            f"Ketu should be exactly 180° from Rahu; diff={diff:.4f}°"
        )

    def test_all_longitudes_in_range(self, chart):
        assert 0 <= chart.lagna < 360
        for p in chart.planets.values():
            assert 0 <= p.longitude < 360, (
                f"{p.name} longitude out of range: {p.longitude}"
            )


class TestInputValidation:
    """Bug-fix regression: P-1 midnight, P-4 ayanamsha."""

    def test_midnight_birth_p1(self):
        """P-1: hour=0.0 (midnight) must not be treated as falsy."""
        chart = compute_chart(
            year=1947, month=8, day=15,
            hour=0.0,   # midnight — this was the bug
            lat=28.6139, lon=77.2090, tz_offset=5.5,
        )
        assert chart.lagna_sign == "Taurus", (
            "Midnight birth (hour=0.0) produced wrong lagna — P-1 bug may be present"
        )

    def test_none_hour_treated_as_midnight(self):
        """hour=None should be treated as 0.0, not crash."""
        chart = compute_chart(
            year=1947, month=8, day=15,
            hour=None,
            lat=28.6139, lon=77.2090, tz_offset=5.5,
        )
        assert chart.lagna_sign == "Taurus"

    def test_invalid_ayanamsha_raises_p4(self):
        """P-4: unknown ayanamsha must raise ValueError, not silently pass."""
        with pytest.raises(ValueError, match="Unknown ayanamsha"):
            compute_chart(
                year=2000, month=1, day=1, hour=12.0,
                lat=28.6, lon=77.2, ayanamsha="invalid_system",
            )

    def test_lahiri_ayanamsha_accepted(self):
        """Lahiri is a supported ayanamsha — must not raise."""
        chart = compute_chart(
            year=2000, month=1, day=1, hour=12.0,
            lat=28.6, lon=77.2, ayanamsha="lahiri",
        )
        assert chart.ayanamsha_name == "lahiri"


class TestChart2000:
    """Sanity check: J2000 epoch, known positions."""

    def test_nine_planets_present(self):
        chart = compute_chart(
            year=2000, month=1, day=1, hour=12.0,
            lat=28.6139, lon=77.2090, tz_offset=5.5,
        )
        expected_planets = {
            "Sun", "Moon", "Mars", "Mercury", "Jupiter",
            "Venus", "Saturn", "Rahu", "Ketu",
        }
        assert set(chart.planets.keys()) == expected_planets

    def test_retrograde_flag_is_bool(self):
        chart = compute_chart(
            year=2000, month=1, day=1, hour=12.0,
            lat=28.6139, lon=77.2090, tz_offset=5.5,
        )
        for p in chart.planets.values():
            assert isinstance(p.is_retrograde, bool)
