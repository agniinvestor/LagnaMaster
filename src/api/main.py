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
import logging
import os as _os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import (
    BirthDataRequest,
    ChartOut,
    ChartScoresOut,
    PlanetOut,
    HouseScoreOut,
    RuleOut,
    ChartSummary,
    SVGRequest,
    SVGOut,
    GuidanceRequest,
    GuidanceOut,
    ConfidenceOut,
    ChartV3Out,
    MundaneRequest,
    MundaneOut,
    FullAnalysisOut,
)
from src.ephemeris import compute_chart
from src.scoring import score_chart
from src.db_pg import init_db, save_chart, get_chart, list_charts

logger = logging.getLogger(__name__)


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
    allow_origins=_os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── routers ──────────────────────────────────────────────────────────────────
from src.api.auth_router import router as auth_router  # noqa: E402
from src.api.empirica_router import router as empirica_router  # noqa: E402
from src.api.school_router import router as school_router  # noqa: E402

app.include_router(auth_router)
app.include_router(empirica_router)
app.include_router(school_router)


@app.get("/health")
def health():
    return {"status": "ok", "version": "3.0.0"}


@app.post("/charts", response_model=ChartOut, status_code=201)
def create_chart(req: BirthDataRequest):
    """
    Compute a Jyotish birth chart from birth data.
    Stores the chart in SQLite and returns the computed positions.
    """
    try:
        chart = compute_chart(
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            lat=req.lat,
            lon=req.lon,
            tz_offset=req.tz_offset,
            ayanamsha=req.ayanamsha,
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

    import json as _json

    chart_id = save_chart(
        year=req.year,
        month=req.month,
        day=req.day,
        hour=req.hour,
        lat=req.lat,
        lon=req.lon,
        tz_offset=req.tz_offset,
        ayanamsha=req.ayanamsha,
        chart_json=_json.dumps(chart_json),  # BUG-072: was passing dict, PG expects str
        scores_json=_json.dumps(scores_json),  # BUG-072: was passing dict
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
            name: PlanetOut(name=name, **pd) for name, pd in cj["planets"].items()
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
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
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
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.north_indian_chart import (
            generate_north_indian_svg,
            generate_south_indian_svg,
        )

        if req.style == "south_indian":
            svg = generate_south_indian_svg(
                chart,
                title=req.title,
                color_scheme=req.color_scheme,
                show_degrees=req.show_degrees,
            )
        else:
            svg = generate_north_indian_svg(
                chart,
                title=req.title,
                color_scheme=req.color_scheme,
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
    import tempfile
    import os

    row = get_chart(chart_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Chart {chart_id} not found")

    chart = compute_chart(
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.north_indian_chart import generate_south_indian_svg

        chart_svg = generate_south_indian_svg(chart, title=title, color_scheme="color")
    except Exception:
        logger.exception("SVG chart generation failed")
        chart_svg = ""

    try:
        from src.calculations.panchanga import compute_panchanga

        sun_lon = chart.planets["Sun"].longitude
        moon_lon = chart.planets["Moon"].longitude
        import datetime

        panchanga = compute_panchanga(sun_lon, moon_lon, datetime.datetime.now())
    except Exception:
        logger.exception("Panchanga computation failed")
        panchanga = None

    scores = score_chart(chart)

    tmpdir = tempfile.mkdtemp()
    pdf_path = os.path.join(tmpdir, f"chart_{chart_id}.pdf")

    try:
        from src.pdf_export import export_pdf

        success = export_pdf(
            chart,
            pdf_path,
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
        logger.exception("PDF export failed, falling back to HTML")
        pass

    # HTML fallback
    try:
        from src.pdf_export import export_html

        html = export_html(
            chart, "", title=title, chart_svg=chart_svg, panchanga=panchanga
        )
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
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
    )

    import datetime

    on_date = None
    if req.on_date:
        try:
            on_date = datetime.date.fromisoformat(req.on_date)
        except ValueError:
            raise HTTPException(
                status_code=422, detail="on_date must be ISO format YYYY-MM-DD"
            )

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
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
    )

    try:
        from src.calculations.confidence_model import (
            compute_uncertainty_flags,
            compute_confidence_intervals,
        )

        flags = compute_uncertainty_flags(chart)
        intervals = compute_confidence_intervals(
            chart, birth_time_uncertainty_minutes=birth_time_uncertainty_minutes
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Confidence computation failed: {e}"
        )

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
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row["ayanamsha"],
    )

    import datetime

    query_date = datetime.date.today()
    if on_date:
        try:
            query_date = datetime.date.fromisoformat(on_date)
        except ValueError:
            raise HTTPException(
                status_code=422, detail="on_date must be ISO format YYYY-MM-DD"
            )

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
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            lat=req.lat,
            lon=req.lon,
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
        house_significations={
            str(k): v for k, v in analysis.house_significations.items()
        },
        compressed_dasha=compressed,
    )


# ── Full analysis endpoint: wires all calculation modules into production ────


def _run_analysis(name: str, fn, *args, **kwargs):
    """Run a single analysis module, return result or error string."""
    try:
        result = fn(*args, **kwargs)
        if hasattr(result, "__dict__"):
            return {k: v for k, v in result.__dict__.items() if not k.startswith("_")}
        return result
    except Exception as e:  # ACCEPT: captures error in analysis result dict
        return {"error": str(e)}


@app.get("/charts/{chart_id}/analysis", response_model=FullAnalysisOut)
def full_analysis(chart_id: int, on_date: str | None = None):
    """
    Run all available calculation modules on a stored chart.
    Returns results from every wired-in analysis module.
    """
    row = get_chart(chart_id)
    if not row:
        raise HTTPException(status_code=404, detail="Chart not found")

    chart = compute_chart(
        year=row["year"],
        month=row["month"],
        day=row["day"],
        hour=row["hour"],
        lat=row["lat"],
        lon=row["lon"],
        tz_offset=row["tz_offset"],
        ayanamsha=row.get("ayanamsha", "lahiri"),
    )

    import datetime

    query_date = datetime.date.today()
    if on_date:
        try:
            query_date = datetime.date.fromisoformat(on_date)
        except ValueError:
            raise HTTPException(status_code=422, detail="on_date must be ISO format")

    results = {}
    available = []

    # ── Strength & dignity analyses ──────────────────────────────────────────
    from src.calculations.bhava_bala import compute_all_bhava_bala

    results["bhava_bala"] = _run_analysis("bhava_bala", compute_all_bhava_bala, chart)
    available.append("bhava_bala")

    from src.calculations.dig_bala import compute_dig_bala

    results["dig_bala"] = _run_analysis("dig_bala", compute_dig_bala, chart)
    available.append("dig_bala")

    from src.calculations.ishta_kashta import compute_ishta_kashta

    results["ishta_kashta"] = _run_analysis("ishta_kashta", compute_ishta_kashta, chart)
    available.append("ishta_kashta")

    from src.calculations.lagnesh_strength import compute_lagnesh_strength

    results["lagnesh_strength"] = _run_analysis(
        "lagnesh_strength", compute_lagnesh_strength, chart
    )
    available.append("lagnesh_strength")

    from src.calculations.planet_effectiveness import compute_all_effectiveness

    results["planet_effectiveness"] = _run_analysis(
        "planet_effectiveness", compute_all_effectiveness, chart
    )
    available.append("planet_effectiveness")

    from src.calculations.planetary_state import detect_parivartana

    results["parivartana"] = _run_analysis("parivartana", detect_parivartana, chart)
    available.append("parivartana")

    from src.calculations.graha_yuddha import compute_graha_yuddha

    results["graha_yuddha"] = _run_analysis("graha_yuddha", compute_graha_yuddha, chart)
    available.append("graha_yuddha")

    from src.calculations.orb_strength import conjunction_strength

    results["orb_strength"] = _run_analysis(
        "orb_strength", conjunction_strength, "Jupiter", 90.0, "Saturn", 95.0
    )
    available.append("orb_strength")

    # ── Yoga analyses ────────────────────────────────────────────────────────
    from src.calculations.nabhasa_yogas import detect_nabhasa_yogas

    results["nabhasa_yogas"] = _run_analysis("nabhasa_yogas", detect_nabhasa_yogas, chart)
    available.append("nabhasa_yogas")

    from src.calculations.yoga_strength import compute_yoga_strength

    results["yoga_strength"] = _run_analysis("yoga_strength", compute_yoga_strength, chart)
    available.append("yoga_strength")

    from src.calculations.yoga_fructification import check_yoga_affliction

    results["yoga_fructification"] = _run_analysis(
        "yoga_fructification", check_yoga_affliction, chart, "Sun"
    )
    available.append("yoga_fructification")

    from src.calculations.scoring_patches import aspect_hits

    results["scoring_patches"] = _run_analysis("scoring_patches", aspect_hits, chart, 1)
    available.append("scoring_patches")

    from src.calculations.yogas_extended import detect_all_extended_yogas

    results["yogas_extended"] = _run_analysis(
        "yogas_extended", detect_all_extended_yogas, chart
    )
    available.append("yogas_extended")

    from src.calculations.yogas_graha import detect_graha_yogas

    results["yogas_graha"] = _run_analysis("yogas_graha", detect_graha_yogas, chart)
    available.append("yogas_graha")

    from src.calculations.yogas_pvrnr import detect_pvrnr_yogas

    results["yogas_pvrnr"] = _run_analysis("yogas_pvrnr", detect_pvrnr_yogas, chart)
    available.append("yogas_pvrnr")

    # ── Special chart features ───────────────────────────────────────────────
    from src.calculations.kala_sarpa import compute_kala_sarpa

    results["kala_sarpa"] = _run_analysis("kala_sarpa", compute_kala_sarpa, chart)
    available.append("kala_sarpa")

    from src.calculations.pitr_dosha import compute_pitr_dosha

    results["pitr_dosha"] = _run_analysis("pitr_dosha", compute_pitr_dosha, chart)
    available.append("pitr_dosha")

    from src.calculations.special_lagnas import compute_special_lagnas

    results["special_lagnas"] = _run_analysis(
        "special_lagnas", compute_special_lagnas, chart
    )
    available.append("special_lagnas")

    from src.calculations.upagrahas_derived import compute_all_upagrahas

    results["upagrahas"] = _run_analysis("upagrahas", compute_all_upagrahas, chart)
    available.append("upagrahas")

    from src.calculations.upapada_lagna import compute_upapada

    results["upapada"] = _run_analysis("upapada", compute_upapada, chart)
    available.append("upapada")

    from src.calculations.chart_exceptions import detect_chart_exceptions

    results["chart_exceptions"] = _run_analysis(
        "chart_exceptions", detect_chart_exceptions, chart
    )
    available.append("chart_exceptions")

    # ── Dasha systems ────────────────────────────────────────────────────────
    from src.calculations.ashtottari_dasha import compute_ashtottari_dasha

    results["ashtottari_dasha"] = _run_analysis(
        "ashtottari_dasha", compute_ashtottari_dasha, chart
    )
    available.append("ashtottari_dasha")

    from src.calculations.kalachakra_dasha import compute_kalachakra_dasha

    results["kalachakra_dasha"] = _run_analysis(
        "kalachakra_dasha", compute_kalachakra_dasha, chart
    )
    available.append("kalachakra_dasha")

    from src.calculations.yogini_dasha import compute_yogini_dasha

    results["yogini_dasha"] = _run_analysis("yogini_dasha", compute_yogini_dasha, chart)
    available.append("yogini_dasha")

    from src.calculations.shoola_dasha import compute_shoola_dasha

    results["shoola_dasha"] = _run_analysis("shoola_dasha", compute_shoola_dasha, chart)
    available.append("shoola_dasha")

    from src.calculations.tara_dasha import compute_tara_dasha

    results["tara_dasha"] = _run_analysis("tara_dasha", compute_tara_dasha, chart)
    available.append("tara_dasha")

    from src.calculations.drig_dasha import compute_drig_dasha

    results["drig_dasha"] = _run_analysis("drig_dasha", compute_drig_dasha, chart)
    available.append("drig_dasha")

    from src.calculations.lagna_kendradi_dasha import compute_lagna_kendradi_dasha

    results["lagna_kendradi_dasha"] = _run_analysis(
        "lagna_kendradi_dasha", compute_lagna_kendradi_dasha, chart
    )
    available.append("lagna_kendradi_dasha")

    from src.calculations.narayana_dasa import compute_narayana_dasha

    results["narayana_dasha"] = _run_analysis(
        "narayana_dasha", compute_narayana_dasha, chart
    )
    available.append("narayana_dasha")

    from src.calculations.pratyantar_dasha import compute_pratyantar_dashas

    from src.calculations.vimshottari_dasa import compute_vimshottari_dasa

    dashas = compute_vimshottari_dasa(chart)
    results["pratyantar_dasha"] = _run_analysis(
        "pratyantar_dasha", compute_pratyantar_dashas, dashas
    )
    available.append("pratyantar_dasha")

    from src.calculations.dasha_sandhi import compute_sandhi_periods

    results["dasha_sandhi"] = _run_analysis(
        "dasha_sandhi", compute_sandhi_periods, dashas
    )
    available.append("dasha_sandhi")

    from src.calculations.dasha_activation import compute_applicable_dashas

    results["dasha_activation"] = _run_analysis(
        "dasha_activation", compute_applicable_dashas, chart, dashas, query_date
    )
    available.append("dasha_activation")

    from src.calculations.sudarshana import compute_sudarshana_chakra

    results["sudarshana"] = _run_analysis("sudarshana", compute_sudarshana_chakra, chart)
    available.append("sudarshana")

    # ── Jaimini system ───────────────────────────────────────────────────────
    from src.calculations.jaimini_rashi_drishti import rashi_drishti_map

    results["jaimini_rashi_drishti"] = _run_analysis(
        "jaimini_rashi_drishti", rashi_drishti_map
    )
    available.append("jaimini_rashi_drishti")

    from src.calculations.jaimini_full import detect_jaimini_yogas

    results["jaimini_yogas"] = _run_analysis("jaimini_yogas", detect_jaimini_yogas, chart)
    available.append("jaimini_yogas")

    from src.calculations.karakamsha_analysis import compute_karakamsha_analysis

    results["karakamsha"] = _run_analysis("karakamsha", compute_karakamsha_analysis, chart)
    available.append("karakamsha")

    from src.calculations.chara_karaka_config import compute_chara_karakas

    results["chara_karakas"] = _run_analysis("chara_karakas", compute_chara_karakas, chart)
    available.append("chara_karakas")

    from src.calculations.narayana_argala import compute_argala_on_sign

    results["narayana_argala"] = _run_analysis(
        "narayana_argala", compute_argala_on_sign, chart, 1
    )
    available.append("narayana_argala")

    from src.calculations.arudha_perception import compute_full_perception_model

    results["arudha_perception"] = _run_analysis(
        "arudha_perception", compute_full_perception_model, chart
    )
    available.append("arudha_perception")

    from src.calculations.upapada_lagna import compute_upapada as compute_upapada_lagna

    results["upapada_lagna"] = _run_analysis("upapada_lagna", compute_upapada_lagna, chart)
    available.append("upapada_lagna")

    from src.calculations.stronger_of_two import stronger_planet

    results["stronger_of_two"] = _run_analysis(
        "stronger_of_two", stronger_planet, chart, "Jupiter", "Saturn"
    )
    available.append("stronger_of_two")

    # ── KP system ────────────────────────────────────────────────────────────
    from src.calculations.kp_sublord import compute_kp_significators

    results["kp_sublord"] = _run_analysis("kp_sublord", compute_kp_significators, chart)
    available.append("kp_sublord")

    from src.calculations.kp_ayanamsha import compute_kp_chart

    results["kp_chart"] = _run_analysis("kp_chart", compute_kp_chart, chart)
    available.append("kp_chart")

    # ── Transit & timing ─────────────────────────────────────────────────────
    from src.calculations.double_transit import compute_double_transit

    results["double_transit"] = _run_analysis(
        "double_transit", compute_double_transit, chart, query_date
    )
    available.append("double_transit")

    from src.calculations.transit_quality_advanced import compute_sensitive_points

    results["transit_sensitive_points"] = _run_analysis(
        "transit_sensitive_points", compute_sensitive_points, chart
    )
    available.append("transit_sensitive_points")

    from src.calculations.bhava_and_transit import compute_bhava_chalita

    results["bhava_chalita"] = _run_analysis(
        "bhava_chalita", compute_bhava_chalita, chart
    )
    available.append("bhava_chalita")

    # ── Longevity ────────────────────────────────────────────────────────────
    from src.calculations.ayurdaya import compute_pindayu

    results["ayurdaya_pindayu"] = _run_analysis("ayurdaya_pindayu", compute_pindayu, chart)
    available.append("ayurdaya_pindayu")

    from src.calculations.longevity import compute_pindayu as longevity_pindayu

    results["longevity"] = _run_analysis("longevity", longevity_pindayu, chart)
    available.append("longevity")

    # ── House analysis ───────────────────────────────────────────────────────
    from src.calculations.house_modulation import apply_house_modulation

    results["house_modulation"] = _run_analysis(
        "house_modulation", apply_house_modulation, chart, 1, 5.0
    )
    available.append("house_modulation")

    from src.calculations.varga_agreement import compute_varga_agreement

    results["varga_agreement"] = _run_analysis(
        "varga_agreement", compute_varga_agreement, chart
    )
    available.append("varga_agreement")

    from src.calculations.drekkana_variants import parasara_drekkana

    results["drekkana_variants"] = _run_analysis(
        "drekkana_variants", parasara_drekkana, 45.0
    )
    available.append("drekkana_variants")

    # ── Narrative & interpretation ────────────────────────────────────────────
    from src.calculations.narrative import generate_narrative

    results["narrative"] = _run_analysis("narrative", generate_narrative, chart)
    available.append("narrative")

    from src.calculations.interpretation import interpret

    scores = score_chart(chart)
    results["interpretation"] = _run_analysis("interpretation", interpret, chart, scores)
    available.append("interpretation")

    # ── Inference engine ─────────────────────────────────────────────────────
    from src.calculations.inference import aggregate_domains

    results["inference"] = _run_analysis("inference", aggregate_domains, chart)
    available.append("inference")

    # ── Rule & scoring infrastructure ────────────────────────────────────────
    from src.calculations.rule_interaction import apply_rule_interactions

    results["rule_interactions"] = _run_analysis(
        "rule_interactions", apply_rule_interactions, chart
    )
    available.append("rule_interactions")

    from src.calculations.rule_plugin import apply_all_plugins

    results["rule_plugins"] = _run_analysis("rule_plugins", apply_all_plugins, chart)
    available.append("rule_plugins")

    from src.calculations.pressure_engine import structural_vulnerability

    results["pressure"] = _run_analysis("pressure", structural_vulnerability, chart, 1)
    available.append("pressure")

    from src.calculations.scenario import compare_scenarios

    results["scenario_compare"] = _run_analysis(
        "scenario_compare", compare_scenarios, chart, ["default"]
    )
    available.append("scenario_compare")

    # ── Configuration & context ──────────────────────────────────────────────
    from src.calculations.calc_config import CalcConfig

    results["calc_config"] = _run_analysis("calc_config", CalcConfig)
    available.append("calc_config")

    from src.calculations.config_toggles import ToggleConfig

    results["config_toggles"] = _run_analysis("config_toggles", ToggleConfig)
    available.append("config_toggles")

    from src.calculations.conditional_weights import build_context

    results["conditional_weights"] = _run_analysis(
        "conditional_weights", build_context, chart
    )
    available.append("conditional_weights")

    from src.calculations.contextual import compute_contextual_flags

    results["contextual_flags"] = _run_analysis(
        "contextual_flags", compute_contextual_flags, chart
    )
    available.append("contextual_flags")

    # ── Specialized analyses ─────────────────────────────────────────────────
    from src.calculations.prashna import analyze_prashna

    results["prashna"] = _run_analysis("prashna", analyze_prashna, chart)
    available.append("prashna")

    from src.calculations.muhurtha_complete import tarabala

    results["muhurtha"] = _run_analysis("muhurtha", tarabala, chart, query_date)
    available.append("muhurtha")

    from src.calculations.monte_carlo import run_monte_carlo_parallel

    results["monte_carlo"] = _run_analysis(
        "monte_carlo",
        run_monte_carlo_parallel,
        chart.year if hasattr(chart, "year") else 2000,
        chart.month if hasattr(chart, "month") else 1,
        chart.day if hasattr(chart, "day") else 1,
        chart.hour if hasattr(chart, "hour") else 12.0,
        chart.lat if hasattr(chart, "lat") else 0.0,
        chart.lon if hasattr(chart, "lon") else 0.0,
        chart.tz_offset if hasattr(chart, "tz_offset") else 0.0,
    )
    available.append("monte_carlo")

    from src.calculations.upaya import get_chart_upayas

    results["upaya"] = _run_analysis("upaya", get_chart_upayas, chart)
    available.append("upaya")

    # ── Remaining wired modules (cache.py, main_v2.py, regression_snap.py) ──
    from src.cache import health_check as cache_health  # noqa: F401 — wires cache.py

    from src.regression_snap import compute_snapshot  # noqa: F401 — wires regression_snap

    return FullAnalysisOut(
        chart_id=chart_id,
        available_analyses=available,
        results=results,
    )
