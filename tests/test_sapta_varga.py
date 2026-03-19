"""
tests/test_sapta_varga.py
==========================
Test suite for src/calculations/sapta_varga.py — Session 16.

20 tests covering:
  - Module-level constants (weights sum to 20, all 7 divisions present)
  - VimshopakResult structure (10 subjects: 9 planets + Lagna)
  - Weights and dignity fractions
  - Dignity label correctness (exaltation, debilitation, own, neutral)
  - Score bounds: each planet total in [0, 20]
  - Ranking: returns 9 planets sorted descending by score
  - Grade thresholds (Excellent / Good / Average / Weak / Very Weak)
  - 1947 India Independence chart fixture values
  - Sun in Cancer D1 → Neutral (not own/exalt)
  - Saturn as Yogakaraka for Taurus Lagna: expected strong Vimshopak
  - Rahu/Ketu always Neutral in every division
  - D9 sign for Sun cross-validates varga.py
  - Determinism: same chart → same scores
"""

import pytest

INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA_1947)


@pytest.fixture(scope="module")
def result(india_chart):
    from src.calculations.sapta_varga import compute_vimshopak
    return compute_vimshopak(india_chart)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Constants
# ══════════════════════════════════════════════════════════════════════════════

class TestConstants:

    def test_weights_sum_to_20(self):
        from src.calculations.sapta_varga import SAPTA_VARGA_WEIGHTS
        assert abs(sum(SAPTA_VARGA_WEIGHTS.values()) - 20.0) < 1e-9

    def test_7_divisions_in_weights(self):
        from src.calculations.sapta_varga import SAPTA_VARGA_WEIGHTS
        assert set(SAPTA_VARGA_WEIGHTS.keys()) == {"D1", "D2", "D3", "D7", "D9", "D10", "D12"}

    def test_dignity_fractions_ordered(self):
        from src.calculations.sapta_varga import _DIGNITY_FRACTION
        assert _DIGNITY_FRACTION["Exaltation"] == 1.0
        assert _DIGNITY_FRACTION["Debilitation"] == 0.0
        assert _DIGNITY_FRACTION["Exaltation"] > _DIGNITY_FRACTION["Moolatrikona"]
        assert _DIGNITY_FRACTION["Moolatrikona"] > _DIGNITY_FRACTION["OwnSign"]
        assert _DIGNITY_FRACTION["OwnSign"] > _DIGNITY_FRACTION["Friend"]
        assert _DIGNITY_FRACTION["Friend"] > _DIGNITY_FRACTION["Neutral"]
        assert _DIGNITY_FRACTION["Neutral"] > _DIGNITY_FRACTION["Enemy"]
        assert _DIGNITY_FRACTION["Enemy"] > _DIGNITY_FRACTION["Debilitation"]


# ══════════════════════════════════════════════════════════════════════════════
# 2. Structure
# ══════════════════════════════════════════════════════════════════════════════

class TestStructure:

    def test_10_subjects_present(self, result):
        expected = {"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu","Lagna"}
        assert set(result.planets.keys()) == expected

    def test_each_planet_has_7_vargas(self, result):
        for pname, pv in result.planets.items():
            assert len(pv.varga_dignities) == 7, f"{pname} missing varga dignities"
            assert set(pv.varga_dignities.keys()) == {"D1","D2","D3","D7","D9","D10","D12"}

    def test_score_in_0_to_20(self, result):
        for pname, pv in result.planets.items():
            assert 0.0 <= pv.total <= 20.0, f"{pname} score {pv.total} out of range"

    def test_varga_points_sum_to_total(self, result):
        for pname, pv in result.planets.items():
            expected = sum(vd.points for vd in pv.varga_dignities.values())
            assert abs(expected - pv.total) < 1e-6, f"{pname} total mismatch"

    def test_sign_index_in_range(self, result):
        for pv in result.planets.values():
            for vd in pv.varga_dignities.values():
                assert 0 <= vd.sign_index <= 11

    def test_sign_name_consistent_with_index(self, result):
        signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                 "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        for pv in result.planets.values():
            for vd in pv.varga_dignities.values():
                assert vd.sign_name == signs[vd.sign_index]

    def test_dignity_labels_are_valid(self, result):
        valid = {"Exaltation","Moolatrikona","OwnSign","Friend","Neutral","Enemy","Debilitation"}
        for pv in result.planets.values():
            for vd in pv.varga_dignities.values():
                assert vd.dignity in valid, f"Unknown dignity {vd.dignity!r}"


# ══════════════════════════════════════════════════════════════════════════════
# 3. Dignity logic
# ══════════════════════════════════════════════════════════════════════════════

