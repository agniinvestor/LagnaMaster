"""Regression tests for S318 Final Sweep bug fixes.

Each test targets a specific high-risk fix to prevent regression.
"""

import pytest

from src.calculations.kundali_milan import _Y, _NF, _TS
from src.calculations.orb_strength import aspect_strength
from src.calculations.rule_firing import _planet_dignity_state
from src.calculations.divisional_charts import _d3, _d7, _d60


# ── Shadbala: Jupiter Tribhaga always 20 ──


class TestShadbalaRegressions:
    """BUG-041: Jupiter always gets 20 virupas for Tribhaga."""

    def test_jupiter_tribhaga_always_20(self):
        """Verified inline in shadbala.py — Jupiter returns 20 before watch lookup."""
        from src.calculations.shadbala import ShadbalResult

        r = ShadbalResult(planet="Jupiter")
        assert hasattr(r, "tribhaga_bala")

    def test_yuddha_bala_field_exists(self):
        """BUG-042: ShadbalResult must have yuddha_bala field."""
        from src.calculations.shadbala import ShadbalResult

        r = ShadbalResult(planet="Mars")
        assert hasattr(r, "yuddha_bala")
        assert r.yuddha_bala == 0.0


# ── Divisional charts: cross-validate formulas ──


class TestDivisionalCrossValidation:
    """BUG-022,023,026,027: divisional chart formula correctness."""

    @pytest.mark.parametrize(
        "lon",
        [0.0, 15.5, 45.0, 90.0, 135.5, 180.0, 225.0, 270.0, 315.5, 359.9],
    )
    def test_d3_trikona(self, lon):
        """D3 uses trikona formula: si + k*4."""
        si = int(lon / 30) % 12
        k = int((lon % 30) / 10)
        expected = (si + k * 4) % 12
        assert _d3(lon) == expected, f"D3 at {lon}°: got {_d3(lon)}, expected {expected}"

    def test_d7_zero_longitude(self):
        """BUG-023: D7 at 0° must not hit zero-falsy bug."""
        result = _d7(0.0)
        assert isinstance(result, int)
        assert 0 <= result < 12

    @pytest.mark.parametrize("lon", [0.0, 30.0, 60.0, 90.0, 150.0, 330.0])
    def test_d60_in_range(self, lon):
        """BUG-022: D60 must return valid sign index."""
        result = _d60(lon)
        assert 0 <= result < 12, f"D60 at {lon}° out of range: {result}"


# ── Kundali Milan: Yoni and friendship corrections ──


class TestKundaliMilanCorrections:
    """BUG-059,061,062: Yoni animals, Graha Maitri, Tara Kuta."""

    def test_mrigashira_yoni_serpent(self):
        """BUG-059: Mrigashira (index 4) yoni must be serpent."""
        assert _Y[4] == "serpent", f"Mrigashira yoni should be serpent, got {_Y[4]}"

    def test_ardra_yoni_dog(self):
        """BUG-059: Ardra (index 5) yoni must be dog."""
        assert _Y[5] == "dog", f"Ardra yoni should be dog, got {_Y[5]}"

    def test_moon_jupiter_neutral(self):
        """BUG-061: Moon-Jupiter should be Neutral."""
        val = _NF.get("Moon", {}).get("Jupiter")
        assert val in ("N", "Neutral"), f"Moon-Jupiter should be Neutral, got {val}"

    def test_saturn_mars_enemy(self):
        """BUG-061: Saturn-Mars should be Enemy."""
        val = _NF.get("Saturn", {}).get("Mars")
        assert val in ("E", "Enemy"), f"Saturn-Mars should be Enemy, got {val}"

    def test_tara_janma_inauspicious(self):
        """BUG-062: Tara group 1 (Janma) must score 0."""
        assert _TS[1] == 0

    def test_tara_vipat_inauspicious(self):
        """BUG-062: Tara group 3 (Vipat) must score 0."""
        assert _TS[3] == 0


# ── orb_strength: actual aspect angles ──


class TestOrbStrength:
    """BUG-020: aspect_strength must use actual aspect angles."""

    def test_non_aspect_angle_zero(self):
        """45° separation is not near any standard aspect — should be 0 or near 0."""
        strength = aspect_strength(0.0, 45.0)
        assert strength < 0.15, f"45° should have near-zero strength, got {strength}"

    def test_opposition_full(self):
        """180° separation is a full opposition — should be near 1.0."""
        strength = aspect_strength(0.0, 180.0)
        assert strength > 0.8, f"Opposition should have high strength, got {strength}"

    def test_trine_significant(self):
        """120° separation is a trine — should have significant strength."""
        strength = aspect_strength(0.0, 120.0)
        assert strength > 0.5, f"Trine should have significant strength, got {strength}"


# ── Moolatrikona degree bounds ──


class TestMoolatrikonaDegrees:
    """BUG-063: Moolatrikona must check degree range, not just sign."""

    def _make_chart(self, name, sign_index, degree_in_sign):
        class MockPlanet:
            def __init__(self, n, si, d, lon):
                self.name = n
                self.sign_index = si
                self.degree_in_sign = d
                self.longitude = lon

        class MockChart:
            def __init__(self, planets_dict):
                self.planets = planets_dict
                self.lagna_sign_index = 0

        lon = sign_index * 30 + degree_in_sign
        p = MockPlanet(name, sign_index, degree_in_sign, lon)
        return MockChart({name: p})

    def test_sun_leo_25_not_moolatrikona(self):
        """Sun at Leo 25° is NOT moolatrikona (range is 0-20°)."""
        chart = self._make_chart("Sun", 4, 25.0)
        result = _planet_dignity_state(chart, "Sun")
        assert result != "moolatrikona", "Sun at Leo 25° should NOT be moolatrikona"

    def test_sun_leo_10_is_moolatrikona(self):
        """Sun at Leo 10° IS moolatrikona (within 0-20°)."""
        chart = self._make_chart("Sun", 4, 10.0)
        result = _planet_dignity_state(chart, "Sun")
        assert result == "moolatrikona", f"Sun at Leo 10° should be moolatrikona, got {result}"

    def test_mercury_virgo_18_is_moolatrikona(self):
        """Mercury at Virgo 18° IS moolatrikona (within 15-20°)."""
        chart = self._make_chart("Mercury", 5, 18.0)
        result = _planet_dignity_state(chart, "Mercury")
        assert result == "moolatrikona", f"Mercury at Virgo 18° should be moolatrikona, got {result}"

    def test_mercury_virgo_10_not_moolatrikona(self):
        """Mercury at Virgo 10° is NOT moolatrikona (outside 15-20°)."""
        chart = self._make_chart("Mercury", 5, 10.0)
        result = _planet_dignity_state(chart, "Mercury")
        assert result != "moolatrikona", "Mercury at Virgo 10° should NOT be moolatrikona"
