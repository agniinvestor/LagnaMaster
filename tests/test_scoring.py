"""
tests/test_scoring.py
======================
Tests for scoring engine and FastAPI endpoints.
"""

import pytest
from datetime import date
from src.ephemeris import compute_chart, BirthChart
from tests.fixtures import INDIA_1947


@pytest.fixture(scope="module")
def india_chart() -> BirthChart:
    f = INDIA_1947
    return compute_chart(
        year=f["year"], month=f["month"], day=f["day"],
        hour=f["hour"], lat=f["lat"], lon=f["lon"],
        tz_offset=f["tz_offset"], ayanamsha=f["ayanamsha"],
    )


# ===========================================================================
# Scoring engine tests
# ===========================================================================

class TestScoringEngine:
    def test_all_12_houses_scored(self, india_chart):
        from src.scoring import score_chart
        result = score_chart(india_chart)
        assert len(result.houses) == 12
        assert set(result.houses.keys()) == set(range(1, 13))

    def test_scores_clamped_to_10(self, india_chart):
        from src.scoring import score_chart
        result = score_chart(india_chart)
        for h, hs in result.houses.items():
            assert -10.0 <= hs.final_score <= 10.0, \
                f"H{h} score {hs.final_score} out of [-10, 10]"

    def test_22_rules_per_house(self, india_chart):
        from src.scoring import score_chart
        result = score_chart(india_chart)
        for h, hs in result.houses.items():
            assert len(hs.rules) == 22, \
                f"H{h} has {len(hs.rules)} rules, expected 22"

    def test_h1_bhavesh_is_venus_for_taurus(self, india_chart):
        """Taurus lagna → H1 Bhavesh = Venus."""
        from src.scoring import score_chart
        result = score_chart(india_chart)
        assert result.houses[1].bhavesh == "Venus"

    def test_h1_lagna_sign(self, india_chart):
        from src.scoring import score_chart
        result = score_chart(india_chart)
        assert result.lagna_sign == "Taurus"

    def test_ratings_are_valid(self, india_chart):
        from src.scoring import score_chart, _rating
        result = score_chart(india_chart)
        valid_ratings = {"Excellent", "Strong", "Moderate", "Weak", "Very Weak"}
        for h, hs in result.houses.items():
            assert hs.rating in valid_ratings, \
                f"H{h} has invalid rating '{hs.rating}'"

    def test_output_life_domains_h2_weak(self, india_chart):
        """
        Excel OUTPUT_LifeDomains shows H2=−5.25 (Very Weak).
        Our engine should also score H2 negatively.
        """
        from src.scoring import score_chart
        result = score_chart(india_chart)
        assert result.houses[2].final_score < 0, \
            f"H2 (Wealth) should be negative for 1947 chart, got {result.houses[2].final_score}"

    def test_output_life_domains_h7_weak(self, india_chart):
        """Excel H7=−4.25 (Very Weak) — relationships afflicted."""
        from src.scoring import score_chart
        result = score_chart(india_chart)
        assert result.houses[7].final_score < 0, \
            f"H7 should be negative, got {result.houses[7].final_score}"

    def test_planet_aspects_engine(self):
        """Jupiter aspects 5th/7th/9th from its house."""
        from src.scoring import _planet_aspects_house
        # Jupiter in H6: aspects H10 (5th from H6), H12 (7th from H6), H2 (9th from H6)
        assert _planet_aspects_house("Jupiter", 6, 10)
        assert _planet_aspects_house("Jupiter", 6, 12)
        assert _planet_aspects_house("Jupiter", 6,  2)
        assert not _planet_aspects_house("Jupiter", 6, 1)

    def test_mars_special_aspects(self):
        """Mars aspects 4th/7th/8th from its house."""
        from src.scoring import _planet_aspects_house
        # Mars in H2: aspects H5 (4th), H8 (7th), H9 (8th)
        assert _planet_aspects_house("Mars", 2, 5)
        assert _planet_aspects_house("Mars", 2, 8)
        assert _planet_aspects_house("Mars", 2, 9)

    def test_saturn_special_aspects(self):
        """Saturn aspects 3rd/7th/10th from its house."""
        from src.scoring import _planet_aspects_house
        # Saturn in H3: aspects H5 (3rd), H9 (7th), H12 (10th)
        assert _planet_aspects_house("Saturn", 3, 5)
        assert _planet_aspects_house("Saturn", 3, 9)
        assert _planet_aspects_house("Saturn", 3, 12)

    def test_summary_output(self, india_chart):
        from src.scoring import score_chart
        result = score_chart(india_chart)
        summary = result.summary()
        assert "Taurus" in summary
        assert "Self" in summary


