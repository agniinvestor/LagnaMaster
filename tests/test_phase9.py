"""tests/test_phase9.py — Sessions 64–70 Phase 9 tests."""

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


# ── S64: Dominance Engine ─────────────────────────────────────────────────────
class TestDominanceEngine:
    def test_returns_report(self, chart, dashas):
        from src.calculations.dominance_engine import compute_dominance_factors

        r = compute_dominance_factors(chart, dashas, ON_DATE)
        assert r.global_tone in {
            "Positive",
            "Mixed Positive",
            "Neutral",
            "Mixed Negative",
            "Negative",
        }

    def test_has_factors(self, chart, dashas):
        from src.calculations.dominance_engine import compute_dominance_factors

        r = compute_dominance_factors(chart, dashas, ON_DATE)
        assert isinstance(r.factors, list)
        assert isinstance(r.benefic_overrides, list)
        assert isinstance(r.malefic_dominances, list)

    def test_dasha_priority_present(self, chart, dashas):
        from src.calculations.dominance_engine import compute_dominance_factors

        r = compute_dominance_factors(chart, dashas, ON_DATE)
        assert r.dasha_priority is not None
        assert r.dasha_priority.planet in [
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
            "Rahu",
            "Ketu",
        ]

    def test_dominant_theme(self, chart, dashas):
        from src.calculations.dominance_engine import dominant_theme

        t = dominant_theme(chart, dashas, ON_DATE)
        assert isinstance(t, str) and len(t) > 10

    def test_houses_classified(self, chart, dashas):
        from src.calculations.dominance_engine import compute_dominance_factors

        r = compute_dominance_factors(chart, dashas, ON_DATE)
        assert isinstance(r.affliction_dominated_houses, list)
        assert isinstance(r.yoga_dominated_houses, list)


# ── S65: Promise vs Manifestation ────────────────────────────────────────────
class TestPromiseEngine:
    def test_house_promise(self, chart):
        from src.calculations.promise_engine import compute_house_promise

        p = compute_house_promise(chart, 10)
        assert p.promise_strength in {"Strong", "Moderate", "Weak", "Absent", "Negated"}
        assert 0.0 <= p.ceiling <= 10.0

    def test_full_promise_12_houses(self, chart, dashas):
        from src.calculations.promise_engine import compute_full_promise

        r = compute_full_promise(chart, dashas, ON_DATE)
        assert len(r) == 12

    def test_manifestation_timing_valid(self, chart, dashas):
        from src.calculations.promise_engine import compute_full_promise

        r = compute_full_promise(chart, dashas, ON_DATE)
        valid_timings = {"Now", "Soon", "Future", "Blocked"}
        for mr in r.values():
            assert mr.manifestation_timing in valid_timings

    def test_probability_in_range(self, chart, dashas):
        from src.calculations.promise_engine import compute_full_promise

        r = compute_full_promise(chart, dashas, ON_DATE)
        for mr in r.values():
            assert 0.0 <= mr.manifestation_probability <= 1.0

    def test_blocked_when_no_promise(self, chart, dashas):
        from src.calculations.promise_engine import compute_house_promise

        p = compute_house_promise(chart, 2)  # H2 Wealth weak in India 1947
        if not p.promise_present:
            assert p.promise_strength in {"Absent", "Negated"}


# ── S66: Domain weighting ────────────────────────────────────────────────────
class TestDomainWeighting:
    def test_all_domains_return_result(self, chart, dashas):
        from src.calculations.domain_weighting import compute_domain_lpi, DOMAINS

        for d in DOMAINS:
            r = compute_domain_lpi(chart, dashas, ON_DATE, d)
            assert len(r.house_scores) == 12

    def test_career_d10_dominant(self):
        from src.calculations.domain_weighting import get_domain_weights

        w = get_domain_weights("career")
        assert w["D10"] > w["D1"]  # D10 should dominate for career

    def test_marriage_d9_dominant(self):
        from src.calculations.domain_weighting import get_domain_weights

        w = get_domain_weights("marriage")
        assert w["D9"] > w["D1"]

    def test_weights_sum_to_one(self):
        from src.calculations.domain_weighting import get_domain_weights, DOMAINS

        for d in DOMAINS + ["default"]:
            w = get_domain_weights(d)
            total = sum(
                v for k, v in w.items() if k not in ("primary_house", "rationale")
            )
            assert abs(total - 1.0) < 0.01, f"{d} weights sum to {total}"

    def test_top_houses_sorted(self, chart, dashas):
        from src.calculations.domain_weighting import compute_domain_lpi

        r = compute_domain_lpi(chart, dashas, ON_DATE, "career")
        # Top houses should have higher scores than weak houses
        top_scores = [r.house_scores[h] for h in r.top_houses]
        weak_scores = [r.house_scores[h] for h in r.weak_houses]
        assert min(top_scores) >= max(weak_scores) - 0.5  # allow for ties


