"""
src/api/main_v2.py — LagnaMaster Session 20
FastAPI application — v2 drop-in replacing src/api/main.py.

Changes from v1
---------------
* Uses src.db_pg (PostgreSQL / SQLite auto-select) instead of src.db
* Ephemeris results cached in Redis Tier 1 before DB insert
* Scores cached in Redis Tier 2 on first computation
* AV tables cached in Redis Tier 3
* GET /health returns DB + cache backend status
* All existing endpoints unchanged — fully backwards-compatible
"""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

import src.db_pg as db
import src.cache as cache
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.calculations.ashtakavarga import compute_ashtakavarga
from src.api.models import (
    BirthDataRequest,
    ChartOut,
    ChartScoresOut,
    ChartSummary,
)

_VERSION = "0.2.0"


# ── lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="LagnaMaster API",
    version=_VERSION,
    lifespan=lifespan,
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _chart_to_dict(chart) -> dict:
    """Serialise BirthChart to a plain dict for JSON storage."""
    return {
        "jd_ut": chart.jd_ut,
        "ayanamsha_name": chart.ayanamsha_name,
        "ayanamsha_value": chart.ayanamsha_value,
        "lagna": chart.lagna,
        "lagna_sign": chart.lagna_sign,
        "lagna_sign_index": chart.lagna_sign_index,
        "lagna_degree_in_sign": chart.lagna_degree_in_sign,
        "planets": {
            name: {
                "name": p.name,
                "longitude": p.longitude,
                "sign": p.sign,
                "sign_index": p.sign_index,
                "degree_in_sign": p.degree_in_sign,
                "is_retrograde": p.is_retrograde,
                "speed": p.speed,
            }
            for name, p in chart.planets.items()
        },
    }


def _scores_to_dict(scores) -> dict:
    return {
        "lagna_sign": scores.lagna_sign,
        "houses": {
            str(h): {
                "house": hs.house,
                "domain": hs.domain,
                "bhavesh": hs.bhavesh,
                "bhavesh_house": hs.bhavesh_house,
                "raw_score": hs.raw_score,
                "final_score": hs.final_score,
                "rating": hs.rating,
                "rules": [
                    {
                        "rule": r.rule,
                        "description": r.description,
                        "score": r.score,
                        "is_wc": r.is_wc,
                        "triggered": r.triggered,
                    }
                    for r in hs.rules
                ],
            }
            for h, hs in scores.houses.items()
        },
    }


def _row_to_chart_out(row: dict, chart_id: int) -> ChartOut:
    cj = json.loads(row["chart_json"]) if isinstance(row["chart_json"], str) else row["chart_json"]
    return ChartOut(
        id=chart_id,
        lagna_sign=cj["lagna_sign"],
        lagna_sign_index=cj["lagna_sign_index"],
        lagna_degree=cj["lagna_degree_in_sign"],
        ayanamsha_name=cj["ayanamsha_name"],
        ayanamsha_value=cj["ayanamsha_value"],
        jd_ut=cj["jd_ut"],
        planets=cj["planets"],  # noqa: F841
    )


# ── endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    db_status = db.health_check()
    cache_status = cache.health_check()
    return {
        "status": "ok" if db_status["ok"] else "degraded",
        "version": _VERSION,
        "db": db_status,
        "cache": cache_status,
    }


