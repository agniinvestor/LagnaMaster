"""src/corpus/bphs_v2_ch13.py — BPHS Ch.13 (2nd House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.132-136.
Chapter: 13 — Effects of the Second House (Dhana Bhava Phala)
Slokas: 13 (v.1-2 wealth combinations, v.3 Jupiter/Mars wealth, v.4 exchange,
  v.5 wealthy subject, v.6-7 poverty yogas, v.8 loss through king,
  v.9 good expenses, v.10 fame, v.11 effortless acquisition,
  v.12 eyes, v.13 untruthful person)

V2 Protocol Compliance:
  Protocol A: One-claim-one-rule — 20 rules from 13 slokas ✓
  Protocol B: Contrary mirrors — v.1-2 (wealth/decline), v.12 (eyes) ✓
  Protocol C: Entity target — all "native" (verified, no father/spouse) ✓
  Protocol D: Santhanam commentary included ✓
  Protocol E: Computable conditions (8 primitives) ✓
  Protocol F: Timing extracted — v.6-7 "from birth", rest unspecified ✓
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.13", category="2nd_house_effects",
    id_start=1300, session="S311", sloka_count=13,
    chapter_tags=["2nd_house", "dhana_bhava"],
    entity_target="native",
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKAS 1-2: Combinations for Wealth
# ═════════════════════════════════════════════════════════════════════════

# v.1-2a: 2nd lord in kendra/trikona → promotes wealth
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [1, 4, 5, 7, 9, 10]},
    ],
    signal_group="h2_lord_kendra_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealth_promoted",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.13 v.1-2",
    commentary_context=(
        "Santhanam notes for v.1-2 (shared): Venus or Mercury in the 2nd "
        "will be favourable for wealth while Jupiter will not be wholly "
        "auspicious. If Jupiter rules the 2nd, financial aspects smooth. "
        "Otherwise Jupiter in the 2nd denotes a problematic financial situation."
    ),
    description=(
        "2nd lord in the 2nd or in an angle or trine from the ascendant: "
        "promotes one's wealth (or monetary state). Financial conditions "
        "are favorable throughout life."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    convergence_signals=["h2_lord_strong_dignity", "benefic_in_2nd"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1301"]},
    tags=["h2_lord", "kendra", "trikona", "wealth"],
)

# v.1-2b: 2nd lord in 6/8/12 → financial decline (contrary mirror)
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [6, 8, 12]},
    ],
    signal_group="h2_lord_dusthana_poverty",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "financial_conditions_decline",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.13 v.1-2",
    commentary_context="Contrary of BPHS1300. See shared Santhanam notes on v.1-2.",
    description=(
        "2nd lord in 6th, 8th, or 12th: financial conditions will decline. "
        "Wealth is lost through disease (6th), sudden events (8th), or "
        "expenditure (12th)."
    ),
    concordance_texts=["Saravali", "Phaladeepika"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1300"]},
    tags=["h2_lord", "dusthana", "poverty"],
)

# v.1-2c: Benefic in 2nd → gives wealth
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_benefic", "house": 2},
    ],
    signal_group="benefic_h2_wealth",
    direction="favorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealth_through_benefic_in_2nd",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.1-2",
    description=(
        "A benefic in the 2nd house will give wealth."
    ),
    commentary_context=(
        "Santhanam notes: Venus or Mercury in the 2nd will be favourable "
        "for wealth while Jupiter will not be wholly auspicious. If "
        "however Jupiter is in the 2nd ruling the 2nd, then financial "
        "aspects will be smooth. This is why the sage specifically "
        "mentions Jupiter in the next sloka."
    ),
    concordance_texts=["Saravali"],
    divergence_notes="Jupiter in 2nd not wholly auspicious unless ruling 2nd",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1303"]},
    tags=["benefic", "h2", "wealth"],
)

# v.1-2d: Malefic in 2nd → destroys wealth (contrary mirror)
b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 2},
    ],
    signal_group="malefic_h2_poverty",
    direction="unfavorable", intensity="moderate",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealth_destroyed_by_malefic",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.1-2",
    commentary_context="Contrary of BPHS1302. Malefic replaces benefic; opposite results.",
    description=(
        "A malefic in the 2nd will destroy wealth instead."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1302"]},
    tags=["malefic", "h2", "poverty"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 3: Jupiter rules 2nd or conjunct Mars → wealthy
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": 2},
    ],
    signal_group="jupiter_h2_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_jupiter_rules_or_occupies_2nd",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.13 v.3",
    description=(
        "One will be wealthy if Jupiter is in the 2nd as the lord of "
        "the 2nd or is with Mars. Jupiter ruling the 2nd applies to "
        "Scorpio and Aquarius ascendants."
    ),
    commentary_context=(
        "Santhanam notes: There are two independent conditions. Jupiter, "
        "if in the 2nd, should be the ruler of the 2nd for the native "
        "becoming wealthy. This applies to Scorpio and Aquarius ascendant. "
        "Whether or not Jupiter owns the 2nd, if he is conjunct Mars, "
        "wealth will be acquired by the native; the house occupied by "
        "them not standing for consideration."
    ),
    concordance_texts=["Saravali"],
    convergence_signals=["mars_conjunct_jupiter", "h2_lord_strong"],
    tags=["jupiter", "h2", "mars", "wealth"],
    modifiers=[],
    lagna_scope=["scorpio", "aquarius"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 4: 2nd-11th lord exchange → wealth
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": 11},
        {"type": "lord_in_house", "lord_of": 11, "house": 2},
    ],
    signal_group="h2_h11_exchange_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealth_acquired_through_exchange",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.13 v.4",
    description=(
        "2nd lord in the 11th while the lord of the 11th is in the 2nd: "
        "wealth will be acquired by the native. Alternatively these two "
        "lords may join in an angle or in a trine for financial gains."
    ),
    commentary_context=(
        "Santhanam notes: The 11th lord has a say in financial matters "
        "apart from the 2nd lord. One's gains are indicated by the 11th "
        "lord. If he is in exchange with the 2nd lord, the native will "
        "be wealthy. These two planets joining in the ascendant, 4th, "
        "7th, 10th, 5th or 9th will also lead to financial gains."
    ),
    tags=["h2_lord", "h11_lord", "exchange", "parivartana", "wealth"],
    modifiers=[
        {"condition": "lords_2_11_join_in_kendra_trikona_instead_of_exchange", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"},
    ],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 5: 2nd lord in angle + 11th lord in trine + Jupiter/Venus
# ═════════════════════════════════════════════════════════════════════════

# v.5a: 2nd lord in angle + 11th lord in trine → wealthy
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [1, 4, 7, 10]},
        {"type": "lord_in_house", "lord_of": 11, "house": [1, 5, 9]},
    ],
    signal_group="h2_kendra_h11_trikona_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_subject",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.13 v.5",
    description=(
        "2nd lord in an angle while the 11th lord is in a trine thereof: "
        "the subject will be wealthy."
    ),
    commentary_context=(
        "Santhanam notes: The lord of the 2nd should be in the ascendant, "
        "or 4th/7th/10th house. The 11th lord should be in the 5th/9th "
        "counted from the house occupied by the 2nd lord. This is one of "
        "two alternative combinations for gaining wealth (see BPHS1307)."
    ),
    modifiers=[],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1307"]},
    tags=["h2_lord", "h11_lord", "wealth"],
)

# v.5b: 2nd lord aspected/conjunct Jupiter or Venus → wealthy (alternative path)
b.add(
    conditions=[
        {"type": "planets_conjunct", "planets": ["lord_of_2", "Jupiter"]},
    ],
    signal_group="h2_lord_jupiter_venus_aspect_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "wealthy_through_jupiter_venus_relation",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.13 v.5",
    description=(
        "Alternatively, the 2nd lord related to Jupiter or Venus by "
        "conjunction or aspect: the subject will be wealthy."
    ),
    commentary_context=(
        "Santhanam notes: Alternatively the 2nd lord should be related "
        "to Jupiter (and) or Venus by conjunction or by aspect. Both "
        "the combinations are for gaining wealth."
    ),
    modifiers=[
        {"condition": "venus_also_aspects_or_conjuncts_lord_of_2", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"},
    ],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1306"]},
    tags=["h2_lord", "jupiter", "venus", "wealth"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKAS 6-7: Yogas for Poverty
# ═════════════════════════════════════════════════════════════════════════

# v.6-7a: 2nd lord in evil house + malefic in 2nd → penniless
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [6, 8, 12]},
        {"type": "planet_in_house", "planet": "any_malefic", "house": 2},
    ],
    signal_group="h2_lord_dusthana_penniless",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "penniless_from_birth",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.9},
    ],
    timing_window={"type": "age", "value": 0, "precision": "exact"},
    verse_ref="Ch.13 v.6-7",
    description=(
        "2nd lord in an evil house while the 11th lord is also badly "
        "placed and the 2nd is occupied by a malefic: one will be "
        "penniless. Penury right from birth."
    ),
    commentary_context=(
        "Santhanam notes: The lords of the 2nd and 11th can be jointly "
        "in the 6th/8th/12th or individually disposed in any two of "
        "the said three houses. Simultaneously the 2nd house needs a "
        "malefic in it. Thus there are afflictions from three "
        "directions which will make the native extremely poor."
    ),
    concordance_texts=["Saravali"],
    tags=["h2_lord", "h11_lord", "dusthana", "poverty", "penury"],
)

# v.6-7b: Both lords combust → beg for food
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_2", "dignity": "weak"},
    ],
    signal_group="h2_lord_combust_begging",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "beg_for_food",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.9},
    ],
    timing_window={"type": "age", "value": 0, "precision": "exact"},
    verse_ref="Ch.13 v.6-7",
    description=(
        "The native will have to beg even for food if the lords of the "
        "2nd and 11th are both combust or be with malefics."
    ),
    commentary_context=(
        "Santhanam notes: Even food is denied to one having combust 2nd "
        "lord and combust 11th lord. Alternatively the 2nd lord may be "
        "with a severe malefic while the 11th lord is also similarly "
        "placed. The conjunction of the 2nd lord with a Yogakaraka, "
        "although a malefic, will not be adverse in the matter of "
        "finance. On the contrary it will prove very auspicious. For "
        "example, Mercury the 2nd lord joining Saturn in the case of "
        "a Taurus native, will make financial prospects superior."
    ),
    exceptions=["if_2nd_lord_conjunct_yogakaraka"],
    cross_chapter_refs=["Ch.34 Yoga Karakas"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1310"]},
    tags=["h2_lord", "h11_lord", "combust", "begging", "poverty"],
)

# v.6-7 contrary: weak 2nd lord BUT conjunct yogakaraka → auspicious (Santhanam)
# NOT a mirror — different condition set (yogakaraka conjunction is REQUIRED here)
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_2", "dignity": "weak"},
        {"type": "planets_conjunct", "planets": ["lord_of_2", "yogakaraka"]},
    ],
    signal_group="h2_lord_yogakaraka_auspicious",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "financial_prospects_superior_despite_weak_lord",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.13 v.6-7",
    description=(
        "Contrary: 2nd lord conjunct a Yogakaraka (though malefic by nature) "
        "will prove very auspicious for finance. E.g., Mercury (2nd lord) "
        "joining Saturn for Taurus lagna makes financial prospects superior."
    ),
    commentary_context=(
        "Santhanam notes: The conjunction of the 2nd lord with a Yogakaraka, "
        "although a malefic, will not be adverse in the matter of finance. "
        "On the contrary it will prove very auspicious."
    ),
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1308"]},
    cross_chapter_refs=["Ch.34 Yoga Karakas"],
    tags=["h2_lord", "yogakaraka", "wealth", "reversal"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 8: Loss of Wealth Through the King
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [6, 8, 12]},
        {"type": "lord_in_house", "lord_of": 11, "house": [6, 8, 12]},
        {"type": "planet_in_house", "planet": "Mars", "house": 11},
        {"type": "planet_in_house", "planet": "Rahu", "house": 2},
    ],
    signal_group="h2_h11_government_loss",
    direction="unfavorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "lose_wealth_through_government",
         "domain": "wealth", "direction": "unfavorable", "magnitude": 0.8},
        {"entity": "native", "claim": "royal_punishments_fines",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.13 v.8",
    description=(
        "Lords of the 2nd and 11th relegated to the 6th/8th/12th "
        "(jointly or separately) while Mars is in the 11th and Rahu "
        "is in the 2nd: the native will lose his wealth on account "
        "of royal punishments."
    ),
    commentary_context=(
        "Santhanam notes: This combination will cause financial losses "
        "through penalties, fines etc. imposed by the government, in "
        "the modern context. Monetary deficiencies will as well persist "
        "throughout."
    ),
    tags=["h2_lord", "h11_lord", "mars", "rahu", "government", "fines"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 9: Expenses on Good Accounts
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "Jupiter", "house": 11},
        {"type": "planet_in_house", "planet": "Venus", "house": 2},
        {"type": "planet_in_house", "planet": "any_benefic", "house": 12},
        {"type": "planets_conjunct", "planets": ["lord_of_2", "any_benefic"]},
    ],
    signal_group="jupiter_h11_venus_h2_charity",
    direction="favorable", intensity="moderate",
    primary_domain="spirituality",
    predictions=[
        {"entity": "native", "claim": "expenses_on_religious_charitable_grounds",
         "domain": "spirituality", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.9",
    commentary_context="No separate Santhanam note for v.9. The conditions are explicit in the verse.",
    description=(
        "Jupiter in the 11th, Venus in the 2nd, and a benefic in the "
        "12th while the 2nd lord is conjunct a benefic: there will be "
        "expenses on religious or charitable grounds."
    ),
    modifiers=[],
    tags=["jupiter", "venus", "h11", "h2", "charity", "religion"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 10: Fame
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_2", "dignity": "exalted"},
    ],
    signal_group="h2_lord_exalted_fame",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "famous_helps_others",
         "domain": "career", "direction": "favorable", "magnitude": 0.7},
        {"entity": "native", "claim": "looks_after_his_people",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.10",
    description=(
        "2nd lord in own sign or exalted: the native will look after "
        "his people, will help others and will become famous."
    ),
    commentary_context=(
        "Santhanam notes: Our text requires the 2nd lord to be in "
        "exaltation or in own sign so that the native will look after "
        "his people & C. Chaukhamba edition has almost a different "
        "condition: the 2nd lord should be in deep exaltation or in "
        "own sign and be in aspect to Jupiter. The result given "
        "therein is 'fame and liked bypall'. I feel mere exaltation "
        "of the 2nd lord is enough for obtaining the said results."
    ),
    tags=["h2_lord", "exalted", "own_sign", "fame"],
    prediction_type="trait",
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 11: Effortless Acquisition
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_2", "dignity": "strong"},
        {"type": "planets_conjunct", "planets": ["lord_of_2", "any_benefic"]},
    ],
    signal_group="h2_lord_paravatamsa_wealth",
    direction="favorable", intensity="strong",
    primary_domain="wealth",
    predictions=[
        {"entity": "native", "claim": "effortless_wealth_all_kinds",
         "domain": "wealth", "direction": "favorable", "magnitude": 0.9},
    ],
    verse_ref="Ch.13 v.11",
    description=(
        "2nd lord conjunct a benefic and in a good division like "
        "Paravatamsa: there will be all kinds of wealth in his family "
        "effortlessly."
    ),
    commentary_context=(
        "Santhanam notes: 'Paravatamsa' denotes six good Vargas out of "
        "Dasavarga scheme (vide ch.6, supra). 'Paravatamsadau' of the "
        "text denotes Paravata or such other higher Vargas. To wit, the "
        "2nd lord should be in Paravatamsa or in Devalokamsa, "
        "Brahmalokamsa, Sakravahanamsa or Sridhanamamsa in the "
        "Dasavarga scheme. The corresponding superior Amsas whom the "
        "entire Shodasavarga scheme is used should be above "
        "Poornachandramsa. This varga denotes 6 good divisions in "
        "Dasavarga scheme i.e. above 50% of good divisions. The 2nd "
        "lord being endowed with such a Varga dignity and conjunct "
        "another benefic brings in effortless wealth and wealth of "
        "all kinds."
    ),
    cross_chapter_refs=["Ch.6 Sixteen Divisions", "Ch.7 Divisional Consideration"],
    modifiers=[],
    tags=["h2_lord", "paravatamsa", "varga", "effortless", "wealth"],
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 12: Eyes
# ═════════════════════════════════════════════════════════════════════════

# v.12a: 2nd lord strong → beautiful eyes
b.add(
    conditions=[
        {"type": "planet_dignity", "planet": "lord_of_2", "dignity": "strong"},
    ],
    signal_group="h2_lord_strong_eyes",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "beautiful_eyes",
         "domain": "character", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.12",
    description=(
        "2nd lord endowed with strength: the native will possess "
        "beautiful eyes."
    ),
    commentary_context=(
        "Santhanam notes: 'Netresa' denotes the lord of the 2nd, i.e. "
        "significator of eyes. This does not mean that the 12th lord "
        "has nothing to do with eyes. Precisely, 2nd lord and 12th "
        "lord over right eye and left eye respectively. However, when "
        "the beauty of the eyes is to be known, it is from the 2nd "
        "house only. Jupiter well placed in the 2nd, or the 2nd lord "
        "in exaltation, or with a benefic will give one beautiful "
        "eyes. While Venus in the 2nd or Full Moon in the 2nd will "
        "not deprive one of beautiful eyes. Mercury in the 2nd will "
        "have a say on the speech rather than on the sight. Hence "
        "Jupiter's position in the 2nd is a safe bet for strong sight "
        "and beauty of the eyes, if the planet is not with evils of "
        "fall and the like."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1315"]},
    tags=["h2_lord", "eyes", "beauty", "sight"],
    prediction_type="trait",
)

# v.12b: 2nd lord in 6/8/12 → eye disease (contrary mirror)
b.add(
    conditions=[
        {"type": "lord_in_house", "lord_of": 2, "house": [6, 8, 12]},
    ],
    signal_group="h2_lord_dusthana_eye_disease",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "native", "claim": "disease_or_deformity_of_eyes",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.13 v.12",
    commentary_context=(
        "Contrary of BPHS1313. Santhanam: Netresa = lord of 2nd = "
        "significator of eyes. 2nd lord over right eye, 12th lord over "
        "left eye. Beauty of eyes from 2nd house only."
    ),
    description=(
        "2nd lord in the 6th, 8th, or 12th: there will be disease or "
        "deformity of eyes."
    ),
    concordance_texts=["Saravali"],
    rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS1313"]},
    tags=["h2_lord", "dusthana", "eye_disease"],
    prediction_type="trait",
)

# ═════════════════════════════════════════════════════════════════════════
# SLOKA 13: Untruthful Person
# ═════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[
        {"type": "planet_in_house", "planet": "any_malefic", "house": 2},
        {"type": "planets_conjunct", "planets": ["lord_of_2", "any_malefic"]},
    ],
    signal_group="h2_malefic_untruthful",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "tale_bearer_speaks_untruth",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
        {"entity": "native", "claim": "windy_diseases_gastric",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.13 v.13",
    description=(
        "2nd house and its lord conjunct malefics: the native will be "
        "a tale-bearer, will speak untruth and will be afflicted by "
        "windy diseases."
    ),
    commentary_context=(
        "Santhanam notes: The 2nd house and its lord are referred in "
        "the matter of windy diseases. Gastric troubles, rheumatism "
        "and the like are classified under windy disorders. If the 2nd "
        "house or its lord is associated with Saturn or Mercury it "
        "will cause rheumatism and such other disorders. If Jupiter "
        "is in affliction so related, gastric troubles will come to "
        "pass."
    ),
    modifiers=[
        {"condition": "saturn_or_mercury_associated", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"},
        {"condition": "jupiter_afflicted_in_connection", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"},
    ],
    tags=["malefic", "h2", "untruth", "windy_disease", "gastric"],
    prediction_type="trait",
)


# v.1-2/v.3 combined: Jupiter in 2nd as ruler — covered by BPHS1304 with lagna_scope
# Removed duplicate BPHS1317 — same condition + lagna_scope as BPHS1304

# ═══ v.3 MISSING: Jupiter conjunct Mars anywhere → wealth
b.add(
    conditions=[{"type": "planets_conjunct", "planets": ["Jupiter", "Mars"]}],
    signal_group="jupiter_mars_conjunct_wealth",
    direction="favorable", intensity="moderate", primary_domain="wealth",
    predictions=[{"entity": "native", "claim": "wealth_acquired_through_jupiter_mars_conjunction", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.13 v.3",
    commentary_context="Santhanam: Jupiter conjunct Mars gives wealth regardless of house ownership or placement. The 'whether or not' clarifies this is unconditional — no lordship or house modifier applies.",
    description="Jupiter conjunct Mars in any house: wealth acquired. House position irrelevant. Unconditional — no lordship modifier.",
    concordance_texts=["Saravali"],
    modifiers=[])

# ═══ v.4 MISSING: 2nd + 11th lords joining in kendra/trikona → gains
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 2, "house": [1, 4, 5, 7, 9, 10]},
                {"type": "lord_in_house", "lord_of": 11, "house": [1, 4, 5, 7, 9, 10]}],
    signal_group="h2_h11_lords_kendra_trikona_gains",
    direction="favorable", intensity="moderate", primary_domain="wealth",
    predictions=[{"entity": "native", "claim": "financial_gains_through_wealth_lords_in_kendra", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
    verse_ref="Ch.13 v.4",
    commentary_context="Santhanam: The 11th lord has a say in financial matters apart from 2nd lord. These two joining in ascendant, 4th, 7th, 10th, 5th or 9th will also lead to financial gains.",
    description="2nd and 11th lords joining in any kendra or trine: financial gains.")

# ═══ v.12 MISSING: Jupiter in 2nd or 2nd lord exalted → beautiful eyes
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 2}],
    signal_group="jupiter_h2_beautiful_eyes",
    direction="favorable", intensity="moderate", primary_domain="character",
    predictions=[{"entity": "native", "claim": "beautiful_eyes_from_jupiter_in_2nd", "domain": "character", "direction": "favorable", "magnitude": 0.6}],
    verse_ref="Ch.13 v.12",
    commentary_context="Santhanam: Jupiter well placed in 2nd, or 2nd lord in exaltation, or with benefic = beautiful eyes. Jupiter's position in 2nd is a safe bet for strong sight and beauty of eyes.",
    description="Jupiter in 2nd: beautiful eyes and strong sight.",
    prediction_type="trait")

# ═══ v.12 MISSING: Venus/Full Moon in 2nd → beautiful eyes
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Venus", "house": 2}],
    signal_group="venus_full_moon_h2_beautiful_eyes",
    direction="favorable", intensity="moderate", primary_domain="character",
    predictions=[{"entity": "native", "claim": "beautiful_eyes_venus_or_full_moon_in_2nd", "domain": "character", "direction": "favorable", "magnitude": 0.5}],
    verse_ref="Ch.13 v.12",
    commentary_context="Santhanam: Venus in 2nd or Full Moon in 2nd will not deprive one of beautiful eyes.",
    description="Venus or Full Moon in 2nd: will not deprive of beautiful eyes.",
    prediction_type="trait")

# ═══ v.12 MISSING: Mercury in 2nd → speech not sight
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mercury", "house": 2}],
    signal_group="mercury_h2_speech_not_sight",
    direction="neutral", intensity="moderate", primary_domain="character",
    predictions=[{"entity": "native", "claim": "mercury_2nd_affects_speech_more_than_sight", "domain": "character", "direction": "neutral", "magnitude": 0.4}],
    verse_ref="Ch.13 v.12",
    commentary_context="Santhanam: Mercury in 2nd will have a say on the speech rather than on the sight. Hence Jupiter's position in the 2nd is a safe bet for strong sight.",
    description="Mercury in 2nd: affects speech more than sight.",
    prediction_type="trait")

# ═══ v.13 MISSING: Saturn in 2nd → rheumatism/windy disorders
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 2}],
    signal_group="saturn_h2_rheumatism",
    direction="unfavorable", intensity="moderate", primary_domain="health",
    predictions=[{"entity": "native", "claim": "rheumatism_and_windy_disorders",
                   "domain": "health", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.13 v.13",
    commentary_context="Santhanam: If 2nd house or its lord is associated with Saturn = rheumatism and such other windy disorders.",
    description="Saturn in 2nd or associated with 2nd lord: rheumatism and windy disorders.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1324"]})

# ═══ v.13 MISSING: Mercury in 2nd → rheumatism/windy disorders (alternative path)
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Mercury", "house": 2}],
    signal_group="mercury_h2_rheumatism",
    direction="unfavorable", intensity="moderate", primary_domain="health",
    predictions=[{"entity": "native", "claim": "rheumatism_and_windy_disorders",
                   "domain": "health", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.13 v.13",
    commentary_context="Santhanam: If 2nd house or its lord is associated with Mercury = rheumatism and such other windy disorders. Mercury is an alternative causal path to Saturn.",
    description="Mercury in 2nd or associated with 2nd lord: rheumatism and windy disorders.",
    rule_relationship={"type": "alternative", "related_rules": ["BPHS1323"]})

# ═══ v.13 MISSING: Jupiter in affliction → gastric
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 2}],
    signal_group="jupiter_h2_afflicted_gastric",
    direction="unfavorable", intensity="moderate", primary_domain="health",
    predictions=[{"entity": "native", "claim": "gastric_troubles_from_afflicted_jupiter", "domain": "health", "direction": "unfavorable", "magnitude": 0.5}],
    verse_ref="Ch.13 v.13",
    commentary_context="Santhanam: If Jupiter is in affliction so related, gastric troubles will come to pass.",
    description="Jupiter in 2nd in affliction: gastric troubles.",
    modifiers=[{"condition": "jupiter_afflicted", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}])

BPHS_V2_CH13_REGISTRY = b.build()
