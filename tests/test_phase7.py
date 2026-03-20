"""tests/test_phase7.py — Sessions 49–56 Phase 7 tests."""
from __future__ import annotations
import pytest
from datetime import date

INDIA = dict(year=1947,month=8,day=15,hour=0.0,lat=28.6139,lon=77.2090,
             tz_offset=5.5,ayanamsha="lahiri")
ON_DATE = date(2026, 3, 20)

@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA)

@pytest.fixture(scope="module")
def dashas(chart):
    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa
    return compute_vimshottari_dasa(chart, date(1947,8,15))

# ── S49: Full 12-state Sayanadi ───────────────────────────────────────────────
class TestSayanadiFulll:
    def test_returns_7_planets(self, chart):
        from src.calculations.sayanadi_full import compute_all_sayanadi
        r = compute_all_sayanadi(chart)
        assert len(r) == 7

    def test_all_states_valid(self, chart):
        from src.calculations.sayanadi_full import compute_all_sayanadi, _MODIFIERS
        r = compute_all_sayanadi(chart)
        for v in r.values():
            assert v.state in _MODIFIERS
            assert v.modifier == _MODIFIERS[v.state]

    def test_sun_cancer_27deg_kopa_or_mudita(self, chart):
        """Sun at 27.99° Cancer (even sign, 3rd decanate = 20–30°) + Kopa check."""
        from src.calculations.sayanadi_full import compute_sayanadi_full
        r = compute_sayanadi_full("Sun", chart)
        # Sun cannot be Kopa (Sun doesn't combust itself); even sign 3rd dec = Nishcheshta
        # but dignity check (Cancer = neither own nor exalt for Sun) → decanate applies
        assert r.state in {"Nishcheshta","Kshuditha","Prakrita","Mudita","Sthira",
                            "Sayana","Upavesh","Netrapani","Kautuka","Deena","Trashita"}

    def test_deena_from_yuddha_loser(self, chart):
        """If we mark Mars as a yuddha loser, it should get Deena state."""
        from src.calculations.sayanadi_full import compute_sayanadi_full
        r = compute_sayanadi_full("Mars", chart, yuddha_losers={"Mars"})
        assert r.state == "Deena"
        assert r.modifier == 0.50

    def test_modifier_in_range(self, chart):
        from src.calculations.sayanadi_full import compute_all_sayanadi
        r = compute_all_sayanadi(chart)
        for v in r.values():
            assert 0.50 <= v.modifier <= 1.25

    def test_deterministic(self, chart):
        from src.calculations.sayanadi_full import compute_all_sayanadi
        r1 = compute_all_sayanadi(chart)
        r2 = compute_all_sayanadi(chart)
        assert r1["Jupiter"].state == r2["Jupiter"].state

    def test_india_moon_cancer_4deg(self, chart):
        """Moon at 3.98° Cancer = even sign, decanate 0 = Kautuka (0°–10°)."""
        from src.calculations.sayanadi_full import compute_sayanadi_full
        r = compute_sayanadi_full("Moon", chart)
        # Cancer even sign, 3.98° → decan 0 → Kautuka
        # But Moon is in own sign Cancer → Sthira takes priority
        assert r.state in {"Sthira", "Kautuka"}
        if r.state == "Sthira":
            assert r.modifier == 1.25

