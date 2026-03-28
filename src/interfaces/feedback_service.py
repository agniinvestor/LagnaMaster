"""
src/interfaces/feedback_service.py — S191 Protocol stub

FeedbackService defines the boundary for the feedback/confirmation layer.

Layer III (Empirical Convergence) infrastructure interface.
Phase 3 (S471–S530) builds the concrete implementation with
DPDP/GDPR compliance and convergence-state capture.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class FeedbackService(Protocol):
    """
    Stores and retrieves prediction feedback for empirical calibration.

    The feedback schema is the most irreversible decision in the project.
    It must capture convergence_state at prediction time — not just outcome.
    (See ROADMAP.md Phase 3 critical note.)

    Implementations: Phase 3 (S491–S515) with `user_prior_prob_pre` enforcement.
    """

    def store_feedback(
        self,
        prediction_id: str,
        outcome: bool,
        convergence_state: dict[str, Any],
        user_id: str | None = None,
    ) -> str:
        """
        Store a confirmed or disconfirmed prediction outcome.

        Parameters
        ----------
        prediction_id : str
            Unique ID of the prediction being confirmed/disconfirmed.
        outcome : bool
            True = confirmed, False = disconfirmed.
        convergence_state : dict
            Must include: school_concordance, varga_agreement_grade,
            promise_capacity_delivery status. Required for Layer III Bayesian updates.
        user_id : str | None
            Anonymised user identifier (DPDP/GDPR compliant).

        Returns
        -------
        str
            Stored feedback record ID.
        """
        ...

    def get_feedback(
        self,
        prediction_id: str | None = None,
        user_id: str | None = None,
        min_concordance: float | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retrieve feedback records, optionally filtered.

        Parameters
        ----------
        prediction_id : str | None
            Filter to a specific prediction.
        user_id : str | None
            Filter to a specific user.
        min_concordance : float | None
            Filter to records with concordance >= threshold.

        Returns
        -------
        list[dict]
            Feedback records with convergence_state included.
        """
        ...
