"""tests/test_montecarlo.py — 20 tests (Session 11)"""
import pytest; from datetime import date
from src.montecarlo import compute_sensitivity,SensitivityReport,HouseSensitivity
I=dict(year=1947,month=8,day=15,hour=0.0,lat=28.6139,lon=77.209,tz_offset=5.5,ayanamsha="lahiri")
class TestReportStructure:
    def test_type(self): assert isinstance(compute_sensitivity(**I,n_samples=5,seed=42),SensitivityReport)
    def test_n(self): assert compute_sensitivity(**I,n_samples=7,seed=42).n_samples==7
    def test_window(self): assert compute_sensitivity(**I,n_samples=5,window_minutes=15,seed=42).birth_time_window_minutes==15
    def test_12_houses(self): assert set(compute_sensitivity(**I,n_samples=5,seed=42).houses.keys())==set(range(1,13))
    def test_fields(self):
        hs=compute_sensitivity(**I,n_samples=5,seed=42).houses[1]
        for a in("mean_score","std_score","min_score","max_score","score_range","rating_mode","stable"): assert hasattr(hs,a)
    def test_stable_bool(self):
        for hs in compute_sensitivity(**I,n_samples=5,seed=42).houses.values(): assert isinstance(hs.stable,bool)
    def test_dominant_lagna(self): assert len(compute_sensitivity(**I,n_samples=5,seed=42).dominant_lagna)>0
class TestStatistics:
    def test_range(self):
        for hs in compute_sensitivity(**I,n_samples=10,seed=42).houses.values(): assert -10.0<=hs.min_score<=hs.max_score<=10.0
    def test_std_nn(self):
        for hs in compute_sensitivity(**I,n_samples=10,seed=42).houses.values(): assert hs.std_score>=0.0
    def test_range_eq(self):
        for hs in compute_sensitivity(**I,n_samples=10,seed=42).houses.values(): assert abs(hs.score_range-(hs.max_score-hs.min_score))<1e-6
    def test_mean_btw(self):
        for hs in compute_sensitivity(**I,n_samples=10,seed=42).houses.values(): assert hs.min_score-1e-9<=hs.mean_score<=hs.max_score+1e-9
    def test_lagna_stab(self): assert 0.0<=compute_sensitivity(**I,n_samples=20,seed=42).lagna_stability<=1.0
    def test_dasha_default(self): assert compute_sensitivity(**I,n_samples=5,seed=42).dasha_stability==1.0
    def test_dasha_with_date(self):
        r=compute_sensitivity(**I,n_samples=10,seed=42,birth_date=date(1947,8,15))
        assert 0.0<=r.dasha_stability<=1.0 and r.dominant_md_lord!="N/A"
class TestEdgeCases:
    def test_n1(self):
        for hs in compute_sensitivity(**I,n_samples=1,seed=42).houses.values(): assert hs.std_score==0.0
    def test_w0(self):
        for hs in compute_sensitivity(**I,n_samples=5,window_minutes=0,seed=42).houses.values(): assert hs.std_score==0.0
    def test_midnight(self): assert isinstance(compute_sensitivity(**I,n_samples=10,seed=42),SensitivityReport)
    def test_non_ist(self): assert isinstance(compute_sensitivity(2000,6,21,12.0,51.5,-0.13,0.0,n_samples=5,seed=42),SensitivityReport)
class TestDeterminism:
    def test_same_seed(self):
        r1=compute_sensitivity(**I,n_samples=8,seed=7); r2=compute_sensitivity(**I,n_samples=8,seed=7)
        for h in range(1,13): assert r1.houses[h].mean_score==r2.houses[h].mean_score
    def test_diff_seeds(self):
        r1=compute_sensitivity(**I,n_samples=20,seed=1); r2=compute_sensitivity(**I,n_samples=20,seed=2)
        assert any(abs(r1.houses[h].mean_score-r2.houses[h].mean_score)>0 for h in range(1,13))
class TestIndiaChart1947:
    def test_lagna(self): assert compute_sensitivity(**I,n_samples=30,seed=42).dominant_lagna in("Taurus","Aries","Gemini")
    def test_stable(self): assert sum(1 for hs in compute_sensitivity(**I,n_samples=20,seed=42).houses.values() if hs.std_score<1.0)>=8
