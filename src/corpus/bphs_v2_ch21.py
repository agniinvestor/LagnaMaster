"""src/corpus/bphs_v2_ch21.py — BPHS Ch.21 (10th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.178-183.
Chapter: 21 — Effects of the Tenth House (Karma Bhava Phala)
Slokas: 22 (20 predictive). Career, fame, deeds, patronage, Gnana yoga.
Entity: native (all — career/karma predictions about the native).
FULL RE-ENCODE S312: Previous version had 6 rules from 22 slokas (0.27 ratio).
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(chapter="Ch.21", category="10th_house_effects", id_start=2100, session="S312",
                      chapter_tags=["10th_house", "karma_bhava"], entity_target="native",
                      sloka_count=20)

# ═══ v.2: 10th lord strong → paternal happiness, fame ════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_10", "dignity": "strong"}],
      signal_group="h10_lord_strong_fame", direction="favorable", intensity="strong",
      domains=["career_status", "fame_reputation"],
      predictions=[{"entity": "native", "claim": "paternal_happiness_fame_good_deeds", "domain": "career_status", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.21 v.2",
      commentary_context="Santhanam: 'Karma' means deed — profession, job, livelihood. 10th house also rules patrimony, last offices to father. 9th house deals with father as individual.",
      description="10th lord strong in exaltation or own Rasi/Navamsa: paternal happiness, fame and good deeds.",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "alternative", "related_rules": ["BPHS2101"]})

# ═══ v.3a: 10th lord weak → obstructions ═════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_10", "dignity": "weak"}],
      signal_group="h10_lord_weak_obstruction", direction="unfavorable", intensity="moderate",
      domains=["career_status"],
      predictions=[{"entity": "native", "claim": "obstructions_in_professional_work", "domain": "career_status", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.3a",
      commentary_context="Contrary of v.2. Weak 10th lord = professional efforts meet resistance.",
      description="10th lord devoid of strength: obstructions in work.",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2100"]})

# ═══ v.3b: Rahu in kendra/trikona → Jyotishtoma ══════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": [1, 4, 5, 7, 9, 10]}],
      signal_group="rahu_kendra_trikona_jyotishtoma", direction="favorable", intensity="moderate",
      domains=["spirituality"],
      predictions=[{"entity": "native", "claim": "performs_jyotishtoma_sacrifice_extremely_religious", "domain": "spirituality", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.21 v.3b",
      commentary_context="Santhanam: Rahu strongly in kendra/trikona = Jyotishtoma — Soma sacrifice of sixteen Vedic rites. Native extremely religious and meritorious.",
      description="Rahu strongly disposed in angle or trine: performs Jyotishtoma sacrifice, extremely religious.")

# ═══ v.4: Royal patronage (+ contrary mirror) ════════════════════════════════
b.add(conditions=[
          {"type": "lord_in_sign", "lord_of": 10,
           "sign": ["Sagittarius", "Pisces", "Taurus", "Libra", "Cancer", "Gemini", "Virgo"]},
      ],
      signal_group="h10_lord_benefic_patronage", direction="favorable", intensity="strong",
      domains=["career_status", "wealth"],
      predictions=[{"entity": "native", "claim": "always_gain_through_royal_patronage_and_business", "domain": "career_status", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.4",
      commentary_context=(
          "Santhanam: 10th lord with benefic or in benefic's Rasi = ever gain. "
          "Benefic signs: Jupiter (Sag/Pisces), Venus (Taurus/Libra), "
          "Moon (Cancer), Mercury (Gemini/Virgo). 'Anyatha-nyatha' = contrary: "
          "malefic Rasi = loser."
      ),
      description="10th lord in benefic's Rasi: always gain through royal patronage and business.",
      concordance_texts=["Saravali"])

b.mirror("BPHS2103",
         description="Contrary: 10th lord with malefic or in malefic's Rasi — loser in calling, will not serve king.",
         signal_group="h10_lord_malefic_loser")

# ═══ v.5: Malefics in 10th + 11th → bad deeds ═══════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 10},
                   {"type": "planet_in_house", "planet": "any_malefic", "house": 11}],
      signal_group="malefics_h10_h11_bad_deeds", direction="unfavorable", intensity="moderate",
      domains=["character_temperament", "career_status"],
      predictions=[{"entity": "native", "claim": "indulge_in_bad_deeds_defile_own_men", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.21 v.5",
      commentary_context="No separate note. Both karma (10th) and gains (11th) corrupted by malefics.",
      description="10th and 11th both occupied by malefics: bad deeds, defile his own men.")

# ═══ v.6: 10th lord in 8th with Rahu → fool ═════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 8},
                   {"type": "planet_in_house", "planet": "Rahu", "house": 8}],
      signal_group="h10_lord_h8_rahu_fool", direction="unfavorable", intensity="strong",
      domains=["intelligence_education", "character_temperament"],
      predictions=[{"entity": "native", "claim": "great_fool_bad_deeds_hate_others", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.6",
      commentary_context="Santhanam: 8th house occupied by Rahu + 10th lord spoils professional happiness, leads to questionable/foolish deeds and misconceptions.",
      description="10th lord in 8th with Rahu: hate others, great fool, bad deeds.")

# ═══ v.7: Saturn+Mars+10th lord in 7th → carnal ══════════════════════════════
b.add(conditions=[
          {"type": "planet_in_house", "planet": "Saturn", "house": 7},
          {"type": "planet_in_house", "planet": "Mars", "house": 7},
          {"type": "lord_in_house", "lord_of": 10, "house": 7},
      ],
      signal_group="saturn_mars_h10_lord_h7_carnal", direction="unfavorable", intensity="moderate",
      domains=["character_temperament", "marriage"],
      predictions=[{"entity": "native", "claim": "fond_of_carnal_pleasures_and_filling_belly", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.5}],
      verse_ref="Ch.21 v.7",
      commentary_context=(
          "Santhanam: 'Sisnodara Parayana' = devoted to male organ and stomach. "
          "All three required in 7th: Saturn + Mars + 10th lord."
      ),
      description="Saturn, Mars and 10th lord all in 7th: fond of carnal pleasures and filling belly.")

# ═══ v.8-10: Exalted 10th lord + Jupiter → honour, robes ═════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": [1, 4, 5, 7, 9, 10]},
                   {"type": "planet_dignity", "planet": "lord_of_10", "dignity": "exalted"}],
      signal_group="h10_lord_exalted_kendra_honour", direction="favorable", intensity="strong",
      domains=["career_status", "wealth", "fame_reputation"],
      predictions=[
          {"entity": "native", "claim": "endowed_with_honour_wealth_and_valour", "domain": "career_status", "direction": "favorable", "magnitude": 0.8},
          {"entity": "native", "claim": "robes_ornaments_and_happiness", "domain": "wealth", "direction": "favorable", "magnitude": 0.7},
      ],
      verse_ref="Ch.21 v.8-10",
      commentary_context="Santhanam: 10th lord in Pisces + Jupiter = obtain robes, ornaments, happiness. If 11th lord in 10th + 10th lord + Jupiter = happy life.",
      description="10th lord exalted in kendra + Jupiter as 9th lord in 10th: honour, wealth, valour, robes, ornaments.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "11th_lord_also_in_10th_with_10th_lord_and_jupiter", "effect": "amplifies", "strength": "strong"}])

# ═══ v.11: 4 malefics in 11th → cessation of duties ═════════════════════════
b.add(conditions=[
          {"type": "planet_in_house", "planet": "Rahu", "house": 11},
          {"type": "planet_in_house", "planet": "Sun", "house": 11},
          {"type": "planet_in_house", "planet": "Saturn", "house": 11},
          {"type": "planet_in_house", "planet": "Mars", "house": 11},
      ],
      signal_group="rahu_sun_saturn_mars_h11_cessation", direction="unfavorable", intensity="strong",
      domains=["career_status"],
      predictions=[{"entity": "native", "claim": "cessation_of_duties_no_happy_calling", "domain": "career_status", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.11",
      commentary_context=(
          "Santhanam: All four malefics required in 11th — Sun, Mars, "
          "Rahu, Saturn. Quadruple affliction of gains house."
      ),
      description="Rahu, Sun, Saturn and Mars all in 11th: cessation of duties.")

# ═══ v.12: Gnana Yoga ════════════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 12}],
      signal_group="jupiter_pisces_venus_gnana_yoga", direction="favorable", intensity="strong",
      domains=["intelligence_education", "wealth", "spirituality"],
      predictions=[
          {"entity": "native", "claim": "learned_and_wealthy_gnana_yoga", "domain": "intelligence_education", "direction": "favorable", "magnitude": 0.8},
          {"entity": "native", "claim": "spiritually_and_materially_wealthy", "domain": "spirituality", "direction": "favorable", "magnitude": 0.7},
      ],
      verse_ref="Ch.21 v.12",
      commentary_context="Santhanam: 'Gnan' = sacred knowledge from meditation/philosophy. Gnana yoga taught by Jupiter+Venus in Pisces. The ascendant lord + exalted Moon renders mind fertile for self-knowledge. Material wealth comes as by-product of spiritual attainment.",
      description="Jupiter in Pisces + Venus + strong ascendant lord + Moon exalted: Gnana Yoga — learned, wealthy.",
      modifiers=[{"condition": "jupiter_in_pisces", "effect": "conditionalizes", "strength": "strong"},
                 {"condition": "venus_conjunct_asc_lord_strong_moon_exalted", "effect": "amplifies", "strength": "strong"}])

# ═══ v.13: Precious stones ═══════════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 11},
                   {"type": "planet_in_house", "planet": "Venus", "house": 10}],
      signal_group="h10_h11_venus_precious_stones", direction="favorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "endowed_with_precious_stones", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.13",
      commentary_context="Santhanam: Planets so disposed confer a huge influx of material wealth on the native.",
      description="10th lord in 11th + 11th lord in ascendant + Venus in 10th: endowed with precious stones.")

# ═══ v.14: Worthy deeds ══════════════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": [1, 4, 5, 7, 9, 10]},
                   {"type": "planet_dignity", "planet": "lord_of_10", "dignity": "exalted"}],
      signal_group="h10_lord_exalted_jupiter_worthy", direction="favorable", intensity="strong",
      domains=["character_temperament", "spirituality"],
      predictions=[{"entity": "native", "claim": "endowed_with_worthy_deeds", "domain": "character_temperament", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.14",
      commentary_context="No separate note. Exalted 10th lord + Jupiter in kendra/trikona = dharmic and meritorious professional actions.",
      description="10th lord exalted in angle/trine + company/aspect of Jupiter: worthy deeds.",
      concordance_texts=["Saravali"])

# ═══ v.15: Good deeds ════════════════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 1}],
      signal_group="h10_lord_h1_good_deeds", direction="favorable", intensity="moderate",
      domains=["character_temperament"],
      predictions=[{"entity": "native", "claim": "interested_in_good_deeds", "domain": "character_temperament", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.21 v.15",
      commentary_context="No separate note. 10th lord in ascendant + ascendant lord + Moon in kendra/trikona = emotional investment in virtuous actions.",
      description="10th lord in ascendant + ascendant lord + Moon in angle/trine: interested in good deeds.",
      modifiers=[{"condition": "ascendant_lord_with_moon_in_kendra_trikona", "effect": "amplifies", "strength": "moderate"}])

# ═══ v.16: Bereft of virtuous acts ═══════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 10}],
      signal_group="saturn_h10_no_virtue", direction="unfavorable", intensity="moderate",
      domains=["character_temperament"],
      predictions=[{"entity": "native", "claim": "bereft_of_virtuous_acts", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.21 v.16",
      commentary_context="No separate note. Saturn + debilitated planet + Navamsa malefic = triple block on dharmic professional conduct.",
      description="Saturn in 10th + debilitated planet + Navamsa ascendant with malefic: bereft of virtuous acts.",
      modifiers=[{"condition": "conjunct_debilitated_planet", "effect": "negates", "strength": "moderate"},
                 {"condition": "navamsa_ascendant_with_malefic", "effect": "amplifies", "strength": "moderate"}])

# ═══ v.17: Bad acts — 8th-10th exchange ══════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 8},
                   {"type": "lord_in_house", "lord_of": 8, "house": 10}],
      signal_group="h10_h8_exchange_bad_acts", direction="unfavorable", intensity="strong",
      domains=["character_temperament", "career_status"],
      predictions=[{"entity": "native", "claim": "indulge_in_bad_acts_career_scandals", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.17",
      commentary_context="No separate note. 8th-10th exchange brings hidden/destructive tendencies into professional sphere.",
      description="10th lord in 8th + 8th lord in 10th with malefic: indulge in bad acts.")

# ═══ v.18: Obstructions ══════════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_10", "dignity": "debilitated"}],
      signal_group="h10_lord_fall_obstruction", direction="unfavorable", intensity="strong",
      domains=["career_status"],
      predictions=[{"entity": "native", "claim": "obstructions_career_completely_blocked", "domain": "career_status", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.18",
      commentary_context="No separate note. 10th lord in fall + malefics in 10th from both ascendant and 10th = career blocked from multiple directions.",
      description="10th lord in fall + both 10th from ascendant and 10th from 10th have malefics: obstructions.",
      modifiers=[{"condition": "h10_from_both_asc_and_10th_with_malefics", "effect": "amplifies", "strength": "moderate"}])

# ═══ v.19: Fame — Moon in 10th ═══════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 10}],
      signal_group="moon_h10_fame_1", direction="favorable", intensity="strong",
      domains=["fame_reputation"],
      predictions=[{"entity": "native", "claim": "endowed_with_fame_public_visibility", "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.19",
      commentary_context="Santhanam: First of three fame yogas (v.19-21). Moon in 10th = public visibility + 10th lord in trine + ascendant lord in kendra = lasting renown.",
      description="Moon in 10th + 10th lord in trine + ascendant lord in angle: endowed with fame.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "h10_lord_in_trikona", "effect": "amplifies", "strength": "moderate"},
                 {"condition": "ascendant_lord_in_kendra", "effect": "amplifies", "strength": "moderate"}])

# ═══ v.20: Fame — 11th lord in 10th ══════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 10}],
      signal_group="h11_lord_h10_fame_2", direction="favorable", intensity="strong",
      domains=["fame_reputation", "career_status"],
      predictions=[{"entity": "native", "claim": "fame_through_professional_achievement", "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.20",
      commentary_context="Santhanam: Second fame yoga. 11th lord in 10th + 10th lord strong + Jupiter aspect = recognition through professional achievement.",
      description="11th lord in 10th + 10th lord strong + aspected by Jupiter: fame.",
      modifiers=[{"condition": "h10_lord_strong_aspected_by_jupiter", "effect": "amplifies", "strength": "strong"}])

# ═══ v.21: Fame — 10th lord in 9th ═══════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 9}],
      signal_group="h10_lord_h9_fame_3", direction="favorable", intensity="strong",
      domains=["fame_reputation"],
      predictions=[{"entity": "native", "claim": "fame_through_dharma_karma_connection", "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.21",
      commentary_context="Santhanam: Third fame yoga. 10th lord in 9th + ascendant lord in 10th + Moon in 5th = dharma-karma connection + purva punya = lasting renown.",
      description="10th lord in 9th + ascendant lord in 10th + Moon in 5th: fame.",
      modifiers=[{"condition": "ascendant_lord_in_10th", "effect": "amplifies", "strength": "moderate"},
                 {"condition": "moon_in_5th_house_completes_dharma_karma_triple_combination", "effect": "amplifies", "strength": "moderate"}])

BPHS_V2_CH21_REGISTRY = b.build()
