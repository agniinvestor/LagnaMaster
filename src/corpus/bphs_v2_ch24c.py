"""src/corpus/bphs_v2_ch24c.py — BPHS Ch.24 Part C: Lords 9-12 + Misc.

S311: BPHS Phase 1B Block B — Effects of the Bhava Lords (final part).
Slokas 97-148: 9th through 12th lord in all 12 houses + 4 miscellaneous.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.220-236.
Verse audit: data/verse_audits/ch24_audit.json (complete from S309).

Confidence formula (Phase 1B mechanical):
  base = 0.60 + 0.05 (verse_ref) = 0.65 minimum
  + 0.08 per concordance text
  - 0.05 per divergence text
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.24", category="bhava_lord_effects",
    id_start=2506, session="S311", sloka_count=52,
    chapter_tags=["bhava_lords", "lord_placement"],
    entity_target="native",
    prediction_type="trait",
)

# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 97-108: 9TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.220-223
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 97: 9th lord in 1st ─────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 1}],
    signal_group="h9_lord_in_h1_fortunate_honoured",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "fortunate_prosperous_honoured_by_king_virtuous_charming_learned",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.97",
    description="9th lord in ascendant: fortunate (or prosperous), honoured by the king, virtuous, charming, learned, honoured by public.",
    commentary_context="Santhanam: If the 9th lord is in the rising sign, the native will hold a very high position which will bring him wealth and fame. He will be free from enemies. A female having the said position will prove a worthy housewife and be rid of afflictions from other planetary sources. These effects will not be enjoyed by a Scorpio native.",
    concordance_texts=["Saravali", "Phaladeepika"],
    exceptions=["scorpio_ascendant_not_enjoy_these_effects"],
)

# ── Sloka 98: 9th lord in 2nd ─────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 2}],
    signal_group="h9_lord_in_h2_scholar_wealthy",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "scholar_dear_to_all_wealthy_sensuous_happiness_wife_sons",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.98",
    description="9th lord in 2nd: be a scholar, dear to all, wealthy, sensuous, endowed with happiness from wife and sons.",
    commentary_context="Santhanam: No separate note. The 9th lord (fortune) in the 2nd (wealth/family) is one of the most favourable combinations for prosperity.",
    concordance_texts=["Saravali"],
)

# ── Sloka 99: 9th lord in 3rd ─────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 3}],
    signal_group="h9_lord_in_h3_fraternal_bliss",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "fraternal_bliss_wealthy_virtuous_charming",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.99",
    description="9th lord in 3rd: endowed with fraternal bliss, wealthy, virtuous and charming.",
    commentary_context="Santhanam: No separate note. Straightforward favourable reading.",
)

# ── Sloka 100: 9th lord in 4th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 4}],
    signal_group="h9_lord_in_h4_conveyances_devoted_mother",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "houses_conveyances_happiness_all_kinds_wealth_devoted_to_mother",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.100",
    description="9th lord in 4th: enjoy houses, conveyances and happiness, have all kinds of wealth, devoted to mother.",
    commentary_context="Santhanam: No separate note. The 9th-4th axis connects fortune with domestic comfort — one of the most auspicious placements.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 101: 9th lord in 5th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 5}],
    signal_group="h9_lord_in_h5_sons_prosperity",
    direction="favorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "endowed_sons_prosperity_devoted_to_elders_bold_charitable_learned",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.101",
    description="9th lord in 5th: endowed with sons and prosperity, devoted to elders, bold, charitable and learned.",
    commentary_context="Santhanam: No separate note. The 9th (fortune/dharma) in the 5th (purva punya/children) creates a highly auspicious trikona-trikona connection.",
    concordance_texts=["Saravali"],
)

# ── Sloka 102: 9th lord in 6th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 6}],
    signal_group="h9_lord_in_h6_meagre_prosperity",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "meagre_prosperity_devoid_happiness_maternal_relatives_troubled_enemies",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.102",
    description="9th lord in 6th: enjoy meagre prosperity, devoid of happiness from maternal relatives, always troubled by enemies.",
    commentary_context="Santhanam: No separate note. The fortune lord in the house of enemies/disease impedes prosperity.",
)

# ── Sloka 103: 9th lord in 7th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 7}],
    signal_group="h9_lord_in_h7_happiness_after_marriage",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "happiness_after_marriage_virtuous_famous_success_all_undertakings",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.103",
    description="9th lord in 7th: beget happiness after marriage, be virtuous and famous. Success in all undertakings.",
    commentary_context="Santhanam: One will further be able to achieve success in all his undertakings. His prosperity will pick up after marriage. The native will be not well disposed to his father. These are additional effects due to the 7th house placement of the 9th lord.",
    concordance_texts=["Saravali"],
)

# ── Sloka 104: 9th lord in 8th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 8}],
    signal_group="h9_lord_in_h8_not_prosperous",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "not_prosperous_no_happiness_from_elder_brother_devoid_fortunes",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.104",
    description="9th lord in 8th: not be prosperous, will not enjoy happiness from elder brother.",
    commentary_context="Santhanam: Having got the 9th lord relegated to the 8th house, one will be devoid of fortunes. He will face failures in all his undertakings. He will not achieve professional and financial stability. His father will primarily incur a cut in longevity. A blessing in disguise with this position is a probable inheritance of patrimony by the native.",
    concordance_texts=["Saravali"],
)

# ── Sloka 105: 9th lord in 9th ────────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 9}],
    signal_group="h9_lord_in_h9_abundant_fortunes",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "abundant_fortunes_virtues_beauty_happiness_from_coborn",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.24 v.105",
    description="9th lord in 9th: endowed with abundant fortunes, virtues and beauty, enjoy much happiness from co-born.",
    commentary_context="Santhanam: Should the 9th lord be in the 9th itself, one will obtain fraternal bliss. His co-born will amass fortune. The native himself will own properties in a large scale. He will achieve easy success in each and every undertaking. His father will play a significant role in his (i.e. the native's) progress. The native's mother will be free from diseases. He will be nurtured by his maternal grand parents.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 106: 9th lord in 10th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 10}],
    signal_group="h9_lord_in_h10_king_minister",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "king_or_minister_or_army_chief_virtuous_dear_to_all",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.24 v.106",
    description="9th lord in 10th: be a king or equal to him, or be a minister or an army chief, be virtuous and dear to all.",
    commentary_context="Santhanam: The sage suggests that with the 9th lord going to the 10th the native will be either a king or a minister or an army chief. Apparently, if the 9th lord is prepotent, one will enjoy royal status. The strength proportionately falling down will make the native enjoy comparatively lesser positions.",
    concordance_texts=["Saravali", "Phaladeepika"],
    modifiers=[{"condition": "strength_proportionate_prepotent_royal_decreasing_lesser_positions", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
)

# ── Sloka 107: 9th lord in 11th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 11}],
    signal_group="h9_lord_in_h11_financial_gains",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "financial_gains_day_by_day_devoted_elders_virtuous_meritorious",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.107",
    description="9th lord in 11th: enjoy financial gains day by day, devoted to elders, virtuous and meritorious in acts.",
    commentary_context="Santhanam: The native who has the 9th lord in the 11th house will see increasing phases of fortunes and prosperity. Hence the said position is extremely favourable for material upliftment. This will, however, not apply to Gemini ascendant having Saturn, the 9th lord, in the 11th house. On the opposite end it will prove highly detrimental for the prosperity of the native.",
    concordance_texts=["Saravali"],
    exceptions=["gemini_ascendant_saturn_in_11th_opposite_effect"],
)

# ── Sloka 108: 9th lord in 12th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 12}],
    signal_group="h9_lord_in_h12_loss_fortunes",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "loss_fortunes_spend_auspicious_acts_poor_entertaining_guests",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.108",
    description="9th lord in 12th: incur loss of fortunes, always spend on auspicious acts, become poor on account of entertaining guests.",
    commentary_context="Santhanam: The 9th lord in the 12th is said to cause loss of wealth on account of entertaining guests. In modern context lavish parties will take this role. The native will land in financial difficulties on account of throwing parties and the like. This position is not also auspicious for the happiness of elder brothers and sisters.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 109-120: 10TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.223-229
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 109: 10th lord in 1st ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 1}],
    signal_group="h10_lord_in_h1_scholarly_famous",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "scholarly_famous_poet_diseases_boyhood_happy_later_wealth_daily",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.109",
    description="10th lord in ascendant: scholarly, famous, be a poet, will incur diseases in boyhood and be happy later on. Wealth increases day by day.",
    commentary_context="Santhanam: The 10th lord occupying the ascendant is very favourable for riches giving a royal status to the native. The horoscope of Sarabhoji Maharaja of Tanjore is given as example — Mercury as 10th lord in own sign in the ascendant.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 110: 10th lord in 2nd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 2}],
    signal_group="h10_lord_in_h2_wealthy_charitable",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_virtuous_honoured_by_king_charitable_happiness_father",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.110",
    description="10th lord in 2nd: wealthy, virtuous, honoured by the king, charitable, happiness from father and others.",
    commentary_context="Santhanam: The placement of the 10th lord in the 2nd will give immeasurable financial success through one's own profession or calling, apart from a large scale patrimony. This will be more effective for Gemini ascendant having the 10th lord Jupiter in the 2nd in exaltation. Example: Morarji Desai, erstwhile Prime Minister of India.",
    concordance_texts=["Saravali"],
)

# ── Sloka 111: 10th lord in 3rd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 3}],
    signal_group="h10_lord_in_h3_valorous_truthful",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "happiness_brothers_servants_valorous_virtuous_eloquent_truthful",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.111",
    description="10th lord in 3rd: enjoy happiness from brothers and servants, be valorous, virtuous, eloquent and truthful.",
    commentary_context="Santhanam: No separate note. The 10th lord (career/action) in the 3rd (effort/siblings) supports industrious and truthful character.",
)

# ── Sloka 112: 10th lord in 4th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 4}],
    signal_group="h10_lord_in_h4_mother_conveyances",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "happy_interested_mother_welfare_conveyances_lands_houses_virtuous_wealthy",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.112",
    description="10th lord in 4th: happy, always interested in mother's welfare, lord over conveyances, lands, houses, be virtuous and wealthy.",
    commentary_context="Santhanam: No separate note. The 10th lord in the 4th creates a kendra-kendra axis — strong for property and maternal relationship.",
    concordance_texts=["Saravali"],
)

# ── Sloka 113: 10th lord in 5th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 5}],
    signal_group="h10_lord_in_h5_learning_sons",
    direction="favorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "all_kinds_learning_always_delighted_wealthy_endowed_sons",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.113",
    description="10th lord in 5th: endowed with all kinds of learning, always delighted, wealthy, endowed with sons.",
    commentary_context="Santhanam: The lord of the 10th house will prove a great asset for the native bestowing abundant wealth which will never leave him. He will have a number of children. There will seldom be filial grief for him. He will always move among wealthy people. In the matter of learning and education, sky is the limit in his case. Example: Rabindranath Tagore (born May 7, 1861 at 3.15 AM IST at 22N35 88E30). Note the 10th lord Jupiter in exaltation in the 5th.",
    concordance_texts=["Saravali"],
)

# ── Sloka 114: 10th lord in 6th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 6}],
    signal_group="h10_lord_in_h6_bereft_paternal",
    direction="unfavorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "bereft_paternal_bliss_skilful_but_bereft_wealth_troubled_enemies",
         "domain": "career", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.114",
    description="10th lord in 6th: bereft of paternal bliss, skilful but bereft of wealth, troubled by enemies.",
    commentary_context="Santhanam: The 10th lord going to the 6th house is a dire blemish for professional and monetary stability. One will undergo frequent changes in his calling and will suffer losses therein. His financial growth will be severely paralyzed. He will have a number of enemies contributing to his decline. He will incur lasting diseases. An advantage, however, will come to him in the form of extreme intelligence.",
    modifiers=[{"condition": "advantage_of_extreme_intelligence_despite_career_and_financial_paralysis", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 115: 10th lord in 7th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 7}],
    signal_group="h10_lord_in_h7_happy_wife_virtuous",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "endowed_happiness_through_wife_intelligent_virtuous_eloquent_religious",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.115",
    description="10th lord in 7th: endowed with happiness through wife, be intelligent, virtuous, eloquent, truthful and religious.",
    commentary_context="Santhanam: No separate note. The 10th lord in the 7th connects career with partnership — favourable for marriage-related gains.",
    concordance_texts=["Saravali"],
)

# ── Sloka 116: 10th lord in 8th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 8}],
    signal_group="h10_lord_in_h8_devoid_good_acts",
    direction="unfavorable", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "devoid_good_acts_longlived_intent_on_blaming_others",
         "domain": "career", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.116",
    description="10th lord in 8th: devoid of (good) acts, longlived, intent on blaming others.",
    commentary_context="Santhanam: The 10th lord's placement in the 8th house denotes potence of longevity — one's Karmic credit and his strength or his position in the 8th house will contribute to great longevity. That the 10th lord should be considered akin to Saturn in the matter of life span is a fact taught to us by Maharshi Parasara. The rule will, however, not apply to Gemini ascendant having Jupiter in the 8th (in fall). And a Leo native with Venus (a significant beneficiary) in the 8th in exaltation will enjoy a considerably long span of life.",
    concordance_texts=["Saravali"],
    exceptions=["gemini_ascendant_jupiter_in_8th_fall_adversely_affects_longevity", "leo_ascendant_venus_in_8th_exaltation_long_span"],
)

# ── Sloka 117: 10th lord in 9th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 9}],
    signal_group="h10_lord_in_h9_royal_scion",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "born_royal_scion_king_equal_progenic_happiness_wealth",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.24 v.117",
    description="10th lord in 9th: born of royal scion, be a king or equal to a king, progenic happiness and wealth.",
    commentary_context="Santhanam: No separate note. The 9th-10th connection (Dharma-Karma Adhipati yoga) is the highest Rajayoga combination in Parashari doctrine.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 118: 10th lord in 10th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 10}],
    signal_group="h10_lord_in_h10_skilful_all_jobs",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "skilful_in_all_jobs_valorous_truthful_devoted_to_elders",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.118",
    description="10th lord in 10th: skilful in all jobs, be valorous, truthful and devoted to elders.",
    commentary_context="Santhanam: No separate note. Lord in own house produces the strongest natural significations for career mastery.",
    concordance_texts=["Saravali"],
)

# ── Sloka 119: 10th lord in 11th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 11}],
    signal_group="h10_lord_in_h11_wealth_sons",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "endowed_wealth_happiness_sons_virtuous_truthful_always_delighted",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.119",
    description="10th lord in 11th: endowed with wealth, happiness and sons, be virtuous, truthful and always delighted.",
    commentary_context="Santhanam: No separate note. The 10th lord in the 11th (gains house) directly channels professional success into material accumulation.",
    concordance_texts=["Saravali"],
)

# ── Sloka 120: 10th lord in 12th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 12}],
    signal_group="h10_lord_in_h12_spend_royal_fear",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "spend_through_royal_abodes_fear_enemies_skilful_worried",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.120",
    description="10th lord in 12th: spend through royal abodes (i.e. kings), have fear from enemies, be skilful but worried.",
    commentary_context="Santhanam: Expenditure through royal abodes possibly indicates that the native will lose on taxes, fines etc. to the government as the 12th house is involved. Otherwise, this can mean luxurious political expenses. This placement will cause troubles in financial matters through the government.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 121-132: 11TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.229-233
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 121: 11th lord in 1st ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 1}],
    signal_group="h11_lord_in_h1_genuine_rich",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "genuine_rich_happy_even_sighted_poet_eloquent_endowed_gains",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.121",
    description="11th lord in ascendant: genuine in disposition, rich, happy, even-sighted, be a poet, eloquent, always endowed with gains.",
    commentary_context="Santhanam: When the 11th lord is in the ascendant, the native will always befriend the virtuous and reject evil associations. He will be extremely prosperous after marriage.",
    concordance_texts=["Saravali"],
)

# ── Sloka 122: 11th lord in 2nd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 2}],
    signal_group="h11_lord_in_h2_all_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "all_kinds_wealth_accomplishments_charitable_religious_always_happy",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.122",
    description="11th lord in 2nd: all kinds of wealth, all kinds of accomplishments, charitable, religious, always happy.",
    commentary_context="Santhanam: No separate note. The gains lord in the wealth house is naturally one of the best combinations for material prosperity.",
    concordance_texts=["Saravali"],
)

# ── Sloka 123: 11th lord in 3rd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 3}],
    signal_group="h11_lord_in_h3_skilful_wealthy",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "skilful_all_jobs_wealthy_fraternal_bliss_sometimes_gout",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.123",
    description="11th lord in 3rd: skilful in all jobs, wealthy, endowed with fraternal bliss, may sometimes incur gout pains.",
    commentary_context="Santhanam: No separate note. Minor health defect (gout) mentioned alongside generally favourable results.",
)

# ── Sloka 124: 11th lord in 4th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 4}],
    signal_group="h11_lord_in_h4_maternal_gains",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_from_maternal_relatives_visits_shrines_house_lands_happiness",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.124",
    description="11th lord in 4th: gain from maternal relatives, undertake visits to shrines, happiness of house and lands.",
    commentary_context="Santhanam: No separate note. The 11th lord (gains) in the 4th (mother/property) brings maternal-line financial support.",
    concordance_texts=["Saravali"],
)

# ── Sloka 125: 11th lord in 5th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 5}],
    signal_group="h11_lord_in_h5_happy_children",
    direction="favorable", intensity="moderate",
    primary_domain="progeny",
    entity_target="children",
    predictions=[
        {"entity": "children", "claim": "children_happy_educated_virtuous_himself_religious_happy",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.125",
    description="11th lord in 5th: native's children will be happy, educated and virtuous. Himself religious and happy.",
    commentary_context="Santhanam: No separate note. The 11th in the 5th connects gains with children — prosperity through/for children.",
)

# ── Sloka 126: 11th lord in 6th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 6}],
    signal_group="h11_lord_in_h6_diseases_foreign",
    direction="unfavorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "afflicted_diseases_cruel_foreign_places_troubled_enemies",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.126",
    description="11th lord in 6th: afflicted by diseases, be cruel, living in foreign places, troubled by enemies.",
    commentary_context="Santhanam: The placement of the 11th lord in the 6th house will augment the chances of 'acquisition' of diseases. The native will incur defects of hearing organ. (In Aquarius, the 11th lord will particularly afflict a Virgo native with dire deafness.) The native will be so selfish that for his own happiness, he will leave his family members and live away from his home or hometown. Servitude will befit him rather than an independent profession. He will often undergo financial reversals.",
)

# ── Sloka 127: 11th lord in 7th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 7}],
    signal_group="h11_lord_in_h7_gain_wife_relatives",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_through_wife_relatives_liberal_virtuous_sensuous_command_spouse",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.127",
    description="11th lord in 7th: always gain through wife's relatives, liberal, virtuous, sensuous, remain at command of spouse.",
    commentary_context="Santhanam: Should the 7th house be occupied by the 11th lord, the native will always look upto and receive help from his wife's relatives. He will be quite affluent. He will lack wisdom and judgement in the matter of expenses and he cannot make out where to spend and where not. A strong urge to seek union with others' females will always be prevalent in him but none will bother for him. Even his own spouse will boss over him.",
    concordance_texts=["Saravali"],
)

# ── Sloka 128: 11th lord in 8th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 8}],
    signal_group="h11_lord_in_h8_reversals_longlived",
    direction="mixed", intensity="moderate",
    primary_domain="longevity",
    predictions=[
        {"entity": "native", "claim": "reversals_in_all_undertakings_but_longlived",
         "domain": "longevity", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.128",
    description="11th lord in 8th: incur reversals in all undertakings, but live long.",
    commentary_context="Santhanam: The 11th lord in the 8th house increases the native's longevity. Mars in the 8th being the 11th lord for Gemini bears ample testimony to this effect. However, this rule should not be applied to Leo ascendant having Mercury (the 11th lord) in the 8th house in debilitation.",
    concordance_texts=["Saravali"],
    exceptions=["leo_ascendant_mercury_11th_lord_in_8th_debilitation_not_apply"],
)
# v.128 split: wife will predecease
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 8}],
    signal_group="h11_lord_in_h8_wife_predecease",
    direction="unfavorable", intensity="strong",
    primary_domain="longevity",
    entity_target="spouse",
    predictions=[
        {"entity": "spouse", "claim": "wife_will_predecease_the_native",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.128",
    description="11th lord in 8th: wife will predecease him.",
    commentary_context="Santhanam: Split from native longevity prediction — same verse, distinct entity per granularity principle #2.",
    concordance_texts=["Saravali"],
)

# ── Sloka 129: 11th lord in 9th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 9}],
    signal_group="h11_lord_in_h9_fortunate_skilful",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "fortunate_skilful_truthful_honoured_by_king_affluent",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.129",
    description="11th lord in 9th: fortunate, skilful, truthful, honoured by the king, affluent.",
    commentary_context="Santhanam: No separate note. The 11th-9th connection is naturally auspicious — gains through fortune/dharma.",
    concordance_texts=["Saravali"],
)

# ── Sloka 130: 11th lord in 10th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 10}],
    signal_group="h11_lord_in_h10_honoured_religious",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "honoured_by_king_virtuous_religious_truthful_intelligent_subdue_senses",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.130",
    description="11th lord in 10th: honoured by the king, virtuous, attached to religion, truthful, intelligent, subdue his senses.",
    commentary_context="Santhanam: With the 11th lord occupying the 10th house, one will be primarily intent on public welfare and redemption. He will delve deep into the core of his religion and bring out myriad truths to educate the public. He will create an epoch of his own which will go into the pages of history. Example: Sri Bhakti Vedanta Swamiji (ISKCON founder) — born September 1st, 1896 AD, at 1530 hrs at Calcutta. 11th lord Venus is in the 10th in debilitation but with the 10th lord Mercury in exaltation (Neechabhanga).",
    concordance_texts=["Saravali"],
)

# ── Sloka 131: 11th lord in 11th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 11}],
    signal_group="h11_lord_in_h11_gain_all",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_in_all_undertakings_learning_happiness_increase_daily",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.131",
    description="11th lord in 11th: gain in all undertakings, learning and happiness will increase day by day.",
    commentary_context="Santhanam: No separate note. Lord in own house = strongest natural signification for ever-increasing gains.",
    concordance_texts=["Saravali"],
)

# ── Sloka 132: 11th lord in 12th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 12}],
    signal_group="h11_lord_in_h12_good_deeds_sensuous",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "expend_good_deeds_sensuous_many_wives_befriend_foreigners",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.132",
    description="11th lord in 12th: always expend on good deeds, be sensuous, have many wives, befriend barbarians (or foreigners in general).",
    commentary_context="Santhanam: No separate note. Mixed result — charitable spending alongside sensuous tendencies and foreign connections.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 133-144: 12TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.233-235
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 133: 12th lord in 1st ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 1}],
    signal_group="h12_lord_in_h1_spendthrift_weak",
    direction="unfavorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "spendthrift_weak_constitution_phlegmatic_disorders_devoid_wealth_learning",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.133",
    description="12th lord in ascendant: spendthrift, weak in constitution, phlegmatic disorders, devoid of wealth and learning.",
    commentary_context="Santhanam: Phlegmatic disorders relate to breathing troubles, lung disorders, tuberculosis etc. With the 12th lord going to the rising sign, the native will always suffer from one disease or the other. He will ever be in the grip of fear of death. He will acquire many vices. His undertakings will not yield success.",
)

# ── Sloka 134: 12th lord in 2nd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 2}],
    signal_group="h12_lord_in_h2_auspicious_religious",
    direction="favorable", intensity="moderate",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "spend_auspicious_deeds_religious_speak_sweetly_virtues_happiness",
         "domain": "spirituality", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.134",
    description="12th lord in 2nd: always spend on auspicious deeds, be religious, speak sweetly, endowed with virtues and happiness.",
    commentary_context="Santhanam: No separate note. The 12th lord (expenditure) in the 2nd (speech/wealth) channels spending toward dharmic purposes.",
)

# ── Sloka 135: 12th lord in 3rd ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 3}],
    signal_group="h12_lord_in_h3_no_fraternal_bliss",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "devoid_fraternal_bliss_hate_others_promote_self_nourishment_selfish",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.135",
    description="12th lord in 3rd: devoid of fraternal bliss, hate others, promote self-nourishment (i.e. be quite selfish).",
    commentary_context="Santhanam: No separate note. The loss lord in the siblings house denies co-born happiness.",
)

# ── Sloka 136: 12th lord in 4th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 4}],
    signal_group="h12_lord_in_h4_devoid_maternal",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_maternal_happiness_day_by_day_losses_lands_conveyances_houses",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.136",
    description="12th lord in 4th: devoid of maternal happiness, day by day accrue losses in respect of lands, conveyances and houses.",
    commentary_context="Santhanam: No separate note. The 12th lord (loss) in the 4th (property) directly erodes domestic assets.",
)

# ── Sloka 137: 12th lord in 5th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 5}],
    signal_group="h12_lord_in_h5_bereft_sons",
    direction="unfavorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "bereft_sons_learning_spend_visit_shrines_to_beget_son",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.137",
    description="12th lord in 5th: bereft of sons and learning, spend as well as visit shrines in order to beget a son.",
    commentary_context="Santhanam: No separate note. The 12th lord in the 5th denies children and learning — the native resorts to pilgrimages seeking divine intervention for progeny.",
)

# ── Sloka 138: 12th lord in 6th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 6}],
    signal_group="h12_lord_in_h6_enmity_sinful",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "enmity_own_men_anger_sinful_miserable_others_wives",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.138",
    description="12th lord in 6th: enmity with own men, given to anger, be sinful, miserable, go to others' wives.",
    commentary_context="Santhanam: No separate note. Double dusthana interaction — the loss lord in the enemy house compounds both domains.",
)

# ── Sloka 139: 12th lord in 7th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 7}],
    signal_group="h12_lord_in_h7_expenditure_wife",
    direction="unfavorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "expenditure_on_wife_not_enjoy_conjugal_bliss_bereft_learning_strength",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.139",
    description="12th lord in 7th: incur expenditure on account of wife, not enjoy conjugal bliss, bereft of learning and strength.",
    commentary_context="Santhanam: No separate note. The 12th lord in the 7th channels loss through the spouse domain.",
)

# ── Sloka 140: 12th lord in 8th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 8}],
    signal_group="h12_lord_in_h8_always_gain",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "always_gain_speak_affably_medium_span_life_all_good_qualities",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.140",
    description="12th lord in 8th: always gain, speak affably, enjoy medium span of life, endowed with all good qualities.",
    commentary_context="Santhanam: By 'medium life' it is meant to denote a span of life of 60 years. So to say the 12th lord in the 8th will not be in a position to contribute to higher bracket of longevity.",
    concordance_texts=["Saravali"],
)

# ── Sloka 141: 12th lord in 9th ───────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 9}],
    signal_group="h12_lord_in_h9_dishonour_elders",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "dishonour_elders_inimical_friends_intent_own_ends",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.141",
    description="12th lord in 9th: dishonour his elders, be inimical even to friends, always intent on achieving own ends.",
    commentary_context="Santhanam: No separate note. The 12th lord in the 9th disrupts dharma and relationships with elders.",
)

# ── Sloka 142: 12th lord in 10th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 10}],
    signal_group="h12_lord_in_h10_expenditure_royal",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "expenditure_through_royal_persons_moderate_paternal_bliss_only",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.142",
    description="12th lord in 10th: incur expenditure through royal persons, enjoy only moderate paternal bliss.",
    commentary_context="Santhanam: No separate note. The 12th lord in the 10th channels losses through authority figures and government.",
)

# ── Sloka 143: 12th lord in 11th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 11}],
    signal_group="h12_lord_in_h11_incur_losses",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "incur_losses_brought_up_others_gain_through_others_sometimes",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.143",
    description="12th lord in 11th: incur losses, be brought up by others, will sometimes gain through others.",
    commentary_context="Santhanam: One will face obstacles in begetting a child if the 12th lord occupies the 11th house. He will at last adopt a child.",
    modifiers=[{"condition": "obstacles_begetting_child_will_at_last_adopt", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 144: 12th lord in 12th ──────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 12, "house": 12}],
    signal_group="h12_lord_in_h12_heavy_expenditure",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "heavy_expenditure_only_no_physical_felicity_iritable_spiteful",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.144",
    description="12th lord in 12th: face heavy expenditure only, not have physical felicity, be iritable and spiteful.",
    commentary_context="Santhanam: No separate note. Lord in own house reinforces the 12th house signification of loss and expenditure at its strongest.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 145-148: MISCELLANEOUS — DUAL LORDSHIP RESOLUTION
# Santhanam Vol 1, pp.235-236
# ═══════════════════════════════════════════════════════════════════════════════

# ── Slokas 145-148: Dual lordship principles ──────────────────────────────
b.add(
    conditions=[],
    signal_group="dual_lordship_contrary_results_nullified",
    direction="neutral", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "general", "claim": "planet_owning_two_bhavas_contrary_results_nullified",
         "domain": "wealth", "direction": "neutral", "magnitude": 0.5},
    ],
    entity_target="general",
    verse_ref="Ch.24 v.145-146",
    description="Miscellaneous: a planet owning two bhavas — results deduced considering both lordships. If opposing results, they are nullified.",
    commentary_context="Santhanam: In the case of a planet owning two bhavas, the results are to be deducted based on its two lordships (for the same placement). If opposing results are thus indicated, the results will be nullified, while results of varied nature will come to pass.",
    prediction_type="trait",
    modifiers=[{"condition": "opposing_results_from_dual_lordship_nullify_each_other", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
)

b.add(
    conditions=[],
    signal_group="dual_lordship_strength_based_yield",
    direction="neutral", intensity="conditional",
    primary_domain="wealth",
    predictions=[
        {"entity": "general", "claim": "planet_yields_full_half_quarter_based_on_strength",
         "domain": "wealth", "direction": "neutral", "magnitude": 0.5},
    ],
    entity_target="general",
    verse_ref="Ch.24 v.147",
    description="Miscellaneous: the planet will yield full, half or a quarter of results according to its strength being full, medium or negligible respectively.",
    commentary_context="Santhanam: The planet will yield full, half or a quarter of the effects according to its strength being full, medium and negligible respectively. Thus I have told you about the effects due to bhava lords in various bhavas.",
    prediction_type="trait",
)

b.add(
    conditions=[],
    signal_group="sun_moon_single_lordship_direct",
    direction="neutral", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "general", "claim": "sun_moon_own_one_sign_results_come_to_pass_directly",
         "domain": "wealth", "direction": "neutral", "magnitude": 0.5},
    ],
    entity_target="general",
    verse_ref="Ch.24 v.148",
    description="Miscellaneous: Sun and Moon own one sign each — results cited will come to pass directly without dual-lordship modification.",
    commentary_context="Santhanam: In the case of the Sun and the Moon, the results cited will come to pass. Here also one should give due consideration to various other relative factors. Simply applying the effects without checking other relative factors will lead to pitfalls. Example: Saturn in 5th for Pisces — as 11th lord gives children/happiness through them, as 12th lord denies education. Resolution: check Jupiter (5th karaka) and Moon (5th lord from Chandra lagna).",
    prediction_type="trait",
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH24C_REGISTRY = b.build()
