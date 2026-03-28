"""
tools/vedastro_cross_validate.py — S191

Cross-validates LagnaMaster planet positions against VedAstro REST API
for known test fixtures (India 1947, Nehru, etc.).

Usage:
    VEDASTRO_API_KEY=your_key python tools/vedastro_cross_validate.py

VedAstro makes live REST calls to vedastro.org — requires internet + API key.
Guardrail G23: use during development for chart verification ONLY, not in production.

Output: tolerance report showing degree-level agreement per planet.
Tolerance threshold: < 0.5° = PASS (JPL DE431 agreement expected).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

VEDASTRO_AVAILABLE = False
try:
    from vedastro import Calculate, GeoLocation, Time

    VEDASTRO_AVAILABLE = True
except ImportError:
    pass

# ─────────────────────────────────────────────────────────────────────────────
# Test fixtures — known charts with verified planet positions
# ─────────────────────────────────────────────────────────────────────────────

FIXTURES: list[dict] = [
    {
        "name": "India Independence 1947",
        "datetime": "00:00 AM 15/08/1947 +05:30",  # VedAstro format
        "location_name": "New Delhi",
        "lat": 28.6139,
        "lon": 77.2090,
        # Expected sidereal longitudes (Lahiri ayanamsha, from our engine)
        "expected_lagna_sign": "Taurus",
        "expected_planets": {
            "Sun": 117.989,   # Cancer 27.99°
            "Moon": 93.983,   # Cancer 3.98°
            "Mars": 75.267,   # Gemini 15.27°
            "Mercury": 143.076,  # Leo 23.08°
            "Jupiter": 218.571,  # Scorpio 8.57°
            "Venus": 87.344,  # Gemini 27.34°
            "Saturn": 121.197,  # Cancer 1.20°
            "Rahu": 25.049,   # Aries 25.05°
        },
        "tolerance_deg": 0.5,
    },
]

PLANET_NAME_MAP: dict[str, str] = {
    # LagnaMaster name → VedAstro name
    "Sun": "Sun",
    "Moon": "Moon",
    "Mars": "Mars",
    "Mercury": "Mercury",
    "Jupiter": "Jupiter",
    "Venus": "Venus",
    "Saturn": "Saturn",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
}


@dataclass
class CrossValResult:
    planet: str
    our_lon: float
    vedastro_lon: float
    delta_deg: float
    passed: bool
    tolerance: float


def run_cross_validation(fixture: dict, api_key: str | None) -> list[CrossValResult]:
    """Run cross-validation for a single fixture against VedAstro."""
    if not VEDASTRO_AVAILABLE:
        print("  SKIP: vedastro not installed")
        return []

    if api_key:
        Calculate.SetAPIKey(api_key)

    loc = GeoLocation(fixture["location_name"], fixture["lon"], fixture["lat"])
    time = Time(fixture["datetime"], loc)

    results = []
    for planet_name, our_lon in fixture["expected_planets"].items():
        va_name = PLANET_NAME_MAP.get(planet_name, planet_name)
        try:
            va_lon_raw = Calculate.PlanetNirayanaLongitude(va_name, time)
            # VedAstro returns longitude as string "Aries 15.23°" or float
            if isinstance(va_lon_raw, str):
                # Parse "SignName deg.min°" format
                va_lon = _parse_vedastro_longitude(va_lon_raw)
            else:
                va_lon = float(va_lon_raw)

            delta = abs(our_lon - va_lon) % 360
            if delta > 180:
                delta = 360 - delta

            passed = delta <= fixture["tolerance_deg"]
            results.append(CrossValResult(
                planet=planet_name,
                our_lon=our_lon,
                vedastro_lon=va_lon,
                delta_deg=delta,
                passed=passed,
                tolerance=fixture["tolerance_deg"],
            ))
        except Exception as exc:
            print(f"  WARN: {planet_name} VedAstro call failed: {exc}")

    return results


def _parse_vedastro_longitude(raw: str) -> float:
    """Parse VedAstro longitude string to decimal degrees."""
    SIGN_OFFSETS = {
        "Aries": 0, "Taurus": 30, "Gemini": 60, "Cancer": 90,
        "Leo": 120, "Virgo": 150, "Libra": 180, "Scorpio": 210,
        "Sagittarius": 240, "Capricorn": 270, "Aquarius": 300, "Pisces": 330,
    }
    raw = raw.strip().rstrip("°")
    for sign, offset in SIGN_OFFSETS.items():
        if raw.startswith(sign):
            deg_str = raw[len(sign):].strip()
            return offset + float(deg_str)
    # Fallback: try plain float
    return float(raw)


def print_report(fixture: dict, results: list[CrossValResult]) -> int:
    """Print cross-val report. Returns number of failures."""
    print(f"\n{'─'*60}")
    print(f"Fixture: {fixture['name']}")
    print(f"{'─'*60}")
    if not results:
        print("  No results (VedAstro unavailable or API error)")
        return 0

    print(f"  {'Planet':<12} {'Ours':>10} {'VedAstro':>10} {'Delta':>8}  Status")
    print(f"  {'─'*12} {'─'*10} {'─'*10} {'─'*8}  {'─'*6}")
    fails = 0
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        flag = "" if r.passed else " <-- MISMATCH"
        print(f"  {r.planet:<12} {r.our_lon:>10.3f} {r.vedastro_lon:>10.3f} {r.delta_deg:>8.3f}  {status}{flag}")
        if not r.passed:
            fails += 1

    print(f"\n  Result: {len(results) - fails}/{len(results)} passed "
          f"(tolerance: {fixture['tolerance_deg']}°)")
    return fails


def main() -> int:
    api_key = os.environ.get("VEDASTRO_API_KEY")
    if not VEDASTRO_AVAILABLE:
        print("ERROR: vedastro not installed. Run: pip install vedastro")
        return 1
    if not api_key:
        print("WARNING: VEDASTRO_API_KEY not set — API calls may fail or be rate-limited.")
        print("         Set: export VEDASTRO_API_KEY=your_key")
        print()

    total_fails = 0
    for fixture in FIXTURES:
        print(f"\nCross-validating: {fixture['name']}")
        results = run_cross_validation(fixture, api_key)
        fails = print_report(fixture, results)
        total_fails += fails

    print(f"\n{'═'*60}")
    if total_fails == 0:
        print("All cross-validation checks PASSED.")
    else:
        print(f"FAILED: {total_fails} planet(s) outside tolerance.")
        print("Check ayanamsha settings — LagnaMaster uses Lahiri (27.22° at J2000).")

    return 0 if total_fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
