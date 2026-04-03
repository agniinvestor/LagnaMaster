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
    conditions=[{"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"}],
    signal_group="h7_lord_strong_happy_marriage",
    direction="favorable", intensity="strong", primary_domain="relationships",
    predictions=[{"entity": "spouse", "claim": "full_happiness_through_wife",
                  "domain": "relationships", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.1",
    commentary_context="Santhanam: Saturn in Capricorn for Leo native or Venus in Pisces for Aries native need not be feared — exaltation placement overrides natural malefic status. Trigger is dignity (own sign/exaltation), not house placement.",
    description="7th lord in own sign or exaltation: full happiness through wife and marriage.",
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1801"]},
)

# ═══ v.2: Sick wife ══════════════════════════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]}],
    signal_group="h7_lord_dusthana_sick_wife",
    direction="unfavorable", intensity="moderate", primary_domain="health",
    predictions=[{"entity": "spouse", "claim": "wife_will_be_sickly",
                  "domain": "health", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.2",
    description="7th lord in 6th, 8th or 12th: the wife will be sickly.",
    commentary_context="Does not apply to own house or exaltation placement. Venus in exaltation in 7th house for Aries native need not be feared.",
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1800"]},
    exceptions=["7th_lord_in_own_sign_or_exaltation_nullifies"],
)

# ═══ v.3: Excessive libidinousness / death of wife ═══════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 7}],
    signal_group="venus_h7_libidinous",
    direction="mixed", intensity="moderate", primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "exceedingly_libidinous",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
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
    direction="favorable", intensity="strong", primary_domain="wealth",
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
    conditions=[
        {"type": "lord_in_sign", "lord_of": 7,
         "sign": ["Capricorn", "Aquarius", "Taurus", "Libra"]},
    ],
    signal_group="h7_lord_saturn_venus_sign_many_wives",
    direction="neutral", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "many_wives",
                  "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
    entity_target="native",
    verse_ref="Ch.18 v.6",
    commentary_context=(
        "7th lord in a sign of Saturn (Capricorn/Aquarius) or Venus "
        "(Taurus/Libra), aspected by a benefic = many wives. 7th lord "
        "in exaltation produces same effect."
    ),
    description="7th lord in a sign of Saturn or Venus, aspected by a benefic: there will be many wives. 7th lord in exaltation → same effect.",
    concordance_texts=[],
    modifiers=[{"condition": "aspected_by_benefic", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ═══ v.14-15: Worthy spouse ══════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "exalted"},
        {"type": "lord_in_house", "lord_of": 1, "house": 7},
    ],
    signal_group="h7_lord_exalted_worthy_spouse",
    direction="favorable", intensity="strong", primary_domain="relationships",
    predictions=[
        {"entity": "spouse", "claim": "spouse_with_seven_principal_virtues",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.8},
        {"entity": "children", "claim": "sons_and_grandsons",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    entity_target="general",
    verse_ref="Ch.18 v.14-15",
    commentary_context=(
        "Santhanam: Compound condition — 7th lord in exaltation AND "
        "ascendant lord with strength in 7th with benefic. Both required "
        "for spouse with seven principal virtues and expanding dynasty."
    ),
    description="7th lord exalted + ascendant lord strong in 7th with benefic: spouse endowed with seven principal virtues, expanding dynasty by sons and grandsons.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "benefic_also_in_7th", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ═══ v.17: Loss of spouse (early death) ══════════════════════════════════════

b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": [6, 8, 12]},
                {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "weak"}],
    signal_group="h7_lord_dusthana_weak_wife_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "spouse", "claim": "wife_destroyed_early_death",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.18 v.17",
    commentary_context="Santhanam: If the 7th lord is in fall, the native's wife will be destroyed (i.e. she will die early). The placement in 6th/8th/12th compounds this.",
    description="7th lord devoid of strength in 6th/8th/12th or if 7th lord is in fall: the native's wife will be destroyed (i.e. she will die early).",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "7th_lord_in_fall_compounds_dusthana_placement", "effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ═══ v.22-34: TIMING OF MARRIAGE — each age as its own rule ══════════════════

_MARRIAGE_TIMING = [
    ("Ch.18 v.22", [5, 9], "7th lord in benefic's house + Venus exalted/own sign",
     [{"type": "lord_in_sign", "lord_of": 7,
       "sign": ["Sagittarius", "Pisces", "Taurus", "Libra", "Gemini", "Virgo", "Cancer"]}]),
    ("Ch.18 v.23", [7, 11], "Sun in 7th + dispositor conjunct Venus",
     [{"type": "planet_in_house", "planet": "Sun", "house": 7}]),
    ("Ch.18 v.24", [10, 16], "Venus in 2nd + 7th lord in 11th",
     [{"type": "planet_in_house", "planet": "Venus", "house": 2}]),
    ("Ch.18 v.25", [11], "Venus in angle from ascendant + ascendant lord in Cap/Aqu",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.26", [12, 19], "Venus in angle + Saturn in 7th from Venus",
     [{"type": "planet_in_house", "planet": "Venus", "house": [1, 4, 7, 10]}]),
    ("Ch.18 v.28", [15], "2nd lord in 11th + ascendant lord in 10th",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11}]),
    ("Ch.18 v.29", [13], "Exchange of 2nd and 11th lords",
     [{"type": "lord_in_house", "lord_of": 2, "house": 11},
      {"type": "lord_in_house", "lord_of": 11, "house": 2}]),
    ("Ch.18 v.30", [22, 27], "Venus in 7th from 8th (= house 2) + dispositor conjunct Mars",
     [{"type": "planet_in_house", "planet": "Venus", "house": 2}]),
    ("Ch.18 v.31", [23, 26], "7th lord in 12th + natal asc lord in 7th Navamsa",
     [{"type": "lord_in_house", "lord_of": 7, "house": 12}]),
    ("Ch.18 v.32", [25, 33], "8th lord in 7th + Venus in Navamsa ascendant",
     [{"type": "lord_in_house", "lord_of": 8, "house": 7}]),
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
        direction="favorable", intensity="moderate", primary_domain="relationships",
        predictions=[{"entity": "native", "claim": f"marriage_at_age_{ages[0]}",
                      "domain": "relationships", "direction": "favorable", "magnitude": 0.5}],
        timing_window={"type": tw_type, "value": age_val, "precision": "approximate"},
        verse_ref=vref,
        commentary_context=f"Santhanam groups v.22-34 as TIMING OF MARRIAGE. Age {ages[0]} indicated by specific planetary combination. These ages may not be literal in modern context but indicate early vs late marriage." if _mt_idx > 0 else "Santhanam: The age of marriage indicated in the text will not be practical in all cases in modern social conditions. These will be simply helpful in knowing of early and belated marriages.",
        description=f"Marriage timing: {desc_suffix} → marry at age {'/'.join(str(a) for a in ages)}.",
    )

# ═══ v.27: Marriage at 18 (Venus relative to Moon — individual rule) ═════════
b.add(
    conditions=[
        {"type": "planet_in_house_from", "planet": "Venus", "reference": "Moon", "offset": 7, "mode": "occupies"},
        {"type": "planet_in_house_from", "planet": "Saturn", "reference": "Venus", "offset": 7, "mode": "occupies"},
    ],
    entity_target="native",
    signal_group="marriage_timing_18",
    direction="favorable", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "marriage_at_age_18",
                  "domain": "relationships", "direction": "favorable", "magnitude": 0.5}],
    timing_window={"type": "age", "value": 18, "precision": "approximate"},
    verse_ref="Ch.18 v.27",
    commentary_context=(
        "Santhanam: Venus in 7th from Moon + Saturn in 7th from Venus. "
        "Both planet-relative conditions are now structurally encoded."
    ),
    description="Marriage timing: Venus in 7th from Moon + Saturn in 7th from Venus → marry at age 18.",
)

