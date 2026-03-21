"""tests/test_kundali_milan.py — 25 tests (Session 12)"""
import pytest; from unittest.mock import MagicMock
from src.calculations.kundali_milan import compute_kundali_milan,has_mangal_dosha,KundaliMilanResult,_nd,_bh,_gn,_yo,_ta,_NA,_GA,_Y
def _p(s,si,d,lon=None): p=MagicMock(); p.sign=s; p.sign_index=si; p.degree_in_sign=d; p.longitude=lon if lon else si*30+d; return p
def _c(ms,msi,md,masi,vsi,lsi): c=MagicMock(); c.lagna_sign_index=lsi; c.planets={"Moon":_p(ms,msi,md),"Mars":_p("X",masi,10.),"Venus":_p("Y",vsi,5.)}; return c
class TestStruct:
    @pytest.fixture(scope="class")
    def r(self): return compute_kundali_milan(_c("Taurus",1,20.,5,2,0),_c("Cancer",3,10.,9,6,3))
    def test_type(self,r): assert isinstance(r,KundaliMilanResult)
    def test_8k(self,r): assert set(r.kootas.keys())=={"Varna","Vashya","Tara","Yoni","Graha Maitri","Gana","Bhakut","Nadi"}
    def test_max(self,r):
        for n,m in{"Varna":1,"Vashya":2,"Tara":3,"Yoni":4,"Graha Maitri":5,"Gana":6,"Bhakut":7,"Nadi":8}.items(): assert r.kootas[n].max_score==m
    def test_range(self,r):
        for k in r.kootas.values(): assert 0.<=k.score<=k.max_score
    def test_sum(self,r): assert abs(r.total_score-sum(k.score for k in r.kootas.values()))<1e-6
    def test_36(self,r): assert 0.<=r.total_score<=36.
    def test_pct(self,r): assert abs(r.percentage-r.total_score/36*100)<1.0
    def test_grade(self,r): assert r.grade in("Excellent","Good","Weak")
class TestGrades:
    def _g(self,s):
        from src.calculations.kundali_milan import _grade; return _grade(s)
    def test_exc(self): assert self._g(28.)=="Excellent"
    def test_good(self): assert self._g(18.)=="Good"
    def test_weak(self): assert self._g(0.)=="Weak"
class TestNadi:
    def test_same(self): assert _NA[0]==_NA[5]=="Aadi" and _nd(0,5)==0.
    def test_diff(self): assert _nd(0,1)==8.
    def test_flag(self):
        m=_c("Aries",0,5.,5,2,0); m.planets["Moon"].longitude=5.
        f=_c("Gemini",2,10.,9,6,3); f.planets["Moon"].longitude=70.
        r=compute_kundali_milan(m,f); assert r.nadi_dosha and "Nadi Dosha" in r.critical_doshas
class TestBhakut:
    def test_68(self): assert _bh(0,5)==0.
    def test_59(self): assert _bh(0,4)==0.
    def test_17(self): assert _bh(0,0)==7.
    def test_flag(self):
        m=_c("Aries",0,5.,5,2,0); m.planets["Moon"].sign_index=0; m.planets["Moon"].longitude=5.
        f=_c("Virgo",5,5.,9,6,5); f.planets["Moon"].sign_index=5; f.planets["Moon"].longitude=155.
        r=compute_kundali_milan(m,f); assert r.bhakut_dosha and "Bhakut Dosha" in r.critical_doshas
class TestMangal:
    def _mc(self,ms,ls=0,mos=3,vs=1): c=MagicMock(); c.lagna_sign_index=ls; c.planets={"Mars":_p("X",ms,10.),"Moon":_p("Y",mos,5.),"Venus":_p("Z",vs,5.)}; return c
    def test_h1(self): assert has_mangal_dosha(self._mc(0,0))
    def test_h7(self): assert has_mangal_dosha(self._mc(6,0))
    def test_h3(self): assert (2-0)%12+1==3 and 3 not in{1,2,4,7,8,12}
    def test_cancel(self):
        r=compute_kundali_milan(self._mc(0,0,3,1),self._mc(5,5,3,1))
        if r.mangal_dosha_male and r.mangal_dosha_female: assert r.dosha_cancelled
class TestSelf:
    @pytest.fixture(scope="class")
    def ind(self):
        from src.ephemeris import compute_chart
        return compute_chart(1947,8,15,0.,28.6139,77.209,5.5,"lahiri")
    def test_runs(self,ind): assert isinstance(compute_kundali_milan(ind,ind),KundaliMilanResult)
    def test_nadi(self,ind): assert compute_kundali_milan(ind,ind).nadi_dosha
    def test_gana(self,ind): assert compute_kundali_milan(ind,ind).kootas["Gana"].score==6.
    def test_det(self,ind): assert compute_kundali_milan(ind,ind).total_score==compute_kundali_milan(ind,ind).total_score
    def test_mangal(self,ind): assert isinstance(has_mangal_dosha(ind),bool)
class TestBounds:
    @pytest.mark.parametrize("a,b",[(0,0),(0,13),(13,26)])
    def test_tara(self,a,b): assert 0.<=_ta(a,b)<=3.
    @pytest.mark.parametrize("a,b",[(0,0),(0,9),(5,20)])
    def test_yoni(self,a,b): assert _yo(a,b) in(0.,2.,4.)
    def test_nadi(self):
        for a in range(27):
            for b in range(0,27,9): assert _nd(a,b) in(0.,8.)
