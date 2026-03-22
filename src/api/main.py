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
    SVGRequest, SVGOut, GuidanceRequest, GuidanceOut,
    ConfidenceOut, ChartV3Out,
    MundaneRequest, MundaneOut,
)
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.db_pg import init_db, save_chart, get_chart, list_charts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="LagnaMaster API",
    description="Vedic Jyotish birth chart calculation and scoring",
    version="3.0.0",
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


# ── S188: XIX Output endpoints ───────────────────────────────────────────────

@app.post("/charts/{chart_id}/svg", response_model=SVGOut)
def get_chart_svg(chart_id: int, req: SVGRequest = None):
    """
    Generate SVG birth chart for a stored chart.
    style: 'north_indian' (diamond) or 'south_indian' (grid)
    """
    if req is None:
        req = SVGRequest()
    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.north_indian_chart import (
            generate_north_indian_svg, generate_south_indian_svg
        )
        if req.style == "south_indian":
            svg = generate_south_indian_svg(
                chart, title=req.title, color_scheme=req.color_scheme,
                show_degrees=req.show_degrees,
            )
        else:
            svg = generate_north_indian_svg(
                chart, title=req.title, color_scheme=req.color_scheme,
                show_degrees=req.show_degrees,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SVG generation failed: {e}")

    return SVGOut(chart_id=chart_id, style=req.style, svg=svg)


@app.post("/charts/{chart_id}/pdf")
def export_chart_pdf(chart_id: int, title: str = "Birth Chart"):
    """
    Export chart as PDF (weasyprint) or HTML fallback.
    Returns the file as a downloadable response.
    """
    from fastapi.responses import FileResponse, HTMLResponse
    import tempfile, os

    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.north_indian_chart import generate_south_indian_svg
        chart_svg = generate_south_indian_svg(chart, title=title, color_scheme="color")
    except Exception:
        chart_svg = ""

    try:
        from src.calculations.panchanga import compute_panchanga
        sun_lon = chart.planets["Sun"].longitude
        moon_lon = chart.planets["Moon"].longitude
        import datetime
        panchanga = compute_panchanga(sun_lon, moon_lon, datetime.datetime.now())
    except Exception:
        panchanga = None

    scores = score_chart(chart)

    tmpdir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmpdir, f"chart_{chart_id}.pdf")

    try:
        from src.pdf_export import export_pdf
        success = export_pdf(
            chart, pdf_path,
            title=title,
            chart_svg=chart_svg,
            panchanga=panchanga,
            scores=scores,
        )
        if success and os.path.exists(pdf_path):
            return FileResponse(
                pdf_path,
                media_type="application/pdf",
                filename=f"lagnamaster_chart_{chart_id}.pdf",
            )
    except Exception:
        pass

    # HTML fallback
    try:
        from src.pdf_export import export_html
        html = export_html(chart, "", title=title, chart_svg=chart_svg, panchanga=panchanga)
        return HTMLResponse(content=html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {e}")


@app.post("/charts/{chart_id}/guidance", response_model=GuidanceOut)
def get_guidance_endpoint(chart_id: int, req: GuidanceRequest = None):
    """
    Consumer-facing guidance for a domain.
    Returns L1 (default), L2, or L3 depth response.
    Raw scores are never exposed at L1/L2.
    """
    if req is None:
        req = GuidanceRequest()

    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )

    import datetime
    on_date = None
    if req.on_date:
        try:
            on_date = datetime.date.fromisoformat(req.on_date)
        except ValueError:
            raise HTTPException(status_code=422, detail="on_date must be ISO format YYYY-MM-DD")

    try:
        from src.guidance.guidance_api import get_guidance
        resp = get_guidance(
            chart=chart,
            domain=req.domain,
            depth=req.depth,
            on_date=on_date,
            school=req.school,
            l3_opted_in=req.l3_opted_in,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Guidance computation failed: {e}")

    return GuidanceOut(
        chart_id=chart_id,
        domain=resp.domain,
        heading=resp.heading,
        summary=resp.summary,
        signal_bars=resp.signal_bars,
        signal_display=resp.signal_display,
        timing_label=resp.timing_label,
        confidence_label=resp.confidence_label,
        confidence_note=resp.confidence_note,
        disclaimer=resp.disclaimer,
        factors=resp.factors,
        timing_note=resp.timing_note,
        domain_context=resp.domain_context,
        technical_detail=resp.technical_detail,
        depth_returned=resp.depth_returned,
    )


@app.get("/charts/{chart_id}/confidence", response_model=ConfidenceOut)
def get_confidence_endpoint(chart_id: int, birth_time_uncertainty_minutes: float = 5.0):
    """
    Confidence model for a chart.
    Returns lagna boundary warnings, nakshatra boundary flags,
    and per-house confidence intervals.
    """
    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.confidence_model import (
            compute_uncertainty_flags, compute_confidence_intervals
        )
        flags = compute_uncertainty_flags(chart)
        intervals = compute_confidence_intervals(
            chart, birth_time_uncertainty_minutes=birth_time_uncertainty_minutes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Confidence computation failed: {e}")

    house_conf = {}
    if hasattr(intervals, "houses"):
        for h, hc in intervals.houses.items():
            house_conf[str(h)] = {
                "label": getattr(hc, "confidence_label", "Moderate"),
                "interval": getattr(hc, "score_interval", 0.0),
            }

    return ConfidenceOut(
        chart_id=chart_id,
        lagna_boundary_margin_deg=flags.lagna_boundary_margin_deg,
        lagna_boundary_warning=flags.lagna_boundary_margin_deg < 1.0,
        moon_nakshatra_boundary=getattr(flags, "moon_nakshatra_boundary", False),
        overall_reliability=getattr(intervals, "overall_reliability", "Moderate"),
        uncertainty_sources=getattr(flags, "uncertainty_sources", []),
        house_confidence=house_conf,
    )


@app.get("/charts/{chart_id}/scores/v3", response_model=ChartV3Out)
def get_scores_v3_endpoint(
    chart_id: int,
    school: str = "parashari",
    on_date: str = None,
    strict_school: bool = False,
):
    """
    Full v3 multi-axis scores with dasha sensitization.
    Uses score_chart_v3 (dasha-aware, multi-axis, school-filtered).
    """
    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"], month=row["month"], day=row["day"],
        hour=row["hour"], lat=row["lat"], lon=row["lon"],
        tz_offset=row["tz_offset"], ayanamsha=row["ayanamsha"],
    )

    import datetime
    query_date = datetime.date.today()
    if on_date:
        try:
            query_date = datetime.date.fromisoformat(on_date)
        except ValueError:
            raise HTTPException(status_code=422, detail="on_date must be ISO format YYYY-MM-DD")

    try:
        from src.calculations.scoring_v3 import score_chart_v3
        result = score_chart_v3(chart, on_date=query_date, school=school)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"v3 scoring failed: {e}")

    return ChartV3Out(
        chart_id=chart_id,
        lagna_sign=result.lagna_sign,
        engine_version=result.engine_version,
        d1_scores={str(k): v for k, v in result.d1_scores.items()},
        cl_scores={str(k): v for k, v in result.cl_scores.items()},
        sl_scores={str(k): v for k, v in result.sl_scores.items()},
        d9_scores={str(k): v for k, v in result.d9_scores.items()},
        d10_scores={str(k): v for k, v in result.d10_scores.items()},
        raja_yogas=[str(y) for y in result.raja_yogas],
        viparita_yogas=[str(y) for y in result.viparita_yogas],
        neecha_bhanga=[str(y) for y in result.neecha_bhanga],
    )



