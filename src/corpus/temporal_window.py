"""src/corpus/temporal_window.py — Temporal window management (Tier 3, Item 4).

Determines whether a rule's prediction is currently active, expired, or
pending based on the native's current age and the rule's timing_window.

Usage:
    from src.corpus.temporal_window import prediction_status

    status = prediction_status(rule.timing_window, native_age=35)
    # Returns: "active" | "expired" | "pending" | "permanent"
"""
from __future__ import annotations


def prediction_status(timing_window: dict, native_age: float) -> str:
    """Determine if a prediction is active for the native's current age.

    Returns:
        "permanent" — no timing constraint (trait rules)
        "active" — within the prediction window
        "pending" — prediction window hasn't opened yet
        "expired" — prediction window has passed
        "unknown" — timing type not recognized
    """
    if not timing_window:
        return "permanent"

    tw_type = timing_window.get("type", "unspecified")

    if tw_type == "unspecified":
        return "permanent"

    if tw_type == "age":
        target_age = timing_window.get("value", 0)
        precision = timing_window.get("precision", "approximate")
        window = 2.0 if precision == "exact" else 5.0
        if native_age < target_age - window:
            return "pending"
        if native_age > target_age + window:
            return "expired"
        return "active"

    if tw_type == "age_range":
        values = timing_window.get("value", [0, 0])
        if len(values) != 2:
            return "unknown"
        low, high = values[0], values[1]
        window = 2.0
        if native_age < low - window:
            return "pending"
        if native_age > high + window:
            return "expired"
        return "active"

    if tw_type == "dasha_period":
        # Dasha activation requires chart computation — return "active"
        # and let the dasha engine determine if the period is running
        return "active"

    if tw_type == "after_event":
        # Event-based timing cannot be determined from age alone
        return "active"

    return "unknown"


def is_rule_active(timing_window: dict, native_age: float) -> bool:
    """Convenience: is this rule's prediction currently active?"""
    status = prediction_status(timing_window, native_age)
    return status in ("active", "permanent")
