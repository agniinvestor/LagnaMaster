"""
src/interfaces/ml_service.py — S191 Protocol stub

MLService defines the boundary for the empirical ML layer.

Layer III (Empirical Convergence) inference interface.
Phase 6 (S701–S790) builds the concrete XGBoost + SHAP implementation.
Must be pre-registered with OSF before first use (S461 gate).
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MLService(Protocol):
    """
    Issues empirically-calibrated predictions from the ML pipeline.

    Implementations: Phase 6 (S701–S730) XGBoost + SHAP, HDBSCAN clustering.

    Critical principle: ML predictions do not replace Layer I classical
    convergence — they calibrate it. See PREDICTION_PIPELINE.md Layer III.
    """

    def predict(
        self,
        chart_features: dict[str, Any],
        house: int,
        concordance_state: dict[str, float],
    ) -> dict[str, Any]:
        """
        Issue an empirically-calibrated prediction for a chart + house.

        Parameters
        ----------
        chart_features : dict
            Feature vector (150+ continuous features after Phase 2).
        house : int
            House number (1–12) being predicted.
        concordance_state : dict
            Current Layer I concordance scores by school — required for
            convergence interaction terms (the novel scientific signal).

        Returns
        -------
        dict with keys:
            probability: float — calibrated posterior probability
            confidence_interval: tuple[float, float]
            shap_values: dict[str, float] — feature attributions
            brier_score: float | None — only after Phase 6 live scoring
        """
        ...

    def calibrate(
        self,
        feedback_records: list[dict[str, Any]],
        min_events: int = 1000,
    ) -> dict[str, Any]:
        """
        Update model weights from confirmed feedback records.

        Bayesian weight updates require >= 1,000 events (S746–S760).
        Below that threshold, returns current calibration state unchanged.

        Parameters
        ----------
        feedback_records : list[dict]
            Feedback records from FeedbackService, with convergence_state.
        min_events : int
            Minimum events required to trigger a weight update.

        Returns
        -------
        dict with keys:
            updated: bool
            n_events_used: int
            calibration_version: str
        """
        ...
