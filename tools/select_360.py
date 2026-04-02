"""
Deterministic selection of diverse charts from PyJHora-computed ADB stubs.

Adapts to available pool: takes all qualifying charts per lagna (target 30,
but accepts fewer when pool is limited). Selection criteria:
- Rodden AA or A only
- Composite score: data_quality + diversity + edge_case_density
- Deterministic tie-break: score desc → birth_year asc → chart_id asc

Usage:
    .venv/bin/python tools/select_360.py [--input DIR] [--output PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

PYJHORA_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"
OUTPUT_PATH = ROOT / "tests" / "fixtures" / "verified_360.json"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

COMBUSTION_THRESHOLDS = {
    "Mercury": 14, "Venus": 10, "Mars": 17, "Jupiter": 11, "Saturn": 15,
}

NAKSHATRA_SPAN = 360.0 / 27.0  # 13.333...°

CHARTS_PER_LAGNA = 30  # target, not enforced
GOLDEN_50_COUNT = 50


def _compute_edge_flags(birth_data: dict, pjh: dict) -> dict:
    """Compute binary edge-case flags."""
    flags = {}

    # Lagna boundary
    lagna_in_sign = pjh.get("lagna_degree_in_sign", 15.0)
    flags["lagna_boundary"] = lagna_in_sign < 1.0 or lagna_in_sign > 29.0

    # Nakshatra boundary (Moon within 0.5° of boundary)
    moon_lon = pjh.get("planets", {}).get("Moon", {}).get("longitude", 180.0)
    nak_position_in_span = moon_lon % NAKSHATRA_SPAN
    flags["nakshatra_boundary"] = (
        nak_position_in_span < 0.5
        or nak_position_in_span > (NAKSHATRA_SPAN - 0.5)
    )

    # Retrograde — stubbed (PyJHora rasi_chart doesn't expose speed)
    flags["retrograde_present"] = False

    # Combustion edge
    sun_lon = pjh.get("planets", {}).get("Sun", {}).get("longitude", 0.0)
    flags["combustion_edge"] = False
    for planet, threshold in COMBUSTION_THRESHOLDS.items():
        p_lon = pjh.get("planets", {}).get(planet, {}).get("longitude")
        if p_lon is not None:
            dist = abs(p_lon - sun_lon)
            if dist > 180:
                dist = 360 - dist
            if abs(dist - threshold) <= 1.0:
                flags["combustion_edge"] = True
                break

    # Exact conjunction
    planet_names = [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    ]
    longitudes = []
    for name in planet_names:
        lon = pjh.get("planets", {}).get(name, {}).get("longitude")
        if lon is not None:
            longitudes.append(lon)
    flags["exact_conjunction"] = False
    for i in range(len(longitudes)):
        for j in range(i + 1, len(longitudes)):
            diff = abs(longitudes[i] - longitudes[j])
            if diff > 180:
                diff = 360 - diff
            if diff < 1.0:
                flags["exact_conjunction"] = True
                break
        if flags["exact_conjunction"]:
            break

    # Midnight window
    hour = birth_data.get("hour", 12.0)
    flags["midnight_window"] = hour < (10 / 60) or hour > (23 + 50 / 60)

    # High latitude
    lat = birth_data.get("lat", 0.0)
    flags["high_latitude"] = abs(lat) >= 50.0

    # DST transition — simplified
    month = birth_data.get("month", 6)
    flags["dst_transition"] = month in (3, 10, 11)

    return flags


def select(input_dir: Path) -> dict:
    """Select charts deterministically from all available."""
    candidates_by_lagna: dict[str, list[dict]] = {s: [] for s in SIGN_NAMES}

    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text())
        rating = data.get("rodden_rating", "")
        if rating not in ("AA", "A"):
            continue

        pjh = data.get("pyjhora", {})
        lagna = pjh.get("lagna_sign")
        if not lagna or lagna not in SIGN_NAMES:
            continue

        birth_data = data.get("birth_data", {})
        flags = _compute_edge_flags(birth_data, pjh)
        edge_count = sum(1 for v in flags.values() if v)
        quality = 1.0 if rating == "AA" else 0.8

        candidates_by_lagna[lagna].append({
            "chart_id": data["chart_id"],
            "rodden_rating": rating,
            "score": round(quality + edge_count, 2),
            "edge_case_flags": flags,
            "edge_case_count": edge_count,
            "pyjhora_lagna_degree": round(pjh.get("lagna_degree", 0.0), 4),
            "birth_year": birth_data.get("year", 0),
            "golden_50": False,
        })

    # Sort each lagna group deterministically
    selected: dict[str, list[dict]] = {}
    all_entries = []

    for lagna in SIGN_NAMES:
        pool = candidates_by_lagna[lagna]
        pool.sort(key=lambda c: (-c["score"], c["birth_year"], c["chart_id"]))

        chosen = pool[:CHARTS_PER_LAGNA]
        for rank, c in enumerate(chosen, 1):
            c["selection_rank"] = rank

        selected[lagna] = chosen
        all_entries.extend(chosen)

    # Tag golden 50 (or fewer if total < 50)
    all_entries.sort(key=lambda c: (-c["edge_case_count"], c["chart_id"]))
    golden_count = min(GOLDEN_50_COUNT, len(all_entries))
    golden_ids = {c["chart_id"] for c in all_entries[:golden_count]}
    for lagna_entries in selected.values():
        for entry in lagna_entries:
            entry["golden_50"] = entry["chart_id"] in golden_ids
            entry.pop("birth_year", None)  # internal, not in output

    total = sum(len(v) for v in selected.values())

    # Compute selection hash
    selection_input = json.dumps(selected, sort_keys=True)
    selection_hash = hashlib.sha256(selection_input.encode()).hexdigest()

    manifest = {
        "schema_version": "1.0",
        "generated_date": "2026-04-03",
        "engine_versions": {"lagnamaster": "3.0.0", "pyjhora": "4.7.0"},
        "selection_hash": selection_hash,
        "total_charts": total,
        "golden_50_count": sum(
            1 for entries in selected.values()
            for e in entries if e["golden_50"]
        ),
    }
    manifest.update(selected)

    return manifest


def main():
    parser = argparse.ArgumentParser(description="Select diverse charts")
    parser.add_argument("--input", type=Path, default=PYJHORA_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    manifest = select(args.input)
    args.output.write_text(json.dumps(manifest, indent=2))

    print(f"Manifest written to {args.output}")
    print(f"  Total: {manifest['total_charts']}")
    print(f"  Golden: {manifest['golden_50_count']}")
    print(f"  Per lagna:")
    for sign in SIGN_NAMES:
        count = len(manifest.get(sign, []))
        print(f"    {sign}: {count}")


if __name__ == "__main__":
    main()
