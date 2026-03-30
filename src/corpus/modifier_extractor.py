"""src/corpus/modifier_extractor.py — Extract modifiers from rule descriptions.

Applied at build time by combined_corpus.py.
Parses conditional language into structured modifier dicts.
"""
from __future__ import annotations
import re

_MODIFIER_PATTERNS = [
    (r"aspected by (\w+)", lambda m: {"condition": f"aspected_by_{m.group(1).lower()}", "effect": "modifies", "strength": "strong"}),
    (r"aspect of (\w+)", lambda m: {"condition": f"aspected_by_{m.group(1).lower()}", "effect": "modifies", "strength": "strong"}),
    (r"if exalted|when exalted", lambda m: {"condition": "if_exalted", "effect": "amplifies", "strength": "strong"}),
    (r"if debilitated|when debilitated", lambda m: {"condition": "if_debilitated", "effect": "negates", "strength": "strong"}),
    (r"in own sign|own house", lambda m: {"condition": "if_own_sign", "effect": "amplifies", "strength": "moderate"}),
    (r"combust|combustion", lambda m: {"condition": "if_combust", "effect": "negates", "strength": "moderate"}),
    (r"retrograde", lambda m: {"condition": "if_retrograde", "effect": "modifies", "strength": "moderate"}),
    (r"malefic aspect|aspected by malefic", lambda m: {"condition": "malefic_aspect", "effect": "negates", "strength": "strong"}),
    (r"benefic aspect|aspected by benefic", lambda m: {"condition": "benefic_aspect", "effect": "amplifies", "strength": "moderate"}),
    (r"waxing moon|full moon", lambda m: {"condition": "moon_waxing", "effect": "amplifies", "strength": "moderate"}),
    (r"waning moon|new moon|dark moon", lambda m: {"condition": "moon_waning", "effect": "negates", "strength": "moderate"}),
]

_EXCEPTION_PATTERNS = [
    r"unless (\w[\w ]*)",
    r"except when",
    r"cancell?ation|cancelled if",
    r"negated by",
    r"neecha bhanga",
]


def extract_modifiers_from_description(description: str) -> tuple[list[dict], list[str]]:
    """Extract structured modifiers and exceptions from a rule description.

    Returns (modifiers: list[dict], exceptions: list[str]).
    """
    desc = description.lower()
    modifiers: list[dict] = []
    exceptions: list[str] = []

    for pattern, builder in _MODIFIER_PATTERNS:
        match = re.search(pattern, desc)
        if match:
            mod = builder(match)
            if mod not in modifiers:
                modifiers.append(mod)

    for pattern in _EXCEPTION_PATTERNS:
        match = re.search(pattern, desc)
        if match:
            exc = match.group(0).strip()
            if exc not in exceptions:
                exceptions.append(exc)

    return modifiers, exceptions
