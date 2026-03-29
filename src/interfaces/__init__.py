"""
Protocol definitions and concrete adapters for service boundaries in LagnaMaster.

S191: Protocol stubs (ClassicalEngine, DashaEngine, FeedbackService, MLService)
S192: Concrete adapters (ScoringEngineAdapter, VimshottariDasaAdapter,
      NullFeedbackService, NullMLService)

Phase 9 strangler-fig: swap adapters for microservice clients without changing
any call site that programs to the Protocol interface.
"""
from .classical_engine import ClassicalEngine
from .dasha_engine import DashaEngine
from .feedback_service import FeedbackService
from .ml_service import MLService
from .adapters import (
    NullFeedbackService,
    NullMLService,
    ScoringEngineAdapter,
    VimshottariDasaAdapter,
)

__all__ = [
    # Protocols
    "ClassicalEngine",
    "DashaEngine",
    "FeedbackService",
    "MLService",
    # Adapters
    "ScoringEngineAdapter",
    "VimshottariDasaAdapter",
    "NullFeedbackService",
    "NullMLService",
]
