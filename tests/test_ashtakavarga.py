"""
tests/test_ashtakavarga.py
===========================
Tests for the Ashtakavarga bindu computation.
1947 India Independence chart is the primary fixture.
"""

import pytest
from tests.fixtures import INDIA_1947
from src.ephemeris import compute_chart, SIGNS
from src.calculations.ashtakavarga import (
    compute_ashtakavarga,
    AshtakavargaChart,
    AshtakavargaTable,
    FIXED_TOTALS,
    _PLANETS,
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
def india_av(india_chart):
    return compute_ashtakavarga(india_chart)


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

class TestAshtakavargaStructure:

    def test_returns_ashtakavarga_chart(self, india_av):
        assert isinstance(india_av, AshtakavargaChart)

    def test_has_seven_planet_tables(self, india_av):
        assert set(india_av.planet_av.keys()) == set(_PLANETS)

    def test_each_table_has_12_bindus(self, india_av):
        for p in _PLANETS:
            table = india_av.planet_av[p]
            assert len(table.bindus) == 12, f"{p}: expected 12 bindus"

    def test_sarva_has_12_bindus(self, india_av):
        assert len(india_av.sarva.bindus) == 12

    def test_all_planet_tables_are_AshtakavargaTable(self, india_av):
        for p in _PLANETS:
            assert isinstance(india_av.planet_av[p], AshtakavargaTable)
        assert isinstance(india_av.sarva, AshtakavargaTable)

    def test_planet_table_has_correct_planet_name(self, india_av):
        for p in _PLANETS:
            assert india_av.planet_av[p].planet == p
        assert india_av.sarva.planet == "Sarva"

    def test_bindus_in_valid_range(self, india_av):
        """Each planet table has bindus 0–8 (8 contributors max)."""
        for p in _PLANETS:
            for b in india_av.planet_av[p].bindus:
                assert 0 <= b <= 8, f"{p}: bindu {b} out of range"

    def test_sarva_bindus_in_valid_range(self, india_av):
        """Sarva bindus are 0–56 (7 planets × max 8 each)."""
        for b in india_av.sarva.bindus:
            assert 0 <= b <= 56, f"Sarva bindu {b} out of range"


# ---------------------------------------------------------------------------
# Fixed totals (chart-independent)
# ---------------------------------------------------------------------------

class TestFixedTotals:

    def test_each_planet_total_matches_fixed(self, india_av):
        """
        The sum of bindus per planet table is chart-independent
        (determined only by the benefic-house tables, not by planet positions).
        """
        for p in _PLANETS:
            table = india_av.planet_av[p]
            assert table.total == FIXED_TOTALS[p], \
                f"{p}: total={table.total}, expected={FIXED_TOTALS[p]}"

    def test_sarva_total_equals_sum_of_planet_totals(self, india_av):
        expected = sum(FIXED_TOTALS[p] for p in _PLANETS)
        assert india_sum(av.sarva.raw_bindus) == expected

    def test_fixed_totals_are_chart_independent(self, india_chart):
        """
        Compute AV for a different chart and verify totals are the same.
        We use a chart 10 years later at the same location.
        """
        chart2 = compute_chart(1957, 8, 15, 12.0, 28.6139, 77.2090, 5.5, "lahiri")
        av2 = compute_ashtakavarga(chart2)
        for p in _PLANETS:
            assert av2.planet_av[p].total == FIXED_TOTALS[p], \
                f"{p}: second chart total differs"


# ---------------------------------------------------------------------------
# Sarva = sum of planet tables
# ---------------------------------------------------------------------------

class TestSarvaConsistency:

    def test_sarva_equals_sum_of_planet_bindus(self, india_av):
        """Sarva[sign] must equal sum of all 7 planet bindus for that sign."""
        for si in range(12):
            expected = sum(india_av.planet_av[p].bindus[si] for p in _PLANETS)
            actual = india_av.sarva.bindus[si]
            assert actual == expected, \
                f"{SIGNS[si]}: sarva={actual}, sum={expected}"

    def test_for_planet_accessor_matches_planet_av(self, india_av):
        for p in _PLANETS:
            assert india_av.for_planet(p) is india_av.planet_av[p]


# ---------------------------------------------------------------------------
# 1947 India chart known values
# ---------------------------------------------------------------------------

class TestIndia1947Values:
    """
    1947 India: Taurus Lagna.
    Taurus (sign_index=1) is the lagna sign + has many planets in it (Rahu).
    All 5 planets (Sun/Moon/Mercury/Venus/Saturn) are in Cancer (index=3).
    Jupiter in Libra (index=6), Mars in Gemini (index=2), Rahu in Taurus (index=1).
    Expected: Cancer has fewer bindus per planet (stellium concentrates
    contributors, weakening the receiving sign's bindu count).
    """

    def test_taurus_sarva_above_average(self, india_av):
        """Taurus (lagna sign) tends to be stronger — Sarva bindus ≥ 30."""
        taurus_sarva = india_av.sarva.bindus[1]
        assert taurus_sarva >= 30, \
            f"Taurus Sarva={taurus_sarva}: expected strong bindus for lagna sign"

    def test_cancer_sarva_in_range(self, india_av):
        """Cancer has the most planets but bindus are independent of occupants."""
        cancer_sarva = india_av.sarva.bindus[3]
        assert 0 < cancer_sarva <= 56

    def test_each_sign_sarva_positive(self, india_av):
        """Every sign should receive at least some Sarva bindus."""
        for si, sign in enumerate(SIGNS):
            assert india_av.sarva.bindus[si] > 0, f"{sign}: zero Sarva bindus"

    def test_sun_cancer_bindus_in_range(self, india_av):
        """Sun's bindus in Cancer (where Sun itself sits) must be 0-8."""
        b = india_av.planet_av["Sun"].bindus[3]  # Cancer = index 3
        assert 0 <= b <= 8

    def test_bindu_for_sign_name_matches_index(self, india_av):
        for planet in _PLANETS:
            table = india_av.planet_av[planet]
            for si, sign_name in enumerate(SIGNS):
                assert table.bindu_for_sign_name(sign_name) == table.bindus[si]

    def test_bindu_for_sign_index_matches(self, india_av):
        for planet in _PLANETS:
            table = india_av.planet_av[planet]
            for si in range(12):
                assert table.bindu_for_sign(si) == table.bindus[si]


# ---------------------------------------------------------------------------
# Strength ratings
# ---------------------------------------------------------------------------

class TestStrengthRatings:

    def test_planet_strength_categories(self, india_av):
        for planet in _PLANETS:
            table = india_av.planet_av[planet]
            for si in range(12):
                rating = table.strength(si)
                assert rating in {"Strong", "Average", "Weak"}, \
                    f"{planet}/{SIGNS[si]}: unexpected rating {rating!r}"
                b = table.bindus[si]
                if b >= 5:
                    assert rating == "Strong"
                elif b == 4:
                    assert rating == "Average"
                else:
                    assert rating == "Weak"

    def test_sarva_strength_categories(self, india_av):
        for si in range(12):
            rating = india_av.sarva.strength(si)
            assert rating in {"Strong", "Average", "Weak"}
            b = india_av.sarva.bindus[si]
            if b >= 30:
                assert rating == "Strong"
            elif b >= 25:
                assert rating == "Average"
            else:
                assert rating == "Weak"


# ---------------------------------------------------------------------------
# Accuracy: E-1 and A-2 (regression guards)
# ---------------------------------------------------------------------------

class TestAccuracyGuards:
    """
    E-1: JDN Gregorian +0.5 day correction.
    Confirms our JD is correct: -5.5h UT works (swe.julday handles day rollback).

    A-2: Mercury direction uses wrong row reference.
    Confirms Mercury retrograde is computed from speed < 0.
    """

    def test_e1_jdn_negative_ut_hour_correct(self, india_chart):
        """1947-08-15 00:00 IST → JD 2432412.2708 (±0.001)."""
        # JD for 1947-08-14 18:30 UT = 2432411.5 + (18.5/24) = 2432412.2708...
        assert abs(india_chart.jd_ut - 2432412.2708) < 0.001, \
            f"JD mismatch: {india_chart.jd_ut:.6f} ≠ 2432412.2708 (E-1 regression)"

    def test_a2_mercury_retrograde_detection(self):
        """Mercury Rx during known 2022-09-10 – 2022-10-02 period."""
        rx_chart = compute_chart(2022, 9, 20, 12.0, 28.6139, 77.2090, 5.5, "lahiri")
        assert rx_chart.planets["Mercury"].is_retrograde, \
            "Mercury should be retrograde 2022-09-20 (A-2 regression)"
        assert rx_chart.planets["Mercury"].speed < 0

    def test_a2_mercury_direct_after_rx_period(self):
        """Mercury direct after 2022-10-02 retrograde end."""
        dx_chart = compute_chart(2022, 10, 15, 12.0, 28.6139, 77.2090, 5.5, "lahiri")
        assert not dx_chart.planets["Mercury"].is_retrograde, \
            "Mercury should be direct 2022-10-15 (A-2 regression)"
        assert dx_chart.planets["Mercury"].speed > 0

    def test_a2_mercury_not_rx_in_1947_india(self, india_chart):
        """1947 India chart: Mercury in Cancer, direct (speed > 0)."""
        merc = india_chart.planets["Mercury"]
        assert not merc.is_retrograde
        assert merc.speed > 0
        assert merc.sign == "Cancer"


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------

class TestDeterminism:

    def test_same_chart_produces_same_av(self, india_chart):
        av1 = compute_ashtakavarga(india_chart)
        av2 = compute_ashtakavarga(india_chart)
        for p in _PLANETS:
            assert av1.planet_av[p].bindus == av2.planet_av[p].bindus
        assert av1.sarva.bindus == av2.sarva.bindus
