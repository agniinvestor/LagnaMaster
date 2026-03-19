"""tests/test_pushkara.py — 10 tests (Session 11)"""
import pytest
from src.calculations.pushkara_navamsha import _PUSHKARA_STARTS,_NAVAMSHA_WIDTH,is_pushkara_navamsha,pushkara_navamsha_planets,pushkara_navamsha_zones,pushkara_strength_label
class TestIsPN:
    def test_aries1(self): assert is_pushkara_navamsha(0,18.5)
    def test_aries2(self): assert is_pushkara_navamsha(0,25.5)
    def test_gap(self): assert not is_pushkara_navamsha(0,22.)
    def test_taurus(self): assert is_pushkara_navamsha(1,3.5)
    def test_libra0(self): assert is_pushkara_navamsha(6,0.)
    def test_pisces(self): assert is_pushkara_navamsha(11,26.)
    def test_starts(self):
        for si,(s1,s2) in _PUSHKARA_STARTS.items(): assert is_pushkara_navamsha(si,s1) and is_pushkara_navamsha(si,s2)
    def test_ends(self):
        for si,(s1,s2) in _PUSHKARA_STARTS.items():
            if s1+_NAVAMSHA_WIDTH<30: assert not is_pushkara_navamsha(si,s1+_NAVAMSHA_WIDTH)
    def test_2zones(self):
        for si in range(12): assert len(pushkara_navamsha_zones(si))==2
    def test_invalid(self): assert not is_pushkara_navamsha(-1,5.)
class TestLabel:
    def test_in(self): assert pushkara_strength_label(0,18.5)=="Pushkara Navamsha"
    def test_out(self): assert pushkara_strength_label(0,10.)==""
class TestChart:
    @pytest.fixture(scope="class")
    def c(self):
        from src.ephemeris import compute_chart
        return compute_chart(1947,8,15,0.,28.6139,77.209,5.5,"lahiri")
    def test_list(self,c): assert isinstance(pushkara_navamsha_planets(c),list)
    def test_sun(self,c): assert is_pushkara_navamsha(c.planets["Sun"].sign_index,c.planets["Sun"].degree_in_sign)
    def test_moon(self,c): assert is_pushkara_navamsha(3,c.planets["Moon"].degree_in_sign)
    def test_names(self,c):
        for n in pushkara_navamsha_planets(c): assert n in c.planets
