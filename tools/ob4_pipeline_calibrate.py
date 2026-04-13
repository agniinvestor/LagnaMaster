#!/usr/bin/env python3
"""
tools/ob4_pipeline_calibrate.py — OB-4 Pipeline Calibration
============================================================
Measures how well the NEW unified pipeline (G1-G6) predicts real-world
outcomes, compared to the OLD score_all_axes() house scores.

Computes Spearman ρ for THREE signal types per house:
  1. OLD: raw house score from score_all_axes() (same as OB-3)
  2. NEW: convergence_score from converge() (independent channel count)
  3. NEW: total_confirmations from time_project() (natal + temporal)

If the pipeline is working, signals 2 and 3 should produce equal or
higher ρ than signal 1 for most houses.

Usage:
    .venv/bin/python tools/ob4_pipeline_calibrate.py
    .venv/bin/python tools/ob4_pipeline_calibrate.py --report
    .venv/bin/python tools/ob4_pipeline_calibrate.py --sample 200
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES_DIR = ROOT / "tests/fixtures/adb_charts"

# Same category labels as OB-3 for direct comparison
CATEGORY_LABELS: list[tuple[str, int, float]] = [
    ("Notable : Famous : Top 5%",           10,  1.0),
    ("Notable : Awards : Vocational",        10,  1.0),
    ("Vocation : Politics : Public office",  10,  1.0),
    ("Vocation : Entertainment : Actor",     10,  1.0),
    ("Vocation : Entertain/Music : Vocal",   10,  1.0),
    ("Personal : Death : Long life",          1,  1.0),
    ("Personal : Death : Accident",           1, -1.0),
    ("Personal : Death : Suicide",            1, -1.0),
    ("Personal : Death : Short life",         1, -1.0),
    ("Family : Relationship : Marriage more than 15", 7,  1.0),
    ("Family : Relationship : Divorce",               7, -1.0),
    ("Family : Parenting : Kids more than 3", 5,  1.0),
    ("Family : Parenting : No children",      5, -1.0),
    ("Vocation : Education : Teacher",        9,  1.0),
    ("Vocation : Writers : Textbook",         9,  1.0),
    ("Vocation : Writers : Columnist",        3,  1.0),
    ("Vocation : Writers : Fiction",          3,  1.0),
    ("Vocation : Writers : Playwright",       3,  1.0),
]

RELIABLE_RATINGS = {"AA", "A"}


# ── Mock chart (reused from OB-3) ─────────────────────────────────────────────

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


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
        if not self.sign:
            self.sign = SIGNS[self.sign_index % 12]


@dataclass
class _MockChart:
    lagna: float
    lagna_sign_index: int
    lagna_sign: str
    lagna_degree_in_sign: float
    jd_ut: float = 2432412.5
    ayanamsha_value: float = 23.15
    ayanamsha_name: str = "lahiri"
    planets: dict = field(default_factory=dict)
    planetary_war_losers: list = field(default_factory=list)

    def planet(self, name):
        return self.planets[name]

    @classmethod
    def from_fixture(cls, data: dict) -> "_MockChart":
        computed = data["computed"]
        lsi = computed["lagna_sign_index"]
        chart = cls(
            lagna=computed["lagna"],
            lagna_sign_index=lsi,
            lagna_sign=computed["lagna_sign"],
            lagna_degree_in_sign=computed.get("lagna_degree_in_sign", computed["lagna"] % 30),
            jd_ut=computed.get("jd_ut", 2432412.5),
            ayanamsha_value=computed.get("ayanamsha_value", 23.15),
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
        if "Rahu" in chart.planets and "Ketu" not in chart.planets:
            rahu = chart.planets["Rahu"]
            kl = (rahu.longitude + 180) % 360
            ksi = int(kl / 30) % 12
            chart.planets["Ketu"] = _PlanetPos(
                name="Ketu", longitude=kl, sign_index=ksi,
                degree_in_sign=kl % 30, is_retrograde=True,
                speed=rahu.speed, sign=SIGNS[ksi],
            )
        return chart


# ── Load + label ──────────────────────────────────────────────────────────────

def load_fixtures(max_n: int = 0) -> list[dict]:
    charts = []
    for fname in sorted(os.listdir(FIXTURES_DIR)):
        if not fname.endswith(".json"):
            continue
        try:
            d = json.loads((FIXTURES_DIR / fname).read_text())
        except Exception:
            continue
        if d.get("rodden_rating") not in RELIABLE_RATINGS:
            continue
        if not d.get("computed", {}).get("planets"):
            continue
        charts.append(d)
        if max_n and len(charts) >= max_n:
            break
    return charts


def build_labels(fixtures):
    labels = {}
    cat_sets = [set(d.get("categories", [])) for d in fixtures]
    for cat_sub, house, direction in CATEGORY_LABELS:
        key = (house, cat_sub[:40])
        vals = [1.0 if any(cat_sub in c for c in cats) else 0.0 for cats in cat_sets]
        labels[key] = vals
    return labels


# ── Score with OLD engine (OB-3 baseline) ─────────────────────────────────────

def score_old(fixtures, verbose=True):
    from src.scoring import score_chart
    scores = []
    n = len(fixtures)
    t0 = time.time()
    errors = 0
    for i, d in enumerate(fixtures):
        if verbose and i % 100 == 0:
            print(f"  OLD scoring {i+1}/{n} err={errors}", end="\r")
        try:
            chart = _MockChart.from_fixture(d)
            sc = score_chart(chart)
            scores.append({h: sc.houses[h].final_score for h in range(1, 13)})
        except Exception:
            errors += 1
            scores.append({})
    if verbose:
        print(f"  OLD done. {n} charts, {errors} errors, {time.time()-t0:.1f}s")
    return scores


# ── Score with NEW pipeline ───────────────────────────────────────────────────

def score_new(fixtures, verbose=True):
    from src.calculations.chart_context import build_chart_context
    from src.calculations.unified_engine import evaluate_all_rules
    from src.calculations.convergence import converge
    from src.calculations.temporal_projection import time_project

    convergence_scores = []  # {house: convergence_score}
    total_scores = []        # {house: total_confirmations}
    n = len(fixtures)
    t0 = time.time()
    errors = 0

    for i, d in enumerate(fixtures):
        if verbose and i % 50 == 0:
            print(f"  NEW pipeline {i+1}/{n} err={errors}", end="\r")
        try:
            chart = _MockChart.from_fixture(d)
            bd_data = d.get("birth_data", {})
            bd = None
            if bd_data.get("year") and bd_data.get("month") and bd_data.get("day"):
                try:
                    bd = date(bd_data["year"], bd_data["month"], bd_data["day"])
                except (ValueError, TypeError):
                    pass

            ctx = build_chart_context(chart, birth_date=bd)
            ur = evaluate_all_rules(ctx)
            conv = converge(ur.results, ctx)

            # Build per-house convergence scores
            # For each house, take the NET convergence (favorable - unfavorable)
            conv_by_house = {}
            for cp in conv:
                key = cp.house
                val = cp.convergence_score if cp.direction == "favorable" else -cp.convergence_score
                conv_by_house[key] = conv_by_house.get(key, 0) + val

            # Time project for total_confirmations
            timed = time_project(conv, ctx, birth_date=bd) if bd else []
            total_by_house = {}
            for tp in timed:
                key = tp.house
                val = tp.total_confirmations if tp.direction == "favorable" else -tp.total_confirmations
                total_by_house[key] = total_by_house.get(key, 0) + val

            convergence_scores.append(conv_by_house)
            total_scores.append(total_by_house)
        except Exception:
            errors += 1
            convergence_scores.append({})
            total_scores.append({})

    if verbose:
        print(f"  NEW done. {n} charts, {errors} errors, {time.time()-t0:.1f}s")
    return convergence_scores, total_scores


# ── Spearman ──────────────────────────────────────────────────────────────────

def spearman(x, y):
    pairs = [(a, b) for a, b in zip(x, y) if not math.isnan(a) and not math.isnan(b)]
    if len(pairs) < 30:
        return float("nan")
    n = len(pairs)

    def rank(vals):
        sv = sorted(enumerate(vals), key=lambda t: t[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and sv[j+1][1] == sv[i][1]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j+1):
                ranks[sv[k][0]] = avg_rank
            i = j + 1
        return ranks

    xs, ys = zip(*pairs)
    rx, ry = rank(list(xs)), rank(list(ys))
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - (6 * d2) / (n * (n*n - 1))


# ── Main ──────────────────────────────────────────────────────────────────────

def run(sample: int = 0, verbose: bool = True):
    print("OB-4 Pipeline Calibration")
    print("=" * 60)

    print(f"\n[1/5] Loading fixtures from {FIXTURES_DIR}")
    fixtures = load_fixtures(max_n=sample)
    print(f"  Loaded {len(fixtures)} AA+A charts")

    print("\n[2/5] Building outcome labels")
    labels = build_labels(fixtures)

    print("\n[3/5] Scoring with OLD engine (OB-3 baseline)")
    old_scores = score_old(fixtures, verbose=verbose)

    print("\n[4/5] Scoring with NEW pipeline (convergence + temporal)")
    conv_scores, total_scores = score_new(fixtures, verbose=verbose)

    print("\n[5/5] Computing Spearman correlations")
    print()
    print(f"  {'House':>5}  {'Category':<42}  {'OLD ρ':>7}  {'CONV ρ':>7}  {'TOTAL ρ':>7}  {'Winner':>8}")
    print(f"  {'─'*5}  {'─'*42}  {'─'*7}  {'─'*7}  {'─'*7}  {'─'*8}")

    results = []
    for (house, cat), label_vals in sorted(labels.items()):
        old_vals = [s.get(house, float("nan")) for s in old_scores]
        conv_vals = [s.get(house, float("nan")) for s in conv_scores]
        total_vals = [s.get(house, float("nan")) for s in total_scores]

        rho_old = spearman(old_vals, label_vals)
        rho_conv = spearman(conv_vals, label_vals)
        rho_total = spearman(total_vals, label_vals)

        # Determine winner
        rhos = {"OLD": rho_old, "CONV": rho_conv, "TOTAL": rho_total}
        valid = {k: v for k, v in rhos.items() if v == v}  # filter NaN
        winner = max(valid, key=lambda k: abs(valid[k])) if valid else "N/A"

        results.append({
            "house": house, "category": cat,
            "rho_old": round(rho_old, 4) if rho_old == rho_old else None,
            "rho_conv": round(rho_conv, 4) if rho_conv == rho_conv else None,
            "rho_total": round(rho_total, 4) if rho_total == rho_total else None,
            "winner": winner,
        })

        def fmt(r):
            return f"{r:+.4f}" if r == r else "   N/A"

        print(f"  H{house:02d}    {cat:<42}  {fmt(rho_old)}  {fmt(rho_conv)}  {fmt(rho_total)}  {winner:>8}")

    # House-level summary
    house_old = defaultdict(list)
    house_conv = defaultdict(list)
    house_total = defaultdict(list)
    for r in results:
        if r["rho_old"] is not None:
            house_old[r["house"]].append(r["rho_old"])
        if r["rho_conv"] is not None:
            house_conv[r["house"]].append(r["rho_conv"])
        if r["rho_total"] is not None:
            house_total[r["house"]].append(r["rho_total"])

    print()
    print("  ── House-level summary ──")
    print(f"  {'House':>5}  {'OLD ρ':>7}  {'CONV ρ':>7}  {'TOTAL ρ':>7}  {'Δ(CONV-OLD)':>12}  {'Δ(TOTAL-OLD)':>12}")
    print(f"  {'─'*5}  {'─'*7}  {'─'*7}  {'─'*7}  {'─'*12}  {'─'*12}")

    wins = {"OLD": 0, "CONV": 0, "TOTAL": 0}
    for h in sorted(set(house_old) | set(house_conv) | set(house_total)):
        avg_old = sum(house_old[h]) / len(house_old[h]) if house_old[h] else 0
        avg_conv = sum(house_conv[h]) / len(house_conv[h]) if house_conv[h] else 0
        avg_total = sum(house_total[h]) / len(house_total[h]) if house_total[h] else 0
        delta_conv = avg_conv - avg_old
        delta_total = avg_total - avg_old

        best = max(
            [("OLD", abs(avg_old)), ("CONV", abs(avg_conv)), ("TOTAL", abs(avg_total))],
            key=lambda x: x[1],
        )[0]
        wins[best] += 1

        print(f"  H{h:02d}    {avg_old:+.4f}  {avg_conv:+.4f}  {avg_total:+.4f}  "
              f"{'↑' if delta_conv > 0.005 else ('↓' if delta_conv < -0.005 else '≈')}{delta_conv:+.4f}     "
              f"{'↑' if delta_total > 0.005 else ('↓' if delta_total < -0.005 else '≈')}{delta_total:+.4f}")

    print()
    print(f"  Wins: OLD={wins['OLD']}  CONV={wins['CONV']}  TOTAL={wins['TOTAL']}")
    print()

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    run(sample=args.sample, verbose=not args.quiet)


if __name__ == "__main__":
    main()
