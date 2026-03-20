"""
src/calculations/upaya.py — Session 97

Upaya (Remedial Measures) — classical Jyotish prescriptions.
Source: PVRNR textbook Ch.34 (p450-458), Tables 77-78.

Four classical remedy categories (PVRNR p451-452):
  1. Gemstones   — worn on specific finger, day, metal
  2. Good deeds  — charitable acts aligned with planet's domain
  3. Mantras     — recitation counts per planet (PVRNR p455-458)
  4. Deities     — propitiation of corresponding deity

IMPORTANT: These are classical prescriptions for information only.
Gemstone recommendations require qualified astrologer review.
Health/medical decisions require professional consultation.
This module presents archetypes, not prescriptions.
"""
from __future__ import annotations
from dataclasses import dataclass, field

# PVRNR Table 77: Gemstones
_GEMSTONES = {
    "Sun":     {"gem":"Ruby",              "metal":"Gold",    "finger":"Ring finger",    "day":"Sunday"},
    "Moon":    {"gem":"White Pearl",       "metal":"Gold",    "finger":"Little finger",  "day":"Monday"},
    "Mars":    {"gem":"Red Coral",         "metal":"Copper",  "finger":"Ring finger",    "day":"Tuesday"},
    "Mercury": {"gem":"Emerald",           "metal":"Silver",  "finger":"Little finger",  "day":"Wednesday"},
    "Jupiter": {"gem":"Yellow Sapphire",   "metal":"Gold",    "finger":"Index finger",   "day":"Thursday"},
    "Venus":   {"gem":"Diamond",           "metal":"Silver",  "finger":"Middle finger",  "day":"Friday"},
    "Saturn":  {"gem":"Blue Sapphire",     "metal":"Iron",    "finger":"Middle finger",  "day":"Saturday"},
    "Rahu":    {"gem":"Hessonite (Gomedh)","metal":"Silver",  "finger":"Middle finger",  "day":"Saturday"},
    "Ketu":    {"gem":"Cat's Eye",         "metal":"Silver",  "finger":"Ring finger",    "day":"Tuesday"},
}

# PVRNR Table 78: Deities
_DEITIES = {
    "Sun":     ["Shiva", "Rama"],
    "Moon":    ["Gauri", "Lalita", "Saraswati", "Krishna"],
    "Mars":    ["Hanuman", "Rudra", "Kartikeya (Subrahmanya)", "Narasimha"],
    "Mercury": ["Vishnu", "Narayana", "Buddha"],
    "Jupiter": ["Hayagreeva", "Vishnu", "Parameswara", "Dattatreya"],
    "Venus":   ["Lakshmi", "Parvati"],
    "Saturn":  ["Vishnu", "Brahma"],
    "Rahu":    ["Durga", "Narasimha"],
    "Ketu":    ["Ganesha"],
}

# Mantra recitation counts (PVRNR p455-458)
_MANTRA_COUNTS = {
    "Sun": 6000, "Moon": 10000, "Mars": 7000, "Mercury": 17000,
    "Jupiter": 16000, "Venus": 20000, "Saturn": 19000,
    "Rahu": 18000, "Ketu": 7000,
}

# Good deeds / charitable acts by planet
_CHARITY = {
    "Sun":     "Donate wheat, copper, or red cloth on Sundays; support leadership/authority causes",
    "Moon":    "Donate white items, milk, rice on Mondays; support women or children",
    "Mars":    "Donate red lentils, red cloth on Tuesdays; support firefighters or soldiers",
    "Mercury": {"donate":"Green vegetables, books on Wednesdays; support education or communication"},
    "Jupiter": "Donate yellow items, turmeric, gold on Thursdays; support teachers or scholars",
    "Venus":   "Donate white sweets, white flowers on Fridays; support arts or beauty",
    "Saturn":  "Donate black sesame, iron, oil on Saturdays; support the elderly or poor",
    "Rahu":    "Donate blue items on Saturdays; support the marginalised",
    "Ketu":    "Donate spotted items on Tuesdays; support spiritual seekers",
}

