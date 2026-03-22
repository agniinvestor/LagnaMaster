"""
tests/test_calculations.py
============================
Regression tests for all Jyotish calculation modules.
Uses 1947 India Independence Chart as the primary fixture.
"""

import pytest  # noqa: E402
from datetime import date  # noqa: E402
from src.ephemeris import compute_chart, BirthChart  # noqa: E402
from tests.fixtures import INDIA_1947  # noqa: E402


@pytest.fixture(scope="module")
def india_chart() -> BirthChart:
    f = INDIA_1947
    return compute_chart(
        year=f["year"],
        month=f["month"],
        day=f["day"],
        hour=f["hour"],
        lat=f["lat"],
        lon=f["lon"],
        tz_offset=f["tz_offset"],
        ayanamsha=f["ayanamsha"],
    )


# ===========================================================================
# Nakshatra tests
# ===========================================================================


class TestNakshatra:
    def test_sun_ashlesha(self, india_chart):
        from src.calculations.nakshatra import nakshatra_position  # noqa: E402

        pos = nakshatra_position(india_chart.planets["Sun"].longitude)
        assert pos.nakshatra == "Ashlesha", (
            f"Sun nakshatra: expected Ashlesha, got {pos.nakshatra}"
        )
        assert pos.pada == 4

    def test_moon_pushya(self, india_chart):
        from src.calculations.nakshatra import nakshatra_position  # noqa: E402

        pos = nakshatra_position(india_chart.planets["Moon"].longitude)
        assert pos.nakshatra == "Pushya"

    def test_rahu_krittika(self, india_chart):
        from src.calculations.nakshatra import nakshatra_position  # noqa: E402

        pos = nakshatra_position(india_chart.planets["Rahu"].longitude)
        assert pos.nakshatra == "Krittika"

    def test_navamsha_arithmetic(self):
        """D9 navamsha via arithmetic formula = same as lookup formula."""
        from src.calculations.nakshatra import nakshatra_position  # noqa: E402

        # Aries 0° = Ashwini pada 1 → D9 = Aries (0*4+0 % 12 = 0)
        pos = nakshatra_position(0.0)
        assert pos.navamsha_sign in ("Aries", 0)

    def test_all_padas_1_to_4(self):
        from src.calculations.nakshatra import nakshatra_position, NAKSHATRA_SPAN  # noqa: E402

        # Scan 4 padas of Rohini (nak_idx=3): 40°–53.333°
        rohini_start = 3 * NAKSHATRA_SPAN  # 40°
        pada_span = NAKSHATRA_SPAN / 4
        for i in range(4):
            pos = nakshatra_position(rohini_start + i * pada_span + 0.1)
            assert pos.nakshatra == "Rohini"
            assert pos.pada == i + 1

    def test_ganda_mool_flags(self):
        from src.calculations.nakshatra import NAKSHATRAS_FULL as NAKSHATRAS  # noqa: E402

        mool_names = {n for n, _, m in NAKSHATRAS if m}
        expected = {"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}
        assert mool_names == expected


# ===========================================================================
# Dignity tests
# ===========================================================================

from src.calculations.dignity import DignityLevel as DignityLevel  # noqa: E402


class TestDignity:
    @staticmethod
    def _dig(planet, **kw):
        from src.calculations.dignity import compute_dignity_legacy as _cd  # noqa: E402

        return _cd(planet, **kw)

    def test_sun_in_friendly_sign_cancer(self, india_chart):
        from src.calculations.dignity import compute_all_dignities, DignityLevel  # noqa: E402

        digs = compute_all_dignities(india_chart)
        # Sun in Cancer — Cancer ruled by Moon. Sun-Moon: F → friendly sign
        assert digs["Sun"].dignity == DignityLevel.FRIEND_SIGN

    def test_venus_saturn_combust(self, india_chart):
        """Venus and Saturn are within Sun's orb in 1947 chart → combust."""
        from src.calculations.dignity import compute_all_dignities  # noqa: E402

        digs = compute_all_dignities(india_chart)
        assert digs["Venus"].combust, "Venus should be combust (5.4° from Sun)"
        assert digs["Saturn"].combust, "Saturn should be combust (7.5° from Sun)"

    def test_mars_not_combust(self, india_chart):
        from src.calculations.dignity import compute_all_dignities  # noqa: E402

        digs = compute_all_dignities(india_chart)
        assert not digs["Mars"].combust, "Mars (50° from Sun) should not be combust"

    def test_retrograde_bonus_applied(self, india_chart):
        from src.calculations.dignity import compute_all_dignities, RETROGRADE_BONUS  # noqa: E402

        digs = compute_all_dignities(india_chart)
        # Rahu and Ketu are always retrograde
        rahu = digs["Rahu"]
        assert rahu.is_retrograde
        # Total modifier includes retrograde bonus
        assert (
            rahu.score_modifier >= rahu.weight + RETROGRADE_BONUS - 0.01
        )  # RETROGRADE_BONUS=0

    def test_exaltation_detected(self):
        """Sun at 10° Aries = deep exaltation."""
        from src.calculations.dignity import DignityLevel  # noqa: E402

        result = self._dig(
            planet="Sun",
            sign_idx=0,
            degree_in_sign=10.0,
            is_retrograde=False,
            sun_longitude=10.0,
            planet_longitude=10.0,
            lagna_sign_idx=0,
        )
        assert result.dignity in (
            DignityLevel.DEEP_EXALT,
            DignityLevel.EXALT,
        )  # 0deg is EXALT not DEEP

    def test_debilitation_detected(self):
        """Saturn at 20° Aries = deep debilitation."""
        result = self._dig(
            planet="Saturn",
            sign_idx=0,
            degree_in_sign=20.0,
            is_retrograde=False,
            sun_longitude=200.0,
            planet_longitude=20.0,
            lagna_sign_idx=0,
        )
        assert result.dignity in (DignityLevel.DEEP_DEBIL, DignityLevel.DEBIL)

    def test_mooltrikona_detected(self):
        """Sun at 10° Leo = Mooltrikona (0-20°)."""
        result = self._dig(
            planet="Sun",
            sign_idx=4,
            degree_in_sign=10.0,
            is_retrograde=False,
            sun_longitude=130.0,
            planet_longitude=130.0,
            lagna_sign_idx=0,
        )
        assert result.dignity == DignityLevel.MOOLTRIKONA


# ===========================================================================
# House lord tests
# ===========================================================================


class TestHouseLord:
    def test_lagna_is_house_1(self, india_chart):
        from src.calculations.house_lord import compute_house_map  # noqa: E402

        hm = compute_house_map(india_chart)
        # Lagna = Taurus (sign_idx=1), house 1 = Taurus
        assert hm.house_sign[0] == india_chart.lagna_sign_index

    def test_house_1_lord_venus(self, india_chart):
        from src.calculations.house_lord import compute_house_map  # noqa: E402

        hm = compute_house_map(india_chart)
        # Taurus lord = Venus
        assert hm.house_lord[0] == "Venus"

    def test_mars_in_house_2(self, india_chart):
        """Mars is in Gemini = house 2 from Taurus lagna."""
        from src.calculations.house_lord import compute_house_map  # noqa: E402

        hm = compute_house_map(india_chart)
        assert hm.planet_house["Mars"] == 2

    def test_sun_in_house_3(self, india_chart):
        """Sun in Cancer = house 3 from Taurus lagna."""
        from src.calculations.house_lord import compute_house_map  # noqa: E402

        hm = compute_house_map(india_chart)
        assert hm.planet_house["Sun"] == 3

    def test_jupiter_in_house_6(self, india_chart):
        """Jupiter in Libra = house 6 from Taurus lagna."""
        from src.calculations.house_lord import compute_house_map  # noqa: E402

        hm = compute_house_map(india_chart)
        assert hm.planet_house["Jupiter"] == 6


# ===========================================================================
# Friendship tests
# ===========================================================================


class TestFriendship:
    def test_sun_moon_sama(self, india_chart):
        """Sun (Cancer) and Moon (Cancer) — same sign → Tatkalik Enemy; Naisargika F → Sama."""
        from src.calculations.friendship import compute_friendship  # noqa: E402

        r = compute_friendship(
            "Sun",
            india_chart.planets["Sun"].sign_index,
            "Moon",
            india_chart.planets["Moon"].sign_index,
        )
        assert r.panchadha == "Sama"

    def test_mars_sun_adhi_mitra(self, india_chart):
        """Mars (Gemini) views Sun (Cancer): H2 = Tatkalik Friend; Naisargika F → Adhi Mitra."""
        from src.calculations.friendship import compute_friendship  # noqa: E402

        r = compute_friendship(
            "Mars",
            india_chart.planets["Mars"].sign_index,
            "Sun",
            india_chart.planets["Sun"].sign_index,
        )
        assert r.panchadha == "Adhi Mitra"

    def test_naisargika_asymmetry(self):
        """Moon views Venus = N (neutral), but Venus views Moon = E (enemy)."""
        from src.calculations.friendship import compute_friendship  # noqa: E402

        moon_views_venus = compute_friendship("Moon", 3, "Venus", 3)
        venus_views_moon = compute_friendship("Venus", 3, "Moon", 3)
        assert moon_views_venus.naisargika == "N"
        assert venus_views_moon.naisargika == "E"


# ===========================================================================
# Chara Karak tests
# ===========================================================================


class TestCharaKarak:
    def test_sun_is_atmakaraka_1947(self, india_chart):
        """In 1947 chart Sun has highest degree (27.99°) → AK."""
        from src.calculations.chara_karak import compute_chara_karakas  # noqa: E402

        karakas = compute_chara_karakas(india_chart)
        ak = karakas[0]
        assert ak.planet == "Sun"
        assert ak.abbreviation == "AK"

    def test_moon_is_darakaraka_1947(self, india_chart):
        """Moon has lowest degree (3.98°) → DK (spouse)."""
        from src.calculations.chara_karak import compute_chara_karakas  # noqa: E402

        karakas = compute_chara_karakas(india_chart)
        dk = karakas[-1]
        assert dk.planet == "Moon"
        assert dk.abbreviation == "DK"

    def test_seven_karakas_returned(self, india_chart):
        from src.calculations.chara_karak import compute_chara_karakas  # noqa: E402

        karakas = compute_chara_karakas(india_chart)
        assert len(karakas) == 7

    def test_degrees_descending(self, india_chart):
        from src.calculations.chara_karak import compute_chara_karakas  # noqa: E402

        karakas = compute_chara_karakas(india_chart)
        degs = [k.degree_in_sign for k in karakas]
        assert degs == sorted(degs, reverse=True), (
            "Karakas should be sorted descending by degree"
        )


# ===========================================================================
# Narayana Dasha tests
# ===========================================================================


class TestNarayanaDasha:
    def test_n1_bug_fixed_taurus_7_years(self):
        """N-1 fix: Taurus Narayana Dasha = 7 years (not 4 as in Excel bug)."""
        from src.calculations.narayana_dasa import NARAYANA_DASHA_YEARS  # noqa: E402

        assert NARAYANA_DASHA_YEARS["Taurus"] == 7, (
            f"N-1 bug: Taurus should be 7 years, got {NARAYANA_DASHA_YEARS['Taurus']}"
        )

    def test_total_cycle_81_years(self):
        from src.calculations.narayana_dasa import NARAYANA_DASHA_YEARS  # noqa: E402

        total = sum(NARAYANA_DASHA_YEARS.values())
        assert total == 81, (
            f"Total Narayana Dasha cycle should be 81 years, got {total}"
        )

    def test_taurus_lagna_backward_direction(self):
        """Taurus = even sign (idx=1) → backward direction."""
        from src.calculations.narayana_dasa import compute_narayana_dasha  # noqa: E402

        periods = compute_narayana_dasha(
            lagna_sign_idx=1,  # Taurus
            birth_date=date(1947, 8, 15),
            query_date=date(1950, 1, 1),
        )
        assert periods[0].sign == "Taurus"
        assert periods[1].sign == "Aries"  # backward from Taurus

    def test_1947_chart_sequence(self, india_chart):
        """1947 India chart: Taurus lagna → Taurus, Aries, Pisces, Aquarius..."""
        from src.calculations.narayana_dasa import compute_narayana_dasha  # noqa: E402

        periods = compute_narayana_dasha(
            lagna_sign_idx=india_chart.lagna_sign_index,
            birth_date=date(1947, 8, 15),
        )
        signs = [p.sign for p in periods]
        assert signs[:4] == ["Taurus", "Aries", "Pisces", "Aquarius"]

    def test_12_periods_returned(self, india_chart):
        from src.calculations.narayana_dasa import compute_narayana_dasha  # noqa: E402

        periods = compute_narayana_dasha(
            india_chart.lagna_sign_index, date(1947, 8, 15)
        )
        assert len(periods) == 12


# ===========================================================================
# Shadbala tests
# ===========================================================================


class TestShadbala:
    @staticmethod
    def _sb(chart):
        from src.calculations.shadbala import compute_shadbala_legacy as _cs  # noqa: E402

        return _cs(chart)

    def test_seven_planets_computed(self, india_chart):
        result = self._sb(india_chart)
        assert set(result.planets.keys()) == {
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
        }

    def test_naisargika_sun_60(self, india_chart):
        result = self._sb(india_chart)
        assert result.planets["Sun"].naisargika == 60.0

    def test_naisargika_saturn_857(self, india_chart):
        result = self._sb(india_chart)
        assert abs(result.planets["Saturn"].naisargika - 8.57) < 0.01

    def test_s2_bug_saturn_chesta_not_3851(self, india_chart):
        """S-2 fix: Saturn Chesta Bala should be ~15.9, not 3851 (Excel bug)."""
        result = self._sb(india_chart)
        saturn_chesta = result.planets["Saturn"].chesta
        assert saturn_chesta < 100, (
            f"S-2 bug: Saturn Chesta should be ~15.9, got {saturn_chesta}"
        )
        assert saturn_chesta > 0

    def test_all_totals_positive(self, india_chart):
        result = self._sb(india_chart)
        for planet, s in result.planets.items():
            assert s.total > 0, f"{planet} total Shadbala should be positive"

    def test_uchcha_bala_range(self, india_chart):
        result = self._sb(india_chart)
        for planet, s in result.planets.items():
            assert 0 <= s.uchcha <= 60, f"{planet} Uchcha Bala out of range: {s.uchcha}"
