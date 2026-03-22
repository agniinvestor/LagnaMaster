"""
tests/test_session20.py — LagnaMaster Session 20
Tests for:
  - src/db_pg.py   PostgreSQL / SQLite auto-select + immutable inserts
  - src/cache.py   Redis 3-tier caching (no-op when Redis absent)
  - src/api/main_v2.py  Updated health endpoint + cache integration

All tests pass with no external services (SQLite + disabled Redis).
PostgreSQL-specific tests are skipped unless PG_DSN is set.
Redis-specific tests verify graceful degradation when Redis is absent.

Run:
    PYTHONPATH=. pytest tests/test_session20.py -v
"""

from __future__ import annotations

import json
import os
import pytest


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

INDIA_1947_CHART_JSON = json.dumps(
    {
        "jd_ut": 2432412.2708,
        "ayanamsha_name": "lahiri",
        "ayanamsha_value": 23.1489,
        "lagna": 37.7286,
        "lagna_sign": "Taurus",
        "lagna_sign_index": 1,
        "lagna_degree_in_sign": 7.7286,
        "planets": {
            "Sun": {
                "name": "Sun",
                "longitude": 117.989,
                "sign": "Cancer",
                "sign_index": 3,
                "degree_in_sign": 27.989,
                "is_retrograde": False,
                "speed": 0.953,
            },
            "Moon": {
                "name": "Moon",
                "longitude": 93.983,
                "sign": "Cancer",
                "sign_index": 3,
                "degree_in_sign": 3.983,
                "is_retrograde": False,
                "speed": 13.1,
            },
        },
    }
)

INDIA_1947_SCORES_JSON = json.dumps(
    {
        "lagna_sign": "Taurus",
        "houses": {
            "1": {
                "house": 1,
                "domain": "Self & Vitality",
                "bhavesh": "Venus",
                "bhavesh_house": 3,
                "raw_score": 2.5,
                "final_score": 2.5,
                "rating": "Moderate",
                "rules": [],
            }
        },
    }
)


# ──────────────────────────────────────────────────────────────────────────────
# db_pg — SQLite fallback (always runs, no PG_DSN needed)
# ──────────────────────────────────────────────────────────────────────────────


class TestDbPgSQLiteFallback:
    """db_pg auto-selects SQLite when PG_DSN is absent."""

    def setup_method(self):
        """Ensure PG_DSN is not set and reset db_pg state."""
        os.environ.pop("PG_DSN", None)
        import src.db_pg as pg

        pg._USE_PG = False
        pg._pool = None

    def test_health_check_returns_sqlite(self):
        import src.db_pg as pg

        pg.init_db()
        result = pg.health_check()
        assert result["backend"] == "sqlite"
        assert result["ok"] is True

    def test_save_and_get_chart_roundtrip(self, tmp_path):
        import src.db as sqlite_db
        import src.db_pg as pg

        sqlite_db.DB_PATH = str(tmp_path / "test.db")
        pg.init_db()

        chart_id = pg.save_chart(
            year=1947,
            month=8,
            day=15,
            hour=0.0,
            lat=28.6139,
            lon=77.2090,
            tz_offset=5.5,
            ayanamsha="lahiri",
            chart_json=INDIA_1947_CHART_JSON,
            scores_json=INDIA_1947_SCORES_JSON,
            name="India Independence",
        )
        assert isinstance(chart_id, int)
        assert chart_id >= 1

        row = pg.get_chart(chart_id)
        assert row is not None
        assert row["year"] == 1947
        assert row["name"] == "India Independence"
        assert "chart_json" in row

    def test_get_missing_chart_returns_none(self, tmp_path):
        import src.db as sqlite_db
        import src.db_pg as pg

        sqlite_db.DB_PATH = str(tmp_path / "test2.db")
        pg.init_db()
        assert pg.get_chart(99999) is None

    def test_list_charts_ordered(self, tmp_path):
        import src.db as sqlite_db
        import src.db_pg as pg

        sqlite_db.DB_PATH = str(tmp_path / "test3.db")
        pg.init_db()

        for i in range(3):
            pg.save_chart(
                year=2000 + i,
                month=1,
                day=1,
                hour=12.0,
                lat=0.0,
                lon=0.0,
                tz_offset=0.0,
                ayanamsha="lahiri",
                chart_json=INDIA_1947_CHART_JSON,
                name=f"Chart {i}",
            )

        rows = pg.list_charts(limit=10)
        assert len(rows) == 3
        # Most recent first
        assert rows[0]["year"] == 2002

    def test_immutable_insert_creates_new_row(self, tmp_path):
        """Two saves with identical data produce two distinct rows."""
        import src.db as sqlite_db
        import src.db_pg as pg

        sqlite_db.DB_PATH = str(tmp_path / "test4.db")
        pg.init_db()

        id1 = pg.save_chart(
            year=1947,
            month=8,
            day=15,
            hour=0.0,
            lat=28.6139,
            lon=77.2090,
            tz_offset=5.5,
            ayanamsha="lahiri",
            chart_json=INDIA_1947_CHART_JSON,
        )
        id2 = pg.save_chart(
            year=1947,
            month=8,
            day=15,
            hour=0.0,
            lat=28.6139,
            lon=77.2090,
            tz_offset=5.5,
            ayanamsha="lahiri",
            chart_json=INDIA_1947_CHART_JSON,
        )
        assert id1 != id2


