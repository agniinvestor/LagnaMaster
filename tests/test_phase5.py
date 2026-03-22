"""tests/test_phase5.py — Sessions 33–40 Phase 5 tests."""

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


ON_DATE = date(2026, 3, 20)


# ── Session 33: Multi-lagna + Arudha Padas ───────────────────────────────────
class TestMultiLagna:
    def test_chandra_lagna_ref_sign(self, chart):
        from src.calculations.multi_lagna import compute_chandra_lagna

        cl = compute_chandra_lagna(chart)
        assert cl.reference_sign == chart.planets["Moon"].sign

    def test_surya_lagna_ref_sign(self, chart):
        from src.calculations.multi_lagna import compute_surya_lagna

        sl = compute_surya_lagna(chart)
        assert sl.reference_sign == chart.planets["Sun"].sign

    def test_chandra_lagna_has_12_houses(self, chart):
        from src.calculations.multi_lagna import compute_chandra_lagna

        cl = compute_chandra_lagna(chart)
        assert len(cl.house_lord) == 12

    def test_yogakaraka_taurus_is_saturn(self):
        from src.calculations.multi_lagna import yogakaraka_for_lagna

        assert yogakaraka_for_lagna(1) == "Saturn"

    def test_yogakaraka_aries_is_none(self):
        from src.calculations.multi_lagna import yogakaraka_for_lagna

        assert yogakaraka_for_lagna(0) is None

    def test_all_arudha_padas_12_entries(self, chart):
        from src.calculations.multi_lagna import compute_all_arudha_padas

        r = compute_all_arudha_padas(chart)
        assert len(r.padas) == 12

    def test_arudha_lagna_is_pada1(self, chart):
        from src.calculations.multi_lagna import compute_all_arudha_padas

        r = compute_all_arudha_padas(chart)
        assert r.arudha_lagna == r.padas[1]

    def test_upapada_is_pada12(self, chart):
        from src.calculations.multi_lagna import compute_all_arudha_padas

        r = compute_all_arudha_padas(chart)
        assert r.upapada == r.padas[12]

    def test_karakamsha_returns_result(self, chart):
        from src.calculations.multi_lagna import compute_karakamsha

        kk = compute_karakamsha(chart)
        assert kk.atmakaraka in [
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
        ]

    def test_india_al_sign_virgo(self, chart):
        """1947 chart: AL should be Virgo (workbook CALC_ArudhaPada row 1)."""
        from src.calculations.multi_lagna import compute_all_arudha_padas

        r = compute_all_arudha_padas(chart)
        assert r.arudha_lagna.sign == "Virgo"


# ── Session 34: Multi-axis scoring ───────────────────────────────────────────
class TestMultiAxisScoring:
    def test_score_all_axes_returns_5_axes(self, chart):
        from src.calculations.multi_axis_scoring import score_all_axes

        m = score_all_axes(chart)
        assert m.d1 is not None
        assert m.cl is not None
        assert m.d9 is not None

    def test_all_axes_have_12_houses(self, chart):
        from src.calculations.multi_axis_scoring import score_all_axes

        m = score_all_axes(chart)
        for ax in [m.d1, m.cl, m.sl, m.d9, m.d10]:
            assert len(ax.scores) == 12

    def test_scores_within_bounds(self, chart):
        from src.calculations.multi_axis_scoring import score_all_axes

        m = score_all_axes(chart)
        for ax in [m.d1, m.cl, m.sl, m.d9, m.d10]:
            for s in ax.scores.values():
                assert -10.0 <= s <= 10.0

    def test_composite_formula(self, chart):
        from src.calculations.multi_axis_scoring import score_all_axes

        m = score_all_axes(chart)
        for h in range(1, 13):
            expected = round(
                m.d1.scores[h] * 0.5 + m.d9.scores[h] * 0.3 + m.d10.scores[h] * 0.2, 3
            )
            assert abs(m.composite(h) - expected) < 0.01

    def test_kp_school_different_weights(self, chart):
        from src.calculations.multi_axis_scoring import score_all_axes

        p = score_all_axes(chart, "parashari")
        k = score_all_axes(chart, "kp")
        # R04 weight differs (2.0 vs 1.5) so scores should differ for some house
        diffs = [abs(p.d1.scores[h] - k.d1.scores[h]) for h in range(1, 13)]
        assert max(diffs) > 0


