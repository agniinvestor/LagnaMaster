"""
src/api/models.py
==================
Pydantic request/response models for the LagnaMaster API.
"""

from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class BirthDataRequest(BaseModel):
    """POST /charts — birth data input."""
    year:      int   = Field(..., ge=1800, le=2100, description="Birth year")
    month:     int   = Field(..., ge=1, le=12)
    day:       int   = Field(..., ge=1, le=31)
    hour:      float = Field(..., ge=0.0, lt=24.0, description="Local time as decimal hours (0.0=midnight)")
    lat:       float = Field(..., ge=-90.0, le=90.0, description="Latitude (N positive)")
    lon:       float = Field(..., ge=-180.0, le=180.0, description="Longitude (E positive)")
    tz_offset: float = Field(5.5, description="UTC offset in hours (IST=5.5)")
    ayanamsha: str   = Field("lahiri", description="Ayanamsha system")
    name:      Optional[str] = Field(None, description="Optional name/label for the chart")

    @field_validator("ayanamsha")
    @classmethod
    def validate_ayanamsha(cls, v: str) -> str:
        supported = {"lahiri", "raman", "krishnamurti"}
        if v.lower() not in supported:
            raise ValueError(f"Unsupported ayanamsha '{v}'. Choose from {supported}")
        return v.lower()


class PlanetOut(BaseModel):
    name: str
    sign: str
    sign_index: int
    degree_in_sign: float
    longitude: float
    is_retrograde: bool
    speed: float


class ChartOut(BaseModel):
    """Full chart response."""
    id: int
    lagna_sign: str
    lagna_sign_index: int
    lagna_degree: float
    ayanamsha_name: str
    ayanamsha_value: float
    jd_ut: float
    planets: dict[str, PlanetOut]


class RuleOut(BaseModel):
    rule: str
    description: str
    score: float
    is_wc: bool


class HouseScoreOut(BaseModel):
    house: int
    domain: str
    bhavesh: str
    bhavesh_house: int
    final_score: float
    raw_score: float
    rating: str
    rules: list[RuleOut]


class ChartScoresOut(BaseModel):
    chart_id: int
    lagna_sign: str
    houses: dict[int, HouseScoreOut]


class ChartSummary(BaseModel):
    id: int
    created_at: str
    name: Optional[str]
    year: int
    month: int
    day: int
    hour: float
    lat: float
    lon: float

# ── S188: XIX Output models ──────────────────────────────────────────────────


# ── S189: Mundane models ─────────────────────────────────────────────────────

class MundaneRequest(BaseModel):
    """POST /mundane/analyze — mundane chart analysis."""
    year:       int   = Field(..., ge=1800, le=2100)
    month:      int   = Field(..., ge=1, le=12)
    day:        int   = Field(..., ge=1, le=31)
    hour:       float = Field(0.0, ge=0.0, lt=24.0)
    lat:        float = Field(..., ge=-90.0, le=90.0)
    lon:        float = Field(..., ge=-180.0, le=180.0)
    tz_offset:  float = Field(0.0)
    chart_type: str   = Field("ingress", description="'nation'|'ingress'|'lunar_new_year'|'swearing_in'")
    event_description: Optional[str] = Field(None)
    location:   Optional[str] = Field(None)


class MundaneOut(BaseModel):
    chart_type: str
    event_description: str
    date: str
    location: Optional[str]
    key_themes: list[str]
    challenges: list[str]
    house_significations: dict
    compressed_dasha: Optional[list] = None


class SVGRequest(BaseModel):
    """Request body for SVG chart generation."""
    style: str = Field("north_indian", description="'north_indian' or 'south_indian'")
    color_scheme: str = Field("color", description="'color' or 'bw'")
    show_degrees: bool = Field(False)
    title: Optional[str] = Field(None)


class SVGOut(BaseModel):
    chart_id: int
    style: str
    svg: str


class GuidanceRequest(BaseModel):
    """Request body for consumer guidance."""
    domain: str = Field("default", description="e.g. 'career','relationships','health','finance'")
    depth: str = Field("L1", description="'L1' | 'L2' | 'L3'")
    on_date: Optional[str] = Field(None, description="ISO date YYYY-MM-DD; defaults to today")
    school: str = Field("parashari")
    l3_opted_in: bool = Field(False)


class GuidanceOut(BaseModel):
    chart_id: int
    domain: str
    heading: str
    summary: str
    signal_bars: int
    signal_display: str
    timing_label: str
    confidence_label: str
    confidence_note: str
    disclaimer: str
    factors: list[str] = []
    timing_note: str = ""
    domain_context: str = ""
    technical_detail: dict = {}
    depth_returned: str = "L1"


class ConfidenceOut(BaseModel):
    chart_id: int
    lagna_boundary_margin_deg: float
    lagna_boundary_warning: bool
    moon_nakshatra_boundary: bool
    overall_reliability: str
    uncertainty_sources: list[str]
    house_confidence: dict  # house -> {"label": str, "interval": float}


class ChartV3Out(BaseModel):
    """Full v3 scoring response with dasha-sensitized D1 scores."""
    chart_id: int
    lagna_sign: str
    engine_version: str
    d1_scores: dict
    cl_scores: dict
    sl_scores: dict
    d9_scores: dict
    d10_scores: dict
    raja_yogas: list = []
    viparita_yogas: list = []
    neecha_bhanga: list = []

