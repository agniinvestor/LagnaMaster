"""
Backfill tz_offset for ADB stubs that have lat/lon but no timezone.

Uses timezonefinder to get the IANA timezone, then computes the UTC offset
for the specific birth date (handling DST correctly).

Usage:
    .venv/bin/python tools/backfill_tz_offset.py [--dry-run] [--limit N]
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

ROOT = Path(__file__).parent.parent
ADB_DIR = ROOT / "tests" / "fixtures" / "adb_charts"

tf = TimezoneFinder()


def compute_tz_offset(lat: float, lon: float, year: int, month: int,
                      day: int, hour: float) -> float | None:
    """Compute UTC offset in hours for a given location and datetime."""
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        return None

    try:
        tz = ZoneInfo(tz_name)
        h = int(hour)
        m = int((hour - h) * 60)
        dt = datetime(year, month, day, h, m, tzinfo=tz)
        offset = dt.utcoffset()
        if offset is None:
            return None
        return offset.total_seconds() / 3600.0
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="Backfill tz_offset")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    stubs = sorted(ADB_DIR.glob("*.json"))
    updated = 0
    failed = 0
    skipped = 0

    for i, path in enumerate(stubs):
        if args.limit and i >= args.limit:
            break

        data = json.loads(path.read_text())
        bd = data.get("birth_data", {})

        if "tz_offset" in bd:
            skipped += 1
            continue

        if not all(k in bd for k in ("year", "month", "day", "hour", "lat", "lon")):
            skipped += 1
            continue

        tz = compute_tz_offset(
            bd["lat"], bd["lon"], bd["year"], bd["month"], bd["day"], bd["hour"]
        )

        if tz is None:
            failed += 1
            continue

        bd["tz_offset"] = tz
        bd["ayanamsha"] = "lahiri"

        if not args.dry_run:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

        updated += 1

        if (i + 1) % 500 == 0:
            print(f"  [{i+1}/{len(stubs)}] updated={updated} failed={failed}")

    print(f"\nDone: {updated} updated, {failed} failed, {skipped} skipped")


if __name__ == "__main__":
    main()
