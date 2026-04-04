"""Tests for governance: derived house resolver, archetypes, interpretation."""
from src.calculations.derived_house import resolve_house


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
