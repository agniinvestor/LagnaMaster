"""Phase 2: House lord correctness across diverse charts."""
from src.data.constants import SIGN_LORDS
import pytest

pytestmark = pytest.mark.phase2



class TestHouseLords:
    def test_all_12_house_lords(self, verified_chart, computed_chart):
        for h in range(1, 13):
            key = f"house_{h}_lord"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            sign_idx = (computed_chart.lagna_sign_index + h - 1) % 12
            lm_lord = SIGN_LORDS[sign_idx]
            assert lm_lord == verdict["pjh"], (
                f"H{h}: LM={lm_lord} vs PJH={verdict['pjh']}"
            )
