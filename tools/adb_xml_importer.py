#!/usr/bin/env python3
"""
tools/adb_xml_importer.py — LagnaMaster ADB XML Importer
Parses the official Astrodienst ADB XML export format (schema 160715)
and converts records to LagnaMaster fixture JSON files.

Usage:
    # Import from c_sample.zip (already downloaded):
    cd ~/LagnaMaster
    .venv/bin/python3 tools/adb_xml_importer.py adb_sample/c_sample.xml

    # Import full dataset (after license is signed and file received):
    .venv/bin/python3 tools/adb_xml_importer.py /path/to/adb_full_export.xml

    # Filter by minimum Rodden rating (default: AA and A only):
    .venv/bin/python3 tools/adb_xml_importer.py adb_sample/c_sample.xml --min-rating A

    # Dry run (print parsed records, no files written):
    .venv/bin/python3 tools/adb_xml_importer.py adb_sample/c_sample.xml --dry-run

Key design decisions:
    - jd_ut from <sbtime jd_ut="..."> is used directly — no timezone guesswork
    - lat/lon parsed from slati/slong attributes (e.g. "45n10", "9e10")
    - Rodden rating stored in fixture for trust-aware test assertions
    - Records with time_unknown are stored but flagged — Lagna not computed
    - research_data (categories, events) stored but never used in engine scoring
      (per ADB copyright: research_data is for research only, not for services)

Schema reference: https://www.astro.com/astro-databank/Help:XML_export_format
License: https://www.astro.com/adbexport/adb_export_license.pdf

Copyright notice: Birth data (public_data) is freely redistributable.
research_data requires individual permission for service use — it is stored
in fixtures but never exposed via the LagnaMaster API or consumer layer.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "adb_charts"

# Rodden rating numeric rank (higher = more reliable)
RODDEN_RANK = {"AA": 5, "A": 4, "B": 3, "C": 2, "DD": 1, "X": 0, "XX": 0}

# Minimum rating to import (default: B and above)
DEFAULT_MIN_RATING = "B"


@dataclass
class ADBRecord:
    adb_id: int
    name: str                          # "Cardano, Girolamo"
    given_name: str                    # "Girolamo Cardano"
    gender: str                        # "m", "f", "e", "u"
    rodden_rating: str                 # "AA", "A", "B", "C", "DD", "X", "XX"
    rodden_rank: int

    # Birth data
    jd_ut: Optional[float]            # Julian Day UT — primary key for computation
    year: int
    month: int
    day: int
    calendar: str                      # "g" (gregorian) or "j" (julian)
    time_str: str                      # "18:29"
    time_type: str                     # "l"=LMT, "u"=UT, "z"=zone, "s"=solar
    time_zone_merid: str               # e.g. "m9e10" (meridian 9°10'E)
    time_unknown: bool

    # Location
    place: str
    country: str
    lat: float
    lon: float

    # Pre-computed positions from ADB (tropical, for cross-check only)
    sun_sign: str
    moon_sign: str
    asc_sign: str

    # Source
    adb_link: str
    source_notes: str
    categories: list[str] = field(default_factory=list)


def _parse_latlon(slati: str, slong: str) -> tuple[float, float]:
    """
    Parse ADB lat/lon strings to decimal degrees.
    slati like "45n10" or "52n0445" (52°04'45")
    slong like "9e10" or "1w20"
    """
    def _parse_one(s: str, pos_char: str, neg_char: str) -> float:
        s = s.lower()
        sign = 1 if pos_char in s else -1
        s = s.replace(pos_char, ".").replace(neg_char, ".")
        parts = s.split(".")
        deg = int(parts[0]) if parts[0] else 0
        rest = parts[1] if len(parts) > 1 else "0"
        # rest can be MM or MMSS
        if len(rest) <= 2:
            mins = int(rest)
            secs = 0
        else:
            mins = int(rest[:2])
            secs = int(rest[2:4]) if len(rest) >= 4 else 0
        return sign * (deg + mins / 60.0 + secs / 3600.0)

    lat = _parse_one(slati, "n", "s")
    lon = _parse_one(slong, "e", "w")
    return round(lat, 6), round(lon, 6)


def _parse_time(time_str: str) -> float:
    """Convert "18:29" to decimal hours 18.4833... Robust against malformed input."""
    try:
        # Strip anything non-numeric before the first digit
        import re as _re
        clean = time_str.strip()
        # Extract first HH:MM or HH:MM:SS pattern found
        m = _re.search(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", clean)
        if m:
            h = int(m.group(1))
            mi = int(m.group(2))
            s = int(m.group(3)) if m.group(3) else 0
            return h + mi / 60.0 + s / 3600.0
        # Try plain integer hour
        digits = _re.sub(r"[^\d]", "", clean.split(",")[0])
        if digits:
            return float(digits[:2])
    except Exception:
        pass
    return 12.0  # safe default for unknown times


def _safe_filename(name: str) -> str:
    """Convert "Cardano, Girolamo" to "cardano_girolamo.json"."""
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s-]+", "_", name)
    return name.strip("_") + ".json"


def parse_adb_xml(xml_path: str) -> list[ADBRecord]:
    """Parse the full ADB XML export file and return list of ADBRecord."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    records = []
    for entry in root.findall("adb_entry"):
        try:
            rec = _parse_entry(entry)
            if rec:
                records.append(rec)
        except Exception as e:
            adb_id = entry.get("adb_id", "?")
            print(f"  WARN — adb_id={adb_id}: {e}", file=sys.stderr)

    return records


def _parse_entry(entry: ET.Element) -> Optional[ADBRecord]:
    adb_id = int(entry.get("adb_id", 0))
    pub = entry.find("public_data")
    if pub is None:
        return None

    name = pub.findtext("name", "").strip()
    given = pub.findtext("sflname", name).strip()
    gender_el = pub.find("gender")
    gender = gender_el.get("csex", "u") if gender_el is not None else "u"

    rr_el = pub.find("roddenrating")
    rodden_rating = rr_el.text.strip() if rr_el is not None else "X"
    rodden_rank = RODDEN_RANK.get(rodden_rating, 0)

    bdata = pub.find("bdata")
    if bdata is None:
        return None

    # Date
    sbdate = bdata.find("sbdate")
    if sbdate is None:
        return None
    year  = int(sbdate.get("iyear", 0))
    month = int(sbdate.get("imonth", 0))
    day   = int(sbdate.get("iday", 0))
    calendar = sbdate.get("ccalendar", "g")  # "g" or "j"

    # Time
    sbtime = bdata.find("sbtime")
    jd_ut = None
    time_str = "12:00"
    time_type = "u"
    time_merid = ""
    time_unknown = False

    if sbtime is not None:
        jd_ut_str = sbtime.get("jd_ut")
        if jd_ut_str:
            jd_ut = float(jd_ut_str)
        time_str = sbtime.text.strip() if sbtime.text else "12:00"
        time_type = sbtime.get("ctimetype", "u")
        time_merid = sbtime.get("stmerid", "")
        time_unknown = sbtime.get("time_unknown", "0") == "1"

    # Location
    place_el = bdata.find("place")
    place = place_el.text.strip() if place_el is not None else ""
    slati = place_el.get("slati", "0n00") if place_el is not None else "0n00"
    slong = place_el.get("slong", "0e00") if place_el is not None else "0e00"
    lat, lon = _parse_latlon(slati, slong)

    country_el = bdata.find("country")
    country = country_el.text.strip() if country_el is not None else ""

    # Pre-computed positions (tropical, ADB internal — for reference only)
    pos_el = bdata.find("positions")
    sun_sign = moon_sign = asc_sign = ""
    if pos_el is not None:
        sun_sign  = pos_el.get("sun_sign", "")
        moon_sign = pos_el.get("moon_sign", "")
        asc_sign  = pos_el.get("asc_sign", "")

    # Text data
    text = entry.find("text_data")
    adb_link = ""
    source_notes = ""
    if text is not None:
        adb_link = text.findtext("adb_link", "").strip()
        source_notes = text.findtext("sourcenotes", "").strip()

    # Research data — categories only (for tagging fixtures)
    categories = []
    research = entry.find("research_data")
    if research is not None:
        for cat in research.findall(".//category"):
            if cat.text:
                categories.append(cat.text.strip())

    return ADBRecord(
        adb_id=adb_id, name=name, given_name=given,
        gender=gender, rodden_rating=rodden_rating, rodden_rank=rodden_rank,
        jd_ut=jd_ut, year=year, month=month, day=day,
        calendar=calendar, time_str=time_str, time_type=time_type,
        time_zone_merid=time_merid, time_unknown=time_unknown,
        place=place, country=country, lat=lat, lon=lon,
        sun_sign=sun_sign, moon_sign=moon_sign, asc_sign=asc_sign,
        adb_link=adb_link, source_notes=source_notes,
        categories=categories,
    )


def compute_chart_from_jd(rec: ADBRecord) -> Optional[dict]:
    """
    Compute sidereal chart using jd_ut directly — the correct approach.
    No timezone guesswork; jd_ut from ADB is the ground truth.
    """
    if rec.jd_ut is None:
        return None
    try:
        import swisseph as swe
        ephe_path = str(ROOT / "ephe")
        swe.set_ephe_path(ephe_path)
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL

        _PLANET_IDS = {
            "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
            "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS, "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE,
        }

        planets = {}
        for name, pid in _PLANET_IDS.items():
            if name == "Moon":
                swe.set_topo(rec.lon, rec.lat, 0)
                result, _ = swe.calc_ut(rec.jd_ut, pid, flags | swe.FLG_TOPOCTR)
            else:
                result, _ = swe.calc_ut(rec.jd_ut, pid, flags)
            lon_sid = result[0] % 360
            speed   = result[3]
            sign_idx = int(lon_sid / 30)
            planets[name] = {
                "longitude": round(lon_sid, 6),
                "sign_index": sign_idx,
                "degree_in_sign": round(lon_sid % 30, 6),
                "is_retrograde": speed < 0,
                "speed": round(speed, 6),
            }

        # Ketu = Rahu + 180
        rahu_lon = planets["Rahu"]["longitude"]
        ketu_lon = (rahu_lon + 180) % 360
        planets["Ketu"] = {
            "longitude": round(ketu_lon, 6),
            "sign_index": int(ketu_lon / 30),
            "degree_in_sign": round(ketu_lon % 30, 6),
            "is_retrograde": True,
            "speed": 0.0,
        }

        # Lagna (Ascendant) using ARMC
        topo_flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
        cusps, ascmc = swe.houses_ex(
            rec.jd_ut, rec.lat, rec.lon, b"P", topo_flags
        )
        lagna_lon = ascmc[0] % 360  # tropical ASC
        # Apply ayanamsha correction for sidereal
        ayanamsha = swe.get_ayanamsa_ut(rec.jd_ut)
        lagna_sid = (lagna_lon - ayanamsha) % 360
        lagna_sign_idx = int(lagna_sid / 30)

        _SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

        return {
            "lagna_sign": _SIGNS[lagna_sign_idx],
            "lagna_sign_index": lagna_sign_idx,
            "lagna_degree_in_sign": round(lagna_sid % 30, 6),
            "lagna": round(lagna_sid, 6),
            "ayanamsha_name": "lahiri",
            "ayanamsha_value": round(ayanamsha, 6),
            "jd_ut": rec.jd_ut,
            "planets": planets,
        }
    except Exception as e:
        return {"error": str(e)}


def record_to_fixture(rec: ADBRecord, chart: Optional[dict]) -> dict:
    """Convert ADBRecord + computed chart to LagnaMaster fixture dict."""
    fixture = {
        "adb_id": rec.adb_id,
        "name": rec.name,
        "given_name": rec.given_name,
        "gender": rec.gender,
        "rodden_rating": rec.rodden_rating,
        "rodden_rank": rec.rodden_rank,
        "birth_data": {
            "jd_ut": rec.jd_ut,
            "year": rec.year,
            "month": rec.month,
            "day": rec.day,
            "calendar": rec.calendar,
            "time": rec.time_str,
            "time_type": rec.time_type,
            "hour": round(_parse_time(rec.time_str), 6),
            "time_unknown": rec.time_unknown,
            "place": rec.place,
            "country": rec.country,
            "lat": rec.lat,
            "lon": rec.lon,
        },
        "adb_positions": {
            "sun_sign": rec.sun_sign,
            "moon_sign": rec.moon_sign,
            "asc_sign": rec.asc_sign,
        },
        "adb_link": rec.adb_link,
        "source_notes": rec.source_notes,
        # research_data categories stored for fixture tagging only
        # NOT to be used in service/API per ADB copyright
        "categories": rec.categories,
        "trust_note": (
            "time_unknown — Lagna not reliable" if rec.time_unknown
            else f"Rodden {rec.rodden_rating} — {'high' if rec.rodden_rank >= 4 else 'medium' if rec.rodden_rank == 3 else 'low'} trust"
        ),
    }
    if chart:
        fixture["computed"] = chart
    return fixture


def import_xml(
    xml_path: str,
    min_rating: str = DEFAULT_MIN_RATING,
    dry_run: bool = False,
    overwrite: bool = False,
) -> dict:
    """Main import function. Returns summary stats."""
    min_rank = RODDEN_RANK.get(min_rating.upper(), 0)
    records = parse_adb_xml(xml_path)

    stats = {
        "total_parsed": len(records),
        "below_min_rating": 0,
        "time_unknown": 0,
        "computed_ok": 0,
        "compute_error": 0,
        "written": 0,
        "skipped_existing": 0,
    }

    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    for rec in records:
        if rec.rodden_rank < min_rank:
            stats["below_min_rating"] += 1
            continue

        if rec.time_unknown:
            stats["time_unknown"] += 1

        chart = None
        if rec.jd_ut and not rec.time_unknown:
            chart = compute_chart_from_jd(rec)
            if chart and "error" not in chart:
                stats["computed_ok"] += 1
            else:
                stats["compute_error"] += 1

        fixture = record_to_fixture(rec, chart)

        if dry_run:
            print(f"  [{rec.rodden_rating}] {rec.name} — "
                  f"{'Lagna: ' + chart['lagna_sign'] if chart and 'lagna_sign' in chart else 'time unknown'}")
            continue

        fname = _safe_filename(rec.name)
        fpath = FIXTURE_DIR / fname
        if fpath.exists() and not overwrite:
            stats["skipped_existing"] += 1
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(fixture, f, indent=2, ensure_ascii=False)
        stats["written"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(description="Import ADB XML export to LagnaMaster fixtures")
    parser.add_argument("xml_file", help="Path to ADB XML export file")
    parser.add_argument("--min-rating", default=DEFAULT_MIN_RATING,
                        choices=["AA", "A", "B", "C", "DD"],
                        help="Minimum Rodden rating to import (default: B)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Parse and print records without writing files")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing fixture files")
    args = parser.parse_args()

    if not os.path.exists(args.xml_file):
        print(f"ERROR — file not found: {args.xml_file}")
        sys.exit(1)

    print(f"Importing ADB XML: {args.xml_file}")
    print(f"Minimum Rodden rating: {args.min_rating}")
    print(f"Output dir: {FIXTURE_DIR}")
    print()

    stats = import_xml(
        args.xml_file,
        min_rating=args.min_rating,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )

    print()
    print("=== Import Summary ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if not args.dry_run:
        print()
        print(f"Fixtures written to: {FIXTURE_DIR}")
        print()
        print("Next: sign the ADB license and request the full export:")
        print("  https://www.astro.com/adbexport/adb_export_license.pdf")
        print("  adbdata@astro.com")


if __name__ == "__main__":
    main()
