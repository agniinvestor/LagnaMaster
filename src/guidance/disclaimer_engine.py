"""
src/guidance/disclaimer_engine.py — Session 75

Domain-specific scope disclaimers + dependency prevention nudges.
Prevents the system from presenting itself outside its defined scope.
"""
from __future__ import annotations
from datetime import datetime, date

_DISCLAIMERS = {
    "career":          ("This is reflective guidance inspired by Jyotish principles. "
                        "It is not financial or career advice. Professional guidance is recommended for major decisions."),
    "wealth":          ("This is reflective guidance inspired by Jyotish principles. "
                        "It is not financial advice. Please consult a qualified financial professional."),
    "health_longevity":("This is reflective guidance only. It is not medical advice. "
                        "Please consult a qualified medical professional for health decisions."),
    "marriage":        ("This is reflective guidance inspired by Jyotish principles. "
                        "It is not relationship counselling. Professional support is available if needed."),
    "mind_psychology": ("This is reflective guidance only. "
                        "For mental health support, please speak with a qualified professional."),
    "spirituality":    ("This guidance is offered in the spirit of Jyotish as self-understanding. "
                        "It reflects one interpretive tradition among many."),
    "default":         ("This is reflective guidance inspired by Jyotish principles. "
                        "It is not professional advice of any kind. Use it to support, not replace, your own judgment."),
}

_DEPENDENCY_NUDGE = (
    "Guidance works best when combined with your own judgment and trusted advisors. "
    "This tool supports reflection — it does not make decisions for you."
)

_OVERUSE_NUDGE = (
    "You've been checking in frequently. That's completely natural. "
    "For best results, use this guidance as one input among many, "
    "and consider speaking with a trusted person about the areas you're reflecting on."
)


def get_disclaimer(domain: str) -> str:
    return _DISCLAIMERS.get(domain, _DISCLAIMERS["default"])


def should_show_dependency_nudge(session_count_today: int,
                                  session_count_week: int) -> bool:
    """Return True if usage frequency warrants a dependency nudge."""
    return session_count_today >= 3 or session_count_week >= 15


def get_dependency_nudge(overuse: bool = False) -> str:
    return _OVERUSE_NUDGE if overuse else _DEPENDENCY_NUDGE


def append_disclaimer(response_dict: dict, domain: str,
                       session_count_today: int = 0,
                       session_count_week: int = 0) -> dict:
    """Append disclaimer (and optional nudge) to a response dict."""
    response_dict["disclaimer"] = get_disclaimer(domain)
    if should_show_dependency_nudge(session_count_today, session_count_week):
        response_dict["dependency_nudge"] = get_dependency_nudge(
            overuse=(session_count_today >= 5 or session_count_week >= 20)
        )
    return response_dict
