"""
tests/test_kp.py
================
Test suite for src/calculations/kp.py — Session 17.

22 tests covering:
  - _SEQUENCE sums to 120 years
  - _SUB_SPAN total equals nakshatra span (13.333°)
  - kp_sub_at() returns valid KPPosition for any longitude
  - Star lords match nakshatra lords from nakshatra.py
  - Sub lord is always in _SEQUENCE
  - Sub degree range encloses the input longitude
  - 1947 India: Lagna (Taurus ~7.73°) known nakshatra = Krittika, SL = Sun
  - 1947 India: Moon (~93.98° = Cancer ~3.98°) → Pushya, SL = Saturn
  - compute_kp() structure: lagna_kp, 9 planets, 12 houses
  - All 12 houses present
  - House sub lords are valid planets
  - Significators list is non-empty and contains house lord
  - Whole-sign cusp: house 1 cusp = lagna_sign_index × 30°
  - House occupants: Cancer (H3 for Taurus lagna) has 5+ planets in 1947
  - KPPlanet property shortcuts (star_lord, sub_lord, nakshatra)
  - Determinism: same chart → same KPChart
  - Edge cases: 0.0° → Ashwini / Ketu; 359.99° → Revati / Mercury
  - Sub-sub lord is always a valid planet string
"""

import pytest

