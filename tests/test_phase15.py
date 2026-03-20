"""tests/test_phase15.py — Phases 15-18: Muhurta, Prashna, Dashas, Upaya, Mundane"""
from __future__ import annotations
import pytest
from datetime import date, datetime

INDIA = dict(year=1947,month=8,day=15,hour=0.0,lat=28.6139,lon=77.2090,
             tz_offset=5.5,ayanamsha="lahiri")
BD = date(1947, 8, 15)

@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA)

# ── Panchanga ────────────────────────────────────────────────────────────────
class TestPanchanga:
    def test_compute_panchanga(self, chart):
        from src.calculations.panchanga import compute_panchanga
        sun_lon = chart.planets["Sun"].longitude
        moon_lon = chart.planets["Moon"].longitude
        p = compute_panchanga(sun_lon, moon_lon, datetime(1947,8,15,0,0))
        assert 1 <= p.tithi <= 30
        assert 0 <= p.nakshatra <= 26
        assert 0 <= p.yoga <= 26
        assert p.paksha in {"Shukla","Krishna"}
        assert isinstance(p.amrita_siddhi, bool)
        assert isinstance(p.sarvaartha_siddhi, bool)

    def test_tithi_calculation(self):
        from src.calculations.panchanga import compute_panchanga
        # Full Moon: Sun=0°, Moon=180° → tithi=15
        p = compute_panchanga(0.0, 180.0, datetime.now())
        assert p.tithi in {15, 16}  # 180° is boundary between Purnima and Krishna Pratipada

    def test_nakshatra_range(self, chart):
        from src.calculations.panchanga import compute_panchanga
        p = compute_panchanga(chart.planets["Sun"].longitude,
                              chart.planets["Moon"].longitude)
        assert p.nakshatra_name in [
            "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
            "Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni",
            "Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha",
            "Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana",
            "Dhanishtha","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati",
        ]

    def test_hora_returns_planet(self):
        from src.calculations.panchanga import compute_hora
        lord, num = compute_hora(datetime.now())
        assert lord in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
        assert 1 <= num <= 24

    def test_choghadiya(self):
        from src.calculations.panchanga import compute_choghadiya
        r = compute_choghadiya(datetime.now())
        assert "choghadiya" in r
        assert r["quality"] in {"Excellent","Good","Neutral","Unfavorable"}

# ── Muhurta ──────────────────────────────────────────────────────────────────
class TestMuhurta:
    def test_score_muhurta(self, chart):
        from src.calculations.panchanga import compute_panchanga
        from src.calculations.muhurta import score_muhurta
        p = compute_panchanga(chart.planets["Sun"].longitude,
                              chart.planets["Moon"].longitude)
        s = score_muhurta("marriage", p)
        assert 0 <= s.total_score <= 7
        assert s.quality in {"Excellent","Good","Acceptable","Avoid"}

    def test_all_tasks(self, chart):
        from src.calculations.panchanga import compute_panchanga
        from src.calculations.muhurta import score_muhurta, _TASK_RULES
        p = compute_panchanga(chart.planets["Sun"].longitude,
                              chart.planets["Moon"].longitude)
        for task in _TASK_RULES:
            s = score_muhurta(task, p)
            assert s.task == task

    def test_warnings_are_strings(self, chart):
        from src.calculations.panchanga import compute_panchanga
        from src.calculations.muhurta import score_muhurta
        p = compute_panchanga(chart.planets["Sun"].longitude,
                              chart.planets["Moon"].longitude)
        s = score_muhurta("travel", p)
        for w in s.warnings:
            assert isinstance(w, str)

