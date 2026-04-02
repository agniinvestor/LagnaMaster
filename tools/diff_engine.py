"""
Cross-validation pipeline: LagnaMaster vs PyJHora for selected charts.

For each chart:
1. Load PyJHora pre-computed values
2. Compute with LagnaMaster
3. Normalize both
4. Diff field-by-field
5. Classify disagreements (systematic vs random)
6. Check field-level non-regression
7. Write per-chart verdict files

Usage:
    .venv/bin/python tools/diff_engine.py [--charts-only CHART_ID,...]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.calculations.nakshatra import nakshatra_position  # noqa: E402
from src.ephemeris import compute_chart  # noqa: E402
from tools.classification import classify_disagreements  # noqa: E402
from tools.diff_engine_core import Verdict, diff_field  # noqa: E402
from tools.normalize_outputs import normalize_longitude, normalize_sign  # noqa: E402

MANIFEST_PATH = ROOT / "tests" / "fixtures" / "verified_360.json"
PYJHORA_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"
RESULTS_DIR = ROOT / "tests" / "fixtures" / "verified_360_results"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANET_NAMES = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
    "Saturn", "Rahu", "Ketu",
]

# Metadata keys in manifest that aren't lagna names
_META_KEYS = {
    "schema_version", "generated_date", "engine_versions",
    "selection_hash", "total_charts", "golden_50_count",
}


def _extract_lm_values(chart) -> dict:
    """Extract flat dict of values from a LagnaMaster BirthChart."""
    values = {
        "lagna_degree": chart.lagna,
        "lagna_sign": chart.lagna_sign,
    }
    for name in PLANET_NAMES:
        pos = chart.planets[name]
        values[f"longitude_{name.lower()}"] = pos.longitude
        values[f"sign_{name.lower()}"] = pos.sign
        nak = nakshatra_position(pos.longitude)
        values[f"nakshatra_{name.lower()}"] = nak.nakshatra
    return values


def _extract_pjh_values(pjh: dict) -> dict:
    """Extract flat dict of values from PyJHora computed data."""
    values = {
        "lagna_degree": pjh.get("lagna_degree", 0.0),
        "lagna_sign": pjh.get("lagna_sign", ""),
    }
    planets = pjh.get("planets", {})
    for name in PLANET_NAMES:
        pdata = planets.get(name, {})
        values[f"longitude_{name.lower()}"] = pdata.get("longitude")
        values[f"sign_{name.lower()}"] = pdata.get("sign")
    return values


def _normalize_values(values: dict) -> dict:
    """Normalize all values in a flat chart dict."""
    out = {}
    for key, val in values.items():
        if val is None:
            out[key] = None
            continue
        if "longitude" in key or key == "lagna_degree":
            try:
                out[key] = normalize_longitude(float(val))
            except (ValueError, TypeError):
                out[key] = val
        elif "sign" in key and "nakshatra" not in key:
            try:
                out[key] = normalize_sign(val)
            except (ValueError, TypeError):
                out[key] = val
        else:
            out[key] = val
    return out


def _build_schema(has_edge_flags: bool) -> dict:
    """Build the field comparison schema."""
    lon_tol = 0.2 if has_edge_flags else 0.1
    schema = {
        "lagna_degree": {"field_type": "longitude", "tolerance": lon_tol},
        "lagna_sign": {"field_type": "categorical"},
    }
    for name in PLANET_NAMES:
        n = name.lower()
        schema[f"longitude_{n}"] = {
            "field_type": "longitude", "tolerance": lon_tol,
        }
        schema[f"sign_{n}"] = {"field_type": "categorical"}
        # nakshatra comparison deferred to Phase 2 — requires PyJHora
        # nakshatra extraction (not exposed by rasi_chart output)
    return schema


def _serialize(value):
    """Make values JSON-safe."""
    if isinstance(value, float):
        return round(value, 6)
    return value


def run_pipeline(chart_ids: list[str] | None = None):
    """Run the full diff pipeline."""
    manifest = json.loads(MANIFEST_PATH.read_text())
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Collect all chart entries from manifest
    entries = []
    for key, value in manifest.items():
        if key in _META_KEYS or not isinstance(value, list):
            continue
        for entry in value:
            if chart_ids and entry["chart_id"] not in chart_ids:
                continue
            entries.append(entry)

    all_verdicts: dict[str, dict[str, Verdict]] = {}
    results: dict[str, dict] = {}

    print(f"Processing {len(entries)} charts...")
    start = time.time()

    for i, entry in enumerate(entries):
        chart_id = entry["chart_id"]
        pjh_path = PYJHORA_DIR / f"{chart_id}.json"
        if not pjh_path.exists():
            print(f"  SKIP {chart_id}: no PyJHora data")
            continue

        pjh_data = json.loads(pjh_path.read_text())
        birth_data = pjh_data["birth_data"]

        # Compute with LagnaMaster
        try:
            lm_chart = compute_chart(
                year=birth_data["year"],
                month=birth_data["month"],
                day=birth_data["day"],
                hour=birth_data["hour"],
                lat=birth_data["lat"],
                lon=birth_data["lon"],
                tz_offset=birth_data["tz_offset"],
            )
        except Exception as e:
            print(f"  FAIL {chart_id}: LM compute error: {e}")
            continue

        # Extract + normalize
        lm_values = _normalize_values(_extract_lm_values(lm_chart))
        pjh_values = _normalize_values(
            _extract_pjh_values(pjh_data.get("pyjhora", {}))
        )

        # Diff
        has_edge = entry.get("edge_case_count", 0) > 0
        schema = _build_schema(has_edge)
        verdicts = {}
        for field_name, field_def in schema.items():
            verdicts[field_name] = diff_field(
                field_name,
                lm_values.get(field_name),
                pjh_values.get(field_name),
                field_type=field_def["field_type"],
                tolerance=field_def.get("tolerance"),
            )

        all_verdicts[chart_id] = verdicts
        results[chart_id] = {
            "chart_id": chart_id,
            "birth_data": birth_data,
            "lm_values": {k: _serialize(v) for k, v in lm_values.items()},
            "pyjhora_values": {k: _serialize(v) for k, v in pjh_values.items()},
            "entry": entry,
        }

        if (i + 1) % 20 == 0:
            elapsed = time.time() - start
            print(f"  [{i+1}/{len(entries)}] {elapsed:.1f}s")

    # Classify
    print("Classifying disagreements...")
    classified = classify_disagreements(all_verdicts, segment_size=len(entries))

    # Field-level non-regression check
    regressions = []
    for chart_id, verdicts in classified.items():
        prev_path = RESULTS_DIR / f"{chart_id}.json"
        if not prev_path.exists():
            continue
        prev = json.loads(prev_path.read_text())
        for fname, v in verdicts.items():
            prev_v = prev.get("verdicts", {}).get(fname, {})
            if (prev_v.get("status") == "agreement"
                    and v.status in ("random_disagreement",
                                     "unclassified_disagreement")):
                regressions.append(f"{chart_id}:{fname}")
    if regressions:
        print(f"\n*** REGRESSION: {len(regressions)} previously-agreed fields "
              f"now disagree:")
        for r in regressions[:10]:
            print(f"  {r}")
        print("Aborting — fix regressions before re-running.")
        sys.exit(1)

    # Write per-chart result files
    for chart_id, verdicts in classified.items():
        agreement = sum(1 for v in verdicts.values() if v.status == "agreement")
        total = len(verdicts)

        result_data = results[chart_id]
        result_data["verdicts"] = {
            fname: {
                "status": v.status,
                "lm": _serialize(v.lm),
                "pjh": _serialize(v.pjh),
                "diff": v.diff,
                "field_type": v.field_type,
                "tolerance": v.tolerance,
                "normalized": v.normalized,
                "pattern_id": v.pattern_id,
                "note": v.note,
            }
            for fname, v in verdicts.items()
        }
        result_data["summary"] = {
            "total_fields": total,
            "agreement": agreement,
            "systematic": sum(1 for v in verdicts.values()
                             if v.status == "systematic_disagreement"),
            "random": sum(1 for v in verdicts.values()
                         if v.status == "random_disagreement"),
        }
        result_data["confidence_score"] = (
            round(agreement / total, 4) if total > 0 else 0.0
        )

        out_path = RESULTS_DIR / f"{chart_id}.json"
        out_path.write_text(json.dumps(result_data, indent=2, default=str))

    # Summary
    elapsed = time.time() - start
    total_agreement = sum(
        r.get("summary", {}).get("agreement", 0)
        for r in results.values()
        if "summary" in r
    )
    total_fields = sum(
        r.get("summary", {}).get("total_fields", 0)
        for r in results.values()
        if "summary" in r
    )
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Charts processed: {len(classified)}")
    if total_fields > 0:
        print(f"Agreement rate: {total_agreement}/{total_fields} "
              f"({total_agreement/total_fields:.1%})")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-validate LM vs PyJHora"
    )
    parser.add_argument("--charts-only", type=str, default="",
                        help="Comma-separated chart IDs (empty=all)")
    args = parser.parse_args()

    chart_ids = (
        [c.strip() for c in args.charts_only.split(",") if c.strip()]
        or None
    )
    run_pipeline(chart_ids)


if __name__ == "__main__":
    main()
