"""
src/guidance/educational_layer.py — Session 87

"Learn" mode: explains HOW each factor arises in plain language.
Connected to rule_interaction.py and narrative.py.
Never shows raw scores — shows causes and classical reasoning.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class EducationalExplanation:
    topic: str
    plain_explanation: str
    classical_source: str
    example: str


_EXPLANATIONS = {
    "Jupiter_kendra": EducationalExplanation(
        topic="Jupiter in a kendra house",
        plain_explanation=(
            "Jupiter (Guru) in a kendra house — 1st, 4th, 7th, or 10th from your Lagna — "
            "is one of the most stabilising and expansive positions in Vedic Jyotish. "
            "Kendras are the pillars of the chart. Jupiter here brings wisdom and "
            "protective qualities to the entire chart."
        ),
        classical_source="BPHS Ch.34 — Yogakaraka and kendra placement",
        example="A person with Jupiter in the 1st house often exhibits natural wisdom and tends to attract good counsel.",
    ),
    "benefic_aspect": EducationalExplanation(
        topic="A benefic planet aspects your house",
        plain_explanation=(
            "Natural benefics — Jupiter, Venus, well-associated Mercury, and waxing Moon — "
            "strengthen any house they aspect. In Parashari Jyotish, Jupiter aspects "
            "the 5th and 9th from its position (in addition to the 7th). Venus and Mercury "
            "cast a full 7th aspect. These aspects bring supportive energy to the houses they touch."
        ),
        classical_source="BPHS Ch.26 — Graha Drishti (planetary aspects)",
        example="Jupiter in the 4th house aspects the 8th, 10th, and 12th, bringing its expansive quality there.",
    ),
    "dasha_activation": EducationalExplanation(
        topic="Your current planetary period",
        plain_explanation=(
            "Vimshottari Dasha is a 120-year cycle of planetary periods. Each planet rules "
            "a period (Mahadasha) lasting 6–20 years, then passes to the next. Within each "
            "Mahadasha, there are sub-periods (Antardasha) lasting months to a few years. "
            "The houses ruled and occupied by the active Dasha lord become especially significant."
        ),
        classical_source="BPHS Ch.46 — Vimshottari Dasha",
        example="During a Jupiter Mahadasha, houses ruled by Jupiter and Jupiter's natal position become focal points of life events.",
    ),
    "upachaya": EducationalExplanation(
        topic="Upachaya houses (3rd, 6th, 10th, 11th)",
        plain_explanation=(
            "The upachaya houses — 3rd, 6th, 10th, and 11th from the Lagna — are "
            "'improving houses'. They grow stronger with time and effort. Interestingly, "
            "malefic planets in these houses often produce better results than benefics, "
            "because they provide the friction needed for growth and competition."
        ),
        classical_source="BPHS Ch.7 — House classifications",
        example="A person with Saturn in the 11th house (upachaya) often sees their network and gains improve significantly in later life.",
    ),
    "varga_agreement": EducationalExplanation(
        topic="Multiple divisional charts agree",
        plain_explanation=(
            "Your main chart (D1) shows physical-world patterns. The D9 (Navamsha) shows "
            "the soul-level and marriage. The D10 (Dashamsha) shows career and social role. "
            "When all three point in the same direction for a given area of life, confidence "
            "in the interpretation is highest. When they diverge, the picture is more nuanced."
        ),
        classical_source="BPHS Ch.6 — Divisional charts",
        example="If D1, D9, and D10 all show a challenged 7th house, relationship patterns are more consistently indicated than if only D1 shows this.",
    ),
}


def explain_factor(factor_key: str) -> EducationalExplanation | None:
    return _EXPLANATIONS.get(factor_key)


def available_topics() -> list[str]:
    return list(_EXPLANATIONS.keys())


def get_educational_content(domain: str) -> list[EducationalExplanation]:
    """Return relevant educational explanations for a given domain."""
    domain_topics = {
        "career": ["dasha_activation", "upachaya", "varga_agreement"],
        "marriage": ["benefic_aspect", "varga_agreement", "dasha_activation"],
        "wealth": ["upachaya", "benefic_aspect", "dasha_activation"],
        "health_longevity": ["benefic_aspect", "dasha_activation"],
        "mind_psychology": ["benefic_aspect", "dasha_activation"],
        "spirituality": ["Jupiter_kendra", "varga_agreement"],
        "default": ["dasha_activation", "benefic_aspect"],
    }
    topics = domain_topics.get(domain, domain_topics["default"])
    return [e for t in topics if (e := _EXPLANATIONS.get(t))]
