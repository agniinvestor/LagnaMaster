"""
src/feedback/harm_escalation.py — Session 85

Pattern detector on usage signals.
Does NOT intervene automatically. Surfaces a gentle prompt only.
Does NOT provide crisis resources unless explicitly requested by user.
"""

from __future__ import annotations
from dataclasses import dataclass

_NEGATIVE_DOMAINS = {"health_longevity", "mind_psychology"}
_CONCERN_REPEAT_THRESHOLD = 3  # same negative domain in one session
_DAILY_SESSION_HIGH = 5  # sessions suggesting possible compulsion


@dataclass
class EscalationSignal:
    triggered: bool
    severity: str  # "none" | "gentle" | "moderate"
    prompt: str
    show_to_user: bool


def check_usage_pattern(
    domain_views_today: dict[str, int],
    session_count_today: int,
    session_count_week: int,
    recent_ratings: list[str],
) -> EscalationSignal:
    """
    Check if usage patterns suggest the user might benefit from a gentle prompt.
    Returns EscalationSignal — never intervenes automatically.
    """
    # Pattern 1: repeated viewing of negative domains
    neg_domain_count = sum(domain_views_today.get(d, 0) for d in _NEGATIVE_DOMAINS)
    if neg_domain_count >= _CONCERN_REPEAT_THRESHOLD:
        return EscalationSignal(
            triggered=True,
            severity="gentle",
            show_to_user=True,
            prompt=(
                "You've been reflecting on this area quite a bit today. "
                "That's completely natural. Speaking with a trusted person "
                "or counsellor can offer perspectives that complement what's here."
            ),
        )

    # Pattern 2: multiple 'concerning' ratings
    concerning_count = recent_ratings.count("concerning")
    if concerning_count >= 2:
        return EscalationSignal(
            triggered=True,
            severity="moderate",
            show_to_user=True,
            prompt=(
                "We noticed you've flagged some guidance as concerning. "
                "If you're going through a difficult time, speaking with "
                "someone you trust — a friend, counsellor, or professional — "
                "can be really valuable."
            ),
        )

    # Pattern 3: very high session frequency
    if session_count_today >= _DAILY_SESSION_HIGH:
        return EscalationSignal(
            triggered=True,
            severity="gentle",
            show_to_user=True,
            prompt=(
                "You've been checking in frequently today — which is fine. "
                "As a gentle reminder: guidance works best as one input among many. "
                "Your own judgment and trusted advisors are always the primary source."
            ),
        )

    return EscalationSignal(
        triggered=False, severity="none", prompt="", show_to_user=False
    )


def should_show_prompt(signal: EscalationSignal) -> bool:
    return signal.triggered and signal.show_to_user
