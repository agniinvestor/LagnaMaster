"""
src/guidance/fatalism_filter.py — Session 72

Scans all generated text for deterministic or catastrophising language
and rewrites using possibility framing.

NOT whitewashing: signal direction is preserved.
"Significant resistance" stays. "Financial ruin" becomes "financial caution advised".

Pattern types:
  Outcome certainty  → outcome tendency
  Permanence         → period-bound
  Catastrophe        → challenge
  Fatalism           → agency
"""
from __future__ import annotations
import re

# (pattern, replacement) — order matters, most specific first
_REWRITES = [
    # Catastrophic outcomes
    (r"\bfinancial ruin\b",         "a period requiring financial caution"),
    (r"\bhealth crisis\b",          "a period warranting health attention"),
    (r"\bmarital ruin\b",           "relational challenges"),
    (r"\bcareer destruction\b",     "significant career navigation"),
    (r"\btotal loss\b",             "meaningful setbacks"),
    (r"\bcomplete failure\b",       "significant obstacles"),
    (r"\bno hope\b",                "a need for patience and strategy"),
    # Deterministic outcome words
    (r"\bwill definitely fail\b",   "may face resistance"),
    (r"\bwill fail\b",              "may encounter obstacles"),
    (r"\bwill suffer\b",            "may navigate challenges"),
    (r"\bwill be destroyed\b",      "may face significant disruption"),
    (r"\bwill be ruined\b",         "may encounter serious setbacks"),
    (r"\bcertain to\b",             "may be likely to"),
    (r"\bguaranteed to\b",          "tends to"),
    (r"\bdoomed to\b",              "at risk of — preparation can help with"),
    (r"\binevitably\b",             "in many cases"),
    (r"\bcannot escape\b",          "may find it challenging to avoid"),
    # Permanence words
    (r"\bnever recover\b",          "face a slow recovery requiring patience"),
    (r"\bnever succeed\b",          "face significant headwinds in this area"),
    (r"\balways struggle\b",        "tend to navigate challenges here"),
    (r"\bpermanently damaged\b",    "significantly affected in this period"),
    # Astrological fatalism phrases
    (r"\bdeath indicated\b",        "significant life transition themes present"),
    (r"\bsevere affliction\b",      "meaningful challenges present"),
    (r"\bdamaged beyond repair\b",  "significantly challenged"),
    (r"\bhopeless\b",               "requiring patience and strategy"),
    (r"\bdoomed\b",                 "facing meaningful obstacles"),
    # Softening severe negative templates
    (r"severely weak",              "requiring focused attention"),
    (r"severely damaged",           "significantly challenged"),
    (r"severely afflicted",         "meaningfully challenged"),
    (r"severely negative",          "carrying significant resistance"),
]

_FLAGS = re.IGNORECASE

def filter_output(text: str) -> str:
    """Apply all fatalism rewrites to a text string."""
    for pattern, replacement in _REWRITES:
        text = re.sub(pattern, replacement, text, flags=_FLAGS)
    return text


def is_safe(text: str) -> bool:
    """Check if text contains any fatalistic language."""
    for pattern, _ in _REWRITES:
        if re.search(pattern, text, flags=_FLAGS):
            return False
    return True


def flag_patterns(text: str) -> list[str]:
    """Return list of fatalistic patterns found in text."""
    found = []
    for pattern, _ in _REWRITES:
        if re.search(pattern, text, flags=_FLAGS):
            found.append(pattern)
    return found
