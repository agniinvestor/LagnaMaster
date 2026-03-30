"""tests/test_diverse_rule_firing.py — Rule firing across 12 diverse charts.

Replaces India 1947 monoculture with one chart per lagna.
Every chart must fire rules, produce valid features, and show multi-source firing.
"""
from __future__ import annotations

import pytest
from src.ephemeris import compute_chart
from src.calculations.rule_firing import evaluate_chart


# One chart per lagna — diverse dates, locations, trust levels
DIVERSE_CHARTS = [
    {"name": "C-Section 14674",  "year": 1976, "month": 11, "day": 14, "hour": 15.75,      "lat": 37.77,  "lon": -122.42, "tz": -8.0,  "lagna": "Aries"},
    {"name": "India 1947",       "year": 1947, "month": 8,  "day": 15, "hour": 0.0,        "lat": 28.61,  "lon": 77.21,   "tz": 5.5,   "lagna": "Taurus"},
    {"name": "C-Section 15217",  "year": 1989, "month": 3,  "day": 16, "hour": 11.13,      "lat": 40.71,  "lon": -74.01,  "tz": -5.0,  "lagna": "Gemini"},
    {"name": "Sri Aurobindo",    "year": 1872, "month": 8,  "day": 15, "hour": 5.0,        "lat": 22.57,  "lon": 88.36,   "tz": 5.53,  "lagna": "Cancer"},
    {"name": "C-Section 15224",  "year": 1989, "month": 4,  "day": 10, "hour": 14.87,      "lat": 34.05,  "lon": -118.24, "tz": -8.0,  "lagna": "Leo"},
    {"name": "John F. Kennedy",  "year": 1917, "month": 5,  "day": 29, "hour": 15.0,       "lat": 42.21,  "lon": -71.0,   "tz": -5.0,  "lagna": "Virgo"},
    {"name": "C-Section 14754",  "year": 1979, "month": 4,  "day": 5,  "hour": 20.92,      "lat": 48.86,  "lon": 2.35,    "tz": 1.0,   "lagna": "Libra"},
    {"name": "C-Section 14768",  "year": 1979, "month": 8,  "day": 13, "hour": 14.47,      "lat": 30.40,  "lon": -86.62,  "tz": -6.0,  "lagna": "Scorpio"},
    {"name": "Niels Bohr",       "year": 1885, "month": 10, "day": 7,  "hour": 14.0,       "lat": 55.68,  "lon": 12.57,   "tz": 1.0,   "lagna": "Sagittarius"},
    {"name": "David Bowie",      "year": 1947, "month": 1,  "day": 8,  "hour": 9.0,        "lat": 51.45,  "lon": 0.0,     "tz": 0.0,   "lagna": "Capricorn"},
    {"name": "C-Section 15247",  "year": 1989, "month": 7,  "day": 7,  "hour": 22.47,      "lat": 37.97,  "lon": 23.72,   "tz": 1.5,   "lagna": "Aquarius"},
    {"name": "Otto von Bismarck","year": 1815, "month": 4,  "day": 1,  "hour": 5.5,        "lat": 52.59,  "lon": 12.04,   "tz": 0.8,   "lagna": "Pisces"},
]


def _compute(chart_data):
    return compute_chart(
        year=chart_data["year"], month=chart_data["month"], day=chart_data["day"],
        hour=chart_data["hour"], lat=chart_data["lat"], lon=chart_data["lon"],
        tz_offset=chart_data["tz"],
    )


@pytest.mark.parametrize("chart_data", DIVERSE_CHARTS, ids=[c["name"] for c in DIVERSE_CHARTS])
def test_rules_fire_for_every_lagna(chart_data):
    """Every lagna must have at least 50 rules fire."""
    chart = _compute(chart_data)
    result = evaluate_chart(chart)
    assert result.total_fired >= 50, (
        f"{chart_data['name']} ({chart_data['lagna']}): only {result.total_fired} rules fired"
    )


@pytest.mark.parametrize("chart_data", DIVERSE_CHARTS, ids=[c["name"] for c in DIVERSE_CHARTS])
def test_feature_vector_valid(chart_data):
    """Feature vector must have 89 features, all numeric."""
    chart = _compute(chart_data)
    result = evaluate_chart(chart)
    fv = result.feature_vector()
    assert len(fv) == 89
    for k, v in fv.items():
        assert isinstance(v, (int, float)), f"{k} = {v} (type {type(v)})"


@pytest.mark.parametrize("chart_data", DIVERSE_CHARTS, ids=[c["name"] for c in DIVERSE_CHARTS])
def test_multiple_houses_fire(chart_data):
    """Rules should fire across multiple houses, not concentrated in one."""
    chart = _compute(chart_data)
    result = evaluate_chart(chart)
    active_houses = sum(1 for h in range(1, 13) if result.house_summary.get(h, None)
                        and result.house_summary[h].total_fired > 0)
    assert active_houses >= 3, (
        f"{chart_data['name']}: only {active_houses} houses have fired rules"
    )


def test_all_12_lagnas_represented():
    """Verify the diverse chart set covers all 12 lagnas."""
    lagnas = set()
    for cd in DIVERSE_CHARTS:
        chart = _compute(cd)
        lagnas.add(chart.lagna_sign)
    assert len(lagnas) == 12, f"Missing lagnas: {set(['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']) - lagnas}"
