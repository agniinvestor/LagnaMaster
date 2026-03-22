"""tests/test_phase8.py — Sessions 57–63 Phase 8 tests."""

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
ON_DATE = date(2026, 3, 20)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA)


@pytest.fixture(scope="module")
def dashas(chart):
    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

    return compute_vimshottari_dasa(chart, date(1947, 8, 15))


# ── S57: Orb-sensitive strength ────────────────────────────────────────────
class TestOrbStrength:
    def test_zero_orb_full_strength(self):
        from src.calculations.orb_strength import conjunction_strength

        assert conjunction_strength(100.0, 100.0) == 1.0

    def test_pvrnr_6deg_threshold(self):
        from src.calculations.orb_strength import conjunction_strength

        s6 = conjunction_strength(100.0, 106.0)
        assert 0.45 <= s6 <= 0.65  # near 0.5 at 6°

    def test_8deg_weak(self):
        """PVRNR p149: 8° apart = weak yoga."""
        from src.calculations.orb_strength import conjunction_strength

        s8 = conjunction_strength(100.0, 108.0)
        assert s8 < 0.50

    def test_beyond_15deg_zero(self):
        from src.calculations.orb_strength import conjunction_strength

        assert conjunction_strength(100.0, 116.0) == 0.0

    def test_association_strength(self, chart):
        from src.calculations.orb_strength import association_strength

        r = association_strength("Sun", "Mercury", chart)
        assert r.in_same_sign  # Sun and Mercury both in Cancer 1947
        assert r.strength > 0.0
        assert r.quality in {"Tight", "Strong", "Moderate", "Weak", "Absent"}

    def test_parivartana_detection(self, chart):
        from src.calculations.orb_strength import association_strength

        r = association_strength("Sun", "Mercury", chart)
        assert isinstance(r.parivartana, bool)

    def test_yoga_conjunction_strength(self, chart):
        from src.calculations.orb_strength import yoga_conjunction_strength

        s = yoga_conjunction_strength(["Sun", "Mercury"], chart)
        assert 0.0 <= s <= 1.0

    def test_reduces_yoga(self, chart):
        from src.calculations.orb_strength import association_strength

        r = association_strength("Sun", "Mercury", chart)
        assert isinstance(r.reduces_yoga(), bool)
        assert isinstance(r.is_pvrnr_close(), bool)


# ── S58: Yoga fructification ───────────────────────────────────────────────
class TestYogaFructification:
    def test_amsa_level(self, chart):
        from src.calculations.yoga_fructification import compute_amsa_level

        count, name = compute_amsa_level("Sun", chart)
        assert 0 <= count <= 10
        assert isinstance(name, str)

    def test_fructification_result(self, chart):
        from src.calculations.yoga_fructification import yoga_fructification_score

        r = yoga_fructification_score(["Sun", "Mercury"], chart)
        assert r.verdict in {"Full", "Partial", "Weak", "Minimal"}
        assert 0.0 <= r.fructification_score <= 1.0

    def test_fructification_conditions(self, chart):
        from src.calculations.yoga_fructification import yoga_fructification_score

        r = yoga_fructification_score(["Sun", "Mercury"], chart)
        assert isinstance(r.affliction_free, bool)
        assert isinstance(r.close_conjunction, bool)
        assert isinstance(r.dignity_adequate, bool)

    def test_check_affliction(self, chart):
        from src.calculations.yoga_fructification import check_yoga_affliction

        issues = check_yoga_affliction("Moon", chart)
        assert isinstance(issues, list)

    def test_india_budhaditya_strong(self, chart):
        """Sun+Mercury in Cancer: should have reasonably good fructification."""
        from src.calculations.yoga_fructification import yoga_fructification_score

        r = yoga_fructification_score(["Sun", "Mercury"], chart)
        assert r.fructification_score > 0.0


# ── S59: Stronger-of-two ───────────────────────────────────────────────────
class TestStrongerOfTwo:
    def test_stronger_planet_returns_valid(self, chart):
        from src.calculations.stronger_of_two import stronger_planet

        winner = stronger_planet("Mars", "Ketu", chart)
        assert winner in {"Mars", "Ketu"}

    def test_planet_strength_score(self, chart):
        from src.calculations.stronger_of_two import planet_strength_score

        s = planet_strength_score("Jupiter", chart)
        assert isinstance(s.cotenant_count, int)
        assert s.dignity_score in {0, 1, 2}
        assert 0.0 <= s.degree_in_sign <= 30.0

    def test_stronger_sign(self, chart):
        from src.calculations.stronger_of_two import stronger_sign

        lagna_si = chart.lagna_sign_index
        seventh_si = (lagna_si + 6) % 12
        winner = stronger_sign(lagna_si, seventh_si, chart)
        assert winner in {lagna_si, seventh_si}

    def test_strength_tuple_ordering(self, chart):
        from src.calculations.stronger_of_two import planet_strength_score

        s1 = planet_strength_score("Sun", chart)
        s2 = planet_strength_score("Saturn", chart)
        # Just verify comparison works
        assert (s1.as_tuple() >= s2.as_tuple()) or (s2.as_tuple() > s1.as_tuple())

    def test_cotenant_count_correct(self, chart):
        """India 1947: Sun/Moon/Mars/Mercury/Venus all in Cancer — many cotenants."""
        from src.calculations.stronger_of_two import planet_strength_score

        s = planet_strength_score("Sun", chart)
        assert s.cotenant_count >= 3  # Moon, Mercury, Venus also in Cancer