# ── Session 35: Rule interactions ────────────────────────────────────────────
class TestRuleInteraction:
    def test_amplified_r04_r02(self):
        from src.calculations.rule_interaction import apply_rule_interactions

        fired = {"R04", "R02"}
        scores = {"R04": 2.0, "R02": 1.0}
        mod = apply_rule_interactions(fired, scores)
        assert mod > 0

    def test_neg_amplified_r09_r12(self):
        from src.calculations.rule_interaction import apply_rule_interactions

        fired = {"R09", "R12"}
        scores = {"R09": -1.0, "R12": -0.75}
        mod = apply_rule_interactions(fired, scores)
        assert mod < 0

    def test_no_interaction_when_only_one_fires(self):
        from src.calculations.rule_interaction import apply_rule_interactions

        fired = {"R04"}
        scores = {"R04": 2.0}
        mod = apply_rule_interactions(fired, scores)
        assert mod == 0.0


# ── Session 36: Full LPI ──────────────────────────────────────────────────────
class TestLPI:
    def test_compute_lpi_returns_result(self, chart, dashas):
        from src.calculations.lpi import compute_lpi

        r = compute_lpi(chart, dashas, ON_DATE)
        assert len(r.houses) == 12

    def test_lpi_within_bounds(self, chart, dashas):
        from src.calculations.lpi import compute_lpi

        r = compute_lpi(chart, dashas, ON_DATE)
        for h, hl in r.houses.items():
            assert -10.0 <= hl.full_index <= 10.0

    def test_domain_balance_four_domains(self, chart, dashas):
        from src.calculations.lpi import compute_lpi

        r = compute_lpi(chart, dashas, ON_DATE)
        assert set(r.domain_balance.keys()) == {"Dharma", "Artha", "Kama", "Moksha"}

    def test_confidence_valid_values(self, chart, dashas):
        from src.calculations.lpi import compute_lpi

        r = compute_lpi(chart, dashas, ON_DATE)
        for hl in r.houses.values():
            assert hl.confidence in {"High", "Med", "Low"}

    def test_rag_valid_values(self, chart, dashas):
        from src.calculations.lpi import compute_lpi

        r = compute_lpi(chart, dashas, ON_DATE)
        for hl in r.houses.values():
            assert hl.rag in {"Green", "Amber", "Red"}


# ── Session 37: Divisional charts ────────────────────────────────────────────
class TestDivisionalCharts:
    def test_divisional_map_has_all_vargas(self, chart):
        from src.calculations.divisional_charts import compute_divisional_signs

        dm = compute_divisional_signs(chart)
        expected_vargas = {
            "D1",
            "D2",
            "D3",
            "D4",
            "D7",
            "D9",
            "D10",
            "D12",
            "D16",
            "D20",
            "D24",
            "D27",
            "D30",
            "D40",
            "D45",
            "D60",
        }
        for p in ["Sun", "Moon", "Mars"]:
            assert set(dm.planets[p].keys()) == expected_vargas

    def test_vimshopaka_seven_planets(self, chart):
        from src.calculations.divisional_charts import compute_vimshopaka

        v = compute_vimshopaka(chart)
        assert len(v.scores) == 7

    def test_vimshopaka_max_20(self, chart):
        from src.calculations.divisional_charts import compute_vimshopaka

        v = compute_vimshopaka(chart)
        for s in v.scores.values():
            assert 0 <= s <= 20.01

    def test_d60_seven_planets(self, chart):
        from src.calculations.divisional_charts import compute_d60

        d60 = compute_d60(chart)
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            assert p in d60
            assert d60[p].quality in {"Benefic", "Malefic", "Mixed", "Neutral"}

    def test_india_d9_lagna_pisces(self, chart):
        from src.calculations.divisional_charts import compute_divisional_signs

        dm = compute_divisional_signs(chart)
        # D9 lagna sign for Taurus 7.73° should be Pisces (workbook-verified)
        d9_lagna_si = dm.lagna["D9"]
        assert d9_lagna_si == 11  # Pisces


# ── Session 38: Extended yogas + Rasi Drishti + Bhavat Bhavam ────────────────
class TestExtendedYogas:
    def test_raja_yogas_returns_list(self, chart, dashas):
        from src.calculations.extended_yogas import detect_raja_dhana_yogas

        r = detect_raja_dhana_yogas(chart, dashas, ON_DATE)
        assert len(r) == 13  # 8 Raja + 5 Dhana

    def test_viparita_yogas_four_entries(self, chart, dashas):
        from src.calculations.extended_yogas import detect_viparita_yogas

        r = detect_viparita_yogas(chart, dashas, ON_DATE)
        assert len(r) == 4  # Harsha + Sarala + Vimala + Dainya

    def test_neecha_bhanga_seven_planets(self, chart, dashas):
        from src.calculations.extended_yogas import detect_neecha_bhanga

        r = detect_neecha_bhanga(chart, dashas, ON_DATE)
        assert len(r) == 7

    def test_rasi_drishti_12_houses(self, chart):
        from src.calculations.extended_yogas import compute_rasi_drishti

        rd = compute_rasi_drishti(chart)
        assert len(rd.house_aspects) == 12

    def test_rasi_drishti_aries_aspects(self, chart):
        """Aries sign aspects Leo(4), Scorpio(7), Aquarius(10)."""
        from src.calculations.extended_yogas import _RASI_DRISHTI

        assert _RASI_DRISHTI[0] == {4, 7, 10}

    def test_bhavat_bhavam_h2_is_h3(self, chart):
        from src.calculations.extended_yogas import compute_bhavat_bhavam

        bb = compute_bhavat_bhavam(chart)
        assert bb[2] == 3

    def test_bhavat_bhavam_h4_is_h7(self, chart):
        from src.calculations.extended_yogas import compute_bhavat_bhavam

        bb = compute_bhavat_bhavam(chart)
        assert bb[4] == 7


