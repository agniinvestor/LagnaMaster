"""
src/interfaces/classical_engine.py — S191 Protocol stub

ClassicalEngine defines the boundary between the classical scoring layer
and any consumer (API, UI, ML pipeline, future microservice).

This Protocol enables Phase 9 strangler-fig extraction without rewriting
call sites — every consumer already programs to this interface.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ClassicalEngine(Protocol):
    """
    Computes classical Jyotish scores for a birth chart.

    Layer I (Classical Convergence) interface.
    Implementations: scoring_v3.score_chart_v3 wrapper, VedAstro adapter (S191+).
    """

    def score_chart(
        self,
        chart: Any,
        dashas: list | None = None,
        on_date: Any = None,
        school: str = "parashari",
    ) -> Any:
        """
        Compute multi-axis house scores for a birth chart.

        Parameters
        ----------
        chart : BirthChart
            Computed ephemeris chart (pyswisseph-based).
        dashas : list | None
            Active dasha periods for dasha-sensitized scoring.
        on_date : date | None
            Reference date for transit/dasha-sensitized scoring.
        school : str
            Scoring school — "parashari" | "kp" | "jaimini".

        Returns
        -------
        ChartScoresV3
            Multi-axis scores: D1, CL, SL, D9, D10 + LPI + concordance.
        """
        ...

    def school_concordance(
        self,
        chart: Any,
        house: int,
        on_date: Any = None,
    ) -> float:
        """
        Compute cross-school concordance score for a house.

        Returns
        -------
        float
            Concordance in [0, 1]. Values < 0.35 = anti-prediction zone.
            Values >= 0.75 = high concordance (prediction-ready).
        """
        ...
