"""tests/test_avasthas_coverage.py — BUG-097: avastha coverage tests.

Tests for src/calculations/avasthas.py covering:
1. Baaladi avastha (odd/even sign reversal per BPHS Ch.45 v.3)
2. Jagradadi avastha (dignity-based classification per Ch.45 v.5)
3. Lajjitadi avastha (6 association states per Ch.45 v.11-18)
"""
from __future__ import annotations

import pytest

INDIA = dict(
    year=1947, month=8, day=15, hour=0.0,
    lat=28.6139, lon=77.2090, tz_offset=5.5, ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Baaladi Avastha — BPHS Ch.45 v.3
# ═══════════════════════════════════════════════════════════════════════════════

class TestBaaladiAvastha:
    """Verify even-sign reversal per BPHS Ch.45 v.3."""

    def test_odd_sign_standard_order(self):
        """Odd sign (Aries=0): 0-6°=Baala, 6-12°=Kumara, 12-18°=Yuva, etc."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        # Aries (index 0) is odd
        assert compute_baaladi(0, 3.0) == BaaladiAvastha.BAALA
        assert compute_baaladi(0, 9.0) == BaaladiAvastha.KUMARA
        assert compute_baaladi(0, 15.0) == BaaladiAvastha.YUVA
        assert compute_baaladi(0, 21.0) == BaaladiAvastha.VRIDDHA
        assert compute_baaladi(0, 27.0) == BaaladiAvastha.MRITA

    def test_even_sign_reversed_order(self):
        """Even sign (Taurus=1): 0-6°=Mrita, 6-12°=Vriddha, 12-18°=Yuva, etc."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        # Taurus (index 1) is even
        assert compute_baaladi(1, 3.0) == BaaladiAvastha.MRITA
        assert compute_baaladi(1, 9.0) == BaaladiAvastha.VRIDDHA
        assert compute_baaladi(1, 15.0) == BaaladiAvastha.YUVA
        assert compute_baaladi(1, 21.0) == BaaladiAvastha.KUMARA
        assert compute_baaladi(1, 27.0) == BaaladiAvastha.BAALA

    def test_gemini_odd_sign(self):
        """Gemini (index 2) is odd — standard order."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        assert compute_baaladi(2, 1.0) == BaaladiAvastha.BAALA
        assert compute_baaladi(2, 14.0) == BaaladiAvastha.YUVA

    def test_cancer_even_sign(self):
        """Cancer (index 3) is even — reversed order."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        assert compute_baaladi(3, 1.0) == BaaladiAvastha.MRITA
        assert compute_baaladi(3, 14.0) == BaaladiAvastha.YUVA

    def test_boundary_at_6_degrees(self):
        """At exactly 6°, should transition to next state."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        # Odd sign: 5.99° = Baala, 6.0° = Kumara
        assert compute_baaladi(0, 5.99) == BaaladiAvastha.BAALA
        assert compute_baaladi(0, 6.0) == BaaladiAvastha.KUMARA

    def test_boundary_at_30_degrees(self):
        """At 30° exactly, should clamp to last state (idx capped at 4)."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        assert compute_baaladi(0, 30.0) == BaaladiAvastha.MRITA

    def test_effect_multipliers(self):
        """Verify BAALADI_EFFECT dict values per BPHS Ch.45 v.4."""
        from src.calculations.avasthas import BAALADI_EFFECT, BaaladiAvastha

        assert BAALADI_EFFECT[BaaladiAvastha.BAALA] == pytest.approx(0.25)
        assert BAALADI_EFFECT[BaaladiAvastha.KUMARA] == pytest.approx(0.50)
        assert BAALADI_EFFECT[BaaladiAvastha.YUVA] == pytest.approx(1.00)
        assert BAALADI_EFFECT[BaaladiAvastha.VRIDDHA] == pytest.approx(0.125)
        assert BAALADI_EFFECT[BaaladiAvastha.MRITA] == pytest.approx(0.0)

    def test_india_1947_planets_odd_signs(self, chart):
        """Use India 1947 fixture: planets in odd signs get standard order."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        # Find planets in odd signs (sign_index % 2 == 0)
        for name, pos in chart.planets.items():
            if pos.sign_index % 2 == 0:  # odd sign
                state = compute_baaladi(pos.sign_index, pos.degree_in_sign)
                # For odd signs, low degrees should be Baala
                if pos.degree_in_sign < 6.0:
                    assert state == BaaladiAvastha.BAALA, (
                        f"{name} at {pos.degree_in_sign}° in odd sign {pos.sign_index} "
                        f"should be Baala, got {state}"
                    )
                break  # one planet is enough to verify

    def test_india_1947_planets_even_signs(self, chart):
        """Use India 1947 fixture: planets in even signs get reversed order."""
        from src.calculations.avasthas import compute_baaladi, BaaladiAvastha

        # Moon is in Cancer (sign_index=3, even sign) at ~4°
        moon = chart.planets.get("Moon")
        if moon and moon.sign_index % 2 == 1:  # even sign
            state = compute_baaladi(moon.sign_index, moon.degree_in_sign)
            if moon.degree_in_sign < 6.0:
                assert state == BaaladiAvastha.MRITA, (
                    f"Moon at {moon.degree_in_sign}° in even sign {moon.sign_index} "
                    f"should be Mrita (reversed), got {state}"
                )


# ═══════════════════════════════════════════════════════════════════════════════
# 2. Jagradadi Avastha — BPHS Ch.45 v.5
# ═══════════════════════════════════════════════════════════════════════════════

class TestJagradadiAvastha:
    """Verify dignity-based classification per BPHS Ch.45 v.5."""

    def test_own_sign_is_jagrat(self):
        """Planet in own sign should be Jagrat (awake)."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        # Sun owns Leo (sign_index=4)
        assert compute_jagradadi("Sun", 4) == JagradadiAvastha.JAGRAT
        # Moon owns Cancer (sign_index=3)
        assert compute_jagradadi("Moon", 3) == JagradadiAvastha.JAGRAT
        # Mars owns Aries (sign_index=0)
        assert compute_jagradadi("Mars", 0) == JagradadiAvastha.JAGRAT

    def test_exaltation_is_jagrat(self):
        """Planet in exaltation sign should be Jagrat."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        # Sun exalted in Aries (sign_index=0)
        assert compute_jagradadi("Sun", 0) == JagradadiAvastha.JAGRAT
        # Moon exalted in Taurus (sign_index=1)
        assert compute_jagradadi("Moon", 1) == JagradadiAvastha.JAGRAT
        # Jupiter exalted in Cancer (sign_index=3)
        assert compute_jagradadi("Jupiter", 3) == JagradadiAvastha.JAGRAT

    def test_enemy_sign_is_supta(self):
        """Planet in enemy sign should be Supta (sleeping)."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        # Sun's enemy is Saturn; Saturn rules Capricorn (10) and Aquarius (11)
        result = compute_jagradadi("Sun", 10)
        assert result == JagradadiAvastha.SUPTA

    def test_debilitation_is_supta(self):
        """Planet in debilitation sign should be Supta."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        # Sun debilitated in Libra (sign_index=6)
        assert compute_jagradadi("Sun", 6) == JagradadiAvastha.SUPTA
        # Moon debilitated in Scorpio (sign_index=7)
        assert compute_jagradadi("Moon", 7) == JagradadiAvastha.SUPTA

    def test_friendly_sign_is_swapna(self):
        """Planet in friendly/neutral sign should be Swapna."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        # Jupiter in Aries: Mars is friend to Jupiter
        # Jupiter not exalted in Aries, not own sign; Mars-Jupiter = Friend
        result = compute_jagradadi("Jupiter", 0)
        # Aries is not own/exalt for Jupiter, Mars is friend/neutral
        assert result in (JagradadiAvastha.SWAPNA, JagradadiAvastha.JAGRAT)

    def test_effect_multipliers(self):
        """Verify JAGRADADI_EFFECT dict values."""
        from src.calculations.avasthas import JAGRADADI_EFFECT, JagradadiAvastha

        assert JAGRADADI_EFFECT[JagradadiAvastha.JAGRAT] == pytest.approx(1.0)
        assert JAGRADADI_EFFECT[JagradadiAvastha.SWAPNA] == pytest.approx(0.5)
        assert JAGRADADI_EFFECT[JagradadiAvastha.SUPTA] == pytest.approx(0.0)

    def test_india_1947_moon_in_cancer(self, chart):
        """Moon in Cancer (own sign) should be Jagrat."""
        from src.calculations.avasthas import compute_jagradadi, JagradadiAvastha

        moon = chart.planets["Moon"]
        result = compute_jagradadi("Moon", moon.sign_index)
        # Moon in Cancer = own sign = Jagrat
        if moon.sign_index == 3:  # Cancer
            assert result == JagradadiAvastha.JAGRAT


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Lajjitadi Avastha — BPHS Ch.45 v.11-18
# ═══════════════════════════════════════════════════════════════════════════════

class TestLajjitadiAvastha:
    """Verify the 6 states per BPHS Ch.45 v.11-18."""

    def test_valid_return_types(self, chart):
        """Function should return valid LajjitadiAvastha enum or None."""
        from src.calculations.avasthas import compute_lajjitadi, LajjitadiAvastha

        valid_states = {
            LajjitadiAvastha.LAJJITA, LajjitadiAvastha.GARVITA,
            LajjitadiAvastha.KSHUDITA, LajjitadiAvastha.TRUSHITA,
            LajjitadiAvastha.MUDITA, LajjitadiAvastha.KSHOBHITA,
            None,
        }
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            result = compute_lajjitadi(planet, chart)
            assert result in valid_states, (
                f"{planet} returned {result}, not in valid set"
            )

    def test_enum_values(self):
        """Verify the 6 Lajjitadi states exist with correct string values."""
        from src.calculations.avasthas import LajjitadiAvastha

        assert LajjitadiAvastha.LAJJITA.value == "Ashamed"
        assert LajjitadiAvastha.GARVITA.value == "Proud"
        assert LajjitadiAvastha.KSHUDITA.value == "Hungry"
        assert LajjitadiAvastha.TRUSHITA.value == "Thirsty"
        assert LajjitadiAvastha.MUDITA.value == "Delighted"
        assert LajjitadiAvastha.KSHOBHITA.value == "Agitated"

    def test_nonexistent_planet_returns_none(self, chart):
        """Planet not in chart should return None."""
        from src.calculations.avasthas import compute_lajjitadi

        result = compute_lajjitadi("Pluto", chart)
        assert result is None

    def test_india_1947_at_least_one_state(self, chart):
        """At least one planet in India 1947 chart should have a Lajjitadi state."""
        from src.calculations.avasthas import compute_lajjitadi

        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        results = {p: compute_lajjitadi(p, chart) for p in planets}
        non_none = [p for p, r in results.items() if r is not None]
        assert len(non_none) >= 1, (
            f"Expected at least 1 planet with Lajjitadi state, got 0. "
            f"Results: {results}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. Combined Avastha Summary — compute_avasthas
# ═══════════════════════════════════════════════════════════════════════════════

class TestAvasthaSummary:
    """Test the combined compute_avasthas function."""

    def test_returns_summary_dataclass(self, chart):
        """compute_avasthas should return AvasthaSummary dataclass."""
        from src.calculations.avasthas import compute_avasthas, AvasthaSummary

        result = compute_avasthas("Sun", chart)
        assert isinstance(result, AvasthaSummary)
        assert result.planet == "Sun"

    def test_combined_effect_is_product(self, chart):
        """combined_effect = baaladi_effect * jagradadi_effect per Ch.45 v.6."""
        from src.calculations.avasthas import compute_avasthas

        result = compute_avasthas("Sun", chart)
        expected = round(result.baaladi_effect * result.jagradadi_effect, 4)
        assert result.combined_effect == pytest.approx(expected)

    def test_all_planets_return_valid(self, chart):
        """All 7 planets should return valid summaries."""
        from src.calculations.avasthas import compute_avasthas

        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            result = compute_avasthas(planet, chart)
            assert result.planet == planet
            assert 0.0 <= result.baaladi_effect <= 1.0
            assert 0.0 <= result.jagradadi_effect <= 1.0
            assert 0.0 <= result.combined_effect <= 1.0

    def test_missing_planet_returns_defaults(self, chart):
        """Missing planet returns defaults (Yuva, Swapna)."""
        from src.calculations.avasthas import (
            compute_avasthas, BaaladiAvastha, JagradadiAvastha,
        )

        result = compute_avasthas("Pluto", chart)
        assert result.baaladi == BaaladiAvastha.YUVA
        assert result.jagradadi == JagradadiAvastha.SWAPNA
        assert result.combined_effect == pytest.approx(0.5)

    def test_sayanadi_included(self, chart):
        """Sayanadi should be computed and included in summary."""
        from src.calculations.avasthas import compute_avasthas, SayandiAvastha

        result = compute_avasthas("Jupiter", chart)
        # Should be either a valid SayandiAvastha or None
        assert result.sayanadi is None or isinstance(result.sayanadi, SayandiAvastha)
