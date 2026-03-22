"""tests/test_chara_dasha.py — 20 tests (Session 14)"""

import pytest
from datetime import date
from src.calculations.chara_dasha import (
    compute_chara_dasha,
    current_chara_dasha,
    atmakaraka_sign,
    _atmakaraka,
    _dy,
    _sld,
    _pis,
    CharaDashaEntry,
    _SIGN_NAMES,
)

BD = date(1947, 8, 15)


@pytest.fixture(scope="module")
def ic():
    from src.ephemeris import compute_chart

    return compute_chart(1947, 8, 15, 0.0, 28.6139, 77.209, 5.5, "lahiri")


@pytest.fixture(scope="module")
def ids(ic):
    return compute_chara_dasha(ic, BD)


class TestAK:
    def test_sun(self, ic):
        assert _atmakaraka(ic) == "Sun"

    def test_tuple(self, ic):
        ak, s = atmakaraka_sign(ic)
        assert isinstance(ak, str) and isinstance(s, str)

    def test_cancer(self, ic):
        ak, s = atmakaraka_sign(ic)
        assert ak == "Sun" and s == "Cancer"


class TestSequence:
    def test_12(self, ids):
        assert len(ids) == 12

    def test_type(self, ids):
        for d in ids:
            assert isinstance(d, CharaDashaEntry)

    def test_backward(self, ids):
        assert (
            ids[0].sign == "Taurus"
            and ids[1].sign == "Aries"
            and ids[2].sign == "Pisces"
        )

    def test_all_signs(self, ids):
        assert {d.sign for d in ids} == set(_SIGN_NAMES)

    def test_no_dupes(self, ids):
        signs = [d.sign for d in ids]
        assert len(signs) == len(set(signs))

    def test_contiguous(self, ids):
        for i in range(len(ids) - 1):
            assert ids[i].end == ids[i + 1].start

    def test_starts_birth(self, ids):
        assert ids[0].start == BD

    def test_years_range(self, ids):
        for d in ids:
            assert 0.5 <= d.years <= 12.0

    def test_si_valid(self, ids):
        for d in ids:
            assert 0 <= d.sign_index <= 11


class TestYears:
    def test_min1(self, ic):
        for si in range(12):
            assert _dy(si, ic) >= 1

    def test_max12(self, ic):
        for si in range(12):
            assert _dy(si, ic) <= 12

    def test_sld_min1(self, ic):
        for si in range(12):
            assert _sld(si, ic) >= 1

    def test_cancer_planets(self, ic):
        assert len(_pis(3, ic)) >= 4


class TestBalance:
    def test_le_full(self, ic, ids):
        assert ids[0].years <= _dy(ids[0].sign_index, ic) + 0.01

    def test_positive(self, ids):
        assert ids[0].years > 0


class TestCurrent:
    def test_type(self, ids):
        assert isinstance(current_chara_dasha(ids, date(2026, 3, 19)), CharaDashaEntry)

    def test_within(self, ids):
        td = date(2000, 1, 1)
        cd = current_chara_dasha(ids, td)
        assert cd.start <= td < cd.end

    def test_birth_first(self, ids):
        assert current_chara_dasha(ids, BD).sign == ids[0].sign

    def test_flag(self, ids):
        assert current_chara_dasha(ids, date(2000, 1, 1)).is_current


class TestDet:
    def test_same(self, ic):
        d1 = compute_chara_dasha(ic, BD)
        d2 = compute_chara_dasha(ic, BD)
        for i in range(12):
            assert d1[i].sign == d2[i].sign and d1[i].years == d2[i].years
