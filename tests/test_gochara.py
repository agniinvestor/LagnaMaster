"""
tests/test_gochara.py
======================
Tests for Gochara (transit) analysis.
Uses the 1947 India Independence chart as natal, with specific transit
dates where planetary positions are verifiable.
"""

import pytest
from datetime import date

from tests.fixtures import INDIA_1947
from src.ephemeris import compute_chart, SIGNS
from src.calculations.gochara import (
    compute_gochara,
    GocharaReport,
    TransitPlanet,
    _whole_sign_house,
    _sade_sati_phase,
)


@pytest.fixture(scope="module")
def natal_chart():
    f = INDIA_1947
    return compute_chart(
        year=f["year"], month=f["month"], day=f["day"],
        hour=f["hour"], lat=f["lat"], lon=f["lon"],
        tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
    )


@pytest.fixture(scope="module")
def gochara_2026(natal_chart):
    """Transit snapshot: 2026-03-19 (today during development)."""
    return compute_gochara(natal_chart, date(2026, 3, 19))


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------

class TestGocharaStructure:

    def test_returns_gochara_report(self, gochara_2026):
        assert isinstance(gochara_2026, GocharaReport)

    def test_has_nine_planets(self, gochara_2026):
        expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter",
                    "Venus", "Saturn", "Rahu", "Ketu"}
        assert set(gochara_2026.planets.keys()) == expected

    def test_each_transit_is_TransitPlanet(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            assert isinstance(tp, TransitPlanet)

    def test_transit_date_preserved(self, gochara_2026):
        assert gochara_2026.transit_date == date(2026, 3, 19)

    def test_natal_lagna_and_moon_preserved(self, gochara_2026):
        assert gochara_2026.natal_lagna_sign == "Taurus"
        assert gochara_2026.natal_moon_sign  == "Cancer"
        assert gochara_2026.natal_moon_sign_index == 3  # Cancer = index 3


# ---------------------------------------------------------------------------
# Transit planet validity
# ---------------------------------------------------------------------------

class TestTransitPlanetValidity:

    def test_longitudes_in_range(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            assert 0.0 <= tp.longitude < 360.0, \
                f"{tp.planet}: lon={tp.longitude}"

    def test_sign_index_consistent_with_longitude(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            expected_si = int(tp.longitude / 30) % 12
            assert tp.sign_index == expected_si, \
                f"{tp.planet}: sign_index={tp.sign_index}, expected={expected_si}"

    def test_sign_name_consistent_with_index(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            assert tp.sign == SIGNS[tp.sign_index], \
                f"{tp.planet}: sign={tp.sign}, index={tp.sign_index}"

    def test_degree_in_sign_in_range(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            assert 0.0 <= tp.degree_in_sign < 30.0, \
                f"{tp.planet}: degree_in_sign={tp.degree_in_sign}"

    def test_retrograde_consistent_with_speed(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            if tp.planet not in ("Rahu", "Ketu"):  # nodes always Rx
                if tp.speed < 0:
                    assert tp.is_retrograde, f"{tp.planet}: speed<0 but not Rx"
                else:
                    assert not tp.is_retrograde, f"{tp.planet}: speed>0 but Rx"

    def test_natal_house_in_range(self, gochara_2026):
        for tp in gochara_2026.planets.values():
            assert 1 <= tp.natal_house <= 12, \
                f"{tp.planet}: natal_house={tp.natal_house}"

    def test_av_bindus_for_seven_planets(self, gochara_2026):
        """Rahu and Ketu have no AV table (av_bindus = -1)."""
        av_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
        for tp in gochara_2026.planets.values():
            if tp.planet in av_planets:
                assert 0 <= tp.av_bindus <= 8, \
                    f"{tp.planet}: av_bindus={tp.av_bindus}"
            else:
                assert tp.av_bindus == -1, \
                    f"{tp.planet}: expected av_bindus=-1, got {tp.av_bindus}"

    def test_rahu_ketu_opposite(self, gochara_2026):
        """Rahu and Ketu must be exactly 180° apart."""
        rahu = gochara_2026.planets["Rahu"]
        ketu = gochara_2026.planets["Ketu"]
        diff = abs(((rahu.longitude - ketu.longitude) % 360) - 180)
        assert diff < 0.01, f"Rahu-Ketu not 180°: diff={diff:.4f}"


# ---------------------------------------------------------------------------
# House computation helper
# ---------------------------------------------------------------------------

class TestWholeSignHouse:

    def test_same_sign_as_lagna(self):
        """Planet in same sign as lagna → H1."""
        assert _whole_sign_house(1, 1) == 1   # Taurus lagna, Taurus planet

    def test_next_sign(self):
        """Planet in next sign → H2."""
        assert _whole_sign_house(2, 1) == 2   # Taurus lagna, Gemini planet

    def test_wrap_around(self):
        """H12 wraps around correctly: planet in Aries, lagna Taurus → H12."""
        assert _whole_sign_house(0, 1) == 12  # Aries planet, Taurus lagna

    def test_opposite_sign(self):
        """7th house = 6 signs away."""
        assert _whole_sign_house(7, 1) == 7   # Taurus lagna, Scorpio = 7th


# ---------------------------------------------------------------------------
# Sade Sati logic
# ---------------------------------------------------------------------------

class TestSadeSati:

    def test_peak_phase(self):
        """Saturn in natal Moon sign = Peak."""
        active, phase = _sade_sati_phase(saturn_si=3, moon_si=3)
        assert active is True
        assert phase == "Peak"

    def test_rising_phase(self):
        """Saturn one sign before natal Moon = Rising."""
        active, phase = _sade_sati_phase(saturn_si=2, moon_si=3)
        assert active is True
        assert phase == "Rising"

    def test_setting_phase(self):
        """Saturn one sign after natal Moon = Setting."""
        active, phase = _sade_sati_phase(saturn_si=4, moon_si=3)
        assert active is True
        assert phase == "Setting"

    def test_none_when_not_adjacent(self):
        """Saturn two signs away → not Sade Sati."""
        active, phase = _sade_sati_phase(saturn_si=5, moon_si=3)
        assert active is False
        assert phase == "None"

    def test_wrap_around_rising(self):
        """Natal Moon in Aries (0): rising = Pisces (11)."""
        active, phase = _sade_sati_phase(saturn_si=11, moon_si=0)
        assert active is True
        assert phase == "Rising"

    def test_sade_sati_field_on_report(self, gochara_2026):
        """GocharaReport.sade_sati and sade_sati_phase are consistent."""
        ss = gochara_2026.sade_sati
        phase = gochara_2026.sade_sati_phase
        if ss:
            assert phase in {"Rising", "Peak", "Setting"}
        else:
            assert phase == "None"


# ---------------------------------------------------------------------------
# Transit house accessor
# ---------------------------------------------------------------------------

class TestTransitHouseAccessor:

    def test_transit_house_method(self, gochara_2026):
        for planet in ["Sun", "Moon", "Mars", "Jupiter", "Saturn"]:
            h = gochara_2026.transit_house(planet)
            assert h == gochara_2026.planets[planet].natal_house


# ---------------------------------------------------------------------------
# Default date (today)
# ---------------------------------------------------------------------------

class TestDefaultDate:

    def test_no_date_uses_today(self, natal_chart):
        from datetime import date as dt
        report = compute_gochara(natal_chart)
        assert report.transit_date == dt.today()

    def test_two_consecutive_calls_same_result(self, natal_chart):
        """Same date → same positions (determinism)."""
        fixed = date(2026, 1, 1)
        r1 = compute_gochara(natal_chart, fixed)
        r2 = compute_gochara(natal_chart, fixed)
        for planet in r1.planets:
            assert abs(r1.planets[planet].longitude - r2.planets[planet].longitude) < 1e-9


# ---------------------------------------------------------------------------
# Guru (Jupiter) transit
# ---------------------------------------------------------------------------

class TestJupiterTransit:

    def test_guru_transit_house_in_range(self, gochara_2026):
        assert 1 <= gochara_2026.guru_transit_house <= 12

    def test_guru_chandal_is_bool(self, gochara_2026):
        assert isinstance(gochara_2026.guru_chandal_transit, bool)

    def test_guru_chandal_means_same_sign(self, gochara_2026):
        """Guru-Chandal requires Jupiter and Rahu in same sign."""
        jup_si = gochara_2026.planets["Jupiter"].sign_index
        rah_si = gochara_2026.planets["Rahu"].sign_index
        expected = (jup_si == rah_si)
        assert gochara_2026.guru_chandal_transit == expected
