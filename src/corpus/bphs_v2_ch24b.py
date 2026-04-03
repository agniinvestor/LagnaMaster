"""src/corpus/bphs_v2_ch24b.py — BPHS Ch.24 Part B: Lords 5-8 in 12 Houses.

S310: BPHS Phase 1B Block B — Effects of the Bhava Lords (continued).
Slokas 49-96: 5th through 8th lord in all 12 houses.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.202-220.
Verse audit: data/verse_audits/ch24_audit.json (already complete from S309).

Confidence formula (Phase 1B mechanical):
  base = 0.60 + 0.05 (verse_ref) = 0.65 minimum
  + 0.08 per concordance text
  - 0.05 per divergence text
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.24", category="bhava_lord_effects",
    id_start=2456, session="S310", sloka_count=48,
    chapter_tags=["bhava_lords", "lord_placement"],
    entity_target="native",
    prediction_type="trait",
)

# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 49-60: 5TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.202-208
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 49: 5th lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 1}],
    signal_group="h5_lord_in_h1_scholarly_mixed",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "scholarly_progenic_happiness_but_miser_crooked_steal_others_wealth",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.49",
    description="5th lord in ascendant: scholarly, progenic happiness, but a miser, crooked, will steal others' wealth.",
    commentary_context="Santhanam: The native having the 5th lord in the ascendant will be of unsteady disposition. Though progenic happiness is denoted by our text, there are other exponents warning of an unpleasant situation in respect of one of the native's sons.",
    concordance_texts=["Saravali"],
)

# ── Sloka 50: 5th lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 2}],
    signal_group="h5_lord_in_h2_many_sons_fame",
    direction="favorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "many_sons_wealth_pater_familias_honourable_famous_worldwide",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.50",
    description="5th lord in 2nd: many sons and wealth, be a pater familias, honourable, attached to spouse, famous in the world.",
    commentary_context="Santhanam: Maharshi Parasara praises very highly the placement of the 5th lord in the 2nd house and attributes worldwide fame for the native. It is actually true in the case of Smt. Indira Gandhi, Prime Minister of India, whose map of birth is furnished (born 19 November 1917, 2317 hrs IST at Allahabad). Note the lord of the 5th Mars occupying the 2nd house in Leo.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 51: 5th lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 3}],
    signal_group="h5_lord_in_h3_talebearer_miser",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "attached_coborn_talebearer_miser_interested_own_work",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.51",
    description="5th lord in 3rd: attached to co-born, be a talebearer and a miser, always interested in own work.",
    commentary_context="Santhanam: The native will further be an imposter. He will not be helpful to anybody in any manner.",
)

# ── Sloka 52: 5th lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 4}],
    signal_group="h5_lord_in_h4_maternal_happiness_wealth",
    direction="favorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "happy_maternal_happiness_wealth_intelligence_king_minister",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.52",
    description="5th lord in 4th: happy, endowed with maternal happiness, wealth and intelligence, be a king or a minister or a preceptor.",
    commentary_context="Santhanam: A very long life will come to the native's mother. The native will start acquiring prosperity, right from his youth. He will also own a posh or beautiful house. These effects that will come to pass with the 4th house having the 5th lord in it.",
    concordance_texts=["Saravali"],
)

# ── Sloka 53: 5th lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 5}],
    signal_group="h5_lord_in_h5_happy_sons_benefic",
    direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "happy_sons_virtuous_dear_to_friends_if_benefic_related",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.53",
    description="5th lord in 5th: happy, have sons, be virtuous, dear to friends — if related to benefic. If malefic related, no issues.",
    commentary_context="Santhanam: If the 5th lord is related to the said 5th lord placed in 5th, the 5th lord in 5th will, however, make one virtuous and dear to friends. The contrary condition (malefic) denies progeny.",
    modifiers=[{"condition": "related_to_benefic", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
    concordance_texts=["Saravali"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS2458"]},
)

# Malefic contrary
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 5}],
    signal_group="h5_lord_in_h5_malefic_no_issues",
    direction="unfavorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "no_issues_if_related_to_malefic",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.53",
    description="5th lord in 5th related to malefic: no issues (progeny denied).",
    commentary_context="Santhanam: The contrary condition — if malefic is related to the 5th lord placed in 5th, there will be no issues. This is the explicit contrary stated in the verse.",
    modifiers=[{"condition": "related_to_malefic", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2457"]},
)

# ── Sloka 54: 5th lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 6}],
    signal_group="h5_lord_in_h6_sons_inimical",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    entity_target="children",
    predictions=[
        {"entity": "children", "claim": "sons_inimical_or_lost_acquire_adopted_purchased_son",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.54",
    description="5th lord in 6th: sons inimical to native, or will lose them, or acquire adopted/purchased son.",
    commentary_context="Santhanam: Maharshi Parasara enunciates four different possibilities if the 5th lord is in the 6th: (1) sons inimical to native, (2) loss of children (6th is maraka for 5th), (3) obtaining adopted issue, (4) purchase of a child. It is also not advisable for a female to have her 9th lord from the 10th house from the point of view of filial happiness.",
    modifiers=[{"condition": "four_possibilities_inimical_sons_or_loss_or_adopted_or_purchased", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
)

# ── Sloka 55: 5th lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 7}],
    signal_group="h5_lord_in_h7_honourable_religious",
    direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "honourable_very_religious_progenic_happiness_helpful",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.55",
    description="5th lord in 7th: honourable, very religious, endowed with progenic happiness, helpful to others.",
    commentary_context="Santhanam: With the 5th lord going to the 7th house, the native will be tall in stature and will speak only truth. He will honestly serve his employer, and his dealings will be honest. He will be firm in disposition.",
    concordance_texts=["Saravali"],
)

# ── Sloka 56: 5th lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 8}],
    signal_group="h5_lord_in_h8_no_progeny_pulmonary",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "not_much_progenic_happiness_cough_pulmonary_anger_devoid_happiness",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.56",
    description="5th lord in 8th: not have much progenic happiness, troubled by cough and pulmonary disorders, given to anger, devoid of happiness.",
    commentary_context="Santhanam: No separate note. The 5th lord in the 8th (4th from 5th = comfort of children denied, plus 8th house association brings health troubles).",
)

# ── Sloka 57: 5th lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 9}],
    signal_group="h5_lord_in_h9_prince_author",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "prince_or_equal_author_treatises_famous_shine_in_race",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.57",
    description="5th lord in 9th: be a prince or equal to him, author treatises, be famous and shine in his race.",
    commentary_context="Santhanam: The placement of the 5th lord in the 9th house is a good augury for writership, authorship, editorship and the like. See the horoscope of the most venerable Jagadguru Adi Sankaracharya. Please note that the 5th lord is in the 9th in a house of Jupiter. Mars is a favourable planet for Cancer ascendant.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 58: 5th lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 10}],
    signal_group="h5_lord_in_h10_rajayoga_famous",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "rajayoga_various_pleasures_very_famous",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.24 v.58",
    description="5th lord in 10th: enjoy a Rajayoga and various pleasures, be very famous.",
    commentary_context="Santhanam: For enjoying a superior degree of material benefits like wealth, position, fame etc. the 5th lord is the best placed in the 10th house than elsewhere. This one position with sterling qualities will equal many Rajayogas. It is a prerequisite of course that in such a placement the 5th lord is preferably with exaltation or such other dignities. If he is placed in an enemy's house or such other afflictions tormenting him, he will prove rather adverse than a Rajayoga maker.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "if_in_enemy_house_or_afflicted_proves_adverse_not_rajayoga", "effect": "negates", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 59: 5th lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 11}],
    signal_group="h5_lord_in_h11_learned_many_sons",
    direction="favorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "learned_dear_to_people_author_treatises_many_sons_wealth",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.59",
    description="5th lord in 11th: learned, dear to people, author of treatises, skilful, many sons and wealth.",
    commentary_context="Santhanam: The 5th lord's station in the 11th house will keep one free from misfortunes and unhappiness. His academic achievements will be abundant. He will be happy in respect of his children, but the said 11th house should be a friendly sign for the 5th lord. If the 5th lord is inimically placed in the 11th, for example the Sun in Aquarius in the 11th in the case of Aries ascendant, the progeny will be inimical to the native.",
    modifiers=[{"condition": "5th_lord_inimically_placed_in_11th_progeny_inimical_eg_sun_in_aquarius_aries", "effect": "negates", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 60: 5th lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 5, "house": 12}],
    signal_group="h5_lord_in_h12_bereft_sons",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "bereft_happiness_own_sons_adopted_son_loss_of_children",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.60",
    description="5th lord in 12th: bereft of happiness from own sons, will have an adopted or purchased son.",
    commentary_context="Santhanam: The placement of the 5th lord in the 12th terminal house will cause various kinds of miseries in the matter of children. One may not obtain a child at all, or may incur inimical relations with his own child. Adoption will surely come to pass if Saturn or Mercury ruling the 5th is in the 12th. Further grave defects with the 5th in the 12th are difficulties in digestion and abdominal disorders.",
    modifiers=[{"condition": "adoption_certain_if_saturn_or_mercury_rules_5th_in_12th_also_digestive_defects", "effect": "qualifies", "target": "prediction", "strength": "strong", "scope": "local"}],
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 61-72: 6TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.208-211
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 61: 6th lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 1}],
    signal_group="h6_lord_in_h1_sickly_famous",
    direction="mixed", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "sickly_famous_inimical_to_own_men_rich_honourable_adventurous",
         "domain": "health", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.61",
    description="6th lord in ascendant: sickly, famous, inimical to own men, rich, honourable, adventurous, virtuous.",
    commentary_context="Santhanam: The 6th lord in the ascending sign will bring various diseases to the native. He will incur adverse effects in the matter of acquisition of progeny. Venus in Taurus ascendant will particularly give benefic results in full measure as stated. There will, however, be more daughters than sons, while the first child will be a male.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "venus_in_taurus_ascendant_gives_full_benefic_results_more_daughters_first_male", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 62: 6th lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 2}],
    signal_group="h6_lord_in_h2_adventurous_foreign",
    direction="favorable", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "adventurous_famous_live_alien_countries_skilful_speaker",
         "domain": "career", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.62",
    description="6th lord in 2nd: adventurous, famous among racemen, live in alien countries (or places), skilful speaker, interested in own work.",
    commentary_context="Santhanam: The native will further be skilful in dealing with hoary lore. His financial position will be somewhat shaky. He will enjoy good health.",
)

# ── Sloka 63: 6th lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 3}],
    signal_group="h6_lord_in_h3_anger_no_courage",
    direction="unfavorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "anger_bereft_courage_inimical_all_coborn_disobedient_servants",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.63",
    description="6th lord in 3rd: given to anger, bereft of courage, inimical to all co-born, disobedient servants.",
    commentary_context="Santhanam: The 3rd house containing the 6th lord will not serve the native with intelligence at all times. To wit, he will be partly deprived of benefits due to his intelligence. He will also not be steady in disposition.",
)

# ── Sloka 64: 6th lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 4}],
    signal_group="h6_lord_in_h4_no_maternal_happiness",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_maternal_happiness_intelligent_talebearer_jealous_very_rich",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.64",
    description="6th lord in 4th: devoid of maternal happiness, intelligent, talebearer, jealous, fickle-minded, very rich.",
    commentary_context="Santhanam: No separate note. Mixed result — wealth is indicated but maternal happiness and stability of mind are denied.",
)

# ── Sloka 65: 6th lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 5}],
    signal_group="h6_lord_in_h5_fluctuating_finances",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "fluctuating_finances_enmity_with_sons_happy_selfish_kind",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.65",
    description="6th lord in 5th: fluctuating finances, enmity with sons and friends, but happy, selfish and kind.",
    commentary_context="Santhanam: No separate note. The 6th lord (enemies/disease) in the 5th (children/intelligence) creates tension in filial and financial domains.",
)

# ── Sloka 66: 6th lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 6}],
    signal_group="h6_lord_in_h6_enmity_kinsmen",
    direction="mixed", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "enmity_with_kinsmen_friendly_to_others_mediocre_wealth",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
        {"entity": "native", "claim": "free_from_diseases_long_life_conveyances",
         "domain": "health", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.66",
    description="6th lord in 6th: enmity with kinsmen, friendly to others, mediocre wealth. Notes: free from diseases, happiness of conveyances, long life.",
    commentary_context="Santhanam: The native will enjoy happiness of conveyances and be free from diseases. His life span will also be considerably lengthy. These are additional effects for the 6th lord in the 6th itself.",
    concordance_texts=["Saravali"],
)

# ── Sloka 67: 6th lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 7}],
    signal_group="h6_lord_in_h7_no_marital_happiness",
    direction="mixed", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "deprived_happiness_wedlock_famous_virtuous_adventurous_wealthy",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.67",
    description="6th lord in 7th: deprived of happiness through wedlock, but famous, virtuous, honourable, adventurous, wealthy.",
    commentary_context="Santhanam: Apart from denying marital happiness, the 6th lord's occupancy of the 7th house will dissatisfy the native in the matter of progeny. His own spouse will be his sworn enemy.",
    concordance_texts=["Saravali"],
)

# ── Sloka 68: 6th lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 8}],
    signal_group="h6_lord_in_h8_sickly_inimical",
    direction="unfavorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "sickly_inimical_desire_others_wealth_interested_others_wives_impure",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.68",
    description="6th lord in 8th: sickly, inimical, desire others' wealth, interested in others' wives, impure (or degraded).",
    commentary_context="Santhanam: It is not good for one's purity of character if the 8th house is occupied by the 6th lord. The native will be ever incurring enmity with others and be not happy. He will have a green eye on others' learning and an eye on others' wealth.",
    modifiers=[{"condition": "6th_lord_in_8th_ever_incurring_enmity_eye_on_others_learning_wealth", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 69: 6th lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 9}],
    signal_group="h6_lord_in_h9_trade_wood_stones",
    direction="mixed", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "trade_in_wood_stones_or_poison_fluctuating_professional_fortunes",
         "domain": "career", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.69",
    description="6th lord in 9th: trade in wood and stones (or poison), fluctuating professional fortunes.",
    commentary_context="Santhanam: The Maharishi seems to suggest that one will deal in building construction material by saying one will sell wood and stones with the 6th lord in the 9th. It will further cause ups and downs in one's livelihood.",
)

# ── Sloka 70: 6th lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 10}],
    signal_group="h6_lord_in_h10_well_known_foreign",
    direction="mixed", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "well_known_not_disposed_to_father_happy_foreign_countries_gifted_speaker",
         "domain": "career", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.70",
    description="6th lord in 10th: well-known among his men, not respectfully disposed to father, happy in foreign countries, gifted speaker.",
    commentary_context="Santhanam: One will be greatly valorous and learned in Sastras (or ancient lore). There will be litigations on account of one's ancestral properties. Dutifulness and living in foreign place will also come to pass. These are in furtherance to the sage's views for the placement of the 6th lord in the 10th house.",
    concordance_texts=["Saravali"],
)

# ── Sloka 71: 6th lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 11}],
    signal_group="h6_lord_in_h11_gain_through_enemies",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_wealth_through_enemies_virtuous_bereft_progenic_happiness",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.71",
    description="6th lord in 11th: gain wealth through enemies, be virtuous, adventurous, but bereft of progenic happiness.",
    commentary_context="Santhanam: One will, to some extent, be happy and to yet some extent be unhappy if the 6th lord occupies the 11th house. This is in regard to progeny. There is also a view that this position can wholly deny acquisition of a child.",
    modifiers=[{"condition": "position_can_wholly_deny_acquisition_of_child", "effect": "negates", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 72: 6th lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 6, "house": 12}],
    signal_group="h6_lord_in_h12_spend_vices",
    direction="unfavorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "spend_on_vices_hostile_learned_people_torture_living_beings",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.72",
    description="6th lord in 12th: always spend on vices, be hostile to learned people, will torture living beings.",
    commentary_context="Santhanam: The native will be of questionable morality and will ever be intent on deriving sexual pleasures from other females as well.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 73-84: 7TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.212-216
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 73: 7th lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 1}],
    signal_group="h7_lord_in_h1_others_wives_wicked",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "go_to_others_wives_wicked_skilful_devoid_courage_windy_diseases",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.73",
    description="7th lord in ascendant: go to others' wives, be wicked, skilful, devoid of courage, afflicted by windy diseases.",
    commentary_context="Santhanam: The native will not be firm in his words and will impart courage in others although he himself will be bereft of courage. So say learned astrologers in the context of the ascendant being occupied by the 7th lord.",
    concordance_texts=["Saravali"],
)

# ── Sloka 74: 7th lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 2}],
    signal_group="h7_lord_in_h2_many_wives_wealth",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "many_wives_wealth_through_wife_procrastinating",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.74",
    description="7th lord in 2nd: have many wives, gain wealth through wife, but be procrastinating in nature.",
    commentary_context="Santhanam: This position will further give corrupt character making one addicted to many women. He will lose his wife early in his marriage. His prosperity will ascend with his marriage.",
    concordance_texts=["Saravali"],
)

# ── Sloka 75: 7th lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 3}],
    signal_group="h7_lord_in_h3_loss_children",
    direction="unfavorable", intensity="moderate",
    primary_domain="progeny",
    entity_target="children",
    predictions=[
        {"entity": "children", "claim": "loss_of_children_difficulty_living_son_possibility_of_daughter",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.75",
    description="7th lord in 3rd: face loss of children, with great difficulty a living son, possibility of birth of a daughter.",
    commentary_context="Santhanam: Three salient features in regard to progeny are denoted by sage Parasara for the 3rd house placement of the 7th lord. Firstly, loss of children in general. Secondly, possibility of (rarely) acquiring a daughter. Lastly, no possibility of having a living son. In fine, probably a female child will live long to keep the native happy, while male children will pass away as they are born.",
)

# ── Sloka 76: 7th lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 4}],
    signal_group="h7_lord_in_h4_wife_not_under_control",
    direction="mixed", intensity="moderate",
    primary_domain="relationships",
    entity_target="spouse",
    predictions=[
        {"entity": "spouse", "claim": "wife_not_under_control_fond_of_truth_intelligent_religious_dental",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.76",
    description="7th lord in 4th: wife not under his control, fond of truth, intelligent, religious, suffer dental diseases.",
    commentary_context="Santhanam: A disobedient wife follows the 4th house position of the 7th lord. This is Maharshi's instruction. However, Ramadayalu states in this context that the native's wife will brilliantly shine with chastity and devotion to husband. The Chaukambha edition also clearly states that the native's wife will not be chaste.",
    concordance_texts=["Saravali"],
    divergence_notes="Ramadayalu contradicts — says wife will shine with chastity",
    modifiers=[{"condition": "ramadayalu_contradicts_says_wife_shines_with_chastity_devotion", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 77: 7th lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 5}],
    signal_group="h7_lord_in_h5_honourable_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "honourable_seven_principal_virtues_delighted_all_kinds_wealth",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.77",
    description="7th lord in 5th: honourable, endowed with all seven principal virtues, always delighted, all kinds of wealth.",
    commentary_context="Santhanam: I have observed two salient features in the 7th lord's getting into the 5th house: (1) Delay and disappointments in married life. The conjugal life seldom proves happy. (2) Severe affliction to progenic indications. Either there will be unhappiness on account of children or loss of children.",
    concordance_texts=["Saravali"],
)

# ── Sloka 78: 7th lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 6}],
    signal_group="h7_lord_in_h6_sickly_wife",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "beget_sickly_wife_inimical_to_her_anger_devoid_happiness",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.78",
    description="7th lord in 6th: beget a sickly wife, be inimical to her, given to anger, devoid of happiness.",
    commentary_context="Santhanam: The 7th lord in the 6th will reduce the general happiness of the native apart from severely inflicting his conjugal bliss. His own health will be poor while his wife will equally have adverse health conditions. The native will coalesce with harlots.",
)

# ── Sloka 79: 7th lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 7}],
    signal_group="h7_lord_in_h7_happy_wife_courageous",
    direction="favorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "happiness_through_wife_courageous_skilful_intelligent",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.79",
    description="7th lord in 7th: endowed with happiness through wife, courageous, skilful, intelligent, only afflicted by windy diseases.",
    commentary_context="Santhanam: By using the word 'only' in the text, the sage hints that the only possible defect in the 7th lord's placement in the 7th itself will be troubles from windy diseases (like rheumatism, arthritis etc.). One undesirable quality will, however, be found in the native: his addiction to other females. This is an exception to Venus occupying the 7th house identical with Taurus or Libra.",
    concordance_texts=["Saravali", "Phaladeepika"],
    exceptions=["venus_in_taurus_or_libra_7th_addiction_to_other_females"],
)

# ── Sloka 80: 7th lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 8}],
    signal_group="h7_lord_in_h8_deprived_marital",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "deprived_marital_happiness_wife_diseased_devoid_good_disposition",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.80",
    description="7th lord in 8th: deprived of marital happiness, wife troubled by diseases, devoid of good disposition, will not obey.",
    commentary_context="Santhanam: As the 7th lord goes to the 8th house, the native's spouse will be liable to incur afflictions on her longevity. However, marriage may bring some pecuniary gains for the native.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "marriage_may_bring_pecuniary_gains_despite_marital_unhappiness", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 81: 7th lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 9}],
    signal_group="h7_lord_in_h9_many_women_well_disposed",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "union_many_women_well_disposed_own_wife_many_undertakings",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.81",
    description="7th lord in 9th: union with many women, but well-disposed to own wife, have many undertakings (or assignments).",
    commentary_context="Santhanam: No separate note. Favourable for marriage despite multiple relationships.",
)

# ── Sloka 82: 7th lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 10}],
    signal_group="h7_lord_in_h10_disobedient_wife_religious",
    direction="mixed", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "disobedient_wife_religious_wealthy_endowed_with_sons",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.82",
    description="7th lord in 10th: beget a disobedient wife, be religious, endowed with wealth and sons.",
    commentary_context="Santhanam: No separate note. Mixed result — wealth and religious inclination alongside problematic marriage.",
)

# ── Sloka 83: 7th lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 11}],
    signal_group="h7_lord_in_h11_gain_through_wife",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_wealth_through_wife_less_happiness_from_sons_have_daughters",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.83",
    description="7th lord in 11th: gain wealth through wife, less happiness from sons, have daughters.",
    commentary_context="Santhanam: If the 7th lord is in the 11th house, there is a possibility of the native losing his children to his grief. He will obtain (more) daughters. His own sons will be hostile to him and will cause him no happiness. Living son also seems to be a very remote probability.",
    modifiers=[{"condition": "possibility_losing_children_hostile_sons_daughters_obtained_sons_not_longlived", "effect": "negates", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 84: 7th lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 12}],
    signal_group="h7_lord_in_h12_penury_miser",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "penury_miser_livelihood_related_to_clothes",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.84",
    description="7th lord in 12th: incur penury, be a miser, livelihood related to clothes.",
    commentary_context="Santhanam: No separate note. The 7th lord in the house of loss creates financial difficulties.",
)
# v.84 split: wife spendthrift
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 7, "house": 12}],
    signal_group="h7_lord_in_h12_wife_spendthrift",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    entity_target="spouse",
    predictions=[
        {"entity": "spouse", "claim": "wife_will_be_a_spendthrift",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.84",
    description="7th lord in 12th: wife will be a spendthrift.",
    commentary_context="Santhanam: Split from native penury prediction — same verse, distinct entity per granularity principle #2. Spending-prone spouse.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 85-96: 8TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.216-220
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 85: 8th lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 1}],
    signal_group="h8_lord_in_h1_devoid_felicity_wounds",
    direction="unfavorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "devoid_physical_felicity_suffer_wounds_hostile_to_gods_brahmins",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.85",
    description="8th lord in ascendant: devoid of physical felicity, suffer from wounds, hostile to gods and brahmins (or religious people).",
    commentary_context="Santhanam: No separate note. The 8th lord (misfortune/death) in the 1st (body/self) brings physical afflictions and wounds.",
)

# ── Sloka 86: 8th lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 2}],
    signal_group="h8_lord_in_h2_devoid_vigour",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_bodily_vigour_little_wealth_not_regain_lost_wealth",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.86",
    description="8th lord in 2nd: devoid of bodily vigour, enjoy a little wealth, not regain lost wealth.",
    commentary_context="Santhanam: No separate note. The 8th lord in the 2nd (wealth house) impedes financial recovery.",
)

# ── Sloka 87: 8th lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 3}],
    signal_group="h8_lord_in_h3_no_fraternal_happiness",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "devoid_fraternal_happiness_indolent_devoid_servants_strength",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.87",
    description="8th lord in 3rd: devoid of fraternal happiness, indolent, devoid of servants and strength.",
    commentary_context="Santhanam: No separate note. The 8th lord in the 3rd house denies co-born happiness and courage.",
)

# ── Sloka 88: 8th lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 4}],
    signal_group="h8_lord_in_h4_lose_mother_early",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    entity_target="mother",
    predictions=[
        {"entity": "mother", "claim": "deprived_of_mother_early_devoid_house_lands_happiness_betray_friends",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
        {"entity": "mother", "claim": "mother_lost_in_early_childhood",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.88",
    description="8th lord in 4th: deprived of mother (shishu — lose mother in childhood), devoid of house, lands and happiness, betray friends.",
    commentary_context="Santhanam: Maharshi Parasara uses the word 'shishu' meaning child. Hence it is apparent that the native will lose his mother in the very childhood if the 8th lord is in the 4th house.",
    modifiers=[{"condition": "parasara_uses_shishu_indicating_mother_lost_in_very_childhood", "effect": "qualifies", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 89: 8th lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 5}],
    signal_group="h8_lord_in_h5_dull_witted_longlived",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "dull_witted_limited_children_longlived_wealthy",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.89",
    description="8th lord in 5th: dull-witted, limited number of children, longlived, wealthy.",
    commentary_context="Santhanam: One's financial acquisitions, though abundant, will not be steady and be subjected to fluctuations. Though his intentions and actions will be bona fide, they will go unrecognised. He will not be steady in disposition and will off and on change his line of thinking. He will not enjoy filial bliss. These are additional hints for the 8th lord's stationing in the 5th house at birth.",
)

# ── Sloka 90: 8th lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 6}],
    signal_group="h8_lord_in_h6_win_enemies_childhood_danger",
    direction="mixed", intensity="moderate",
    primary_domain="longevity",
    predictions=[
        {"entity": "native", "claim": "win_over_enemies_diseases_childhood_danger_snakes_water_long_life",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
        {"entity": "native", "claim": "long_span_of_life_indicated",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.90",
    description="8th lord in 6th: win over enemies, afflicted by diseases in childhood, danger through snakes/water, but indicates long life.",
    commentary_context="Santhanam: The position of the 8th lord in the 6th house is a sureshot of success over enemies and in litigations. The native will be reduced to danger through snakes, scorpions etc. during childhood. Afterwards he will be free from such calamities. However, this position is not very favourable for one's health. This also indicates a long span of life.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "not_favourable_for_health_but_indicates_long_span_of_life", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 91: 8th lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 7}],
    signal_group="h8_lord_in_h7_two_wives_downfall",
    direction="mixed", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "two_wives_downfall_business_if_malefic_conjunct",
         "domain": "relationships", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.91",
    description="8th lord in 7th: two wives; if conjunct malefic, downfall in business (or livelihood).",
    commentary_context="Santhanam: The 7th house being occupied by the 8th lord is a forerunner of difficulties in married life. There will be want of understanding between the native and his spouse. The constitution of the spouse will be quite weak and she will always be subjected to uncertainties or dangers. Outwardly the native may pose to be God-fearing, but he will not be sincerely devoted to the Almighty. He will be an expert in stealing others' things.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "malefic_conjunct", "effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 92: 8th lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 8}],
    signal_group="h8_lord_in_h8_longlived",
    direction="favorable", intensity="strong",
    primary_domain="longevity",
    predictions=[
        {"entity": "native", "claim": "longlived_if_strong_medium_longevity_if_weak",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.92",
    description="8th lord in 8th: longlived. If the said planet is weak, medium longevity; will be a thief, blameworthy, blame others.",
    commentary_context="Santhanam: In remaining in the 8th itself, the 8th lord should be quite strong in Shadbala, so the native will enjoy full span of life. If he is bereft of strength, the native will not enjoy full span of life. The 8th house in occupation by its own lord will give a spouse with questionable character. However she will be a source of financial help to the native by her own earnings or inheritance.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "8th_lord_weak_in_shadbala_reduces_to_medium_longevity", "effect": "attenuates", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 93: 8th lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 9}],
    signal_group="h8_lord_in_h9_betray_religion",
    direction="unfavorable", intensity="strong",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "betray_religion_heterodox_wicked_wife_steal_others_wealth",
         "domain": "spirituality", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.93",
    description="8th lord in 9th: betray religion, be heterodox, beget a wicked wife, steal others' wealth.",
    commentary_context="Santhanam: The native will suffer frequent misfortunes and downfalls. His prosperity will not be unobstructed and he will find it difficult to cope up with professional adversities. His father will suffer a cut in longevity. His understanding with his father will be deficient. His wife will be of 'questionable birth'. In the case of a Gemini native, Saturn occupying the 9th house (his Moolatrikona) will not produce these malefic effects. But his benefic tendencies will be quite meagre.",
    exceptions=["gemini_ascendant_saturn_in_9th_moolatrikona"],
)

# ── Sloka 94: 8th lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 10}],
    signal_group="h8_lord_in_h10_devoid_paternal",
    direction="unfavorable", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "devoid_paternal_bliss_talebearer_bereft_livelihood",
         "domain": "career", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.94",
    description="8th lord in 10th: devoid of paternal bliss, be a talebearer, bereft of livelihood. If benefic aspect, evils will not mature.",
    commentary_context="Santhanam: There is a school of thought to say that the 8th lord occupying the 9th house will cause the deaths of parents right in the native's boyhood. Apparently one will not enjoy parental happiness for a long duration. This placement of the 8th lord in the 10th will produce all kinds of miseries in livelihood, fortunes, fame, properties and the like. According to Maharshi Parasara, if the 8th lord in the 10th is (well) related to a benefic, no evils will come to pass.",
    modifiers=[{"condition": "benefic_aspect_on_8th_lord_in_10th_prevents_evils_from_maturing", "effect": "negates", "target": "prediction", "strength": "strong", "scope": "local"}],
)

# ── Sloka 95: 8th lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 11}],
    signal_group="h8_lord_in_h11_devoid_wealth_longlived",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_wealth_with_malefic_miserable_boyhood_happy_later_longlived",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.95",
    description="8th lord in 11th with malefic: devoid of wealth, miserable in boyhood but happy later, longlived.",
    commentary_context="Santhanam: The 11th house will, unless related to a malefic, particularly by conjunction, will not deprive the native of financial benefits. If he is alone in the 11th, he will not prove that bad in this respect. Moreover, for Taurus ascendant, Jupiter in the 11th is not baneful. And for Scorpio ascendant, Mercury in the 11th will prove a highly favourable bargain in the matter of wealth, fame, knowledge etc.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "8th_lord_conjunct_malefic_in_11th_deprivation_of_wealth_amplified", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 96: 8th lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 8, "house": 12}],
    signal_group="h8_lord_in_h12_evil_deeds_short_life",
    direction="unfavorable", intensity="strong",
    primary_domain="longevity",
    predictions=[
        {"entity": "native", "claim": "spend_on_evil_deeds_short_life_more_so_if_malefic",
         "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.96",
    description="8th lord in 12th: spend on evil deeds, incur a short life. If additionally with malefic, more so.",
    commentary_context="Santhanam: No separate note. The double 12th (loss) from the 8th (longevity) creates the worst conditions for lifespan and moral conduct.",
    modifiers=[{"condition": "additionally_with_malefic", "effect": "amplifies", "target": "prediction", "strength": "strong", "scope": "local"}],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH24B_REGISTRY = b.build()