@app.post("/charts", status_code=201)
def create_chart(req: BirthDataRequest) -> ChartOut:
    # Tier 1: check ephemeris cache
    eph_key = cache.make_ephemeris_key(
        req.year, req.month, req.day, req.hour,
        req.lat, req.lon, req.tz_offset, req.ayanamsha,
    )
    cached_chart_dict = cache.get(cache.TIER_EPHEMERIS, eph_key)

    if cached_chart_dict is None:
        chart = compute_chart(
            req.year, req.month, req.day, req.hour,
            req.lat, req.lon, req.tz_offset, req.ayanamsha,
        )
        chart_dict = _chart_to_dict(chart)
        cache.set(cache.TIER_EPHEMERIS, eph_key, chart_dict)
    else:
        chart_dict = cached_chart_dict
        # Reconstruct a lightweight chart-like object for scoring
        chart = _reconstruct_chart(chart_dict)

    scores = score_chart(chart)
    scores_dict = _scores_to_dict(scores)

    chart_id = db.save_chart(
        year=req.year, month=req.month, day=req.day, hour=req.hour,
        lat=req.lat, lon=req.lon, tz_offset=req.tz_offset,
        ayanamsha=req.ayanamsha,
        chart_json=json.dumps(chart_dict),
        scores_json=json.dumps(scores_dict),
        name=req.name,
    )

    # Tier 2: prime scores cache
    cache.set(cache.TIER_SCORES, cache.make_scores_key(chart_id), scores_dict)

    return ChartOut(
        id=chart_id,
        lagna_sign=chart_dict["lagna_sign"],
        lagna_sign_index=chart_dict["lagna_sign_index"],
        lagna_degree=chart_dict["lagna_degree_in_sign"],
        ayanamsha_name=chart_dict["ayanamsha_name"],
        ayanamsha_value=chart_dict["ayanamsha_value"],
        jd_ut=chart_dict["jd_ut"],
        planets=chart_dict["planets"],  # noqa: F841
    )


@app.get("/charts")
def list_charts(limit: int = 20) -> list[ChartSummary]:
    rows = db.list_charts(limit)
    summaries = []
    for row in rows:
        cj = json.loads(row["chart_json"]) if isinstance(row["chart_json"], str) else row["chart_json"]
        summaries.append(ChartSummary(
            id=row["id"],
            name=row.get("name"),
            lagna_sign=cj["lagna_sign"],
            created_at=str(row["created_at"]),
        ))
    return summaries


@app.get("/charts/{chart_id}")
def get_chart(chart_id: int) -> ChartOut:
    row = db.get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")
    return _row_to_chart_out(row, chart_id)


@app.get("/charts/{chart_id}/scores")
def get_scores(chart_id: int) -> ChartScoresOut:
    # Tier 2: check scores cache
    scores_cached = cache.get(cache.TIER_SCORES, cache.make_scores_key(chart_id))
    if scores_cached is not None:
        return ChartScoresOut(chart_id=chart_id, **scores_cached)

    row = db.get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    cj = json.loads(row["chart_json"]) if isinstance(row["chart_json"], str) else row["chart_json"]
    chart = _reconstruct_chart(cj)
    scores = score_chart(chart)
    scores_dict = _scores_to_dict(scores)

    # Prime cache
    cache.set(cache.TIER_SCORES, cache.make_scores_key(chart_id), scores_dict)

    return ChartScoresOut(chart_id=chart_id, **scores_dict)


# ── chart reconstruction helper ───────────────────────────────────────────────

def _reconstruct_chart(cj: dict):
    """Rebuild a minimal BirthChart-like namespace from a stored JSON dict."""
    from src.ephemeris import BirthChart, PlanetPosition

    planets = {
        name: PlanetPosition(
            name=name,
            longitude=p["longitude"],
            sign=p["sign"],
            sign_index=p["sign_index"],
            degree_in_sign=p["degree_in_sign"],
            is_retrograde=p["is_retrograde"],
            speed=p["speed"],
        )
        for name, p in cj["planets"].items()
    }
    return BirthChart(
        jd_ut=cj["jd_ut"],
        ayanamsha_name=cj["ayanamsha_name"],
        ayanamsha_value=cj["ayanamsha_value"],
        lagna=cj["lagna"],
        lagna_sign=cj["lagna_sign"],
        lagna_sign_index=cj["lagna_sign_index"],
        lagna_degree_in_sign=cj["lagna_degree_in_sign"],
        planets=planets,  # noqa: F841
    )
