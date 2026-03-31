"""src/corpus/bphs_v2_ch23.py — BPHS Ch.23 (12th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.186-189. Slokas: 14. Moksha/expenses/foreign.
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(chapter="Ch.23", category="12th_house_effects", id_start=2300, session="S311",
                      chapter_tags=["12th_house", "vyaya_bhava"], entity_target="native")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 12, "house": "any"},
                   {"type": "planet_dignity", "planet": "lord_of_12", "dignity": "strong"}],
      signal_group="h12_lord_strong_good_expenses", direction="favorable", intensity="moderate",
      domains=["wealth", "property_vehicles"],
      predictions=[{"entity": "native", "claim": "expenses_on_good_accounts_beautiful_houses", "domain": "property_vehicles", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.1-4", description="12th lord with benefic or in own house or exalted: expenses on good accounts, beautiful houses, scented articles.",
      concordance_texts=["Saravali"])

b.add(conditions=[{"type": "lord_in_house", "lord_of": 12, "house": [6, 8]}],
      signal_group="h12_lord_dusthana_devoid_happiness", direction="unfavorable", intensity="moderate",
      domains=["marriage", "wealth"],
      predictions=[{"entity": "native", "claim": "devoid_of_happiness_from_wife_troubled_expenses", "domain": "marriage", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.5-6", description="12th lord in 6th/8th or debilitation Navamsa: devoid of happiness from wife, troubled by expenses.",
      concordance_texts=["Saravali"])

b.add(conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": 12},
                   {"type": "planet_in_house", "planet": "Mars", "house": 12},
                   {"type": "planet_in_house", "planet": "Saturn", "house": 12}],
      signal_group="rahu_mars_saturn_h12_hell", direction="unfavorable", intensity="strong",
      domains=["spirituality", "character_temperament"],
      predictions=[{"entity": "native", "claim": "severe_karmic_consequences_hell", "domain": "spirituality", "direction": "unfavorable", "magnitude": 0.8}],
      verse_ref="Ch.23 v.9", description="Rahu + Mars + Saturn + Sun in 12th + 12th lord with Sun: native will go to hell.",
      commentary_context="The 12th house governs final emancipation. Four malefics there deny moksha and indicate severe post-mortem suffering.")

b.add(conditions=[{"type": "planet_in_house", "planet": "any_benefic", "house": 12},
                   {"type": "planet_dignity", "planet": "any_benefic", "dignity": "exalted"}],
      signal_group="benefic_h12_exalted_moksha", direction="favorable", intensity="strong",
      domains=["spirituality"],
      predictions=[{"entity": "native", "claim": "attain_final_emancipation_moksha", "domain": "spirituality", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.23 v.10", description="Benefic in 12th exalted or conjunct/aspected by benefic: one will attain final emancipation (moksha).",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2302"]})

b.add(conditions=[{"type": "lord_in_house", "lord_of": 12, "house": "any"}],
      signal_group="h12_lord_malefic_wandering", direction="unfavorable", intensity="moderate",
      domains=["foreign_travel"],
      predictions=[{"entity": "native", "claim": "wander_from_country_to_country", "domain": "foreign_travel", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.11", description="12th lord and 12th house with malefics and aspected by malefics: wander from country to country.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "h12_and_lord_with_malefics", "effect": "conditionalizes", "strength": "moderate"}],
      rule_relationship={"type": "alternative", "related_rules": ["BPHS2305"]})

b.add(conditions=[{"type": "lord_in_house", "lord_of": 12, "house": "any"}],
      signal_group="h12_lord_benefic_own_country", direction="favorable", intensity="moderate",
      domains=["property_vehicles"],
      predictions=[{"entity": "native", "claim": "move_in_own_country_progress", "domain": "property_vehicles", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.12", description="12th lord and 12th with benefics: one will move in his own country and progress in his own place.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "h12_and_lord_with_benefics", "effect": "conditionalizes", "strength": "moderate"}],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2304"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 12}],
      signal_group="saturn_h12_sinful_earnings", direction="unfavorable", intensity="moderate",
      domains=["wealth", "character_temperament"],
      predictions=[{"entity": "native", "claim": "earnings_through_sinful_measures", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.13", description="12th occupied by Saturn/Mars + not aspected by benefic: earnings through sinful measures.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "not_aspected_by_benefic", "effect": "amplifies", "strength": "moderate"}])

b.add(conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 12},
                   {"type": "planet_in_house", "planet": "Venus", "house": 12}],
      signal_group="lagna_lord_venus_h12_religious_expense", direction="favorable", intensity="moderate",
      domains=["spirituality", "wealth"],
      predictions=[{"entity": "native", "claim": "expenses_on_religious_grounds", "domain": "spirituality", "direction": "favorable", "magnitude": 0.5}],
      verse_ref="Ch.23 v.14", description="Ascendant lord in 12th + Venus in 12th: expenses on religious grounds.")

BPHS_V2_CH23_REGISTRY = b.build()
