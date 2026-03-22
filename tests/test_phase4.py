"""tests/test_phase4.py — Sessions 28–32 Phase 4 tests."""

from __future__ import annotations
import pytest
from datetime import date

INDIA = dict(
    year=1947,
    month=8,
    day=15,
    hour=0.0,
    lat=28.6139,
    lon=77.2090,
    tz_offset=5.5,
    ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA)


@pytest.fixture(scope="module")
def dashas(chart):
    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

    return compute_vimshottari_dasa(chart, date(1947, 8, 15))


# ── Session 28: Functional Roles ─────────────────────────────────────────────
class TestFunctionalRoles:
    def test_returns_functional_roles(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert r.lagna_sign == "Taurus"

    def test_taurus_yogakaraka_is_saturn(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert "Saturn" in r.yogakarakas

    def test_taurus_badhaka_house_is_12(self, chart):
        # Taurus = fixed sign → badhaka = H9? No: fixed (1,4,7,10) → H9
        # Wait: Taurus si=1 → fixed → badhaka=H9
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert r.badhaka_house == 9

    def test_badhaka_lord_set(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert r.badhaka_lord != ""

    def test_maraka_lords_are_two_planets(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert len(r.maraka_lords) == 2

    def test_dusthana_lords_set(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert len(r.dusthana_lords) >= 2

    def test_house_lords_has_12_entries(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert len(r.house_lords) == 12

    def test_is_yogakaraka_method(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        assert r.is_yogakaraka("Saturn") is True
        assert r.is_yogakaraka("Sun") is False

    def test_all_seven_planets_classified(self, chart):
        from src.calculations.functional_roles import compute_functional_roles

        r = compute_functional_roles(chart)
        all_classified = set(
            r.functional_benefics + r.functional_malefics + r.functional_neutrals
        )
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            assert p in all_classified, f"{p} not classified"


# ── Session 29: Avastha ───────────────────────────────────────────────────────
class TestAvastha:
    def test_deeptadi_returns_valid_state(self, chart):
        from src.calculations.avastha import compute_deeptadi, DEEPTADI_STATES

        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            s = compute_deeptadi(p, chart)
            assert s in DEEPTADI_STATES

    def test_baladi_returns_valid_state(self, chart):
        from src.calculations.avastha import compute_baladi, BALADI_STATES

        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            s = compute_baladi(p, chart)
            assert s in BALADI_STATES

    def test_lajjitadi_returns_result(self, chart):
        from src.calculations.avastha import compute_lajjitadi, LAJJITADI_STATES

        r = compute_lajjitadi(chart)
        assert r.state in LAJJITADI_STATES
        assert 0.0 <= r.pressure_score <= 1.0

    def test_lajjitadi_has_fifth_lord(self, chart):
        from src.calculations.avastha import compute_lajjitadi

        r = compute_lajjitadi(chart)
        assert r.fifth_lord != ""

    def test_all_avasthas_has_effective_multipliers(self, chart):
        from src.calculations.avastha import compute_all_avasthas

        r = compute_all_avasthas(chart)
        assert len(r.effective_multipliers) == 7
        for p, m in r.effective_multipliers.items():
            assert 0.0 <= m <= 1.5

    def test_baladi_yuva_highest_multiplier(self):
        from src.calculations.avastha import BALADI_STATES

        assert (
            BALADI_STATES["Yuva"]["multiplier"] > BALADI_STATES["Mrita"]["multiplier"]
        )


# ── Session 30: Pressure Engine ──────────────────────────────────────────────
class TestPressureEngine:
    def test_compute_pressure_index_returns_point(self, chart, dashas):
        from src.calculations.pressure_engine import compute_pressure_index

        p = compute_pressure_index(chart, dashas, date(2026, 3, 19))
        assert 0.0 <= p.pressure_index <= 10.0

    def test_pressure_label_valid(self, chart, dashas):
        from src.calculations.pressure_engine import compute_pressure_index

        p = compute_pressure_index(chart, dashas, date(2026, 3, 19))
        assert p.label in {
            "Tranquil",
            "Mild",
            "Moderate",
            "Elevated",
            "High",
            "Critical",
        }

    def test_structural_vulnerability_returns_float(self, chart):
        from src.calculations.pressure_engine import structural_vulnerability

        v, drivers = structural_vulnerability(chart)
        assert 0.0 <= v <= 10.0
        assert isinstance(drivers, list)

    def test_dasha_activation_returns_float(self, chart, dashas):
        from src.calculations.pressure_engine import dasha_activation_weight

        w, note = dasha_activation_weight(chart, dashas, date(2026, 3, 19))
        assert 0.1 <= w <= 2.0

    def test_transit_load_returns_float(self, chart):
        from src.calculations.pressure_engine import transit_load

        t, note = transit_load(chart, date(2026, 3, 19))
        assert 0.1 <= t <= 2.0

    def test_resilience_factor_returns_float(self, chart, dashas):
        from src.calculations.pressure_engine import resilience_factor

        r, note = resilience_factor(chart, dashas, date(2026, 3, 19))
        assert 0.5 <= r <= 2.0

    def test_pressure_timeline_returns_list(self, chart, dashas):
        from src.calculations.pressure_engine import compute_pressure_timeline

        pts = compute_pressure_timeline(
            chart,
            dashas,
            from_date=date(2026, 1, 1),
            to_date=date(2026, 12, 31),
            step_months=3,
        )
        assert len(pts) >= 4
        for p in pts:
            assert 0.0 <= p.pressure_index <= 10.0

    def test_pressure_point_has_drivers(self, chart, dashas):
        from src.calculations.pressure_engine import compute_pressure_index

        p = compute_pressure_index(chart, dashas, date(2026, 3, 19))
        assert isinstance(p.key_drivers, list)

    def test_is_critical_property(self, chart, dashas):
        from src.calculations.pressure_engine import PressurePoint

        high = PressurePoint(date.today(), 8.0, "High", 6.0, 1.5, 1.5, 1.0)
        low = PressurePoint(date.today(), 2.0, "Mild", 2.0, 1.0, 1.0, 1.0)
        assert high.is_critical is True
        assert low.is_critical is False


# ── Session 31: Argala + Arudha ───────────────────────────────────────────────
class TestArgala:
    def test_argala_returns_result(self, chart):
        from src.calculations.argala import compute_argala

        r = compute_argala(chart, reference_house=1)
        assert r.reference_house == 1
        assert isinstance(r.net_argala_score, float)

    def test_argala_entries_have_valid_types(self, chart):
        from src.calculations.argala import compute_argala

        r = compute_argala(chart)
        for e in r.entries:
            assert e.net_effect in {"supports", "obstructs", "cancelled", "neutral"}
            assert e.nature in {"benefic_argala", "malefic_argala", "mixed"}

    def test_arudha_lagna_returns_result(self, chart):
        from src.calculations.argala import compute_arudha_lagna

        r = compute_arudha_lagna(chart)
        assert r.arudha_lagna_sign in [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]

    def test_arudha_condition_valid(self, chart):
        from src.calculations.argala import compute_arudha_lagna

        r = compute_arudha_lagna(chart)
        assert r.al_condition in {"Strong", "Afflicted", "Mixed", "Neutral"}

    def test_arudha_lagna_lord_is_planet(self, chart):
        from src.calculations.argala import compute_arudha_lagna

        r = compute_arudha_lagna(chart)
        assert r.lagna_lord in [
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
        ]


# ── Session 32: Graha Yuddha + Scoring v2 ────────────────────────────────────
class TestGrahaYuddha:
    def test_returns_list(self, chart):
        from src.calculations.graha_yuddha import compute_graha_yuddha

        result = compute_graha_yuddha(chart)
        assert isinstance(result, list)

    def test_war_planets_only_five(self, chart):
        from src.calculations.graha_yuddha import compute_graha_yuddha, _WAR_PLANETS

        for war in compute_graha_yuddha(chart):
            assert war.winner in _WAR_PLANETS
            assert war.loser in _WAR_PLANETS

    def test_separation_under_one_degree(self, chart):
        from src.calculations.graha_yuddha import compute_graha_yuddha

        for war in compute_graha_yuddha(chart):
            assert war.separation_degrees <= 1.0


class TestScoringV2:
    def test_returns_chart_scores_v2(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2, ChartScoresV2

        result = score_chart_v2(chart)
        assert isinstance(result, ChartScoresV2)

    def test_engine_version_present(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2, ENGINE_VERSION

        result = score_chart_v2(chart)
        assert result.engine_version == ENGINE_VERSION

    def test_twelve_houses_present(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2

        result = score_chart_v2(chart)
        assert len(result.houses) == 12

    def test_scores_within_bounds(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2

        result = score_chart_v2(chart)
        for h, hs in result.houses.items():
            assert -10.0 <= hs.final_score <= 10.0

    def test_lagna_sign_correct(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2

        result = score_chart_v2(chart)
        assert result.lagna_sign == "Taurus"

    def test_functional_malefic_bhavesh_flag(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2

        result = score_chart_v2(chart)
        for h, hs in result.houses.items():
            assert isinstance(hs.functional_malefic_bhavesh, bool)

    def test_v2_deterministic(self, chart):
        from src.calculations.scoring_v2 import score_chart_v2

        r1 = score_chart_v2(chart)
        r2 = score_chart_v2(chart)
        for h in range(1, 13):
            assert r1.houses[h].final_score == r2.houses[h].final_score