# ═══ v.33: Marriage at 31/33 (Venus 9th from 5th — individual rule) ═════════
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Venus", "house": 1},
        {"type": "planet_in_house", "planet": "Rahu", "house": [1, 5]},
    ],
    entity_target="native",
    signal_group="marriage_timing_31",
    direction="favorable", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "marriage_at_age_31",
                  "domain": "relationships", "direction": "favorable", "magnitude": 0.5}],
    timing_window={"type": "age_range", "value": [31, 33], "precision": "approximate"},
    verse_ref="Ch.18 v.33",
    commentary_context=(
        "Santhanam: Venus in 9th from 5th (= house 1) + Rahu in one of "
        "said houses (1st or 5th). 9th from 5th computed: 5+8=13 mod 12=1."
    ),
    description="Marriage timing: Venus in 9th from 5th + Rahu in one of said houses → marry at age 31/33.",
)

# ═══ v.35-39: TIMING OF WIFE'S DEATH ════════════════════════════════════════

_WIFE_DEATH_TIMING = [
    ("Ch.18 v.35", [18, 33], "7th lord in fall + Venus in 8th",
     [{"type": "planet_dignity", "planet": "lord_of_7", "dignity": "debilitated"},
      {"type": "planet_in_house", "planet": "Venus", "house": 8}]),
    ("Ch.18 v.36", [19], "7th lord in 8th + 12th lord in 7th",
     [{"type": "lord_in_house", "lord_of": 7, "house": 8},
      {"type": "lord_in_house", "lord_of": 12, "house": 7}]),
    ("Ch.18 v.38", [17, 21], "Venus in 8th + dispositor in Saturn sign",
     [{"type": "planet_in_house", "planet": "Venus", "house": 8}]),
    ("Ch.18 v.39", [13], "Ascendant lord in debilitation + 2nd lord in 8th",
     [{"type": "planet_dignity", "planet": "lord_of_1", "dignity": "debilitated"},
      {"type": "lord_in_house", "lord_of": 2, "house": 8}]),
]

