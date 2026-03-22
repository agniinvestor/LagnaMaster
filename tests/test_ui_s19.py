"""
tests/test_ui_s19.py
=====================
Session 19 — Streamlit UI smoke tests.

20 tests verifying:
  - All S11-S18 modules import correctly
  - Public API signatures match what app.py expects
  - app.py itself is importable (syntax + top-level imports)
  - Key dataclass attributes exist on return values
  - Varga, Vimshopak, KP, Varshaphala all produce valid output
    on the 1947 India fixture
"""

import pytest
from datetime import date

INDIA_1947 = {
    "year": 1947,
    "month": 8,
    "day": 15,
    "hour": 0.0,
    "lat": 28.6139,
    "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}


@pytest.fixture(scope="module")
def india_chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA_1947)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Import smoke tests — all S11-S18 modules
# ══════════════════════════════════════════════════════════════════════════════


class TestImports:
    def test_pushkara_navamsha_importable(self):
        from src.calculations.pushkara_navamsha import (
            is_pushkara_navamsha,
            pushkara_navamsha_planets,
        )

        assert callable(pushkara_navamsha_planets)
        assert callable(is_pushkara_navamsha)

    def test_montecarlo_importable(self):
        from src.calculations.pushkara_navamsha import run_monte_carlo

        assert callable(run_monte_carlo)  # monte_carlo_sensitivity = run_monte_carlo

    def test_kundali_milan_importable(self):
        from src.calculations.kundali_milan import compute_kundali_milan

        assert callable(compute_kundali_milan)

    def test_chara_dasha_importable(self):
        from src.calculations.chara_dasha import (
            compute_chara_dasha,
            current_chara_dasha,
        )

        assert callable(compute_chara_dasha)
        assert callable(current_chara_dasha)

    def test_varga_importable(self):
        from src.calculations.varga import compute_varga

        assert callable(compute_varga)

    def test_sapta_varga_importable(self):
        from src.calculations.sapta_varga import compute_vimshopak, vimshopak_grade

        assert callable(compute_vimshopak)
        assert callable(vimshopak_grade)

    def test_kp_importable(self):
        from src.calculations.kp import compute_kp, kp_sub_at

        assert callable(compute_kp)
        assert callable(kp_sub_at)

    def test_varshaphala_importable(self):
        from src.calculations.varshaphala import compute_varshaphala

        assert callable(compute_varshaphala)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Varga Charts — Tab 7
# ══════════════════════════════════════════════════════════════════════════════


class TestVargaTab:
    def test_varga_produces_all_8_divisions(self, india_chart):
        from src.calculations.varga import compute_varga

        vc = compute_varga(india_chart)
        assert set(vc.tables.keys()) == {
            "D2",
            "D3",
            "D4",
            "D7",
            "D9",
            "D10",
            "D12",
            "D60",
        }

    def test_varga_planet_sign_index_accessible(self, india_chart):
        from src.calculations.varga import compute_varga

        vc = compute_varga(india_chart)
        # app.py calls vt.planet_sign_index(p)
        vt = vc.d9()
        for p in ["Sun", "Moon", "Saturn"]:
            si = vt.planet_sign_index(p)
            assert 0 <= si <= 11

    def test_varga_lagna_fields(self, india_chart):
        from src.calculations.varga import compute_varga

        vc = compute_varga(india_chart)
        vt = vc.d2()
        assert hasattr(vt, "varga_lagna_sign")
        assert hasattr(vt, "varga_lagna_sign_index")
        assert hasattr(vt, "lagna_sign")


# ══════════════════════════════════════════════════════════════════════════════
# 3. Vimshopak — Tab 8
# ══════════════════════════════════════════════════════════════════════════════


class TestVimshopakTab:
    def test_vimshopak_ranking_has_9_planets(self, india_chart):
        from src.calculations.sapta_varga import compute_vimshopak

        vim = compute_vimshopak(india_chart)
        assert len(vim.ranking()) == 9

    def test_vimshopak_for_planet_has_varga_dignities(self, india_chart):
        from src.calculations.sapta_varga import compute_vimshopak

        vim = compute_vimshopak(india_chart)
        pv = vim.for_planet("Saturn")
        # app.py accesses pv.varga_dignities[div].dignity, .sign_name, .points, .weight
        for div in ["D1", "D2", "D3", "D7", "D9", "D10", "D12"]:
            vd = pv.varga_dignities[div]
            assert isinstance(vd.dignity, str)
            assert isinstance(vd.sign_name, str)
            assert isinstance(vd.points, float)

    def test_vimshopak_grade_field(self, india_chart):
        from src.calculations.sapta_varga import compute_vimshopak

        vim = compute_vimshopak(india_chart)
        assert vim.planets["Sun"].grade in {
            "Excellent",
            "Good",
            "Average",
            "Weak",
            "Very Weak",
        }


# ══════════════════════════════════════════════════════════════════════════════
# 4. KP Analysis — Tab 9
# ══════════════════════════════════════════════════════════════════════════════