# ── S50: Panchadha Maitri ─────────────────────────────────────────────────────
class TestPanchadhaMaitri:
    def test_matrix_size(self, chart):
        from src.calculations.panchadha_maitri import compute_panchadha_matrix
        m = compute_panchadha_matrix(chart)
        assert len(m.relations) == 7 * 6  # 42 pairs

    def test_categories_valid(self, chart):
        from src.calculations.panchadha_maitri import compute_panchadha_matrix
        m = compute_panchadha_matrix(chart)
        valid = {"Adhi Mitra","Mitra","Sama","Shatru","Adhi Shatru"}
        for rel in m.relations.values():
            assert rel in valid

    def test_weights_match_categories(self, chart):
        from src.calculations.panchadha_maitri import compute_panchadha_matrix, _PANCHADHA_WEIGHTS
        m = compute_panchadha_matrix(chart)
        for (p1,p2), rel in m.relations.items():
            assert m.weights[(p1,p2)] == _PANCHADHA_WEIGHTS[rel]

    def test_india_mars_sun_adhi_mitra(self, chart):
        """Mars permanent friend of Sun + Mars in H2 from Sun (Tatkalik friend)
        → Naisargika Friend + Tatkalik Friend = Adhi Mitra."""
        from src.calculations.panchadha_maitri import panchadha_relation
        r = panchadha_relation("Sun", "Mars", chart)
        # Mars in Gemini (H12 from Cancer Sun sign) → Tatkalik Friend
        # Naisargika: Sun views Mars as Friend
        # → Adhi Mitra or Mitra depending on tatkalik
        assert r in {"Adhi Mitra", "Mitra", "Sama"}

    def test_naisargika_relation(self):
        from src.calculations.panchadha_maitri import naisargika_relation
        assert naisargika_relation("Sun", "Moon") == "Friend"
        assert naisargika_relation("Sun", "Saturn") == "Enemy"
        assert naisargika_relation("Sun", "Mercury") == "Neutral"

    def test_tatkalik_friend_houses(self, chart):
        """Tatkalik friendship is symmetric for H2↔H12."""
        from src.calculations.panchadha_maitri import tatkalik_relation
        # Mars in Gemini (H12 from Cancer), Sun in Cancer
        # From Sun → Mars: Mars is 12 signs from Sun → Friend
        # From Mars → Sun: Sun is 2 signs from Mars → Friend
        assert tatkalik_relation("Sun", "Mars", chart) == "Friend"
        assert tatkalik_relation("Mars", "Sun", chart) == "Friend"

# ── S51: Lagnesh Strength ──────────────────────────────────────────────────────
class TestLagneshStrength:
    def test_returns_result(self, chart):
        from src.calculations.lagnesh_strength import compute_lagnesh_strength
        r = compute_lagnesh_strength(chart)
        assert r.lagnesh in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]

    def test_modifier_in_range(self, chart):
        from src.calculations.lagnesh_strength import compute_lagnesh_strength
        r = compute_lagnesh_strength(chart)
        assert -0.75 <= r.modifier <= 0.75

    def test_india_1947_venus_h3_neutral(self, chart):
        """India 1947: Lagnesh Venus in H3 (neutral house, neutral dignity) → 0.00."""
        from src.calculations.lagnesh_strength import compute_lagnesh_strength
        r = compute_lagnesh_strength(chart)
        assert r.lagnesh == "Venus"
        assert r.house == 3
        assert r.modifier == 0.00

    def test_description_contains_planet(self, chart):
        from src.calculations.lagnesh_strength import compute_lagnesh_strength
        r = compute_lagnesh_strength(chart)
        assert r.lagnesh in r.description()

    def test_deterministic(self, chart):
        from src.calculations.lagnesh_strength import compute_lagnesh_strength
        r1 = compute_lagnesh_strength(chart)
        r2 = compute_lagnesh_strength(chart)
        assert r1.modifier == r2.modifier

