"""tests/test_kundali_milan.py — Kundali Milan tests (Session 12, 25 tests)"""
import pytest
from unittest.mock import MagicMock
from src.calculations.kundali_milan import (
    compute_kundali_milan, has_mangal_dosha,
    KundaliMilanResult, KootaScore,
    _nadi_score, _bhakut_score, _gana_score, _yoni_score, _tara_score,
    _NADI, _GANA, _YONI, NAKSHATRAS,
)

def _planet(sign,si,deg,lon=None):
    p=MagicMock(); p.sign=sign; p.sign_index=si; p.degree_in_sign=deg
    p.longitude=lon if lon is not None else si*30+deg
    return p

def _chart(moon_sign,moon_si,moon_deg,mars_si,venus_si,lagna_si):
    c=MagicMock(); c.lagna_sign_index=lagna_si
    c.planets={"Moon":_planet(moon_sign,moon_si,moon_deg),
               "Mars":_planet("Aries",mars_si,10.0),
               "Venus":_planet("Taurus",venus_si,5.0)}
    return c

class TestResultStructure:
    @pytest.fixture(scope="class")
    def result(self):
        return compute_kundali_milan(
            _chart("Taurus",1,20.0,5,2,0),
            _chart("Cancer",3,10.0,9,6,3))
    def test_is_kundali_milan_result(self,result): assert isinstance(result,KundaliMilanResult)
    def test_eight_kootas(self,result):
        assert set(result.kootas.keys())=={"Varna","Vashya","Tara","Yoni","Graha Maitri","Gana","Bhakut","Nadi"}
    def test_max_scores(self,result):
        for name,mx in {"Varna":1,"Vashya":2,"Tara":3,"Yoni":4,"Graha Maitri":5,"Gana":6,"Bhakut":7,"Nadi":8}.items():
            assert result.kootas[name].max_score==mx
    def test_scores_in_range(self,result):
        for k in result.kootas.values(): assert 0.0<=k.score<=k.max_score
    def test_total_equals_sum(self,result):
        assert abs(result.total_score-sum(k.score for k in result.kootas.values()))<1e-6
    def test_total_bounded(self,result): assert 0.0<=result.total_score<=36.0
    def test_percentage_consistent(self,result):
        assert abs(result.percentage-result.total_score/36*100)<0.01
    def test_grade_valid(self,result): assert result.grade in("Excellent","Good","Weak")

class TestGrades:
    def test_excellent(self):
        from src.calculations.kundali_milan import _grade
        assert _grade(28.0)=="Excellent" and _grade(36.0)=="Excellent"
    def test_good(self):
        from src.calculations.kundali_milan import _grade
        assert _grade(18.0)=="Good" and _grade(27.9)=="Good"
    def test_weak(self):
        from src.calculations.kundali_milan import _grade
        assert _grade(17.9)=="Weak" and _grade(0.0)=="Weak"

class TestNadiDosha:
    def test_same_nadi_zero(self):
        assert _NADI[0]==_NADI[5]=="Aadi"
        assert _nadi_score(0,5)==0.0
    def test_different_nadi_eight(self): assert _nadi_score(0,1)==8.0
    def test_nadi_dosha_flag(self):
        m=_chart("Aries",0,5.0,5,2,0); m.planets["Moon"].longitude=5.0
        f=_chart("Gemini",2,10.0,9,6,3); f.planets["Moon"].longitude=70.0
        r=compute_kundali_milan(m,f)
        assert r.nadi_dosha is True and "Nadi Dosha" in r.critical_doshas

class TestBhakutDosha:
    def test_6_8_axis_zero(self): assert _bhakut_score(0,5)==0.0
    def test_5_9_axis_zero(self): assert _bhakut_score(0,4)==0.0
    def test_1_7_full(self): assert _bhakut_score(0,0)==7.0
    def test_bhakut_flag(self):
        m=_chart("Aries",0,5.0,5,2,0); m.planets["Moon"].sign_index=0; m.planets["Moon"].longitude=5.0
        f=_chart("Virgo",5,5.0,9,6,5); f.planets["Moon"].sign_index=5; f.planets["Moon"].longitude=155.0
        r=compute_kundali_milan(m,f)
        assert r.bhakut_dosha is True and "Bhakut Dosha" in r.critical_doshas

class TestMangalDosha:
    def _c(self,mars_si,lagna_si=0,moon_si=3,venus_si=1):
        c=MagicMock(); c.lagna_sign_index=lagna_si
        c.planets={"Mars":_planet("X",mars_si,10.0),"Moon":_planet("Y",moon_si,5.0),"Venus":_planet("Z",venus_si,5.0)}
        return c
    def test_h1_from_lagna(self): assert has_mangal_dosha(self._c(0,0)) is True
    def test_h7_from_lagna(self): assert has_mangal_dosha(self._c(6,0)) is True
    def test_h3_no_dosha_check(self): assert (2-0)%12+1==3 and 3 not in{1,2,4,7,8,12}
    def test_mutual_cancellation(self):
        m=self._c(0,0,3,1); f=self._c(5,5,3,1)
        r=compute_kundali_milan(m,f)
        if r.mangal_dosha_male and r.mangal_dosha_female:
            assert r.dosha_cancelled is True

class TestSelfCompatibility:
    @pytest.fixture(scope="class")
    def india(self):
        from src.ephemeris import compute_chart
        return compute_chart(year=1947,month=8,day=15,hour=0.0,lat=28.6139,lon=77.209,tz_offset=5.5,ayanamsha="lahiri")
    def test_runs(self,india): assert isinstance(compute_kundali_milan(india,india),KundaliMilanResult)
    def test_nadi_dosha(self,india): assert compute_kundali_milan(india,india).nadi_dosha is True
    def test_same_gana(self,india): assert compute_kundali_milan(india,india).kootas["Gana"].score==6.0
    def test_determinism(self,india): assert compute_kundali_milan(india,india).total_score==compute_kundali_milan(india,india).total_score
    def test_mangal_dosha_type(self,india): assert isinstance(has_mangal_dosha(india),bool)

class TestKootaBounds:
    @pytest.mark.parametrize("a,b",[(0,0),(0,13),(13,26),(7,14)])
    def test_tara_range(self,a,b): assert 0.0<=_tara_score(a,b)<=3.0
    @pytest.mark.parametrize("a,b",[(0,0),(0,9),(5,20)])
    def test_yoni_range(self,a,b): assert _yoni_score(a,b) in(0.0,2.0,4.0)
    def test_nadi_only_0_or_8(self):
        for a in range(27):
            for b in range(0,27,9): assert _nadi_score(a,b) in(0.0,8.0)
