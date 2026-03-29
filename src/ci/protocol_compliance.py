"""
src/ci/protocol_compliance.py — S213: Protocol compliance verification

Checks that all concrete adapter classes satisfy their Protocol interfaces
using runtime isinstance() checks (requires @runtime_checkable Protocols).

Public API
----------
  check_all_protocols() -> dict[str, dict]
      Returns compliance report for all four core Protocols.
"""

from __future__ import annotations


def check_all_protocols() -> dict[str, dict]:
    """
    Verify all Protocol adapters satisfy their interfaces.

    Returns
    -------
    dict mapping protocol name to compliance result:
      {
        "ClassicalEngine": {"compliant": bool, "adapter": str, "error": str},
        "DashaEngine":     {"compliant": bool, "adapter": str, "error": str},
        "FeedbackService": {"compliant": bool, "adapter": str, "error": str},
        "MLService":       {"compliant": bool, "adapter": str, "error": str},
      }
    """
    checks = [
        ("ClassicalEngine", _check_classical_engine),
        ("DashaEngine", _check_dasha_engine),
        ("FeedbackService", _check_feedback_service),
        ("MLService", _check_ml_service),
    ]
    report: dict[str, dict] = {}
    for name, fn in checks:
        try:
            result = fn()
            report[name] = result
        except Exception as exc:
            report[name] = {
                "compliant": False,
                "adapter": "unknown",
                "error": str(exc),
            }
    return report


def _check_classical_engine() -> dict:
    from src.interfaces.classical_engine import ClassicalEngine
    from src.interfaces.adapters.scoring_engine import ScoringEngineAdapter
    adapter = ScoringEngineAdapter()
    return {
        "compliant": isinstance(adapter, ClassicalEngine),
        "adapter": "ScoringEngineAdapter",
        "error": "",
    }


def _check_dasha_engine() -> dict:
    from src.interfaces.dasha_engine import DashaEngine
    from src.interfaces.adapters.dasha_engine import VimshottariDasaAdapter
    adapter = VimshottariDasaAdapter()
    return {
        "compliant": isinstance(adapter, DashaEngine),
        "adapter": "VimshottariDasaAdapter",
        "error": "",
    }


def _check_feedback_service() -> dict:
    from src.interfaces.feedback_service import FeedbackService
    from src.interfaces.adapters.null_feedback import NullFeedbackService
    adapter = NullFeedbackService()
    return {
        "compliant": isinstance(adapter, FeedbackService),
        "adapter": "NullFeedbackService",
        "error": "",
    }


def _check_ml_service() -> dict:
    from src.interfaces.ml_service import MLService
    from src.interfaces.adapters.null_ml import NullMLService
    adapter = NullMLService()
    return {
        "compliant": isinstance(adapter, MLService),
        "adapter": "NullMLService",
        "error": "",
    }
