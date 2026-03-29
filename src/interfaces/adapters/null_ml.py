"""
src/interfaces/adapters/null_ml.py — S192

NullMLService is the stub adapter for the MLService Protocol.

Returns zeroed/stub predictions. Real implementation ships in Phase 6
(S701–S730) after OSF pre-registration (S461 gate — must precede any
live prediction use).

IMPORTANT: ML predictions cannot be used in production until the OSF
pre-registration is filed. This stub ensures call sites compile and
the interface is wired correctly, but never returns real predictions.
"""

from __future__ import annotations

from typing import Any


_CALIBRATION_VERSION = "null-0.0.0"


class NullMLService:
    """
    No-op stub implementing the MLService Protocol.

    Always returns:
      predict()   → probability=0.5 (maximum uncertainty), updated=False
      calibrate() → updated=False, n_events_used=0

    Phase 6 replacement will use XGBoost + SHAP with HDBSCAN chart clustering.
    See ROADMAP.md Phase 6 (S701–S790) and PREDICTION_PIPELINE.md Layer III.
    """

    def predict(
        self,
        chart_features: dict[str, Any],
        house: int,
        concordance_state: dict[str, float],
    ) -> dict[str, Any]:
        """
        Stub: returns maximum-uncertainty prediction.

        Real implementation requires OSF pre-registration before use (G22).
        """
        return {
            "probability": 0.5,
            "confidence_interval": (0.0, 1.0),
            "shap_values": {},
            "brier_score": None,
            "note": "NullMLService — real predictions require Phase 6 (S701+) and OSF pre-reg (G22)",
        }

    def calibrate(
        self,
        feedback_records: list[dict[str, Any]],
        min_events: int = 1000,
    ) -> dict[str, Any]:
        """
        Stub: no-op calibration. Returns updated=False always.

        Real implementation requires >= 1,000 confirmed events (S746).
        """
        return {
            "updated": False,
            "n_events_used": 0,
            "calibration_version": _CALIBRATION_VERSION,
            "note": f"NullMLService — {len(feedback_records)} events received, "
                    f"{min_events} required to trigger update",
        }
