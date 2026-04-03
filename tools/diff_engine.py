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

from src.calculations.dignity import compute_dignity  # noqa: E402
from src.calculations.nakshatra import nakshatra_position  # noqa: E402
from src.ephemeris import compute_chart  # noqa: E402
from tools.classification import classify_disagreements  # noqa: E402
from tools.diff_engine_core import Verdict, diff_field  # noqa: E402
from tools.normalize_outputs import normalize_longitude, normalize_sign, normalize_nakshatra  # noqa: E402

# Sign → lord mapping (standard Parashari)
_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
    6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# Nakshatra names for index-to-name conversion
_NAK_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]

# Dignity labels used by LM
# Coarse dignity: own/exalted/debilitated/other
# Finer levels (friend/enemy/mooltrikona) need relationship table
# which PyJHora doesn't expose via sign lookup — compare at this level
_DIGNITY_COARSE = {
    "Own Sign": "own",
    "Exalted": "exalted",
    "Debilitated": "debilitated",
    "Mooltrikona": "own",  # mooltrikona is a subset of own sign
    "Friendly Sign": "other",
    "Neutral Sign": "other",
    "Enemy Sign": "other",
    "Great Friend Sign": "other",
    "Great Enemy Sign": "other",
}

# PyJHora planet ID → name (SWE constants)
_PJH_PLANET_MAP = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury", 4: "Jupiter",
    5: "Venus", 6: "Saturn", 7: "Rahu", 8: "Ketu",
}

# Dignity from sign placement (simplified — matches PyJHora's approach)
_EXALTATION = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
_DEBILITATION = {"Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11, "Jupiter": 9, "Venus": 5, "Saturn": 0}
_OWN_SIGNS = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
}

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

    # Phase 1: positions + nakshatras
    for name in PLANET_NAMES:
        pos = chart.planets[name]
        n = name.lower()
        values[f"longitude_{n}"] = pos.longitude
        values[f"sign_{n}"] = pos.sign
        nak = nakshatra_position(pos.longitude)
        values[f"nakshatra_{n}"] = nak.nakshatra

    # Phase 2: dignity
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        try:
            d = compute_dignity(name, chart)
            values[f"dignity_{name.lower()}"] = _DIGNITY_COARSE.get(d.dignity.value, "other")
        except Exception:
            values[f"dignity_{name.lower()}"] = None

    # Phase 2: house lords
    for h in range(1, 13):
        sign_idx = (chart.lagna_sign_index + h - 1) % 12
        values[f"house_{h}_lord"] = _SIGN_LORDS[sign_idx]

    return values


def _pjh_dignity(planet_name: str, sign_index: int) -> str:
    """Derive dignity from sign placement (matches basic Parashari rules)."""
    if planet_name in ("Rahu", "Ketu"):
        return "other"
    if sign_index == _EXALTATION.get(planet_name):
        return "exalted"
    if sign_index == _DEBILITATION.get(planet_name):
        return "debilitated"
    if sign_index in _OWN_SIGNS.get(planet_name, []):
        return "own"
    return "other"  # friend/enemy/neutral requires relationship table — compare at coarser level


def _extract_pjh_values(pjh: dict) -> dict:
    """Extract flat dict of values from PyJHora computed data."""
    values = {
        "lagna_degree": pjh.get("lagna_degree", 0.0),
        "lagna_sign": pjh.get("lagna_sign", ""),
    }

    planets = pjh.get("planets", {})
    lagna_sign_index = pjh.get("lagna_sign_index", 0)

    # Phase 1: positions
    for name in PLANET_NAMES:
        pdata = planets.get(name, {})
        n = name.lower()
        values[f"longitude_{n}"] = pdata.get("longitude")
        values[f"sign_{n}"] = pdata.get("sign")

        # Phase 1+: nakshatras (derived from longitude)
        lon = pdata.get("longitude")
        if lon is not None:
            nak_idx = int(lon / (360.0 / 27.0))
            values[f"nakshatra_{n}"] = _NAK_NAMES[nak_idx] if 0 <= nak_idx <= 26 else None
        else:
            values[f"nakshatra_{n}"] = None

    # Phase 2: dignity (derived from sign placement)
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        pdata = planets.get(name, {})
        si = pdata.get("sign_index")
        if si is not None:
            values[f"dignity_{name.lower()}"] = _pjh_dignity(name, si)
        else:
            values[f"dignity_{name.lower()}"] = None

    # Phase 2: house lords
    for h in range(1, 13):
        sign_idx = (lagna_sign_index + h - 1) % 12
        values[f"house_{h}_lord"] = _SIGN_LORDS[sign_idx]

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
        elif "nakshatra" in key:
            try:
                out[key] = normalize_nakshatra(val)
            except (ValueError, TypeError):
                out[key] = val
        elif "sign" in key:
            try:
                out[key] = normalize_sign(val)
            except (ValueError, TypeError):
                out[key] = val
        else:
            out[key] = val
    return out


def _build_schema(has_edge_flags: bool) -> dict:
    """Build the field comparison schema — Phase 1 + 2 + 3."""
    lon_tol = 0.2 if has_edge_flags else 0.1
    schema = {
        "lagna_degree": {"field_type": "longitude", "tolerance": lon_tol},
        "lagna_sign": {"field_type": "categorical"},
    }

    # Phase 1: positions + nakshatras
    for name in PLANET_NAMES:
        n = name.lower()
        schema[f"longitude_{n}"] = {
            "field_type": "longitude", "tolerance": lon_tol,
        }
        schema[f"sign_{n}"] = {"field_type": "categorical"}
        schema[f"nakshatra_{n}"] = {"field_type": "categorical"}

    # Phase 2: dignity
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        schema[f"dignity_{name.lower()}"] = {"field_type": "categorical"}

    # Phase 2: house lords
    for h in range(1, 13):
        schema[f"house_{h}_lord"] = {"field_type": "categorical"}

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
