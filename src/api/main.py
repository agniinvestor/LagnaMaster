"""
src/api/main.py
================
FastAPI application for LagnaMaster birth chart API.

Endpoints:
  POST /charts              — compute + store a birth chart
  GET  /charts              — list recent charts
  GET  /charts/{id}         — retrieve a stored chart
  GET  /charts/{id}/scores  — get house scores for a chart
  GET  /health              — health check
"""

from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import (
    BirthDataRequest, ChartOut, ChartScoresOut,
    PlanetOut, HouseScoreOut, RuleOut, ChartSummary,
)
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.db import init_db, save_chart, get_chart, list_charts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="LagnaMaster API",
    description="Vedic Jyotish birth chart calculation and scoring",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}


@app.post("/charts", response_model=ChartOut, status_code=201)
def create_chart(req: BirthDataRequest):
    """
    Compute a Jyotish birth chart from birth data.
    Stores the chart in SQLite and returns the computed positions.
    """
    try:
        chart = compute_chart(
            year=req.year, month=req.month, day=req.day,
            hour=req.hour, lat=req.lat, lon=req.lon,
            tz_offset=req.tz_offset, ayanamsha=req.ayanamsha,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Compute scores
    scores = score_chart(chart)

    # Serialize for storage
    chart_json = {
        "lagna_sign": chart.lagna_sign,
        "lagna_sign_index": chart.lagna_sign_index,
        "lagna_degree": chart.lagna_degree_in_sign,
        "ayanamsha_name": chart.ayanamsha_name,
        "ayanamsha_value": chart.ayanamsha_value,
        "jd_ut": chart.jd_ut,
        "planets": {
            name: {
                "sign": p.sign,
                "sign_index": p.sign_index,
                "degree_in_sign": p.degree_in_sign,
                "longitude": p.longitude,
                "is_retrograde": p.is_retrograde,
                "speed": p.speed,
            }
            for name, p in chart.planets.items()
        },
    }

    scores_json = {
        str(h): {
            "domain": hs.domain,
            "final_score": hs.final_score,
            "raw_score": hs.raw_score,
            "rating": hs.rating,
            "bhavesh": hs.bhavesh,
            "bhavesh_house": hs.bhavesh_house,
        }
        for h, hs in scores.houses.items()
    }

    chart_id = save_chart(
        year=req.year, month=req.month, day=req.day,
        hour=req.hour, lat=req.lat, lon=req.lon,
        tz_offset=req.tz_offset, ayanamsha=req.ayanamsha,
        chart_json=chart_json,
        scores_json=scores_json,
        name=req.name,
    )

    return ChartOut(
        id=chart_id,
        lagna_sign=chart.lagna_sign,
        lagna_sign_index=chart.lagna_sign_index,
        lagna_degree=chart.lagna_degree_in_sign,
        ayanamsha_name=chart.ayanamsha_name,
        ayanamsha_value=chart.ayanamsha_value,
        jd_ut=chart.jd_ut,
        planets={
            name: PlanetOut(
                name=name,
                sign=p.sign,
                sign_index=p.sign_index,
                degree_in_sign=p.degree_in_sign,
                longitude=p.longitude,
                is_retrograde=p.is_retrograde,
                speed=p.speed,
            )
            for name, p in chart.planets.items()
        },
    )


@app.get("/charts", response_model=list[ChartSummary])
def list_charts_endpoint(limit: int = 20):
    """List the most recent charts."""
    return [ChartSummary(**row) for row in list_charts(limit=limit)]


@app.get("/charts/{chart_id}", response_model=ChartOut)
def get_chart_endpoint(chart_id: int):
    """Retrieve a previously computed chart."""
    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")
    cj = row["chart_json"]
    return ChartOut(
        id=chart_id,
        lagna_sign=cj["lagna_sign"],
        lagna_sign_index=cj["lagna_sign_index"],
        lagna_degree=cj["lagna_degree"],
        ayanamsha_name=cj["ayanamsha_name"],
        ayanamsha_value=cj["ayanamsha_value"],
        jd_ut=cj["jd_ut"],
        planets={
            name: PlanetOut(name=name, **pd)
            for name, pd in cj["planets"].items()
        },
    )


@app.get("/charts/{chart_id}/scores", response_model=ChartScoresOut)
def get_scores_endpoint(chart_id: int):
    """
    Get full 22-rule house scores for a chart.
    Recomputes from stored birth data (scores are always fresh).
    """
    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )
    scores = score_chart(chart)

    return ChartScoresOut(
        chart_id=chart_id,
        lagna_sign=scores.lagna_sign,
        houses={
            h: HouseScoreOut(
                house=h,
                domain=hs.domain,
                bhavesh=hs.bhavesh,
                bhavesh_house=hs.bhavesh_house,
                final_score=hs.final_score,
                raw_score=hs.raw_score,
                rating=hs.rating,
                rules=[
                    RuleOut(
                        rule=r.rule,
                        description=r.description,
                        score=r.score,
                        is_wc=r.is_wc,
                    )
                    for r in hs.rules
                ],
            )
            for h, hs in scores.houses.items()
        },
    )
