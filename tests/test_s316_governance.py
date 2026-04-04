"""Tests for governance: derived house resolver, archetypes, interpretation."""
from src.calculations.derived_house import resolve_house
from src.corpus.planet_archetypes import PLANET_ARCHETYPES


def test_resolve_house_5th_from_3rd():
    assert resolve_house(3, 5) == 7


def test_resolve_house_wraps():
    assert resolve_house(10, 5) == 2


def test_resolve_house_12th_from_1st():
    assert resolve_house(1, 12) == 12


def test_resolve_house_1st_from_1st():
    assert resolve_house(1, 1) == 1


def test_resolve_house_7th_from_7th():
    assert resolve_house(7, 7) == 1


def test_all_nine_planets_in_archetypes():
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(PLANET_ARCHETYPES.keys()) == expected


def test_archetype_has_nature_and_themes():
    for planet, arch in PLANET_ARCHETYPES.items():
        assert "nature" in arch, f"{planet} missing nature"
        assert "themes" in arch, f"{planet} missing themes"
        assert arch["nature"] in ("benefic", "malefic"), f"{planet} has invalid nature"
        assert len(arch["themes"]) >= 3, f"{planet} needs at least 3 themes"
