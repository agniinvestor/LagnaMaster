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
    id_start=1900, session="S311",
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
    description="8th lord in an angle: long life is indicated.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1901"]},
)

# ═══ v.2: Short life — 8th lord with malefic/ascendant lord in 8th ════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 8}],
    signal_group="h8_lord_h8_malefic_short_life",
    direction="unfavorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "short_lived",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.2",
    description=(
        "8th lord joining the ascendant lord or a malefic and being in "
        "the 8th itself: the native will be short-lived."
    ),
    commentary_context=(
        "Santhanam notes: To get the actual import of this verse, read it "
        "in the context of the previous verse. Short life will come to pass "
        "if: 1) The 8th lord is in the 8th along with a malefic or along "
        "with the ascendant lord, or 2) Saturn joins a malefic/ascendant "
        "lord in the 8th house."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1900"]},
)

# ═══ v.3: Saturn and 10th lord in longevity ══════════════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 8}],
    signal_group="saturn_h8_10th_lord_longevity",
    direction="mixed", intensity="moderate", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "saturn_and_10th_lord_affect_longevity",
                  "domain": "longevity", "direction": "mixed", "magnitude": 0.6}],
    verse_ref="Ch.19 v.3",
    description=(
        "Similarly consider Saturn and 10th lord in the matter of longevity."
    ),
    commentary_context=(
        "Santhanam notes: The 10th lord also has a role to play. If the "
        "10th lord is in the 8th with a malefic planet/ascendant lord, "
        "short life should be declared."
    ),
    concordance_texts=[],
)

# ═══ v.4-7: Long life yogas ══════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 12}],
    signal_group="h6_lord_h12_long_life",
    direction="favorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "long_life_viparita_yoga",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4-7",
    description=(
        "There will be long life if the 6th lord is in the 12th or if "
        "the 6th lord is in the 6th as the 12th lord. Also if the 6th "
        "and 12th lord are in the ascendant and the 8th."
    ),
    concordance_texts=["Phaladeepika"],
)

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": "any"},
        {"type": "lord_in_house", "lord_of": 8, "house": "any"},
    ],
    signal_group="h5_h8_lords_own_navamsa_long_life",
    direction="favorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "native", "claim": "long_span_of_life",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4-7",
    description=(
        "If the lords of the 5th, 8th and ascendant are in their own "
        "navamsas, own Rasis or in friendly signs, the native will enjoy "
        "a long span of life. Also if the lords of the ascendant, 8th "
        "and 10th and Saturn are all disposed severally in an angle, "
        "in a trine or in the 11th, the subject will live long."
    ),
    commentary_context=(
        "Santhanam notes: In sloka 4, we have three yogas for long life: "
        "1. The 6th lord in the 12th. 2. The 5th, 8th and ascendant lords "
        "in own navamsas/rasis/friendly signs. 3. Lords of ascendant, 8th, "
        "10th and Saturn all in angles/trines/11th. Like these, there are "
        "many other yogas dealing with the issue of longevity. The strength "
        "and weakness of the planets concerned be estimated in deciding "
        "longevity."
    ),
    concordance_texts=["Phaladeepika"],
)

BPHS_V2_CH19_REGISTRY = b.build()
