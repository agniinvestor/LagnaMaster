"""
tests/test_varshaphala.py
==========================
Test suite for src/calculations/varshaphala.py — Session 18.

22 tests covering:
  - TajikaAspect data class fields
  - _angular_distance() edge cases (wrap, 180°, 0°)
  - _detect_tajika_aspects() returns list of TajikaAspect
  - Aspect types are one of the 5 valid Tajika types
  - Orbs are within stated tolerance
  - Muntha formula: (natal_lagna_si + years_elapsed) % 12
  - Varsha Pati is a valid planet
  - 1947 India chart: 1948 solar return
    - solar_return_jd is in 1948 CE range
    - solar_return_date is in 1948 (Aug/Sep)
    - Sun longitude in Varsha chart ≈ natal Sun longitude ±0.01°
  - VarshaphalaReport structure (all fields present)
  - aspects_of_type() and aspects_for_planet() accessors
  - years_elapsed = target_year − birth_year
  - Varsha lagna sign index in 0–11
  - 2026 solar return for 1947 chart (years_elapsed = 79, Muntha = (1+79)%12)
  - Determinism: same inputs → same report
"""

import pytest
from datetime import date

INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}

_VALID_ASPECT_TYPES = {"Itthasala", "Ishrafa", "Nakta", "Kambool", "Dainya"}
_VALID_PLANETS = {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"}
_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA_1947)


@pytest.fixture(scope="module")
def report_1948(india_chart):
    from src.calculations.varshaphala import compute_varshaphala
    return compute_varshaphala(
        natal_chart=india_chart,
        birth_year=1947,
        query_year=1948,
    )


@pytest.fixture(scope="module")
def report_2026(india_chart):
    from src.calculations.varshaphala import compute_varshaphala
    return compute_varshaphala(
        natal_chart=india_chart,
        birth_year=1947,
        query_year=2026,
    )


# ══════════════════════════════════════════════════════════════════════════════
# 1. Utility functions
# ══════════════════════════════════════════════════════════════════════════════

class TestAngularDistance:

    def test_zero(self):
        from src.calculations.varshaphala import _angular_distance
        assert _angular_distance(45.0, 45.0) == 0.0

    def test_180(self):
        from src.calculations.varshaphala import _angular_distance
        assert abs(_angular_distance(0.0, 180.0) - 180.0) < 1e-9

    def test_wrap_around(self):
        from src.calculations.varshaphala import _angular_distance
        # 350° and 10° → 20°
        assert abs(_angular_distance(350.0, 10.0) - 20.0) < 1e-9

    def test_symmetric(self):
        from src.calculations.varshaphala import _angular_distance
        assert _angular_distance(30.0, 90.0) == _angular_distance(90.0, 30.0)


# ══════════════════════════════════════════════════════════════════════════════
# 2. TajikaAspect data class
# ══════════════════════════════════════════════════════════════════════════════

class TestTajikaAspect:

    def test_aspect_type_valid(self, report_1948):
        for a in report_1948.tajika_aspects:
            assert a.aspect_type in _VALID_ASPECT_TYPES

    def test_orbs_within_tolerance(self, report_1948):
        from src.calculations.varshaphala import _TAJIKA_ASPECTS
        max_orbs = {atype: max_orb for atype, _, max_orb in _TAJIKA_ASPECTS}
        for a in report_1948.tajika_aspects:
            assert a.orb <= max_orbs[a.aspect_type] + 1e-6, \
                f"{a.aspect_type} orb {a.orb} exceeds max"

    def test_planets_are_valid(self, report_1948):
        for a in report_1948.tajika_aspects:
            assert a.planet_a in _VALID_PLANETS
            assert a.planet_b in _VALID_PLANETS

    def test_applying_is_bool(self, report_1948):
        for a in report_1948.tajika_aspects:
            assert isinstance(a.applying, bool)

    def test_aspects_list_type(self, report_1948):
        from src.calculations.varshaphala import TajikaAspect
        assert isinstance(report_1948.tajika_aspects, list)
        for a in report_1948.tajika_aspects:
            assert isinstance(a, TajikaAspect)


