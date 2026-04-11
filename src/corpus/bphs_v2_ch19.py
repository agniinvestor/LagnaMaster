"""src/corpus/bphs_v2_ch19.py — BPHS Ch.19 (8th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.169-172.
Chapter: 19 — Effects of the Eighth House (Randhra Bhava Phala)
Slokas: 15. Topics: longevity, short life, Saturn/10th lord, long life yogas,
    short life combinations (instant death, infant mortality), ascendant lord
    strength for longevity.
Entity: native (all — longevity is about the native).

Re-encoded S318 Final Sweep: Original S311 encoding only covered v.1-7 (6 rules).
BUG-094 identified 9 missing slokas (v.8-13 short-life, v.14-15 long-life).
Also fixed under-encoding in v.3 and v.4-7.
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.19", category="8th_house_effects",
    id_start=1900, session="S318", sloka_count=15,
    chapter_tags=["8th_house", "randhra_bhava", "longevity"],
    entity_target="native",
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.1: Long life — 8th lord in angle (p.169)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": [1, 4, 7, 10]}],
    signal_group="h8_lord_kendra_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_life_indicated",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.1",
    commentary_context="Santhanam: The 8th lord in an angle indicates long life. Read in context with v.2 — short life if 8th lord joins malefic/ascendant lord in 8th itself.",
    description="8th lord in an angle: long life is indicated.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1901"]},
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.2: Short life — 8th lord with malefic/ascendant lord in 8th (p.169)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_8", "any_malefic"]},
    ],
    signal_group="h8_lord_h8_malefic_short_life",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "short_lived_malefic_in_8th",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.2",
    description=(
        "8th lord in the 8th conjunct a malefic: the native will be "
        "short-lived."
    ),
    commentary_context=(
        "Santhanam: Short life if 8th lord in 8th with malefic. "
        "Ascendant lord variant encoded as alternative rule BPHS1902."
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
    direction="unfavorable", intensity="strong", primary_domain="longevity",
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

# ═══════════════════════════════════════════════════════════════════════════════
# v.3: Saturn and 10th lord in longevity (p.170)
# ═══════════════════════════════════════════════════════════════════════════════

# v.3a: Saturn joins malefic/ascendant lord in 8th → short life
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 8},
        {"type": "planets_conjunct", "planets": ["Saturn", "any_malefic"]},
    ],
    signal_group="saturn_h8_malefic_short_life",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "saturn_malefic_8th_short_life",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.3",
    commentary_context=(
        "Santhanam: Similarly consider Saturn and 10th lord in the matter "
        "of longevity. Notes expand: short life if Saturn joins a "
        "malefic or the ascendant lord in the 8th house. This applies "
        "the v.2 logic to Saturn specifically."
    ),
    description=(
        "Saturn in the 8th house conjunct a malefic: short life "
        "should be declared, similarly to the 8th lord rule."
    ),
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1901"]},
)

# v.3b: 10th lord in 8th with malefic/ascendant lord → short life
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 10, "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_10", "any_malefic"]},
    ],
    signal_group="h10_lord_h8_malefic_short_life",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "10th_lord_malefic_8th_short_life",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.3",
    commentary_context=(
        "Santhanam: The 10th lord in the 8th with a malefic planet or "
        "the ascendant lord also produces short life — same logic as "
        "v.2 applied to the 10th lord."
    ),
    description=(
        "10th lord in the 8th conjunct a malefic: short life, "
        "similarly to the 8th lord rule."
    ),
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1901"]},
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.4-7: Long life yogas (pp.170-171)
# ═══════════════════════════════════════════════════════════════════════════════

# v.4 yoga 1: 6th lord in 12th → long life (Viparita)
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 12}],
    signal_group="h6_lord_h12_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_life_viparita_yoga",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4",
    commentary_context=(
        "Santhanam: First of three long-life yogas from v.4. "
        "6th lord in 12th = Viparita Raja Yoga for longevity. "
        "Dusthana lords in dusthana neutralize each other."
    ),
    description="6th lord in the 12th: long life is indicated.",
    concordance_texts=["Phaladeepika"],
)

# v.4 yoga 2: 6th and 12th lords simultaneously in 6th and 12th
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 6, "house": [6, 12]},
        {"type": "lord_in_house", "lord_of": 12, "house": [6, 12]},
    ],
    signal_group="h6_h12_lords_mutual_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_life_6th_12th_mutual",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4",
    commentary_context=(
        "Santhanam note: Second yoga — 6th and 12th lords simultaneously "
        "in the 6th and the 12th. Mutual dusthana exchange for longevity."
    ),
    description=(
        "6th and 12th lords simultaneously in the 6th and the 12th: "
        "long life."
    ),
    concordance_texts=["Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1905"]},
)

# v.4 yoga 3: 6th lord in ascendant while 12th lord in 8th
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 6, "house": 1},
        {"type": "lord_in_house", "lord_of": 12, "house": 8},
    ],
    signal_group="h6_lord_h1_h12_lord_h8_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_life_6th_1st_12th_8th",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.4",
    commentary_context=(
        "Santhanam note: Third yoga — 6th lord in the ascendant while "
        "12th lord is in the 8th. Both dusthana lords contained in "
        "specific houses."
    ),
    description=(
        "6th lord in the ascendant while the 12th lord is in the 8th: "
        "long life."
    ),
    concordance_texts=["Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1905"]},
)

# v.5-6: Lords of 5th, 8th, ascendant in own navamsas/rasis/friendly signs
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
        {"type": "planet_dignity", "planet": "lord_of_8", "dignity": "strong"},
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "strong"},
    ],
    signal_group="h5_h8_h1_lords_strong_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_span_of_life_lords_strong",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.19 v.5-6",
    commentary_context=(
        "Santhanam: The lords of the 5th, 8th and ascendant being in "
        "their own navamsas, own Rasis or in friendly signs, the native "
        "will enjoy a long span of life. Strength and weakness of "
        "planets must be estimated in deciding longevity."
    ),
    description=(
        "Lords of the 5th, 8th and ascendant in their own navamsas, "
        "own Rasis or friendly signs: long span of life."
    ),
    concordance_texts=["Phaladeepika"],
)

# v.7: Lords of 1st, 8th, 10th + Saturn all in angles/trines/11th
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [1, 4, 5, 7, 9, 10, 11]},
        {"type": "lord_in_house", "lord_of": 8, "house": [1, 4, 5, 7, 9, 10, 11]},
        {"type": "lord_in_house", "lord_of": 10, "house": [1, 4, 5, 7, 9, 10, 11]},
        {"type": "planet_in_house", "planet": "Saturn", "house": [1, 4, 5, 7, 9, 10, 11]},
    ],
    signal_group="h1_h8_h10_saturn_kendra_trikona_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_life_all_longevity_lords_well_placed",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.7",
    commentary_context=(
        "Santhanam: Should the lords of the ascendant, 8th and 10th and "
        "Saturn are all disposed severally in an angle, in a trine or in "
        "the 11th, the subject will live long. Like these, there are many "
        "other yogas dealing with longevity."
    ),
    description=(
        "Lords of the ascendant, 8th and 10th and Saturn all in "
        "angles, trines or the 11th: the subject will live long."
    ),
    concordance_texts=["Phaladeepika"],
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.8: Short life 20-32 years — weak ascendant lord + 8th lord in angle (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "weak"},
        {"type": "lord_in_house", "lord_of": 8, "house": [1, 4, 7, 10]},
    ],
    signal_group="weak_asc_lord_h8_kendra_medium_life",
    direction="unfavorable", intensity="moderate", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "life_span_20_to_32_years",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.19 v.8",
    commentary_context=(
        "Santhanam: One's span of life will be between 20 and 32 years "
        "if the ascendant lord is weak while the 8th lord is in an angle. "
        "Note: v.1 says 8th lord in angle = long life, but when the "
        "ascendant lord is simultaneously weak, it reduces to medium life."
    ),
    description=(
        "Ascendant lord weak while the 8th lord is in an angle: "
        "life span between 20 and 32 years."
    ),
    timing_window={"type": "age_range", "value": "20-32"},
    concordance_texts=[],
    rule_relationship={"type": "override", "related_rules": ["BPHS1900"]},
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.9: Short life — 8th lord in fall + malefic in 8th + weak ascendant (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_8", "dignity": "debilitated"},
        {"type": "planet_in_house", "planet": "any_malefic", "house": 8},
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "weak"},
    ],
    signal_group="h8_lord_fall_malefic_h8_weak_asc_short",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "short_lived_8th_lord_fall_malefic",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.19 v.9",
    commentary_context=(
        "Santhanam: The native will only be short-lived if the 8th lord "
        "is in fall while the 8th has a malefic in it and the ascendant "
        "lord is bereft of strength. Three conditions required simultaneously."
    ),
    description=(
        "8th lord debilitated, malefic in the 8th, and ascendant lord "
        "bereft of strength: the native will be short-lived."
    ),
    concordance_texts=[],
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.10: Death instant at birth — all three locations afflicted (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 8},
        {"type": "lord_in_house", "lord_of": 8, "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_8", "any_malefic"]},
        {"type": "planet_in_house", "planet": "any_malefic", "house": 12},
    ],
    signal_group="h8_h12_all_malefic_instant_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "death_instant_at_birth",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.9}],
    verse_ref="Ch.19 v.10",
    description=(
        "Death will be instant at birth if the 8th house, 8th lord "
        "and the 12th house are all conjunct malefics."
    ),
    commentary_context=(
        "Santhanam: Three simultaneous conditions required — malefics "
        "in 8th house, 8th lord conjunct malefics, and malefics in "
        "12th house. Each location requires at least one natural malefic "
        "(Sun, Mars, Saturn, Rahu, Ketu). This is among the most severe "
        "combinations in BPHS longevity assessment."
    ),
    exceptions=[
        "Benefic aspect on 8th house or ascendant may mitigate per Ch.10 (Antidotes for Evils)",
        "Strong ascendant lord in angle/trine may override per v.14-15 of this chapter",
    ],
    modifiers=[{
        "condition": "benefic_aspects_8th_house_or_ascendant",
        "effect": "attenuates", "target": "prediction",
        "strength": "strong", "scope": "local",
    }],
    timing_window={"type": "age", "value": "0"},
    concordance_texts=[],
    rule_relationship={"type": "override", "related_rules": ["BPHS1900"]},
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.11: Immediate end — malefics in angles/trines + benefics in 6/8 + 8th lord
#       in fall in ascendant (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic",
         "house": [1, 4, 5, 7, 9, 10]},
        {"type": "planet_in_house", "planet": "any_benefic", "house": [6, 8]},
        {"type": "lord_in_house", "lord_of": 8, "house": 1},
        {"type": "planet_dignity", "planet": "lord_of_8", "dignity": "debilitated"},
    ],
    signal_group="malefic_kendra_benefic_dusthana_8th_lord_fall_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "immediate_end_malefic_dominance",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.9}],
    verse_ref="Ch.19 v.11",
    description=(
        "Malefics in angles/trines and benefics in 6th/8th, while the "
        "ascendant has in it the 8th lord in fall: this yoga will cause "
        "immediate end."
    ),
    commentary_context=(
        "Santhanam: Four simultaneous conditions — (1) malefics occupy "
        "kendras or trikonas, (2) benefics relegated to 6th/8th dusthanas, "
        "(3) 8th lord placed in the ascendant, (4) 8th lord debilitated. "
        "The complete reversal of natural protective placements."
    ),
    exceptions=[
        "Benefic aspect on ascendant may mitigate per Ch.10",
    ],
    modifiers=[{
        "condition": "benefic_aspects_ascendant",
        "effect": "attenuates", "target": "prediction",
        "strength": "strong", "scope": "local",
    }],
    timing_window={"type": "age", "value": "0"},
    concordance_texts=[],
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.12: Very brief life — 5th house, 8th house, 8th lord all with malefics (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 5},
        {"type": "planet_in_house", "planet": "any_malefic", "house": 8},
        {"type": "planets_conjunct", "planets": ["lord_of_8", "any_malefic"]},
    ],
    signal_group="h5_h8_lord8_all_malefic_brief_life",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "life_span_very_brief",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.85}],
    verse_ref="Ch.19 v.12",
    description=(
        "5th house, 8th house and the 8th lord all conjunct malefics: "
        "the life span will be very brief."
    ),
    commentary_context=(
        "Santhanam: In sloka 12, it is stated that 8th lord should be "
        "in fall in the ascendant. For no ascendant, the 8th lord is "
        "debilitated in the ascending sign. Should the 8th lord be in "
        "the 8th, long life to the native is denoted (v.1 logic). But "
        "when 5th and 8th houses both have malefics, life is very brief."
    ),
    concordance_texts=[],
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.13: Death within a month — 8th lord in 8th + Moon afflicted (p.171)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": 8},
        {"type": "planets_conjunct", "planets": ["Moon", "any_malefic"]},
    ],
    signal_group="h8_lord_h8_moon_malefic_infant_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "death_within_month_of_birth",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.85}],
    verse_ref="Ch.19 v.13",
    description=(
        "Within a month of birth, death will befall the child if the "
        "8th lord is in the 8th itself while the Moon is with malefics "
        "and bereft of benefic aspect."
    ),
    commentary_context=(
        "Santhanam: 8th lord in 8th normally gives long life (v.1), "
        "but when simultaneously the Moon is captured by a malefic and "
        "without any help from a benefic, early evils to life span "
        "will have to be predicted. The Moon's affliction overrides "
        "the otherwise favorable 8th lord placement."
    ),
    exceptions=[
        "Benefic aspect on Moon cancels this combination",
    ],
    modifiers=[{
        "condition": "benefic_aspect_on_moon",
        "effect": "negates", "target": "prediction",
        "strength": "strong", "scope": "local",
    }],
    timing_window={"type": "age", "value": "0"},
    concordance_texts=[],
    rule_relationship={"type": "override", "related_rules": ["BPHS1900"]},
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.14: Long life — ascendant lord exalted + Moon in 11th + Jupiter in 8th (p.172)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "exalted"},
        {"type": "planet_in_house", "planet": "Moon", "house": 11},
        {"type": "planet_in_house", "planet": "Jupiter", "house": 8},
    ],
    signal_group="asc_exalted_moon_11_jupiter_8_long_life",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "native", "claim": "long_lived_triple_strength",
                  "domain": "longevity", "direction": "favorable", "magnitude": 0.85}],
    verse_ref="Ch.19 v.14",
    description=(
        "One will be long-lived if the ascendant lord is in exaltation "
        "while the Moon and Jupiter are respectively in the 11th and "
        "8th from the ascendant."
    ),
    commentary_context=(
        "Santhanam: Even Jupiter alone well-placed in the 8th "
        "house leads to a long span of life. When he is further helped "
        "by the Moon being in the 11th house and by the ascendant lord's "
        "exaltation, doubtlessly the life will be exceedingly lengthy."
    ),
    concordance_texts=[],
)

# ═══════════════════════════════════════════════════════════════════════════════
# v.15: Long life — strong ascendant lord aspected by benefic from angle (p.172)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "strong"},
        {"type": "planet_aspecting", "planet": "any_benefic",
         "house": "lord_of_1"},
    ],
    signal_group="strong_asc_lord_benefic_aspect_longevity",
    direction="favorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "native", "claim": "wealthy_virtuous_long_lived",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.19 v.15",
    description=(
        "If the ascendant lord is exceedingly strong and aspected by a "
        "benefic from an angle, the person will be wealthy, virtuous "
        "and long-lived."
    ),
    commentary_context=(
        "Santhanam: If the ascendant lord is exceedingly strong and "
        "aspected by a benefic from an angle, the person concerned will "
        "be wealthy, virtuous and longlived. Multiple outcome domains: "
        "longevity, wealth, and character."
    ),
    concordance_texts=[],
)

BPHS_V2_CH19_REGISTRY = b.build()
