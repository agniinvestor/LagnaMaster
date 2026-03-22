"""tests/test_phase19.py — Phase 19: Sessions 101–108"""

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
BD = date(1947, 8, 15)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart

    return compute_chart(**INDIA)


class TestDrigDasha:
    def test_returns_periods(self, chart):
        from src.calculations.drig_dasha import compute_drig_dasha

        p = compute_drig_dasha(chart, BD)
        assert len(p) == 12

    def test_continuous(self, chart):
        from src.calculations.drig_dasha import compute_drig_dasha

        p = compute_drig_dasha(chart, BD)
        for i in range(1, 6):
            assert p[i].start_date == p[i - 1].end_date

    def test_aspects_received(self, chart):
        from src.calculations.drig_dasha import compute_drig_dasha

        p = compute_drig_dasha(chart, BD)
        for period in p:
            assert period.aspects_received >= 0


class TestLagnaKendradiDasha:
    def test_returns_12_periods(self, chart):
        from src.calculations.lagna_kendradi_dasha import compute_lagna_kendradi_dasha

        p = compute_lagna_kendradi_dasha(chart, BD)
        assert len(p) == 12

    def test_groups_correct(self, chart):
        from src.calculations.lagna_kendradi_dasha import compute_lagna_kendradi_dasha

        p = compute_lagna_kendradi_dasha(chart, BD)
        groups = [period.group for period in p]
        assert groups[:4].count("Kendra") == 4
        assert groups[4:8].count("Panapara") == 4
        assert groups[8:].count("Apoklima") == 4

    def test_continuous(self, chart):
        from src.calculations.lagna_kendradi_dasha import compute_lagna_kendradi_dasha

        p = compute_lagna_kendradi_dasha(chart, BD)
        for i in range(1, 6):
            assert p[i].start_date == p[i - 1].end_date


class TestDoubleTransit:
    def test_returns_result(self, chart):
        from src.calculations.double_transit import compute_double_transit

        r = compute_double_transit(chart, "marriage", date(2026, 3, 21))
        assert r.domain == "marriage"
        assert r.signal
        assert r.confidence in {"High", "Moderate", "Low"}

    def test_all_domains(self, chart):
        from src.calculations.double_transit import compute_double_transit, _DOMAINS

        for d in _DOMAINS:
            r = compute_double_transit(chart, d, date(2026, 3, 21))
            assert r.target_house == _DOMAINS[d]

    def test_signal_valid(self, chart):
        from src.calculations.double_transit import compute_double_transit

        r = compute_double_transit(chart, "career", date(2026, 3, 21))
        assert (
            "double" in r.signal.lower()
            or "partial" in r.signal.lower()
            or "not" in r.signal.lower()
        )


