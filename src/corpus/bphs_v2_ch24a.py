"""src/corpus/bphs_v2_ch24a.py — BPHS Ch.24 Part A: Lords 1-4 in 12 Houses.

S309: BPHS Phase 1B Block B — Effects of the Bhava Lords (Bhava Adhipati Phala).
Ch.24 is the largest chapter in BPHS (148 slokas, pp.189-236).
This file covers slokas 1-48: 1st through 4th lord in all 12 houses.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.189-201.
Verse audit: data/verse_audits/ch24_audit.json (233 claims, 148 slokas).

Structure: 12 lords x 12 houses = 144 systematic placements + 4 misc.
Part A = lords 1-4 (48 slokas, ~55-65 rules with Santhanam note expansions).

Modifier protocol (Option B — locked in S306):
  primary_condition = lord_in_house atomic placement
  modifiers = verse-stated conditions that CHANGE the outcome
  Zero redundancy. Dignity/aspect modifiers split into separate rules.

Confidence formula (Phase 1B mechanical):
  base = 0.60 + 0.05 (verse_ref) = 0.65 minimum
  + 0.08 per concordance text
  - 0.05 per divergence text
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.24", category="bhava_lord_effects",
    id_start=2400, session="S313", sloka_count=48,
    chapter_tags=["bhava_lords", "lord_placement"],
    entity_target="native",
    prediction_type="trait",
)

# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 1-12: 1ST LORD (LAGNA LORD) IN HOUSES 1-12
# Santhanam Vol 1, pp.189-192
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 1: 1st lord in 1st house ─────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 1}],
    signal_group="h1_lord_in_h1_physical_felicity",
    direction="favorable", intensity="strong",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "strong_constitution_healthy_body_confident_disposition",
         "domain": "health", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.1",
    description="Lagna lord in 1st house: native has physical felicity, strong constitution, healthy body, confident and self-reliant nature.",
    commentary_context="Santhanam: With ascendant lord in 1st, native is of noble descent, ambitious, beautiful, prosper by own efforts. Prosperity comes easily. Ever enjoy physical felicity.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 2: 1st lord in 2nd house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 2}],
    signal_group="h1_lord_in_h2_wealth_speech",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_good_speech_learned_early_accumulation",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.2",
    description="Lagna lord in 2nd house: wealthy family background, good speech, financial support from family, early accumulation of wealth, eloquence and learning.",
    commentary_context="Santhanam: No separate note beyond the verse translation. Wealth and learning are the primary indications.",
    concordance_texts=["Saravali"],
)

# ── Sloka 3: 1st lord in 3rd house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 3}],
    signal_group="h1_lord_in_h3_brave_intelligent",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "brave_valorous_intelligent_happy_no_siblings_lost",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.3",
    description="Lagna lord in 3rd house: brave, no younger siblings lost, intelligent, happy. Equal to a king, respected by others.",
    commentary_context="Santhanam: Should the 3rd house contain the ascendant lord, one will be equal to a king, respected by others and will indulge in unnatural methods of sexual gratification.",
    concordance_texts=["Saravali"],
)

# ── Sloka 4: 1st lord in 4th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 4}],
    signal_group="h1_lord_in_h4_maternal_happiness",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "paternal_maternal_happiness_many_brothers_virtuous_charming",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.4",
    description="Lagna lord in 4th house: endowed with paternal and maternal happiness, many brothers, lustful virtuous and charming.",
    commentary_context="Santhanam: With ascendant lord in 4th, native is of noble descent. Will prosper by own efforts. He will be ambitious and beautiful. Prosperity will come to him easily. He will ever enjoy physical felicity.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 5: 1st lord in 5th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 5}],
    signal_group="h1_lord_in_h5_mediocre_progeny",
    direction="mixed", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "mediocre_progenic_happiness_lose_first_child_honourable",
         "domain": "progeny", "direction": "mixed", "magnitude": 0.5},
        {"entity": "native", "claim": "honourable_given_to_anger_dear_to_king",
         "domain": "career", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.5",
    description="Lagna lord in 5th house: mediocre progenic happiness, will lose first child, honourable, given to anger, dear to king.",
    commentary_context="Santhanam: No separate note beyond verse translation. The 5th house placement creates mixed results — honour and social status are indicated, but progeny matters suffer.",
)

# ── Sloka 6: 1st lord in 6th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 6}],
    signal_group="h1_lord_in_h6_devoid_physical_happiness",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "devoid_of_physical_happiness_troubled_by_enemies",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.6",
    description="Lagna lord in 6th and related to a malefic: devoid of physical happiness, troubled by enemies if no benefic aspect.",
    commentary_context="Santhanam: The ascendant lord going to 6th mars health prospects. However, for Scorpio and Taurus ascendant, it will be a felicitous augury for freedom from diseases. The 6th house position of Lagna Lord in general will give abundant wealth and respect apart from royal status. There is, however, a possibility of more than one marriage or losing the spouse early.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# Exception: Scorpio/Taurus ascendant
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 6}],
    signal_group="h1_lord_in_h6_scorpio_taurus_exception",
    direction="favorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "felicitous_augury_freedom_from_diseases_scorpio_taurus",
         "domain": "health", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.6",
    description="Exception: For Scorpio and Taurus ascendant, lagna lord in 6th is felicitous for freedom from diseases.",
    commentary_context="Santhanam: However, for Scorpio and Taurus ascendant, it will be a felicitous augury for freedom from diseases. This is a lagna-specific exception to the general unfavorable reading.",
    lagna_scope=["scorpio", "taurus"],
    rule_relationship={"type": "override", "related_rules": ["BPHS2405"]},
)

# ── Sloka 7: 1st lord in 7th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 7}],
    signal_group="h1_lord_in_h7_wife_short_life",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    entity_target="spouse",
    predictions=[
        {"entity": "spouse", "claim": "wife_will_not_live_long_if_malefic",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.7",
    description="Lagna lord in 7th as malefic: wife will not live long.",
    commentary_context="Santhanam: If the ascendant lord is a malefic and be in the 7th, the native's wife will not live long. If the planet in question be a benefic, one will wander aimlessly, face penury and be dejected. He will alternatively become a king (if the said planet is strong).",
    modifiers=[{"condition": "planet_is_malefic", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
    concordance_texts=["Saravali"],
)

# Benefic variant
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 7}],
    signal_group="h1_lord_in_h7_benefic_wander",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wander_aimlessly_penury_dejected_if_benefic",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.7",
    description="Lagna lord in 7th as benefic: wander aimlessly, face penury and be dejected.",
    commentary_context="Santhanam: If the planet in question be a benefic, one will wander aimlessly, face penury and be dejected. He will alternatively become a king (if the said planet is strong). The strong-planet exception overrides.",
    modifiers=[{"condition": "planet_is_benefic", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS2407"]},
)

# Strong planet exception
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 7},
                {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "strong"}],
    signal_group="h1_lord_in_h7_strong_king",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "alternatively_become_king_if_planet_strong",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.7",
    description="Lagna lord in 7th and strong: will alternatively become a king.",
    commentary_context="Santhanam: He will alternatively become a king (if the said planet is strong). Strength overrides the general unfavorable reading.",
    rule_relationship={"type": "override", "related_rules": ["BPHS2407", "BPHS2408"]},
)

# ── Sloka 8: 1st lord in 8th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 8}],
    signal_group="h1_lord_in_h8_scholar_sickly",
    direction="mixed", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "accomplished_scholar_but_sickly_thievish_gambler",
         "domain": "character", "direction": "favorable", "magnitude": 0.5},
        {"entity": "native", "claim": "sickly_gambler_thievish_anger_others_wives",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.8",
    description="Lagna lord in 8th: accomplished scholar, but sickly, thievish, gambler, given to anger, join others' wives.",
    commentary_context="Santhanam: The only good effect of the ascendant lord being in the 8th house is one's academic accomplishment. This position will cause Balarishta or child mortality. The native's health will be poor. He will be a repository of misfortunes. He will see many deaths in the family to his grief. In case of Aries and Libra ascendant, this approach for evil results should be avoided and results declared after further scanning the radix.",
    concordance_texts=["Saravali"],
)

# Aries/Libra exception
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 8}],
    signal_group="h1_lord_in_h8_aries_libra_exception",
    direction="mixed", intensity="conditional",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "aries_libra_evil_results_moderated_scan_further",
         "domain": "health", "direction": "mixed", "magnitude": 0.4},
    ],
    verse_ref="Ch.24 v.8",
    description="Exception: For Aries and Libra ascendant, evil results of 1st lord in 8th should be avoided; scan radix further.",
    commentary_context="Santhanam: In case of Aries and Libra ascendant, this approach for evil results should be avoided and results declared after further scanning the radix. Mars (Aries lord) and Venus (Libra lord) are in own houses when in the 8th from these lagnas.",
    lagna_scope=["aries", "libra"],
    rule_relationship={"type": "override", "related_rules": ["BPHS2410"]},
)

# ── Sloka 9: 1st lord in 9th house ────────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 9}],
    signal_group="h1_lord_in_h9_fortunate",
    direction="favorable", intensity="strong",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "fortunate_devotee_vishnu_skilful_eloquent_wife_sons_wealth",
         "domain": "spirituality", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.9",
    description="Lagna lord in 9th: fortunate, dear to people, devotee of Vishnu, skilful, eloquent, endowed with wife, sons and wealth.",
    commentary_context="Santhanam: One will gain abundantly from his father. Every undertaking of his will be fruitful. He will be well-disposed to his co-born. These are additional results of the ascendant lord occupying the 9th house.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 10: 1st lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 10}],
    signal_group="h1_lord_in_h10_fame_wealth",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "paternal_happiness_royal_honour_fame_self_earned_wealth",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.10",
    description="Lagna lord in 10th: paternal happiness, royal honour (or patronage), fame among men, self-earned wealth.",
    commentary_context="Santhanam: The 10th house occupied by the ascendant lord denotes obtainment of co-born. The native will possess ambitions and will prosper in his pursuits.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 11: 1st lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 11}],
    signal_group="h1_lord_in_h11_gains",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "always_endowed_with_gains_good_qualities_fame_many_wives",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.11",
    description="Lagna lord in 11th: always endowed with gains, good qualities, fame, and many wives.",
    commentary_context="Santhanam: No separate note beyond the verse translation. The 11th house is upachaya — lagna lord here directly strengthens gains.",
    concordance_texts=["Saravali"],
)

# ── Sloka 12: 1st lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 12},
               {"type": "planet_not_in_house", "planet": "any_benefic", "house": 12},
               {"type": "planet_not_aspecting", "planet": "any_benefic", "house": 12}],
    signal_group="h1_lord_in_h12_bereft_happiness",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "bereft_physical_happiness_spend_unfruitfully_anger",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.12",
    description="Lagna lord in 12th and devoid of benefic aspect/conjunction: bereft of physical happiness, spend unfruitfully, given to anger.",
    commentary_context="Santhanam: If the ascendant lord is in the 12th, the native's life will not be prosperous. He will be addicted to gambling, debauchery and other vices. He will expend wastefully.",
    concordance_texts=["Saravali"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 13-24: 2ND LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.192-195
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 13: 2nd lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 1}],
    signal_group="h2_lord_in_h1_wealth_inimical_family",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "endowed_sons_wealth_but_inimical_to_family_lustful_hard_hearted",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.13",
    description="2nd lord in ascendant: endowed with sons and wealth, but inimical to family, lustful, hard-hearted, do others' jobs.",
    commentary_context="Santhanam: One will be fraudulent and will face financial upheavals with the lord of the 2nd occupying the ascendant. These evil effects will not wholly apply to Capricorn ascendant, but with some modifications.",
    concordance_texts=["Saravali"],
)

# ── Sloka 14: 2nd lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 2}],
    signal_group="h2_lord_in_h2_wealthy_proud",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_proud_two_or_more_wives_bereft_of_progeny",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
        {"entity": "native", "claim": "bereft_of_progeny_despite_wealth",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.14",
    description="2nd lord in 2nd: wealthy, proud, two or more wives, bereft of progeny.",
    commentary_context="Santhanam: No separate note. Verse is direct — wealth indicated but progeny denied.",
)

# ── Sloka 15: 2nd lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 3}],
    signal_group="h2_lord_in_h3_valorous_benefic",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "valorous_wise_virtuous_lustful_when_related_to_benefic",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.15",
    description="2nd lord in 3rd: valorous, wise, virtuous, lustful — all these when related to a benefic. If related to malefic, heterodox.",
    commentary_context="Santhanam: Should the 2nd lord be in the 3rd house, the native will be ill-related to females and will earn through prostitutes. If a malefic is related to the 2nd lord in the 3rd, the person concerned will not be God-fearing and will have dirty conduct.",
    modifiers=[{"condition": [{"type": "planet_aspecting", "planet": "any_benefic", "house": "self"}], "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
    concordance_texts=["Saravali"],
)

# Malefic variant
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 3}],
    signal_group="h2_lord_in_h3_malefic_heterodox",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "heterodox_dirty_conduct_not_god_fearing_if_malefic",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.15",
    description="2nd lord in 3rd related to malefic: heterodox, not God-fearing, dirty conduct.",
    commentary_context="Santhanam: If a malefic is related to the 2nd lord in the 3rd, the person concerned will not be God-fearing and will have dirty conduct. Contrary condition to the benefic variant.",
    modifiers=[{"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2417"]},
)

# ── Sloka 16: 2nd lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 4}],
    signal_group="h2_lord_in_h4_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "acquire_all_kinds_of_wealth",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.16",
    description="2nd lord in 4th: acquire all kinds of wealth. If exalted and conjunct Jupiter, equal to a king.",
    commentary_context="Santhanam: The placement of the 2nd lord in the 4th will also produce a heterodox and one of questionable character. The exaltation of the 2nd lord in the 4th applies only to Libra ascendant. Obviously the sage suggests the exaltation of Mars in the company of Jupiter (in debilitation) in the 4th house will prove extremely favourable for a Libra native conferring near-regalhood.",
    concordance_texts=["Saravali"],
)

# ── Sloka 17: 2nd lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 5}],
    signal_group="h2_lord_in_h5_native_wealthy",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "native_wealthy_intent_on_earning",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.17",
    description="2nd lord in 5th: the native will be wealthy, intent on earning wealth.",
    commentary_context="Santhanam: The 2nd lord going to the 5th house will make one resort to trickery. His family life will not be happy. He will not be kind to others. He will be very lustful and will be prone to lose a child prematurely.",
)
# v.17 split: children's wealth
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 5}],
    signal_group="h2_lord_in_h5_sons_wealthy",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    entity_target="children",
    predictions=[
        {"entity": "children", "claim": "sons_will_also_be_wealthy",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.17",
    description="2nd lord in 5th: not only the native but also his sons will be wealthy.",
    commentary_context="Santhanam: Same verse as native wealth rule — the text explicitly states both native and sons will be wealthy. Prone to lose a child prematurely.",
)

# ── Sloka 18: 2nd lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 6}],
    signal_group="h2_lord_in_h6_gain_or_loss_enemies",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "gain_wealth_through_enemies_if_benefic_loss_if_malefic",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.18",
    description="2nd lord in 6th with benefic: gain wealth through enemies. With malefic: loss through enemies, mutilation of shanks.",
    commentary_context="Santhanam: There will be severe loss of wealth through thefts and servants. He will have defects of privities. These are further effects of the 2nd lord occupying the 6th house.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "benefic_or_malefic_association", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}],
)

# ── Sloka 19: 2nd lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 7}],
    signal_group="h2_lord_in_h7_others_wives",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "addicted_to_others_wives_doctor_questionable_character",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.19",
    description="2nd lord in 7th: addicted to others' wives, be a doctor. If malefic related, questionable character, wife also.",
    commentary_context="Santhanam: The 2nd lord in the 7th house and related to a dire malefic will render the mother of the native being of questionable character. However, the 4th house and its lord deserve a special attention in the context of mother's disposition.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "malefic_conjunction_or_aspect", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 20: 2nd lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 8}],
    signal_group="h2_lord_in_h8_land_wealth_limited_marriage",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "abundant_land_wealth_but_limited_marital_felicity",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
        {"entity": "native", "claim": "bereft_happiness_from_elder_brother",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.20",
    description="2nd lord in 8th: abundant land and wealth, but limited marital felicity and bereft of happiness from elder brother.",
    commentary_context="Santhanam: No separate note. The verse gives a mixed reading — wealth is favourable but marital and fraternal dimensions suffer.",
)

# ── Sloka 21: 2nd lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 9}],
    signal_group="h2_lord_in_h9_wealthy_diligent",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_diligent_skilful_religious_sick_childhood_happy_later",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.21",
    description="2nd lord in 9th: wealthy, diligent, skilful, sick during childhood and will later on be happy, observing religious code.",
    commentary_context="Santhanam: No separate note. The childhood sickness followed by later prosperity is a notable timing indication.",
)

# ── Sloka 22: 2nd lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 10}],
    signal_group="h2_lord_in_h10_learned_wives",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "libidinous_honourable_learned_many_wives_much_wealth_no_filial_happiness",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.22",
    description="2nd lord in 10th: libidinous, honourable, learned, many wives, much wealth, bereft of filial happiness.",
    commentary_context="Santhanam: No separate note. The mixed result includes wealth/honour alongside lust and denied filial happiness.",
)

# ── Sloka 23: 2nd lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 11}],
    signal_group="h2_lord_in_h11_diligent_famous",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "all_kinds_of_wealth_diligent_honourable_famous",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.23",
    description="2nd lord in 11th: all kinds of wealth, ever diligent, honourable, famous.",
    commentary_context="Santhanam: The native will undergo miseries due to ill-health during childhood and with the march of time he will be endowed with health throughout, if the 2nd lord is in the 11th house.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "childhood_ill_health_transitions_to_good_health_over_time", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 24: 2nd lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 12}],
    signal_group="h2_lord_in_h12_devoid_wealth",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "adventurous_devoid_of_wealth_interested_in_others_wealth",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.24",
    description="2nd lord in 12th: adventurous, devoid of wealth, interested in others' wealth.",
    commentary_context="Santhanam: According to the saying 'if two or more (favourable) planets, the native will be exit emely wealthy.' This is found to be a sound clue in actual cases. However, the 2nd lord lonely in the 12th is bad for riches, except in the case of Aries ascendant with Venus in the 12th in high dignity.",
    concordance_texts=["Saravali"],
    exceptions=["if_two_or_more_favourable_planets_in_12th_then_wealthy"],
)
# v.24 split: eldest child unhappiness
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": 12}],
    signal_group="h2_lord_in_h12_eldest_child_unhappy",
    direction="unfavorable", intensity="moderate",
    primary_domain="progeny",
    entity_target="children",
    predictions=[
        {"entity": "children", "claim": "eldest_child_will_not_keep_native_happy",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.24",
    description="2nd lord in 12th: eldest child will not keep the native happy.",
    commentary_context="Santhanam: Split from native wealth prediction — same verse, distinct entity per granularity principle #2.",
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 25-36: 3RD LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.195-198
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 25: 3rd lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 1}],
    signal_group="h3_lord_in_h1_self_made_wealth",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "self_made_wealth_disposed_to_worship_valorous_intelligent",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.25",
    description="3rd lord in 1st: self-made wealth, disposed to worship, valorous and intelligent although devoid of learning.",
    commentary_context="Santhanam: Notes: lean body with ascendant lord in 3rd. Short-tempered and ill-disposed to others. Having the 3rd lord in the ascendant gives a different shade from the reverse placement.",
    concordance_texts=["Saravali"],
)

# ── Sloka 26: 3rd lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 2}],
    signal_group="h3_lord_in_h2_corpulent_no_valour",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "corpulent_devoid_valour_not_make_efforts_happy_eye_others_wealth",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.26",
    description="3rd lord in 2nd: corpulent, devoid of valour, not make much efforts, happy, eye on others' wives and wealth.",
    commentary_context="Santhanam: Should the 3rd lord be in the 2nd house, one will resort to unnatural sexual means of gratification. He will not show enthusiasm in his undertakings.",
)

# ── Sloka 27: 3rd lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 3}],
    signal_group="h3_lord_in_h3_happy_coborn",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "happiness_through_coborn_wealth_sons_cheerful_extremely_happy",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.27",
    description="3rd lord in 3rd: endowed with happiness through co-born, wealth and sons, cheerful and extremely happy.",
    commentary_context="Santhanam: No separate note. Lord in own house = strong natural indication. Fraternal happiness indicated.",
    concordance_texts=["Saravali"],
)

# ── Sloka 28: 3rd lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 4}],
    signal_group="h3_lord_in_h4_happy_wealthy",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "happy_wealthy_intelligent",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.28",
    description="3rd lord in 4th: happy, wealthy, intelligent.",
    commentary_context="Santhanam: No separate note. Split from spouse prediction — same verse, distinct entities.",
)
# v.28 split: wicked spouse
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 4}],
    signal_group="h3_lord_in_h4_wicked_spouse",
    direction="unfavorable", intensity="moderate",
    primary_domain="relationships",
    entity_target="spouse",
    predictions=[
        {"entity": "spouse", "claim": "spouse_of_wicked_disposition",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.28",
    description="3rd lord in 4th: will acquire a wicked spouse.",
    commentary_context="Santhanam: No separate note. Split from native wealth prediction — same verse, distinct entities per granularity principle #2.",
)

# ── Sloka 29: 3rd lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 5}],
    signal_group="h3_lord_in_h5_sons_virtuous",
    direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "have_sons_be_virtuous_dear_to_friends",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.29",
    description="3rd lord in 5th: have sons, be virtuous. If 3rd lord conjunct/aspected by malefic, will have a formidable wife.",
    commentary_context="Santhanam: No separate note. The malefic influence on 3rd lord in 5th specifically affects the spouse dimension — a formidable (domineering) wife is indicated.",
    modifiers=[{"condition": [{"type": "planet_aspecting", "planet": "any_malefic", "house": "self"}], "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}],
)

# ── Sloka 30: 3rd lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 6}],
    signal_group="h3_lord_in_h6_inimical_coborn",
    direction="unfavorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "inimical_to_coborn_affluent_not_disposed_to_maternal_uncle",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.30",
    description="3rd lord in 6th: inimical to co-born, affluent, not well-disposed to maternal uncle and aunt.",
    commentary_context="Santhanam: An overt clue to the native being fond of physically mating with his maternal aunt. One wonders whether sage Parasara covertly points out to one and the same thing. Possibly so, for the Sanskrit expression is so flexible.",
)

# ── Sloka 31: 3rd lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 7}],
    signal_group="h3_lord_in_h7_serve_king",
    direction="mixed", intensity="moderate",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "interested_serving_king_not_happy_boyhood_unhappy_end_of_life",
         "domain": "career", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.31",
    description="3rd lord in 7th: interested in serving the king, not happy during boyhood, not happy at the end of life.",
    commentary_context="Santhanam: It is not a favourable indication to have an independent profession or business when the 3rd lord is in the 7th house. The 7th denotes one's public relationship, business prospects etc. and an evil lord is not welcome there. As a result, the native will be destined to be in the employ of others. Further, this position will give a tendency to steal. The native will incur a legal award like death.",
    concordance_texts=["Saravali"],
)

# ── Sloka 32: 3rd lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 8}],
    signal_group="h3_lord_in_h8_thief_serve_others",
    direction="unfavorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "thief_derive_livelihood_serving_others_die_at_royal_gate",
         "domain": "career", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.32",
    description="3rd lord in 8th: be a thief, derive livelihood serving others, die at the gate of a royal palace.",
    commentary_context="Santhanam: No separate note. The 3rd lord (effort/courage) in the 8th house (misfortune) leads to criminal livelihood and servitude.",
)

# ── Sloka 33: 3rd lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 9}],
    signal_group="h3_lord_in_h9_fortune_through_wife",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "lack_paternal_bliss_make_fortunes_through_wife_progenic_pleasures",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.33",
    description="3rd lord in 9th: lack paternal bliss, will make fortunes through wife and will enjoy progenic pleasures.",
    commentary_context="Santhanam: Although one may have fortunes and happiness, one will unendingly feel miserable if the 3rd lord occupies the 9th house. His father will be a contemptible person.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "despite_fortunes_native_feels_perpetually_miserable", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 34: 3rd lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 10}],
    signal_group="h3_lord_in_h10_happiness_self_made",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "all_kinds_happiness_self_made_wealth_interested_wicked_females",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.34",
    description="3rd lord in 10th: all kinds of happiness, self-made wealth, interested in nurturing wicked females.",
    commentary_context="Santhanam: No separate note. Mixed result — career success with moral weakness.",
)

# ── Sloka 35: 3rd lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 11}],
    signal_group="h3_lord_in_h11_trading_gain",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "always_gain_in_trading_intelligent_adventurous_serve_others",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.35",
    description="3rd lord in 11th: always gain in trading, be intelligent although not literate, adventurous, serve others.",
    commentary_context="Santhanam: One will have an emaciated body with the 3rd lord's position in the 11th house. He will incur misunderstandings with others and will not be a worthy friend.",
)

# ── Sloka 36: 3rd lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 3, "house": 12}],
    signal_group="h3_lord_in_h12_evil_deeds_wicked_father",
    direction="mixed", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "spend_on_evil_deeds_wicked_father_fortunate_through_female",
         "domain": "wealth", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.36",
    description="3rd lord in 12th: spend on evil deeds, have a wicked father, be fortunate through a female (or wife).",
    commentary_context="Santhanam: The 3rd lord going to the 12th will bestow every happiness in life. Yet the native will feel highly miserable. This view is held by Ramadayalu. If Mars also joins the said 3rd lord, sustenance of co-born will be doubtful.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "mars_conjunct_3rd_lord_in_12th_coborn_sustenance_doubtful", "effect": "negates", "target": "prediction", "strength": "strong", "scope": "local"}],
)


# ═══════════════════════════════════════════════════════════════════════════════
# SLOKAS 37-48: 4TH LORD IN HOUSES 1-12
# Santhanam Vol 1, pp.198-201
# ═══════════════════════════════════════════════════════════════════════════════

# ── Sloka 37: 4th lord in 1st house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 1}],
    signal_group="h4_lord_in_h1_learning_conveyances",
    direction="favorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "endowed_learning_virtues_ornaments_lands_conveyances_maternal_happiness",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.37",
    description="4th lord in ascendant: endowed with learning, virtues, ornaments, lands, conveyances and maternal happiness.",
    commentary_context="Santhanam: As a result of the 4th lord coming to occupy the ascendant, the subject will acquire incomparable learning in various branches. However, there is an element of risk of being deprived of one's ancestral properties. After leading married life for some time, the native will give up worldly life and may turn into an ascetic.",
    concordance_texts=["Saravali", "Phaladeepika"],
    modifiers=[{"condition": "risk_of_ancestral_property_deprivation_and_later_asceticism", "effect": "qualifies", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 38: 4th lord in 2nd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 2}],
    signal_group="h4_lord_in_h2_wealth_family",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "all_kinds_wealth_family_life_honour_adventurous_cunning",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.38",
    description="4th lord in 2nd: enjoy pleasures, all kinds of wealth, family life and honour, adventurous, cunning.",
    commentary_context="Santhanam: The 2nd house tenanted by the 4th lord will bring abundant gains from mother and maternal relatives. The mother of the native will be able to receive great help from her brothers and sisters. The subject will join evil company and face some risks. He will build up self-earned wealth and his lust for lucre will never be subdued.",
    concordance_texts=["Saravali"],
)

# ── Sloka 39: 4th lord in 3rd house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 3}],
    signal_group="h4_lord_in_h3_valorous_charitable",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "valorous_servants_liberal_virtuous_charitable_self_earned_wealth_disease_free",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.39",
    description="4th lord in 3rd: valorous, have servants, liberal, virtuous, charitable, possess self-earned wealth, free from diseases.",
    commentary_context="Santhanam: No separate note. Straightforward favourable reading for 4th lord in 3rd.",
)

# ── Sloka 40: 4th lord in 4th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 4}],
    signal_group="h4_lord_in_h4_minister_wealth",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "minister_all_kinds_wealth_skilful_virtuous_honourable_learned_happy",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.40",
    description="4th lord in 4th: be a minister, possess all kinds of wealth, skilful, virtuous, honourable, learned, happy, well-disposed to spouse.",
    commentary_context="Santhanam: No separate note. Lord in own house produces the strongest natural significations. Career, wealth, learning, and marriage all favoured.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 41: 4th lord in 5th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 5}],
    signal_group="h4_lord_in_h5_happy_devotee",
    direction="favorable", intensity="moderate",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "happy_liked_by_all_devotee_vishnu_virtuous_honourable_self_earned_wealth",
         "domain": "spirituality", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.24 v.41",
    description="4th lord in 5th: happy, liked by all, devoted to Sri Vishnu, virtuous, honourable, self-earned wealth.",
    commentary_context="Santhanam: No separate note. The 4th-5th connection (trikona from trikona) is inherently favourable in Parashari principles.",
)

# ── Sloka 42: 4th lord in 6th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 6}],
    signal_group="h4_lord_in_h6_devoid_maternal_happiness",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_maternal_happiness_anger_thief_conjurer_independent_ill_disposed",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.42",
    description="4th lord in 6th: devoid of maternal happiness, given to anger, be a thief and conjurer, independent in action, ill-disposed.",
    commentary_context="Santhanam: The native will be brought up by another female in the place of his mother. He will be careless about his own matters. He will have litigations on account of properties. His mother will be sickly in constitution and be a source of worry to the family members. He will not be welldisposed toward his mother. These are additional effects for the 6th house placement of the 4th lord.",
    concordance_texts=["Saravali"],
)

# ── Sloka 43: 4th lord in 7th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 7}],
    signal_group="h4_lord_in_h7_education_sacrifice_patrimony",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "high_education_sacrifice_patrimony_dumb_in_assembly",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.43",
    description="4th lord in 7th: endowed with high degree of education, but sacrifice patrimony, be akin to the dumb in an assembly.",
    commentary_context="Santhanam: When the 4th lord occupies the 7th house, the person concerned will not enjoy paternal properties. He may either lose or sacrifice the same. He will not be a householder for a long time and will give up his family burdens sooner or later as a father and as a husband. Though he will achieve a great degree of education, he will be unable to express himself before a group of men.",
)

# ── Sloka 44: 4th lord in 8th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 8}],
    signal_group="h4_lord_in_h8_devoid_comforts",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_domestic_comforts_no_parental_happiness_equal_to_neuter",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.44",
    description="4th lord in 8th: devoid of domestic and other comforts, not enjoy parental happiness, be equal to a neuter.",
    commentary_context="Santhanam: The 4th lord's relegation to the 8th house will affect the progenic ability of the native and he will not be able to carnally satisfy his spouse. His happiness in household life will not be appreciable; some problem or the other will accost him. His education will face many an obstacle. His childhood will be with many difficulties.",
)

# ── Sloka 45: 4th lord in 9th house ───────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 9}],
    signal_group="h4_lord_in_h9_dear_to_all_devoted",
    direction="favorable", intensity="strong",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "dear_to_all_devoted_to_god_virtuous_honourable_every_happiness",
         "domain": "spirituality", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.45",
    description="4th lord in 9th: dear to one and all, devoted to God, virtuous, honourable, endowed with every kind of happiness.",
    commentary_context="Santhanam: No separate note. The 4th-9th axis (fortune + comfort) produces one of the most auspicious combinations in Parashari doctrine.",
    concordance_texts=["Saravali", "Phaladeepika"],
)

# ── Sloka 46: 4th lord in 10th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 10}],
    signal_group="h4_lord_in_h10_royal_honours",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "royal_honours_alchemist_extremely_pleased_conquer_five_senses",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.46",
    description="4th lord in 10th: enjoy royal honours, be an alchemist, extremely pleased, enjoy all pleasures, conquer five senses.",
    commentary_context="Santhanam: One will be professionally happy and prosperous with the 4th lord in the 10th house. He will have abundant self-made properties. He will, however, lack maternal happiness if the 4th lord in the said house is not happily placed.",
    concordance_texts=["Saravali"],
    modifiers=[{"condition": "4th_lord_not_happily_placed_in_10th_lacks_maternal_happiness", "effect": "negates", "target": "prediction", "strength": "medium", "scope": "local"}],
)

# ── Sloka 47: 4th lord in 11th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 11}],
    signal_group="h4_lord_in_h11_secret_disease",
    direction="mixed", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "fear_of_secret_disease_liberal_virtuous_charitable_helpful",
         "domain": "health", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.24 v.47",
    description="4th lord in 11th: fear of secret disease, be liberal, virtuous, charitable and helpful to others.",
    commentary_context="Santhanam: Some say that the 11th house having the 4th lord will ensure freedom from diseases while our sage attributes secret diseases (like venereal affliction or any other diseases caused by physical union). Apparently the sage does not prefer the 4th lord (lord of happiness) getting relegated to the 11th (the 8th from the 4th).",
)

# ── Sloka 48: 4th lord in 12th house ──────────────────────────────────────
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 4, "house": 12}],
    signal_group="h4_lord_in_h12_devoid_comforts_vices",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "devoid_domestic_comforts_vices_foolish_indolent",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.24 v.48",
    description="4th lord in 12th: devoid of domestic and other comforts, have vices, be foolish and indolent.",
    commentary_context="Santhanam: Complete absence of happiness, particularly paternal, will come to pass. One will be bereft of masculine vigour. His mother is of doubtful character. These are additional effects for the 4th lord being in the 12th house, according to classical works.",
    concordance_texts=["Saravali"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD REGISTRY
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH24A_REGISTRY = b.build()