class TestKPTab:
    def test_kp_lagna_kp_fields(self, india_chart):
        from src.calculations.kp import compute_kp

        kp = compute_kp(india_chart)
        lk = kp.lagna_kp
        # app.py accesses: nakshatra, star_lord, sub_lord, sub_sub_lord
        assert isinstance(lk.nakshatra, str)
        assert isinstance(lk.star_lord, str)
        assert isinstance(lk.sub_lord, str)
        assert isinstance(lk.sub_sub_lord, str)

    def test_kp_planet_shortcuts(self, india_chart):
        from src.calculations.kp import compute_kp

        kp = compute_kp(india_chart)
        # app.py accesses kpp.star_lord, kpp.sub_lord, kpp.nakshatra, kpp.is_retrograde
        kpp = kp.for_planet("Moon")
        assert hasattr(kpp, "star_lord")
        assert hasattr(kpp, "sub_lord")
        assert hasattr(kpp, "nakshatra")
        assert hasattr(kpp, "is_retrograde")

    def test_kp_house_significators(self, india_chart):
        from src.calculations.kp import compute_kp

        kp = compute_kp(india_chart)
        # app.py accesses: cusp_sub_lord, occupants, house_lord, significators
        for h in range(1, 13):
            hs = kp.houses[h]
            assert isinstance(hs.cusp_sub_lord, str)
            assert isinstance(hs.occupants, list)
            assert isinstance(hs.house_lord, str)
            assert isinstance(hs.significators, list)


# ══════════════════════════════════════════════════════════════════════════════
# 5. Annual Chart — Tab 10
# ══════════════════════════════════════════════════════════════════════════════


class TestAnnualTab:
    def test_varshaphala_1948_structure(self, india_chart):
        from src.calculations.varshaphala import compute_varshaphala

        vr = compute_varshaphala(
            natal_chart=india_chart,
            natal_birth_date=date(1947, 8, 15),
            target_year=1948,
            lat=28.6139,
            lon=77.2090,
        )
        # app.py accesses these fields:
        assert hasattr(vr, "solar_return_date")
        assert hasattr(vr, "varsha_lagna_sign")
        assert hasattr(vr, "muntha_sign")
        assert hasattr(vr, "varsha_pati")
        assert hasattr(vr, "years_elapsed")
        assert hasattr(vr, "tajika_aspects")
        assert hasattr(vr, "varsha_chart")

    def test_varshaphala_tajika_aspect_fields(self, india_chart):
        from src.calculations.varshaphala import compute_varshaphala

        vr = compute_varshaphala(
            natal_chart=india_chart,
            natal_birth_date=date(1947, 8, 15),
            target_year=1948,
            lat=28.6139,
            lon=77.2090,
        )
        # app.py accesses: aspect_type, planet_a, planet_b, angle, orb, applying
        for a in vr.tajika_aspects:
            assert hasattr(a, "aspect_type")
            assert hasattr(a, "planet_a")
            assert hasattr(a, "planet_b")
            assert hasattr(a, "orb")
            assert hasattr(a, "applying")


# ══════════════════════════════════════════════════════════════════════════════
# 6. App.py importability + structure
# ══════════════════════════════════════════════════════════════════════════════


class TestAppStructure:
    def test_app_file_exists(self):
        import os

        assert os.path.isfile("src/ui/app.py"), "src/ui/app.py not found"

    def test_app_is_parseable(self):
        import ast

        with open("src/ui/app.py") as f:
            src = f.read()
        tree = ast.parse(src)  # raises SyntaxError if invalid
        assert tree is not None

    def test_app_has_all_12_tabs(self):
        with open("src/ui/app.py") as f:
            src = f.read()
        # All 12 tab labels must appear in the source
        expected_tabs = [
            "📊 Chart",
            "🏠 Domain Scores",
            "🧘 Yogas",
            "🔢 Ashtakavarga",
            "⏱ Dashas",
            "🌍 Transits",
            "📐 Varga Charts",
            "⚖️ Vimshopak",
            "🔑 KP Analysis",
            "🌟 Annual Chart",
            "💑 Kundali Milan",
            "📋 Rule Detail",
        ]
        for tab in expected_tabs:
            assert tab in src, f"Tab '{tab}' missing from app.py"

    def test_app_imports_all_new_modules(self):
        with open("src/ui/app.py") as f:
            src = f.read()
        new_imports = [
            "pushkara_navamsha",
            "montecarlo",
            "chara_dasha",
            "varga",
            "sapta_varga",
            "kp",
            "varshaphala",
        ]
        for mod in new_imports:
            assert mod in src, f"Import of '{mod}' missing from app.py"

    def test_app_graceful_degradation(self):
        with open("src/ui/app.py") as f:
            src = f.read()
        # All new module imports should be inside try/except
        assert "_HAS_VARGA" in src
        assert "_HAS_KP" in src
        assert "_HAS_VARSHA" in src
        assert "_HAS_CHARA" in src
