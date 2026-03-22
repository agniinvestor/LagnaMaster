"""
tests/test_yogas.py
====================
Tests for yoga detection engine.
1947 India Independence chart is used as the primary fixture.
"""

import pytest
from tests.fixtures import INDIA_1947
from src.ephemeris import compute_chart
from src.calculations.yogas import detect_yogas, Yoga


@pytest.fixture(scope="module")
def india_chart():
    f = INDIA_1947
    return compute_chart(
        year=f["year"],
        month=f["month"],
        day=f["day"],
        hour=f["hour"],
        lat=f["lat"],
        lon=f["lon"],
        tz_offset=f["tz_offset"],
        ayanamsha=f["ayanamsha"],
    )


@pytest.fixture(scope="module")
def india_yogas(india_chart):
    return detect_yogas(india_chart)


class TestYogaStructure:
    def test_returns_list_of_yoga(self, india_yogas):
        assert isinstance(india_yogas, list)
        for y in india_yogas:
            assert isinstance(y, Yoga)

    def test_each_yoga_has_required_fields(self, india_yogas):
        for y in india_yogas:
            assert y.name, "Yoga missing name"
            assert y.category in {
                "Pancha Mahapurusha",
                "Raj",
                "Dhana",
                "Lunar",
                "Solar",
                "Special",
                "Negative",
            }, f"Unknown category: {y.category}"
            assert y.nature in {"benefic", "malefic", "mixed"}
            assert isinstance(y.planets, list) and len(y.planets) >= 1
            assert y.description

    def test_benefic_yogas_before_negative(self, india_yogas):
        """Benefic/mixed yogas must come before purely malefic ones in sort order."""
        seen_malefic = False
        for y in india_yogas:
            if y.nature == "malefic":
                seen_malefic = True
            if seen_malefic and y.nature == "benefic":
                pytest.fail(f"Benefic yoga {y.name!r} appears after malefic yogas")


class TestIndia1947Yogas:
    """
    1947 India chart — Taurus Lagna, pancha-graha yoga in Cancer.
    Expected yogas (verified against classical references):
    - Pancha-Graha Yoga: 5 planets in Cancer
    - Gajakesari: Jupiter (Libra/H6) in H4 from Moon (Cancer/H3) → kendra from Moon
    - Dhana Yogas: multiple wealth lord conjunctions in Cancer
    - Vasi/Vesi: planets around Sun
    """

    def test_pancha_graha_yoga_present(self, india_yogas):
        """5 planets in Cancer → Pancha-Graha Yoga must be detected."""
        yoga_names = [y.name for y in india_yogas]
        assert "Pancha-Graha Yoga" in yoga_names

    def test_pancha_graha_yoga_has_5_planets(self, india_yogas):
        pg = next(y for y in india_yogas if y.name == "Pancha-Graha Yoga")
        assert len(pg.planets) == 5

    def test_gajakesari_yoga_present(self, india_yogas):
        """Jupiter in Libra (H6 from Taurus lagna) = H4 from Moon (Cancer=H3) → Gajakesari."""
        yoga_names = [y.name for y in india_yogas]
        assert "Gajakesari Yoga" in yoga_names

    def test_gajakesari_involves_moon_jupiter(self, india_yogas):
        gk = next(y for y in india_yogas if y.name == "Gajakesari Yoga")
        assert "Moon" in gk.planets
        assert "Jupiter" in gk.planets

    def test_dhana_yogas_present(self, india_yogas):
        """Multiple wealth lords in Cancer → multiple Dhana Yogas."""
        dhana = [y for y in india_yogas if y.category == "Dhana"]
        assert len(dhana) >= 1, "Expected at least one Dhana Yoga"

    def test_no_duplicate_yoga_descriptions(self, india_yogas):
        """Same planet pair should not create duplicate yogas in the same category."""
        seen = set()
        for y in india_yogas:
            key = (y.name, tuple(sorted(y.planets)))
            assert key not in seen, f"Duplicate yoga: {y.name} with {y.planets}"
            seen.add(key)

    def test_all_planets_in_yogas_are_valid(self, india_chart, india_yogas):
        """Every planet referenced in a yoga must be in the chart."""
        chart_planets = set(india_chart.planets.keys())
        for y in india_yogas:
            for p in y.planets:
                assert p in chart_planets, (
                    f"Yoga {y.name!r} references unknown planet {p!r}"
                )


class TestYogaLogic:
    def test_pancha_mahapurusha_requires_kendra(self, india_chart):
        """
        A Pancha Mahapurusha yoga should only fire when the planet is in kendra.
        We know Jupiter is in Libra (H6 for Taurus lagna) — H6 is NOT kendra.
        Jupiter in H6 despite being in own sign (Sagittarius/Pisces) should NOT fire.
        """
        yogas = detect_yogas(india_chart)
        pm = [y for y in yogas if y.category == "Pancha Mahapurusha"]
        # If any PM yoga exists, check its planet is truly in kendra
        from src.calculations.house_lord import compute_house_map, is_kendra

        hmap = compute_house_map(india_chart)
        for y in pm:
            planet = y.planets[0]
            ph = hmap.planet_house[planet]
            assert is_kendra(ph), (
                f"PM yoga {y.name}: {planet} in H{ph} which is not kendra"
            )

    def test_kemadruma_yoga_logic(self, india_chart):
        """
        Kemadruma: Moon has no planet in adjacent sign.
        1947 chart: Moon in Cancer (sign 3). Adjacent = Gemini (2) and Leo (4).
        Mars is in Gemini (sign 2) → adjacent to Moon.
        Therefore Kemadruma should NOT be present.
        """
        yogas = detect_yogas(india_chart)
        yoga_names = [y.name for y in yogas]
        assert "Kemadruma Yoga" not in yoga_names, (
            "Kemadruma should not form — Mars is adjacent to Moon in 1947 chart"
        )

    def test_guru_chandala_not_in_1947(self, india_chart):
        """Jupiter (Libra) and Rahu (Taurus) are in different signs — no Guru-Chandala."""
        yogas = detect_yogas(india_chart)
        yoga_names = [y.name for y in yogas]
        assert "Guru-Chandala Yoga" not in yoga_names

    def test_detect_yogas_is_deterministic(self, india_chart):
        """Same chart always produces the same yoga list."""
        y1 = detect_yogas(india_chart)
        y2 = detect_yogas(india_chart)
        assert [(y.name, y.planets) for y in y1] == [(y.name, y.planets) for y in y2]
