"""
src/guidance/reflection_prompts.py — Session 88

Converts guidance from declarative to Socratic.
Instead of "this period activates career themes" →
"What feels most significant in your professional life right now?"

Aligned with Jyotish's traditional purpose: self-understanding, not prediction.
"""

from __future__ import annotations

_PROMPTS: dict[str, dict[str, list[str]]] = {
    "career": {
        "Clear passage": [
            "What career opportunities feel most aligned with your values right now?",
            "If this were a particularly clear period for professional decisions, what would you act on?",
        ],
        "Favourable": [
            "What aspects of your work feel most energised lately?",
            "What professional move have you been considering?",
        ],
        "Mixed — lean in": [
            "What's the one professional priority worth focusing on despite the mixed signals?",
            "What would careful, deliberate action look like in your career right now?",
        ],
        "Neutral": [
            "What does your work feel like to you right now — what's working, what isn't?",
            "What professional pattern would you most like to understand better?",
        ],
        "Navigate carefully": [
            "What aspect of your career feels most like it needs patience right now?",
            "Where might slowing down actually serve your long-term professional goals?",
        ],
        "Significant resistance": [
            "What foundation in your professional life would most benefit from strengthening?",
            "What would sustainable, long-term professional growth look like if quick wins aren't available?",
        ],
    },
    "marriage": {
        "Clear passage": [
            "What qualities in your relationships feel most alive right now?"
        ],
        "Neutral": [
            "What patterns in your relationships would you most like to understand?"
        ],
        "Navigate carefully": [
            "Where might more patience or communication support your relationships?"
        ],
    },
    "wealth": {
        "Clear passage": [
            "What financial opportunities feel most aligned with your values?"
        ],
        "Navigate carefully": [
            "What aspect of your financial foundation feels most worth strengthening?"
        ],
    },
    "mind_psychology": {
        "Clear passage": [
            "What feels most settled or clear in your inner life right now?"
        ],
        "Navigate carefully": [
            "What aspect of your emotional life is asking for more gentleness?"
        ],
    },
    "default": {
        "any": [
            "What feels most alive or pressing in this area of your life?",
            "What would you want to understand better about this part of your experience?",
        ],
    },
}


def get_reflection_prompt(domain: str, timing_label: str) -> str:
    """Return a Socratic reflection prompt for the given domain and timing."""
    domain_prompts = _PROMPTS.get(domain, _PROMPTS["default"])
    prompts = (
        domain_prompts.get(timing_label)
        or domain_prompts.get("any")
        or ["What does this area of your life feel like to you right now?"]
    )
    # Rotate based on day of year for variety
    from datetime import date

    idx = date.today().timetuple().tm_yday % len(prompts)
    return prompts[idx]


def get_all_prompts(domain: str) -> list[str]:
    domain_prompts = _PROMPTS.get(domain, _PROMPTS["default"])
    all_p = []
    for ps in domain_prompts.values():
        all_p.extend(ps)
    return all_p
