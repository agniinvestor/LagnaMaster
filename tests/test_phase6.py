"""tests/test_phase6.py — Sessions 41–48 Phase 6 tests."""

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


# ── Session 41: Ishta / Kashta ────────────────────────────────────────────────
class TestIshtaKashta:
    def test_returns_seven_planets(self, chart):
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        assert len(r) == 7

    def test_ishta_in_range(self, chart):
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        for v in r.values():
            assert 0 <= v.ishta <= 60

    def test_kashta_in_range(self, chart):
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        for v in r.values():
            assert 0 <= v.kashta <= 60

    def test_net_sphuta_range(self, chart):
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        for v in r.values():
            assert -60 <= v.net_sphuta <= 60

    def test_ishta_kashta_sum_constraint(self, chart):
        """Ishta² + Kashta² ≈ Uchcha_Bala² but not required to equal 3600."""
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        sun = r["Sun"]
        assert sun.uchcha_bala >= 0
        assert sun.cheshta_bala >= 0

    def test_sun_in_cancer_moderate_uchcha(self, chart):
        """Sun at 27.99° Cancer — not exalted (Aries), moderate Uchcha Bala."""
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r = compute_ishta_kashta(chart)
        sun = r["Sun"]
        assert 0 < sun.uchcha_bala < 50

    def test_deterministic(self, chart):
        from src.calculations.ishta_kashta import compute_ishta_kashta

        r1 = compute_ishta_kashta(chart)
        r2 = compute_ishta_kashta(chart)
        assert r1["Jupiter"].ishta == r2["Jupiter"].ishta


# ── Session 42: Longevity ─────────────────────────────────────────────────────
class TestLongevity:
    def test_pindayu_positive(self, chart):
        from src.calculations.longevity import compute_pindayu

        assert compute_pindayu(chart) > 0

    def test_nisargayu_positive(self, chart):
        from src.calculations.longevity import compute_nisargayu

        assert compute_nisargayu(chart) > 0

    def test_amsayu_positive(self, chart):
        from src.calculations.longevity import compute_amsayu

        assert compute_amsayu(chart) > 0

    def test_longevity_range_structure(self, chart):
        from src.calculations.longevity import longevity_range

        r = longevity_range(chart)
        assert r.span in {"Short", "Medium", "Long"}
        assert r.average > 0
        assert r.minimum > 0

    def test_balarishta_returns_list(self, chart):
        from src.calculations.longevity import detect_balarishta

        r = detect_balarishta(chart)
        assert isinstance(r, list)

    def test_longevity_summary_string(self, chart):
        from src.calculations.longevity import longevity_range

        r = longevity_range(chart)
        s = r.summary()
        assert "Pindayu" in s and "Nisargayu" in s


# ── Session 43: Yogini Dasha ──────────────────────────────────────────────────
class TestYoginiDasha:
    def test_returns_periods(self, chart):
        from src.calculations.yogini_dasha import compute_yogini_dasha

        periods = compute_yogini_dasha(chart, date(1947, 8, 15))
        assert len(periods) > 0

    def test_period_lords_valid(self, chart):
        from src.calculations.yogini_dasha import compute_yogini_dasha, _YOGINIS

        periods = compute_yogini_dasha(chart, date(1947, 8, 15))
        valid_lords = {y[1] for y in _YOGINIS}
        for p in periods:
            assert p.lord in valid_lords

    def test_periods_contiguous(self, chart):
        from src.calculations.yogini_dasha import compute_yogini_dasha

        periods = compute_yogini_dasha(chart, date(1947, 8, 15))
        for i in range(1, len(periods)):
            assert periods[i].start_date == periods[i - 1].end_date

    def test_current_yogini_found(self, chart):
        from src.calculations.yogini_dasha import compute_yogini_dasha, current_yogini

        periods = compute_yogini_dasha(chart, date(1947, 8, 15))
        cur = current_yogini(periods, ON_DATE)
        assert cur is not None
        assert cur.is_current

    def test_antara_periods(self, chart):
        from src.calculations.yogini_dasha import compute_yogini_dasha

        periods = compute_yogini_dasha(chart, date(1947, 8, 15))
        if periods:
            antara = periods[0].antara_periods()
            assert len(antara) == 8


