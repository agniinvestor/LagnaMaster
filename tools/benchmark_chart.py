#!/usr/bin/env python3
"""tools/benchmark_chart.py — D21: Per-layer timing benchmark for a single chart.

Computes the India 1947 chart and measures each pipeline layer separately.
Runs 5 iterations, reports median per-layer.

Usage:
    .venv/bin/python tools/benchmark_chart.py
"""

from __future__ import annotations

import statistics
import sys
import time
from datetime import date
from pathlib import Path

# Ensure project root is on sys.path so 'src' is importable
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Chart parameters — India 1947
# ---------------------------------------------------------------------------
PARAMS = dict(year=1947, month=8, day=15, hour=0.0,
              lat=28.6139, lon=77.2090, tz_offset=5.5)
BIRTH_DATE = date(1947, 8, 15)
ITERATIONS = 5
TARGET_MS = 200  # Q9 target (advisory — report only)


def _time_fn(fn, *args, **kwargs):
    """Run fn once, return (elapsed_seconds, result)."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    return elapsed, result


def run_benchmark():
    # Import inside function to avoid polluting timing with import overhead
    from src.ephemeris import compute_chart
    from src.calculations.chart_context import build_chart_context
    from src.calculations.unified_engine import evaluate_all_rules
    from src.calculations.convergence import converge
    from src.calculations.temporal_projection import time_project
    from src.scoring import score_chart

    layer_names = [
        "1. compute_chart (astronomy)",
        "2. build_chart_context (derived)",
        "3. evaluate_all_rules (engine)",
        "4. converge (convergence)",
        "5. time_project (temporal)",
        "TOTAL end-to-end",
    ]
    # Collect timings: layer_times[layer_index] = list of elapsed_ms
    layer_times: dict[int, list[float]] = {i: [] for i in range(len(layer_names))}

    # Warm-up run (not counted) — ensures imports/caches are primed
    chart = compute_chart(**PARAMS)
    ctx = build_chart_context(chart, birth_date=BIRTH_DATE)
    _ = score_chart(chart, ctx=ctx)
    unified = evaluate_all_rules(ctx, school="parashari")
    conv = converge(unified.results, ctx)
    _ = time_project(conv, ctx, birth_date=BIRTH_DATE)

    for i in range(ITERATIONS):
        # Layer 1
        t1, chart = _time_fn(compute_chart, **PARAMS)

        # Layer 2
        t2, ctx = _time_fn(build_chart_context, chart, birth_date=BIRTH_DATE)

        # Layer 3
        t3, unified = _time_fn(evaluate_all_rules, ctx, school="parashari")

        # Layer 4
        t4, conv = _time_fn(converge, unified.results, ctx)

        # Layer 5
        t5, timed = _time_fn(time_project, conv, ctx, birth_date=BIRTH_DATE)

        total = t1 + t2 + t3 + t4 + t5

        layer_times[0].append(t1 * 1000)
        layer_times[1].append(t2 * 1000)
        layer_times[2].append(t3 * 1000)
        layer_times[3].append(t4 * 1000)
        layer_times[4].append(t5 * 1000)
        layer_times[5].append(total * 1000)

    # Compute medians
    medians = {i: statistics.median(layer_times[i]) for i in range(len(layer_names))}

    # Print table
    print()
    print("=" * 60)
    print("  D21: Per-Layer Benchmark (India 1947 chart)")
    print(f"  Iterations: {ITERATIONS} | Median timing")
    print("=" * 60)
    print(f"  {'Layer':<40s} {'Median (ms)':>10s}")
    print("-" * 60)
    for i, name in enumerate(layer_names):
        marker = " *" if i == len(layer_names) - 1 else ""
        print(f"  {name:<40s} {medians[i]:>10.2f}{marker}")
    print("-" * 60)
    print()

    total_median = medians[len(layer_names) - 1]
    if total_median > TARGET_MS:
        print(f"  NOTE: Total {total_median:.1f}ms exceeds {TARGET_MS}ms target")
        print("  (Pipeline includes 5 layers — target is advisory)")
    else:
        print(f"  Total {total_median:.1f}ms is within {TARGET_MS}ms target")
    print()

    # Exit with error if over target (advisory)
    if total_median > TARGET_MS:
        sys.exit(1)


if __name__ == "__main__":
    run_benchmark()