# ──────────────────────────────────────────────────────────────────────────────
# db_pg — PostgreSQL path (skipped without PG_DSN)
# ──────────────────────────────────────────────────────────────────────────────


@pytest.mark.skipif(
    not os.environ.get("PG_DSN"),
    reason="PG_DSN not set — PostgreSQL tests skipped",
)
class TestDbPgPostgres:
    def test_pg_health_check(self):
        import src.db_pg as pg

        pg._pool = None
        pg._USE_PG = False
        pg.init_db()
        result = pg.health_check()
        assert result["backend"] == "postgres"
        assert result["ok"] is True

    def test_pg_save_get_roundtrip(self):
        import src.db_pg as pg

        pg.init_db()
        chart_id = pg.save_chart(
            year=1947,
            month=8,
            day=15,
            hour=0.0,
            lat=28.6139,
            lon=77.2090,
            tz_offset=5.5,
            ayanamsha="lahiri",
            chart_json=INDIA_1947_CHART_JSON,
        )
        row = pg.get_chart(chart_id)
        assert row is not None
        assert row["year"] == 1947


# ──────────────────────────────────────────────────────────────────────────────
# cache.py — graceful no-op when Redis is absent
# ──────────────────────────────────────────────────────────────────────────────


class TestCacheNoRedis:
    """All cache operations silently no-op when Redis is unavailable."""

    def setup_method(self):
        os.environ.pop("REDIS_URL", None)
        import src.cache as c

        c._client = None
        c._disabled = False

    def test_get_returns_none_without_redis(self):
        import src.cache as c

        os.environ["REDIS_URL"] = ""
        c._disabled = False
        c._client = None
        assert c.get(c.TIER_EPHEMERIS, "missing_key") is None

    def test_set_does_not_raise_without_redis(self):
        import src.cache as c

        os.environ["REDIS_URL"] = ""
        c._disabled = False
        c._client = None
        c.set(c.TIER_EPHEMERIS, "key", {"data": 1})  # must not raise

    def test_health_check_returns_not_ok(self):
        import src.cache as c

        os.environ["REDIS_URL"] = ""
        c._disabled = False
        c._client = None
        result = c.health_check()
        assert result["backend"] == "redis"
        assert result["ok"] is False

    def test_flush_tier_returns_zero_without_redis(self):
        import src.cache as c

        os.environ["REDIS_URL"] = ""
        c._disabled = False
        c._client = None
        assert c.flush_tier(c.TIER_SCORES) == 0


class TestCacheKeyBuilders:
    """Key builder functions are deterministic and stable."""

    def test_ephemeris_key_is_deterministic(self):
        import src.cache as c

        k1 = c.make_ephemeris_key(1947, 8, 15, 0.0, 28.6139, 77.209, 5.5, "lahiri")
        k2 = c.make_ephemeris_key(1947, 8, 15, 0.0, 28.6139, 77.209, 5.5, "lahiri")
        assert k1 == k2

    def test_ephemeris_key_differs_by_ayanamsha(self):
        import src.cache as c

        k_lahiri = c.make_ephemeris_key(
            1947, 8, 15, 0.0, 28.6139, 77.209, 5.5, "lahiri"
        )
        k_raman = c.make_ephemeris_key(1947, 8, 15, 0.0, 28.6139, 77.209, 5.5, "raman")
        assert k_lahiri != k_raman

    def test_scores_key_includes_version(self):
        import src.cache as c

        os.environ["CACHE_VERSION"] = "1"
        k1 = c.make_scores_key(42)
        os.environ["CACHE_VERSION"] = "2"
        k2 = c.make_scores_key(42)
        assert k1 != k2
        os.environ.pop("CACHE_VERSION", None)

    def test_av_key_is_string(self):
        import src.cache as c

        assert c.make_av_key(7) == "7"

    def test_different_chart_ids_differ(self):
        import src.cache as c

        assert c.make_scores_key(1) != c.make_scores_key(2)


# ──────────────────────────────────────────────────────────────────────────────
# API v2 health endpoint — always includes db + cache status
# ──────────────────────────────────────────────────────────────────────────────


class TestApiV2Health:
    @pytest.fixture(autouse=True)
    def client(self, tmp_path):
        os.environ.pop("PG_DSN", None)
        os.environ["REDIS_URL"] = ""

        import src.db as sqlite_db
        import src.db_pg as pg
        import src.cache as c

        sqlite_db.DB_PATH = str(tmp_path / "test_api.db")
        pg._pool = None
        pg._USE_PG = False
        c._client = None
        c._disabled = False

        from fastapi.testclient import TestClient
        from src.api.main_v2 import app

        pg.init_db()
        self._client = TestClient(app)

    def test_health_returns_200(self):
        r = self._client.get("/health")
        assert r.status_code == 200

    def test_health_has_db_and_cache_keys(self):
        r = self._client.get("/health")
        body = r.json()
        assert "db" in body
        assert "cache" in body
        assert "version" in body

    def test_health_db_backend_is_sqlite(self):
        r = self._client.get("/health")
        assert r.json()["db"]["backend"] == "sqlite"

    def test_health_cache_not_ok_without_redis(self):
        r = self._client.get("/health")
        assert r.json()["cache"]["ok"] is False
