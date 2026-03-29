"""
src/calculations/house_score.py — Session 193

HouseScore distribution dataclass: replaces bare float in house-score dicts.

Each house score now carries a point estimate *plus* a distribution summary
(mean, std, p10, p90) derived from birth-time uncertainty propagation.

Public API
----------
  HouseScore                          — dataclass
  compute_house_scores(chart)         — dict[int, HouseScore]

Source
------
  Birth-time uncertainty: Hart de Fouw & Robert Svoboda · Light on Life, App on Research
  Percentile derivation: normal-distribution approximation (std from 95 % CI width)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HouseScore:
    """
    House score with distribution parameters.

    Invariant: p10 <= mean <= p90
    """

    house: int
    score: float   # point estimate (same as mean by construction)
    mean: float    # distribution mean
    std: float     # standard deviation (>= 0)
    p10: float     # 10th percentile
    p90: float     # 90th percentile

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict of all fields."""
        return {
            "house": self.house,
            "score": self.score,
            "mean": self.mean,
            "std": self.std,
            "p10": self.p10,
            "p90": self.p90,
        }


def _build_house_score(house: int, ci) -> HouseScore:
    """
    Convert a ConfidenceInterval into a HouseScore.

    The CI lower/upper bounds represent approximately a 95 % interval, so:
      std  ≈ half_width / 1.96
      p10  = mean − 1.282 × std
      p90  = mean + 1.282 × std
    """
    mean = ci.point_estimate
    half_width = max(0.0, (ci.upper_bound - ci.lower_bound) / 2.0)
    std = half_width / 1.96 if half_width > 0.0 else 0.0
    z10 = 1.2816  # norm.ppf(0.90) ≈ 1.2816
    p10 = round(mean - z10 * std, 4)
    p90 = round(mean + z10 * std, 4)
    return HouseScore(
        house=house,
        score=round(mean, 4),
        mean=round(mean, 4),
        std=round(std, 4),
        p10=p10,
        p90=p90,
    )


def compute_house_scores(chart, school: str = "parashari") -> dict[int, HouseScore]:
    """
    Compute HouseScore distribution for all 12 houses of *chart*.

    Steps:
      1. Score D1 axis via multi_axis_scoring.score_all_axes()
      2. Propagate birth-time uncertainty via confidence_model
      3. Build HouseScore for each house from the resulting intervals

    Args:
        chart:   BirthChart
        school:  scoring school ("parashari" / "kp" / "jaimini")

    Returns:
        dict[int, HouseScore]  — keys 1 … 12
    """
    from src.calculations.multi_axis_scoring import score_all_axes
    from src.calculations.confidence_model import (
        compute_uncertainty_flags,
        compute_confidence_intervals,
    )

    axes = score_all_axes(chart, school)
    d1_scores: dict[int, float] = dict(axes.d1.scores)

    flags = compute_uncertainty_flags(chart)
    intervals = compute_confidence_intervals(d1_scores, flags)

    result: dict[int, HouseScore] = {}
    for ci in intervals:
        result[ci.house] = _build_house_score(ci.house, ci)

    return result
