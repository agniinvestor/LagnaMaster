"""Shared fixtures for the diverse correctness suite."""
import json

import pytest
from pathlib import Path

from src.ephemeris import compute_chart, BirthChart

VERIFIED_DIR = Path("tests/fixtures/verified_360_results")
MANIFEST_PATH = Path("tests/fixtures/verified_360.json")

_META_KEYS = {
    "schema_version", "generated_date", "engine_versions",
    "selection_hash", "total_charts", "golden_50_count",
}


def _load_charts(subset="all"):
    manifest = json.loads(MANIFEST_PATH.read_text())
    charts = []
    for key, entries in manifest.items():
        if key in _META_KEYS or not isinstance(entries, list):
            continue
        for entry in entries:
            if subset == "golden_50" and not entry.get("golden_50"):
                continue
            result_path = VERIFIED_DIR / f"{entry['chart_id']}.json"
            if not result_path.exists():
                continue
            data = json.loads(result_path.read_text())
            charts.append(data)
    return charts


ALL_CHARTS = _load_charts("all")
GOLDEN_50 = _load_charts("golden_50")


@pytest.fixture(params=ALL_CHARTS, ids=lambda c: c["chart_id"])
def verified_chart(request):
    """A single verified chart with verdicts."""
    return request.param


@pytest.fixture(params=GOLDEN_50, ids=lambda c: c["chart_id"])
def golden_chart(request):
    """A golden-50 chart for smoke tests."""
    return request.param


@pytest.fixture
def computed_chart(verified_chart) -> BirthChart:
    """Pre-computed LagnaMaster chart for the verified fixture."""
    bd = verified_chart["birth_data"]
    return compute_chart(
        year=bd["year"], month=bd["month"], day=bd["day"],
        hour=bd["hour"], lat=bd["lat"], lon=bd["lon"],
        tz_offset=bd["tz_offset"],
    )