# ===========================================================================
# API tests
# ===========================================================================

class TestAPI:
    @pytest.fixture(scope="class")
    def client(self, tmp_path_factory):
        import src.db as db
        db.DB_PATH = tmp_path_factory.mktemp("data") / "test.db"
        from fastapi.testclient import TestClient
        from src.api.main import app
        db.init_db()   # ensure tables exist with correct path
        return TestClient(app)

    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_create_chart_1947(self, client):
        f = INDIA_1947
        r = client.post("/charts", json={
            "year": f["year"], "month": f["month"], "day": f["day"],
            "hour": f["hour"], "lat": f["lat"], "lon": f["lon"],
            "tz_offset": f["tz_offset"], "ayanamsha": f["ayanamsha"],
            "name": "India Independence",
        })
        assert r.status_code == 201
        body = r.json()
        assert body["lagna_sign"] == "Taurus"
        assert "Sun" in body["planets"]
        assert body["planets"]["Sun"]["sign"] == "Cancer"
        assert body["id"] >= 1

    def test_get_chart(self, client):
        # Create first
        f = INDIA_1947
        post_r = client.post("/charts", json={
            "year": f["year"], "month": f["month"], "day": f["day"],
            "hour": f["hour"], "lat": f["lat"], "lon": f["lon"],
        })
        chart_id = post_r.json()["id"]
        # Then retrieve
        get_r = client.get(f"/charts/{chart_id}")
        assert get_r.status_code == 200
        assert get_r.json()["id"] == chart_id

    def test_get_chart_not_found(self, client):
        r = client.get("/charts/99999")
        assert r.status_code == 404

    def test_get_scores(self, client):
        f = INDIA_1947
        post_r = client.post("/charts", json={
            "year": f["year"], "month": f["month"], "day": f["day"],
            "hour": f["hour"], "lat": f["lat"], "lon": f["lon"],
        })
        chart_id = post_r.json()["id"]
        scores_r = client.get(f"/charts/{chart_id}/scores")
        assert scores_r.status_code == 200
        body = scores_r.json()
        assert body["lagna_sign"] == "Taurus"
        assert len(body["houses"]) == 12
        # Each house has 22 rules
        h1 = body["houses"]["1"]
        assert len(h1["rules"]) == 22
        assert h1["bhavesh"] == "Venus"

    def test_list_charts(self, client):
        r = client.get("/charts")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_invalid_ayanamsha_rejected(self, client):
        r = client.post("/charts", json={
            "year": 2000, "month": 1, "day": 1,
            "hour": 12.0, "lat": 28.6, "lon": 77.2,
            "ayanamsha": "tropical",
        })
        assert r.status_code == 422

    def test_midnight_birth_api(self, client):
        """P-1 regression: hour=0.0 must work through the API."""
        f = INDIA_1947
        r = client.post("/charts", json={
            "year": f["year"], "month": f["month"], "day": f["day"],
            "hour": 0.0, "lat": f["lat"], "lon": f["lon"],
        })
        assert r.status_code == 201
        assert r.json()["lagna_sign"] == "Taurus"
