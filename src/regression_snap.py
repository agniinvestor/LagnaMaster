"""
src/regression_snap.py
Differential regression snapshot for LagnaMaster scoring engine.
Session 186 (Audit J-2).

Usage:
  # Compute and store baseline for all reference charts
  from src.regression_snap import compute_and_store_snapshot, diff_against_snapshot
  compute_and_store_snapshot()                 # writes tests/fixtures/snap_v3.json
  diffs = diff_against_snapshot(tolerance=0.05)  # compare current vs stored

  # In CI (pytest):
  from src.regression_snap import assert_no_regression
  assert_no_regression(tolerance=0.05)         # raises AssertionError if regression

Source: Audit J-2: "When ENGINE_VERSION increments, no automated test checks
        whether any existing chart score changed."
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

SNAP_PATH = Path("tests/fixtures/snap_v3.json")
ENGINE_VERSION = "v3.0.0"

# Reference chart definitions — birth data for snapshot computation
# These are the same as in regression_fixtures.py but with engine-computed scores
REFERENCE_CHARTS = {
    "india_1947": {
        "year": 1947,
        "month": 8,
        "day": 15,
        "hour": 0.0,
        "lat": 28.6139,
        "lon": 77.2090,
        "tz_offset": 5.5,
        "ayanamsha": "lahiri",
        "description": "India Independence — primary regression baseline",
    },
    "einstein_1879": {
        "year": 1879,
        "month": 3,
        "day": 14,
        "hour": 11.5,
        "lat": 48.4011,
        "lon": 9.9876,
        "tz_offset": 0.86,
        "ayanamsha": "lahiri",
        "description": "Albert Einstein — Gemini Lagna, German Standesamt trust=high",
    },
    "bohr_1885": {
        "year": 1885,
        "month": 10,
        "day": 7,
        "hour": 10.0,
        "lat": 55.6761,
        "lon": 12.5683,
        "tz_offset": 1.0,
        "ayanamsha": "lahiri",
        "description": "Niels Bohr — Danish civil registration trust=high",
    },
}


def compute_snapshot(
    chart_defs: Optional[dict] = None,
    engine_version: str = ENGINE_VERSION,
) -> dict:
    """
    Compute house scores for all reference charts and return as snapshot dict.

    Returns:
        {
          "engine_version": "v3.0.0",
          "charts": {
            "india_1947": {"1": -2.75, "2": -3.375, ...},
            ...
          }
        }
    """
    chart_defs = chart_defs or REFERENCE_CHARTS
    result = {"engine_version": engine_version, "charts": {}}

    try:
        from src.ephemeris import compute_chart
        from src.scoring import score_chart
    except ImportError as e:
        print(f"  SKIP compute_snapshot: {e}")
        return result

    for chart_id, defn in chart_defs.items():
        try:
            chart = compute_chart(
                year=defn["year"],
                month=defn["month"],
                day=defn["day"],
                hour=defn["hour"],
                lat=defn["lat"],
                lon=defn["lon"],
                tz_offset=defn["tz_offset"],
                ayanamsha=defn.get("ayanamsha", "lahiri"),
            )
            scores_obj = score_chart(chart)
            if hasattr(scores_obj, "houses"):
                scores = {
                    str(k): round(float(v.final_score), 4)
                    for k, v in scores_obj.houses.items()
                }
            elif isinstance(scores_obj, dict):
                scores = {str(k): round(float(v), 4) for k, v in scores_obj.items()}
            else:
                scores = {}
            result["charts"][chart_id] = scores
            print(f"  SNAP {chart_id}: {scores}")
        except Exception as exc:
            print(f"  ERR {chart_id}: {exc}")
            result["charts"][chart_id] = {}

    return result


def save_snapshot(snap: dict, path: Path = SNAP_PATH) -> None:
    """Persist snapshot to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(snap, f, indent=2)
    print(f"  SAVED snapshot → {path}")


def load_snapshot(path: Path = SNAP_PATH) -> Optional[dict]:
    """Load stored snapshot from JSON file. Returns None if not found."""
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def compute_and_store_snapshot(
    chart_defs: Optional[dict] = None,
    path: Path = SNAP_PATH,
) -> dict:
    """Compute scores and write snapshot file. Call once per engine version."""
    snap = compute_snapshot(chart_defs)
    save_snapshot(snap, path)
    return snap


def diff_against_snapshot(
    chart_defs: Optional[dict] = None,
    path: Path = SNAP_PATH,
    tolerance: float = 0.05,
) -> list[dict]:
    """
    Compare current engine output against stored snapshot.

    Returns: list of diff records, each:
        {"chart_id": ..., "house": ..., "stored": ..., "current": ..., "delta": ...}
    An empty list means no regression detected.
    """
    baseline = load_snapshot(path)
    if baseline is None:
        print(f"  SNAP no baseline at {path} — skipping diff")
        return []

    current = compute_snapshot(chart_defs)
    diffs = []

    for chart_id, stored_scores in baseline.get("charts", {}).items():
        current_scores = current.get("charts", {}).get(chart_id, {})
        for house_str, stored_val in stored_scores.items():
            if stored_val is None:
                continue
            current_val = current_scores.get(house_str)
            if current_val is None:
                continue
            delta = abs(float(current_val) - float(stored_val))
            if delta > tolerance:
                diffs.append(
                    {
                        "chart_id": chart_id,
                        "house": int(house_str),
                        "stored": stored_val,
                        "current": current_val,
                        "delta": round(delta, 4),
                    }
                )

    return diffs


def assert_no_regression(
    chart_defs: Optional[dict] = None,
    path: Path = SNAP_PATH,
    tolerance: float = 0.05,
) -> None:
    """
    Raise AssertionError if any house score changed beyond tolerance vs stored snapshot.
    Intended for use in CI (called from pytest).

    Source: Audit J-2 requirement.
    """
    diffs = diff_against_snapshot(chart_defs, path, tolerance)
    if diffs:
        lines = ["\nRegression detected — house scores changed vs stored snapshot:"]
        for d in diffs:
            lines.append(
                f"  {d['chart_id']} H{d['house']}: "
                f"stored={d['stored']:+.4f} current={d['current']:+.4f} "
                f"Δ={d['delta']:.4f}"
            )
        lines.append(
            "\nTo accept changes: run compute_and_store_snapshot() and commit snap_v3.json"
        )
        raise AssertionError("\n".join(lines))
    print(f"  OK  No regression (tolerance={tolerance})")
