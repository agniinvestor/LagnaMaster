"""Phase 2: House lord correctness across diverse charts."""
import pytest

pytestmark = pytest.mark.phase2

_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
    6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}


class TestHouseLords:
    def test_all_12_house_lords(self, verified_chart, computed_chart):
        for h in range(1, 13):
            key = f"house_{h}_lord"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            sign_idx = (computed_chart.lagna_sign_index + h - 1) % 12
            lm_lord = _SIGN_LORDS[sign_idx]
            assert lm_lord == verdict["pjh"], (
                f"H{h}: LM={lm_lord} vs PJH={verdict['pjh']}"
            )
