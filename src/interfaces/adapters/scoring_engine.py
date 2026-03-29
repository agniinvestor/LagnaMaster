"""
src/interfaces/adapters/scoring_engine.py — S192

ScoringEngineAdapter wraps score_chart_v3() to implement the ClassicalEngine Protocol.

Layer I (Classical Convergence) concrete adapter.
Phase 9 strangler-fig: when the classical scoring layer is extracted to a
microservice, only this file changes — all consumers already use ClassicalEngine.
"""

from __future__ import annotations

import math
from datetime import date
from typing import Any


class ScoringEngineAdapter:
    """
    Concrete implementation of the ClassicalEngine Protocol.

    Wraps:
      score_chart_v3()   — full multi-axis scoring
      score_all_axes()   — per-school D1 scores for concordance computation
    """

    def score_chart(
        self,
        chart: Any,
        dashas: list | None = None,
        on_date: date | None = None,
        school: str = "parashari",
    ) -> Any:
        """
        Compute multi-axis house scores.

        Returns ChartScoresV3 with D1/CL/SL/D9/D10 + LPI + concordance.
        """
        from src.calculations.scoring_v3 import score_chart_v3

        return score_chart_v3(
            chart=chart,
            dashas=dashas or [],
            on_date=on_date,
            school=school,
        )

    def school_concordance(
        self,
        chart: Any,
        house: int,
        on_date: date | None = None,
    ) -> float:
        """
        Compute cross-school concordance for a house.

        Method: score D1 for this house from all three schools (parashari, kp,
        jaimini), normalize each to [0, 1], then compute:

            concordance = max(0.0, 1.0 - normalized_std)

        Interpretation (from PREDICTION_PIPELINE.md):
          < 0.35 → anti-prediction zone (schools genuinely disagree)
          0.35–0.75 → moderate agreement
          ≥ 0.75 → high concordance (prediction-ready signal)

        Returns float in [0.0, 1.0].
        """
        from src.calculations.multi_axis_scoring import score_all_axes

        schools = ("parashari", "kp", "jaimini")
        raw_scores: list[float] = []

        for school in schools:
            try:
                axes = score_all_axes(chart, school=school)
                # D1 score for this house (1-indexed key)
                score = axes.d1.scores.get(house, 0.0)
                raw_scores.append(float(score))
            except Exception:
                # If a school fails (e.g. KP missing ayanamsha), treat as 0
                raw_scores.append(0.0)

        # Normalize each score from [-10, +10] range to [0, 1]
        normalized = [(s + 10.0) / 20.0 for s in raw_scores]

        # Mean and std of normalized values
        mean = sum(normalized) / len(normalized)
        variance = sum((x - mean) ** 2 for x in normalized) / len(normalized)
        std = math.sqrt(variance)

        # Concordance: 1 = perfect agreement, 0 = maximum disagreement
        # Max possible std for [0,1] values ≈ 0.5 (when values are 0,0,1 etc.)
        # We scale std so that a std of 0.5 → concordance of 0.0
        concordance = max(0.0, 1.0 - (std / 0.5))
        return min(1.0, concordance)