for _wd_idx, (vref, ages, desc_suffix, conds) in enumerate(_WIFE_DEATH_TIMING):
    age_val = ages[0] if len(ages) == 1 else ages
    tw_type = "age" if len(ages) == 1 else "age_range"
    b.add(
        conditions=conds,
        signal_group=f"wife_death_{ages[0]}",
        direction="unfavorable", intensity="strong", primary_domain="longevity",
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
    direction="unfavorable", intensity="strong", primary_domain="longevity",
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
    direction="unfavorable", intensity="strong", primary_domain="longevity",
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
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "befriend_barren_females_for_sexual_union", "domain": "relationships", "direction": "unfavorable", "magnitude": 0.5}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Sun in 7th = native seeks pleasures from barren females. Any planet in 7th (including 7th lord) indicates absence of sterlingness in character regarding sexual union.",
      description="Sun in 7th: native will befriend barren females for sexual union.")

b.add(conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7}],
      entity_target="native",
      signal_group="mars_h7_marriageable_girls", direction="mixed", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "associate_with_marriageable_age_females", "domain": "relationships", "direction": "mixed", "magnitude": 0.5}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Mars in 7th = female of marriageable age, or one in her monthly course, or one devoid of conceiving ability. Jupiter in 7th is also no exception to this negative pattern.",
      description="Mars in 7th: associate with marriageable girls or those with menses.",
      exceptions=["jupiter_in_7th_produces_similar_negative_effects"],
      rule_relationship={"type": "alternative", "related_rules": ["BPHS1828"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "Mercury", "house": 7}],
      entity_target="native",
      signal_group="mercury_h7_traders_community", direction="mixed", intensity="weak",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "associate_with_mean_females_traders_community", "domain": "relationships", "direction": "mixed", "magnitude": 0.4}],
      verse_ref="Ch.18 v.7-8",
      commentary_context="Santhanam: Mercury = harlots, mean females, females of traders' community. The kind corresponds to the sign becoming the 7th house.",
      description="Mercury in 7th: associate with mean females or those from traders' community.")

# ═══ v.9-9½: Physical features of spouse ══════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7}],
      signal_group="mars_h7_spouse_appearance", direction="neutral", intensity="moderate",
      primary_domain="character",
      predictions=[{"entity": "spouse", "claim": "female_with_attractive_breasts", "domain": "character", "direction": "favorable", "magnitude": 0.4}],
      verse_ref="Ch.18 v.9",
      commentary_context="Santhanam: Mars = attractive breasts. Saturn = sick/weak spouse. Jupiter = hard/prominent breasts. Venus = bulky/excellent breasts.",
      description="Mars indicates female with attractive breasts. Saturn = sick/weak. Jupiter = hard/prominent. Venus = excellent.",
      prediction_type="trait")

# ═══ v.10-13½: Morality — spouse controlled by others ════════════════════════
b.add(conditions=[
          {"type": "planet_in_house", "planet": "any_malefic", "house": 12},
          {"type": "planet_in_house", "planet": "Moon", "house": 5},
      ],
      entity_target="spouse",
      signal_group="malefics_h12_moon_h5_spouse_controlled", direction="unfavorable", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "spouse", "claim": "spouse_controlled_by_others_inimical_to_race", "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.10-13",
      commentary_context=(
          "Santhanam: Compound condition — Moon (decreasing) in 5th + "
          "malefic in 12th/7th = high-handed spouse. Part of 4-hint block "
          "(v.10-13). Moon decreasing is additional qualifier."
      ),
      description="Malefics in 12th + Moon in 5th: spouse controlled by others, inimical to family.",
      modifiers=[{"condition": "moon_decreasing_strengthens", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}])

