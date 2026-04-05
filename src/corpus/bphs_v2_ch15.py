"""src/corpus/bphs_v2_ch15.py — BPHS Ch.15 (4th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.142-144.
Chapter: 15 — Effects of the Fourth House (Sukha Bhava Phala)
Slokas: 14. Rules: 14. Rich timing data (ages 12, 32, 42).
Entity: native (most), mother (v.6-7).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.15", category="4th_house_effects",
    id_start=1500, session="S311", sloka_count=14,
    chapter_tags=["4th_house", "sukha_bhava"],
    entity_target="native",
)

# ═══ v.2: Housing comforts — 4th occupied by lord or aspected by benefic ══════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 4}],
    signal_group="h4_lord_own_house_comfort",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "residential_comforts_full_degree",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.15 v.2",
    commentary_context="No separate Santhanam note. The verse conditions are explicit: 4th occupied by its lord or aspected by benefic.",
    description=(
        "One will have residential comforts in full degree if the 4th is "
        "occupied by its lord or by the ascendant lord and be aspected by "
        "a benefic."
    ),
    concordance_texts=["Saravali"],
    tags=["h4_lord", "housing", "comfort"],
)

# ═══ v.3: Lands, conveyances, houses, instruments ════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": [5]},
        {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
    ],
    signal_group="h5_lord_own_house_lands",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "comforts_lands_conveyances_houses",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.15 v.3",
    commentary_context="No separate Santhanam note. The 5th lord (not 4th) is mentioned — likely a bhavat bhavam reference: 5th = 2nd from 4th (resources of the home).",
    description=(
        "5th lord in own house or own Navamsa or in exaltation: endowed "
        "with comforts related to lands, conveyances, houses etc. and "
        "musical instruments."
    ),
    concordance_texts=[],
)

# ═══ v.4: 10th lord + 4th lord in angle/trine → beautiful mansions ════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 10, "house": [1, 4, 5, 7, 9, 10]},
        {"type": "lord_in_house", "lord_of": 4, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="h10_h4_lords_kendra_mansions",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "acquire_beautiful_mansions",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.15 v.4",
    commentary_context="No separate Santhanam note. 10th-4th connection = karma-sukha yoga (career providing domestic happiness).",
    description=(
        "10th lord joins the 4th lord in an angle or in a trine: the "
        "native will acquire beautiful mansions."
    ),
    concordance_texts=[],
)

# ═══ v.5: Honoured by relatives ══════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Mercury", "house": 1},
    ],
    signal_group="mercury_h1_honoured_relatives",
    direction="favorable", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "honoured_by_relatives",
         "domain": "career", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.15 v.5",
    commentary_context="No separate Santhanam note. Mercury in ascendant with benefic 4th lord = intelligence earning respect from relatives.",
    description=(
        "Mercury in the ascendant while the 4th lord being a benefic is "
        "aspected by another benefic: the native will be honoured by "
        "his relatives."
    ),
    modifiers=[
        {"condition": "h4_lord_is_benefic_aspected_by_benefic", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"},
    ],
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1500"]},
)

# ═══ v.6: Long-living mother ═════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_benefic", "house": 4},
        {"type": "planet_dignity", "planet": "lord_of_4", "dignity": "exalted"},
    ],
    entity_target="mother",
    signal_group="benefic_h4_mother_longevity",
    direction="favorable", intensity="strong",
    primary_domain="longevity",
    predictions=[
        {"entity": "mother", "claim": "long_living_mother",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.15 v.6",
    description=(
        "4th house occupied by a benefic while its lord is in his "
        "exaltation sign as the indicator of mother is endowed with "
        "strength: the native will have a long-living mother."
    ),
    commentary_context=(
        "Santhanam notes: The stronger among the Moon and Mars is denoted "
        "as the significator of mother, vide slokas 18-19 ch.32, infra. "
        "There are still many more views about the karakatwas for parents "
        "given by various authors."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Ch.32 v.18-19 Planetary Karakatvas"],
    modifiers=[
        {"condition": [{"type": "dynamic_karaka", "karaka": "mother", "state": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"},
    ],
    convergence_signals=["moon_strong", "h4_lord_exalted", "no_malefic_in_4th"],
)

# ═══ v.7: Happiness to mother ════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 4, "house": [1, 4, 7, 10]},
        {"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]},
        {"type": "planet_dignity", "planet": "Mercury", "dignity": "exalted"},
    ],
    entity_target="mother",
    signal_group="h4_lord_kendra_mother_happy",
    direction="favorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "mother", "claim": "mother_will_be_happy",
         "domain": "health", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.15 v.7",
    commentary_context="No separate Santhanam note. Triple benefic condition: 4th lord in kendra + Venus in kendra + Mercury exalted.",
    description=(
        "The native's mother will be happy if the 4th lord is in an "
        "angle while Venus is also in an angle as Mercury is exalted."
    ),
    concordance_texts=[],
)

# ═══ v.8: Quadrupeds (cows and buffaloes) ════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Sun", "house": 4},
        {"type": "planet_in_house", "planet": "Moon", "house": 9},
        {"type": "planet_in_house", "planet": "Saturn", "house": 11},
        {"type": "planet_in_house", "planet": "Mars", "house": 11},
    ],
    signal_group="sun_h4_moon_h9_quadrupeds",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "confers_cows_and_buffaloes",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.15 v.8",
    commentary_context="No separate Santhanam note. A specific 3-planet yoga for material possessions (cattle/vehicles in modern context).",
    description=(
        "Sun in the 4th, Moon in the 9th and Saturn and Mars in the "
        "11th — this yoga will confer cows and buffaloes on the native."
    ),
    concordance_texts=[],
)

# ═══ v.9: Dumbness ═══════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 4, "house": [6, 8]},
        {"type": "planet_in_house", "planet": "Mars", "house": [6, 8]},
    ],
    signal_group="h4_lord_mars_dusthana_dumb",
    direction="unfavorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "native_will_be_dumb",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.15 v.9",
    commentary_context="No separate Santhanam note. The movable ascendant condition is critical — does not apply to fixed or dual lagnas.",
    description=(
        "4th lord and Mars together in the 6th or the 8th house with "
        "a movable ascendant: the native will be dumb."
    ),
    modifiers=[
        {"condition": [{"type": "lagna_sign_type", "sign_type": "movable"}], "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"},
    ],
    concordance_texts=[],
    prediction_type="trait",
    exceptions=["does_not_apply_to_fixed_or_dual_ascendants"],
)

# ═══ v.10-14: Conveyances with SPECIFIC TIMING ══════════════════════════════

# v.10a: Conveyances in 12th year
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 4, "house": [6, 8, 11, 12]},
    ],
    signal_group="h4_lord_fall_conveyance_12",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "obtain_conveyances_at_age_12",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 12, "precision": "approximate"},
    verse_ref="Ch.15 v.10-14",
    description=(
        "Ascendant lord is a benefic while the 4th lord is in fall or in "
        "the 11th and the significator (Venus) is in the 12th: the native "
        "will obtain conveyances in his 12th year."
    ),
    commentary_context=(
        "Santhanam notes: It is not known why the 4th lord should be in "
        "fall for early obtainment of conveyances. This condition seems to "
        "be the result of defective text as the next line adds that the "
        "4th lord may be in the 11th. I read it as: If the ascendant lord "
        "is a benefic while the 11th is tenanted by Venus and the 4th "
        "lord, early obtainment of conveyance (around the 12th year) will "
        "come to pass."
    ),
    modifiers=[
        {"condition": [{"type": "planet_nature", "planet": "lord_of_1", "nature": "benefic"}], "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"},
        {"condition": [{"type": "planet_in_house", "planet": "Venus", "house": [11, 12]}], "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"},
    ],
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1500"]},
)

# v.10b: Conveyances in 32nd year
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Sun", "house": 4},
        {"type": "planet_dignity", "planet": "lord_of_4", "dignity": "exalted"},
        {"type": "planets_conjunct", "planets": ["lord_of_4", "Venus"]},
    ],
    signal_group="sun_h4_lord_exalted_conveyance_32",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "acquire_conveyances_at_age_32",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age", "value": 32, "precision": "approximate"},
    verse_ref="Ch.15 v.10-14",
    commentary_context="Santhanam: Sun in 4th + 4th lord exalted + Venus = conveyances at 32. This is the second timing condition in the series.",
    description=(
        "Sun in the 4th house, the 4th lord is exalted and be with Venus: "
        "one will acquire conveyances in his 32nd year."
    ),
    concordance_texts=[],
)

# v.10c: Conveyances in 42nd year
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 4, "house": 10},
        {"type": "lord_in_house", "lord_of": 10, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="h4_h10_lords_conveyance_42",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "endowed_with_conveyances_at_age_42",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 42, "precision": "approximate"},
    verse_ref="Ch.15 v.10-14",
    commentary_context="Santhanam: 4th lord joins 10th lord in 4th lord's exaltation Navamsa = conveyances at 42. Third timing condition.",
    description=(
        "It will be in the 42nd year that one will be endowed with "
        "conveyances if the 4th lord joins the 10th lord in his (4th "
        "lord's) exaltation Navamsa."
    ),
    concordance_texts=[],
)

# v.10-14d: Exchange 4th-11th → conveyances in 12th year
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 4, "house": 11},
        {"type": "lord_in_house", "lord_of": 11, "house": 4},
    ],
    signal_group="h4_h11_exchange_conveyance_12",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "conveyances_at_age_12_through_exchange",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 12, "precision": "approximate"},
    verse_ref="Ch.15 v.10-14",
    commentary_context="Santhanam: Exchange between 4th and 11th lords = another route to conveyances at age 12. The sage prescribes multiple combinations for the same timing.",
    description=(
        "An exchange between the 11th and the 4th lords will confer "
        "conveyances in the 12th year."
    ),
    concordance_texts=[],
    tags=["exchange", "parivartana", "conveyance"],
)

# v.10-14e: Benefic in 4th → happy with conveyances, free from accidents
b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_benefic", "house": 4}],
    signal_group="benefic_h4_safe_conveyance",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "happy_with_conveyances_free_from_accidents",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.15 v.10-14",
    commentary_context=(
        "Santhanam: Should a benefic be in the 4th, aspect the 4th, or "
        "aspect the lord of the 4th house, the native will be happy with "
        "conveyances and be free from accidents and dangers. A malefic "
        "replacing the said benefic will cause losses concerning vehicles "
        "and reduce one to severe accidents."
    ),
    description=(
        "A benefic be in the 4th, aspect the 4th, or aspect the lord "
        "of the 4th house: the native will be happy with conveyances "
        "and be free from accidents and dangers."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1513"]},
)

# v.10-14f: Malefic → accidents, dangers (contrary mirror)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 4}],
    signal_group="malefic_h4_vehicle_accidents",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "malefic_effects_on_conveyances_accidents",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.15 v.10-14",
    commentary_context="Contrary of BPHS1512. Santhanam explicitly states malefic = losses and severe accidents.",
    description=(
        "A malefic replacing the said benefic will produce only malefic "
        "effects in respect of conveyances and reduce one to severe "
        "accidents."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1512"]},
)

BPHS_V2_CH15_REGISTRY = b.build()
