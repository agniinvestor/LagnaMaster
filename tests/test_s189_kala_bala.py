"""
tests/test_s189_kala_bala.py
Session 189 — Verify all 8 Kala Bala sub-components.

Each sub-component is tested with a deterministic chart + datetime
so that the expected value can be derived analytically.

Source: BPHS Ch.27 v.30-62
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.calculations.shadbala import compute_kala_bala, _WEEKDAY_LORDS, _HORA_SEQUENCE


# ─── Helpers ────────────────────────────────────────────────────────────────


def _make_chart(sun_lon: float = 180.0, moon_lon: float = 0.0) -> MagicMock:
    """Minimal mock chart with Sun and Moon at specified longitudes."""
    chart = MagicMock()
    planets = {}
    for name, lon in [("Sun", sun_lon), ("Moon", moon_lon),
                      ("Mars", 90.0), ("Mercury", 120.0),
                      ("Jupiter", 150.0), ("Venus", 210.0),
                      ("Saturn", 240.0)]:
        p = MagicMock()
        p.longitude = lon
        p.sign_index = int(lon / 30) % 12
        p.degree_in_sign = lon % 30
        p.is_retrograde = False
        p.speed = 1.0
        planets[name] = p
    chart.planets = planets
    return chart


# ─── 1. Nathonnata Bala (day/night strength) ────────────────────────────────


class TestNathonnataBala:
    """
    Day planets (Sun/Jupiter/Venus) = 60 by day, 0 by night.
    Night planets (Moon/Mars/Saturn) = 0 by day, 60 by night.
    Mercury = 60 always.
    """

    def test_sun_strong_by_day(self):
        """Continuous: Sun at 10 AM = 50 virupas (not binary 60)."""
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)  # 10:00 AM — 2h before noon
        _, comps = compute_kala_bala("Sun", chart, dt)
        assert comps["nathonnata"] > 40.0  # strong but not max
        assert comps["nathonnata"] <= 60.0

    def test_sun_weak_by_night(self):
        """Continuous: Sun at 10 PM = 10 virupas (not binary 0)."""
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 22, 0)  # 10:00 PM — 10h from noon
        _, comps = compute_kala_bala("Sun", chart, dt)
        assert comps["nathonnata"] < 20.0  # weak but not zero
        assert comps["nathonnata"] >= 0.0

    def test_moon_strong_by_night(self):
        """Continuous: Moon at 10 PM = strong (inverse of Sun)."""
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 22, 0)
        _, comps = compute_kala_bala("Moon", chart, dt)
        assert comps["nathonnata"] > 40.0

    def test_moon_weak_by_day(self):
        """Continuous: Moon at 10 AM = weak (inverse of Sun)."""
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)
        _, comps = compute_kala_bala("Moon", chart, dt)
        assert comps["nathonnata"] < 20.0

    def test_mercury_always_60(self):
        chart = _make_chart()
        dt_day = datetime(2024, 3, 15, 10, 0)
        dt_night = datetime(2024, 3, 15, 22, 0)
        _, comps_day = compute_kala_bala("Mercury", chart, dt_day)
        _, comps_night = compute_kala_bala("Mercury", chart, dt_night)
        assert comps_day["nathonnata"] == 60.0
        assert comps_night["nathonnata"] == 60.0

    def test_jupiter_strong_by_day(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 12, 0)
        _, comps = compute_kala_bala("Jupiter", chart, dt)
        assert comps["nathonnata"] == 60.0

    def test_saturn_strong_by_night(self):
        """Continuous: Saturn at 11 PM = strong (night planet)."""
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 23, 0)
        _, comps = compute_kala_bala("Saturn", chart, dt)
        assert comps["nathonnata"] > 40.0


# ─── 2. Paksha Bala (lunar phase) ───────────────────────────────────────────


class TestPakshaBala:
    """
    Waxing Moon (elongation 0→180): benefics increase 0→60.
    Full Moon (elongation=180): benefics = 60, malefics = 0.
    New Moon (elongation=0): benefics = 0, malefics = 60.
    """

    def test_full_moon_jupiter_gets_60(self):
        # Moon at 0°, Sun at 180° → elongation = (0-180) % 360 = 180 — full moon
        chart = _make_chart(sun_lon=180.0, moon_lon=0.0)
        _, comps = compute_kala_bala("Jupiter", chart)
        assert comps["paksha"] == pytest.approx(60.0, abs=1.0)

    def test_new_moon_mars_gets_60(self):
        # Moon and Sun at same longitude → elongation = 0 — new moon, malefic is strong
        chart = _make_chart(sun_lon=30.0, moon_lon=30.0)
        _, comps = compute_kala_bala("Mars", chart)
        assert comps["paksha"] == pytest.approx(60.0, abs=1.0)

    def test_full_moon_mars_gets_0(self):
        # Full moon: malefics get 0
        chart = _make_chart(sun_lon=180.0, moon_lon=0.0)
        _, comps = compute_kala_bala("Mars", chart)
        assert comps["paksha"] == pytest.approx(0.0, abs=1.0)

    def test_quarter_moon_benefic_gets_30(self):
        # Moon 90° ahead of Sun → elongation=90 → paksha_frac=0.5 → benefic gets 30
        chart = _make_chart(sun_lon=0.0, moon_lon=90.0)
        _, comps = compute_kala_bala("Jupiter", chart)
        assert comps["paksha"] == pytest.approx(30.0, abs=1.0)

    def test_paksha_in_range(self):
        chart = _make_chart()
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            _, comps = compute_kala_bala(planet, chart)
            assert 0.0 <= comps["paksha"] <= 60.0, f"{planet} paksha out of range"


# ─── 3. Tribhaga Bala (day/night thirds) ────────────────────────────────────


class TestTribhagaBala:
    """
    Day thirds (6-10, 10-14, 14-18): lords are Jupiter, Sun, Saturn.
    Night thirds (18-22, 22-02, 02-06): lords are Moon, Venus, Mars.
    """

    def test_day_first_watch_jupiter(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 8, 0)   # 8 AM → first day watch → Jupiter
        _, comps = compute_kala_bala("Jupiter", chart, dt)
        assert comps["tribhaga"] == 20.0

    def test_day_second_watch_sun(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 11, 0)  # 11 AM → second day watch → Sun
        _, comps = compute_kala_bala("Sun", chart, dt)
        assert comps["tribhaga"] == 20.0

    def test_day_third_watch_saturn(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 16, 0)  # 4 PM → third day watch → Saturn
        _, comps = compute_kala_bala("Saturn", chart, dt)
        assert comps["tribhaga"] == 20.0

    def test_non_lord_gets_zero(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 8, 0)   # first day watch → Jupiter lord
        _, comps = compute_kala_bala("Mars", chart, dt)
        assert comps["tribhaga"] == 0.0

    def test_night_second_watch_venus(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 23, 0)  # 11 PM → second night watch → Venus
        _, comps = compute_kala_bala("Venus", chart, dt)
        assert comps["tribhaga"] == 20.0


# ─── 4. Vara Bala (weekday lord) ────────────────────────────────────────────


class TestVaraBala:
    """
    The weekday lord gets 45 Virupas; all others get 0.
    _WEEKDAY_LORDS: Mon=Moon, Tue=Mars, Wed=Mercury, Thu=Jupiter, Fri=Venus, Sat=Saturn, Sun=Sun
    """

    def test_tuesday_mars_gets_45(self):
        chart = _make_chart()
        # 2024-03-19 is a Tuesday
        dt = datetime(2024, 3, 19, 12, 0)
        assert dt.weekday() == 1  # Tuesday
        _, comps = compute_kala_bala("Mars", chart, dt)
        assert comps["vara"] == 45.0

    def test_tuesday_sun_gets_0(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 19, 12, 0)  # Tuesday
        _, comps = compute_kala_bala("Sun", chart, dt)
        assert comps["vara"] == 0.0

    def test_sunday_sun_gets_45(self):
        chart = _make_chart()
        # 2024-03-17 is a Sunday
        dt = datetime(2024, 3, 17, 12, 0)
        assert dt.weekday() == 6  # Sunday
        _, comps = compute_kala_bala("Sun", chart, dt)
        assert comps["vara"] == 45.0

    def test_monday_moon_gets_45(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 18, 12, 0)  # Monday
        assert dt.weekday() == 0
        _, comps = compute_kala_bala("Moon", chart, dt)
        assert comps["vara"] == 45.0


# ─── 5. Hora Bala (planetary hour) ──────────────────────────────────────────


class TestHoraBala:
    """
    Hora sequence starts with weekday lord, cycles through _HORA_SEQUENCE.
    The hora lord for the birth hour gets 60 Virupas.
    """

    def test_hora_lord_gets_60(self):
        chart = _make_chart()
        # Sunday midnight (hour 0): weekday=Sun, hora_lord_idx=(6+0)%7=6 → Mars
        dt = datetime(2024, 3, 17, 0, 0)  # Sunday
        assert dt.weekday() == 6
        sun_idx = _HORA_SEQUENCE.index("Sun")  # should be 0
        expected_hora_lord = _HORA_SEQUENCE[(sun_idx + 0) % 7]
        _, comps = compute_kala_bala(expected_hora_lord, chart, dt)
        assert comps["hora"] == 60.0

    def test_non_hora_lord_gets_0(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 17, 0, 0)  # Sunday
        sun_idx = _HORA_SEQUENCE.index("Sun")
        expected_hora_lord = _HORA_SEQUENCE[(sun_idx + 0) % 7]
        # Pick a planet that is NOT the hora lord
        other = next(p for p in ["Sun", "Moon", "Mars", "Mercury",
                                  "Jupiter", "Venus", "Saturn"]
                     if p != expected_hora_lord)
        _, comps = compute_kala_bala(other, chart, dt)
        assert comps["hora"] == 0.0

    def test_hora_in_range(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 9, 30)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            _, comps = compute_kala_bala(planet, chart, dt)
            assert comps["hora"] in (0.0, 60.0), f"{planet} hora must be 0 or 60"


# ─── 6. Masa Bala (solar month lord) ────────────────────────────────────────


class TestMasaBala:
    """
    Solar month lords cycle by Sun's sign: Aries=Mars, Taurus=Venus, ...
    Month lord gets 30 Virupas.
    """

    def test_sun_in_aries_masa_lord_mars(self):
        # Sun at 15° Aries (sign_index=0) → month lord = Mars
        chart = _make_chart(sun_lon=15.0)
        dt = datetime(2024, 4, 5, 12, 0)
        _, comps = compute_kala_bala("Mars", chart, dt)
        assert comps["masa"] == 30.0

    def test_sun_in_aries_venus_gets_0(self):
        chart = _make_chart(sun_lon=15.0)
        dt = datetime(2024, 4, 5, 12, 0)
        _, comps = compute_kala_bala("Venus", chart, dt)
        assert comps["masa"] == 0.0

    def test_sun_in_taurus_masa_lord_venus(self):
        # Sun at 45° (Taurus, sign_index=1) → month lord = Venus
        chart = _make_chart(sun_lon=45.0)
        dt = datetime(2024, 5, 10, 12, 0)
        _, comps = compute_kala_bala("Venus", chart, dt)
        assert comps["masa"] == 30.0

    def test_sun_in_cancer_masa_lord_moon(self):
        # Sun at 105° (Cancer, sign_index=3) → month lord = Moon
        chart = _make_chart(sun_lon=105.0)
        dt = datetime(2024, 7, 10, 12, 0)
        _, comps = compute_kala_bala("Moon", chart, dt)
        assert comps["masa"] == 30.0


# ─── 7. Abda Bala (year lord) ────────────────────────────────────────────────


class TestAbdaBala:
    """
    Year lord = weekday of Jan 1 of birth year. Gets 15 Virupas.
    """

    def test_year_lord_gets_15(self):
        chart = _make_chart()
        dt = datetime(2024, 6, 15, 12, 0)
        jan1_2024 = datetime(2024, 1, 1)
        year_lord = _WEEKDAY_LORDS[jan1_2024.weekday()]
        _, comps = compute_kala_bala(year_lord, chart, dt)
        assert comps["abda"] == 15.0

    def test_non_year_lord_gets_0(self):
        chart = _make_chart()
        dt = datetime(2024, 6, 15, 12, 0)
        jan1_2024 = datetime(2024, 1, 1)
        year_lord = _WEEKDAY_LORDS[jan1_2024.weekday()]
        other = next(p for p in _WEEKDAY_LORDS if p != year_lord)
        _, comps = compute_kala_bala(other, chart, dt)
        assert comps["abda"] == 0.0

    def test_year_boundary_jan1_same_day(self):
        # Birth ON Jan 1 — year lord is the weekday of that same date
        chart = _make_chart()
        dt = datetime(1990, 1, 1, 6, 0)
        year_lord = _WEEKDAY_LORDS[datetime(1990, 1, 1).weekday()]
        _, comps = compute_kala_bala(year_lord, chart, dt)
        assert comps["abda"] == 15.0


# ─── 8. Ayana Bala (declination) ────────────────────────────────────────────


class TestAyanaBala:
    """
    Uttarayana (Sun in Capricorn-Gemini = signs 9-11, 0-2):
      Sun/Mars/Jupiter get 48, Moon/Venus/Saturn get 12.
    Dakshinayana (Sun in Cancer-Sagittarius = signs 3-8):
      Moon/Venus/Saturn get 48, Sun/Mars/Jupiter get 12.
    Mercury: always 30.
    """

    def test_uttarayana_sun_gets_48(self):
        # Sun at 270° = Capricorn (sign_index=9) → Uttarayana
        chart = _make_chart(sun_lon=270.0)
        _, comps = compute_kala_bala("Sun", chart)
        assert comps["ayana"] == 48.0

    def test_uttarayana_moon_gets_12(self):
        chart = _make_chart(sun_lon=270.0)
        _, comps = compute_kala_bala("Moon", chart)
        assert comps["ayana"] == 12.0

    def test_dakshinayana_sun_gets_12(self):
        # Sun at 120° = Leo (sign_index=4) → Dakshinayana
        chart = _make_chart(sun_lon=120.0)
        _, comps = compute_kala_bala("Sun", chart)
        assert comps["ayana"] == 12.0

    def test_dakshinayana_moon_gets_48(self):
        chart = _make_chart(sun_lon=120.0)
        _, comps = compute_kala_bala("Moon", chart)
        assert comps["ayana"] == 48.0

    def test_mercury_always_30(self):
        for sun_lon in [15.0, 120.0, 270.0]:
            chart = _make_chart(sun_lon=sun_lon)
            _, comps = compute_kala_bala("Mercury", chart)
            assert comps["ayana"] == 30.0, f"Mercury ayana wrong at sun_lon={sun_lon}"

    def test_uttarayana_jupiter_gets_48(self):
        chart = _make_chart(sun_lon=30.0)  # Sun in Taurus (sign_index=1) = Uttarayana
        _, comps = compute_kala_bala("Jupiter", chart)
        assert comps["ayana"] == 48.0


# ─── Total & component completeness ─────────────────────────────────────────


class TestKalaBalaTotal:
    """Verify total = sum of 8 components and all components present."""

    EXPECTED_KEYS = {"nathonnata", "paksha", "tribhaga", "vara",
                     "hora", "masa", "abda", "ayana"}

    def test_all_8_components_present(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            _, comps = compute_kala_bala(planet, chart, dt)
            assert set(comps.keys()) == self.EXPECTED_KEYS, (
                f"{planet}: expected keys {self.EXPECTED_KEYS}, got {set(comps.keys())}"
            )

    def test_total_equals_sum_of_components(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            total, comps = compute_kala_bala(planet, chart, dt)
            expected_total = round(sum(comps.values()), 3)
            assert total == pytest.approx(expected_total, abs=0.01), (
                f"{planet}: total {total} ≠ sum of components {expected_total}"
            )

    def test_total_non_negative(self):
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            total, _ = compute_kala_bala(planet, chart, dt)
            assert total >= 0.0, f"{planet}: negative Kala Bala total"

    def test_each_component_in_valid_range(self):
        """Each sub-component must be within its documented maximum."""
        max_values = {
            "nathonnata": 60.0,
            "paksha": 60.0,
            "tribhaga": 20.0,
            "vara": 45.0,
            "hora": 60.0,
            "masa": 30.0,
            "abda": 15.0,
            "ayana": 48.0,
        }
        chart = _make_chart()
        dt = datetime(2024, 3, 15, 10, 0)
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            _, comps = compute_kala_bala(planet, chart, dt)
            for key, max_val in max_values.items():
                assert comps[key] <= max_val + 0.01, (
                    f"{planet}.{key} = {comps[key]} exceeds max {max_val}"
                )
                assert comps[key] >= 0.0, f"{planet}.{key} = {comps[key]} is negative"
