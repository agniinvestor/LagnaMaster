"""Phase 1: Panchangam correctness across diverse charts."""
import pytest
from datetime import datetime

from src.calculations.panchanga import compute_panchanga

pytestmark = pytest.mark.phase1


class TestPanchangam:
    def test_tithi(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("tithi")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        bd = verified_chart["birth_data"]
        p = compute_panchanga(
            computed_chart.planets["Sun"].longitude,
            computed_chart.planets["Moon"].longitude,
            datetime(bd["year"], bd["month"], bd["day"],
                     int(bd["hour"]), int((bd["hour"] % 1) * 60)),
        )
        assert p.tithi == verdict["pjh"], f"Tithi: LM={p.tithi} vs PJH={verdict['pjh']}"

    def test_vara(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("vara")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        bd = verified_chart["birth_data"]
        p = compute_panchanga(
            computed_chart.planets["Sun"].longitude,
            computed_chart.planets["Moon"].longitude,
            datetime(bd["year"], bd["month"], bd["day"],
                     int(bd["hour"]), int((bd["hour"] % 1) * 60)),
        )
        assert p.vara == verdict["pjh"], f"Vara: LM={p.vara} vs PJH={verdict['pjh']}"

    def test_yoga(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("yoga")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        bd = verified_chart["birth_data"]
        p = compute_panchanga(
            computed_chart.planets["Sun"].longitude,
            computed_chart.planets["Moon"].longitude,
            datetime(bd["year"], bd["month"], bd["day"],
                     int(bd["hour"]), int((bd["hour"] % 1) * 60)),
        )
        assert p.yoga == verdict["pjh"], f"Yoga: LM={p.yoga} vs PJH={verdict['pjh']}"
