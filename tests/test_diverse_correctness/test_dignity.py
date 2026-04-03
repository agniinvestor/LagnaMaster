"""Phase 2: Dignity correctness across diverse charts."""
import pytest

from src.calculations.dignity import compute_dignity

pytestmark = pytest.mark.phase2

# Coarse dignity labels matching diff_engine comparison
_COARSE = {
    "Own Sign": "own", "Exalted": "exalted", "Debilitated": "debilitated",
    "Mooltrikona": "own", "Friendly Sign": "other", "Neutral Sign": "other",
    "Enemy Sign": "other", "Great Friend Sign": "other", "Great Enemy Sign": "other",
}
_PLANETS = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]


class TestDignity:
    def test_planet_dignities(self, verified_chart, computed_chart):
        for planet in _PLANETS:
            key = f"dignity_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            d = compute_dignity(planet.capitalize(), computed_chart)
            lm_coarse = _COARSE.get(d.dignity.value, "other")
            assert lm_coarse == verdict["pjh"], (
                f"{planet}: LM={lm_coarse} vs PJH={verdict['pjh']}"
            )
