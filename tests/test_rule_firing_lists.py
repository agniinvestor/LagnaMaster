"""tests/test_rule_firing_lists.py — BUG-103: list-valued conditions in rule_firing.

Verifies that planet_not_in_house and planet_not_aspecting correctly handle
list values (e.g., [4, 7, 10]) by checking ALL houses, not just the first.
"""
from __future__ import annotations

import pytest

INDIA = dict(
    year=1947, month=8, day=15, hour=0.0,
    lat=28.6139, lon=77.2090, tz_offset=5.5, ayanamsha="lahiri",
)


@pytest.fixture(scope="module")
def chart():
    from src.ephemeris import compute_chart
    return compute_chart(**INDIA)


class TestPlanetNotInHouseList:
    """planet_not_in_house with list should check ALL houses."""

    def test_planet_in_one_of_listed_houses_fails(self, chart):
        """If planet IS in one of the listed houses, condition should fail (return False)."""
        from src.calculations.rule_firing import _check_compound_conditions, _planet_house

        # Find a planet and its actual house
        planet = "Sun"
        actual_house = _planet_house(chart, planet)
        assert actual_house > 0, "Sun must be in a house"

        # Create condition where the list includes the actual house
        conditions = [{
            "type": "planet_not_in_house",
            "planet": planet,
            "house": [1, actual_house, 12],  # includes actual house
        }]
        fires, _ = _check_compound_conditions(conditions, chart)
        assert not fires, (
            f"{planet} is in house {actual_house}, "
            f"planet_not_in_house with list {[1, actual_house, 12]} should fail"
        )

    def test_planet_not_in_any_listed_house_passes(self, chart):
        """If planet is NOT in any of the listed houses, condition should pass."""
        from src.calculations.rule_firing import _check_compound_conditions, _planet_house

        planet = "Sun"
        actual_house = _planet_house(chart, planet)

        # Create a list of houses that does NOT include the actual house
        other_houses = [h for h in range(1, 13) if h != actual_house][:3]
        conditions = [{
            "type": "planet_not_in_house",
            "planet": planet,
            "house": other_houses,
        }]
        fires, _ = _check_compound_conditions(conditions, chart)
        assert fires, (
            f"{planet} in house {actual_house}, "
            f"planet_not_in_house with list {other_houses} should pass"
        )

    def test_single_value_still_works(self, chart):
        """Single int value (non-list) should still work correctly."""
        from src.calculations.rule_firing import _check_compound_conditions, _planet_house

        planet = "Mars"
        actual_house = _planet_house(chart, planet)

        # Planet IS in that house: should fail
        conditions_fail = [{
            "type": "planet_not_in_house",
            "planet": planet,
            "house": actual_house,
        }]
        fires_fail, _ = _check_compound_conditions(conditions_fail, chart)
        assert not fires_fail

        # Planet NOT in a different house: should pass
        other = (actual_house % 12) + 1
        conditions_pass = [{
            "type": "planet_not_in_house",
            "planet": planet,
            "house": other,
        }]
        fires_pass, _ = _check_compound_conditions(conditions_pass, chart)
        assert fires_pass


class TestPlanetNotAspectingList:
    """planet_not_aspecting with list should check ALL houses."""

    def test_planet_aspecting_one_of_listed_houses_fails(self, chart):
        """If planet aspects one of the listed houses, condition should fail."""
        from src.calculations.rule_firing import (
            _check_compound_conditions, _planet_house, _planet_aspects_house,
        )

        # Every planet aspects the 7th house from its position
        planet = "Jupiter"
        actual_house = _planet_house(chart, planet)
        aspected_house = ((actual_house - 1 + 6) % 12) + 1  # 7th from planet

        # Verify the planet actually aspects this house
        assert _planet_aspects_house(chart, planet, aspected_house), (
            f"{planet} should aspect house {aspected_house} (7th from {actual_house})"
        )

        # List includes the aspected house
        conditions = [{
            "type": "planet_not_aspecting",
            "planet": planet,
            "house": [1, aspected_house, 12],
        }]
        fires, _ = _check_compound_conditions(conditions, chart)
        assert not fires, (
            f"{planet} aspects house {aspected_house}, "
            f"planet_not_aspecting with list {[1, aspected_house, 12]} should fail"
        )

    def test_planet_not_aspecting_any_listed_house_passes(self, chart):
        """If planet does NOT aspect any listed house, condition should pass."""
        from src.calculations.rule_firing import (
            _check_compound_conditions, _planet_aspects_house,
        )

        planet = "Venus"
        # Find houses Venus does NOT aspect
        non_aspected = [
            h for h in range(1, 13)
            if not _planet_aspects_house(chart, planet, h)
        ]
        assert len(non_aspected) >= 2, "Venus should have non-aspected houses"

        conditions = [{
            "type": "planet_not_aspecting",
            "planet": planet,
            "house": non_aspected[:3],
        }]
        fires, _ = _check_compound_conditions(conditions, chart)
        assert fires, (
            f"{planet} does not aspect {non_aspected[:3]}, "
            f"planet_not_aspecting should pass"
        )

    def test_single_value_still_works(self, chart):
        """Single int value (non-list) should still work."""
        from src.calculations.rule_firing import (
            _check_compound_conditions, _planet_house,
        )

        planet = "Saturn"
        actual_house = _planet_house(chart, planet)
        aspected_house = ((actual_house - 1 + 6) % 12) + 1  # 7th from planet

        # Should fail when planet aspects the house
        conditions = [{
            "type": "planet_not_aspecting",
            "planet": planet,
            "house": aspected_house,
        }]
        fires, _ = _check_compound_conditions(conditions, chart)
        assert not fires