# ═══ v.16: Evils to spouse ════════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 7}],
      entity_target="spouse",
      signal_group="malefic_h7_evils_to_spouse", direction="unfavorable", intensity="moderate",
      primary_domain="health",
      predictions=[{"entity": "spouse", "claim": "wife_incur_evils_especially_if_bereft_of_strength", "domain": "health", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.16",
      commentary_context="Santhanam: 7th house or its lord conjunct malefic + bereft of strength = wife incur evils. Especially if the 7th house/lord is not strong.",
      description="7th house or its lord conjunct malefic, bereft of strength: wife will incur evils.",
      modifiers=[{"condition": "7th_house_or_lord_not_strong_intensifies_evils", "effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local"}])

# ═══ v.18: Lack of conjugal felicity ═════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 7},
                   {"type": "lord_in_house", "lord_of": 7, "house": 12}],
      entity_target="native",
      signal_group="moon_h7_h7_lord_h12_no_marital_happiness", direction="unfavorable", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "not_endowed_with_marital_happiness", "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.18 v.18",
      commentary_context="Santhanam: Moon in 7th + 7th lord in 12th + Venus (Karaka) bereft of strength = no marital happiness. Moon increasing would stall adversity.",
      description="Moon in 7th + 7th lord in 12th + Venus weak: not endowed with marital happiness.",
      modifiers=[{"condition": "venus_bereft_of_strength", "effect": "attenuates", "target": "prediction", "strength": "medium", "scope": "local"}])

# ═══ v.19-21: Plurality of wives ══════════════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_7", "dignity": "debilitated"}],
      entity_target="native",
      signal_group="h7_lord_fall_two_wives", direction="neutral", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "two_wives_if_7th_lord_in_fall", "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
      verse_ref="Ch.18 v.19-21",
      commentary_context="Santhanam: 7th lord in fall + malefic sign + 7th Navamsa eunuch planet = 2 wives. Mars+Venus in 7th + Saturn + ascendant lord in 8th = 3 wives. Venus in dual sign + lord exalted + 7th lord strong = many wives. For dual marriage, 7th from natal or Navamsa ascendant should be owned by eunuch planet (Gemini, Virgo, Capricorn, Aquarius).",
      description="7th lord in fall or malefic sign, 7th Navamsa = eunuch planet: two wives. Mars+Venus+Saturn = three. Venus in dual sign = many.")

# ═══ v.40-41: Three marriages ═════════════════════════════════════════════════
b.add(conditions=[
          {"type": "lord_in_house", "lord_of": 8, "house": 5},
          {"type": "planet_in_house_from", "planet": "Moon", "reference": "Venus", "offset": 7, "mode": "occupies"},
          {"type": "planet_in_house_from", "planet": "Mercury", "reference": "Moon", "offset": 7, "mode": "occupies"},
      ],
      entity_target="native",
      signal_group="moon_venus_mercury_three_marriages", direction="neutral", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "three_marriages_at_10_22_33", "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
      timing_window={"type": "age_range", "value": [10, 33], "precision": "approximate"},
      verse_ref="Ch.18 v.40-41",
      commentary_context=(
          "Santhanam: Moon in 7th from Venus + Mercury in 7th from Moon + "
          "8th lord in 5th = 3 marriages. All conditions are now structurally encoded."
      ),
      description="Moon in 7th from Venus + Mercury in 7th from Moon + 8th lord in 5th: three marriages (10th, 22nd, 33rd year).")

# ═══ GAP FILLS (identified by PDF-first audit 2026-04-01) ═════════════════════

# v.10-13 gap: Saturn/Mars in 7th → spouse harlot/attached to others
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 7}],
    entity_target="spouse",
    signal_group="saturn_h7_spouse_questionable",
    direction="unfavorable", intensity="strong", primary_domain="character",
    predictions=[{"entity": "spouse", "claim": "spouse_harlot_or_attached_to_others",
                  "domain": "character", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: Saturn occupying or owning 7th = spouse of questionable character. Mars variant encoded as alternative rule.",
    description="Saturn in 7th or owning 7th: spouse of questionable character.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1836"]},
)

