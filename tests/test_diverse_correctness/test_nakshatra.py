"""Phase 2: Nakshatra correctness across diverse charts."""
import pytest

from src.calculations.nakshatra import nakshatra_position

pytestmark = pytest.mark.phase2


class TestPlanetNakshatras:
    PLANETS = ["sun", "moon", "mars", "mercury", "jupiter",
               "venus", "saturn", "rahu", "ketu"]

    def test_planet_nakshatras(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"nakshatra_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            nak = nakshatra_position(
                computed_chart.planets[planet.capitalize()].longitude
            )
            assert nak.nakshatra == verdict["pjh"], (
                f"{planet}: LM={nak.nakshatra} vs PJH={verdict['pjh']}"
            )