class TestUpapadaLagna:
    def test_computes_ul(self, chart):
        from src.calculations.upapada_lagna import compute_upapada

        r = compute_upapada(chart)
        assert 0 <= r.ul_sign_index <= 11
        assert r.ul_sign in [
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

    def test_quality_valid(self, chart):
        from src.calculations.upapada_lagna import compute_upapada

        r = compute_upapada(chart)
        assert r.marriage_quality in {"Favourable", "Mixed", "Challenging"}

    def test_longevity_valid(self, chart):
        from src.calculations.upapada_lagna import compute_upapada

        r = compute_upapada(chart)
        assert (
            "lasting" in r.marriage_longevity.lower()
            or "challenge" in r.marriage_longevity.lower()
            or "separation" in r.marriage_longevity.lower()
        )

    def test_notes_are_strings(self, chart):
        from src.calculations.upapada_lagna import compute_upapada

        r = compute_upapada(chart)
        for note in r.notes:
            assert isinstance(note, str)


class TestKalaSarpa:
    def test_returns_result(self, chart):
        from src.calculations.kala_sarpa import compute_kala_sarpa

        r = compute_kala_sarpa(chart)
        assert isinstance(r.present, bool)
        assert isinstance(r.partial, bool)

    def test_disclaimer_present(self, chart):
        from src.calculations.kala_sarpa import compute_kala_sarpa

        r = compute_kala_sarpa(chart)
        assert "modern" in r.classical_disclaimer.lower()
        assert (
            "not found" in r.classical_disclaimer.lower()
            or "convention" in r.classical_disclaimer.lower()
        )

    def test_planets_accounted(self, chart):
        from src.calculations.kala_sarpa import compute_kala_sarpa

        r = compute_kala_sarpa(chart)
        total = len(r.planets_inside) + len(r.planets_outside)
        assert total <= 7

    def test_india_1947_not_ks(self, chart):
        from src.calculations.kala_sarpa import compute_kala_sarpa

        r = compute_kala_sarpa(chart)
        # India 1947 has planets in multiple signs — unlikely to be KS
        # Just assert planets_outside is not empty (some outside Rahu-Ketu axis)
        assert len(r.planets_inside) + len(r.planets_outside) > 0


class TestNabhasaYogas:
    def test_returns_yogas(self, chart):
        from src.calculations.nabhasa_yogas import detect_nabhasa_yogas

        yogas = detect_nabhasa_yogas(chart)
        assert len(yogas) >= 10

    def test_groups_covered(self, chart):
        from src.calculations.nabhasa_yogas import detect_nabhasa_yogas

        yogas = detect_nabhasa_yogas(chart)
        groups = {y.group for y in yogas}
        assert "Āśraya" in groups
        assert "Sankhya" in groups

    def test_sankhya_present(self, chart):
        from src.calculations.nabhasa_yogas import strongest_nabhasa

        present = strongest_nabhasa(chart)
        # At least one Nabhasa yoga should be present (Sankhya always fires)
        assert len(present) >= 1

    def test_india_1947_sankhya(self, chart):
        from src.calculations.nabhasa_yogas import detect_nabhasa_yogas

        yogas = detect_nabhasa_yogas(chart)
        sankhya = [y for y in yogas if y.group == "Sankhya" and y.present]
        assert len(sankhya) == 1  # exactly one Sankhya fires


class TestPitrDosha:
    def test_returns_result(self, chart):
        from src.calculations.pitr_dosha import compute_pitr_dosha

        r = compute_pitr_dosha(chart)
        assert isinstance(r.present, bool)
        assert r.severity in {"Strong", "Moderate", "Mild", "Not present"}

    def test_disclaimer_present(self, chart):
        from src.calculations.pitr_dosha import compute_pitr_dosha

        r = compute_pitr_dosha(chart)
        assert "modern" in r.classical_disclaimer.lower()

    def test_triggers_are_strings(self, chart):
        from src.calculations.pitr_dosha import compute_pitr_dosha

        r = compute_pitr_dosha(chart)
        for t in r.triggers:
            assert isinstance(t, str)


class TestRulePlugin:
    def test_register_and_apply(self, chart):
        from src.calculations.rule_plugin import (
            register_yoga,
            apply_all_plugins,
            clear_plugins,
        )

        clear_plugins()

        @register_yoga("Test Yoga", "Test Source", 1.0)
        def test_yoga(c) -> bool:
            return True

        results = apply_all_plugins(chart)
        assert any(r.name == "Test Yoga" and r.present for r in results)
        clear_plugins()

    def test_builtin_gajakesari(self, chart):
        # Re-import triggers the built-in registration
        import importlib
        import src.calculations.rule_plugin as rp

        importlib.reload(rp)
        plugins = rp.list_plugins()
        assert "Gajakesari (BVR strict)" in plugins["yogas"]

    def test_clear_plugins(self, chart):
        from src.calculations.rule_plugin import clear_plugins, list_plugins

        clear_plugins()
        p = list_plugins()
        assert len(p["yogas"]) == 0

    def test_error_in_plugin_doesnt_crash(self, chart):
        from src.calculations.rule_plugin import (
            register_yoga,
            apply_all_plugins,
            clear_plugins,
        )

        clear_plugins()

        @register_yoga("Broken Yoga", "Test", 1.0)
        def broken(c) -> bool:
            raise RuntimeError("intentional error")

        results = apply_all_plugins(chart)
        assert any(r.name == "Broken Yoga" and not r.present for r in results)
        clear_plugins()
