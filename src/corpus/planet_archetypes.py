"""Central planet archetype registry — single source of truth for nature + themes."""
from __future__ import annotations

PLANET_ARCHETYPES: dict[str, dict] = {
    "Sun":     {"nature": "malefic", "themes": ["authority", "father", "soul", "government"]},
    "Moon":    {"nature": "benefic", "themes": ["mind", "mother", "emotions", "public"]},
    "Mars":    {"nature": "malefic", "themes": ["energy", "courage", "siblings", "property"]},
    "Mercury": {"nature": "benefic", "themes": ["intellect", "speech", "commerce", "adaptability"]},
    "Jupiter": {"nature": "benefic", "themes": ["wisdom", "children", "dharma", "expansion"]},
    "Venus":   {"nature": "benefic", "themes": ["luxury", "spouse", "art", "pleasure"]},
    "Saturn":  {"nature": "malefic", "themes": ["delay", "discipline", "karma", "longevity"]},
    "Rahu":    {"nature": "malefic", "themes": ["obsession", "foreign", "unconventional", "amplification"]},
    "Ketu":    {"nature": "malefic", "themes": ["detachment", "spirituality", "past_karma", "loss"]},
}
