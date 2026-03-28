"""
src/interfaces/adapters — Concrete adapter implementations of the Protocol interfaces.

S192: Module boundary formalization. Each adapter wraps an existing calculation
module and satisfies its corresponding Protocol via @runtime_checkable isinstance.

Phase 9 strangler-fig: swap concrete adapters for microservice clients without
changing any call site that programs to the Protocol interface.
"""

from .dasha_engine import VimshottariDasaAdapter
from .null_feedback import NullFeedbackService
from .null_ml import NullMLService
from .scoring_engine import ScoringEngineAdapter

__all__ = [
    "ScoringEngineAdapter",
    "VimshottariDasaAdapter",
    "NullFeedbackService",
    "NullMLService",
]
