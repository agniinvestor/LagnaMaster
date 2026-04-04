"""Tests for governance: derived house resolver, archetypes, interpretation."""
from src.calculations.derived_house import resolve_house
from src.calculations.interpretation import interpret
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


def test_interpret_basic():
    pred = {"claim": "will be wealthy", "domain": "wealth", "direction": "favorable"}
    ctx = {"qualifications": [], "trigger_planet": ""}
    result = interpret(pred, ctx)
    assert "will be wealthy" in result


def test_interpret_with_qualifications():
    pred = {"claim": "will be wealthy", "domain": "wealth"}
    ctx = {"qualifications": ["more_daughters"], "trigger_planet": ""}
    result = interpret(pred, ctx)
    assert "qualified by" in result
    assert "more_daughters" in result


def test_interpret_with_planet_themes():
    pred = {"claim": "will be wealthy", "domain": "wealth"}
    ctx = {"qualifications": [], "trigger_planet": "Jupiter"}
    result = interpret(pred, ctx)
    assert "Jupiter" in result
    assert "wisdom" in result
