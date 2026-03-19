"""
tests/test_ui.py
================
Tests for the UI data layer (non-browser).
Validates that the full compute → score → save → retrieve round-trip works
exactly as the Streamlit app uses it.
"""

import pytest
from tests.fixtures import INDIA_1947


@pytest.fixture(scope="module")
def db_path(tmp_path_factory):
    import src.db as db
    p = tmp_path_factory.mktemp("ui_data") / "ui_test.db"
    db.DB_PATH = p
    db.init_db()
    return p


class TestUIRoundTrip:
    def test_compute_and_save(self, db_path):
        """Full compute → score → save round-trip (mirrors _run_compute in UI)."""
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
        from src.db import save_chart, get_chart

        f = INDIA_1947
        chart = compute_chart(
            year=f["year"], month=f["month"], day=f["day"],
            hour=f["hour"], lat=f["lat"], lon=f["lon"],
            tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
        )
        scores = score_chart(chart)

        chart_json = {
            "lagna_sign": chart.lagna_sign,
            "lagna_sign_index": chart.lagna_sign_index,
            "lagna_degree": chart.lagna_degree_in_sign,
            "ayanamsha_name": chart.ayanamsha_name,
            "ayanamsha_value": chart.ayanamsha_value,
            "jd_ut": chart.jd_ut,
            "planets": {
                n: {
                    "sign": p.sign, "sign_index": p.sign_index,
                    "degree_in_sign": p.degree_in_sign,
                    "longitude": p.longitude,
                    "is_retrograde": p.is_retrograde, "speed": p.speed,
                }
                for n, p in chart.planets.items()
            },
        }
        scores_json = {
            str(h): {
                "domain": hs.domain, "final_score": hs.final_score,
                "raw_score": hs.raw_score, "rating": hs.rating,
                "bhavesh": hs.bhavesh, "bhavesh_house": hs.bhavesh_house,
            }
            for h, hs in scores.houses.items()
        }

        chart_id = save_chart(
            year=f["year"], month=f["month"], day=f["day"],
            hour=f["hour"], lat=f["lat"], lon=f["lon"],
            tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
            chart_json=chart_json, scores_json=scores_json,
            name="India Independence",
        )
        assert chart_id >= 1

        row = get_chart(chart_id)
        assert row is not None
        assert row["chart_json"]["lagna_sign"] == "Taurus"
        assert row["scores_json"]["1"]["bhavesh"] == "Venus"
        assert row["name"] == "India Independence"

    def test_history_list(self, db_path):
        """list_charts returns saved entries."""
        from src.db import list_charts
        rows = list_charts(limit=10)
        assert len(rows) >= 1
        assert rows[0]["year"] == 1947

    def test_score_card_data(self, db_path):
        """Score cards display correct fields for all 12 houses."""
        from src.ephemeris import compute_chart
        from src.scoring import score_chart

        f = INDIA_1947
        chart = compute_chart(**{k: f[k] for k in ["year","month","day","hour","lat","lon","tz_offset","ayanamsha"]})
        scores = score_chart(chart)

        valid_ratings = {"Excellent", "Strong", "Moderate", "Weak", "Very Weak"}
        for h in range(1, 13):
            hs = scores.houses[h]
            assert hs.domain, f"H{h} missing domain"
            assert hs.bhavesh, f"H{h} missing bhavesh"
            assert 1 <= hs.bhavesh_house <= 12
            assert hs.rating in valid_ratings
            assert -10.0 <= hs.final_score <= 10.0

    def test_rule_breakdown_totals(self, db_path):
        """Effective score from rules matches stored final_score for all 12 houses."""
        from src.ephemeris import compute_chart
        from src.scoring import score_chart

        f = INDIA_1947
        chart = compute_chart(**{k: f[k] for k in ["year","month","day","hour","lat","lon","tz_offset","ayanamsha"]})
        scores = score_chart(chart)

        for h, hs in scores.houses.items():
            computed = sum(r.score * (0.5 if r.is_wc else 1.0) for r in hs.rules)
            # raw_score should match the sum; final_score is the clamped version
            assert abs(computed - hs.raw_score) < 1e-9, f"H{h} raw mismatch"

    def test_house_map_display(self, db_path):
        """Whole-sign house map has 12 entries, all planets assigned."""
        from src.ephemeris import compute_chart
        from src.calculations.house_lord import compute_house_map

        f = INDIA_1947
        chart = compute_chart(**{k: f[k] for k in ["year","month","day","hour","lat","lon","tz_offset","ayanamsha"]})
        hmap = compute_house_map(chart)

        assert len(hmap.house_sign) == 12
        assert len(hmap.house_lord) == 12
        for pname in chart.planets:
            assert pname in hmap.planet_house, f"{pname} not in planet_house"
            assert 1 <= hmap.planet_house[pname] <= 12

    def test_demo_button_values(self, db_path):
        """Demo data (1947) produces Taurus lagna — matches sidebar preset."""
        from src.ephemeris import compute_chart
        chart = compute_chart(1947, 8, 15, 0.0, 28.6139, 77.2090, 5.5, "lahiri")
        assert chart.lagna_sign == "Taurus"
        assert abs(chart.lagna_degree_in_sign - 7.7286) < 0.05
