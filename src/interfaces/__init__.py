"""
Protocol definitions for service boundaries in LagnaMaster.
All later microservices must implement these interfaces exactly.
"""
from .classical_engine import ClassicalEngine
from .dasha_engine import DashaEngine
from .feedback_service import FeedbackService
from .ml_service import MLService

__all__ = [
    "ClassicalEngine",
    "DashaEngine",
    "FeedbackService",
    "MLService",
]