# ── S60: AV transit ────────────────────────────────────────────────────────
class TestAVTransit:
    def test_planet_transit_quality(self, chart):
        from src.calculations.av_transit import planet_transit_quality

        q = planet_transit_quality("Jupiter", 3, chart)  # Jupiter transiting Cancer
        assert q.quality in {"Excellent", "Good", "Average", "Unfavorable", "Malefic"}
        assert 0 <= q.rekhas <= 8

    def test_transit_report(self, chart):
        from src.calculations.av_transit import compute_transit_av_score

        r = compute_transit_av_score(chart, ON_DATE)
        assert isinstance(r.strong_natal_houses, list)
        assert isinstance(r.weak_natal_houses, list)
        assert isinstance(r.active_favorable, list)

    def test_house_sav_12_entries(self, chart):
        from src.calculations.av_transit import compute_transit_av_score

        r = compute_transit_av_score(chart, ON_DATE)
        assert len(r.house_sav) == 12

    def test_sav_thresholds(self, chart):
        from src.calculations.av_transit import compute_transit_av_score

        r = compute_transit_av_score(chart, ON_DATE)
        for h, rekhas in r.house_sav.items():
            assert isinstance(rekhas, int)


# ── S61: Arudha perception model ───────────────────────────────────────────
class TestArudhaPerception:
    def test_returns_analysis(self, chart):
        from src.calculations.arudha_perception import compute_al_perception

        r = compute_al_perception(chart, 10)  # H10 career
        assert r.conflict_type in {
            "Aligned",
            "Hidden Success",
            "Apparent Success",
            "Recognized Struggle",
        }

    def test_malefics_36_al(self, chart):
        from src.calculations.arudha_perception import compute_al_perception

        r = compute_al_perception(chart, 1)
        assert isinstance(r.malefics_3_6_from_al, list)
        assert isinstance(r.benefics_3_6_from_al, list)

    def test_full_model_12_houses(self, chart):
        from src.calculations.arudha_perception import compute_full_perception_model

        m = compute_full_perception_model(chart)
        assert len(m) == 12

    def test_material_strength_range(self, chart):
        from src.calculations.arudha_perception import compute_al_perception

        r = compute_al_perception(chart, 2)  # Wealth house
        assert isinstance(r.material_strength, float)

    def test_commentary_is_string(self, chart):
        from src.calculations.arudha_perception import compute_al_perception

        r = compute_al_perception(chart, 7)
        assert len(r.commentary) > 10


# ── S62: PVRNR yogas ───────────────────────────────────────────────────────
class TestPVRNRYogas:
    def test_returns_list(self, chart, dashas):
        from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

        r = detect_pvrnr_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 8

    def test_india_amala_yoga(self, chart, dashas):
        """India 1947: H10 from lagna — check if only benefics."""
        from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

        r = detect_pvrnr_yogas(chart, dashas, ON_DATE)
        amala = next((y for y in r if y.name == "Amala Yoga"), None)
        assert amala is not None

    def test_all_have_source(self, chart, dashas):
        from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

        r = detect_pvrnr_yogas(chart, dashas, ON_DATE)
        for y in r:
            assert "PVRNR" in y.source

    def test_weighted_scores_leq_base(self, chart, dashas):
        from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

        r = detect_pvrnr_yogas(chart, dashas, ON_DATE)
        for y in r:
            assert y.weighted_score <= y.score + 0.01

    def test_guru_mangala_detected(self, chart, dashas):
        from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

        r = detect_pvrnr_yogas(chart, dashas, ON_DATE)
        gm = next((y for y in r if "Guru-Mangala" in y.name), None)
        assert gm is not None


# ── S63: Planet effectiveness ──────────────────────────────────────────────
class TestPlanetEffectiveness:
    def test_returns_7_planets(self, chart):
        from src.calculations.planet_effectiveness import compute_all_effectiveness

        r = compute_all_effectiveness(chart)
        assert len(r) == 7

    def test_overall_in_range(self, chart):
        from src.calculations.planet_effectiveness import compute_all_effectiveness

        r = compute_all_effectiveness(chart)
        for v in r.values():
            assert 0.0 <= v.overall <= 1.0

    def test_label_valid(self, chart):
        from src.calculations.planet_effectiveness import compute_all_effectiveness

        r = compute_all_effectiveness(chart)
        valid = {"Highly effective", "Effective", "Moderate", "Weak", "Ineffective"}
        for v in r.values():
            assert v.label in valid

    def test_factors_in_range(self, chart):
        from src.calculations.planet_effectiveness import compute_all_effectiveness

        r = compute_all_effectiveness(chart)
        for v in r.values():
            assert 0.0 <= v.shadbala_factor <= 1.0
            assert 0.0 <= v.av_factor <= 1.0
            assert 0.0 <= v.dig_bala_factor <= 1.0
            assert v.combust_penalty in {0.5, 1.0}
            assert v.yuddha_penalty in {0.5, 1.0}

    def test_deterministic(self, chart):
        from src.calculations.planet_effectiveness import compute_planet_effectiveness

        r1 = compute_planet_effectiveness("Jupiter", chart)
        r2 = compute_planet_effectiveness("Jupiter", chart)
        assert r1.overall == r2.overall