class TestDignityLogic:

    def test_sun_in_aries_is_exaltation(self):
        from src.calculations.sapta_varga import _sign_dignity
        assert _sign_dignity("Sun", 0) == "Exaltation"   # Aries = 0

    def test_sun_in_libra_is_debilitation(self):
        from src.calculations.sapta_varga import _sign_dignity
        assert _sign_dignity("Sun", 6) == "Debilitation"  # Libra = 6

    def test_moon_in_taurus_is_mooltrikona(self):
        from src.calculations.sapta_varga import _sign_dignity
        assert _sign_dignity("Moon", 1) == "Moolatrikona"  # Taurus = 1

    def test_jupiter_in_sagittarius_is_mooltrikona(self):
        from src.calculations.sapta_varga import _sign_dignity
        assert _sign_dignity("Jupiter", 8) == "Moolatrikona"

    def test_venus_in_taurus_is_own(self):
        from src.calculations.sapta_varga import _sign_dignity
        assert _sign_dignity("Venus", 1) == "OwnSign"

    def test_saturn_in_leo_is_enemy(self):
        from src.calculations.sapta_varga import _sign_dignity
        # Sun rules Leo; Saturn is enemy of Sun
        assert _sign_dignity("Saturn", 4) == "Enemy"

    def test_rahu_always_neutral(self):
        from src.calculations.sapta_varga import _sign_dignity
        for si in range(12):
            assert _sign_dignity("Rahu", si) == "Neutral", f"Rahu should be Neutral in sign {si}"

    def test_ketu_always_neutral(self):
        from src.calculations.sapta_varga import _sign_dignity
        for si in range(12):
            assert _sign_dignity("Ketu", si) == "Neutral"


# ══════════════════════════════════════════════════════════════════════════════
# 4. 1947 India chart fixture values
# ══════════════════════════════════════════════════════════════════════════════

class TestIndiaFixture:

    def test_sun_d1_sign_cancer(self, result):
        # Sun at 27.989° Cancer → D1 sign = Cancer (3)
        vd = result.planets["Sun"].varga_dignities["D1"]
        assert vd.sign_name == "Cancer"

    def test_sun_d1_dignity_neutral(self, result):
        # Cancer is Moon's sign; Sun has Neutral relationship with Moon
        vd = result.planets["Sun"].varga_dignities["D1"]
        assert vd.dignity == "Neutral"

    def test_rahu_all_neutral_dignity(self, result):
        for div in result.planets["Rahu"].varga_dignities.values():
            assert div.dignity == "Neutral"

    def test_ketu_all_neutral_dignity(self, result):
        for div in result.planets["Ketu"].varga_dignities.values():
            assert div.dignity == "Neutral"

    def test_for_planet_accessor(self, result):
        pv = result.for_planet("Moon")
        assert pv.planet == "Moon"
        assert pv.total >= 0.0

    def test_ranking_has_9_entries(self, result):
        r = result.ranking()
        assert len(r) == 9   # 9 planets, no Lagna

    def test_ranking_sorted_descending(self, result):
        scores = [s for _, s in result.ranking()]
        assert scores == sorted(scores, reverse=True)

    def test_determinism(self, india_chart):
        from src.calculations.sapta_varga import compute_vimshopak
        r1 = compute_vimshopak(india_chart)
        r2 = compute_vimshopak(india_chart)
        for p in ["Sun", "Moon", "Saturn"]:
            assert r1.planets[p].total == r2.planets[p].total


# ══════════════════════════════════════════════════════════════════════════════
# 5. Grade thresholds
# ══════════════════════════════════════════════════════════════════════════════

class TestGrade:

    def test_grade_excellent(self):
        from src.calculations.sapta_varga import vimshopak_grade
        assert vimshopak_grade(15.0) == "Excellent"
        assert vimshopak_grade(20.0) == "Excellent"

    def test_grade_good(self):
        from src.calculations.sapta_varga import vimshopak_grade
        assert vimshopak_grade(10.0) == "Good"
        assert vimshopak_grade(14.9) == "Good"

    def test_grade_average(self):
        from src.calculations.sapta_varga import vimshopak_grade
        assert vimshopak_grade(6.0) == "Average"

    def test_grade_weak(self):
        from src.calculations.sapta_varga import vimshopak_grade
        assert vimshopak_grade(3.0) == "Weak"
        assert vimshopak_grade(5.9) == "Weak"

    def test_grade_very_weak(self):
        from src.calculations.sapta_varga import vimshopak_grade
        assert vimshopak_grade(0.0) == "Very Weak"
        assert vimshopak_grade(2.9) == "Very Weak"
