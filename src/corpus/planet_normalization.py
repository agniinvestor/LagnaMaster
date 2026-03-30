"""src/corpus/planet_normalization.py — Canonical planet name mapping.

Ensures consistent planet naming across all corpus rules.
Conjunction pairs are always alphabetically sorted: jupiter_mars not mars_jupiter.
"""
from __future__ import annotations

CANONICAL_PLANETS = frozenset({
    "sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn",
    "rahu", "ketu",
})

# Non-planet values that are valid in primary_condition.planet
VALID_NON_PLANETS = frozenset({
    "house_lord", "general", "none", "nodes",
})

# Compound planet names (conjunctions, multi-planet)
COMPOUND_PREFIXES = frozenset({
    "three_planet", "four_planet", "five_planet", "six_planet", "seven_planet",
    "stellium", "combustion", "gandanta", "graha_yuddha", "nodal",
    "retrograde", "sandhi",
})


def normalize_planet_name(name: str) -> str:
    """Normalize a planet name to canonical form.

    - Lowercase
    - Conjunction pairs sorted alphabetically: mars_jupiter not jupiter_mars
    - Compound labels preserved as-is
    """
    name = name.lower().strip()

    if name in CANONICAL_PLANETS or name in VALID_NON_PLANETS:
        return name

    # Check if it is a compound label
    for prefix in COMPOUND_PREFIXES:
        if name.startswith(prefix):
            return name

    # Check if it is a conjunction pair (two planets joined by _)
    parts = name.split("_")
    if len(parts) == 2 and all(p in CANONICAL_PLANETS for p in parts):
        return "_".join(sorted(parts))

    # Three-planet conjunctions
    if len(parts) == 3 and all(p in CANONICAL_PLANETS for p in parts):
        return "_".join(sorted(parts))

    # Unknown — return as-is
    return name


def is_valid_planet_name(name: str) -> bool:
    """Check if a planet name is in canonical form."""
    normalized = normalize_planet_name(name)
    return normalized == name
