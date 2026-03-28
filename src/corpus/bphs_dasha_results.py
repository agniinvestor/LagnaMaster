"""
src/corpus/bphs_dasha_results.py — BPHS Vimshottari Dasha Results (S227)

Encodes dasha result rules from BPHS Ch.46-56.
These rules describe what themes activate during each planet's Maha Dasha
and how house lordship modifies the dasha results.

Sources:
  BPHS Ch.51-53 — Vimshottari dasha general principles
  BPHS Ch.54-56 — Planet-specific dasha results

20 rules. All: implemented=False.
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord
from src.corpus.registry import CorpusRegistry

BPHS_DASHA_RESULTS_REGISTRY = CorpusRegistry()

_RULES = [
    RuleRecord(
        rule_id="DAR001",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Sun Maha Dasha: 6-year period. Career, authority, government, "
            "father, vitality are activated. Positive if Sun is strong; "
            "health and career challenges if weak or afflicted."
        ),
        confidence=0.9,
        verse="Ch.51 v.1-5",
        tags=["dasha", "sun", "maha_dasha", "career", "authority"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR002",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Moon Maha Dasha: 10-year period. Emotional life, mother, home, "
            "mind, public interaction are activated. Fluctuating fortunes; "
            "excellent if Moon is strong and unafflicted."
        ),
        confidence=0.9,
        verse="Ch.51 v.6-10",
        tags=["dasha", "moon", "maha_dasha", "emotions", "mother"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR003",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Mars Maha Dasha: 7-year period. Siblings, courage, accidents, "
            "property, and conflict themes activate. Positive for action, "
            "sports, engineering; challenges from enemies."
        ),
        confidence=0.9,
        verse="Ch.51 v.11-15",
        tags=["dasha", "mars", "maha_dasha", "courage", "siblings"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR004",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Rahu Maha Dasha: 18-year period. Foreign influences, unusual "
            "experiences, unconventional path, technological domains. Long "
            "and transformative; results depend strongly on Rahu's sign/house."
        ),
        confidence=0.85,
        verse="Ch.51 v.16-20",
        tags=["dasha", "rahu", "maha_dasha", "foreign", "transformation"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR005",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Jupiter Maha Dasha: 16-year period. Wisdom, children, dharma, "
            "expansion, wealth, and teaching themes activate. One of the "
            "most auspicious dashas for dharmic growth."
        ),
        confidence=0.9,
        verse="Ch.51 v.21-25",
        tags=["dasha", "jupiter", "maha_dasha", "dharma", "wisdom"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR006",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Saturn Maha Dasha: 19-year period. Discipline, service, delay, "
            "masses, karma are activated. Hardships followed by lasting gains. "
            "Career authority comes slowly but solidly."
        ),
        confidence=0.9,
        verse="Ch.51 v.26-30",
        tags=["dasha", "saturn", "maha_dasha", "discipline", "karma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR007",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Mercury Maha Dasha: 17-year period. Communication, business, "
            "learning, analytical skills activated. Excellent for commerce, "
            "writing, education; challenges if Mercury afflicted."
        ),
        confidence=0.9,
        verse="Ch.51 v.31-35",
        tags=["dasha", "mercury", "maha_dasha", "communication", "business"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR008",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Ketu Maha Dasha: 7-year period. Spiritual insight, detachment, "
            "past-life karma completion, psychic experiences. Separative — "
            "losses in material domains, gains in spiritual."
        ),
        confidence=0.85,
        verse="Ch.51 v.36-40",
        tags=["dasha", "ketu", "maha_dasha", "spiritual", "detachment"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR009",
        source="BPHS",
        chapter="Ch.51",
        school="parashari",
        category="dasha",
        description=(
            "Venus Maha Dasha: 20-year period. Love, marriage, luxury, arts, "
            "comforts, wealth, beauty activate. The longest dasha; excellent "
            "for relationship and material prosperity."
        ),
        confidence=0.9,
        verse="Ch.51 v.41-45",
        tags=["dasha", "venus", "maha_dasha", "marriage", "luxury"],
        implemented=False,
    ),

    # ── Dasha modification by house lordship — BPHS Ch.52-53 ─────────────────
    RuleRecord(
        rule_id="DAR010",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Dasha lord as kendra lord: kendra lord dasha (1/4/7/10 lord) "
            "gives strong practical results — career, home, marriage, or "
            "self depending on which kendra."
        ),
        confidence=0.85,
        verse="Ch.52 v.1-4",
        tags=["dasha", "kendra_lord", "practical_results"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR011",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Dasha lord as trikona lord: trikona lord dasha (1/5/9 lord) "
            "gives fortune, dharma, and merit activation. Favorable for "
            "spiritual and intellectual pursuits."
        ),
        confidence=0.85,
        verse="Ch.52 v.5-8",
        tags=["dasha", "trikona_lord", "fortune", "dharma"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR012",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Dasha lord as dusthana lord: 6th/8th/12th lord dasha can bring "
            "disease, enemies, hidden troubles, or losses. Viparita yoga "
            "can reverse this if the lord is in another dusthana."
        ),
        confidence=0.85,
        verse="Ch.52 v.9-12",
        tags=["dasha", "dusthana_lord", "challenges", "disease"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR013",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Antardasha (sub-dasha) modification: within any Maha Dasha, "
            "the Antardasha planet's lordship and position modifies the "
            "sub-period theme. MD/AD of benefic lords = excellent."
        ),
        confidence=0.85,
        verse="Ch.52 v.13-16",
        tags=["dasha", "antardasha", "sub_period", "modification"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR014",
        source="BPHS",
        chapter="Ch.52",
        school="parashari",
        category="dasha",
        description=(
            "Dasha activation of yogas: raja yogas, dhana yogas, and major "
            "combinations activate specifically in the dasha/antardasha "
            "of the yoga-forming planets."
        ),
        confidence=0.9,
        verse="Ch.52 v.17-20",
        tags=["dasha", "yoga_activation", "raja_yoga", "timing"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR015",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Jupiter Antardasha in Saturn Maha Dasha: one of the most "
            "favorable sub-periods across all combinations. Dharma and "
            "discipline align; excellent for career, marriage, and wealth."
        ),
        confidence=0.85,
        verse="Ch.53 v.1-4",
        tags=["dasha", "saturn_md", "jupiter_ad", "favorable"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR016",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Rahu/Ketu in Maha Dasha: results depend heavily on the sign "
            "and house they occupy AND the lord of that sign. Rahu acts like "
            "the sign lord; Ketu acts opposite (separative)."
        ),
        confidence=0.85,
        verse="Ch.53 v.5-8",
        tags=["dasha", "rahu", "ketu", "sign_lord_effect"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR017",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Dasha sandhi (junction period): the transition between two major "
            "dashas (last 6 months of departing MD, first 6 months of new MD) "
            "is unstable — health issues, confusion, and transition challenges."
        ),
        confidence=0.85,
        verse="Ch.53 v.9-12",
        tags=["dasha", "dasha_sandhi", "transition", "instability"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR018",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Maha Dasha strength by Shadbala: the dasha planet's Shadbala "
            "(six-fold strength) determines the quality of its dasha period. "
            "High Shadbala = easier, more positive results."
        ),
        confidence=0.85,
        verse="Ch.53 v.13-16",
        tags=["dasha", "shadbala", "strength", "dasha_quality"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR019",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Atma Dasha timing: soul-level themes activate in the dasha "
            "of Atma Karaka (highest longitude planet). Jaimini-compatible "
            "rule with Parashari dasha timing."
        ),
        confidence=0.8,
        verse="Ch.53 v.17-20",
        tags=["dasha", "atma_karaka", "jaimini", "cross_school"],
        implemented=False,
    ),
    RuleRecord(
        rule_id="DAR020",
        source="BPHS",
        chapter="Ch.53",
        school="parashari",
        category="dasha",
        description=(
            "Transit support for dasha: Jupiter transiting the natal Moon "
            "(Guru Chandala period) while the natal Jupiter dasha is active "
            "doubles the dharmic and expansion effects."
        ),
        confidence=0.8,
        verse="Ch.53 v.21-24",
        tags=["dasha", "transit", "jupiter", "activation"],
        implemented=False,
    ),
]

for _r in _RULES:
    BPHS_DASHA_RESULTS_REGISTRY.add(_r)
