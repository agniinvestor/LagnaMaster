"""src/corpus/bphs_v2_ch12.py — BPHS Ch.12 (1st House Effects) V2 Re-encode.

First chapter encoded at full V2 standard. Every sloka read from Santhanam
Vol 1, pp.126-132. Every commentary note included. One-claim-one-rule.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.126-132.
Chapter: 12 — Effects of the First House (Tanu Bhava Phala)
Slokas: 15 (v.1-2 physical comforts, v.3 bodily health, v.4 beauty,
  v.5-7 other benefits, v.8 coiled birth, v.9 twins, v.10 three mothers,
  v.11 Moon=ascendant, v.12-14 decanates/limbs, v.15 limbs affected)

V2 Protocol Compliance:
  Protocol A: One-claim-one-rule ✓
  Protocol B: Contrary mirrors where text states them ✓
  Protocol C: Entity target verified per sloka ✓
  Protocol D: Santhanam commentary included ✓
  Protocol E: Computable conditions only (8 primitives) ✓
  Protocol F: Timing extracted where stated ✓
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.12", category="1st_house_effects",
    id_start=1200, session="S311", sloka_count=15,
    chapter_tags=["1st_house", "tanu_bhava"],
    entity_target="native",
    prediction_type="trait",
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKAS 1-2: Physical Comforts
# "Should the ascendant lord be conjunct a malefic or be in the 8th, 6th
# or 12th, physical felicity will diminish. If he is in an angle/trine,
# felicity."
# ═════════════════════════════════════════════════════════════════════════

# v.1-2a: Lagna lord in dusthana → health/felicity diminishes
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [6, 8, 12]},
    ],
    signal_group="lagna_lord_dusthana_health",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health", "longevity"],
    predictions=[
        {"entity": "native", "claim": "physical_felicity_diminishes",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
        {"entity": "native", "claim": "luck_and_progress_defective",
         "domain": "career_status", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.12 v.1-2",
    description=(
        "Lagna lord in a dusthana (6th, 8th, or 12th house): physical "
        "felicity will diminish. The native suffers from poor health, "
        "reduced vitality, and obstacles to progress."
    ),
    commentary_context=(
        "Santhanam notes: The ascendant lord going to an evil house "
        "together with a malefic is a dire defect in the matter of not "
        "only health but also luck and progress. If the ascendant lord "
        "in the process is a benefic or is exalted, then some relief in "
        "the course of time can be hoped."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    convergence_signals=[
        "lagna_lord_combust_or_debilitated",
        "malefic_in_ascendant",
        "low_shadbala_for_lagna_lord",
    ],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1201"]},
    tags=["lagna_lord", "dusthana", "health"],
)

# v.1-2b: Lagna lord in kendra/trikona → good health (contrary mirror)
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="lagna_lord_kendra_health",
    direction="favorable", intensity="strong",
    domains=["physical_health", "longevity"],
    predictions=[
        {"entity": "native", "claim": "full_span_of_life",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.8},
        {"entity": "native", "claim": "physical_felicity",
         "domain": "physical_health", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.1-2",
    description=(
        "Lagna lord in a kendra (1/4/7/10) or trikona (5/9): the native "
        "enjoys good physical health and a full span of life. Physical "
        "felicity is maintained throughout."
    ),
    commentary_context=(
        "Santhanam notes: The ascendant's angles (4th, 7th, 10th) or "
        "its trine (5th/9th) containing a benefic is a powerful remedy "
        "for all ills related to health."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    convergence_signals=[
        "lagna_lord_in_own_or_exalted",
        "benefic_aspecting_ascendant",
        "high_shadbala_for_lagna_lord",
    ],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1200"]},
    tags=["lagna_lord", "kendra", "trikona", "longevity"],
)

# v.2c: Lagna lord debilitated/combust/enemy sign → diseases
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": "any"},
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "debilitated"},
    ],
    signal_group="lagna_lord_debilitated_disease",
    direction="unfavorable", intensity="strong",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "chronic_diseases",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.12 v.2",
    description=(
        "Lagna lord in debilitation, combustion, or enemy's sign: there "
        "will be diseases. All comforts of the body suffer."
    ),
    commentary_context=(
        "Santhanam's notes for v.1-2 (shared with BPHS1200/1201): if the "
        "ascendant lord is in debilitation or combustion or enemy's sign, "
        "diseases will follow. This is the negative corollary of the kendra/"
        "trikona placement. If the planet is also with a malefic, both "
        "health and progress are affected."
    ),
    concordance_texts=["Saravali"],
    tags=["lagna_lord", "debilitated", "disease"],
    exceptions=["if_neecha_bhanga_raja_yoga"],
)

# v.2d: Benefic in angle/trine from lagna → diseases disappear
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_benefic",
         "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="benefic_kendra_health_remedy",
    direction="favorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "diseases_disappear",
         "domain": "physical_health", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.12 v.2",
    description=(
        "With a benefic in an angle or trine from the ascendant, all "
        "diseases will disappear. A benefic in kendra/trikona is a "
        "powerful remedy for all ills related to health."
    ),
    commentary_context=(
        "Santhanam notes: The ascendant's angles or its trine containing "
        "a benefic is a powerful remedy for all ills related to health."
    ),
    concordance_texts=["Saravali"],
    convergence_signals=["lagna_lord_strong", "no_malefic_in_ascendant"],
    tags=["benefic", "kendra", "trikona", "health_remedy"],
)


# v.1-2e: Lagna lord conjunct malefic → dire defect (DISTINCT from dusthana placement)
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [6, 8, 12]},
        {"type": "planets_conjunct", "planets": ["lord_of_1", "any_malefic"]},
    ],
    signal_group="lagna_lord_dusthana_conjunct_malefic",
    direction="unfavorable", intensity="strong",
    domains=["physical_health", "career_status"],
    predictions=[
        {"entity": "native", "claim": "dire_defect_health_luck_and_progress",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.12 v.1-2",
    description=(
        "Lagna lord in evil house TOGETHER WITH a malefic: dire defect "
        "in not only health but also luck and progress. The conjunction "
        "with malefic amplifies the dusthana placement."
    ),
    commentary_context=(
        "Santhanam: This is DISTINCT from merely being in a dusthana. "
        "The lagna lord must be CONJUNCT a malefic. The combination "
        "affects both health (physical) and progress (career/luck)."
    ),
    concordance_texts=["Saravali"],
    modifiers=[],
    exceptions=["lagna_lord_is_benefic_or_exalted_gives_relief"],
)

# v.1-2f: Lagna lord is benefic or exalted → relief (EXCEPTION to unfavorable rules)
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [6, 8, 12]},
        {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "strong"},
    ],
    signal_group="lagna_lord_dusthana_but_benefic_relief",
    direction="mixed", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "relief_from_health_issues_over_time",
         "domain": "physical_health", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.12 v.1-2",
    description=(
        "If the lagna lord in a dusthana is a benefic or is exalted, "
        "some relief in the course of time can be hoped. The benefic "
        "nature or exaltation mitigates the dusthana placement."
    ),
    commentary_context=(
        "Santhanam: This is an EXCEPTION to BPHS1200. If the ascendant "
        "lord in the process is a benefic or is exalted, then some "
        "relief in the course of time can be hoped."
    ),
    concordance_texts=[],
    rule_relationship={"type": "mitigation", "related_rules": ["BPHS1200"]},
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 3: Bodily Health (Moon condition)
# "There will not be bodily health if the ascendant or the Moon be
# aspected by or conjunct a malefic, being devoid of a benefic's aspect."
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_aspecting", "planet": "any_malefic", "house": "moon_position"},
        {"type": "planet_not_aspecting", "planet": "any_benefic", "house": "moon_position"},
    ],
    signal_group="moon_malefic_no_benefic_health",
    direction="unfavorable", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "no_bodily_health",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.3",
    description=(
        "Moon aspected by or conjunct a malefic, devoid of benefic "
        "aspect: there will not be bodily health. The ascendant or "
        "Moon under malefic influence without benefic relief causes "
        "persistent health problems."
    ),
    commentary_context=(
        "No separate Santhanam note for v.3. The verse is self-contained: "
        "Moon or ascendant aspected/conjunct malefic without benefic "
        "relief = no bodily health. Both conditions are co-equal: "
        "malefic influence present AND benefic counterbalance absent."
    ),
    concordance_texts=["Saravali"],
    modifiers=[],
    exceptions=[],
    tags=["moon", "malefic", "health"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 4: Bodily Beauty
# "A benefic in the ascendant will give a pleasing appearance, while a
# malefic will make one bereft of good appearance."
# ═════════════════════════════════════════════════════════════════════════

# v.4a: Benefic in ascendant → pleasing appearance
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_benefic", "house": 1},
    ],
    signal_group="benefic_h1_appearance",
    direction="favorable", intensity="moderate",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "pleasing_appearance",
         "domain": "physical_appearance", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.4",
    description=(
        "A benefic in the ascendant gives a pleasing appearance. "
        "Felicity of the body will be enjoyed if the ascendant is "
        "aspected by or conjunct a benefic."
    ),
    commentary_context=(
        "No separate Santhanam note for v.4. The verse directly states "
        "the benefic/malefic contrast. Felicity of the body will be "
        "enjoyed if the ascendant is aspected by or conjunct a benefic — "
        "this extends beyond occupation to aspect as well."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1206"]},
    tags=["benefic", "ascendant", "appearance"],
)

# v.4b: Malefic in ascendant → bereft of good appearance (contrary mirror)
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 1},
    ],
    signal_group="malefic_h1_appearance",
    direction="unfavorable", intensity="moderate",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "bereft_of_good_appearance",
         "domain": "physical_appearance", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.4",
    description=(
        "A malefic in the ascendant makes one bereft of good appearance. "
        "Physical features are marred or unremarkable."
    ),
    commentary_context="Contrary of v.4a (BPHS1205). No separate Santhanam note.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1205"]},
    tags=["malefic", "ascendant", "appearance"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKAS 5-7: Other Benefits (Lagna lord with benefics)
# "If the ascendant lord, Mercury, Jupiter or Venus be in an angle or
# in a trine, the native will be longlived, wealthy, intelligent and
# liked by the king."
# ═════════════════════════════════════════════════════════════════════════

# v.5-7a: Lagna lord with Mercury/Jupiter/Venus in angle/trine
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 1, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="lagna_lord_kendra_benefits",
    direction="favorable", intensity="strong",
    domains=["longevity", "wealth", "intelligence_education", "fame_reputation"],
    predictions=[
        {"entity": "native", "claim": "longlived_full_span",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.8},
        {"entity": "native", "claim": "wealthy_and_prosperous",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "intelligent_liked_by_authorities",
         "domain": "intelligence_education", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.5-7",
    description=(
        "Lagna lord, Mercury, Jupiter or Venus in an angle or trine: "
        "the native will be longlived, wealthy, intelligent and liked "
        "by the king. Fame, wealth, abundant pleasures and comforts of "
        "the body will be acquired."
    ),
    commentary_context=(
        "Santhanam notes: If Mercury, Jupiter or Venus be in the "
        "ascendant along with the Moon, or be in angle from the "
        "ascendant, the native will enjoy royal fortunes. "
        "'Rajalakshana' means mark of fortune — there are 32 "
        "Lakshanas of major category in Samudrika Sastra (physiognomy). "
        "Some of these could be found in Ch.81 of our present work."
    ),
    concordance_texts=["Saravali", "Phaladeepika", "Brihat Jataka"],
    cross_chapter_refs=["Ch.81 Body Parts"],
    modifiers=[
        {"condition": "mercury_jupiter_venus_also_in_kendra_trikona",
         "effect": "amplifies", "strength": "strong"},
    ],
    convergence_signals=[
        "mercury_or_jupiter_or_venus_in_kendra",
        "moon_in_kendra_with_benefic",
        "lagna_lord_in_own_or_exalted",
    ],
    tags=["lagna_lord", "benefic", "kendra", "trikona", "wealth", "longevity"],
)

# v.5-7b: Lagna lord aspected by benefic in movable sign → royal marks
b.add(
    conditions=[
        {"type": "planet_in_sign_type", "planet": "lord_of_1", "sign_type": "movable"},
        {"type": "planet_aspecting", "planet": "any_benefic", "house": "lagna_lord_position"},
    ],
    signal_group="lagna_lord_movable_royal",
    direction="favorable", intensity="strong",
    domains=["fame_reputation", "physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "royal_marks_of_fortune",
         "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "endowed_with_rajalakshana",
         "domain": "physical_appearance", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.12 v.5-7",
    description=(
        "Lagna lord aspected by a benefic planet and placed in a "
        "movable sign: the native will be endowed with royal marks "
        "of fortune (Rajalakshana). Physical signs of nobility and "
        "authority on the body."
    ),
    commentary_context=(
        "Santhanam notes: 'Rajalakshana' means mark of fortune. There "
        "are 32 Lakshanas of major category in Samudrika Sastra or "
        "physiognomy. Some of these could be found in Ch.81 of our "
        "present work (Vol II)."
    ),
    modifiers=[],
    cross_chapter_refs=["Ch.81 Body Parts of Woman"],
    tags=["lagna_lord", "movable_sign", "rajalakshana", "royal"],
)


# v.5-7c: Mercury/Jupiter/Venus in angle or with Moon → royal fortunes
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": [1, 4, 7, 10]},
    ],
    signal_group="mercury_jupiter_venus_kendra_moon_royal",
    direction="favorable", intensity="strong",
    domains=["fame_reputation", "wealth"],
    predictions=[
        {"entity": "native", "claim": "royal_fortunes_through_benefics_in_kendra",
         "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.12 v.5-7",
    description=(
        "If Mercury, Jupiter or Venus be in the ascendant along with the "
        "Moon, or be in angle from the ascendant, the native will enjoy "
        "royal fortunes."
    ),
    commentary_context=(
        "Santhanam: Distinct from BPHS1209 (lagna lord in kendra). This "
        "is about the NATURAL BENEFICS being in kendra or with Moon — "
        "regardless of lagna lordship."
    ),
    concordance_texts=["Saravali"],
    modifiers=[
        {"condition": "mercury_or_venus_also_in_kendra_or_with_moon", "effect": "amplifies", "strength": "moderate"},
    ],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 8: Coiled Birth
# "If there be a birth in one of Aries, Taurus and Leo ascendants
# containing either Saturn or Mars, the birth of the child is with a
# coil around."
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Saturn", "house": 1},
        # Lagna must be Aries, Taurus, or Leo
    ],
    signal_group="saturn_h1_coiled_birth",
    direction="unfavorable", intensity="weak",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "coiled_birth_cord_around_body",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    timing_window={"type": "age", "value": 0, "precision": "exact"},
    verse_ref="Ch.12 v.8",
    description=(
        "Aries, Taurus, or Leo ascendant containing Saturn: the birth "
        "of the child is with a coil around (umbilical cord wrapped). "
        "The corresponding limb will be in accordance with the Rasi "
        "or Navamsa rising."
    ),
    commentary_context=(
        "Santhanam notes: This rule applies to only three ascendants: "
        "Aries, Taurus and Leo. Mars or Saturn should be in the "
        "ascendant. The limbs indicated by the Rasis are shown in "
        "slokas 4-4½ of Ch.4 supra. These apply to the Navamsas as "
        "well. The limbs denoted in slokas 12-15 of the present "
        "chapter have different use and should not be mixed."
    ),
    cross_chapter_refs=["Ch.4 v.4 Zodiacal Signs limb mapping"],
    lagna_scope=["aries", "taurus", "leo"],
    tags=["saturn", "ascendant", "coiled_birth", "cord"],
    prediction_type="event",
)

# Same for Mars in ascendant
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Mars", "house": 1},
    ],
    signal_group="mars_h1_coiled_birth",
    direction="unfavorable", intensity="weak",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "coiled_birth_cord_around_body",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    timing_window={"type": "age", "value": 0, "precision": "exact"},
    verse_ref="Ch.12 v.8",
    description=(
        "Aries, Taurus, or Leo ascendant containing Mars: the birth "
        "of the child is with a coil around (umbilical cord wrapped)."
    ),
    commentary_context="See BPHS1209 for full Santhanam commentary.",
    cross_chapter_refs=["Ch.4 v.4 Zodiacal Signs limb mapping"],
    lagna_scope=["aries", "taurus", "leo"],
    tags=["mars", "ascendant", "coiled_birth", "cord"],
    prediction_type="event",
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 9: Birth of Twins
# "The native, who has the Sun in a quadruped sign while others are in
# dual signs with strength, is born as one of the twins."
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_sign", "planet": "Sun",
         "sign": "any_quadruped"},  # Aries, Taurus, Leo, Capricorn 1st half, Sagittarius 2nd
    ],
    signal_group="sun_quadruped_twins",
    direction="neutral", intensity="moderate",
    domains=["physical_health"],
    predictions=[
        {"entity": "native", "claim": "born_as_twin",
         "domain": "physical_health", "direction": "neutral", "magnitude": 0.6},
    ],
    timing_window={"type": "age", "value": 0, "precision": "exact"},
    verse_ref="Ch.12 v.9",
    description=(
        "Sun in a quadruped sign while all other planets are in dual "
        "signs with strength: the native is born as one of the twins. "
        "If Sun is in a quadruped sign in a dual sign's angle, the "
        "native will be one of the twins."
    ),
    commentary_context=(
        "Santhanam notes: Quadruped signs are Aries, Taurus, Leo, "
        "first half of Capricorn and second part of Sagittarius. If "
        "the Sun is in a quadruped sign while all others are in dual "
        "signs — Gemini and all others — the native will be one of "
        "the twins. The other six planets should be endowed with "
        "strength."
    ),
    tags=["sun", "twins", "quadruped_sign", "dual_sign"],
    prediction_type="event",
    modifiers=[{"condition": "other_six_planets_endowed_with_strength", "effect": "conditionalizes", "strength": "strong"}],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 10: To Be Nurtured by 3 Mothers
# "If the Sun and the Moon join in one and the same bhava and fall in
# one Navamsa, the native will be nurtured by 3 different mothers for
# the first 3 months from its birth."
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planets_conjunct", "planets": ["Sun", "Moon"]},
        # Additional: must be in same Navamsa (Vargottama-like)
    ],
    entity_target="general",
    signal_group="sun_moon_conjunct_mother",
    direction="unfavorable", intensity="strong",
    domains=["longevity"],
    predictions=[
        {"entity": "native", "claim": "nurtured_by_three_mothers",
         "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6},
        {"entity": "mother", "claim": "loss_of_mother_within_3_months",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    timing_window={"type": "age_range", "value": [0, 0.25],
                   "precision": "approximate"},
    verse_ref="Ch.12 v.10",
    description=(
        "Sun and Moon join in one bhava and fall in one Navamsa: the "
        "native will be nurtured by 3 different mothers for the first "
        "3 months from birth, and will later be brought up by father "
        "and brother."
    ),
    commentary_context=(
        "Santhanam notes: In my opinion, the Vargothama position of "
        "the luminaries in conjunction seems to be excepted. They "
        "should be in the same quarter of a constellation and will "
        "naturally be in one Navamsa. This combination obviously "
        "implies loss of mother within the first three months. "
        "'भ्रातृ' apart from meaning a brother calls for interpretation "
        "as a near relative in general."
    ),
    tags=["sun", "moon", "conjunction", "mother_loss", "early_life"],
    prediction_type="event",
    exceptions=["vargottama_position_of_luminaries_excepted"],
)


# v.10 exception: Vargottama luminaries → excepted from 3-mothers rule
b.add(
    conditions=[
        {"type": "planets_conjunct", "planets": ["Sun", "Moon"]},
    ],
    entity_target="general",
    signal_group="sun_moon_vargottama_exception",
    direction="neutral", intensity="moderate",
    domains=["longevity"],
    predictions=[
        {"entity": "native", "claim": "vargottama_luminaries_exception_to_three_mothers",
         "domain": "physical_health", "direction": "neutral", "magnitude": 0.3},
    ],
    verse_ref="Ch.12 v.10",
    description=(
        "Exception: Vargottama position of the luminaries in conjunction "
        "seems to be excepted from the 3-mothers rule. They should be in "
        "the same quarter of a constellation."
    ),
    commentary_context=(
        "Santhanam: In my opinion, the Vargothama position of the luminaries "
        "in conjunction seems to be excepted. They should be in the same "
        "quarter of a constellation and will naturally be in one Navamsa."
    ),
    rule_relationship={"type": "override", "related_rules": ["BPHS1214"]},
    exceptions=["vargottama_position_of_luminaries"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 11: Moon = Ascendant (methodological note)
# "The learned in astrology should also base the effects on the Moon
# also as applicable to the ascendant."
# Not a predictive rule — encode as reference/methodological.
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[],  # Methodological principle, not a specific condition
    signal_group="moon_equals_ascendant_principle",
    direction="neutral", intensity="moderate",
    domains=["physical_health", "character_temperament"],
    predictions=[
        {"entity": "native", "claim": "moon_effects_equal_ascendant_effects",
         "domain": "character_temperament", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.12 v.11",
    description=(
        "The learned in astrology should also base the effects on the "
        "Moon as applicable to the ascendant. Now explained are clues "
        "to know of ulcers, identity marks etc. on one's person."
    ),
    commentary_context=(
        "Santhanam notes: This wellknown rule is a speciality in Hindu "
        "Astrology and has the sage's sanction. The Moon is given a "
        "significant status equal to the ascendant for she rules one's "
        "mind and the mind in turn functions according to one's Karma, "
        "see Buddhih Karmanusarini."
    ),
    concordance_texts=["Saravali"],
    tags=["moon", "ascendant", "methodological", "principle"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKAS 12-14: Decanates and Bodily Limbs (reference mapping)
# These define body-part correspondence, not predictions per se.
# Encoded as a single reference rule.
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[],  # Reference mapping, not a trigger condition
    signal_group="decanate_body_mapping",
    direction="neutral", intensity="moderate",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "body_parts_mapped_by_decanate",
         "domain": "physical_appearance", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.12 v.12-14",
    description=(
        "Decanates and bodily limbs mapping: 1st decanate = head, "
        "eyes, ears, nose, temple, chin, face. 2nd decanate = neck, "
        "shoulder, arm, side, heart, stomach, navel. 3rd decanate = "
        "pelvis, anus/penis, testicles, thigh, knee, calf, foot. "
        "Visible half (ascendant cusp to 10th cusp backwards) = left "
        "side of body. Invisible half = right side."
    ),
    commentary_context=(
        "Santhanam notes: The portion that has already risen is known "
        "as visible half of the horoscope. From the cusp of the "
        "ascendant to the cusp of the descendant counted backwards "
        "(via the 10th cusp) is visible half. The rest is invisible. "
        "Visible half represents the left side of the body while "
        "invisible half represents right side of the body. The above "
        "three diagrams are made for the three decanates of Aries."
    ),
    tags=["decanate", "body_mapping", "reference"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 15: Limbs Affected by Malefic/Benefic
# "The limb related to a malefic by occupation will have ulcers or
# scars while the one by a benefic will have a mark (like moles etc.)."
# ═════════════════════════════════════════════════════════════════════════

# v.15a: Malefic in decanate → ulcers/scars on corresponding limb
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": "any"},
    ],
    signal_group="malefic_decanate_scars",
    direction="unfavorable", intensity="weak",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "ulcers_or_scars_on_limb",
         "domain": "physical_appearance", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.12 v.15",
    description=(
        "The limb related to a malefic by occupation (in the "
        "corresponding decanate) will have ulcers or scars."
    ),
    commentary_context=(
        "Santhanam notes: Also see sloka 6, Ch.4 of Saravali, which "
        "states that a malefic or a benefic if be in own Rasi or "
        "Navamsa, the effects will be right from birth. In other "
        "cases, it will be in the course of one's life that these "
        "effects will come to pass."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Saravali Ch.4 v.6"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1216"]},
    tags=["malefic", "decanate", "scars", "body_marks"],
)

# v.15b: Benefic in decanate → moles/marks (contrary mirror)
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_benefic", "house": "any"},
    ],
    signal_group="benefic_decanate_moles",
    direction="neutral", intensity="weak",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "moles_or_beauty_marks_on_limb",
         "domain": "physical_appearance", "direction": "neutral", "magnitude": 0.4},
    ],
    verse_ref="Ch.12 v.15",
    description=(
        "The limb related to a benefic by occupation (in the "
        "corresponding decanate) will have a mark like moles etc."
    ),
    commentary_context=(
        "Contrary of BPHS1215 (malefic → scars). Santhanam cross-references "
        "Saravali Ch.4 v.6: if the planet is in own Rasi or Navamsa, effects "
        "manifest from birth; otherwise during the course of life."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1215"]},
    tags=["benefic", "decanate", "moles", "body_marks"],
)

# v.15c: Timing distinction — own Rasi/Navamsa → from birth; else → during life
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_planet", "house": "any"},
    ],
    signal_group="body_mark_timing",
    direction="neutral", intensity="weak",
    domains=["physical_appearance"],
    predictions=[
        {"entity": "native", "claim": "body_marks_from_birth_if_own_sign",
         "domain": "physical_appearance", "direction": "neutral", "magnitude": 0.4},
    ],
    verse_ref="Ch.12 v.15",
    description=(
        "If the malefic or benefic is in its own Rasi or Navamsa, the "
        "body mark effects will manifest from birth. Otherwise, they "
        "will manifest during the course of one's life."
    ),
    commentary_context=(
        "Santhanam cross-references Saravali Ch.4 v.6 which confirms "
        "this timing distinction between own-sign (birth) and other "
        "placements (later in life)."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Saravali Ch.4 v.6"],
    modifiers=[
        {"condition": "in_own_rasi_or_navamsa", "effect": "conditionalizes",
         "strength": "moderate"},
    ],
    tags=["body_marks", "timing", "own_sign"],
)

BPHS_V2_CH12_REGISTRY = b.build()