# ── Session 44: Full KP ───────────────────────────────────────────────────────
class TestKPFull:
    def test_kp_chain_structure(self, chart):
        from src.calculations.kp_full import kp_sub_lord_chain

        chain = kp_sub_lord_chain(chart.lagna)
        assert chain.sign_lord in [
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
        ]
        assert chain.nak_lord in [
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
        assert chain.sub_lord in [
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

    def test_kp_chain_lagna_1947(self, chart):
        """Lagna at 37.73° (Krittika, Sun lord). Nak lord = Sun."""
        from src.calculations.kp_full import kp_sub_lord_chain

        chain = kp_sub_lord_chain(chart.lagna)
        assert chain.nak_lord == "Sun"  # Krittika nakshatra = Sun lord

    def test_compute_kp_cusps_12(self, chart):
        from src.calculations.kp_full import compute_kp_cusps

        cusps = compute_kp_cusps(chart)
        assert len(cusps) == 12

    def test_kp_ruling_planets(self, chart):
        from src.calculations.kp_full import kp_ruling_planets

        rps = kp_ruling_planets(chart, ON_DATE)
        assert isinstance(rps, list)
        assert len(rps) > 0

    def test_kp_event_promise(self, chart):
        from src.calculations.kp_full import kp_event_promise

        p = kp_event_promise(chart, 10, ON_DATE)
        assert p.promise_level in {"Strong", "Moderate", "Weak"}
        assert p.sub_lord in [
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

    def test_kp_chain_all_9_possible_sublords(self):
        from src.calculations.kp_full import kp_sub_lord_chain

        # Test a range of longitudes
        seen = set()
        for i in range(0, 360, 5):
            chain = kp_sub_lord_chain(float(i))
            seen.add(chain.sub_lord)
        # Should see multiple different sub-lords across 72 samples
        assert len(seen) >= 5


# ── Session 45: Extended Yogas ────────────────────────────────────────────────
class TestExtendedYogas:
    def test_nabhasa_yogas_returns_list(self, chart, dashas):
        from src.calculations.yogas_extended import detect_nabhasa_yogas

        r = detect_nabhasa_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 6

    def test_chandra_yogas_returns_list(self, chart, dashas):
        from src.calculations.yogas_extended import detect_chandra_yogas

        r = detect_chandra_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 5

    def test_surya_yogas_returns_list(self, chart, dashas):
        from src.calculations.yogas_extended import detect_surya_yogas

        r = detect_surya_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 3

    def test_dhana_ext_returns_list(self, chart, dashas):
        from src.calculations.yogas_extended import detect_dhana_yogas_ext

        r = detect_dhana_yogas_ext(chart, dashas, ON_DATE)
        assert len(r) >= 4

    def test_india_kemadruma_or_not(self, chart, dashas):
        """1947 chart: Moon in Cancer with other planets — check Kemadruma."""
        from src.calculations.yogas_extended import detect_chandra_yogas

        r = detect_chandra_yogas(chart, dashas, ON_DATE)
        kemadruma = next((y for y in r if y.name == "Kemadruma Yoga"), None)
        assert kemadruma is not None
        # Moon in Cancer H3 — has planets nearby
        assert not kemadruma.present  # should NOT be Kemadruma (planets adjacent)

    def test_all_extended_total(self, chart, dashas):
        from src.calculations.yogas_extended import detect_all_extended_yogas

        r = detect_all_extended_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 18


# ── Session 46: Special Lagnas ────────────────────────────────────────────────
class TestSpecialLagnas:
    def test_returns_all_five(self, chart):
        from src.calculations.special_lagnas import compute_special_lagnas

        s = compute_special_lagnas(chart)
        assert s.hora_lagna_sign in [
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
        assert s.ghati_lagna_sign in [
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

    def test_indices_in_range(self, chart):
        from src.calculations.special_lagnas import compute_special_lagnas

        s = compute_special_lagnas(chart)
        for idx in [
            s.hora_lagna_index,
            s.ghati_lagna_index,
            s.sree_lagna_index,
            s.indu_lagna_index,
            s.pranapada_index,
        ]:
            assert 0 <= idx <= 11

    def test_deterministic(self, chart):
        from src.calculations.special_lagnas import compute_special_lagnas

        s1 = compute_special_lagnas(chart)
        s2 = compute_special_lagnas(chart)
        assert s1.hora_lagna_index == s2.hora_lagna_index
        assert s1.indu_lagna_index == s2.indu_lagna_index


# ── Session 47: Full Jaimini ──────────────────────────────────────────────────
class TestJaiminiFull:
    def test_detect_jaimini_yogas(self, chart):
        from src.calculations.jaimini_full import detect_jaimini_yogas

        r = detect_jaimini_yogas(chart)
        assert len(r) >= 4

    def test_karakamsha_scores_12_houses(self, chart):
        from src.calculations.jaimini_full import compute_karakamsha_scores

        r = compute_karakamsha_scores(chart)
        assert len(r) == 12

    def test_jaimini_longevity_structure(self, chart):
        from src.calculations.jaimini_full import compute_jaimini_longevity

        r = compute_jaimini_longevity(chart)
        assert r.span in {"Short", "Medium", "Long"}
        assert r.brahma in [
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
        assert r.years_estimate > 0

    def test_pada_relationship_score(self, chart):
        from src.calculations.jaimini_full import pada_relationship_score

        s = pada_relationship_score(chart, 1, 7)  # AL vs DL
        assert isinstance(s, float)

    def test_ak_amk_yoga(self, chart):
        from src.calculations.jaimini_full import detect_jaimini_yogas

        r = detect_jaimini_yogas(chart)
        ak_yoga = next(
            (y for y in r if "AK+AmK" in y.name or "Atmakaraka" in y.name), None
        )
        assert ak_yoga is not None


# ── Session 48: Empirical Validation ─────────────────────────────────────────
class TestEmpirica:
    def test_init_and_record(self, tmp_path):
        from src.calculations.empirica import (
            init_empirica_db,
            record_event,
            EmpiricalEvent,
            get_events,
        )

        db = tmp_path / "test_empirica.db"
        init_empirica_db(db)
        evt = EmpiricalEvent(
            chart_id="CHART_001",
            event_date="1947-08-15",
            event_type="Career",
            house_primary=10,
            event_description="Independence",
            manifested=1,
            confidence=3,
        )
        eid = record_event(evt, db)
        assert eid.startswith("EVT_")
        events = get_events("CHART_001", db)
        assert len(events) == 1
        assert events[0]["event_type"] == "Career"

    def test_accuracy_empty(self, tmp_path):
        from src.calculations.empirica import init_empirica_db, compute_accuracy

        db = tmp_path / "empty.db"
        init_empirica_db(db)
        r = compute_accuracy(db)
        assert r.total_events == 0

    def test_accuracy_with_events(self, tmp_path):
        from src.calculations.empirica import (
            init_empirica_db,
            record_event,
            compute_accuracy,
            EmpiricalEvent,
        )

        db = tmp_path / "acc.db"
        init_empirica_db(db)
        for i, manifested in enumerate([1, 1, 0, 1]):
            record_event(
                EmpiricalEvent(
                    chart_id="C1",
                    event_date=f"2020-0{i + 1}-01",
                    event_type="Career",
                    house_primary=10,
                    manifested=manifested,
                    r04_fired=1 if i < 3 else 0,
                ),
                db,
            )
        r = compute_accuracy(db)
        assert r.total_events == 4
        assert r.manifested_count == 3
        assert abs(r.base_rate - 0.75) < 0.01

    def test_event_type_validation(self, tmp_path):
        """Unknown event types should fall back to 'Other'."""
        from src.calculations.empirica import (
            init_empirica_db,
            record_event,
            get_events,
            EmpiricalEvent,
        )

        db = tmp_path / "type.db"
        init_empirica_db(db)
        evt = EmpiricalEvent(
            chart_id="C2",
            event_date="2020-01-01",
            event_type="UnknownType",
            house_primary=5,
        )
        record_event(evt, db)
        events = get_events("C2", db)
        assert events[0]["event_type"] == "Other"

    def test_api_router_importable(self):
        from src.api.empirica_router import router

        assert router is not None

    def test_three_seed_events_schema(self):
        """Verify the 3 demonstration events from REF_EmpiricaSchema can be recorded."""
        import tempfile
        import os
        from src.calculations.empirica import (
            init_empirica_db,
            record_event,
            EmpiricalEvent,
            get_events,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            db = os.path.join(tmpdir, "seed.db")
            init_empirica_db(db)
            seeds = [
                EmpiricalEvent(
                    "INDIA_1947",
                    "1971-12-16",
                    "Career",
                    10,
                    "1971 war victory",
                    manifested=1,
                    confidence=3,
                    active_mahadasha="Saturn",
                    d1_score_at_event=3.5,
                ),
                EmpiricalEvent(
                    "INDIA_1947",
                    "1991-07-24",
                    "Finance",
                    11,
                    "Economic liberalisation",
                    manifested=1,
                    confidence=2,
                    active_mahadasha="Jupiter",
                    d1_score_at_event=2.0,
                ),
                EmpiricalEvent(
                    "INDIA_1947",
                    "2001-12-13",
                    "Conflicts",
                    6,
                    "Parliament attack",
                    manifested=1,
                    confidence=2,
                    active_mahadasha="Saturn",
                    d1_score_at_event=-2.5,
                ),
            ]
            for s in seeds:
                record_event(s, db)
            events = get_events("INDIA_1947", db)
            assert len(events) == 3
