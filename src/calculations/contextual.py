"""
src/calculations/contextual.py — Session 99

Contextual interpretation layer (partial Desha-Kala-Patra).

What IS encodable:
  - Era-aware profession/activity mapping (king → CEO, minister → politician)
  - Geographic latitude effect on house strengths
  - Cultural context flags for marriage timing interpretation
  - Birth-time precision sensitivity (already in confidence model)

What is NOT encodable (acknowledged):
  - Practitioner situational judgment ("patra" — the individual's context)
  - Social class, family background, karma context
  - Full "era" adjustment for all classical results

PVRNR on DKP: "rules are guidelines, exact application requires
the astrologer's knowledge" (p458).
"""
from __future__ import annotations
from dataclasses import dataclass

# Modern era profession mapping from classical planetary/house combinations
# "King" → "Leader/CEO/Politician" etc.
_ERA_PROFESSION_MAP = {
    # (Primary planet, Key house): (Classical result, Modern equivalent)
    ("Sun",   10): ("King, administrator",     "CEO, government official, leader"),
    ("Moon",  10): ("Trader, public figure",   "Merchant, media personality, public servant"),
    ("Mars",  10): ("Soldier, warrior",        "Athlete, military, surgeon, engineer"),
    ("Mercury",10):("Scholar, minister",       "Analyst, writer, teacher, communicator"),
    ("Jupiter",10):("Counselor, priest",       "Advisor, educator, judge, spiritual teacher"),
    ("Venus", 10): ("Artist, luxury trader",  "Designer, entertainer, luxury industry"),
    ("Saturn", 10):("Worker, servant",        "Service industry, labor, discipline-based work"),
    ("Sun",   2):  ("Wealthy from authority", "Income from leadership or government"),
    ("Jupiter",5): ("Learned, children-blessed","Academic achievement, progeny"),
}

# Latitude adjustments: higher latitudes affect house strength calculations
# Ascendant rises at different speeds — simplified flag
_HIGH_LATITUDE_FLAG = 55.0  # above this, house boundaries diverge significantly


@dataclass
class ContextualFlags:
    era_profession_hints: list[str]
    high_latitude_warning: bool
    cultural_marriage_note: str
    precision_sensitivity: str
    practitioner_note: str


def compute_contextual_flags(chart, lat: float = 28.0,
                              birth_year: int = 1980) -> ContextualFlags:
    """Generate contextual interpretation flags."""
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    # Era profession mapping
    profession_hints = []
    for (planet, house), (classical, modern) in _ERA_PROFESSION_MAP.items():
        if ph.get(planet, 0) == house:
            profession_hints.append(
                f"{planet} in H{house}: Classical = '{classical}' → "
                f"Modern context: '{modern}'"
            )

    # Geographic warning
    high_lat = abs(lat) > _HIGH_LATITUDE_FLAG

    # Cultural marriage note (era-aware)
    if birth_year < 1960:
        marriage_note = "Classical marriage age expectations apply (earlier unions common)"
    elif birth_year < 2000:
        marriage_note = "Modern context: marriage timing spans wider range; D9 themes still apply"
    else:
        marriage_note = "Contemporary context: partnership forms vary; focus on D9 and 7th house themes"

    precision_note = (
        "Birth time within ±5 minutes: high lagna precision. "
        "±15 minutes: lagna may shift 1 sign — confidence flags apply. "
        "Unknown birth time: Moon-based analysis preferred over lagna-based."
    )

    return ContextualFlags(
        era_profession_hints=profession_hints,
        high_latitude_warning=high_lat,
        cultural_marriage_note=marriage_note,
        precision_sensitivity=precision_note,
        practitioner_note=(
            "Full Desha-Kala-Patra (geographic/cultural/era context) requires "
            "a Jyotish practitioner who knows the individual's circumstances. "
            "This layer provides partial algorithmic context flags only."
        ),
    )