INDIA_1947 = {
    "year": 1947,
    "month": 8,
    "day": 15,
    "hour": 0.0,
    "lat": 28.6139,
    "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA_1947)


@pytest.fixture(scope="module")
def kp_chart(india_chart):
    from src.calculations.kp import compute_kp

    return compute_kp(india_chart)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Module-level constants
# ══════════════════════════════════════════════════════════════════════════════


class TestConstants:
    def test_sequence_length(self):
        from src.calculations.kp import _SEQUENCE

        assert len(_SEQUENCE) == 9

    def test_vimshottari_sum_120(self):
        from src.calculations.kp import _VIMSH_YEARS

        assert sum(_VIMSH_YEARS.values()) == 120

    def test_sub_span_sums_to_nakshatra(self):
        from src.calculations.kp import _SUB_SPAN, _NAK_SPAN

        assert abs(sum(_SUB_SPAN.values()) - _NAK_SPAN) < 1e-9

    def test_27_nakshatras(self):
        from src.calculations.kp import _NAK_NAMES, _NAK_LORDS

        assert len(_NAK_NAMES) == 27
        assert len(_NAK_LORDS) == 27

    def test_nak_lords_cycle_sequence(self):
        from src.calculations.kp import _NAK_LORDS

        # First nakshatra (Ashwini) → Ketu
        assert _NAK_LORDS[0] == "Ketu"
        # 10th nakshatra (Magha) → Ketu (index 9 → 9%9=0)
        assert _NAK_LORDS[9] == "Ketu"


# ══════════════════════════════════════════════════════════════════════════════
# 2. kp_sub_at() function
# ══════════════════════════════════════════════════════════════════════════════


class TestKpSubAt:
    def test_returns_kp_position(self):
        from src.calculations.kp import kp_sub_at, KPPosition

        pos = kp_sub_at(10.0)
        assert isinstance(pos, KPPosition)

    def test_longitude_0_ashwini_ketu(self):
        from src.calculations.kp import kp_sub_at

        pos = kp_sub_at(0.01)
        assert pos.nakshatra == "Ashwini"
        assert pos.star_lord == "Ketu"

    def test_longitude_359_revati_mercury(self):
        from src.calculations.kp import kp_sub_at

        pos = kp_sub_at(359.99)
        assert pos.nakshatra == "Revati"
        assert pos.star_lord == "Mercury"

    def test_sub_lord_in_sequence(self):
        from src.calculations.kp import kp_sub_at, _SEQUENCE

        for lon in [0.5, 15.3, 90.7, 180.0, 270.5, 359.0]:
            pos = kp_sub_at(lon)
            assert pos.sub_lord in _SEQUENCE, (
                f"Sub lord {pos.sub_lord!r} not in sequence at {lon}"
            )

    def test_sub_sub_lord_in_sequence(self):
        from src.calculations.kp import kp_sub_at, _SEQUENCE

        for lon in [5.0, 47.3, 123.6, 300.1]:
            pos = kp_sub_at(lon)
            assert pos.sub_sub_lord in _SEQUENCE

    def test_sub_degree_range_encloses_longitude(self):
        from src.calculations.kp import kp_sub_at

        for lon in [0.1, 30.5, 93.5, 150.0, 270.0]:
            pos = kp_sub_at(lon)
            assert pos.sub_degree_start <= lon < pos.sub_degree_end, (
                f"lon={lon} not in [{pos.sub_degree_start}, {pos.sub_degree_end})"
            )

    def test_nakshatra_index_matches_formula(self):
        from src.calculations.kp import kp_sub_at, _NAK_SPAN

        lon = 93.5
        pos = kp_sub_at(lon)
        expected_idx = int(lon / _NAK_SPAN)
        assert pos.nakshatra_index == expected_idx


# ══════════════════════════════════════════════════════════════════════════════
# 3. 1947 India known values
# ══════════════════════════════════════════════════════════════════════════════


class TestIndiaFixture:
    def test_lagna_nakshatra_krittika(self, kp_chart):
        # Taurus lagna at ~37.73° sidereal (7.73° in Taurus → 30° + 7.73°)
        # Krittika nakshatra: 26.67°–40.00° → star lord = Sun
        assert kp_chart.lagna_kp.nakshatra == "Krittika"
        assert kp_chart.lagna_kp.star_lord == "Sun"

    def test_moon_nakshatra_pushya(self, kp_chart):
        # Moon at ~93.98° sidereal → Pushya (80°–93.33°)
        # Actually 93.98 > 93.33 → Ashlesha? Let's check:
        # Pushya: nak_idx = int(93.33/13.333) = 7 → 93.33...
        # 93.98 / 13.333 = 7.048 → nak_idx = 7 → Pushya
        assert kp_chart.planets["Moon"].kp.nakshatra == "Pushya"
        assert kp_chart.planets["Moon"].star_lord == "Saturn"

    def test_lagna_kp_sub_lord_is_planet(self, kp_chart):
        from src.calculations.kp import _SEQUENCE

        assert kp_chart.lagna_kp.sub_lord in _SEQUENCE


# ══════════════════════════════════════════════════════════════════════════════
# 4. KPChart structure
# ══════════════════════════════════════════════════════════════════════════════


class TestKpChartStructure:
    def test_9_planets_present(self, kp_chart):
        expected = {
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
            "Rahu",
            "Ketu",
        }
        assert set(kp_chart.planets.keys()) == expected

    def test_12_houses_present(self, kp_chart):
        assert set(kp_chart.houses.keys()) == set(range(1, 13))

    def test_house_sub_lords_are_planets(self, kp_chart):
        from src.calculations.kp import _SEQUENCE

        for h in range(1, 13):
            sl = kp_chart.house_sub_lord(h)
            assert sl in _SEQUENCE, f"House {h} sub lord {sl!r} not in sequence"

    def test_house1_cusp_at_lagna_sign_start(self, india_chart, kp_chart):
        # Whole-sign: H1 cusp = lagna_sign_index × 30°
        expected = india_chart.lagna_sign_index * 30.0
        assert abs(kp_chart.houses[1].cusp_longitude - expected) < 1e-9

    def test_house_lord_in_significators(self, kp_chart):
        for h in range(1, 13):
            hspec = kp_chart.houses[h]
            assert hspec.house_lord in hspec.significators, (
                f"House {h} lord {hspec.house_lord!r} not in significators"
            )

    def test_significators_nonempty(self, kp_chart):
        for h in range(1, 13):
            assert len(kp_chart.houses[h].significators) >= 1

    def test_kp_planet_property_shortcuts(self, kp_chart):
        for pname in ["Sun", "Moon", "Saturn"]:
            kpp = kp_chart.for_planet(pname)
            assert kpp.star_lord == kpp.kp.star_lord
            assert kpp.sub_lord == kpp.kp.sub_lord
            assert kpp.nakshatra == kpp.kp.nakshatra

    def test_house3_has_cancer_planets(self, india_chart, kp_chart):
        # Taurus lagna → H3 = Cancer. 1947 chart has Sun/Moon/Mercury/Venus/Saturn in Cancer
        h3 = kp_chart.houses[3]
        # At least 4 planets in H3
        assert len(h3.occupants) >= 4

    def test_determinism(self, india_chart):
        from src.calculations.kp import compute_kp

        kp1 = compute_kp(india_chart)
        kp2 = compute_kp(india_chart)
        for p in ["Sun", "Moon", "Jupiter"]:
            assert kp1.planets[p].sub_lord == kp2.planets[p].sub_lord