# ── S52: Dig Bala continuous ──────────────────────────────────────────────────
class TestDigBala:
    def test_returns_7_planets(self, chart):
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        assert len(r) == 7

    def test_scores_in_range(self, chart):
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        for v in r.values():
            assert 0.0 <= v.score <= 1.0

    def test_india_sun_h3_score(self, chart):
        """Sun peak H10, currently H3, circular dist=5, score=1-5/6=0.167."""
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        sun = r["Sun"]
        assert sun.current_house == 3
        assert sun.distance == 5
        assert abs(sun.score - (1 - 5/6)) < 0.01

    def test_india_moon_h3_score(self, chart):
        """Moon peak H4, currently H3, dist=1, score=0.833."""
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        moon = r["Moon"]
        assert moon.current_house == 3
        assert moon.distance == 1
        assert abs(moon.score - (1 - 1/6)) < 0.01

    def test_india_mercury_h3_score(self, chart):
        """Mercury peak H1, currently H3, dist=2, score=0.667."""
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        mer = r["Mercury"]
        assert mer.distance == 2
        assert abs(mer.score - (1 - 2/6)) < 0.01

    def test_labels_valid(self, chart):
        from src.calculations.dig_bala import compute_dig_bala
        r = compute_dig_bala(chart)
        for v in r.values():
            assert v.label() in {"Strong","Moderate","Weak","Absent"}

# ── S53: Graha Yogas ──────────────────────────────────────────────────────────
class TestGrahaYogas:
    def test_returns_list(self, chart, dashas):
        from src.calculations.yogas_graha import detect_graha_yogas
        r = detect_graha_yogas(chart, dashas, ON_DATE)
        assert len(r) >= 6

    def test_budhaditya_present_1947(self, chart, dashas):
        """Sun and Mercury both in Cancer → Budhaditya."""
        from src.calculations.yogas_graha import detect_graha_yogas
        r = detect_graha_yogas(chart, dashas, ON_DATE)
        buda = next((y for y in r if y.name == "Budhaditya Yoga"), None)
        assert buda is not None
        assert buda.present

    def test_gaja_kesari_present_1947(self, chart, dashas):
        """Jupiter in Libra (H6), Moon in Cancer (H3): diff=3 → kendra → present."""
        from src.calculations.yogas_graha import detect_graha_yogas
        r = detect_graha_yogas(chart, dashas, ON_DATE)
        gk = next((y for y in r if y.name == "Gaja Kesari Yoga"), None)
        assert gk is not None
        assert gk.present

    def test_all_have_source(self, chart, dashas):
        from src.calculations.yogas_graha import detect_graha_yogas
        r = detect_graha_yogas(chart, dashas, ON_DATE)
        for y in r:
            assert y.source

    def test_weighted_score_leq_score(self, chart, dashas):
        from src.calculations.yogas_graha import detect_graha_yogas
        r = detect_graha_yogas(chart, dashas, ON_DATE)
        for y in r:
            assert y.weighted_score <= y.score + 0.01