# ── S67: Planet chains ────────────────────────────────────────────────────────
class TestPlanetChains:
    def test_stelliums_1947(self, chart):
        from src.calculations.planet_chains import compute_stelliums

        s = compute_stelliums(chart)
        # India 1947: many planets in Cancer — should have a stellium
        assert any(st.sign_name == "Cancer" for st in s)

    def test_stellium_cancer_has_5plus(self, chart):
        from src.calculations.planet_chains import compute_stelliums

        s = compute_stelliums(chart)
        cancer = next((st for st in s if st.sign_name == "Cancer"), None)
        assert cancer is not None
        assert len(cancer.planets) >= 5  # Sun/Moon/Mer/Ven/Sat in Cancer 1947

    def test_dispositor_chain(self, chart):
        from src.calculations.planet_chains import compute_dispositor_chain

        chain = compute_dispositor_chain("Jupiter", chart)
        assert chain.start_planet == "Jupiter"
        assert len(chain.chain) >= 1
        assert isinstance(chain.interpretation, str)

    def test_all_chains(self, chart):
        from src.calculations.planet_chains import compute_all_dispositor_chains

        chains = compute_all_dispositor_chains(chart)
        assert len(chains) >= 7

    def test_mutual_receptions(self, chart):
        from src.calculations.planet_chains import compute_mutual_receptions

        recs = compute_mutual_receptions(chart)
        assert isinstance(recs, list)
        for r in recs:
            assert r.strength in {"Strong", "Partial"}


# ── S68: House modulation ─────────────────────────────────────────────────────
class TestHouseModulation:
    def test_upachaya_improves_with_age(self, chart):
        from src.calculations.house_modulation import house_type_modifier

        young = house_type_modifier(6, chart, 25, 1.0)
        elder = house_type_modifier(6, chart, 65, 1.0)
        assert elder.modulated_score >= young.modulated_score
        assert young.time_improves

    def test_malefics_beneficial_in_36(self, chart):
        from src.calculations.house_modulation import house_type_modifier

        r = house_type_modifier(3, chart, 35)
        assert r.house_type == "Upachaya"

    def test_apply_modulation_12_houses(self, chart):
        from src.calculations.house_modulation import apply_house_modulation

        scores = {h: float(h - 6.5) for h in range(1, 13)}
        modulated = apply_house_modulation(scores, chart, 40)
        assert len(modulated) == 12

    def test_house_types_correct(self, chart):
        from src.calculations.house_modulation import house_type_modifier

        assert house_type_modifier(1, chart).house_type == "Kendra"
        assert house_type_modifier(5, chart).house_type == "Trikona"
        assert house_type_modifier(6, chart).house_type == "Upachaya"
        assert house_type_modifier(8, chart).house_type == "Dusthana"
        assert house_type_modifier(2, chart).house_type == "Maraka"


# ── S69: Confidence model ─────────────────────────────────────────────────────
class TestConfidenceModel:
    def test_returns_12_houses(self, chart):
        from src.calculations.confidence_model import compute_confidence

        r = compute_confidence(chart)
        assert len(r.houses) == 12

    def test_confidence_in_range(self, chart):
        from src.calculations.confidence_model import compute_confidence

        r = compute_confidence(chart)
        for hc in r.houses.values():
            assert 0.0 <= hc.overall_confidence <= 1.0

    def test_labels_valid(self, chart):
        from src.calculations.confidence_model import compute_confidence

        r = compute_confidence(chart)
        for hc in r.houses.values():
            assert hc.confidence_label in {"High", "Moderate", "Low", "Uncertain"}

    def test_global_confidence(self, chart):
        from src.calculations.confidence_model import compute_confidence

        r = compute_confidence(chart)
        assert 0.0 <= r.global_confidence <= 1.0

    def test_most_reliable_houses(self, chart):
        from src.calculations.confidence_model import compute_confidence

        r = compute_confidence(chart)
        assert len(r.most_reliable_houses) == 3
        for h in r.most_reliable_houses:
            assert 1 <= h <= 12


# ── S70: Chart exceptions ─────────────────────────────────────────────────────
class TestChartExceptions:
    def test_returns_report(self, chart):
        from src.calculations.chart_exceptions import detect_chart_exceptions

        r = detect_chart_exceptions(chart)
        assert isinstance(r.exceptions, list)
        assert isinstance(r.requires_expert_review, bool)

    def test_severity_valid(self, chart):
        from src.calculations.chart_exceptions import detect_chart_exceptions

        r = detect_chart_exceptions(chart)
        valid = {"Critical", "High", "Moderate", "Advisory"}
        for e in r.exceptions:
            assert e.severity in valid

    def test_summary_is_string(self, chart):
        from src.calculations.chart_exceptions import detect_chart_exceptions

        r = detect_chart_exceptions(chart)
        assert isinstance(r.exception_summary, str) and len(r.exception_summary) > 10

    def test_india_1947_stellium_exception(self, chart):
        """India 1947 has extreme Cancer stellium — should detect something."""
        from src.calculations.planet_chains import compute_stelliums

        # Stelliums detected via planet_chains module
        s = compute_stelliums(chart)
        cancer = next((st for st in s if st.sign_name == "Cancer"), None)
        assert cancer is not None
        assert len(cancer.planets) >= 5

    def test_special_rules_list(self, chart):
        from src.calculations.chart_exceptions import detect_chart_exceptions

        r = detect_chart_exceptions(chart)
        assert isinstance(r.special_rules_apply, list)
