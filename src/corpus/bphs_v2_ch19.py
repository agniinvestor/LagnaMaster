"""src/corpus/bphs_v2_ch19.py — BPHS Ch.19 (8th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.169-172.
Chapter: 19 — Effects of the Eighth House (Randhra Bhava Phala)
Slokas: ~7. Topics: longevity, short life, Saturn/10th lord, long life yogas.
Entity: native (all — longevity is about the native).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.19", category="8th_house_effects",
    id_start=1900, session="S311", sloka_count=7,
    chapter_tags=["8th_house", "randhra_bhava"],
    entity_target="native",
)

# ═══ v.1: Long life — 8th lord in angle ══════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": [1, 4, 7, 10]}],
    signal_group="h8_lord_kendra_long_life",
    direction="favorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "long_life_indicated",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.1",
    commentary_context="Santhanam: The 8th lord in an angle indicates long life. Read in context with v.2 — short life if 8th lord joins malefic/ascendant lord in 8th itself.",
    description="8th lord in an angle: long life is indicated.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1901"]},
)

# ═══ v.2: Short life — 8th lord with malefic/ascendant lord in 8th ════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_8", "any_malefic"]},
    ],
    signal_group="h8_lord_h8_malefic_short_life",
    direction="unfavorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "short_lived_malefic_in_8th",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.2",
    description=(
        "8th lord in the 8th conjunct a malefic: the native will be "
        "short-lived."
    ),
    commentary_context=(
        "Santhanam: Short life if 8th lord in 8th with malefic. "
        "Ascendant lord variant encoded as alternative rule."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1900"]},
)

# v.2b: Alternative — 8th lord in 8th with ascendant lord
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_8", "lord_of_1"]},
    ],
    signal_group="h8_lord_h8_asc_lord_short_life",
    direction="unfavorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "short_lived_asc_lord_in_8th",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.2",
    description=(
        "8th lord in the 8th conjunct the ascendant lord: the native "
        "will be short-lived."
    ),
    commentary_context=(
        "Santhanam: Alternative path — ascendant lord joining 8th lord "
        "in 8th also produces short life."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1901"]},
)

# ═══ v.3: Saturn and 10th lord in longevity ══════════════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 8}],
    signal_group="saturn_h8_10th_lord_longevity",
    direction="mixed", intensity="moderate", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "saturn_and_10th_lord_affect_longevity",
                  "domain": "longevity", "direction": "mixed", "magnitude": 0.6}],
    verse_ref="Ch.19 v.3",
    commentary_context="Santhanam: Consider Saturn and 10th lord similarly. If 10th lord in 8th with malefic/ascendant lord, short life should be declared.",
    description=(
        "Similarly consider Saturn and 10th lord in the matter of longevity."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "10th_lord_in_8th_with_malefic_or_ascendant_lord", "effect": "amplifies", "strength": "strong"}],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1901"]},
)

# ═══ v.4-7: Long life yogas ══════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 12}],
    signal_group="h6_lord_h12_long_life",
    direction="favorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "long_life_viparita_yoga",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4-7",
    commentary_context="Santhanam: One of the three long-life yogas from v.4. Dusthana lords in dusthana = Viparita Raja Yoga for longevity.",
    description=(
        "There will be long life if the 6th lord is in the 12th or if "
        "the 6th lord is in the 6th as the 12th lord. Also if the 6th "
        "and 12th lord are in the ascendant and the 8th."
    ),
    concordance_texts=["Phaladeepika"],
)

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
        {"type": "planet_dignity", "planet": "lord_of_8", "dignity": "strong"},
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "strong"},
    ],
    signal_group="h5_h8_lords_own_navamsa_long_life",
    direction="favorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "long_span_of_life",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4-7",
    commentary_context=(
        "Santhanam: Three yogas for long life: 1) 6th lord in 12th, "
        "2) 5th/8th/ascendant lords in own navamsas/rasis/friendly signs, "
        "3) Lords of ascendant/8th/10th + Saturn all in angles/trines/11th. "
        "The strength and weakness of planets must be estimated."
    ),
    description=(
        "If the lords of the 5th, 8th and ascendant are in their own "
        "navamsas, own Rasis or in friendly signs, the native will enjoy "
        "a long span of life. Also if the lords of the ascendant, 8th "
        "and 10th and Saturn are all disposed severally in an angle, "
        "in a trine or in the 11th, the subject will live long."
    ),
    concordance_texts=["Phaladeepika"],
)

BPHS_V2_CH19_REGISTRY = b.build()
