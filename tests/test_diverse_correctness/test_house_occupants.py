"""Phase 2: Planets-in-house correctness across diverse charts."""
import pytest

pytestmark = pytest.mark.phase2

PLANET_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                "Saturn", "Rahu", "Ketu"]


class TestHouseOccupants:
    def test_planets_in_houses(self, verified_chart, computed_chart):
        for h in range(1, 13):
            key = f"house_{h}_planets"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            sign_idx = (computed_chart.lagna_sign_index + h - 1) % 12
            occupants = sorted(
                name for name in PLANET_NAMES
                if computed_chart.planets[name].sign_index == sign_idx
            )
            lm_val = ",".join(occupants) if occupants else ""
            assert lm_val == verdict["pjh"], (
                f"H{h}: LM={lm_val} vs PJH={verdict['pjh']}"
            )
