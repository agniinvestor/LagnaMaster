"""src/corpus/bphs_v2_ch18.py — BPHS Ch.18 (7th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.160-169.
Chapter: 18 — Effects of the Seventh House (Yuvati Bhava Phala)
Slokas: 42. MOST timing-rich chapter. Marriage ages: 5-34. Wife death ages: 13-33.
Entity: spouse (most), native (some for marriage timing).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.18", category="7th_house_effects",
    id_start=1800, session="S311", sloka_count=42,
    chapter_tags=["7th_house", "yuvati_bhava"],
    entity_target="spouse",
)

# ═══ v.1: Full happiness through wife ════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"}],
    signal_group="h7_lord_strong_happy_marriage",
    direction="favorable", intensity="strong", domains=["marriage"],
    predictions=[{"entity": "spouse", "claim": "full_happiness_through_wife",
                  "domain": "marriage", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.1",
    commentary_context="Santhanam: Saturn in Capricorn for Leo native or Venus in Pisces for Aries native need not be feared — exaltation placement overrides natural malefic status.",
    description="7th lord in own sign or exaltation: full happiness through wife and marriage.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1801"]},
)

# ═══ v.2: Sick wife ══════════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]}],
    signal_group="h7_lord_dusthana_sick_wife",
    direction="unfavorable", intensity="moderate", domains=["marriage", "physical_health"],
    predictions=[{"entity": "spouse", "claim": "wife_will_be_sickly",
                  "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.2",
    description="7th lord in 6th, 8th or 12th: the wife will be sickly.",
    commentary_context="Does not apply to own house or exaltation placement. Venus in exaltation in 7th house for Aries native need not be feared.",
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1800"]},
)

# ═══ v.3: Excessive libidinousness / death of wife ═══════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 7}],
    signal_group="venus_h7_libidinous",
    direction="mixed", intensity="moderate", domains=["marriage", "character_temperament"],
    predictions=[
        {"entity": "native", "claim": "exceedingly_libidinous",
         "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6},
        {"entity": "spouse", "claim": "death_of_wife_if_venus_joins_malefic",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.5},
    ],
    entity_target="general",
    verse_ref="Ch.18 v.3",
    commentary_context="Santhanam: Venus in 7th makes native exceedingly libidinous. Venus joining a malefic in any house causes loss of wife — not just in the 7th.",
    description="Venus in 7th: native exceedingly libidinous. Venus joining a malefic in any house will cause loss of wife.",
    concordance_texts=["Saravali"],
)

# ═══ v.4-5: 7th lord strong + benefic → wealthy, honourable ══════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [1, 4, 5, 7, 9, 10]},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"}],
    signal_group="h7_lord_kendra_strong_wealthy",
    direction="favorable", intensity="strong", domains=["marriage", "wealth"],
    predictions=[
        {"entity": "native", "claim": "wealthy_honourable_happy_fortunate",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    entity_target="native",
    verse_ref="Ch.18 v.4-5",
    description="7th lord endowed with strength, conjunct/aspected by benefic: native wealthy, honourable, happy and fortunate.",
    commentary_context="Plurality of wives and sickness to them will come from the 7th lord occupying his sign of debilitation or having got combust or inimical placement.",
    concordance_texts=["Saravali"],
)

# ═══ v.6: Plurality of wives ═════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"}],
    signal_group="h7_lord_saturn_venus_sign_many_wives",
    direction="neutral", intensity="moderate", domains=["marriage"],
    predictions=[{"entity": "native", "claim": "many_wives",
                  "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
    entity_target="native",
    verse_ref="Ch.18 v.6",
    commentary_context="No separate Santhanam note for v.6. 7th lord in Saturn/Venus sign + benefic aspect = many wives. Exaltation produces same result.",
    description="7th lord in a sign of Saturn or Venus, aspected by a benefic: there will be many wives. 7th lord in exaltation → same effect.",
    concordance_texts=[],
    modifiers=[{"condition": "in_saturn_or_venus_sign", "effect": "conditionalizes", "strength": "moderate"},
               {"condition": "aspected_by_benefic", "effect": "amplifies", "strength": "moderate"}],
)

# ═══ v.14-15: Worthy spouse ══════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "exalted"}],
    signal_group="h7_lord_exalted_worthy_spouse",
    direction="favorable", intensity="strong", domains=["marriage", "progeny"],
    predictions=[
        {"entity": "spouse", "claim": "spouse_with_seven_principal_virtues",
         "domain": "marriage", "direction": "favorable", "magnitude": 0.8},
        {"entity": "children", "claim": "sons_and_grandsons",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    entity_target="general",
    verse_ref="Ch.18 v.14-15",
    commentary_context="Santhanam: The above verses hint at the possibility of native obtaining children and grandchildren if the ascendant lord with strength is in the 7th with a benefic as the 7th lord is disposed in exaltation sign.",
    description="7th lord exalted + 7th with benefic + strong ascendant lord and benefic: spouse endowed with seven principal virtues, expanding dynasty by sons and grandsons.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "ascendant_lord_with_strength_in_7th_with_benefic", "effect": "conditionalizes", "strength": "strong"}],
)

# ═══ v.17: Loss of spouse (early death) ══════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "weak"}],
    signal_group="h7_lord_dusthana_weak_wife_death",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_destroyed_early_death",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.17",
    commentary_context="Santhanam: If the 7th lord is in fall, the native's wife will be destroyed (i.e. she will die early). The placement in 6th/8th/12th compounds this.",
    description="7th lord devoid of strength in 6th/8th/12th or if 7th lord is in fall: the native's wife will be destroyed (i.e. she will die early).",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "7th_lord_in_fall_compounds_dusthana_placement", "effect": "amplifies", "strength": "strong"}],
)

# ═══ v.22-34: TIMING OF MARRIAGE — each age as its own rule ══════════════════

_MARRIAGE_TIMING = [
    ("Ch.18 v.22", [5, 9], "7th lord in benefic's house + Venus exalted/own sign",
     [{"type": "lord_in_house", "lord_of": 7, "house": "any"}]),
    ("Ch.18 v.23", [7, 11], "Sun in 7th + dispositor conjunct Venus",
     [{"type": "planet_in_house", "planet": "Sun", "house": 7}]),
    ("Ch.18 v.24", [10, 16], "Venus in 2nd + 7th lord in 11th",
     [{"type": "planet_in_house", "planet": "Venus", "house": 2}]),
    ("Ch.18 v.25", [11], "Venus in angle from ascendant + ascendant lord in Cap/Aqu",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.26", [12, 19], "Venus in angle + Saturn in 7th from Venus",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.27", [18], "Venus in 7th from Moon + Saturn in 7th from Venus",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.28", [15], "2nd lord in 11th + ascendant lord in 10th",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11}]),
    ("Ch.18 v.29", [13], "Exchange of 2nd and 11th lords",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11},
      {"type": "lord_in_house", "lord_of": 11, "house": 2}]),
    ("Ch.18 v.30", [22, 27], "Venus in 7th from 8th + dispositor conjunct Mars",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.31", [23, 26], "7th lord in 12th + natal asc lord in 7th Navamsa",
     [{"type": "lord_in_house", "lord_of": 7, "house": 12}]),
    ("Ch.18 v.32", [25, 33], "8th lord in 7th + Venus in Navamsa ascendant",
     [{"type": "lord_in_house", "lord_of": 8, "house": 7}]),
    ("Ch.18 v.33", [31, 33], "Venus in 9th from 5th + Rahu in one of said houses",
     [{"type": "planet_in_house", "planet": "Venus", "house": "any"}]),
    ("Ch.18 v.34", [30, 27], "Venus in ascendant + 7th lord in 7th itself",
     [{"type": "planet_in_house", "planet": "Venus", "house": 1}]),
]

for _mt_idx, (vref, ages, desc_suffix, conds) in enumerate(_MARRIAGE_TIMING):
    age_val = ages[0] if len(ages) == 1 else ages
    tw_type = "age" if len(ages) == 1 else "age_range"
    b.add(
        conditions=conds,
        entity_target="native",
        signal_group=f"marriage_timing_{ages[0]}",
        direction="favorable", intensity="moderate", domains=["marriage"],
        predictions=[{"entity": "native", "claim": f"marriage_at_age_{ages[0]}",
                      "domain": "marriage", "direction": "favorable", "magnitude": 0.5}],
        timing_window={"type": tw_type, "value": age_val, "precision": "approximate"},
        verse_ref=vref,
        commentary_context=f"Santhanam groups v.22-34 as TIMING OF MARRIAGE. Age {ages[0]} indicated by specific planetary combination. These ages may not be literal in modern context but indicate early vs late marriage." if _mt_idx > 0 else "Santhanam: The age of marriage indicated in the text will not be practical in all cases in modern social conditions. These will be simply helpful in knowing of early and belated marriages.",
        description=f"Marriage timing: {desc_suffix} → marry at age {'/'.join(str(a) for a in ages)}.",
    )

# ═══ v.35-39: TIMING OF WIFE'S DEATH ════════════════════════════════════════

_WIFE_DEATH_TIMING = [
    ("Ch.18 v.35", [18, 33], "7th lord in fall + Venus in 8th",
     [{"type": "lord_in_house", "lord_of": 7, "house": "any"},
      {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "debilitated"}]),
    ("Ch.18 v.36", [19], "7th lord in 8th + 12th lord in 7th",
     [{"type": "lord_in_house", "lord_of": 7, "house": 8},
      {"type": "lord_in_house", "lord_of": 12, "house": 7}]),
    ("Ch.18 v.38", [17, 21], "Venus in 8th + dispositor in Saturn sign",
     [{"type": "planet_in_house", "planet": "Venus", "house": 8}]),
    ("Ch.18 v.39", [13], "Ascendant lord in debilitation + 2nd lord in 8th",
     [{"type": "lord_in_house", "lord_of": 1, "house": "any"},
      {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "debilitated"}]),
]

for _wd_idx, (vref, ages, desc_suffix, conds) in enumerate(_WIFE_DEATH_TIMING):
    age_val = ages[0] if len(ages) == 1 else ages
    tw_type = "age" if len(ages) == 1 else "age_range"
    b.add(
        conditions=conds,
        signal_group=f"wife_death_{ages[0]}",
        direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
        predictions=[{"entity": "spouse", "claim": f"loss_of_wife_at_age_{ages[0]}",
                      "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
        timing_window={"type": tw_type, "value": age_val, "precision": "approximate"},
        verse_ref=vref,
        commentary_context=f"Santhanam groups v.35-39 as TIMING OF WIFE'S DEATH. Age {ages[0]} indicated. The combinations are extreme and specific — multiple afflictions required simultaneously.",
        description=f"Wife's death timing: {desc_suffix} → loss of wife at age {'/'.join(str(a) for a in ages)}.",
    )

# v.37: Wife dies within 3 days of marriage (snake bite!)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": 2},
                {"type": "planet_in_house", "planet": "Mars", "house": 7}],
    signal_group="rahu_h2_mars_h7_wife_death_3_days",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_dies_within_3_days_of_marriage_snakebite",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    timing_window={"type": "after_event", "value": "marriage", "precision": "exact"},
    verse_ref="Ch.18 v.37",
    commentary_context="Santhanam: Rahu in 2nd (maraka sthana) + Mars in 7th (marriage house) = wife dies within three days of marriage due to snake bite. Extreme and specific combination.",
    description="Rahu in 2nd + Mars in 7th: the native's wife will die within three days of marriage due to snake bite.",
    concordance_texts=[],
)

# ═══ v.42: Mars/Rahu/Saturn in 6-7-8 → wife will not live long ═══════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 6},
                {"type": "planet_in_house", "planet": "Rahu", "house": 7},
                {"type": "planet_in_house", "planet": "Saturn", "house": 8}],
    signal_group="mars_rahu_saturn_678_wife_short_life",
    direction="unfavorable", intensity="strong", domains=["marriage", "longevity"],
    predictions=[{"entity": "spouse", "claim": "wife_will_not_live_long",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.42",
    commentary_context="No separate Santhanam note. The specific ordering (Mars-6th, Rahu-7th, Saturn-8th) creates a malefic siege around the marriage house.",
    description="If the 6th, 7th and 8th are in their order occupied by Mars, Rahu and Saturn, the native's wife will not live long.",
    concordance_texts=[],
)


# ═══ v.7-8½: Miscellaneous — planets in 7th indicate type of female ══════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Sun", "house": 7}],
      entity_target="native",
      signal_group="sun_h7_barren_females", direction="unfavorable", intensity="moderate",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "befriend_barren_females_for_sexual_union", "domain": "marriage", "direction": "unfavorable", "magnitude": 0.5}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Sun in 7th = native seeks pleasures from barren females. Any planet in 7th (including 7th lord) indicates absence of sterlingness in character regarding sexual union.",
      description="Sun in 7th: native will befriend barren females for sexual union.")

b.add(conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7}],
      entity_target="native",
      signal_group="mars_h7_marriageable_girls", direction="mixed", intensity="moderate",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "associate_with_marriageable_age_females", "domain": "marriage", "direction": "mixed", "magnitude": 0.5}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Mars in 7th = female of marriageable age, or one in her monthly course, or one devoid of conceiving ability. Jupiter in 7th is also no exception.",
      description="Mars in 7th: associate with marriageable girls or those with menses.",
      modifiers=[{"condition": "jupiter_in_7th_produces_similar_effects", "effect": "amplifies", "strength": "moderate"}])

b.add(conditions=[{"type": "planet_in_house", "planet": "Mercury", "house": 7}],
      entity_target="native",
      signal_group="mercury_h7_traders_community", direction="mixed", intensity="weak",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "associate_with_mean_females_traders_community", "domain": "marriage", "direction": "mixed", "magnitude": 0.4}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Mercury = harlots, mean females, females of traders' community. The kind corresponds to the sign becoming the 7th house.",
      description="Mercury in 7th: associate with mean females or those from traders' community.")

# ═══ v.9-9½: Physical features of spouse ══════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7}],
      signal_group="mars_h7_spouse_appearance", direction="neutral", intensity="moderate",
      domains=["marriage", "physical_appearance"],
      predictions=[{"entity": "spouse", "claim": "female_with_attractive_breasts", "domain": "physical_appearance", "direction": "favorable", "magnitude": 0.4}],
      verse_ref="Ch.18 v.9",
      commentary_context="Santhanam: Mars = attractive breasts. Saturn = sick/weak spouse. Jupiter = hard/prominent breasts. Venus = bulky/excellent breasts.",
      description="Mars indicates female with attractive breasts. Saturn = sick/weak. Jupiter = hard/prominent. Venus = excellent.",
      prediction_type="trait")

# ═══ v.10-13½: Morality — spouse controlled by others ════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 12}],
      entity_target="spouse",
      signal_group="malefics_h12_moon_h5_spouse_controlled", direction="unfavorable", intensity="moderate",
      domains=["marriage", "character_temperament"],
      predictions=[{"entity": "spouse", "claim": "spouse_controlled_by_others_inimical_to_race", "domain": "marriage", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.10-13",
      commentary_context="Santhanam: 4 hints in v.10-13: 1) Moon decreasing + 5th house malefic + 12th/7th malefic = high-handed spouse. 2) Saturn/Mars in 7th = questionable character. 3) Venus in Mars Navamsa = unusual sexual habits. 4) Venus related to Saturn = ugly relations with another male.",
      description="Malefics in 12th + Moon in 5th: spouse controlled by others, inimical to family.",
      modifiers=[{"condition": "moon_decreasing_in_5th", "effect": "conditionalizes", "strength": "moderate"}])

# ═══ v.16: Evils to spouse ════════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 7}],
      entity_target="spouse",
      signal_group="malefic_h7_evils_to_spouse", direction="unfavorable", intensity="moderate",
      domains=["marriage", "physical_health"],
      predictions=[{"entity": "spouse", "claim": "wife_incur_evils_especially_if_bereft_of_strength", "domain": "physical_health", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.16",
      commentary_context="Santhanam: 7th house or its lord conjunct malefic + bereft of strength = wife incur evils. Especially if the 7th house/lord is not strong.",
      description="7th house or its lord conjunct malefic, bereft of strength: wife will incur evils.",
      modifiers=[{"condition": "7th_house_or_lord_not_strong_intensifies_evils", "effect": "amplifies", "strength": "strong"}])

# ═══ v.18: Lack of conjugal felicity ═════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 7},
                   {"type": "lord_in_house", "lord_of": 7, "house": 12}],
      entity_target="native",
      signal_group="moon_h7_h7_lord_h12_no_marital_happiness", direction="unfavorable", intensity="moderate",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "not_endowed_with_marital_happiness", "domain": "marriage", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.18",
      commentary_context="Santhanam: Moon in 7th + 7th lord in 12th + Venus (Karaka) bereft of strength = no marital happiness. Moon increasing would stall adversity.",
      description="Moon in 7th + 7th lord in 12th + Venus weak: not endowed with marital happiness.",
      modifiers=[{"condition": "venus_bereft_of_strength", "effect": "amplifies", "strength": "moderate"}])

# ═══ v.19-21: Plurality of wives ══════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 7, "house": "any"},
                   {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "debilitated"}],
      entity_target="native",
      signal_group="h7_lord_fall_two_wives", direction="neutral", intensity="moderate",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "two_wives_if_7th_lord_in_fall", "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
      verse_ref="Ch.18 v.19-21",
      commentary_context="Santhanam: 7th lord in fall + malefic sign + 7th Navamsa eunuch planet = 2 wives. Mars+Venus in 7th + Saturn + ascendant lord in 8th = 3 wives. Venus in dual sign + lord exalted + 7th lord strong = many wives. For dual marriage, 7th from natal or Navamsa ascendant should be owned by eunuch planet (Gemini, Virgo, Capricorn, Aquarius).",
      description="7th lord in fall or malefic sign, 7th Navamsa = eunuch planet: two wives. Mars+Venus+Saturn = three. Venus in dual sign = many.")

# ═══ v.40-41: Three marriages ═════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Moon", "house": "any"}],
      entity_target="native",
      signal_group="moon_venus_mercury_three_marriages", direction="neutral", intensity="moderate",
      domains=["marriage"],
      predictions=[{"entity": "native", "claim": "three_marriages_at_10_22_33", "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
      timing_window={"type": "age_range", "value": [10, 33], "precision": "approximate"},
      verse_ref="Ch.18 v.40-41",
      commentary_context="Santhanam: Moon in 7th from Venus + Mercury in 7th from Moon + 8th lord in 5th = 3 marriages. Marriage in 10th year, another in 22nd year, another in 33rd year.",
      description="Moon in 7th from Venus + Mercury in 7th from Moon + 8th lord in 5th: three marriages (10th, 22nd, 33rd year).")

# ═══ GAP FILLS (identified by PDF-first audit 2026-04-01) ═════════════════════

# v.10-13 gap: Saturn/Mars in 7th → spouse harlot/attached to others
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 7}],
    entity_target="spouse",
    signal_group="saturn_mars_h7_spouse_questionable",
    direction="unfavorable", intensity="strong", domains=["marriage", "character_temperament"],
    predictions=[{"entity": "spouse", "claim": "spouse_harlot_or_attached_to_others",
                  "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: 'If the 7th house is occupied or owned by Saturn/Mars, the native will beget a harlot as his spouse or she will be attached to other men illegally.'",
    description="7th house occupied or owned by Saturn/Mars: spouse of questionable character.",
    modifiers=[{"condition": "mars_in_7th_or_owning_7th", "effect": "conditionalizes", "strength": "moderate"}])

# v.10-13 gap: Venus in Mars Navamsa/Rasi → unusual sexual gratification
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": "any"}],
    entity_target="native",
    signal_group="venus_mars_navamsa_sexual",
    direction="unfavorable", intensity="moderate", domains=["character_temperament"],
    predictions=[{"entity": "native", "claim": "unusual_sexual_gratification_from_female",
                  "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: Venus in Navamsa of Mars or Rasi of Mars or in aspect to/conjunct Mars → native indulges in unusual sexual gratification from female.",
    description="Venus in Mars Navamsa/Rasi or aspect/conjunct Mars: unusual sexual habits.",
    modifiers=[{"condition": "venus_in_mars_navamsa_or_rasi_or_conjunct", "effect": "conditionalizes", "strength": "strong"}],
    prediction_type="trait")

# v.10-13 gap: Venus related to Saturn → ugly relations with male
b.add(
    conditions=[{"type": "planets_conjunct", "planets": ["Venus", "Saturn"]}],
    entity_target="native",
    signal_group="venus_saturn_ugly_relations_male",
    direction="unfavorable", intensity="strong", domains=["character_temperament"],
    predictions=[{"entity": "native", "claim": "ugly_relations_with_another_male",
                  "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: 'If Venus is so related to Saturn, the native will have ugly relations with another male.' Venus-Saturn variant produces entirely different prediction direction from Venus-Mars.",
    description="Venus related to Saturn (instead of Mars): ugly relations with another male.",
    prediction_type="trait",
    modifiers=[{"condition": "venus_saturn_conjunction_or_aspect_specifically", "effect": "conditionalizes", "strength": "strong"}])

# v.19-21 gap: 3 wives (Mars+Venus in 7th or Saturn in 7th + asc lord in 8th)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7},
                {"type": "planet_in_house", "planet": "Venus", "house": 7}],
    entity_target="native",
    signal_group="mars_venus_h7_three_wives",
    direction="neutral", intensity="moderate", domains=["marriage"],
    predictions=[{"entity": "native", "claim": "three_wives",
                  "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.18 v.19-21",
    commentary_context="Text: 'If Mars and Venus are in the 7th or if Saturn is in the 7th while the lord of the ascendant is in the 8th, the native will have 3 wives.'",
    description="Mars+Venus in 7th, or Saturn in 7th + ascendant lord in 8th: three wives.",
    modifiers=[{"condition": "alternative_saturn_in_7th_plus_ascendant_lord_in_8th_also_gives_3_wives", "effect": "conditionalizes", "strength": "strong"}])

# v.19-21 gap: Many wives (Venus in dual sign + lord exalted + 7th lord strong)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": "any"}],
    entity_target="native",
    signal_group="venus_dual_sign_many_wives",
    direction="neutral", intensity="moderate", domains=["marriage"],
    predictions=[{"entity": "native", "claim": "many_wives",
                  "domain": "marriage", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.18 v.19-21",
    commentary_context="Text: 'There will be many wives if Venus is in a dual sign while its lord is in exaltation as the 7th lord is endowed with strength.'",
    description="Venus in dual sign + lord in exaltation + 7th lord strong: many wives.",
    modifiers=[{"condition": "venus_in_dual_sign", "effect": "conditionalizes", "strength": "strong"},
               {"condition": "dispositor_exalted_h7_lord_strong", "effect": "amplifies", "strength": "moderate"}])

BPHS_V2_CH18_REGISTRY = b.build()
