"""Phase 3: Ashtakavarga correctness across diverse charts."""
import pytest

pytestmark = pytest.mark.phase3

SIGNS = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
         "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]


class TestSarvaAshtakavarga:
    def test_sarva_av_per_sign(self, verified_chart, computed_chart):
        for sign in SIGNS:
            key = f"sav_{sign}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            from src.calculations.ashtakavarga import compute_ashtakavarga
            av = compute_ashtakavarga(computed_chart)
            idx = SIGNS.index(sign)
            lm_val = av.sarva.bindus[idx]
            assert lm_val == verdict["pjh"], (
                f"SAV {sign}: LM={lm_val} vs PJH={verdict['pjh']}"
            )
