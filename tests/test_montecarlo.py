"""tests/test_montecarlo.py — Monte Carlo sensitivity tests (Session 11, 20 tests)"""
import pytest
from datetime import date
from src.montecarlo import compute_sensitivity, SensitivityReport, HouseSensitivity

INDIA=dict(year=1947,month=8,day=15,hour=0.0,lat=28.6139,lon=77.209,tz_offset=5.5,ayanamsha="lahiri")

class TestReportStructure:
    def test_returns_sensitivity_report(self):
        assert isinstance(compute_sensitivity(**INDIA,n_samples=5,seed=42),SensitivityReport)
    def test_n_samples_recorded(self):
        assert compute_sensitivity(**INDIA,n_samples=7,seed=42).n_samples==7
    def test_window_minutes_recorded(self):
        assert compute_sensitivity(**INDIA,n_samples=5,window_minutes=15,seed=42).birth_time_window_minutes==15
    def test_twelve_houses_present(self):
        assert set(compute_sensitivity(**INDIA,n_samples=5,seed=42).houses.keys())==set(range(1,13))
    def test_house_sensitivity_fields(self):
        hs=compute_sensitivity(**INDIA,n_samples=5,seed=42).houses[1]
        assert isinstance(hs,HouseSensitivity)
        for a in("mean_score","std_score","min_score","max_score","score_range","rating_mode","stable"):
            assert hasattr(hs,a)
    def test_stable_flag_type(self):
        for hs in compute_sensitivity(**INDIA,n_samples=5,seed=42).houses.values():
            assert isinstance(hs.stable,bool)
    def test_dominant_lagna_nonempty(self):
        r=compute_sensitivity(**INDIA,n_samples=5,seed=42)
        assert isinstance(r.dominant_lagna,str) and len(r.dominant_lagna)>0

class TestStatistics:
    def test_scores_in_valid_range(self):
        for hs in compute_sensitivity(**INDIA,n_samples=10,seed=42).houses.values():
            assert -10.0<=hs.min_score<=hs.max_score<=10.0
    def test_std_nonnegative(self):
        for hs in compute_sensitivity(**INDIA,n_samples=10,seed=42).houses.values():
            assert hs.std_score>=0.0
    def test_range_equals_max_minus_min(self):
        for hs in compute_sensitivity(**INDIA,n_samples=10,seed=42).houses.values():
            assert abs(hs.score_range-(hs.max_score-hs.min_score))<1e-6
    def test_mean_between_min_and_max(self):
        for hs in compute_sensitivity(**INDIA,n_samples=10,seed=42).houses.values():
            assert hs.min_score-1e-9<=hs.mean_score<=hs.max_score+1e-9
    def test_lagna_stability_in_unit_interval(self):
        r=compute_sensitivity(**INDIA,n_samples=20,seed=42)
        assert 0.0<=r.lagna_stability<=1.0
    def test_dasha_stability_default_one(self):
        assert compute_sensitivity(**INDIA,n_samples=5,seed=42).dasha_stability==1.0
    def test_dasha_stability_with_birth_date(self):
        r=compute_sensitivity(**INDIA,n_samples=10,seed=42,birth_date=date(1947,8,15))
        assert 0.0<=r.dasha_stability<=1.0 and r.dominant_md_lord!="N/A"

class TestEdgeCases:
    def test_single_sample(self):
        r=compute_sensitivity(**INDIA,n_samples=1,seed=42)
        for hs in r.houses.values(): assert hs.std_score==0.0
    def test_zero_window_all_identical(self):
        r=compute_sensitivity(**INDIA,n_samples=5,window_minutes=0,seed=42)
        for hs in r.houses.values(): assert hs.std_score==0.0
    def test_midnight_birth_no_error(self):
        assert isinstance(compute_sensitivity(**INDIA,n_samples=10,seed=42),SensitivityReport)
    def test_non_ist_timezone(self):
        assert isinstance(compute_sensitivity(year=2000,month=6,day=21,hour=12.0,
            lat=51.5074,lon=-0.1278,tz_offset=0.0,n_samples=5,seed=42),SensitivityReport)

class TestDeterminism:
    def test_same_seed_same_result(self):
        r1=compute_sensitivity(**INDIA,n_samples=8,seed=7)
        r2=compute_sensitivity(**INDIA,n_samples=8,seed=7)
        for h in range(1,13):
            assert r1.houses[h].mean_score==r2.houses[h].mean_score
    def test_different_seeds_vary(self):
        r1=compute_sensitivity(**INDIA,n_samples=20,seed=1)
        r2=compute_sensitivity(**INDIA,n_samples=20,seed=2)
        assert any(abs(r1.houses[h].mean_score-r2.houses[h].mean_score)>0 for h in range(1,13))

class TestIndiaChart1947:
    def test_dominant_lagna(self):
        r=compute_sensitivity(**INDIA,n_samples=30,seed=42)
        assert r.dominant_lagna in("Taurus","Aries","Gemini")
    def test_most_houses_stable(self):
        r=compute_sensitivity(**INDIA,n_samples=20,seed=42)
        assert sum(1 for hs in r.houses.values() if hs.std_score<1.0)>=8