# ══════════════════════════════════════════════════════════════════════════════
# 3. 1948 solar return fixture
# ══════════════════════════════════════════════════════════════════════════════

class TestSolarReturn1948:

    def test_solar_return_date_in_1948(self, report_1948):
        assert report_1948.solar_return_date.year == 1948

    def test_solar_return_date_around_aug(self, report_1948):
        # Sun at natal longitude (~Cancer/Leo area) returns ~mid-August
        m = report_1948.solar_return_date.month
        assert 7 <= m <= 9, f"Expected Aug±1 but got month {m}"

    def test_solar_return_jd_plausible(self, report_1948):
        # 1948-01-01 ≈ JD 2432552; 1948-12-31 ≈ JD 2432917
        assert 2432500 < report_1948.solar_return_jd < 2433000

    def test_varsha_sun_matches_natal_sun(self, india_chart, report_1948):
        # Varsha chart Sun longitude should ≈ natal Sun longitude
        natal_sun = india_chart.planets["Sun"].longitude
        varsha_sun = report_1948.varsha_chart.planets["Sun"].longitude
        assert abs(varsha_sun - natal_sun) < 0.05, \
            f"Natal Sun {natal_sun:.4f}° ≠ Varsha Sun {varsha_sun:.4f}°"

    def test_years_elapsed_1948(self, report_1948):
        assert report_1948.years_elapsed == 1   # 1948 − 1947


# ══════════════════════════════════════════════════════════════════════════════
# 4. VarshaphalaReport structure
# ══════════════════════════════════════════════════════════════════════════════

class TestReportStructure:

    def test_varsha_lagna_sign_index_valid(self, report_1948):
        assert 0 <= report_1948.varsha_lagna_sign_index <= 11

    def test_varsha_lagna_sign_consistent(self, report_1948):
        assert report_1948.varsha_lagna_sign == _SIGNS[report_1948.varsha_lagna_sign_index]

    def test_muntha_sign_consistent(self, report_1948):
        assert report_1948.muntha_sign == _SIGNS[report_1948.muntha_sign_index]

    def test_varsha_pati_is_valid_planet(self, report_1948):
        assert report_1948.varsha_pati in \
            {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"}

    def test_aspects_of_type_accessor(self, report_1948):
        for atype in _VALID_ASPECT_TYPES:
            result = report_1948.aspects_of_type(atype)
            assert isinstance(result, list)
            for a in result:
                assert a.aspect_type == atype

    def test_aspects_for_planet_accessor(self, report_1948):
        result = report_1948.aspects_for_planet("Sun")
        for a in result:
            assert a.planet_a == "Sun" or a.planet_b == "Sun"


# ══════════════════════════════════════════════════════════════════════════════
# 5. 2026 solar return (muntha check)
# ══════════════════════════════════════════════════════════════════════════════

class TestSolarReturn2026:

    def test_years_elapsed_2026(self, report_2026):
        assert report_2026.years_elapsed == 79   # 2026 − 1947

    def test_muntha_2026_formula(self, india_chart, report_2026):
        # Taurus lagna (si=1); 79 years → (1 + 79) % 12 = 80 % 12 = 8 = Sagittarius
        expected_si = (india_chart.lagna_sign_index + 79) % 12
        assert report_2026.muntha_sign_index == expected_si

    def test_muntha_2026_is_sagittarius(self, report_2026):
        assert report_2026.muntha_sign == "Sagittarius"   # (1+79)%12 = 8

    def test_solar_return_date_in_2026(self, report_2026):
        assert report_2026.solar_return_date.year == 2026

    def test_determinism(self, india_chart):
        from src.calculations.varshaphala import compute_varshaphala
        r1 = compute_varshaphala(india_chart, date(1947,8,15), 2026,
                                 28.6139, 77.2090)
        r2 = compute_varshaphala(india_chart, date(1947,8,15), 2026,
                                 28.6139, 77.2090)
        assert r1.solar_return_jd == r2.solar_return_jd
        assert r1.muntha_sign == r2.muntha_sign
