"""Interpretation abstraction layer — annotated output from predictions + context."""
from __future__ import annotations

from src.corpus.planet_archetypes import PLANET_ARCHETYPES


def interpret(prediction: dict, context: dict) -> str:
    """Convert structured prediction + context into annotated output.

    Invariant: no interpretation without context.
    """
    claim = prediction.get("claim", "")
    qualifications = context.get("qualifications", [])
    planet = context.get("trigger_planet", "")
    archetype = PLANET_ARCHETYPES.get(planet, {})

    parts = [claim]
    if qualifications:
        parts.append(f"(qualified by: {', '.join(qualifications)})")
    if archetype.get("themes"):
        parts.append(f"[{planet} themes: {', '.join(archetype['themes'][:2])}]")

    return " ".join(parts)