# ── Prashna ──────────────────────────────────────────────────────────────────
class TestPrashna:
    def test_analyze_prashna(self, chart):
        from src.calculations.prashna import analyze_prashna
        r = analyze_prashna(chart, "general")
        assert r.hora_lord in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
        assert r.verdict
        assert r.confidence in {"High","Moderate","Low"}

    def test_all_query_types(self, chart):
        from src.calculations.prashna import analyze_prashna, _PRASHNA_QUERY_HOUSES
        for qt in _PRASHNA_QUERY_HOUSES:
            r = analyze_prashna(chart, qt)
            assert r.key_house == _PRASHNA_QUERY_HOUSES[qt]

    def test_reasoning_nonempty(self, chart):
        from src.calculations.prashna import analyze_prashna
        r = analyze_prashna(chart, "career")
        assert len(r.reasoning) >= 1

# ── Kalachakra Dasha ─────────────────────────────────────────────────────────
class TestKalachakraDasha:
    def test_returns_periods(self, chart):
        from src.calculations.kalachakra_dasha import compute_kalachakra_dasha
        periods = compute_kalachakra_dasha(chart, BD)
        assert len(periods) > 0

    def test_periods_continuous(self, chart):
        from src.calculations.kalachakra_dasha import compute_kalachakra_dasha
        periods = compute_kalachakra_dasha(chart, BD)
        for i in range(1, min(5, len(periods))):
            assert periods[i].start_date == periods[i-1].end_date

    def test_deha_jeeva_flags(self, chart):
        from src.calculations.kalachakra_dasha import compute_kalachakra_dasha
        periods = compute_kalachakra_dasha(chart, BD)
        deha = [p for p in periods if p.is_deha]
        jeeva = [p for p in periods if p.is_jeeva]
        assert len(deha) >= 1
        assert len(jeeva) >= 1

    def test_current_period(self, chart):
        from src.calculations.kalachakra_dasha import current_kalachakra_period
        p = current_kalachakra_period(chart, BD, date(2026,3,21))
        if p:
            assert p.sign in ["Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg","Cp","Aq","Pi"]

# ── Shoola Dasha + Sudasa ─────────────────────────────────────────────────────
class TestShoolaSudasa:
    def test_shoola_dasha(self, chart):
        from src.calculations.shoola_dasha import compute_shoola_dasha
        periods = compute_shoola_dasha(chart, BD)
        assert len(periods) >= 12

    def test_sudasa(self, chart):
        from src.calculations.shoola_dasha import compute_sudasa
        periods = compute_sudasa(chart, BD)
        assert len(periods) >= 12

    def test_trishoola_flags(self, chart):
        from src.calculations.shoola_dasha import compute_shoola_dasha
        periods = compute_shoola_dasha(chart, BD)
        trishoola = [p for p in periods if p.trishoola_spike]
        assert len(trishoola) == 3  # exactly 3 trishoola spikes per cycle

    def test_sudasa_planets_per_sign(self, chart):
        from src.calculations.shoola_dasha import compute_sudasa
        periods = compute_sudasa(chart, BD)
        for p in periods:
            assert isinstance(p.planets_in_sign, list)

# ── Tara Dasha ────────────────────────────────────────────────────────────────
class TestTaraDasha:
    def test_returns_periods(self, chart):
        from src.calculations.tara_dasha import compute_tara_dasha
        periods = compute_tara_dasha(chart, BD)
        assert len(periods) > 0

    def test_tara_categories(self, chart):
        from src.calculations.tara_dasha import compute_tara_dasha, _TARA_NAMES
        periods = compute_tara_dasha(chart, BD)
        for p in periods[:9]:
            assert p.tara_category in _TARA_NAMES

    def test_quality_strings(self, chart):
        from src.calculations.tara_dasha import compute_tara_dasha
        periods = compute_tara_dasha(chart, BD)
        for p in periods[:9]:
            assert isinstance(p.tara_quality, str) and len(p.tara_quality) > 5

