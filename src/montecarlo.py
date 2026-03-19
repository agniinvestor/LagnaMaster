"""
Monte Carlo birth time sensitivity analysis (Session 11).
"""
from __future__ import annotations
import random, statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class HouseSensitivity:
    house: int
    mean_score: float
    std_score: float
    min_score: float
    max_score: float
    score_range: float
    rating_mode: str
    stable: bool


@dataclass
class SensitivityReport:
    n_samples: int
    birth_time_window_minutes: int
    lagna_stability: float
    dominant_lagna: str
    dasha_stability: float
    dominant_md_lord: str
    houses: dict[int, HouseSensitivity]


def _worker(args: tuple) -> dict:
    (year, month, day, hour, lat, lon, tz_offset, ayanamsha, ephe_path,
     birth_date_iso) = args
    from src.ephemeris import compute_chart
    from src.scoring import score_chart
    chart = compute_chart(year=year, month=month, day=day, hour=hour,
                          lat=lat, lon=lon, tz_offset=tz_offset,
                          ayanamsha=ayanamsha, ephe_path=ephe_path)
    scores = score_chart(chart)
    md_lord = "N/A"
    if birth_date_iso:
        try:
            from src.calculations.vimshottari_dasa import compute_vimshottari_dasa, current_dasha
            from datetime import date as _date
            bd = _date.fromisoformat(birth_date_iso)
            dashas = compute_vimshottari_dasa(chart, bd)
            md, _ = current_dasha(dashas)
            md_lord = md.lord
        except Exception:
            pass
    return {
        "lagna_sign": chart.lagna_sign,
        "md_lord": md_lord,
        "house_scores": {h: hs.final_score for h, hs in scores.houses.items()},
        "house_ratings": {h: hs.rating for h, hs in scores.houses.items()},
    }


def compute_sensitivity(
    year: int, month: int, day: int, hour: float,
    lat: float, lon: float,
    tz_offset: float = 5.5, ayanamsha: str = "lahiri",
    ephe_path: Optional[str] = None,
    n_samples: int = 100, window_minutes: int = 30,
    seed: Optional[int] = None,
    birth_date: Optional[date] = None,
    max_workers: int = 4,
) -> SensitivityReport:
    rng = random.Random(seed)
    window_hours = window_minutes / 60.0
    sample_hours = [
        max(0.0, min(23.9999, hour + rng.uniform(-window_hours, window_hours)))
        for _ in range(n_samples)
    ]
    birth_date_iso = birth_date.isoformat() if birth_date else None
    args_list = [
        (year, month, day, h, lat, lon, tz_offset, ayanamsha, ephe_path, birth_date_iso)
        for h in sample_hours
    ]
    original_args = (year, month, day, hour, lat, lon, tz_offset, ayanamsha, ephe_path, birth_date_iso)
    original = _worker(original_args)
    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_worker, a) for a in args_list]
        for f in as_completed(futures):
            results.append(f.result())
    lagna_counts: dict[str, int] = {}
    for r in results:
        lg = r["lagna_sign"]
        lagna_counts[lg] = lagna_counts.get(lg, 0) + 1
    dominant_lagna = max(lagna_counts, key=lambda k: lagna_counts[k])
    n = len(results)
    lagna_stability = lagna_counts.get(original["lagna_sign"], 0) / n if n else 1.0
    md_counts: dict[str, int] = {}
    for r in results:
        ml = r["md_lord"]
        md_counts[ml] = md_counts.get(ml, 0) + 1
    dominant_md = max(md_counts, key=lambda k: md_counts[k]) if md_counts else "N/A"
    if birth_date and original["md_lord"] != "N/A":
        dasha_stability = md_counts.get(original["md_lord"], 0) / n if n else 1.0
    else:
        dasha_stability = 1.0
    houses: dict[int, HouseSensitivity] = {}
    for h in range(1, 13):
        house_scores = [r["house_scores"].get(h, 0.0) for r in results]
        house_ratings = [r["house_ratings"].get(h, "Unknown") for r in results]
        hn = len(house_scores)
        mean = sum(house_scores) / hn if hn else 0.0
        std = statistics.stdev(house_scores) if hn > 1 else 0.0
        mn = min(house_scores) if house_scores else 0.0
        mx = max(house_scores) if house_scores else 0.0
        rating_mode = max(set(house_ratings), key=house_ratings.count) if house_ratings else "Unknown"
        houses[h] = HouseSensitivity(
            house=h, mean_score=round(mean,4), std_score=round(std,4),
            min_score=round(mn,4), max_score=round(mx,4),
            score_range=round(mx-mn,4), rating_mode=rating_mode, stable=std < 0.5,
        )
    return SensitivityReport(
        n_samples=n_samples, birth_time_window_minutes=window_minutes,
        lagna_stability=round(lagna_stability,4), dominant_lagna=dominant_lagna,
        dasha_stability=round(dasha_stability,4), dominant_md_lord=dominant_md,
        houses=houses,
    )
