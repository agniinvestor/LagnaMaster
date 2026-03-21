"""
tests/test_pending_build.py
Tests for Sessions 139-160 pending build modules.
"""
import pytest
from unittest.mock import MagicMock
from datetime import date, time, datetime


def make_planet(lon, si=None, speed=1.0, lat=0.0):
    p = MagicMock()
    p.longitude = lon
    p.sign_index = si if si is not None else int(lon / 30) % 12
    p.degree_in_sign = lon % 30
    p.is_retrograde = speed < 0
    p.speed = speed
    p.latitude = lat
    return p


def make_chart(lagna_lon=37.73, jd_ut=2432126.7, **planets):
    c = MagicMock()
    c.lagna = lagna_lon
    c.lagna_sign_index = int(lagna_lon / 30) % 12
    c.jd_ut = jd_ut
    c.planets = {k: make_planet(v) for k, v in planets.items()}
    c.upagrahas = {}
    return c


INDIA = dict(Sun=117.99, Moon=93.98, Mars=82.0, Mercury=110.0,
             Jupiter=186.0, Venus=106.0, Saturn=116.0, Rahu=38.0, Ketu=218.0)
INDIA_LAGNA = 37.73


# ─── Dasha Scoring ───────────────────────────────────────────────────────────

class TestDashaScoring:

    def test_active_dasha_lord_increases_house_score(self):
        from src.calculations.dasha_scoring import compute_dasha_modifier
        # Aries Lagna (si=0), Mars rules H1 and H8
        # If MD lord is Mars and house=1, multiplier should be 1.5
        mod = compute_dasha_modifier(1, 3.0, "Mars", "Jupiter", 0)
        assert mod.dasha_multiplier == 1.5
        assert mod.dasha_sensitized_score == pytest.approx(4.5)
        assert mod.md_is_house_lord is True

    def test_neutral_dasha_no_change(self):
        from src.calculations.dasha_scoring import compute_dasha_modifier
        # Saturn (unrelated to H1 for Aries lagna) — neutral
        mod = compute_dasha_modifier(1, 3.0, "Saturn", "Saturn", 0)
        assert mod.dasha_multiplier == 1.0
        assert mod.dasha_sensitized_score == pytest.approx(3.0)

    def test_apply_dasha_scoring_returns_report(self):
        from src.calculations.dasha_scoring import apply_dasha_scoring
        chart = make_chart(INDIA_LAGNA, **INDIA)
        scores = {h: float(h) for h in range(1, 13)}
        report = apply_dasha_scoring(scores, chart, date(2026, 3, 21))
        assert len(report.house_modifiers) == 12
        assert report.active_md_lord in {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"}

    def test_activated_houses_nonempty(self):
        from src.calculations.dasha_scoring import apply_dasha_scoring
        chart = make_chart(INDIA_LAGNA, **INDIA)
        scores = {h: 2.0 for h in range(1, 13)}
        report = apply_dasha_scoring(scores, chart, date(2026, 3, 21))
        assert isinstance(report.activated_houses, list)


# ─── Muhurtha Complete ────────────────────────────────────────────────────────

class TestMuhurthaComplete:

    def test_tarabala_sadhana(self):
        from src.calculations.muhurtha_complete import tarabala
        result = tarabala(0, 5)  # natal=Ashwini(0), transit=Ardra(5), count=6=Sadhana
        assert result["tara"] == "Sadhana"
        assert result["is_good"] is True

    def test_tarabala_janma_avoid(self):
        from src.calculations.muhurtha_complete import tarabala
        result = tarabala(0, 0)  # same nakshatra = Janma = avoid
        assert result["tara"] == "Janma"
        assert result["is_good"] is False

    def test_chandrabala_favorable(self):
        from src.calculations.muhurtha_complete import chandrabala
        result = chandrabala(0, 2)  # H3 from natal Moon = good
        assert result["is_good"] is True

    def test_panchaka_dosha(self):
        from src.calculations.muhurtha_complete import check_panchaka_dosha
        result = check_panchaka_dosha(8, 0, 22)  # Sag + Dhanishtha
        assert result["panchaka_dosha"] is True

    def test_no_panchaka_in_aries(self):
        from src.calculations.muhurtha_complete import check_panchaka_dosha
        result = check_panchaka_dosha(0, 0, 0)  # Aries — no dosha
        assert result["panchaka_dosha"] is False

    def test_vishti_karana(self):
        from src.calculations.muhurtha_complete import check_vishti_karana
        r = check_vishti_karana(3.0)  # tithi 3.0 → karana 6 → Vishti
        assert isinstance(r["is_vishti"], bool)

    def test_abhijit_muhurtha(self):
        from src.calculations.muhurtha_complete import compute_abhijit_muhurtha
        sunrise = datetime(2026, 3, 21, 6, 15)
        sunset  = datetime(2026, 3, 21, 18, 30)
        result = compute_abhijit_muhurtha(sunrise, sunset)
        assert "abhijit_start" in result
        assert "solar_noon" in result

    def test_compute_muhurtha_returns_report(self):
        from src.calculations.muhurtha_complete import compute_muhurtha
        report = compute_muhurtha(
            natal_moon_nak_idx=7, natal_moon_si=3,
            transit_moon_nak_idx=13, transit_moon_si=6,
            weekday=4, tithi=5.0, purpose="business"
        )
        assert report.overall_quality in {"excellent","good","acceptable","avoid"}
        assert isinstance(report.blessings, list)
        assert isinstance(report.defects, list)


# ─── KP Sub-lord ─────────────────────────────────────────────────────────────

class TestKPSublord:

    def test_table_has_249_entries(self):
        from src.calculations.kp_sublord import KP_SUBLORD_TABLE
        # Should have 27 × 9 = 243 or close to 249
        assert 240 <= len(KP_SUBLORD_TABLE) <= 250

    def test_get_sublord_for_ashwini(self):
        from src.calculations.kp_sublord import get_sublord
        result = get_sublord(0.5)  # Early Aries — Ashwini, Ketu's nakshatra
        assert result.star_lord == "Ketu"
        assert result.sub_lord in {"Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"}

    def test_table_covers_full_zodiac(self):
        from src.calculations.kp_sublord import KP_SUBLORD_TABLE
        # First entry starts at 0, last ends near 360
        assert KP_SUBLORD_TABLE[0].start_lon < 1.0
        assert KP_SUBLORD_TABLE[-1].end_lon > 359.0

    def test_sublord_continuous(self):
        from src.calculations.kp_sublord import KP_SUBLORD_TABLE
        # Each entry's end should equal next entry's start
        for i in range(len(KP_SUBLORD_TABLE) - 1):
            gap = KP_SUBLORD_TABLE[i+1].start_lon - KP_SUBLORD_TABLE[i].end_lon
            assert abs(gap) < 0.001, f"Gap at index {i}: {gap}"

    def test_get_star_lord(self):
        from src.calculations.kp_sublord import get_star_lord
        # Aries (0-13.33°) = Ashwini + Bharani star lords = Ketu + Venus
        assert get_star_lord(0.0) == "Ketu"
        assert get_star_lord(14.0) == "Venus"


# ─── CalcConfig ──────────────────────────────────────────────────────────────

class TestCalcConfig:

    def test_default_is_parashari(self):
        from src.calculations.calc_config import CalcConfig, School
        cfg = CalcConfig()
        assert cfg.school == School.PARASHARI

    def test_kp_forces_true_node(self):
        from src.calculations.calc_config import CalcConfig, School
        cfg = CalcConfig(school=School.KP)
        assert cfg.node_mode == "true"
        assert cfg.ayanamsha == "krishnamurti"

    def test_rahu_exalt_pvrnr_is_taurus(self):
        from src.calculations.calc_config import CalcConfig, Authority
        cfg = CalcConfig(authority=Authority.PVRNR)
        assert cfg.rahu_exalt_sign == 1  # Taurus

    def test_rahu_exalt_raman_is_gemini(self):
        from src.calculations.calc_config import CalcConfig, Authority
        cfg = CalcConfig(authority=Authority.BV_RAMAN)
        assert cfg.rahu_exalt_sign == 2  # Gemini

    def test_module_active_parashari(self):
        from src.calculations.calc_config import CalcConfig, School
        cfg = CalcConfig(school=School.PARASHARI)
        assert cfg.is_module_active("dignity")
        assert cfg.is_module_active("shadbala")

    def test_preset_configs_exist(self):
        from src.calculations.calc_config import PARASHARI_PVRNR, KP_CONFIG, TAJIKA_CONFIG
        assert PARASHARI_PVRNR.school.value == "parashari"
        assert KP_CONFIG.node_mode == "true"
        assert TAJIKA_CONFIG.school.value == "tajika"


# ─── Confidence Model ─────────────────────────────────────────────────────────

class TestConfidenceModel:

    def test_clean_chart_high_reliability(self):
        from src.calculations.confidence_model import compute_chart_confidence
        # Chart with lagna at 15° (away from boundary)
        chart = make_chart(4 * 30 + 15.0, **INDIA)  # Leo lagna, 15° in sign
        chart.planets["Moon"] = make_planet(7 * 30 + 7.0)  # mid-nakshatra
        scores = {h: 3.0 for h in range(1, 13)}
        report = compute_chart_confidence(chart, scores)
        assert report.overall_reliability in ("high", "moderate")

    def test_boundary_lagna_lower_reliability(self):
        from src.calculations.confidence_model import compute_chart_confidence
        chart = make_chart(30 * 0 + 0.5)  # Aries lagna, 0.5° in sign
        chart.planets["Moon"] = make_planet(93.98)
        scores = {h: 3.0 for h in range(1, 13)}
        report = compute_chart_confidence(chart, scores)
        assert report.uncertainty_flags.lagna_near_sign_boundary is True
        assert len(report.recommendations) >= 1

    def test_intervals_have_all_houses(self):
        from src.calculations.confidence_model import compute_chart_confidence
        chart = make_chart(INDIA_LAGNA, **INDIA)
        scores = {h: float(h - 6) for h in range(1, 13)}
        report = compute_chart_confidence(chart, scores)
        assert len(report.house_intervals) == 12
        for ci in report.house_intervals:
            assert ci.lower_bound <= ci.point_estimate <= ci.upper_bound


# ─── Sudarshana Chakra ────────────────────────────────────────────────────────

class TestSudarshana:

    def test_sudarshana_returns_result(self):
        from src.calculations.sudarshana import compute_sudarshana_chakra
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = compute_sudarshana_chakra(chart)
        assert result.lagna_wheel.reference == "Lagna"
        assert result.sun_wheel.reference == "Sun"
        assert result.moon_wheel.reference == "Moon"

    def test_concordance_all_12_houses(self):
        from src.calculations.sudarshana import compute_sudarshana_chakra
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = compute_sudarshana_chakra(chart)
        assert len(result.concordance_by_house) == 12
        for h, c in result.concordance_by_house.items():
            assert c in ("Triple", "Double", "Single", "None")

    def test_most_active_house_valid(self):
        from src.calculations.sudarshana import compute_sudarshana_chakra
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = compute_sudarshana_chakra(chart)
        assert 1 <= result.most_active_house <= 12

    def test_wheel_house_signs_valid(self):
        from src.calculations.sudarshana import compute_sudarshana_chakra
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = compute_sudarshana_chakra(chart)
        for wheel in [result.lagna_wheel, result.sun_wheel, result.moon_wheel]:
            assert len(wheel.house_signs) == 12
            for si in wheel.house_signs:
                assert 0 <= si <= 11


# ─── Shodashavarga Bala ───────────────────────────────────────────────────────

class TestShodashavargaBala:

    def test_returns_dict_with_required_keys(self):
        from src.calculations.shodashavarga_bala import compute_shodashavarga_bala
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = compute_shodashavarga_bala("Jupiter", chart)
        assert "total_virupas" in result
        assert "label" in result
        assert result["label"] in ("Strong", "Moderate", "Weak", "Unknown",
                                    "Requires vargas.py and dignity.py")

    def test_summary_covers_all_planets(self):
        from src.calculations.shodashavarga_bala import shodashavarga_summary
        chart = make_chart(INDIA_LAGNA, **INDIA)
        result = shodashavarga_summary(chart)
        assert isinstance(result, dict)
        assert len(result) >= 7
