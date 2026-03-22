"""
tests/test_vimshottari.py
==========================
Tests for Vimshottari Dasha calculation.
"""

import pytest
from datetime import date
from tests.fixtures import INDIA_1947
from src.ephemeris import compute_chart


@pytest.fixture(scope="module")
def india_chart():
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


@pytest.fixture(scope="module")
def india_dashas(india_chart):
    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

    return compute_vimshottari_dasa(india_chart, date(1947, 8, 15))


class TestVimshottariStructure:
    def test_returns_9_mahadashas(self, india_dashas):
        assert len(india_dashas) == 9

    def test_each_mahadasha_has_9_antardashas(self, india_dashas):
        for md in india_dashas:
            assert len(md.antardashas) == 9, (
                f"{md.lord} mahadasha has {len(md.antardashas)} antardashas"
            )

    def test_total_span_equals_sum_of_years(self, india_dashas):
        """Total calendar span matches sum of individual dasha years."""
        from src.calculations.vimshottari_dasa import _DAYS_PER_YEAR

        total_days = (india_dashas[-1].end - india_dashas[0].start).days
        expected_days = sum(md.years for md in india_dashas) * _DAYS_PER_YEAR
        assert abs(total_days - expected_days) < 5  # ±5 days rounding ok

    def test_full_periods_sum_to_120(self, india_dashas):
        """All 9 lords' full periods sum to exactly 120 years."""
        from src.calculations.vimshottari_dasa import VIMSHOTTARI_YEARS, TOTAL_YEARS

        total = sum(VIMSHOTTARI_YEARS[md.lord] for md in india_dashas)
        assert total == TOTAL_YEARS

    def test_dashas_are_contiguous(self, india_dashas):
        """Each dasha starts exactly where the previous one ends."""
        for i in range(1, len(india_dashas)):
            assert india_dashas[i].start == india_dashas[i - 1].end

    def test_antardashas_contiguous(self, india_dashas):
        for md in india_dashas:
            for i in range(1, 9):
                assert md.antardashas[i].start == md.antardashas[i - 1].end

    def test_antardasha_sum_equals_mahadasha(self, india_dashas):
        """Sum of antardasha years must equal mahadasha years (within float tolerance)."""
        for md in india_dashas:
            total = sum(ad.years for ad in md.antardashas)
            assert abs(total - md.years) < 1e-6, (
                f"{md.lord}: antardasha sum {total:.4f} ≠ maha years {md.years:.4f}"
            )

    def test_all_9_lords_appear(self, india_dashas):
        from src.calculations.vimshottari_dasa import _SEQUENCE

        lords = {md.lord for md in india_dashas}
        assert lords == set(_SEQUENCE)

    def test_unique_lords_in_sequence(self, india_dashas):
        lords = [md.lord for md in india_dashas]
        assert len(lords) == len(set(lords))


class TestVimshottari1947:
    """1947 India Independence chart specific assertions.

    Moon at ~3.98° Cancer → sidereal longitude ~93.98°
    Nakshatra: floor(93.98 / 13.333) = 7 → Pushya (index 7)
    Pushya lord = Saturn → birth dasha = Saturn
    """

    def test_birth_dasha_lord_is_saturn(self, india_dashas):
        assert india_dashas[0].lord == "Saturn"

    def test_birth_nakshatra_is_pushya(self, india_dashas):
        assert india_dashas[0].nakshatra == "Pushya"

    def test_birth_dasha_balance_less_than_full(self, india_dashas):
        """Balance of Saturn dasha at birth must be < 19 (full period)."""
        assert india_dashas[0].years < 19
        assert india_dashas[0].years > 0

    def test_second_dasha_is_mercury_full_17(self, india_dashas):
        """After Saturn (index 8 in sequence), next is Mercury (index 0 wrap) → 17 years."""
        md2 = india_dashas[1]
        assert md2.lord == "Mercury"
        assert abs(md2.years - 17.0) < 1e-6

    def test_dasha_sequence_order(self, india_dashas):
        """Starting from Saturn, sequence: Saturn→Mercury→Ketu→Venus→Sun→Moon→Mars→Rahu→Jupiter."""
        from src.calculations.vimshottari_dasa import _SEQUENCE

        saturn_idx = _SEQUENCE.index("Saturn")
        expected = [_SEQUENCE[(saturn_idx + i) % 9] for i in range(9)]
        actual = [md.lord for md in india_dashas]
        assert actual == expected

    def test_nakshatra_function(self, india_chart):
        from src.calculations.vimshottari_dasa import nakshatra_of_moon

        nak, lord = nakshatra_of_moon(india_chart)
        assert nak == "Pushya"
        assert lord == "Saturn"


class TestCurrentDasha:
    def test_current_dasha_returns_tuple(self, india_dashas):
        from src.calculations.vimshottari_dasa import current_dasha

        md, ad = current_dasha(india_dashas, date(2000, 1, 1))
        assert md is not None
        assert ad is not None
        assert ad.lord in [md.lord] + [ad2.lord for ad2 in md.antardashas]

    def test_current_dasha_within_maha_span(self, india_dashas):
        from src.calculations.vimshottari_dasa import current_dasha

        md, ad = current_dasha(india_dashas, date(1960, 6, 1))
        assert md.start <= date(1960, 6, 1) < md.end

    def test_antardasha_within_maha_span(self, india_dashas):
        from src.calculations.vimshottari_dasa import current_dasha

        for test_date in [date(1948, 1, 1), date(1975, 6, 15), date(2020, 3, 1)]:
            md, ad = current_dasha(india_dashas, test_date)
            assert md.start <= test_date < md.end, (
                f"{test_date}: not within {md.lord} ({md.start}–{md.end})"
            )


class TestAntarDashaDurations:
    def test_antardasha_proportional_to_periods(self, india_dashas):
        """Antardasha years ∝ (maha_years × antar_full_years) / 120."""
        from src.calculations.vimshottari_dasa import VIMSHOTTARI_YEARS, TOTAL_YEARS

        for md in india_dashas:
            for ad in md.antardashas:
                expected = md.years * VIMSHOTTARI_YEARS[ad.lord] / TOTAL_YEARS
                assert abs(ad.years - expected) < 1e-9, (
                    f"{md.lord}/{ad.lord}: expected {expected:.6f}, got {ad.years:.6f}"
                )

    def test_first_antardasha_is_maha_lord(self, india_dashas):
        """First antardasha of each mahadasha is the mahadasha lord itself."""
        for md in india_dashas:
            assert md.antardashas[0].lord == md.lord
