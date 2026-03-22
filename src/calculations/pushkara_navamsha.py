"""Pushkara Navamsha — 24 auspicious navamsha zones (Session 11)."""

from __future__ import annotations  # noqa: E402

_NAVAMSHA_WIDTH: float = 10.0 / 3.0
_PUSHKARA_STARTS: dict = {
    0: (18 + 20 / 60, 25.0),
    1: (3 + 20 / 60, 28 + 20 / 60),
    2: (13 + 20 / 60, 25.0),
    3: (1 + 40 / 60, 25.0),
    4: (11 + 40 / 60, 19 + 10 / 60),
    5: (23 + 20 / 60, 28 + 20 / 60),
    6: (0.0, 23 + 20 / 60),
    7: (19 + 10 / 60, 28 + 20 / 60),
    8: (5.0, 23 + 20 / 60),
    9: (10.0, 28 + 20 / 60),
    10: (6 + 40 / 60, 25.0),
    11: (13 + 20 / 60, 25.0),
}


def is_pushkara_navamsha(si: int, d: float) -> bool:
    if not (0 <= si <= 11):
        return False
    for s in _PUSHKARA_STARTS[si]:
        if s <= d < s + _NAVAMSHA_WIDTH:
            return True
    return False


def pushkara_navamsha_planets(chart) -> list:
    return [
        n
        for n, p in chart.planets.items()
        if is_pushkara_navamsha(p.sign_index, p.degree_in_sign)
    ]


def pushkara_navamsha_zones(si: int) -> list:
    return [(s, s + _NAVAMSHA_WIDTH) for s in _PUSHKARA_STARTS.get(si, (0.0, 0.0))]


def pushkara_strength_label(si: int, d: float) -> str:
    return "Pushkara Navamsha" if is_pushkara_navamsha(si, d) else ""


# ── MonteCarloResult stub (added by diagnose_and_fix.sh) ──────────────────────
from dataclasses import dataclass  # noqa: E402


@dataclass
class MonteCarloResult:
    base_scores: dict
    mean_scores: dict
    std_scores: dict
    sensitivity: dict
    sample_count: int


def run_monte_carlo(
    year,
    month,
    day,
    hour,
    lat,
    lon,
    tz_offset=5.5,
    ayanamsha="lahiri",
    samples=100,
    window_minutes=30.0,
) -> MonteCarloResult:
    """Synchronous Monte Carlo — runs all samples in the calling thread."""
    import random  # noqa: E402
    import statistics  # noqa: E402
    from src.ephemeris import compute_chart  # noqa: E402
    from src.scoring import score_chart  # noqa: E402

    base = compute_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha)
    base_scores = {h: hs.final_score for h, hs in score_chart(base).houses.items()}
    half = window_minutes / 60.0 / 2.0
    rng = random.Random(42)
    all_scores: dict[int, list[float]] = {h: [] for h in range(1, 13)}

    for _ in range(samples):
        h_sample = max(0.0, min(23.9999, hour + rng.uniform(-half, half)))
        c = compute_chart(year, month, day, h_sample, lat, lon, tz_offset, ayanamsha)
        for h, hs in score_chart(c).houses.items():
            all_scores[h].append(hs.final_score)

    mean_scores = {h: statistics.mean(v) for h, v in all_scores.items()}
    std_scores = {
        h: (statistics.stdev(v) if len(v) > 1 else 0.0) for h, v in all_scores.items()
    }
    sensitivity = {}
    for h, s in std_scores.items():
        sensitivity[h] = "Stable" if s < 0.5 else "Sensitive" if s < 1.5 else "High"

    return MonteCarloResult(
        base_scores=base_scores,
        mean_scores=mean_scores,
        std_scores=std_scores,
        sensitivity=sensitivity,
        sample_count=samples,
    )