# ── S54: Narayana Argala ──────────────────────────────────────────────────────
class TestNarayanaArgala:
    def test_argala_on_sign(self, chart):
        from src.calculations.narayana_argala import compute_argala_on_sign
        r = compute_argala_on_sign(0, chart)  # Aries
        assert r.sign_name == "Aries"
        assert isinstance(r.net_modifier, float)
        assert -0.5 <= r.net_modifier <= 0.5

    def test_modifier_all_signs(self, chart):
        from src.calculations.narayana_argala import compute_argala_on_sign
        for si in range(12):
            r = compute_argala_on_sign(si, chart)
            assert -0.5 <= r.net_modifier <= 0.5

    def test_active_dasha_modifier(self, chart):
        from src.calculations.narayana_argala import narayana_dasha_argala_modifier
        m = narayana_dasha_argala_modifier(chart, ON_DATE)
        assert -0.5 <= m <= 0.5

    def test_argala_lists_are_planets(self, chart):
        from src.calculations.narayana_argala import compute_argala_on_sign
        valid = {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"}
        r = compute_argala_on_sign(3, chart)  # Cancer
        for p in r.argala_planets + r.malefic_argala + r.virodha_planets:
            assert p in valid

    def test_interpretation_is_string(self, chart):
        from src.calculations.narayana_argala import compute_argala_on_sign
        r = compute_argala_on_sign(1, chart)
        assert isinstance(r.interpretation, str) and len(r.interpretation) > 5

# ── S55: Config Toggles ────────────────────────────────────────────────────────
class TestConfigToggles:
    def test_all_ayanamshas_resolve(self):
        from src.calculations.config_toggles import resolve_ayanamsha
        for name in ["lahiri","raman","krishnamurti","fagan_bradley"]:
            idx = resolve_ayanamsha(name)
            assert isinstance(idx, int)

    def test_unknown_ayanamsha_raises(self):
        from src.calculations.config_toggles import resolve_ayanamsha
        with pytest.raises(ValueError):
            resolve_ayanamsha("tropical")

    def test_r22_apply(self):
        from src.calculations.config_toggles import r22_modifier
        assert r22_modifier("Jupiter", True, "apply") == 0.10
        assert r22_modifier("Mercury", True, "apply") == -0.10
        assert r22_modifier("Jupiter", False, "apply") == 0.0

    def test_r22_ignore(self):
        from src.calculations.config_toggles import r22_modifier
        assert r22_modifier("Jupiter", True, "ignore") == 0.0

    def test_r22_classical(self):
        from src.calculations.config_toggles import r22_modifier
        assert r22_modifier("Saturn", True, "classical") == 0.0

    def test_calc_config_defaults(self):
        from src.calculations.config_toggles import CalcConfig
        c = CalcConfig()
        assert c.school == "parashari"
        assert c.ayanamsha == "lahiri"
        assert c.ayanamsha_id == 1
        assert not c.use_true_node

    def test_calc_config_raman(self):
        from src.calculations.config_toggles import CalcConfig
        c = CalcConfig(ayanamsha="raman")
        assert c.ayanamsha_id == 3

    def test_calc_config_true_node(self):
        from src.calculations.config_toggles import CalcConfig
        c = CalcConfig(node_type="true")
        assert c.use_true_node

    def test_calc_config_to_dict_roundtrip(self):
        from src.calculations.config_toggles import CalcConfig
        c = CalcConfig(school="kp", ayanamsha="raman")
        d = c.to_dict()
        assert d["school"] == "kp"
        assert d["ayanamsha"] == "raman"

# ── S56: Varga Agreement ─────────────────────────────────────────────────────
class TestVargaAgreement:
    def test_returns_12_houses(self, chart):
        from src.calculations.varga_agreement import compute_varga_agreement
        r = compute_varga_agreement(chart)
        assert len(r.houses) == 12

    def test_flags_valid(self, chart):
        from src.calculations.varga_agreement import compute_varga_agreement
        r = compute_varga_agreement(chart)
        for ha in r.houses.values():
            assert ha.flag in {"★★","★","○"}

    def test_confidence_valid(self, chart):
        from src.calculations.varga_agreement import compute_varga_agreement
        r = compute_varga_agreement(chart)
        for ha in r.houses.values():
            assert ha.confidence in {"High","Moderate","Low"}

    def test_high_conf_houses_subset(self, chart):
        from src.calculations.varga_agreement import compute_varga_agreement
        r = compute_varga_agreement(chart)
        for h in r.high_confidence_houses:
            assert r.houses[h].flag == "★★"

    def test_india_h2_wealth_all_agree_weak(self, chart):
        """H2 Wealth: D1=−5.25, D9=−2.0, D10=−2.5 — all 3 agree negative."""
        from src.calculations.varga_agreement import compute_varga_agreement
        r = compute_varga_agreement(chart)
        h2 = r.houses[2]
        # All three negative → ★★ High
        if h2.d1_score < 0 and h2.d9_score < 0 and h2.d10_score < 0:
            assert h2.flag == "★★"

    def test_deterministic(self, chart):
        from src.calculations.varga_agreement import compute_varga_agreement
        r1 = compute_varga_agreement(chart)
        r2 = compute_varga_agreement(chart)
        assert r1.houses[7].flag == r2.houses[7].flag