# ── S189: Mundane astrology endpoint ─────────────────────────────────────────

@app.post("/mundane/analyze", response_model=MundaneOut)
def analyze_mundane(req: MundaneRequest):
    """
    Analyze a mundane chart (nation, solar ingress, swearing-in, lunar new year).
    Returns key themes, challenges, and compressed dasha for the period.
    Source: PVRNR Ch.35 p460-469.
    """
    import datetime

    try:
        chart = compute_chart(
            year=req.year, month=req.month, day=req.day,
            hour=req.hour, lat=req.lat, lon=req.lon,
            tz_offset=req.tz_offset,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    try:
        from src.calculations.mundane import analyze_mundane_chart, compress_vimshottari
        event_date = datetime.date(req.year, req.month, req.day)
        analysis = analyze_mundane_chart(
            chart,
            chart_type=req.chart_type,
            event_description=req.event_description,
            event_date=event_date,
            location=req.location,
        )
        compressed = compress_vimshottari(chart, event_date, period_years=1.0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mundane analysis failed: {e}")

    return MundaneOut(
        chart_type=analysis.chart_type,
        event_description=analysis.event_description,
        date=str(analysis.date),
        location=analysis.location,
        key_themes=analysis.key_themes,
        challenges=analysis.challenges,
        house_significations={str(k): v for k, v in analysis.house_significations.items()},
        compressed_dasha=compressed,
    )

