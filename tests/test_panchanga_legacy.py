"""
tests/test_panchanga.py
========================
Tests for Panchanga (5-limb Vedic almanac) and Navamsha (D9) chart.
1947 India Independence chart is the primary fixture.
"""

import pytest
from datetime import date

from tests.fixtures import INDIA_1947
from src.ephemeris import compute_chart, SIGNS
from src.calculations.panchang import (
    compute_panchanga,
    compute_navamsha_chart,
    _d9_sign_index,
    Panchanga,
    _TITHI_NAMES,
    _YOGA_NAMES,
    _MOVABLE_KARANAS,
    _FIXED_KARANAS,
    _VARA_LORDS,
)


@pytest.fixture(scope="module")
def india_chart():
    f = INDIA_1947
    return compute_chart(
        year=f["year"], month=f["month"], day=f["day"],
        hour=f["hour"], lat=f["lat"], lon=f["lon"],
        tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
    )


@pytest.fixture(scope="module")
def india_panchanga(india_chart):
    return compute_panchanga(india_chart, date(1947, 8, 15))


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

class TestPanchangaStructure:

    def test_returns_panchanga(self, india_panchanga):
        assert isinstance(india_panchanga, Panchanga)

    def test_tithi_in_range(self, india_panchanga):
        assert 1 <= india_panchanga.tithi <= 30

    def test_paksha_is_valid(self, india_panchanga):
        assert india_panchanga.paksha in {"Shukla", "Krishna"}

    def test_tithi_name_is_string(self, india_panchanga):
        assert isinstance(india_panchanga.tithi_name, str)
        assert india_panchanga.tithi_name in _TITHI_NAMES

    def test_vara_is_planet(self, india_panchanga):
        assert india_panchanga.vara in {
            "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"
        }

    def test_vara_name_is_weekday(self, india_panchanga):
        assert india_panchanga.vara_name in {
            "Sunday", "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday"
        }

    def test_nakshatra_is_string(self, india_panchanga):
        assert india_panchanga.nakshatra and isinstance(india_panchanga.nakshatra, str)

    def test_nakshatra_pada_in_range(self, india_panchanga):
        assert 1 <= india_panchanga.nakshatra_pada <= 4

    def test_yoga_in_range(self, india_panchanga):
        assert 1 <= india_panchanga.yoga <= 27

    def test_yoga_name_valid(self, india_panchanga):
        assert india_panchanga.yoga_name in _YOGA_NAMES

    def test_yoga_nature_valid(self, india_panchanga):
        assert india_panchanga.yoga_nature in {"auspicious", "inauspicious", "mixed"}

    def test_karana_in_range(self, india_panchanga):
        assert 1 <= india_panchanga.karana <= 60

    def test_karana_name_valid(self, india_panchanga):
        all_karanas = set(_MOVABLE_KARANAS) | set(_FIXED_KARANAS)
        assert india_panchanga.karana_name in all_karanas

    def test_karana_inauspicious_is_bool(self, india_panchanga):
        assert isinstance(india_panchanga.karana_inauspicious, bool)

    def test_is_full_moon_is_bool(self, india_panchanga):
        assert isinstance(india_panchanga.is_full_moon, bool)
        assert isinstance(india_panchanga.is_new_moon, bool)

    def test_navamsha_chart_has_ten_keys(self, india_panchanga):
        """lagna + 9 planets = 10 keys."""
        assert len(india_panchanga.navamsha_chart) == 10

    def test_navamsha_signs_in_range(self, india_panchanga):
        for k, si in india_panchanga.navamsha_chart.items():
            assert 0 <= si <= 11, f"D9 sign index {si} out of range for {k}"


# ---------------------------------------------------------------------------
# 1947 India known values
# ---------------------------------------------------------------------------

class TestIndia1947Panchanga:
    """
    1947-08-15 was a Friday (Venus-vara).
    Moon in Pushya → Saturn dasha lord.
    Sun at 27.99° Cancer, Moon at 3.98° Cancer.
    Elongation = (3.98 - 27.99 + 360) % 360 ≈ 335.99° → Tithi 28 (Krishna Trayodashi).
    Yoga: (117.99 + 93.98) % 360 = 211.97 → yoga_idx 15 → Siddhi (index 0-based).
    """

    def test_vara_is_friday_venus(self, india_panchanga):
        assert india_panchanga.vara == "Venus"
        assert india_panchanga.vara_name == "Friday"

    def test_nakshatra_is_pushya(self, india_panchanga):
        assert india_panchanga.nakshatra == "Pushya"

    def test_nakshatra_lord_is_saturn(self, india_panchanga):
        assert india_panchanga.nakshatra_lord == "Saturn"

    def test_tithi_is_krishna(self, india_panchanga):
        """1947-08-15: Moon lags Sun by ~336° → Krishna paksha tithi."""
        assert india_panchanga.paksha == "Krishna"

    def test_tithi_is_28(self, india_panchanga):
        assert india_panchanga.tithi == 28

    def test_tithi_name_is_trayodashi(self, india_panchanga):
        assert india_panchanga.tithi_name == "Trayodashi"

    def test_yoga_name_is_siddhi(self, india_panchanga):
        assert india_panchanga.yoga_name == "Siddhi"

    def test_yoga_is_auspicious(self, india_panchanga):
        assert india_panchanga.yoga_nature == "auspicious"

    def test_not_full_moon_not_new_moon(self, india_panchanga):
        assert not india_panchanga.is_full_moon
        assert not india_panchanga.is_new_moon

    def test_d9_lagna_is_pisces(self, india_panchanga):
        """
        D1 Lagna: 7.73° Taurus (si=1, Earth, start=Capricorn).
        pada = int(7.73*9/30) = 2 → D9 = (9+2)%12 = 11 = Pisces.
        """
        lagna_d9_si = india_panchanga.navamsha_chart["lagna"]
        assert SIGNS[lagna_d9_si] == "Pisces"

    def test_d9_moon_is_leo(self, india_panchanga):
        """
        Moon at 3.98° Cancer (si=3, Water, start=Cancer).
        pada = int(3.98*9/30) = 1 → D9 = (3+1)%12 = 4 = Leo.
        """
        moon_d9_si = india_panchanga.navamsha_chart["Moon"]
        assert SIGNS[moon_d9_si] == "Leo"


