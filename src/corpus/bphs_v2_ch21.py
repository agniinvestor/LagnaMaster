"""src/corpus/bphs_v2_ch21.py — BPHS Ch.21 (10th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.178-183. Slokas: 22. Career/fame chapter.
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(chapter="Ch.21", category="10th_house_effects", id_start=2100, session="S311", sloka_count=22,
                      chapter_tags=["10th_house", "karma_bhava"], entity_target="native")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": "any"},
                   {"type": "planet_dignity", "planet": "lord_of_10", "dignity": "strong"}],
      signal_group="h10_lord_strong_paternal_fame", direction="favorable", intensity="strong",
      domains=["career_status", "fame_reputation"],
      predictions=[{"entity": "native", "claim": "paternal_happiness_fame_good_deeds", "domain": "career_status", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.21 v.2", description="10th lord strong in exaltation or own Rasi/Navamsa: paternal happiness, fame and good deeds.",
      concordance_texts=["Saravali"], rule_relationship={"type": "alternative", "related_rules": ["BPHS2101"]})

b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": "any"},
                   {"type": "planet_dignity", "planet": "lord_of_10", "dignity": "weak"}],
      signal_group="h10_lord_weak_career_obstruction", direction="unfavorable", intensity="moderate",
      domains=["career_status"],
      predictions=[{"entity": "native", "claim": "obstructions_in_work", "domain": "career_status", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.3", description="10th lord devoid of strength: obstructions in work.", concordance_texts=["Saravali"],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2100"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 10},
                   {"type": "planet_in_house", "planet": "any_malefic", "house": 11}],
      signal_group="malefics_h10_h11_bad_deeds", direction="unfavorable", intensity="moderate",
      domains=["character_temperament", "career_status"],
      predictions=[{"entity": "native", "claim": "indulge_in_bad_deeds_defile_own_men", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.21 v.5", description="10th and 11th both occupied by malefics: bad deeds, defile his own men.")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 10, "house": 8},
                   {"type": "planet_in_house", "planet": "Rahu", "house": 8}],
      signal_group="h10_lord_h8_rahu_fool", direction="unfavorable", intensity="strong",
      domains=["intelligence_education", "character_temperament"],
      predictions=[{"entity": "native", "claim": "great_fool_bad_deeds", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.6", description="10th lord in 8th with Rahu: great fool, bad deeds.",
      commentary_context="Rahu in 8th with 10th lord spoils professional happiness and leads to questionable actions.")

b.add(conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 12}],
      signal_group="jupiter_pisces_venus_gnana_yoga", direction="favorable", intensity="strong",
      domains=["intelligence_education", "wealth", "spirituality"],
      predictions=[{"entity": "native", "claim": "learned_and_wealthy_gnana_yoga", "domain": "intelligence_education", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.21 v.12", description="Jupiter in Pisces + Venus + ascendant lord strong + Moon exalted: Gnana Yoga — learned and wealthy.",
      commentary_context="Gnana yoga: supreme knowledge from meditation and philosophy. Material wealth as by-product of spiritual attainment.",
      modifiers=[{"condition": "jupiter_in_pisces", "effect": "conditionalizes", "strength": "strong"},
                 {"condition": "conjunct_venus_asc_lord_strong_moon_exalted", "effect": "amplifies", "strength": "strong"}])

b.add(conditions=[{"type": "planet_in_house", "planet": "Moon", "house": 10}],
      signal_group="moon_h10_fame", direction="favorable", intensity="strong",
      domains=["fame_reputation"],
      predictions=[{"entity": "native", "claim": "endowed_with_fame", "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.21 v.19", description="Moon in 10th + 10th lord in trine + ascendant lord in angle: fame.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "h10_lord_in_trikona", "effect": "amplifies", "strength": "moderate"},
                 {"condition": "ascendant_lord_in_kendra", "effect": "amplifies", "strength": "moderate"}])

BPHS_V2_CH21_REGISTRY = b.build()