# ── Upaya ─────────────────────────────────────────────────────────────────────
class TestUpaya:
    def test_get_upaya(self):
        from src.calculations.upaya import get_upaya
        u = get_upaya("Jupiter", "debilitated")
        assert "Sapphire" in u.gemstone or "Yellow" in u.gemstone or u.gemstone
        assert u.primary_deity
        assert u.mantra_count > 0
        assert "not" in u.disclaimer.lower() or "classical" in u.disclaimer.lower()

    def test_all_planets(self):
        from src.calculations.upaya import get_upaya, _GEMSTONES
        for planet in _GEMSTONES:
            u = get_upaya(planet)
            assert u.planet == planet
            assert u.gemstone
            assert u.charitable_act

    def test_disclaimer_on_all(self):
        from src.calculations.upaya import get_upaya
        for planet in ["Sun","Moon","Mars"]:
            u = get_upaya(planet)
            assert "disclaimer" in u.__dataclass_fields__
            assert len(u.disclaimer) > 20

    def test_chart_upayas(self, chart):
        from src.calculations.upaya import get_chart_upayas
        upayas = get_chart_upayas(chart)
        assert isinstance(upayas, list)
        for u in upayas:
            assert u.planet

# ── Mundane ───────────────────────────────────────────────────────────────────
class TestMundane:
    def test_analyze_mundane(self, chart):
        from src.calculations.mundane import analyze_mundane_chart
        r = analyze_mundane_chart(chart, "nation", "India 1947", date(1947,8,15))
        assert r.chart_type == "nation"
        assert isinstance(r.key_themes, list)
        assert isinstance(r.challenges, list)
        assert len(r.house_significations) == 12

    def test_house_significations_complete(self):
        from src.calculations.mundane import _MUNDANE_HOUSES
        for h in range(1, 13):
            assert h in _MUNDANE_HOUSES
            assert len(_MUNDANE_HOUSES[h]) > 5

    def test_compress_vimshottari(self, chart):
        from src.calculations.mundane import compress_vimshottari
        r = compress_vimshottari(chart, BD, 1.0)
        assert len(r) >= 9

# ── Contextual ────────────────────────────────────────────────────────────────
class TestContextual:
    def test_contextual_flags(self, chart):
        from src.calculations.contextual import compute_contextual_flags
        f = compute_contextual_flags(chart, lat=28.6, birth_year=1947)
        assert isinstance(f.era_profession_hints, list)
        assert isinstance(f.high_latitude_warning, bool)
        assert "DKP" in f.practitioner_note or "Desha" in f.practitioner_note

    def test_high_latitude_flag(self, chart):
        from src.calculations.contextual import compute_contextual_flags
        f_high = compute_contextual_flags(chart, lat=65.0)
        f_low  = compute_contextual_flags(chart, lat=20.0)
        assert f_high.high_latitude_warning
        assert not f_low.high_latitude_warning

    def test_marriage_note_era(self, chart):
        from src.calculations.contextual import compute_contextual_flags
        f_old = compute_contextual_flags(chart, birth_year=1950)
        f_new = compute_contextual_flags(chart, birth_year=2000)
        assert f_old.cultural_marriage_note != f_new.cultural_marriage_note

# ── Ashtottari Dasha ──────────────────────────────────────────────────────────
class TestAshtottariDasha:
    def test_qualifies(self, chart):
        from src.calculations.ashtottari_dasha import qualifies_for_ashtottari
        result = qualifies_for_ashtottari(chart)
        assert isinstance(result, bool)

    def test_returns_periods(self, chart):
        from src.calculations.ashtottari_dasha import compute_ashtottari_dasha
        periods = compute_ashtottari_dasha(chart, BD)
        assert len(periods) > 0

    def test_total_years(self, chart):
        from src.calculations.ashtottari_dasha import compute_ashtottari_dasha, _ASHTO_YEARS
        periods = compute_ashtottari_dasha(chart, BD)
        # One cycle = 108 years
        cycle_years = sum(_ASHTO_YEARS)
        assert cycle_years == 108

    def test_periods_continuous(self, chart):
        from src.calculations.ashtottari_dasha import compute_ashtottari_dasha
        periods = compute_ashtottari_dasha(chart, BD)
        for i in range(1, min(5, len(periods))):
            assert periods[i].start_date == periods[i-1].end_date