# Domain-specific remedy trigger rules
_AFFLICTION_TRIGGERS = {
    "combust":       "Gemstone and deity of combust planet; charitable acts on planet's day",
    "debilitated":   "Mantra of debilitated planet; worship of its deity",
    "in_dusthana":   "Charitable acts; behavioral correction in planet's domain",
    "functional_malefic": "Propitiate the functional malefic's deity; avoid its day for major starts",
    "8th_lord_strong":    "Shoola dasha caution; longevity practices",
}


@dataclass
class UpayadRecommendation:
    planet: str
    affliction_type: str
    gemstone: str
    gemstone_metal: str
    gemstone_finger: str
    gemstone_day: str
    primary_deity: str
    mantra_count: int
    charitable_act: str
    behavioral_note: str
    disclaimer: str = (
        "These are classical Jyotish prescriptions for reflection only. "
        "Gemstone selection requires a qualified astrologer's individual assessment. "
        "No medical, legal, or financial claim is made."
    )


def get_upaya(planet: str, affliction_type: str = "general") -> UpayadRecommendation:
    """Get classical remedy recommendations for an afflicted planet."""
    gem_data = _GEMSTONES.get(planet, {})
    deities = _DEITIES.get(planet, ["Universal"])
    charity = _CHARITY.get(planet, "Perform acts of service related to this planet's domain")
    if isinstance(charity, dict):
        charity = list(charity.values())[0]

    behavioral = {
        "Sun":     "Respect authority figures; reduce ego; be generous",
        "Moon":    "Be kind to mother and women; maintain emotional balance; drink clean water",
        "Mars":    "Channel energy constructively; avoid aggression; exercise regularly",
        "Mercury": "Speak truth; keep written commitments; engage in learning",
        "Jupiter": "Maintain dharmic conduct; respect teachers; be generous",
        "Venus":   "Cultivate aesthetic sense; maintain purity in relationships",
        "Saturn":  "Be disciplined and patient; serve the elderly; work honestly",
        "Rahu":    "Avoid deception; reduce worldly obsession; practice detachment",
        "Ketu":    "Cultivate spiritual practice; reduce attachment; be selfless",
    }.get(planet, "Perform general acts of dharma")

    return UpayadRecommendation(
        planet=planet, affliction_type=affliction_type,
        gemstone=gem_data.get("gem", "Consult astrologer"),
        gemstone_metal=gem_data.get("metal", ""),
        gemstone_finger=gem_data.get("finger", ""),
        gemstone_day=gem_data.get("day", ""),
        primary_deity=deities[0] if deities else "Universal",
        mantra_count=_MANTRA_COUNTS.get(planet, 1000),
        charitable_act=charity,
        behavioral_note=behavioral,
    )


def get_chart_upayas(chart) -> list[UpayadRecommendation]:
    """Get remedy recommendations for all afflicted planets in a chart."""
    try:
        from src.calculations.dignity import compute_all_dignities
        from src.calculations.functional_roles import compute_functional_roles
        digs = compute_all_dignities(chart)
        fr = compute_functional_roles(chart)
    except Exception:
        return []

    upayas = []
    for planet in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]:
        dig = digs.get(planet)
        affliction = None
        if dig and dig.is_combust and planet != "Sun":
            affliction = "combust"
        elif dig and hasattr(dig, 'level'):
            from src.calculations.dignity import DignityLevel
            try:
                if dig.level == DignityLevel.DEBIL or dig.level == DignityLevel.DEEP_DEBIL:
                    affliction = "debilitated"
            except Exception:
                pass
        if planet in fr.functional_malefics:
            if not affliction:
                affliction = "functional_malefic"

        if affliction:
            upayas.append(get_upaya(planet, affliction))

    return upayas
