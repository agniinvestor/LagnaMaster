"""src/pipeline.py — Full prediction pipeline entry point.

Runs the complete chain: astronomy → context → rules → convergence → timing.
This is the PRODUCTION entry point for the new architecture (G1–G6).

Usage (Python):
    from src.pipeline import run_pipeline, PipelineResult
    result = run_pipeline(year=1985, month=3, day=15, hour=10.5,
                          lat=28.61, lon=77.21, tz_offset=5.5)
    for p in result.predictions[:5]:
        print(f"H{p.house} {p.direction} conv={p.convergence_score} peak={p.peak_window}")

Usage (CLI):
    .venv/bin/python -m src.pipeline 1985 3 15 10.5 28.61 77.21 5.5
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from src.calculations.chart_context import ChartContext, build_chart_context
from src.calculations.convergence import ConvergedPrediction, converge
from src.calculations.temporal_projection import TimedPrediction, time_project
from src.calculations.unified_engine import UnifiedResult, evaluate_all_rules
from src.calculations.weight_store import VersionInfo
from src.ephemeris import BirthChart, compute_chart
from src.scoring import ChartScores, score_chart


@dataclass
class PipelineResult:
    """Complete pipeline output — scores + predictions + timing + versions."""

    # Layer 1: chart
    chart: BirthChart

    # Layer 2: shared context
    ctx: ChartContext

    # Legacy scoring (existing API consumers need this)
    scores: ChartScores

    # Layer 3: unified rule evaluation
    unified: UnifiedResult

    # Layer 4+5: convergence + timing
    predictions: list[TimedPrediction]

    # Reproducibility (Q6)
    version: VersionInfo

    @property
    def converged(self) -> list[ConvergedPrediction]:
        """Intermediate convergence (before temporal overlay)."""
        return converge(self.unified.results, self.ctx)


def run_pipeline(
    *,
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float,
    ayanamsha: str = "lahiri",
    school: str = "parashari",
) -> PipelineResult:
    """Run the full prediction pipeline end-to-end.

    Computes: chart → context → scores → unified rules → convergence → timing.
    Returns everything in a single PipelineResult.
    """
    birth_date = date(year, month, day)

    # Layer 1: Astronomy
    chart = compute_chart(
        year=year, month=month, day=day, hour=hour,
        lat=lat, lon=lon, tz_offset=tz_offset,
        ayanamsha=ayanamsha,
    )

    # Layer 2: Shared context (G1)
    ctx = build_chart_context(chart, birth_date=birth_date)

    # Legacy scoring (uses ctx internally now via D0c)
    scores = score_chart(chart, ctx=ctx)

    # Layer 3: Unified rule evaluation (G2+G3)
    unified = evaluate_all_rules(ctx, school=school)

    # Layer 4: Convergence (G5)
    conv = converge(unified.results, ctx)

    # Layer 5: Temporal projection (G6)
    timed = time_project(conv, ctx, birth_date=birth_date)

    return PipelineResult(
        chart=chart,
        ctx=ctx,
        scores=scores,
        unified=unified,
        predictions=timed,
        version=unified.version,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    import sys

    if len(sys.argv) < 8:
        print("Usage: python -m src.pipeline YEAR MONTH DAY HOUR LAT LON TZ_OFFSET")
        print("Example: python -m src.pipeline 1947 8 15 0.0 28.6139 77.2090 5.5")
        sys.exit(1)

    year, month, day = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    hour = float(sys.argv[4])
    lat, lon, tz = float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])

    result = run_pipeline(
        year=year, month=month, day=day, hour=hour,
        lat=lat, lon=lon, tz_offset=tz,
    )

    print(f"Chart: {result.chart.lagna_sign} lagna")
    print(f"Version: corpus={result.version.corpus_version[:8]} "
          f"schema={result.version.schema_version} "
          f"weight={result.version.weight_version}")
    print(f"Scoring rules fired: {len(result.unified.scoring_results)}")
    print(f"Corpus rules fired:  {len(result.unified.corpus_results)}")
    print(f"Predictions: {len(result.predictions)}")
    print()

    for h in range(1, 13):
        s = result.scores.houses[h]
        print(f"  H{h:2d} ({s.domain:12s}): score={s.final_score:+.2f}  rating={s.rating}")
    print()

    print("Top converged predictions:")
    for p in result.predictions[:10]:
        systems = list({w.system for w in p.contributing_systems})
        print(f"  H{p.house:2d} {p.direction:12s}  "
              f"conv={p.convergence_score} contra={p.contra_score}  "
              f"peak={p.peak_window}  conf={p.timing_confidence:.2f}  "
              f"strength={p.strength_label}  systems={systems}")


if __name__ == "__main__":
    _cli()
