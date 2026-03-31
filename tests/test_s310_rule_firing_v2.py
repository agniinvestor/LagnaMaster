"""tests/test_s310_rule_firing_v2.py — S310: V2 computable primitive condition tests.

Tests the 8 computable primitives in rule_firing.py:
  planet_in_house, planet_in_sign, planets_conjunct_in_house,
  planets_conjunct, lord_in_house, lord_in_sign, planet_aspecting,
  planet_dignity

Uses the India 1947 fixture (Taurus lagna).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from src.calculations.rule_firing import (
    _check_compound_conditions,
    _lord_of_house,
    _planet_aspects_house,
    _planet_dignity_state,
    _planet_house,
)


# ── Minimal chart fixture (India 1947: Taurus lagna) ──────────────────────────

@dataclass
class _FakePlanet:
    name: str
    longitude: float
    sign: str
    sign_index: int
    degree_in_sign: float
    is_retrograde: bool = False
    speed: float = 1.0


@dataclass
class _FakeChart:
    lagna_sign: str = "Taurus"
    lagna_sign_index: int = 1  # Taurus = 1
    planets: dict = field(default_factory=dict)


def _india_1947():
    """India 1947 chart: Taurus lagna, approximate positions."""
    return _FakeChart(
        lagna_sign="Taurus",
        lagna_sign_index=1,
        planets={
            "Sun": _FakePlanet("Sun", 118.5, "Cancer", 3, 28.5),
            "Moon": _FakePlanet("Moon", 99.2, "Cancer", 3, 9.2),
            "Mars": _FakePlanet("Mars", 72.8, "Gemini", 2, 12.8),
            "Mercury": _FakePlanet("Mercury", 108.3, "Cancer", 3, 18.3),
            "Jupiter": _FakePlanet("Jupiter", 178.9, "Virgo", 5, 28.9),
            "Venus": _FakePlanet("Venus", 101.4, "Cancer", 3, 11.4),
            "Saturn": _FakePlanet("Saturn", 108.7, "Cancer", 3, 18.7),
            "Rahu": _FakePlanet("Rahu", 27.5, "Aries", 0, 27.5, is_retrograde=True),
            "Ketu": _FakePlanet("Ketu", 207.5, "Libra", 6, 27.5, is_retrograde=True),
        },
    )


# ── Helper function tests ─────────────────────────────────────────────────────

def test_lord_of_house_taurus_lagna():
    """Taurus lagna: H1=Venus, H2=Mercury, H3=Moon, H4=Sun, ..."""
    chart = _india_1947()
    assert _lord_of_house(chart, 1) == "Venus"   # Taurus
    assert _lord_of_house(chart, 2) == "Mercury"  # Gemini
    assert _lord_of_house(chart, 3) == "Moon"     # Cancer
    assert _lord_of_house(chart, 4) == "Sun"      # Leo
    assert _lord_of_house(chart, 5) == "Mercury"  # Virgo
    assert _lord_of_house(chart, 9) == "Saturn"   # Capricorn
    assert _lord_of_house(chart, 10) == "Saturn"  # Aquarius


def test_planet_house_india_1947():
    """Sun in Cancer = H3 for Taurus lagna."""
    chart = _india_1947()
    assert _planet_house(chart, "Sun") == 3      # Cancer(3) - Taurus(1) + 1 = 3
    assert _planet_house(chart, "Jupiter") == 5  # Virgo(5) - Taurus(1) + 1 = 5
    assert _planet_house(chart, "Rahu") == 12    # Aries(0) - Taurus(1) + 1 = 12


def test_planet_dignity_state():
    chart = _india_1947()
    # Jupiter in Virgo — not exalted, not debilitated, not own sign
    assert _planet_dignity_state(chart, "Jupiter") == "neutral"
    # Moon in Cancer — own sign
    assert _planet_dignity_state(chart, "Moon") == "own_sign"


def test_planet_aspects_house():
    """Jupiter in H5 (Virgo) aspects H11 (7th), H9 (5th special), H1 (9th special)."""
    chart = _india_1947()
    # Jupiter is in H5. 7th from H5 = H11.
    assert _planet_aspects_house(chart, "Jupiter", 11) is True
    # Jupiter 5th aspect: H5 + 5 = H9 (but Jupiter aspects houses 5 and 9 away)
    # diff = (9 - 5) % 12 = 4 → in Jupiter's special aspects {4, 8}
    assert _planet_aspects_house(chart, "Jupiter", 9) is True
    # diff = (1 - 5) % 12 = 8 → in Jupiter's special aspects
    assert _planet_aspects_house(chart, "Jupiter", 1) is True
    # Jupiter does NOT aspect H6 (diff = 1)
    assert _planet_aspects_house(chart, "Jupiter", 6) is False


# ── Compound condition tests ──────────────────────────────────────────────────

def test_planet_in_house_condition():
    chart = _india_1947()
    conds = [{"type": "planet_in_house", "planet": "Sun", "house": 3}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires is True
    assert house == 3


def test_planet_in_house_list():
    chart = _india_1947()
    conds = [{"type": "planet_in_house", "planet": "Sun", "house": [1, 3, 5]}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires is True


def test_planet_in_house_miss():
    chart = _india_1947()
    conds = [{"type": "planet_in_house", "planet": "Sun", "house": 7}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False


def test_lord_in_house_condition():
    """Lord of 3rd (Moon, Cancer) is in H3 (Cancer) for Taurus lagna → fires."""
    chart = _india_1947()
    conds = [{"type": "lord_in_house", "lord_of": 3, "house": 3}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires is True
    assert house == 3


def test_lord_in_house_list():
    """Lord of 9th (Saturn, Capricorn) is in H3 (Cancer). Check if in [1,3,5,7]."""
    chart = _india_1947()
    conds = [{"type": "lord_in_house", "lord_of": 9, "house": [1, 3, 5, 7]}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_lord_in_house_miss():
    """Lord of 9th (Saturn) is in H3. Check if in [10, 11] → miss."""
    chart = _india_1947()
    conds = [{"type": "lord_in_house", "lord_of": 9, "house": [10, 11]}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False


def test_planet_dignity_exalted():
    """Construct a chart where Jupiter is exalted (Cancer, si=3)."""
    chart = _FakeChart(
        lagna_sign="Aries", lagna_sign_index=0,
        planets={"Jupiter": _FakePlanet("Jupiter", 100.0, "Cancer", 3, 10.0)},
    )
    conds = [{"type": "planet_dignity", "planet": "Jupiter", "dignity": "exalted"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_planet_dignity_debilitated():
    """Jupiter in Capricorn (si=9) is debilitated."""
    chart = _FakeChart(
        lagna_sign="Aries", lagna_sign_index=0,
        planets={"Jupiter": _FakePlanet("Jupiter", 280.0, "Capricorn", 9, 10.0)},
    )
    conds = [{"type": "planet_dignity", "planet": "Jupiter", "dignity": "debilitated"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_planet_dignity_lord_of_reference():
    """'lord_of_3' should resolve to Moon for Taurus, then check Moon's dignity."""
    chart = _india_1947()
    # Moon is in Cancer (own sign)
    conds = [{"type": "planet_dignity", "planet": "lord_of_3", "dignity": "own_sign"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_planet_aspecting_condition():
    """Jupiter in H5 aspects H11 (7th aspect)."""
    chart = _india_1947()
    conds = [{"type": "planet_aspecting", "planet": "Jupiter", "house": 11}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires is True
    assert house == 11


def test_compound_and_logic():
    """Two conditions must BOTH be true."""
    chart = _india_1947()
    # Sun in H3 AND lord of 3 (Moon) in H3 → both true
    conds = [
        {"type": "planet_in_house", "planet": "Sun", "house": 3},
        {"type": "lord_in_house", "lord_of": 3, "house": 3},
    ]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_compound_and_logic_one_fails():
    """If one condition fails, the whole compound fails."""
    chart = _india_1947()
    # Sun in H3 (true) AND lord of 9 in H10 (false — Saturn is in H3)
    conds = [
        {"type": "planet_in_house", "planet": "Sun", "house": 3},
        {"type": "lord_in_house", "lord_of": 9, "house": 10},
    ]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False


def test_planets_conjunct_in_house():
    """Sun and Moon are both in Cancer (H3) for India 1947."""
    chart = _india_1947()
    conds = [{"type": "planets_conjunct_in_house", "planets": ["Sun", "Moon"], "house": 3}]
    fires, house = _check_compound_conditions(conds, chart)
    assert fires is True
    assert house == 3
