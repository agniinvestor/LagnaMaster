"""
tests/test_integration.py
==========================
End-to-end integration tests — full user journey as it runs in Docker.

Tests the complete stack: birth data → compute → score → SQLite → API retrieval,
including multi-chart scenarios, history ordering, and idempotency.
"""

import pytest
from tests.fixtures import INDIA_1947


# ---------------------------------------------------------------------------
# Shared DB fixture (one DB for the whole module — tests build on each other)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    """Full API client backed by a temporary SQLite database."""
    import src.db as db

    db.DB_PATH = tmp_path_factory.mktemp("integration") / "int_test.db"
    db.init_db()
    from fastapi.testclient import TestClient
    from src.api.main import app

    return TestClient(app)


# ---------------------------------------------------------------------------
# Journey 1: single chart — create, retrieve, score
# ---------------------------------------------------------------------------


class TestSingleChartJourney:
    _chart_id: int = None

    def test_health_check(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_create_india_1947(self, client):
        f = INDIA_1947
        r = client.post(
            "/charts",
            json={
                "year": f["year"],
                "month": f["month"],
                "day": f["day"],
                "hour": f["hour"],
                "lat": f["lat"],
                "lon": f["lon"],
                "tz_offset": f["tz_offset"],
                "ayanamsha": f["ayanamsha"],
                "name": "India Independence",
            },
        )
        assert r.status_code == 201
        body = r.json()
        assert body["lagna_sign"] == "Taurus"
        assert body["id"] >= 1
        assert "Sun" in body["planets"]
        assert body["planets"]["Sun"]["sign"] == "Cancer"
        assert body["planets"]["Ketu"]["sign"] == "Scorpio"
        TestSingleChartJourney._chart_id = body["id"]

    def test_retrieve_chart(self, client):
        cid = TestSingleChartJourney._chart_id
        r = client.get(f"/charts/{cid}")
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == cid
        assert body["lagna_sign"] == "Taurus"
        assert abs(body["lagna_degree"] - 7.7286) < 0.05

    def test_get_scores(self, client):
        cid = TestSingleChartJourney._chart_id
        r = client.get(f"/charts/{cid}/scores")
        assert r.status_code == 200
        body = r.json()
        assert body["chart_id"] == cid
        assert body["lagna_sign"] == "Taurus"
        assert len(body["houses"]) == 12
        # H1 lord (Bhavesh) for Taurus lagna = Venus
        assert body["houses"]["1"]["bhavesh"] == "Venus"
        # Each house has 22 rules
        for h_str, hs in body["houses"].items():
            assert len(hs["rules"]) == 22, f"H{h_str} has {len(hs['rules'])} rules"
            assert -10.0 <= hs["final_score"] <= 10.0
            assert hs["rating"] in {
                "Excellent",
                "Strong",
                "Moderate",
                "Weak",
                "Very Weak",
            }

    def test_score_domains_present(self, client):
        cid = TestSingleChartJourney._chart_id
        r = client.get(f"/charts/{cid}/scores")
        body = r.json()
        expected_domains = {
            "1": "Self & Vitality",
            "2": "Wealth & Family",
            "7": "Relationships",
            "10": "Career & Status",
        }
        for h_str, domain in expected_domains.items():
            assert body["houses"][h_str]["domain"] == domain

    def test_404_on_missing_chart(self, client):
        r = client.get("/charts/99999")
        assert r.status_code == 404

    def test_invalid_ayanamsha_rejected(self, client):
        r = client.post(
            "/charts",
            json={
                "year": 2000,
                "month": 1,
                "day": 1,
                "hour": 12.0,
                "lat": 28.6,
                "lon": 77.2,
                "ayanamsha": "tropical",
            },
        )
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# Journey 2: multiple charts — history, ordering, pagination
# ---------------------------------------------------------------------------


class TestMultiChartHistory:
    _ids: list = []

    def test_create_three_charts(self, client):
        births = [
            {
                "year": 1947,
                "month": 8,
                "day": 15,
                "hour": 0.0,
                "lat": 28.61,
                "lon": 77.21,
                "name": "India",
            },
            {
                "year": 2000,
                "month": 1,
                "day": 1,
                "hour": 6.0,
                "lat": 19.07,
                "lon": 72.87,
                "name": "Millennium Mumbai",
            },
            {
                "year": 1969,
                "month": 7,
                "day": 20,
                "hour": 22.0,
                "lat": 28.61,
                "lon": 77.21,
                "name": "Moon Landing",
            },
        ]
        TestMultiChartHistory._ids = []
        for b in births:
            r = client.post("/charts", json=b)
            assert r.status_code == 201
            TestMultiChartHistory._ids.append(r.json()["id"])
        assert len(TestMultiChartHistory._ids) == 3

    def test_list_returns_newest_first(self, client):
        r = client.get("/charts?limit=10")
        assert r.status_code == 200
        items = r.json()
        ids = [item["id"] for item in items]
        # IDs must be in descending order (newest first)
        assert ids == sorted(ids, reverse=True)

    def test_list_contains_all_names(self, client):
        r = client.get("/charts?limit=20")
        names = [item.get("name") for item in r.json()]
        assert "India Independence" in names  # from Journey 1
        assert "India" in names
        assert "Millennium Mumbai" in names
        assert "Moon Landing" in names

    def test_list_limit_respected(self, client):
        r = client.get("/charts?limit=2")
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_each_chart_independently_retrievable(self, client):
        for cid in TestMultiChartHistory._ids:
            r = client.get(f"/charts/{cid}")
            assert r.status_code == 200
            assert r.json()["id"] == cid

    def test_idempotency_same_birth_data_creates_new_id(self, client):
        """Same birth data → distinct chart records (immutable insert pattern)."""
        f = INDIA_1947
        r1 = client.post(
            "/charts",
            json={
                "year": f["year"],
                "month": f["month"],
                "day": f["day"],
                "hour": f["hour"],
                "lat": f["lat"],
                "lon": f["lon"],
            },
        )
        r2 = client.post(
            "/charts",
            json={
                "year": f["year"],
                "month": f["month"],
                "day": f["day"],
                "hour": f["hour"],
                "lat": f["lat"],
                "lon": f["lon"],
            },
        )
        assert r1.status_code == r2.status_code == 201
        assert r1.json()["id"] != r2.json()["id"]
        # But planet positions are identical
        assert r1.json()["planets"] == r2.json()["planets"]


# ---------------------------------------------------------------------------
# Journey 3: midnight birth edge case (P-1 regression)
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_midnight_birth_end_to_end(self, client):
        """P-1: hour=0.0 must flow through API without error."""
        r = client.post(
            "/charts",
            json={
                "year": 1947,
                "month": 8,
                "day": 15,
                "hour": 0.0,
                "lat": 28.6139,
                "lon": 77.2090,
            },
        )
        assert r.status_code == 201
        assert r.json()["lagna_sign"] == "Taurus"

    def test_rahu_ketu_always_present(self, client):
        """Ketu derived from Rahu must always appear in response."""
        r = client.post(
            "/charts",
            json={
                "year": 2010,
                "month": 6,
                "day": 15,
                "hour": 12.0,
                "lat": 13.08,
                "lon": 80.27,
            },
        )
        assert r.status_code == 201
        planets = r.json()["planets"]
        assert "Rahu" in planets
        assert "Ketu" in planets
        # Ketu is always 180° from Rahu
        rahu_lon = planets["Rahu"]["longitude"]
        ketu_lon = planets["Ketu"]["longitude"]
        diff = abs(((rahu_lon - ketu_lon) % 360) - 180)
        assert diff < 0.001

    def test_scores_deterministic(self, client):
        """Same birth data always produces same scores."""
        f = INDIA_1947
        payload = {
            "year": f["year"],
            "month": f["month"],
            "day": f["day"],
            "hour": f["hour"],
            "lat": f["lat"],
            "lon": f["lon"],
        }
        r1 = client.post("/charts", json=payload)
        r2 = client.post("/charts", json=payload)
        id1, id2 = r1.json()["id"], r2.json()["id"]

        s1 = client.get(f"/charts/{id1}/scores").json()
        s2 = client.get(f"/charts/{id2}/scores").json()

        for h_str in s1["houses"]:
            assert (
                s1["houses"][h_str]["final_score"] == s2["houses"][h_str]["final_score"]
            )

    def test_all_ayanamshas_accepted(self, client):
        """All three supported ayanamshas must succeed."""
        for ayan in ["lahiri", "raman", "krishnamurti"]:
            r = client.post(
                "/charts",
                json={
                    "year": 2000,
                    "month": 1,
                    "day": 1,
                    "hour": 12.0,
                    "lat": 28.6,
                    "lon": 77.2,
                    "ayanamsha": ayan,
                },
            )
            assert r.status_code == 201, f"ayanamsha {ayan!r} failed: {r.text}"
            assert r.json()["ayanamsha_name"] == ayan
