"""src/corpus/bphs_v2_ch17.py — BPHS Ch.17 (6th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.152-160.
Chapter: 17 — Effects of the Sixth House (Ari Bhava Phala)
Slokas: 28. EXTREMELY rich timing data (15+ specific ages).
Entity: native (all — diseases/enemies affect the native).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.17", category="6th_house_effects",
    id_start=1700, session="S311",
    chapter_tags=["6th_house", "ari_bhava"],
    entity_target="native",
)

# ═══ v.2: 6th lord in ascendant/8th → ulcers/bruises ═════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": [1, 8]}],
    signal_group="h6_lord_asc_or_h8_ulcers",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "ulcers_or_bruises_on_body",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.17 v.2",
    description=(
        "6th lord in the ascendant or 8th: there will be ulcers or bruises "
        "on the body. The sign becoming the 6th house will lead to the "
        "knowledge of the concerned limb."
    ),
    concordance_texts=["Saravali"],
)

# ═══ v.3-5: Relatives affected — universal principle ═════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 6, "house": [6, 8]},
    ],
    signal_group="h6_lord_karaka_relatives_affected",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "relatives_afflicted_per_karaka",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.17 v.3-5",
    description=(
        "The Karaka of a relative or the lord of such a house joining the "
        "6th lord or being in the 6th/8th house indicates ulcers/bruises "
        "to such a relative. Sun → head, Moon → face, Mars → neck, "
        "Mercury → navel, Jupiter → nose, Venus → eyes, Saturn → feet, "
        "Ketu → abdomen."
    ),
    commentary_context=(
        "Santhanam: The relatives signified by planets and Bhavas are "
        "denoted in ch.32, infra. Replacing the ascendant with a certain "
        "bhava, these afflictions to the concerned relatives be predicted. "
        "For example, if the 6th and 8th lords join the Moon in the 3rd "
        "bhava, danger to coborn by drowning, lung disorders etc."
    ),
    concordance_texts=[],
    cross_chapter_refs=["Ch.32 Planetary Karakatvas"],
    prediction_type="trait",
)

# ═══ v.6: Facial diseases ════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": "any"}],
    signal_group="asc_lord_mars_mercury_facial",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "facial_diseases",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.17 v.6",
    description=(
        "Lord of ascendant in a sign of Mars or Mercury and be aspected "
        "by Mercury: there will be diseases of the face."
    ),
    commentary_context=(
        "Santhanam notes: The lord of the ascendant should be in Aries, "
        "Scorpio, Gemini or Virgo and be aspected by Mercury. Even if "
        "Mars, ruling the ascendant, is in Gemini or Virgo and is "
        "aspected by Mercury, the native will suffer facial diseases."
    ),
    concordance_texts=[],
    modifiers=[
        {"condition": "in_mars_or_mercury_sign", "effect": "conditionalizes", "strength": "moderate"},
        {"condition": "aspected_by_mercury", "effect": "amplifies", "strength": "moderate"},
    ],
)

# ═══ v.7-8½: Leprosy ════════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": "any"}],
    signal_group="asc_lord_leprosy",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "leprosy_or_skin_disease",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.17 v.7-8",
    description=(
        "Mars or Mercury having ownership of the ascending sign and "
        "joining the Moon, Rahu and Saturn will cause leprosy. Moon not "
        "in ascendant but with Rahu → white leprosy. Saturn in place of "
        "Rahu → black leprosy. Mars → blood-leprosy."
    ),
    concordance_texts=[],
    modifiers=[
        {"condition": "moon_rahu_saturn_conjunction", "effect": "conditionalizes", "strength": "strong"},
    ],
)

# ═══ v.9-12½: Diseases by planet in 6th/8th with ascendant lords ═════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Sun", "house": [6, 8]},
    ],
    signal_group="sun_h6_h8_fever_tumours",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "fever_and_tumours",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.17 v.9-12",
    description=(
        "Ascendant occupied by lords of 6th and 8th along with the Sun: "
        "afflicted by fever and tumours. Disease table: Sun → tumours/fever; "
        "Mars → blood vessels/weapons; Mercury → bilious/jaundice; "
        "Jupiter → freedom from diseases; Venus → sexual diseases; "
        "Saturn → windy/rheumatism/arthritis; Rahu → danger from low-caste; "
        "Ketu → navel diseases; Moon → drowning/phlegmatic/lung disorders."
    ),
    commentary_context=(
        "Santhanam provides extensive disease encyclopaedia by planet from "
        "Dr. H.L. Cornell's 'Encyclopaedia of Medical Astrology'. "
        "Sun: nerves, brain, cellular excitation, blood affliction. "
        "Moon: gaseous distention, abdomen, bladder, bronchial. "
        "Mars: death by abortions, blood vessels, boils, burns. "
        "Mercury: nervous complaints, asthma, impure blood. "
        "Jupiter: adiposis, adrenals, arterial blood. "
        "Venus: comedo, bowel disorders, Bright's Disease. "
        "Saturn: antiperistalsis, arthritis, rheumatism."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Saravali Ch.47 (Notes on diseases)"],
    prediction_type="trait",
)

# ═══ v.13-19½: TIMING OF ILLNESS — each age gets its own rule ════════════════

# v.13: Illness throughout life
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": "any"},
        {"type": "planets_conjunct", "planets": ["Saturn", "Rahu"]},
    ],
    signal_group="saturn_rahu_h6_malefic_illness_lifelong",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "afflicted_by_illness_throughout_life",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.17 v.13",
    description=(
        "The native will be afflicted by illness throughout life if Saturn "
        "is with Rahu while the 6th lord and 6th house are conjunct malefics."
    ),
    concordance_texts=[],
)

# v.14: Severe fever at age 6 and 12
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Mars", "house": 6},
        {"type": "lord_in_house", "lord_of": 6, "house": 8},
    ],
    signal_group="mars_h6_h6_lord_h8_fever_6_12",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "severe_fever_at_age_6_and_12",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age_range", "value": [6, 12], "precision": "exact"},
    verse_ref="Ch.17 v.14",
    description=(
        "One will suffer from severe fever at the age of 6 and at the age "
        "of 12 if Mars is in the 6th while the 6th lord is in the 8th."
    ),
    concordance_texts=[],
)

# v.15: Leprosy at age 19 and 22
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": 6},
    ],
    signal_group="jupiter_h6_moon_sag_pisces_leprosy_19_22",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "leprosy_at_age_19_and_22",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age_range", "value": [19, 22], "precision": "exact"},
    verse_ref="Ch.17 v.15",
    description=(
        "If the Moon is in Sagittarius/Pisces while Jupiter is in the 6th "
        "from the ascendant, one will suffer from leprosy at the age of "
        "19 and 22."
    ),
    modifiers=[{"condition": "moon_in_sagittarius_or_pisces", "effect": "conditionalizes", "strength": "strong"}],
    concordance_texts=[],
)

# v.16: Consumption at age 26
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Rahu", "house": 6},
    ],
    signal_group="rahu_h6_consumption_26",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "consumption_at_age_26",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age", "value": 26, "precision": "approximate"},
    verse_ref="Ch.17 v.16",
    description=(
        "If Rahu is in the 6th, ascendant lord is in the 8th and Mandi "
        "is in an angle, consumption will trouble the native at the age "
        "of 26."
    ),
    modifiers=[
        {"condition": "ascendant_lord_in_8th", "effect": "amplifies", "strength": "strong"},
        {"condition": "mandi_in_kendra", "effect": "amplifies", "strength": "moderate"},
    ],
    concordance_texts=[],
)

# v.17: Spleenary disorders at age 29 and 30
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 6, "house": 12},
        {"type": "lord_in_house", "lord_of": 12, "house": 6},
    ],
    signal_group="h6_h12_exchange_spleen_29_30",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "spleenary_disorders_at_age_29_and_30",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [29, 30], "precision": "approximate"},
    verse_ref="Ch.17 v.17",
    description=(
        "Spleenary disorders will be experienced at the age of 29 and 30 "
        "if the lords of 6th and 12th are in exchange of their signs."
    ),
    concordance_texts=[],
)

# v.18: Blood leprosy at age 45
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 6},
        {"type": "planet_in_house", "planet": "Moon", "house": 6},
    ],
    signal_group="saturn_moon_h6_leprosy_45",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "blood_leprosy_at_age_45",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age", "value": 45, "precision": "approximate"},
    verse_ref="Ch.17 v.18",
    description=(
        "Saturn and the Moon together in the 6th will inflict blood "
        "leprosy at the age of 45."
    ),
    concordance_texts=[],
)

# v.19: Windy disorders (rheumatism) at age 59
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": 1},
    ],
    signal_group="asc_lord_inimical_windy_59",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "windy_disorders_rheumatism_at_age_59",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 59, "precision": "approximate"},
    verse_ref="Ch.17 v.19",
    description=(
        "If Saturn is with an inimical planet while the ascendant lord "
        "is in the ascendant itself, windy disorders (like rheumatism) "
        "will trouble the native at the age of 59."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "saturn_with_inimical_planet", "effect": "conditionalizes", "strength": "moderate"}],
)

# ═══ v.20: Troubled by animals at age 8 ══════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": 6},
    ],
    signal_group="h8_lord_h6_moon_animals_8",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "troubled_by_animals_at_age_8",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    timing_window={"type": "age", "value": 8, "precision": "approximate"},
    verse_ref="Ch.17 v.20",
    description=(
        "Moon conjuncts 6th lord while the 8th lord is in the 6th and the "
        "12th lord is in the ascendant: the native will be troubled by "
        "animals at the age of eight."
    ),
    concordance_texts=[],
)

# ═══ v.20-22: Danger from water at ages 5 and 9 ═════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Sun", "house": [6, 8]},
    ],
    signal_group="sun_h6_h8_water_danger_5_9",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health", "longevity"],
    predictions=[
        {"entity": "native", "claim": "danger_through_water_at_ages_5_and_9",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [5, 9], "precision": "approximate"},
    verse_ref="Ch.17 v.20-22",
    description=(
        "Danger through water will have to be feared during the 5th and "
        "the 9th years if the Sun is in the 6th or 8th while the Moon "
        "is in the 12th from the said Sun."
    ),
    concordance_texts=[],
)

# v.22: Smallpox at age 10 and 30
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 8},
        {"type": "planet_in_house", "planet": "Mars", "house": 7},
    ],
    signal_group="saturn_h8_mars_h7_smallpox_10_30",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "smallpox_at_age_10_and_30",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [10, 30], "precision": "approximate"},
    verse_ref="Ch.17 v.22",
    description=(
        "Saturn in the 8th as Mars is in the 7th will cause smallpox "
        "in the 10th year and 30th year of age."
    ),
    concordance_texts=[],
)

# v.22b: Urinary disorders at age 18 and 22
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 8, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="h8_lord_kendra_rahu_urinary_18_22",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "urinary_disorders_at_age_18_and_22",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age_range", "value": [18, 22], "precision": "approximate"},
    verse_ref="Ch.17 v.22",
    description=(
        "If 8th lord joins Rahu in an angle/trine from the 8th house and "
        "be in the 8th in Navamsa, the subject will be troubled by urinary "
        "disorders etc. during the 18th year and the 22nd year."
    ),
    concordance_texts=[],
)

# ═══ v.26: Loss through enemies at age 31 ════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 11, "house": 6},
        {"type": "lord_in_house", "lord_of": 6, "house": 11},
    ],
    signal_group="h11_h6_exchange_enemy_loss_31",
    direction="unfavorable", intensity="moderate",
    domains=["wealth", "enemies_litigation"],
    predictions=[
        {"entity": "native", "claim": "loss_of_wealth_through_enemies_at_31",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 31, "precision": "approximate"},
    verse_ref="Ch.17 v.26",
    description=(
        "Loss of wealth will come to pass during the 31st year if the "
        "11th and 6th lords exchange their Rasis."
    ),
    concordance_texts=[],
)

# ═══ v.27: Inimical sons ═════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 5, "house": 6},
        {"type": "lord_in_house", "lord_of": 12, "house": 1},
    ],
    entity_target="children",
    signal_group="h5_lord_h6_inimical_sons",
    direction="unfavorable", intensity="moderate",
    domains=["enemies_litigation"],
    predictions=[
        {"entity": "children", "claim": "own_sons_will_be_enemies",
         "domain": "enemies_litigation", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.17 v.27",
    description=(
        "One's own sons will be his enemies if the 5th lord is in the 6th "
        "while the 6th lord is with Jupiter. Simultaneously the 12th lord "
        "should be in the ascendant."
    ),
    concordance_texts=[],
    modifiers=[{"condition": "h6_lord_with_jupiter", "effect": "conditionalizes", "strength": "moderate"}],
)

# ═══ v.28: Fear from dogs at age 10 and 19 ═══════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": "any"},
        {"type": "lord_in_house", "lord_of": 6, "house": "any"},
    ],
    signal_group="asc_h6_exchange_dogs_10_19",
    direction="unfavorable", intensity="weak",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "fear_from_dogs_at_age_10_and_19",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.4},
    ],
    timing_window={"type": "age_range", "value": [10, 19], "precision": "approximate"},
    verse_ref="Ch.17 v.28",
    description=(
        "There will be fear from dogs during the 10th and 19th year "
        "if the ascendant lord and the 6th lord are in exchange."
    ),
    concordance_texts=[],
)

BPHS_V2_CH17_REGISTRY = b.build()
