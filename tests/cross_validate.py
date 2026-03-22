"""
tests/cross_validate.py
Cross-validation against JHora CSV export.
Session 114 (Phase 0).

Usage:
    python tests/cross_validate.py --jhora-csv jhora_1947.csv

JHora CSV export format: planet, longitude, sign, degree, nakshatra
"""

from __future__ import annotations
import argparse
import csv
from dataclasses import dataclass
from typing import Any


@dataclass
class FieldDiff:
    field: str
    lm_value: Any
    jhora_value: Any
    tolerance: float
    within_tolerance: bool


@dataclass
class ValidationReport:
    chart_name: str
    total_fields: int
    passing: int
    failing: int
    diffs: list[FieldDiff]

    @property
    def pass_rate(self) -> float:
        return self.passing / self.total_fields if self.total_fields else 0.0

    def print_summary(self):
        print(f"\n=== Cross-Validation: {self.chart_name} ===")
        print(f"Fields checked: {self.total_fields}")
        print(f"Passing: {self.passing} ({self.pass_rate:.1%})")
        print(f"Failing: {self.failing}")
        if self.failing > 0:
            print("\nFailing fields:")
            for d in self.diffs:
                if not d.within_tolerance:
                    print(
                        f"  {d.field}: LM={d.lm_value:.4f} JHora={d.jhora_value:.4f} "
                        f"(tol±{d.tolerance})"
                    )


def cross_validate_positions(
    lm_chart,
    jhora_csv_path: str,
    chart_name: str = "Chart",
    position_tolerance: float = 0.1,
    shadbala_tolerance_pct: float = 5.0,
) -> ValidationReport:
    """
    Compare LagnaMaster planet positions against JHora CSV export.

    JHora CSV expected columns: planet, longitude
    """
    diffs = []

    try:
        jhora_data: dict[str, float] = {}
        with open(jhora_csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                planet = row.get("planet", "").strip()
                lon = float(row.get("longitude", 0))
                jhora_data[planet] = lon
    except FileNotFoundError:
        print(f"JHora CSV not found: {jhora_csv_path}")
        return ValidationReport(chart_name, 0, 0, 0, [])

    for planet_name, jhora_lon in jhora_data.items():
        if planet_name in lm_chart.planets:
            lm_lon = lm_chart.planets[planet_name].longitude
            diff = abs(lm_lon - jhora_lon) % 360
            diff = min(diff, 360 - diff)
            within = diff <= position_tolerance
            diffs.append(
                FieldDiff(
                    field=f"{planet_name}.longitude",
                    lm_value=lm_lon,
                    jhora_value=jhora_lon,
                    tolerance=position_tolerance,
                    within_tolerance=within,
                )
            )

    # Lagna
    if "Lagna" in jhora_data:
        diff = abs(lm_chart.lagna - jhora_data["Lagna"]) % 360
        diff = min(diff, 360 - diff)
        diffs.append(
            FieldDiff(
                "Lagna",
                lm_chart.lagna,
                jhora_data["Lagna"],
                position_tolerance,
                diff <= position_tolerance,
            )
        )

    passing = sum(1 for d in diffs if d.within_tolerance)
    return ValidationReport(
        chart_name=chart_name,
        total_fields=len(diffs),
        passing=passing,
        failing=len(diffs) - passing,
        diffs=diffs,
    )


# ─── Additional regression fixtures ─────────────────────────────────────────

# Fixture: Neecha Bhanga chart — Mars debilitated in Cancer with 2 NB conditions
NEECHA_BHANGA_FIXTURE = {
    "year": 1990,
    "month": 6,
    "day": 15,
    "hour": 12.0,
    "lat": 28.6139,
    "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
    "_description": "Mars in Cancer (debilitated); Moon in Capricorn-Kendra provides NB",
    "_validates": ["Neecha Bhanga all 6 conditions", "NBRY when >=2 conditions"],
}

# Fixture: Nakshatra cusp birth
NAK_CUSP_FIXTURE = {
    "year": 1947,
    "month": 8,
    "day": 15,
    "hour": 0.0,
    "lat": 28.6139,
    "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
    "_moon_override": 40.000001,  # Moon at exact Krittika start
    "_description": "Moon at exact nakshatra boundary (40.0°)",
    "_validates": ["Nakshatra float boundary fix"],
}

# Fixture: Female chart, night birth
FEMALE_CHART_FIXTURE = {
    "year": 1975,
    "month": 3,
    "day": 21,
    "hour": 22.0,
    "lat": 18.9667,
    "lon": 72.8333,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
    "_description": "Female chart, night birth for gender-specific yoga rules",
    "_validates": ["Mahabhagya Yoga gender conditions"],
}

# Fixture: High-latitude birth (Helsinki, 60.2°N)
HIGH_LATITUDE_FIXTURE = {
    "year": 1985,
    "month": 6,
    "day": 21,
    "hour": 3.0,
    "lat": 60.1699,
    "lon": 24.9384,
    "tz_offset": 3.0,
    "ayanamsha": "lahiri",
    "_description": "Helsinki — high latitude affects house boundaries",
    "_validates": ["Bhava Chalita cusp divergence at high latitude"],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jhora-csv", help="Path to JHora CSV export")
    parser.add_argument("--chart", default="india_1947", help="Chart to validate")
    args = parser.parse_args()

    if args.jhora_csv:
        from src.ephemeris import compute_chart

        if args.chart == "india_1947":
            chart = compute_chart(1947, 8, 15, 0.0, 28.6139, 77.2090, 5.5)
        report = cross_validate_positions(chart, args.jhora_csv, args.chart)
        report.print_summary()
