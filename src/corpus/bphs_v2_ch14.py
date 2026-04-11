"""src/corpus/bphs_v2_ch14.py — BPHS Ch.14 (3rd House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.137-141.
Chapter: 14 — Effects of the Third House (Sahaj Bhava Phala)
Slokas: 15. Rules: 31. V2 Completeness: 95%+.
Entity: siblings (all rules). Timing: all unspecified (no ages in text).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.14", category="3rd_house_effects",
    id_start=1400, session="S311", sloka_count=15,
    chapter_tags=["3rd_house", "sahaj_bhava"],
    entity_target="siblings",
)

# ═══ v.1: Benefic in 3rd → co-born and courage ═══════════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "any_benefic", "house": 3}],
    entity_target="general",
    signal_group="benefic_h3_coborn", direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "endowed_with_coborn",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "courageous",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.1",
    description=(
        "3rd house conjunct or aspected by a benefic: the native will "
        "be endowed with co-born (brothers/sisters) and be courageous."
    ),
    commentary_context=(
        "Santhanam notes: 'Bhratru' in Sanskrit simply means a brother. "
        "Jyeshta for elder, Kanishta for younger. 3rd house deals with "
        "after-born while 11th house deals with preborn (sloka 32, Ch.32)."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Ch.32 v.32 Planetary Karakatvas"],
    tags=["benefic", "h3", "coborn", "courage"],
)

# ═══ v.2: 3rd lord + Mars aspects 3rd → good for co-born ═════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 3, "house": 3},
        {"type": "planet_aspecting", "planet": "Mars", "house": 3},
    ],
    signal_group="h3_lord_mars_aspect_coborn", direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "good_results_for_coborn",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.2",
    description=(
        "3rd lord along with Mars aspects the 3rd house: good results "
        "for co-born. Alternatively these two planets may be in the 3rd."
    ),
    commentary_context=(
        "Santhanam notes: Mars alone in 3rd, except in Capricorn/Scorpio/"
        "Aries, is not conducive to brothers. The 3rd house must be "
        "jointly aspected or occupied by Mars and the 3rd lord."
    ),
    exceptions=["mars_alone_in_3rd_without_3rd_lord_not_conducive_except_capricorn_scorpio_aries"],
)

# ═══ v.5-6: Destruction of co-born ═══════════════════════════════════════════

b.add(
    conditions=[
        {"type": "or_group", "alternatives": [
            {"type": "planets_conjunct", "planets": ["lord_of_3", "any_malefic"]},
            {"type": "planet_dignity", "planet": "lord_of_3", "dignity": "debilitated"},
        ]},
        {"type": "planets_conjunct", "planets": ["Mars", "lord_of_3"]},
    ],
    signal_group="h3_lord_malefic_coborn_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "destruction_of_coborn",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
        {"entity": "siblings", "claim": "coborn_will_not_live_long",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.14 v.5-6",
    description=(
        "3rd lord and Mars together with malefic or in debilitation: "
        "destruction of coborn at once. 'The coborn will not live long.'"
    ),
    commentary_context=(
        "Santhanam notes: Universal principle — the significator and lord "
        "of a house together in debilitation/inimical sign or with malefic "
        "brings harm to that relative. Jupiter+11th lord → elder siblings; "
        "Venus+7th lord → spouse; Jupiter+5th lord → progeny; Sun+9th lord "
        "→ father; Moon+4th lord → mother. Verse also says happiness comes "
        "if Mars or 3rd lord is in angle/trine/exaltation/friendly divisions."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=[
        "Ch.15 (4th house, mother)", "Ch.16 (5th house, children)",
        "Ch.18 (7th house, spouse)", "Ch.20 (9th house, father)",
    ],
    convergence_signals=["mars_in_malefic_sign", "h3_lord_combust"],
)

# ═══ v.4-4½: Female and male co-born ═════════════════════════════════════════

# NOTE: Verse says "female planet" not "benefic". No planet-gender primitive
# exists yet. Using Venus in 3rd as primary female-planet condition. Moon is
# the other female planet but has its own rule (BPHS1408). Governance backlog:
# consider adding planet_gender primitive for male/female/neutral classification.
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 3}],
    signal_group="h3_female_planet_sisters",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "sisters_born_after_native",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "3rd lord is female planet or 3rd house occupied by female planets: "
        "sisters born after native. Male planets → brothers. Mixed → both."
    ),
    commentary_context=(
        "Santhanam notes: Saturn/Mercury neutral, Rahu/Ketu shadowy. For "
        "sex: Saturn/Rahu = male, Mercury/Ketu = female. Odd signs = male, "
        "even signs = female. Venus and Moon are primary female planets."
    ),
    prediction_type="trait",
)

# ═══ v.5-6: 3rd lord + Mars in 8th → destruction; contrary in angle ══════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 3, "house": 8},
        {"type": "planet_in_house", "planet": "Mars", "house": 8},
    ],
    signal_group="h3_lord_mars_h8_coborn_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "destruction_of_coborn",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.14 v.5-6",
    description="3rd lord and Mars together in the 8th: destruction of coborn.",
    commentary_context=(
        "Santhanam notes: Venus+7th lord in 8th → short married life. "
        "Their conjunction in angle/trine → longlasting benefic effects. "
        "Significator+lord in debilitation/inimical = lost; exaltation/"
        "friendly = prosperity."
    ),
    concordance_texts=["Saravali"],
    derived_house_chains=[{
        "base_house": 3, "derivative": "6th_from",
        "effective_house": 8, "entity": "siblings", "domain": "longevity",
    }],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1405"]},
)

# v.5-6b: contrary mirror — 3rd lord in angle/trine → happiness
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": [1, 4, 5, 7, 9, 10]}],
    signal_group="h3_lord_kendra_coborn_happy",
    direction="favorable", intensity="moderate", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "happiness_for_coborn",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.5-6",
    commentary_context="Contrary of BPHS1404. Santhanam: significator+lord in exaltation/friendly = significance gains prosperity.",
    description=(
        "Mars or 3rd lord in angle/trine/exaltation/friendly: happiness for coborn."
    ),
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1404"]},
    modifiers=[{"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "strong"}], "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ═══ v.7-11: Number of siblings (complex) ════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Mercury", "house": 3},
        {"type": "planets_conjunct", "planets": ["Mars", "Saturn"]},
    ],
    signal_group="mercury_h3_mars_saturn_siblings",
    direction="mixed", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "elder_sister_born",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
        {"entity": "siblings", "claim": "younger_brothers_will_die",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
        {"entity": "siblings", "claim": "third_brother_dies",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.7-11",
    description=(
        "Mercury in 3rd + 3rd lord and Moon together + Mars joins Saturn: "
        "elder sister born, younger brothers die, third brother dies."
    ),
    commentary_context="Santhanam: 'Karaka' in sloka 7 = Mars, not Jupiter (per sloka 11). Text does not restrict Mars+Saturn conjunction to 3rd house specifically — encoded as conjunction anywhere per source fidelity.",
)

# v.7-11b: 3rd lord exalted in trine + Jupiter → 12 total co-born
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 3, "house": [1, 5, 9]},
        {"type": "planet_dignity", "planet": "Mars", "dignity": "exalted"},
    ],
    signal_group="h3_lord_exalted_trikona_12_coborn",
    direction="favorable", intensity="strong", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "twelve_total_coborn",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
        {"entity": "siblings", "claim": "six_of_twelve_longlived",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.7-11",
    description=(
        "3rd lord exalted in trine + company of Jupiter → 12 total coborn. "
        "2 elders; 3rd/7th/9th/12th younger shortlived; six longlived."
    ),
    commentary_context=(
        "Santhanam: 12 = indicative number. Mars exalted + Jupiter company "
        "= Jupiter in fall. Some coborn die due to Jupiter's debilitation."
    ),
    modifiers=[],
)

# ═══ v.12-13: Seven co-born ══════════════════════════════════════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 3}],
    signal_group="moon_h3_seven_coborn",
    direction="favorable", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "seven_coborn",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.14 v.12-13",
    commentary_context="No separate Santhanam note for v.12-13. Verse conditions are explicit.",
    description=(
        "11th/12th lord joins Mars+Jupiter + Moon in 3rd → 7 coborn. "
        "Moon alone + male planets → younger brothers; Venus aspect → sisters."
    ),
)

# ═══ v.14: Adverse planets — Sun/Saturn/Mars each different ══════════════════

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Sun", "house": 3}],
    signal_group="sun_h3_elder_sibling_loss",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "elder_siblings_destroyed",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.14",
    description="Sun in 3rd destroys the preborn (elder siblings).",
    commentary_context="Sage Bhrigu: Sun in 3rd won't allow retaining elder siblings.",
    concordance_texts=["Saravali"],
)

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 3}],
    signal_group="saturn_h3_younger_sibling_loss",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "younger_siblings_destroyed",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.14",
    commentary_context="Part of the Sun/Saturn/Mars triad in v.14. Each planet destroys a different birth-order group.",
    description="Saturn in 3rd: afterborn (younger siblings) destroyed.",
    concordance_texts=["Saravali"],
)

b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 3}],
    signal_group="mars_h3_all_sibling_loss",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "both_elder_and_younger_destroyed",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.14 v.14",
    description="Mars in 3rd destroys both preborn and later born.",
    commentary_context=(
        "Garga Maharshi: 2 brothers + 2 sisters, all 4 pass early. "
        "Mars in 3rd also adverse on native's character."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Saravali Effects of Planets in Bhavas"],
)

# ═══ v.15: Yoga strength (methodological) ════════════════════════════════════

b.add(
    conditions=[],
    signal_group="yoga_strength_siblings_method",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "assess_yoga_strength_before_declaring",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.14 v.15",
    commentary_context="Methodological instruction — no Santhanam note. The sage directs assessment before declaration.",
    description="After estimating yoga strength/weakness, announce sibling effects.",
    prediction_type="trait",
)

# ═══ GAP FILLS (identified by PDF-first audit 2026-04-01) ═════════════════════

# v.2 gap: Mars alone in 3rd (except Cap/Sco/Ari) → not conducive to brothers
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 3}],
    signal_group="mars_alone_h3_not_conducive",
    direction="unfavorable", intensity="moderate", primary_domain="progeny",
    predictions=[{"entity": "siblings", "claim": "mars_alone_not_conducive_to_brothers",
                  "domain": "progeny", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.14 v.2",
    commentary_context="Santhanam: Mars alone in 3rd, except in Capricorn/Scorpio/Aries, is not conducive to brothers. The 3rd house must be jointly aspected/occupied by Mars AND the 3rd lord.",
    description="Mars alone in 3rd (not in Cap/Sco/Ari): not conducive to brothers.",
    exceptions=["mars_in_capricorn", "mars_in_scorpio", "mars_in_aries"],
    concordance_texts=["Saravali"])

# v.3 gap: Universal relative-harm principle — elder siblings
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_11", "dignity": "weak"},
        {"type": "planets_conjunct", "planets": ["Jupiter", "lord_of_11"]},
    ],
    entity_target="siblings",
    signal_group="jupiter_h11_lord_malefic_elder_harm",
    direction="unfavorable", intensity="moderate", primary_domain="longevity",
    predictions=[{"entity": "siblings", "claim": "elder_siblings_harmed",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.14 v.3",
    commentary_context="Santhanam: Jupiter + 11th lord together in malefic sign or with malefic → elder siblings harmed. Universal principle applied.",
    description="Jupiter + 11th lord in malefic sign or with malefic: elder siblings harmed.",
    modifiers=[],
    concordance_texts=["Saravali"])

# v.3 gap: Universal relative-harm principle — spouse
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_7", "dignity": "weak"},
        {"type": "planets_conjunct", "planets": ["Venus", "lord_of_7"]},
    ],
    entity_target="spouse",
    signal_group="venus_h7_lord_malefic_spouse_harm",
    direction="unfavorable", intensity="moderate", primary_domain="longevity",
    predictions=[{"entity": "spouse", "claim": "spouse_harmed",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.14 v.3",
    commentary_context="Santhanam: Venus + 7th lord in malefic sign or with malefic → spouse harmed.",
    description="Venus + 7th lord in malefic sign or with malefic: spouse harmed.",
    modifiers=[])

# v.3 gap: Universal relative-harm principle — father
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_9", "dignity": "weak"},
        {"type": "planets_conjunct", "planets": ["Sun", "lord_of_9"]},
    ],
    entity_target="father",
    signal_group="sun_h9_lord_malefic_father_harm",
    direction="unfavorable", intensity="moderate", primary_domain="longevity",
    predictions=[{"entity": "father", "claim": "father_harmed",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.14 v.3",
    commentary_context="Santhanam: Sun + 9th lord in malefic sign or with malefic → father harmed.",
    description="Sun + 9th lord in malefic sign or with malefic: father harmed.",
    modifiers=[])

# v.3 gap: Universal relative-harm principle — mother
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_4", "dignity": "weak"},
        {"type": "planets_conjunct", "planets": ["Moon", "lord_of_4"]},
    ],
    entity_target="mother",
    signal_group="moon_h4_lord_malefic_mother_harm",
    direction="unfavorable", intensity="moderate", primary_domain="longevity",
    predictions=[{"entity": "mother", "claim": "mother_harmed",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.6}],
    verse_ref="Ch.14 v.3",
    commentary_context="Santhanam: Moon + 4th lord in malefic sign or with malefic → mother harmed.",
    description="Moon + 4th lord in malefic sign or with malefic: mother harmed.",
    modifiers=[])

# v.5-6 gap: Venus+7th lord in 8th → short married life
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 8},
                {"type": "lord_in_house", "lord_of": 7, "house": 8}],
    entity_target="spouse",
    signal_group="venus_h7_lord_h8_short_marriage",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "spouse", "claim": "short_married_life",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.14 v.5-6",
    commentary_context="Santhanam: Venus + 7th lord in 8th → short married life. Their conjunction in angle/trine → longlasting benefic effects.",
    description="Venus + 7th lord together in 8th: short married life.")

# v.7-11 gap: Mars+Rahu + 3rd lord debilitated → loss of younger, 3 elders
b.add(
    conditions=[{"type": "planets_conjunct", "planets": ["Mars", "Rahu"]},
                {"type": "planet_dignity", "planet": "lord_of_3", "dignity": "debilitated"}],
    signal_group="mars_rahu_h3_lord_fall_sibling_loss",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[{"entity": "siblings", "claim": "loss_of_younger_three_elders_remain",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    verse_ref="Ch.14 v.7-11",
    commentary_context="Mars+Rahu conjunct + 3rd lord debilitated → loss of younger siblings while 3 elders remain.",
    description="Mars+Rahu conjunct + 3rd lord debilitated: loss of younger, 3 elders survive.")

# v.12-13 gap: Moon alone + Venus aspect → younger sisters
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Moon", "house": 3},
        {"type": "planet_aspecting", "planet": "Venus", "house": 3},
    ],
    signal_group="moon_h3_venus_aspect_sisters",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[{"entity": "siblings", "claim": "younger_sisters_indicated",
                  "domain": "progeny", "direction": "neutral", "magnitude": 0.5}],
    verse_ref="Ch.14 v.12-13",
    commentary_context="Moon alone in 3rd + Venus aspect → younger sisters. Without Venus aspect and with male planet aspect → younger brothers instead.",
    description="Moon alone in 3rd with Venus aspect: younger sisters.",
    modifiers=[],
    prediction_type="trait")

# v.14 gap: Mars in 3rd → adverse on native's character
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 3}],
    entity_target="native",
    signal_group="mars_h3_adverse_character",
    direction="unfavorable", intensity="moderate", primary_domain="character",
    predictions=[{"entity": "native", "claim": "adverse_effect_on_character",
                  "domain": "character", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.14 v.14",
    commentary_context="Santhanam: Mars in 3rd has also adverse say on the native's character. See Saravali 'Effects of Planets in Bhavas' for details.",
    description="Mars in 3rd: adverse effect on native's character.",
    prediction_type="trait")

# ═══ v.1 ASPECT VARIANT: Benefic aspecting 3rd → co-born and courage ════════
# Verse says "aspected by or conjunct with a benefic" — above rule (BPHS1400)
# encodes occupation; this encodes the aspect path.

b.add(
    conditions=[{"type": "planet_aspecting", "planet": "any_benefic", "house": 3}],
    entity_target="general",
    signal_group="benefic_h3_coborn_aspect", direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "endowed_with_coborn",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "courageous",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.1",
    description=(
        "3rd house aspected by a benefic: the native will be endowed "
        "with co-born (brothers/sisters) and be courageous."
    ),
    commentary_context=(
        "Aspect path of v.1. Verse explicitly says 'aspected by or "
        "conjunct with a benefic'. BPHS1400 encodes conjunction/occupation; "
        "this rule encodes the aspect path."
    ),
    concordance_texts=["Saravali"],
    cross_chapter_refs=["Ch.32 v.32 Planetary Karakatvas"],
    tags=["benefic", "h3", "coborn", "courage", "aspect"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1400"]},
)

# ═══ GAP FILLS — S319 Ch.14 deep audit (male planets, sign-gender, combos) ════

# v.4 gap: Moon in 3rd as female planet → sisters
# Verse says "female planet" = Venus or Moon. BPHS1403 encodes Venus.
# This rule encodes Moon as the other female planet in 3rd → sisters.
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 3}],
    signal_group="h3_female_planet_moon_sisters",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "sisters_born_after_native",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "Moon (female planet) in 3rd house: sisters born after native. "
        "Verse says female planet in 3rd or 3rd lord is female planet → sisters."
    ),
    commentary_context=(
        "Santhanam: Venus and Moon are primary female planets. This is the "
        "Moon path of v.4. BPHS1403 encodes Venus path. The verse treats both "
        "Venus and Moon as female planets indicating sisters."
    ),
    prediction_type="trait",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1403"]},
    tags=["female_planet", "moon", "h3", "sisters"],
)

# v.4 gap: Male planet (Sun, Mars, Jupiter) in 3rd → brothers
# Verse: "male planets will cause birth of brothers"
# Sun, Mars, Jupiter are the three male planets per BPHS.
b.add(
    conditions=[
        {"type": "or_group", "alternatives": [
            {"type": "planet_in_house", "planet": "Sun", "house": 3},
            {"type": "planet_in_house", "planet": "Mars", "house": 3},
            {"type": "planet_in_house", "planet": "Jupiter", "house": 3},
        ]},
    ],
    signal_group="h3_male_planet_brothers",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "brothers_born_after_native",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "Male planet (Sun, Mars, or Jupiter) in 3rd: brothers born after native. "
        "Male signs exclusively occupied by male planets → brothers."
    ),
    commentary_context=(
        "Santhanam: Sun, Mars, Jupiter are male planets. Saturn and Rahu treated "
        "as male for sex determination. Mercury and Ketu as female. This rule "
        "encodes the three primary male planets per verse text. Saturn/Rahu "
        "male treatment noted but not encoded as primary — they are neutral/"
        "shadowy planets reclassified only for sex-determination context."
    ),
    prediction_type="trait",
    tags=["male_planet", "h3", "brothers"],
)

# v.4 gap: 3rd house in odd sign (male sign) → male coborn tendency
# Verse: "All odd signs are male signs and all even signs are female signs.
# Male signs exclusively occupied by male planets will cause birth of brothers."
b.add(
    conditions=[
        {"type": "planet_in_sign_type", "planet": "lord_of_3", "sign_type": "odd"},
    ],
    signal_group="h3_odd_sign_male_coborn",
    direction="neutral", intensity="weak", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "male_coborn_tendency",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "3rd lord in odd (male) sign: tendency toward male co-born. "
        "Verse says odd signs = male signs, even = female."
    ),
    commentary_context=(
        "Santhanam: 'This should be known from the 3rd house being male or "
        "female sign & C.' Odd signs (Aries, Gemini, Leo, Libra, Sagittarius, "
        "Aquarius) are male signs. The 3rd lord's sign type serves as proxy for "
        "3rd cusp sign type since no house_sign_type primitive exists. If the "
        "3rd house is occupied by a male planet as well as in a male sign, the "
        "contribution is strong — brothers indicated."
    ),
    prediction_type="trait",
    tags=["sign_gender", "odd_sign", "male_coborn", "h3"],
)

# v.4 gap: 3rd house in even sign (female sign) → female coborn tendency
b.add(
    conditions=[
        {"type": "planet_in_sign_type", "planet": "lord_of_3", "sign_type": "even"},
    ],
    signal_group="h3_even_sign_female_coborn",
    direction="neutral", intensity="weak", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "female_coborn_tendency",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "3rd lord in even (female) sign: tendency toward female co-born. "
        "Even signs = female signs per verse."
    ),
    commentary_context=(
        "Contrary of odd-sign rule. Even signs (Taurus, Cancer, Virgo, Scorpio, "
        "Capricorn, Pisces) are female signs. Female sign + female planet = "
        "sisters. This is the sign-gender dimension; planet-gender is separate."
    ),
    prediction_type="trait",
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1425"]},
    tags=["sign_gender", "even_sign", "female_coborn", "h3"],
)

# v.4 gap: Mixed male + female planets in 3rd → coborn of both sexes
# Verse: "Should it be of mixed nature, coborn of both sexes will be obtained."
b.add(
    conditions=[
        {"type": "or_group", "alternatives": [
            {"type": "planet_in_house", "planet": "Sun", "house": 3},
            {"type": "planet_in_house", "planet": "Mars", "house": 3},
            {"type": "planet_in_house", "planet": "Jupiter", "house": 3},
        ]},
        {"type": "or_group", "alternatives": [
            {"type": "planet_in_house", "planet": "Venus", "house": 3},
            {"type": "planet_in_house", "planet": "Moon", "house": 3},
        ]},
    ],
    signal_group="h3_mixed_planets_both_sexes",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "coborn_of_both_sexes",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.6},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "Both male and female planets in 3rd: co-born of both sexes. "
        "Verse: 'Should it be of mixed nature, coborn of both sexes will be obtained.'"
    ),
    commentary_context=(
        "Santhanam: If the 3rd house is occupied by a male planet as well as "
        "a female planet, there will be brothers and sisters as well. This "
        "requires at least one male planet (Sun/Mars/Jupiter) AND at least one "
        "female planet (Venus/Moon) in the 3rd house simultaneously."
    ),
    prediction_type="trait",
    tags=["mixed_planets", "h3", "both_sexes", "coborn"],
)

# v.12-13 gap: Full condition — 11th/12th lord joins Mars+Jupiter + Moon in 3rd → 7 coborn
# Existing BPHS1408 only has Moon in 3rd. The full verse condition is more complex.
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Moon", "house": 3},
        {"type": "planets_conjunct", "planets": ["Mars", "Jupiter"]},
        {"type": "or_group", "alternatives": [
            {"type": "planets_conjunct", "planets": ["lord_of_11", "Mars"]},
            {"type": "planets_conjunct", "planets": ["lord_of_12", "Mars"]},
        ]},
    ],
    signal_group="moon_h3_mars_jupiter_11_12_lord_7coborn",
    direction="favorable", intensity="strong", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "seven_coborn_full_condition",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.12-13",
    description=(
        "11th or 12th lord joins Mars and Jupiter while Moon occupies 3rd: "
        "7 co-born indicated. Full condition from verse (some texts read "
        "12th lord instead of 11th)."
    ),
    commentary_context=(
        "Verse: 'There will be 7 coborn if the 12th lord (some texts read "
        "as the 11th lord) joins Mars and Jupiter while the 3rd is occupied "
        "by the Moon.' BPHS1408 encodes the simpler Moon-in-3rd condition; "
        "this encodes the full multi-planet combination."
    ),
    rule_relationship={"type": "addition", "related_rules": ["BPHS1408"]},
    tags=["moon", "mars", "jupiter", "h3", "7_coborn", "multi_planet"],
)

# v.12-13 gap: Moon alone in 3rd + male planet aspect → younger brothers
# Existing BPHS1420 encodes Venus aspect → sisters. This is the male counterpart.
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Moon", "house": 3},
        {"type": "or_group", "alternatives": [
            {"type": "planet_aspecting", "planet": "Sun", "house": 3},
            {"type": "planet_aspecting", "planet": "Mars", "house": 3},
            {"type": "planet_aspecting", "planet": "Jupiter", "house": 3},
        ]},
    ],
    signal_group="moon_h3_male_aspect_brothers",
    direction="neutral", intensity="moderate", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "younger_brothers_indicated",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.14 v.12-13",
    description=(
        "Moon alone in 3rd with male planet (Sun/Mars/Jupiter) aspect: "
        "younger brothers indicated."
    ),
    commentary_context=(
        "Verse: 'If the Moon is lonely placed in the 3rd in aspect to male "
        "planets, there will be younger brothers.' Male planets = Sun, Mars, "
        "Jupiter. BPHS1420 encodes the Venus aspect → sisters counterpart."
    ),
    prediction_type="trait",
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1420"]},
    tags=["moon", "h3", "male_aspect", "younger_brothers"],
)

# v.14 gap: Mars in 3rd → 2 brothers + 2 sisters, all pass early (Garga Maharshi)
# BPHS1411 encodes the general "both elder and younger destroyed" claim.
# Garga Maharshi's specific prediction is a distinct claim with specific numbers.
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mars", "house": 3}],
    signal_group="mars_h3_garga_4_siblings_early_death",
    direction="unfavorable", intensity="strong", primary_domain="longevity",
    predictions=[
        {"entity": "siblings", "claim": "two_brothers_two_sisters_pass_early",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.14 v.14",
    description=(
        "Mars in 3rd: Garga Maharshi says native will obtain two brothers "
        "and two sisters, all four of whom will pass away early."
    ),
    commentary_context=(
        "Santhanam: 'Regarding Mars in the 3rd, Garga Maharshi states that "
        "the native will obtain two brothers and two sisters all the 4 of "
        "whom will pass away early.' This is a specific numbered prediction "
        "from Garga, distinct from the general claim in BPHS1411."
    ),
    concordance_texts=["Garga Samhita"],
    rule_relationship={"type": "addition", "related_rules": ["BPHS1411"]},
    tags=["mars", "h3", "garga", "sibling_death", "specific_count"],
)

# v.4 gap: Saturn in 3rd → brothers (male planet per Santhanam's notes)
# Verse says "male planets" generically; Santhanam's note on p.139 classifies
# Saturn and Rahu as male for sex determination. This is translator
# classification, not verse text (Principle #8, L013). Confidence reduced.
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 3}],
    signal_group="h3_saturn_male_brothers",
    direction="neutral", intensity="weak", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "brothers_born_after_native",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.55},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "Saturn (treated as male planet) in 3rd: brothers born after native. "
        "Saturn's male classification is from Santhanam's notes, not verse text."
    ),
    commentary_context=(
        "Santhanam p.139: 'Saturn and Rahu be treated as males while Mercury "
        "and Ketu are females.' This is translator classification for sex "
        "determination context, not direct verse statement. The verse itself "
        "names 'male planets' without enumerating which planets are male. "
        "Sun/Mars/Jupiter are the primary male planets (BPHS1424). Saturn is "
        "a secondary male classification per Santhanam. Confidence reduced by "
        "0.05 per L013 (translator gloss ≠ verse text)."
    ),
    prediction_type="trait",
    rule_relationship={"type": "addition", "related_rules": ["BPHS1424"]},
    tags=["male_planet", "saturn", "h3", "brothers", "santhanam_note"],
)

# v.4 gap: Rahu in 3rd → brothers (male planet per Santhanam's notes)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": 3}],
    signal_group="h3_rahu_male_brothers",
    direction="neutral", intensity="weak", primary_domain="progeny",
    predictions=[
        {"entity": "siblings", "claim": "brothers_born_after_native",
         "domain": "progeny", "direction": "neutral", "magnitude": 0.55},
    ],
    verse_ref="Ch.14 v.4",
    description=(
        "Rahu (treated as male planet) in 3rd: brothers born after native. "
        "Rahu's male classification is from Santhanam's notes, not verse text."
    ),
    commentary_context=(
        "Santhanam p.139: 'Saturn and Rahu be treated as males while Mercury "
        "and Ketu are females.' Same translator classification as Saturn rule. "
        "Rahu does not own any house but is classified as male for sex "
        "determination context per Santhanam's notes. Confidence reduced by "
        "0.05 per L013."
    ),
    prediction_type="trait",
    rule_relationship={"type": "addition", "related_rules": ["BPHS1424"]},
    tags=["male_planet", "rahu", "h3", "brothers", "santhanam_note"],
)

BPHS_V2_CH14_REGISTRY = b.build()
