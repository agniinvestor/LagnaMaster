"""
src/interfaces/adapters/null_feedback.py — S192

NullFeedbackService is the stub adapter for the FeedbackService Protocol.

Stores records in-memory (process lifetime only). Used in development and
tests. Real implementation ships in Phase 3 (S491–S515) with:
  - DPDP/GDPR compliance
  - PostgreSQL persistence
  - convergence_state capture enforcement
  - user_prior_prob_pre field (required for Layer III Bayesian updates)
"""

from __future__ import annotations

import uuid
from typing import Any


class NullFeedbackService:
    """
    In-memory stub implementing the FeedbackService Protocol.

    Phase 3 note: the real implementation must enforce that
    convergence_state includes school_concordance, varga_agreement_grade,
    and promise_capacity_delivery status — these are required for the
    Layer III Bayesian updates in Phase 6 (S746–S760).
    """

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []

    def store_feedback(
        self,
        prediction_id: str,
        outcome: bool,
        convergence_state: dict[str, Any],
        user_id: str | None = None,
    ) -> str:
        record_id = str(uuid.uuid4())
        self._records.append({
            "record_id": record_id,
            "prediction_id": prediction_id,
            "outcome": outcome,
            "convergence_state": convergence_state,
            "user_id": user_id,
        })
        return record_id

    def get_feedback(
        self,
        prediction_id: str | None = None,
        user_id: str | None = None,
        min_concordance: float | None = None,
    ) -> list[dict[str, Any]]:
        records = self._records

        if prediction_id is not None:
            records = [r for r in records if r["prediction_id"] == prediction_id]

        if user_id is not None:
            records = [r for r in records if r.get("user_id") == user_id]

        if min_concordance is not None:
            records = [
                r for r in records
                if r.get("convergence_state", {}).get("school_concordance", 0.0)
                >= min_concordance
            ]

        return list(records)
