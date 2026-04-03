"""
Compute all ADB stubs with PyJHora (Lahiri ayanamsha).

Produces unbiased lagna distribution for chart selection.
G17: PyJHora (AGPL-3.0) allowed in tools/ for study only.

Usage:
    .venv/bin/python tools/compute_pyjhora_all.py [--limit N] [--output PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from jhora.panchanga import drik  # noqa: E402, TID251
from jhora.horoscope.chart.charts import rasi_chart  # noqa: E402, TID251
from jhora.horoscope.chart import ashtakavarga  # noqa: E402, TID251
from jhora.horoscope.chart.charts import divisional_chart  # noqa: E402, TID251
from jhora.horoscope.chart import strength as jhora_strength  # noqa: E402, TID251
from jhora.horoscope.dhasa.graha import vimsottari  # noqa: E402, TID251
import swisseph as swe  # noqa: E402

ADB_DIR = ROOT / "tests" / "fixtures" / "adb_charts"
OUTPUT_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# PyJHora uses Swiss Ephemeris planet constants:
# 0=Sun, 1=Moon, 2=Mars, 3=Mercury, 4=Jupiter, 5=Venus, 6=Saturn, 7=Rahu, 8=Ketu
PJH_PLANET_MAP = {
    0: "Sun", 1: "Moon", 2: "Mars", 3: "Mercury", 4: "Jupiter",
    5: "Venus", 6: "Saturn", 7: "Rahu", 8: "Ketu",
}


def compute_one_chart(birth_data: dict) -> dict | None:
    """Compute a single chart with PyJHora. Returns None on failure."""
    try:
        drik.set_ayanamsa_mode("LAHIRI")

        place = drik.Place(
            "loc",
            birth_data["lat"],
            birth_data["lon"],
            birth_data["tz_offset"],
        )

        # PyJHora expects LOCAL time JD — it subtracts tz internally
        # (drik.py: jd_utc = jd - place.timezone / 24)
        jd = swe.julday(
            birth_data["year"],
            birth_data["month"],
            birth_data["day"],
            birth_data["hour"],
        )

        chart = rasi_chart(jd, place)
        if not chart:
            return None

        result = {"planets": {}}
        for entry in chart:
            planet_id, (rasi_idx, degree_in_sign) = entry
            if planet_id == "L":
                result["lagna_sign"] = SIGN_NAMES[rasi_idx]
                result["lagna_sign_index"] = rasi_idx
                result["lagna_degree"] = rasi_idx * 30 + degree_in_sign
                result["lagna_degree_in_sign"] = degree_in_sign
            elif planet_id in PJH_PLANET_MAP:
                name = PJH_PLANET_MAP[planet_id]
                result["planets"][name] = {
                    "longitude": rasi_idx * 30 + degree_in_sign,
                    "sign": SIGN_NAMES[rasi_idx],
                    "sign_index": rasi_idx,
                    "degree_in_sign": degree_in_sign,
                }

        # Phase 1: Panchangam
        try:
            tithi_data = drik.tithi(jd, place)
            vara_data = drik.vaara(jd)
            yogam_data = drik.yogam(jd, place)
            _karana_data = drik.karana(jd, place)  # noqa: F841 — computed for future use
            result["panchangam"] = {
                "tithi": tithi_data[0] if isinstance(tithi_data, (list, tuple)) else None,
                "vara": vara_data if isinstance(vara_data, int) else None,
                "yoga": yogam_data[0] if isinstance(yogam_data, (list, tuple)) else None,
            }
        except Exception:
            result["panchangam"] = None

        # Phase 3: Ashtakavarga
        try:
            house_list = ["" for _ in range(12)]
            for entry in chart:
                pid, (rasi, _deg) = entry
                tag = "L" if pid == "L" else str(pid) if isinstance(pid, int) else None
                if tag is None:
                    continue
                if house_list[rasi]:
                    house_list[rasi] += "/" + tag
                else:
                    house_list[rasi] = tag
            bav, sav, _pav = ashtakavarga.get_ashtaka_varga(house_list)
            result["sarva_av"] = sav  # list of 12 ints (Aries..Pisces)
        except Exception:
            result["sarva_av"] = None

        # Phase 3: Vimsottari dasha (sequence + JD boundaries)
        try:
            md = vimsottari.vimsottari_mahadasa(jd, place)
            result["vimsottari_sequence"] = [
                PJH_PLANET_MAP.get(k, str(k)) for k in md.keys()
            ]
            result["vimsottari_jds"] = [float(v) for v in md.values()]
        except Exception:
            result["vimsottari_sequence"] = None
            result["vimsottari_jds"] = None

        # Phase 3: Shadbala
        try:
            sb = jhora_strength.shad_bala(jd, place)
            result["shadbala"] = sb
        except Exception:
            result["shadbala"] = None

        # Phase 3: D9 Navamsha
        try:
            d9_chart = divisional_chart(jd, place, divisional_chart_factor=9)
            d9_data = {"planets": {}}
            for entry in d9_chart:
                pid, (rasi_idx, deg) = entry
                if pid == "L":
                    d9_data["lagna_sign"] = SIGN_NAMES[rasi_idx]
                elif pid in PJH_PLANET_MAP:
                    name = PJH_PLANET_MAP[pid]
                    d9_data["planets"][name] = {
                        "sign": SIGN_NAMES[rasi_idx],
                        "sign_index": rasi_idx,
                        "degree_in_sign": deg,
                    }
            result["d9"] = d9_data
        except Exception:
            result["d9"] = None

        return result

    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Compute all ADB stubs with PyJHora"
    )
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of charts (0=all)")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    stubs = sorted(ADB_DIR.glob("*.json"))
    if args.limit > 0:
        stubs = stubs[: args.limit]

    success = 0
    fail = 0
    start = time.time()

    for i, stub_path in enumerate(stubs):
        stub = json.loads(stub_path.read_text())
        birth_data = stub.get("birth_data")
        if not birth_data:
            fail += 1
            continue

        result = compute_one_chart(birth_data)
        if result is None:
            fail += 1
            continue

        out = {
            "chart_id": stub_path.stem,
            "name": stub.get("name", ""),
            "rodden_rating": stub.get("rodden_rating", ""),
            "birth_data": birth_data,
            "birth_place": stub.get("birth_place", ""),
            "pyjhora": result,
        }

        out_path = args.output / f"{stub_path.stem}.json"
        out_path.write_text(json.dumps(out, indent=2, default=str))
        success += 1

        if (i + 1) % 500 == 0:
            elapsed = time.time() - start
            rate = (i + 1) / elapsed
            print(f"  [{i+1}/{len(stubs)}] {rate:.1f} charts/sec, "
                  f"{success} ok, {fail} fail")

    elapsed = time.time() - start
    print(f"\nDone: {success} computed, {fail} failed, "
          f"{elapsed:.1f}s total")


if __name__ == "__main__":
    main()
