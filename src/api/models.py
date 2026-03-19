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