# v.10-13 gap: Mars variant — Mars in 7th/owning 7th → same prediction
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7}],
    entity_target="spouse",
    signal_group="mars_h7_spouse_questionable",
    direction="unfavorable", intensity="strong", primary_domain="character",
    predictions=[{"entity": "spouse", "claim": "spouse_harlot_or_attached_to_others",
                  "domain": "character", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: Mars occupying or owning 7th = spouse of questionable character. Alternative to Saturn variant.",
    description="Mars in 7th or owning 7th: spouse of questionable character.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1835"]},
)

# v.10-13 gap: Venus in Mars Navamsa/Rasi → unusual sexual gratification
b.add(
    conditions=[
        {"type": "planet_in_sign", "planet": "Venus",
         "sign": ["Aries", "Scorpio"]},
    ],
    entity_target="native",
    signal_group="venus_mars_navamsa_sexual",
    direction="unfavorable", intensity="moderate", primary_domain="character",
    predictions=[{"entity": "native", "claim": "unusual_sexual_gratification_from_female",
                  "domain": "character", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.18 v.10-13",
    commentary_context=(
        "Text: Venus in Rasi of Mars (Aries/Scorpio) or Navamsa of Mars "
        "or conjunct/aspected by Mars → unusual sexual gratification. "
        "Navamsa condition not yet structurable. Venus-Mars conjunction "
        "as alternative trigger."
    ),
    description="Venus in Mars Rasi/Navamsa or conjunct Mars: unusual sexual habits.",
    modifiers=[{"condition": "venus_in_mars_navamsa_or_conjunct_mars_also_triggers", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
    prediction_type="trait")

# v.10-13 gap: Venus related to Saturn → ugly relations with male
b.add(
    conditions=[{"type": "planets_conjunct", "planets": ["Venus", "Saturn"]}],
    entity_target="native",
    signal_group="venus_saturn_ugly_relations_male",
    direction="unfavorable", intensity="strong", primary_domain="character",
    predictions=[{"entity": "native", "claim": "ugly_relations_with_another_male",
                  "domain": "character", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.18 v.10-13",
    commentary_context="Text: 'If Venus is so related to Saturn, the native will have ugly relations with another male.' Venus-Saturn variant produces entirely different prediction direction from Venus-Mars.",
    description="Venus related to Saturn (instead of Mars): ugly relations with another male.",
    prediction_type="trait",
    modifiers=[{"condition": "venus_saturn_conjunction_or_aspect_specifically", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}])

# v.19-21 gap: 3 wives (Mars+Venus in 7th or Saturn in 7th + asc lord in 8th)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 7},
                {"type": "planet_in_house", "planet": "Venus", "house": 7}],
    entity_target="native",
    signal_group="mars_venus_h7_three_wives",
    direction="neutral", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "three_wives",
                  "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.18 v.19-21",
    commentary_context="Text: Mars and Venus both in 7th = three wives. Alternative path (Saturn in 7th + asc lord in 8th) encoded separately below.",
    description="Mars and Venus both in 7th: three wives.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1839"]},
)

# v.19-21 gap: Alternative path — Saturn in 7th + asc lord in 8th → 3 wives
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 7},
                {"type": "lord_in_house", "lord_of": 1, "house": 8}],
    entity_target="native",
    signal_group="saturn_h7_asc_lord_h8_three_wives",
    direction="neutral", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "three_wives",
                  "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.18 v.19-21",
    commentary_context="Text: Saturn in 7th + lord of ascendant in 8th = three wives. Alternative path to Mars+Venus in 7th.",
    description="Saturn in 7th + ascendant lord in 8th: three wives.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1838"]},
)

# v.19-21 gap: Many wives (Venus in dual sign + lord exalted + 7th lord strong)
b.add(
    conditions=[
        {"type": "planet_in_sign_type", "planet": "Venus", "sign_type": "dual"},
        {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "strong"},
        {"type": "dispositor_condition", "planet": "Venus", "dispositor_state": "dignity", "dignity": "exalted"},
    ],
    entity_target="native",
    signal_group="venus_dual_sign_many_wives",
    direction="neutral", intensity="moderate", primary_domain="relationships",
    predictions=[{"entity": "native", "claim": "many_wives",
                  "domain": "relationships", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.18 v.19-21",
    commentary_context=(
        "Text: Venus in dual sign (Gemini/Virgo/Sagittarius/Pisces) + "
        "dispositor in exaltation + 7th lord strong = many wives. "
        "Dispositor exaltation promoted from modifier to condition (Track 4)."
    ),
    description="Venus in dual sign + dispositor exalted + 7th lord strong: many wives.")

BPHS_V2_CH18_REGISTRY = b.build()