# ── Session 39: Avastha v2 + Narrative ───────────────────────────────────────
class TestAvasthaV2:
    def test_baaladi_sun_cancer_27deg_is_bala(self, chart):
        """Sun at 27.99° Cancer (even sign) → Bala (workbook-verified)."""
        from src.calculations.avastha_v2 import compute_baaladi

        state, eff = compute_baaladi("Sun", chart)
        assert state == "Bala"
        assert eff == 0.25

    def test_baaladi_moon_cancer_4deg_is_mrita(self, chart):
        """Moon at 3.98° Cancer (even sign) → Mrita (workbook-verified)."""
        from src.calculations.avastha_v2 import compute_baaladi

        state, eff = compute_baaladi("Moon", chart)
        assert state == "Mrita"
        assert eff == 0.0

    def test_avasthas_v2_seven_planets(self, chart):
        from src.calculations.avastha_v2 import compute_avasthas_v2

        r = compute_avasthas_v2(chart)
        assert len(r.planets) == 7

    def test_combined_modifier_range(self, chart):
        from src.calculations.avastha_v2 import compute_avasthas_v2

        r = compute_avasthas_v2(chart)
        for av in r.planets.values():
            assert 0.0 <= av.combined_modifier <= 2.0


class TestNarrative:
    def test_narrative_12_houses(self, chart, dashas):
        from src.calculations.lpi import compute_lpi
        from src.calculations.narrative import generate_narrative

        lpi = compute_lpi(chart, dashas, ON_DATE)
        nr = generate_narrative(lpi, chart, dashas, ON_DATE)
        assert len(nr.houses) == 12

    def test_narrative_domain_summaries(self, chart, dashas):
        from src.calculations.lpi import compute_lpi
        from src.calculations.narrative import generate_narrative

        lpi = compute_lpi(chart, dashas, ON_DATE)
        nr = generate_narrative(lpi, chart, dashas, ON_DATE)
        assert set(nr.domain_summaries.keys()) == {"Dharma", "Artha", "Kama", "Moksha"}


# ── Session 40: Scoring v3 + Scenario ────────────────────────────────────────
class TestScoringV3:
    def test_score_chart_v3_returns_result(self, chart, dashas):
        from src.calculations.scoring_v3 import score_chart_v3, ENGINE_VERSION

        r = score_chart_v3(chart, dashas, ON_DATE)
        assert r.engine_version == ENGINE_VERSION
        assert r.lagna_sign == "Taurus"

    def test_v3_has_all_axes(self, chart, dashas):
        from src.calculations.scoring_v3 import score_chart_v3

        r = score_chart_v3(chart, dashas, ON_DATE)
        assert len(r.d1_scores) == 12
        assert len(r.cl_scores) == 12
        assert len(r.d9_scores) == 12

    def test_v3_has_lpi(self, chart, dashas):
        from src.calculations.scoring_v3 import score_chart_v3

        r = score_chart_v3(chart, dashas, ON_DATE)
        assert r.lpi is not None
        assert r.lpi.overall_index is not None

    def test_v3_deterministic(self, chart, dashas):
        from src.calculations.scoring_v3 import score_chart_v3

        r1 = score_chart_v3(chart, dashas, ON_DATE)
        r2 = score_chart_v3(chart, dashas, ON_DATE)
        assert r1.d1_scores == r2.d1_scores


class TestScenario:
    def test_apply_scenario_changes_planet(self, chart):
        from src.calculations.scenario import apply_scenario

        sc = apply_scenario(chart, {"Sun": {"longitude": 45.0}})
        assert abs(sc.planets["Sun"].longitude - 45.0) < 0.01
        assert sc.planets["Sun"].sign == "Taurus"

    def test_compare_scenarios_returns_list(self, chart, dashas):
        from src.calculations.scenario import compare_scenarios

        overrides = [("Sun to Taurus", {"Sun": {"longitude": 45.0}})]
        results = compare_scenarios(chart, overrides, dashas, ON_DATE)
        assert len(results) == 1
        assert len(results[0].d1_delta) == 12
