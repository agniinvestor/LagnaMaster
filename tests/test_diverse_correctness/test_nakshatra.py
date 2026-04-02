"""Phase 1: Nakshatra correctness across diverse charts."""
import pytest

from src.calculations.nakshatra import nakshatra_position

pytestmark = pytest.mark.phase1


class TestMoonNakshatra:
    def test_moon_nakshatra(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("nakshatra_moon")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip("disputed or missing")
        moon_nak = nakshatra_position(computed_chart.planets["Moon"].longitude)
        assert moon_nak.nakshatra == verdict["pjh"]
