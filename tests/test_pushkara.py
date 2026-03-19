"""tests/test_pushkara.py — Pushkara Navamsha tests (Session 11, 10 tests)"""
import pytest
from src.calculations.pushkara_navamsha import (
    _PUSHKARA_STARTS, _NAVAMSHA_WIDTH,
    is_pushkara_navamsha, pushkara_navamsha_planets,
    pushkara_navamsha_zones, pushkara_strength_label,
)

class TestIsPushkaraNavamsha:
    def test_aries_first_zone(self):
        assert is_pushkara_navamsha(0, 18.5) is True
    def test_aries_second_zone(self):
        assert is_pushkara_navamsha(0, 25.5) is True
    def test_aries_gap_between_zones(self):
        assert is_pushkara_navamsha(0, 22.0) is False
    def test_taurus_first_zone(self):
        assert is_pushkara_navamsha(1, 3.5) is True
    def test_libra_zero_start(self):
        assert is_pushkara_navamsha(6, 0.0) is True
    def test_pisces_second_zone(self):
        assert is_pushkara_navamsha(11, 26.0) is True
    def test_boundary_inclusive_start(self):
        for si,(s1,s2) in _PUSHKARA_STARTS.items():
            assert is_pushkara_navamsha(si,s1) is True
            assert is_pushkara_navamsha(si,s2) is True
    def test_boundary_exclusive_end(self):
        for si,(s1,s2) in _PUSHKARA_STARTS.items():
            e1=s1+_NAVAMSHA_WIDTH; e2=s2+_NAVAMSHA_WIDTH
            if e1<30.0: assert is_pushkara_navamsha(si,e1) is False
            if e2<30.0: assert is_pushkara_navamsha(si,e2) is False
    def test_all_12_signs_have_two_zones(self):
        for si in range(12):
            zones=pushkara_navamsha_zones(si)
            assert len(zones)==2
    def test_invalid_sign_index_returns_false(self):
        assert is_pushkara_navamsha(-1,5.0) is False
        assert is_pushkara_navamsha(12,5.0) is False

class TestStrengthLabel:
    def test_label_in_pn(self): assert pushkara_strength_label(0,18.5)=="Pushkara Navamsha"
    def test_label_outside_pn(self): assert pushkara_strength_label(0,10.0)==""

class TestPushkaraWithChart:
    @pytest.fixture(scope="class")
    def india_chart(self):
        from src.ephemeris import compute_chart
        return compute_chart(year=1947,month=8,day=15,hour=0.0,
                             lat=28.6139,lon=77.209,tz_offset=5.5,ayanamsha="lahiri")
    def test_returns_list(self,india_chart):
        assert isinstance(pushkara_navamsha_planets(india_chart),list)
    def test_sun_cancer_in_pn(self,india_chart):
        sun=india_chart.planets["Sun"]
        assert sun.sign_index==3
        assert is_pushkara_navamsha(sun.sign_index,sun.degree_in_sign) is True
    def test_moon_cancer_in_pn(self,india_chart):
        moon=india_chart.planets["Moon"]
        assert moon.sign_index==3
        assert is_pushkara_navamsha(3,moon.degree_in_sign) is True
    def test_planets_are_valid_names(self,india_chart):
        valid=set(india_chart.planets.keys())
        for name in pushkara_navamsha_planets(india_chart):
            assert name in valid
