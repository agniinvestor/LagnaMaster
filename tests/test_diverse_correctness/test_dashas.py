"""Phase 3: Vimsottari dasha sequence correctness across diverse charts."""
import pytest

pytestmark = pytest.mark.phase3


class TestVimsottariSequence:
    def test_mahadasha_sequence(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("vimsottari_sequence")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")

        # Recompute from LM
        from datetime import datetime
        from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

        bd = verified_chart["birth_data"]
        birth_dt = datetime(bd["year"], bd["month"], bd["day"],
                            int(bd["hour"]), int((bd["hour"] % 1) * 60))
        vd = compute_vimshottari_dasa(computed_chart, birth_dt)
        if isinstance(vd, list) and vd:
            lm_seq = ",".join(md.lord for md in vd)
            assert lm_seq == verdict["pjh"], (
                f"Dasha: LM={lm_seq} vs PJH={verdict['pjh']}"
            )
