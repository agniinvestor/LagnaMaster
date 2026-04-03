"""src/corpus/bphs_v2_ch20.py — BPHS Ch.20 (9th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.172-178.
Chapter: 20 — Effects of the Ninth House (Dharma Bhava Phala)
Slokas: 32. Father-heavy chapter. v.13-25 = father death timing (12+ specific ages).
Entity: father (most), native (fortune/dharma rules).
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.20", category="9th_house_effects",
    id_start=2000, session="S311", sloka_count=32,
    chapter_tags=["9th_house", "dharma_bhava"],
    entity_target="native",
)

# ═══ v.1-2: Fortune combinations ═════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 9},
                   {"type": "planet_dignity", "planet": "lord_of_9", "dignity": "strong"}],
      signal_group="h9_lord_strong_h9_fortune", direction="favorable", intensity="strong",
      domains=["wealth", "spirituality"],
      predictions=[{"entity": "native", "claim": "fortunate_and_affluent", "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.20 v.1-2", commentary_context="Santhanam: Bhagyasthana = fortune. One's capacity to retain wealth should be studied from 9th house.", description="9th lord with strength in the 9th: fortunate and affluent.",
      concordance_texts=["Saravali", "Phaladeepika"])

b.add(conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 9},
                  {"type": "lord_in_house", "lord_of": 9, "house": [1, 4, 7, 10]}],
      signal_group="jupiter_h9_fortune", direction="favorable", intensity="strong",
      domains=["wealth", "spirituality", "fame_reputation"],
      predictions=[{"entity": "native", "claim": "extremely_fortunate", "domain": "wealth", "direction": "favorable", "magnitude": 0.9}],
      verse_ref="Ch.20 v.2", commentary_context="Santhanam: Triple combination — Jupiter + 9th lord kendra + strong ascendant lord = highest grade of fortune.", description="Jupiter in 9th + 9th lord in angle + ascendant lord strong: extremely fortunate.",
      concordance_texts=["Saravali"])

# ═══ v.3: Fortunate father ═══════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "strong"}],
      entity_target="father", signal_group="h9_lord_strong_father_fortunate",
      direction="favorable", intensity="strong", domains=["wealth"],
      predictions=[{"entity": "father", "claim": "father_is_fortunate_affluent", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.20 v.3", commentary_context="No separate note. Venus + Jupiter supporting 9th house ensure father's wealth.", description="9th lord with strength + Venus in 9th + Jupiter in kendra: father fortunate.",
      derived_house_chains=[{"base_house": 9, "derivative": "self", "effective_house": 9, "entity": "father", "domain": "wealth"}])

# ═══ v.4: Indigent father ════════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"}],
      entity_target="father", signal_group="h9_lord_debilitated_father_poor",
      direction="unfavorable", intensity="moderate", domains=["wealth"],
      predictions=[{"entity": "father", "claim": "father_is_poor", "domain": "wealth", "direction": "unfavorable", "magnitude": 0.7}],
      verse_ref="Ch.20 v.4", description="9th lord debilitated: father is poor. Mars in 10th/12th (not own/exaltation) → patrimony lost through litigation.",
      commentary_context="Mars in 10th or 12th = 2nd or 4th from 9th. Patrimony will not come to hands easily.",
      derived_house_chains=[{"base_house": 9, "derivative": "2nd_from", "effective_house": 10, "entity": "father", "domain": "wealth"}],
      concordance_texts=["Saravali"], exceptions=["if_neecha_bhanga_raja_yoga"])

# ═══ v.5: Long-living father ═════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "exalted"}],
      entity_target="father", signal_group="h9_lord_exalted_father_long_life",
      direction="favorable", intensity="strong", domains=["longevity"],
      predictions=[{"entity": "father", "claim": "father_enjoys_long_life", "domain": "longevity", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.20 v.5", commentary_context="Three-factor protection: exalted 9th lord + Venus kendra + Jupiter D9 confirmation.", description="9th lord in deep exaltation + Venus in angle + Jupiter 9th from D9 asc: father long-lived.")

# ═══ v.6: Royal status for father ════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 9, "house": [1, 4, 7, 10]}],
      entity_target="father", signal_group="h9_lord_kendra_father_royal",
      direction="favorable", intensity="strong", domains=["career_status", "wealth"],
      predictions=[{"entity": "father", "claim": "father_like_king_with_conveyances", "domain": "career_status", "direction": "favorable", "magnitude": 0.7}],
      verse_ref="Ch.20 v.6", commentary_context="No separate note. Kendra + Jupiter aspect = directional strength + benefic support.", description="9th lord in angle in aspect to Jupiter: father will be a king, endowed with conveyances.",
      modifiers=[{"condition": "aspecting_or_aspected_by_jupiter", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}])

# ═══ v.7: Wealthy and famous father ══════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 10}],
      entity_target="father", signal_group="h9_lord_h10_father_wealthy_famous",
      direction="favorable", intensity="strong", domains=["wealth", "fame_reputation"],
      predictions=[{"entity": "father", "claim": "father_very_rich_and_famous", "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.20 v.7", commentary_context="Santhanam: 9th-10th = dharma-karma adhipati yoga. Father benefits from elevated combination.", description="9th lord in 10th + 10th lord aspected by benefic: father very rich and famous.",
      derived_house_chains=[{"base_house": 9, "derivative": "2nd_from", "effective_house": 10, "entity": "father", "domain": "career_status"}])

# ═══ v.10: Fortune at age 32 ═════════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 2},
                   {"type": "lord_in_house", "lord_of": 2, "house": 9}],
      signal_group="h9_h2_exchange_fortune_32", direction="favorable", intensity="moderate",
      domains=["wealth", "property_vehicles", "fame_reputation"],
      predictions=[{"entity": "native", "claim": "fortune_conveyances_fame_at_32", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      timing_window={"type": "age", "value": 32, "precision": "approximate"},
      verse_ref="Ch.20 v.10", commentary_context="Santhanam: Fortune, conveyances and fame at age 32. 9th-2nd exchange links fortune with wealth.", description="9th lord in 2nd + 2nd lord in 9th: fortune, conveyances and fame at age 32.")

# ═══ v.11: Inimical to father ════════════════════════════════════════════════
b.add(conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 9},
                   {"type": "lord_in_house", "lord_of": 6, "house": 9}],
      entity_target="father", signal_group="lagna_h6_lords_h9_father_enmity",
      direction="unfavorable", intensity="moderate", domains=["character_temperament"],
      predictions=[{"entity": "father", "claim": "mutual_enmity_with_father", "domain": "character_temperament", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.20 v.11", commentary_context="No separate note. 6th lord in 9th pollutes dharma-sthana with hostility.", description="Ascendant lord in 9th + 6th lord also in 9th: mutual enmity between father and native.")

# ═══ v.13-25: FATHER DEATH TIMING — one-claim-one-rule ════════════════════════
_FATHER_DEATH = [
    ("Ch.20 v.13", "before_birth", "Sun in 6/8/12 + 8th lord in 9th + 12th lord in ascendant",
     [{"type": "planet_in_house", "planet": "Sun", "house": [6, 8, 12]}],
     {"type": "age", "value": 0, "precision": "exact"}),
    ("Ch.20 v.14", "3_or_16", "9th lord in debilitation Navamsa",
     [{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"}],
     {"type": "age_range", "value": [3, 16], "precision": "approximate"}),
    ("Ch.20 v.15", "2_or_12", "Ascendant lord in 2nd as 8th lord in 8th",
     [{"type": "lord_in_house", "lord_of": 1, "house": 2}],
     {"type": "age_range", "value": [2, 12], "precision": "approximate"}),
    ("Ch.20 v.16", "16_or_18", "Rahu in 4th from ascendant + Sun in 5th from ascendant",
     [{"type": "planet_in_house", "planet": "Rahu", "house": 4}, {"type": "planet_in_house", "planet": "Sun", "house": 5}],
     {"type": "age_range", "value": [16, 18], "precision": "approximate"}),
    ("Ch.20 v.17", "44", "Saturn in 9th from 9th + Moon with Sun and Rahu",
     [{"type": "planet_in_house", "planet": "Saturn", "house": 5}],
     {"type": "age", "value": 44, "precision": "approximate"}),
    ("Ch.20 v.18", "35_or_41", "Moon in Sun's Navamsa",
     [{"type": "planet_in_house", "planet": "Moon", "house": "any"}],
     {"type": "age_range", "value": [35, 41], "precision": "approximate"}),
    ("Ch.20 v.19", "50", "Sun as lord of 9th conjunct Mars and Saturn",
     [{"type": "planets_conjunct", "planets": ["Sun", "Mars", "Saturn"]}],
     {"type": "age", "value": 50, "precision": "approximate"}),
    ("Ch.20 v.20", "26_or_30", "9th lord in debilitation + dispositor in 9th",
     [{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"}],
     {"type": "age_range", "value": [26, 30], "precision": "approximate"}),
    ("Ch.20 v.21", "6_or_25", "Saturn in 7th from 8th (= 2nd from ascendant)",
     [{"type": "planet_in_house", "planet": "Saturn", "house": 2}],
     {"type": "age_range", "value": [6, 25], "precision": "approximate"}),
    ("Ch.20 v.22", "30_21_26", "Sun in 7th from Saturn (= 8th from ascendant)",
     [{"type": "planet_in_house", "planet": "Sun", "house": 8}],
     {"type": "age_range", "value": [21, 30], "precision": "approximate"}),
]

for vref, age_label, desc_suffix, conds, tw in _FATHER_DEATH:
    b.add(
        conditions=conds,
        entity_target="father",
        signal_group=f"father_death_{age_label}",
        direction="unfavorable", intensity="strong",
        domains=["longevity"],
        predictions=[{"entity": "father", "claim": f"father_death_at_{age_label}",
                      "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
        timing_window=tw,
        verse_ref=vref,
        commentary_context=f"Santhanam groups v.13-25 as COMBINATIONS FOR FATHER'S DEATH. Each sloka gives specific ages based on different planetary configurations. Age {age_label} indicated by: {desc_suffix}.",
        description=f"Father death timing: {desc_suffix} → father passes at native's age {age_label}.",
        derived_house_chains=[{"base_house": 9, "derivative": "8th_from", "effective_house": 4, "entity": "father", "domain": "longevity"}],
    )

# ═══ v.26-28: Fortune timing ═════════════════════════════════════════════════
b.add(conditions=[{"type": "planet_in_house", "planet": "Jupiter", "house": 9}],
      signal_group="jupiter_h9_fortune_after_20", direction="favorable", intensity="moderate",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "abundant_fortunes_after_20", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      timing_window={"type": "age", "value": 20, "precision": "approximate"},
      verse_ref="Ch.20 v.27", commentary_context="Santhanam: Abundant fortunes after 20th year. Time-activated wealth combination.", description="Jupiter in 9th + lord's dispositor in kendra: abundant fortunes after 20th year.",
      concordance_texts=["Saravali"])

b.add(conditions=[{"type": "planet_in_house", "planet": "Mercury", "house": 9},
                   {"type": "planet_dignity", "planet": "Mercury", "dignity": "exalted"}],
      signal_group="mercury_h9_exalted_fortune_36", direction="favorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "abundant_fortunes_after_36", "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
      timing_window={"type": "age", "value": 36, "precision": "approximate"},
      verse_ref="Ch.20 v.28", commentary_context="Santhanam: Mercury exalted as 9th lord in 9th = fortunes after 36th year. Capricorn/Aquarius lagnas.", description="Mercury in deep exaltation as 9th lord in 9th: abundant fortunes earned after 36th year.")

# ═══ v.30: Lack of fortunes ══════════════════════════════════════════════════
b.add(conditions=[
          {"type": "planet_in_house", "planet": "Rahu", "house": 9},
          {"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"},
      ],
      signal_group="rahu_h9_no_fortune", direction="unfavorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "devoid_of_fortunes", "domain": "wealth", "direction": "unfavorable", "magnitude": 0.8}],
      verse_ref="Ch.20 v.30",
      commentary_context=(
          "Compound condition: Rahu in 9th + 9th lord in fall + Rahu's "
          "dispositor in 8th. Dispositor condition is planet-relative, "
          "kept as modifier."
      ),
      description="Rahu in 9th + 9th lord in fall + dispositor in 8th: devoid of fortunes.",
      modifiers=[{"condition": "rahus_dispositor_in_8th", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}])

# ═══ v.31: Begging ═══════════════════════════════════════════════════════════
b.add(conditions=[
          {"type": "planet_in_house", "planet": "Saturn", "house": 9},
          {"type": "planet_in_house", "planet": "Moon", "house": 9},
          {"type": "planet_dignity", "planet": "lord_of_1", "dignity": "debilitated"},
      ],
      signal_group="saturn_moon_h9_begging", direction="unfavorable", intensity="strong",
      domains=["wealth"],
      predictions=[{"entity": "native", "claim": "acquire_food_by_begging", "domain": "wealth", "direction": "unfavorable", "magnitude": 0.9}],
      verse_ref="Ch.20 v.31",
      commentary_context=(
          "Compound condition: Saturn in 9th + Moon in 9th + ascendant "
          "lord in fall. All three required for extreme poverty prediction."
      ),
      description="Saturn in 9th + Moon in 9th + ascendant lord in fall: food by begging.")

# ═══ GAP FILLS (identified by PDF-first audit 2026-04-01) ═════════════════════

# v.8 gap: Sun deep exaltation + 9th lord in 11th → virtuous, dear to king, devoted to father
b.add(
    conditions=[{"type": "planet_dignity", "planet": "Sun", "dignity": "exalted"},
                {"type": "lord_in_house", "lord_of": 9, "house": 11}],
    signal_group="sun_exalted_h9_lord_h11_virtuous",
    direction="favorable", intensity="strong", domains=["character_temperament", "fame_reputation"],
    predictions=[
        {"entity": "native", "claim": "virtuous_dear_to_king", "domain": "fame_reputation", "direction": "favorable", "magnitude": 0.7},
        {"entity": "father", "claim": "native_devoted_to_father", "domain": "character_temperament", "direction": "favorable", "magnitude": 0.6},
    ],
    entity_target="general",
    verse_ref="Ch.20 v.8-9",
    commentary_context="Sun in deep exaltation + 9th lord in 11th = native virtuous, dear to king and devoted to father.",
    description="Sun in deep exaltation + 9th lord in 11th: virtuous, dear to king, devoted to father.")

# v.9 gap: Sun in trine + 9th lord in 7th + Jupiter → devoted to father
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Sun", "house": [1, 5, 9]},
                {"type": "lord_in_house", "lord_of": 9, "house": 7}],
    entity_target="father",
    signal_group="sun_trine_h9_lord_h7_jupiter_devoted",
    direction="favorable", intensity="moderate", domains=["character_temperament"],
    predictions=[{"entity": "father", "claim": "native_devoted_to_father_sun_trine",
                  "domain": "character_temperament", "direction": "favorable", "magnitude": 0.6}],
    verse_ref="Ch.20 v.8-9",
    commentary_context="Sun in trine from ascendant + 9th lord in 7th + conjunction/aspect of Jupiter → native devoted to father.",
    description="Sun in trine + 9th lord in 7th + Jupiter conjunction/aspect: devoted to father.",
    modifiers=[{"condition": "jupiter_conjunct_or_aspecting", "effect": "amplifies", "target": "prediction", "strength": "medium", "scope": "local"}])

# v.23-25 gap: Sun in 8th + 8th lord in 9th → father dies within 1 year
b.add(
    conditions=[{"type": "planet_in_house", "planet": "Sun", "house": 8},
                {"type": "lord_in_house", "lord_of": 8, "house": 9}],
    entity_target="father",
    signal_group="sun_h8_h8_lord_h9_father_death_1yr",
    direction="unfavorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "father", "claim": "father_dies_within_1_year_of_birth",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.8}],
    timing_window={"type": "age", "value": 1, "precision": "approximate"},
    verse_ref="Ch.20 v.23-25",
    commentary_context="Distinct from v.13 (BPHS2009) which requires 12th lord in ascendant. This needs only Sun in 8th + 8th lord in 9th.",
    description="Sun in 8th + 8th lord in 9th: father dies within 1 year of native's birth.")

# v.23-25 gap: 9th-12th lord exchange → father dies at age 44
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 12},
                {"type": "lord_in_house", "lord_of": 12, "house": 9}],
    entity_target="father",
    signal_group="h9_h12_exchange_father_death_44",
    direction="unfavorable", intensity="strong", domains=["longevity"],
    predictions=[{"entity": "father", "claim": "father_dies_at_native_age_44_exchange",
                  "domain": "longevity", "direction": "unfavorable", "magnitude": 0.7}],
    timing_window={"type": "age", "value": 44, "precision": "approximate"},
    verse_ref="Ch.20 v.23-25",
    commentary_context="Second condition for age 44 (distinct from BPHS2013 which has Saturn in 5th). 9th lord in 12th + 12th lord in 9th exchange.",
    description="9th-12th lord exchange: father dies at native's age 44.")

# v.12 gap: 10th+3rd lord weak + 9th lord fall/combust → begging
b.add(
    conditions=[{"type": "planet_dignity", "planet": "lord_of_9", "dignity": "debilitated"}],
    signal_group="h10_h3_weak_h9_fall_begging",
    direction="unfavorable", intensity="strong", domains=["wealth"],
    predictions=[{"entity": "native", "claim": "go_begging_for_food",
                  "domain": "wealth", "direction": "unfavorable", "magnitude": 0.8}],
    verse_ref="Ch.20 v.12",
    commentary_context="If the 10th lord and 3rd lord are both bereft of strength while the 9th lord is in fall or in combustion, the native will go abegging for his food.",
    description="10th + 3rd lords both weak + 9th lord in fall/combustion: native begs for food.",
    modifiers=[{"condition": "h10_lord_and_h3_lord_both_weak", "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}])

# v.26 gap: Venus deep exaltation + 9th lord + Saturn in 3rd → abundant fortunes
b.add(
    conditions=[{"type": "planet_dignity", "planet": "Venus", "dignity": "exalted"},
                {"type": "planet_in_house", "planet": "Saturn", "house": 3},
                {"type": "planets_conjunct", "planets": ["Venus", "lord_of_9"]}],
    signal_group="venus_exalted_h9_lord_saturn_h3_fortune",
    direction="favorable", intensity="strong", domains=["wealth"],
    predictions=[{"entity": "native", "claim": "abundant_fortunes",
                  "domain": "wealth", "direction": "favorable", "magnitude": 0.8}],
    verse_ref="Ch.20 v.26",
    commentary_context="One will enjoy abundant fortunes if Venus is in deep exaltation and be in the company of the 9th lord as Saturn is in the 3rd.",
    description="Venus in deep exaltation + company of 9th lord + Saturn in 3rd: abundant fortunes.",
    rule_relationship={"type": "addition", "related_rules": ["BPHS2019"]},
)

# v.29 gap: 9th lord in 9th + asc lord in asc + Jupiter in 7th → wealth/conveyances
b.add(
    conditions=[{"type": "lord_in_house", "lord_of": 9, "house": 9},
                {"type": "lord_in_house", "lord_of": 1, "house": 1},
                {"type": "planet_in_house", "planet": "Jupiter", "house": 7}],
    signal_group="h9_lord_h9_asc_lord_h1_jupiter_h7_wealth",
    direction="favorable", intensity="strong", domains=["wealth", "property_vehicles"],
    predictions=[{"entity": "native", "claim": "gains_of_wealth_and_conveyances",
                  "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
    verse_ref="Ch.20 v.29",
    commentary_context="9th lord in 9th + ascendant lord in ascendant + Jupiter in 7th = gains of wealth and conveyances.",
    description="9th lord in 9th + ascendant lord in ascendant + Jupiter in 7th: gains of wealth and conveyances.")

BPHS_V2_CH20_REGISTRY = b.build()
