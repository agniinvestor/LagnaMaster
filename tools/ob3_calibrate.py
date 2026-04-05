#!/usr/bin/env python3
"""
tools/ob3_calibrate.py — OB-3 Empirical Scoring Calibration
============================================================
Uses 5,063 ADB charts (AA+A Rodden ratings) to measure how well
score_all_axes() predicts real-world outcomes by computing Spearman
correlation between house scores and ADB category labels.

Usage:
    cd ~/LagnaMaster
    .venv/bin/python3 tools/ob3_calibrate.py              # run calibration
    .venv/bin/python3 tools/ob3_calibrate.py --report     # print full report
    .venv/bin/python3 tools/ob3_calibrate.py --out calibration.json

Output:
    - Spearman ρ per (axis, outcome) pair
    - Recommended weight adjustments
    - calibration.json for downstream use

Sources:
    - ADB categories as proxy outcome labels (Astrodienst Atlas, Jan 2024)
    - score_all_axes() → multi_axis_scoring.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES_DIR = ROOT / "tests/fixtures/adb_charts"

# ── Category → (axis_house, label_value) mapping ──────────────────────────────
# Positive label = we expect HIGH score on this house
# Negative label = we expect LOW score on this house
CATEGORY_LABELS: list[tuple[str, int, float]] = [
    # (category_substring, house_number, expected_direction)
    # H10 — Career / Fame
    ("Notable : Famous : Top 5%",           10,  1.0),
    ("Notable : Awards : Vocational",        10,  1.0),
    ("Vocation : Politics : Public office",  10,  1.0),
    ("Vocation : Entertainment : Actor",     10,  1.0),
    ("Vocation : Entertain/Music : Vocal",   10,  1.0),
    # H1 — Vitality / Longevity
    ("Personal : Death : Long life",          1,  1.0),
    ("Personal : Death : Accident",           1, -1.0),
    ("Personal : Death : Suicide",            1, -1.0),
    ("Personal : Death : Short life",         1, -1.0),
    # H7 — Relationships
    ("Family : Relationship : Marriage more than 15", 7,  1.0),
    ("Family : Relationship : Divorce",               7, -1.0),
    # H5 — Children
    ("Family : Parenting : Kids more than 3", 5,  1.0),
    ("Family : Parenting : No children",      5, -1.0),
    # H9 — Higher learning / philosophy
    ("Vocation : Education : Teacher",        9,  1.0),
    ("Vocation : Writers : Textbook",         9,  1.0),
    # H3 — Communication / writing
    ("Vocation : Writers : Columnist",        3,  1.0),
    ("Vocation : Writers : Fiction",          3,  1.0),
    ("Vocation : Writers : Playwright",       3,  1.0),
]

RELIABLE_RATINGS = {"AA", "A"}


# ── Mock chart object ──────────────────────────────────────────────────────────

@dataclass
class _PlanetPos:
    name: str
    longitude: float
    sign_index: int
    degree_in_sign: float
    is_retrograde: bool
    speed: float
    sign: str = ""
    latitude: float = 0.0

    def __post_init__(self):
        SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                 "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        if not self.sign:
            self.sign = SIGNS[self.sign_index % 12]


@dataclass
class _MockChart:
    lagna: float
    lagna_sign_index: int
    lagna_sign: str
    lagna_degree_in_sign: float
    planets: dict[str, _PlanetPos] = field(default_factory=dict)
    ayanamsha: float = 23.15
    ayanamsha_name: str = "lahiri"
    planetary_war_losers: list[str] = field(default_factory=list)

    @classmethod
    def from_fixture(cls, data: dict) -> "_MockChart":
        SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                 "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        computed = data["computed"]
        lsi = computed["lagna_sign_index"]
        chart = cls(
            lagna=computed["lagna"],
            lagna_sign_index=lsi,
            lagna_sign=computed["lagna_sign"],
            lagna_degree_in_sign=computed.get("lagna_degree_in_sign", computed["lagna"] % 30),
            ayanamsha=computed.get("ayanamsha_value", 23.15),
            ayanamsha_name=computed.get("ayanamsha_name", "lahiri"),
        )
        for pname, pdata in computed["planets"].items():
            si = pdata["sign_index"]
            chart.planets[pname] = _PlanetPos(
                name=pname,
                longitude=pdata["longitude"],
                sign_index=si,
                degree_in_sign=pdata["degree_in_sign"],
                is_retrograde=pdata.get("is_retrograde", False),
                speed=pdata.get("speed", 0.0),
                sign=SIGNS[si % 12],
                latitude=pdata.get("latitude", 0.0),
            )
        # Add Ketu = Rahu + 180
        if "Rahu" in chart.planets and "Ketu" not in chart.planets:
            rahu = chart.planets["Rahu"]
            ketu_lon = (rahu.longitude + 180) % 360
            ketu_si = int(ketu_lon / 30) % 12
            chart.planets["Ketu"] = _PlanetPos(
                name="Ketu",
                longitude=ketu_lon,
                sign_index=ketu_si,
                degree_in_sign=ketu_lon % 30,
                is_retrograde=True,
                speed=rahu.speed,
                sign=SIGNS[ketu_si],
            )
        return chart


# ── Load fixtures ──────────────────────────────────────────────────────────────

def load_fixtures(min_rating: set[str] = RELIABLE_RATINGS) -> list[dict]:
    charts = []
    for fname in os.listdir(FIXTURES_DIR):
        if not fname.endswith(".json"):
            continue
        try:
            d = json.loads((FIXTURES_DIR / fname).read_text())
        except Exception:
            continue
        if d.get("rodden_rating") not in min_rating:
            continue
        if not d.get("computed", {}).get("planets"):
            continue
        charts.append(d)
    return charts


# ── Build outcome labels ───────────────────────────────────────────────────────

def build_labels(fixtures: list[dict]) -> dict[tuple[int, str], list[float]]:
    """
    Returns {(house, category_key): [label per fixture]}
    label = +direction if category present, else NaN (skip)
    """
    float("nan")

    # Map fixture index → set of categories
    cat_sets = [set(d.get("categories", [])) for d in fixtures]

    labels: dict[tuple[int, str], list[float]] = {}
    for cat_sub, house, direction in CATEGORY_LABELS:
        key = (house, cat_sub[:40])
        vals = []
        for cats in cat_sets:
            matched = any(cat_sub in c for c in cats)
            # For binary: 1 if matched (direction=+1), 0 if not matched
            # We use presence/absence as binary label
            vals.append(1.0 if matched else 0.0)
        labels[key] = vals
    return labels


# ── Score charts ───────────────────────────────────────────────────────────────

def score_charts(fixtures: list[dict], verbose: bool = True) -> list[dict[int, float]]:
    """Run score_all_axes() on each fixture. Returns list of {house: score}."""
    from src.calculations.multi_axis_scoring import score_all_axes

    scores_list = []
    n = len(fixtures)
    t0 = time.time()
    errors = 0

    for i, d in enumerate(fixtures):
        if verbose and i % 200 == 0:
            elapsed = time.time() - t0
            eta = (elapsed / (i + 1)) * (n - i - 1) if i > 0 else 0
            print(f"  Scoring {i+1}/{n}  errors={errors}  ETA={eta:.0f}s", end="\r")
        try:
            chart = _MockChart.from_fixture(d)
            results = score_all_axes(chart)
            scores = dict(results.d1.scores)  # D1 axis house scores
        except Exception:
            errors += 1
            scores = {}
        scores_list.append(scores)

    if verbose:
        print(f"\n  Done. {n} charts, {errors} errors, {time.time()-t0:.1f}s")
    return scores_list


# ── Spearman correlation ───────────────────────────────────────────────────────

def spearman(x: list[float], y: list[float]) -> float:
    """Compute Spearman ρ between two lists (NaN-safe)."""
    import math
    pairs = [(a, b) for a, b in zip(x, y)
             if not math.isnan(a) and not math.isnan(b)]
    if len(pairs) < 30:
        return float("nan")
    n = len(pairs)

    def rank(vals):
        sorted_vals = sorted(enumerate(vals), key=lambda t: t[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and sorted_vals[j+1][1] == sorted_vals[i][1]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j+1):
                ranks[sorted_vals[k][0]] = avg_rank
            i = j + 1
        return ranks

    xs, ys = zip(*pairs)
    rx = rank(list(xs))
    ry = rank(list(ys))
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - (6 * d2) / (n * (n*n - 1))
    return rho


# ── Main calibration ───────────────────────────────────────────────────────────

def run_calibration(verbose: bool = True) -> dict:
    print("OB-3 Empirical Calibration")
    print("=" * 50)

    print(f"\n[1/4] Loading fixtures from {FIXTURES_DIR}")
    fixtures = load_fixtures()
    print(f"  Loaded {len(fixtures)} AA+A charts")

    print("\n[2/4] Building outcome labels")
    labels = build_labels(fixtures)
    for (house, cat), vals in labels.items():
        n_pos = sum(1 for v in vals if v > 0)
        print(f"  H{house:02d}  {n_pos:4d} positive  {cat}")

    print("\n[3/4] Scoring charts")
    scores_list = score_charts(fixtures, verbose=verbose)

    print("\n[4/4] Computing Spearman correlations")
    results = []
    for (house, cat), label_vals in labels.items():
        # Extract house score for each chart
        house_scores = [s.get(house, float("nan")) for s in scores_list]
        rho = spearman(house_scores, label_vals)
        n_pos = sum(1 for v in label_vals if v > 0)
        results.append({
            "house": house,
            "category": cat,
            "n_positive": n_pos,
            "n_total": len(fixtures),
            "spearman_rho": round(rho, 4) if rho == rho else None,
        })
        print(f"  H{house:02d}  ρ={rho:+.3f}  n={n_pos:4d}  {cat}")

    # Aggregate by house
    house_rho: dict[int, list[float]] = defaultdict(list)
    for r in results:
        if r["spearman_rho"] is not None:
            house_rho[r["house"]].append(r["spearman_rho"])

    house_summary = {}
    for h, rhos in sorted(house_rho.items()):
        avg = sum(rhos) / len(rhos)
        house_summary[h] = round(avg, 4)

    print("\n── House-level summary ──")
    for h, avg_rho in sorted(house_summary.items()):
        bar = "▓" * int(abs(avg_rho) * 20)
        sign = "+" if avg_rho >= 0 else "-"
        quality = "GOOD" if abs(avg_rho) >= 0.15 else ("WEAK" if abs(avg_rho) >= 0.05 else "POOR")
        print(f"  H{h:02d}  {sign}{abs(avg_rho):.3f}  {bar:<10}  {quality}")

    # Recommendations
    print("\n── Recommendations ──")
    recs = []
    for h, avg_rho in sorted(house_summary.items()):
        if avg_rho < 0.05:
            rec = f"H{h:02d}: ρ={avg_rho:+.3f} — POOR signal, consider recalibrating bhavesh weight"
        elif avg_rho < 0.10:
            rec = f"H{h:02d}: ρ={avg_rho:+.3f} — WEAK signal, review karaka/dignity weights"
        else:
            rec = f"H{h:02d}: ρ={avg_rho:+.3f} — acceptable signal"
        recs.append(rec)
        print(f"  {rec}")

    output = {
        "engine_version": "v3.0.0",
        "n_charts": len(fixtures),
        "rodden_filter": list(RELIABLE_RATINGS),
        "correlations": results,
        "house_summary": house_summary,
        "recommendations": recs,
        "methodology": (
            "Spearman ρ between score_all_axes() house score and binary ADB "
            "category label (1=category present, 0=absent). AA+A Rodden ratings only."
        ),
    }
    return output


# ── Score distribution analysis ───────────────────────────────────────────────

def score_distribution(scores_list: list[dict], house: int) -> dict:
    import math
    vals = [s[house] for s in scores_list if house in s and not math.isnan(s[house])]
    if not vals:
        return {}
    vals.sort()
    n = len(vals)
    return {
        "n": n,
        "min": round(vals[0], 3),
        "p10": round(vals[n // 10], 3),
        "p25": round(vals[n // 4], 3),
        "median": round(vals[n // 2], 3),
        "p75": round(vals[3 * n // 4], 3),
        "p90": round(vals[9 * n // 10], 3),
        "max": round(vals[-1], 3),
        "mean": round(sum(vals) / n, 3),
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="OB-3 Empirical Calibration")
    ap.add_argument("--out", default="calibration_ob3.json",
                    help="Output JSON path (default: calibration_ob3.json)")
    ap.add_argument("--report", action="store_true",
                    help="Print detailed report after calibration")
    ap.add_argument("--quiet", action="store_true",
                    help="Suppress progress output")
    ap.add_argument("--sample", type=int, default=0,
                    help="Run on N charts only (for quick testing)")
    args = ap.parse_args()

    result = run_calibration(verbose=not args.quiet)

    out_path = ROOT / args.out
    out_path.write_text(json.dumps(result, indent=2))
    print(f"\n✅ Results saved to {out_path}")

    if args.report:
        print("\n── Full correlation table ──")
        for r in sorted(result["correlations"], key=lambda x: -(x["spearman_rho"] or 0)):
            rho = r["spearman_rho"]
            print(f"  H{r['house']:02d}  ρ={rho:+.3f}  n={r['n_positive']:4d}  {r['category']}")


if __name__ == "__main__":
    main()