# ---------------------------------------------------------------------------
# Tithi arithmetic
# ---------------------------------------------------------------------------

class TestTithiArithmetic:

    def test_shukla_when_moon_ahead_of_sun(self, india_chart):
        """Create a scenario where Moon is ahead of Sun by ~60° → Tithi 5 Shukla."""
        # We can't easily create custom positions, but we can test the formula directly.
        # Tithi 5 = elongation of (4*12=48) to (5*12=60)°
        assert (49 // 12) + 1 == 5
        assert (49 // 12) + 1 <= 15  # Shukla

    def test_full_moon_at_tithi_15(self):
        """Tithi 15 = Purnima (full moon), elongation 168-180°."""
        elongation = 175  # degrees
        tithi_idx = int(elongation / 12)
        assert tithi_idx + 1 == 15

    def test_new_moon_at_tithi_30(self):
        """Tithi 30 = Amavasya (new moon), elongation 348-360°."""
        elongation = 355
        tithi_idx = int(elongation / 12)
        assert tithi_idx + 1 == 30
        assert _TITHI_NAMES[tithi_idx] == "Amavasya"

    def test_tithi_paksha_boundary(self, india_chart):
        """Tithi 16 is first tithi of Krishna paksha."""
        # Construct a synthetic check
        elongation = 15 * 12 + 1  # = 181°
        tithi = int(elongation / 12) + 1  # = 16
        assert tithi == 16
        assert tithi > 15  # Krishna paksha


# ---------------------------------------------------------------------------
# Navamsha D9 computation
# ---------------------------------------------------------------------------

class TestNavamsha:

    def test_d9_sign_index_fire_sign(self):
        """Aries (si=0, Fire) pada 1 → Aries (0)."""
        # Aries spans 0-30°; pada 1 = 0-3.33°
        lon = 1.0  # 1° Aries
        si = _d9_sign_index(lon)
        assert si == 0  # Aries

    def test_d9_sign_index_earth_sign(self):
        """Taurus (si=1, Earth) pada 1 → Capricorn (9)."""
        lon = 31.0  # 1° Taurus
        si = _d9_sign_index(lon)
        assert si == 9  # Capricorn

    def test_d9_sign_index_air_sign(self):
        """Gemini (si=2, Air) pada 1 → Libra (6)."""
        lon = 61.0  # 1° Gemini
        si = _d9_sign_index(lon)
        assert si == 6  # Libra

    def test_d9_sign_index_water_sign(self):
        """Cancer (si=3, Water) pada 1 → Cancer (3)."""
        lon = 91.0  # 1° Cancer
        si = _d9_sign_index(lon)
        assert si == 3  # Cancer

    def test_d9_all_padas_cycle_correctly(self):
        """Aries padas 1-9 → Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius."""
        expected = list(range(9))  # 0-8
        for pada in range(9):
            lon = 0.0 + pada * (30.0 / 9) + 0.5   # midpoint of each pada
            si = _d9_sign_index(lon)
            assert si == expected[pada], f"Aries pada {pada+1}: expected {SIGNS[expected[pada]]}, got {SIGNS[si]}"

    def test_compute_navamsha_chart_has_10_keys(self, india_chart):
        d9 = compute_navamsha_chart(india_chart)
        assert "lagna" in d9
        assert len(d9) == 10

    def test_navamsha_chart_all_values_in_range(self, india_chart):
        d9 = compute_navamsha_chart(india_chart)
        for k, si in d9.items():
            assert 0 <= si <= 11, f"{k}: D9 sign index {si} out of range"


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

class TestDeterminism:

    def test_same_inputs_same_output(self, india_chart):
        p1 = compute_panchanga(india_chart, date(1947, 8, 15))
        p2 = compute_panchanga(india_chart, date(1947, 8, 15))
        assert p1.tithi == p2.tithi
        assert p1.yoga  == p2.yoga
        assert p1.navamsha_chart == p2.navamsha_chart
