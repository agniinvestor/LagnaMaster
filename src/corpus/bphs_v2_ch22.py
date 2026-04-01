"""src/corpus/bphs_v2_ch22.py — BPHS Ch.22 (11th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.183-186. Slokas: 11. Gains/Nishka timing.
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(chapter="Ch.22", category="11th_house_effects", id_start=2200, session="S311", sloka_count=11,
                      chapter_tags=["11th_house", "labha_bhava"], entity_target="native")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": [1, 4, 5, 7, 9, 10, 11]}],
      signal_group="h11_lord_kendra_gains", direction="favorable", intensity="strong", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "many_gains", "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.22 v.2", commentary_context="Santhanam: Even combust 11th lord in exaltation = abundant gains. Exaltation overrides combustion.", description="11th lord in 11th or angle/trine: many gains. Even if combust but exalted → abundant gains.",
      concordance_texts=["Saravali"], rule_relationship={"type": "alternative", "related_rules": ["BPHS2207"]})

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 3}],
      signal_group="h11_lord_h3_2000_nishkas_36", direction="favorable", intensity="moderate", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "gain_2000_nishkas_at_36", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
      timing_window={"type": "age", "value": 36, "precision": "approximate"},
      verse_ref="Ch.22 v.4", description="11th lord in 3rd + 11th occupied by benefic: 2000 Nishkas in 36th year.",
      commentary_context="Nishka = gold coin, one Karsha or Suvarna of 16 Mashas. Indicates opulence level.")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": [1, 4, 5, 7, 9, 10]}],
      signal_group="h11_lord_kendra_500_nishkas_40", direction="favorable", intensity="moderate", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "acquire_500_nishkas_at_40", "domain": "wealth", "direction": "favorable", "magnitude": 0.5}],
      timing_window={"type": "age", "value": 40, "precision": "approximate"},
      verse_ref="Ch.22 v.5", commentary_context="No separate note. 11th lord + benefic in kendra/trikona = moderate gains at age 40.", description="11th lord conjunct benefic in angle/trine: 500 Nishkas at 40th year.",
      modifiers=[{"condition": "conjunct_benefic", "effect": "conditionalizes", "strength": "moderate"}])

b.add(conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 11}],
      signal_group="jupiter_h11_6000_nishkas", direction="favorable", intensity="strong", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "own_6000_nishkas", "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.22 v.6", commentary_context="No separate note. Three natural benefics in wealth(2nd)/fortune(9th)/gains(11th) = extraordinary dhana yoga.", description="Jupiter in 11th + 2nd by Moon + 9th by Venus: 6000 Nishkas.",
      modifiers=[{"condition": "moon_in_2nd_house_additional_benefic_in_wealth_house", "effect": "conditionalizes", "strength": "moderate"},
                 {"condition": "venus_in_9th_house_additional_benefic_in_fortune_house", "effect": "conditionalizes", "strength": "moderate"}])

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 1},
                   {"type": "lord_in_house", "lord_of": 1, "house": 11}],
      signal_group="h11_h1_exchange_1000_nishkas_33", direction="favorable", intensity="strong", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "gain_1000_nishkas_at_33", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      timing_window={"type": "age", "value": 33, "precision": "approximate"},
      verse_ref="Ch.22 v.8", commentary_context="No separate note. 11th-1st parivartana links personality with gains at age 33.", description="11th lord in ascendant + ascendant lord in 11th: 1000 Nishkas at 33rd year.")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 2},
                   {"type": "lord_in_house", "lord_of": 2, "house": 11}],
      signal_group="h11_h2_exchange_after_marriage", direction="favorable", intensity="moderate", domains=["wealth", "marriage"],
      predictions=[{"entity": "native", "claim": "abundant_fortunes_after_marriage", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
      timing_window={"type": "after_event", "value": "marriage", "precision": "approximate"},
      verse_ref="Ch.22 v.9", commentary_context="No separate note. 2nd-11th exchange ties wealth accumulation to marriage partnership.", description="11th lord in 2nd + 2nd lord in 11th: abundant fortunes after marriage.")

b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": [6, 8, 12]}],
      signal_group="h11_lord_dusthana_no_gains", direction="unfavorable", intensity="strong", domains=["wealth"],
      predictions=[{"entity": "native", "claim": "no_gains_despite_efforts", "domain": "wealth", "direction": "unfavorable", "magnitude": 0.8}],
      verse_ref="Ch.22 v.11", commentary_context="Santhanam: Dusthana placement + fall/combustion + malefic = complete blockage of gains despite efforts.", description="11th lord in fall/combustion or 6/8/12 with malefic: no gains despite numerous efforts.",
      concordance_texts=["Saravali"], rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2200"]})


# ═══ v.3: Great gains through 2nd-11th-Jupiter ═══════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 2}],
      signal_group="h11_lord_h2_jupiter_great_gains", direction="favorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "gains_will_be_great_through_wealth_houses", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.22 v.3",
      commentary_context="Santhanam: 11th lord in 2nd + 2nd lord in angle from ascendant + Jupiter = great gains. Two wealth houses connected with Jupiter amplification.",
      description="11th lord in 2nd + 2nd lord in angle + Jupiter: gains will be great.",
      modifiers=[{"condition": "h2_lord_in_kendra_with_jupiter", "effect": "amplifies", "strength": "strong"}])

# ═══ v.7: Jupiter+Mercury+Moon in 11th → diamonds ════════════════════════════
b.add(conditions=[{"type": "planets_conjunct_in_house", "planets": ["Jupiter", "Mercury", "Moon"], "house": 11}],
      signal_group="jupiter_mercury_moon_h11_diamonds", direction="favorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "wealth_grains_fortunes_diamonds_ornaments", "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.22 v.7",
      commentary_context="Santhanam: Jupiter, Mercury and Moon in 11th (9th from ascendant) = wealth, grains, fortunes, diamonds and ornaments. Three benefics in gains house.",
      description="Jupiter, Mercury and Moon in 11th: wealth, grains, fortunes, diamonds, ornaments.")

# ═══ v.10: 3rd-11th exchange → co-born wealth ════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 11, "house": 3},
                   {"type": "lord_in_house", "lord_of": 3, "house": 11}],
      signal_group="h11_h3_exchange_coborn_wealth", direction="favorable", intensity="moderate",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "wealth_through_siblings_excellent_ornaments", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.22 v.10",
      commentary_context="No separate note. 3rd-11th exchange connects initiative and siblings with the house of gains.",
      description="11th lord in 3rd + 3rd lord in 11th: wealth through co-born, excellent ornaments.")

BPHS_V2_CH22_REGISTRY = b.build()
