"""Phase 2: 7th-house aspect correctness across diverse charts."""
import pytest

pytestmark = pytest.mark.phase2

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


class TestSeventhAspect:
    PLANETS = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]

    def test_7th_aspects(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"aspect7_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            pos = computed_chart.planets[planet.capitalize()]
            aspected = SIGNS[(pos.sign_index + 6) % 12]
            assert aspected == verdict["pjh"], (
                f"{planet} 7th aspect: LM={aspected} vs PJH={verdict['pjh']}"
            )
