"""src/corpus/bphs_v2_ch23.py — BPHS Ch.23 (12th House Effects) V2 Re-encode.

Source: R. Santhanam, BPHS Vol 1, pp.186-189. Slokas: 14. Moksha/expenses/foreign.
"""
from __future__ import annotations
from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(chapter="Ch.23", category="12th_house_effects", id_start=2300, session="S311", sloka_count=14,
                      chapter_tags=["12th_house", "vyaya_bhava"], entity_target="native")

b.add(conditions=[{"type": "planet_dignity", "planet": "lord_of_12", "dignity": "strong"}],
      signal_group="h12_lord_strong_good_expenses", direction="favorable", intensity="moderate",
      primary_domain="wealth",
      predictions=[{"entity": "native", "claim": "expenses_on_good_accounts_beautiful_houses", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.1-4", commentary_context="Santhanam: 12th lord well-placed channels expenditure toward luxury and comfort rather than loss. Moon as 12th lord exalted = rich clothes.", description="12th lord with benefic or in own house or exalted: expenses on good accounts, beautiful houses, scented articles.",
      concordance_texts=["Saravali"])

b.add(conditions=[{"type": "lord_in_house", "lord_of": 12, "house": [6, 8]}],
      signal_group="h12_lord_dusthana_devoid_happiness", direction="unfavorable", intensity="moderate",
      primary_domain="relationships",
      predictions=[{"entity": "native", "claim": "devoid_of_happiness_from_wife_troubled_expenses", "domain": "relationships", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.5-6", commentary_context="Santhanam: 12th lord in dusthana compounds loss. In kendra/trikona = bed pleasures manifest as happy marriage.", description="12th lord in 6th/8th or debilitation Navamsa: devoid of happiness from wife, troubled by expenses.",
      concordance_texts=["Saravali"])

b.add(conditions=[{"type": "planet_in_house", "planet": "Rahu", "house": 12},
                   {"type": "planet_in_house", "planet": "Mars", "house": 12},
                   {"type": "planet_in_house", "planet": "Saturn", "house": 12},
                   {"type": "planet_in_house", "planet": "Sun", "house": 12}],
      signal_group="rahu_mars_saturn_h12_hell", direction="unfavorable", intensity="strong",
      primary_domain="spirituality",
      predictions=[{"entity": "native", "claim": "severe_karmic_consequences_hell", "domain": "spirituality", "direction": "unfavorable", "magnitude": 0.8}],
      verse_ref="Ch.23 v.9", commentary_context="Santhanam: The 12th house relates to fate after death — whether reincarnation or attaining Lotus Feet of the Lord. Four malefics there deny moksha.", description="Rahu + Mars + Saturn + Sun in 12th + 12th lord with Sun: native will go to hell.")

b.add(conditions=[{"type": "planet_in_house", "planet": "any_benefic", "house": 12},
                   {"type": "planet_dignity", "planet": "any_benefic", "dignity": "exalted"}],
      signal_group="benefic_h12_exalted_moksha", direction="favorable", intensity="strong",
      primary_domain="spirituality",
      predictions=[{"entity": "native", "claim": "attain_final_emancipation_moksha", "domain": "spirituality", "direction": "favorable", "magnitude": 0.8}],
      verse_ref="Ch.23 v.10", commentary_context="Santhanam: Benefic exalted in 12th = moksha. NOTE: both conditions must be satisfied by the SAME benefic planet (same-planet constraint). Current encoding approximates this as any_benefic in 12th AND any_benefic exalted — which could match two different benefics. Pending same-planet constraint primitive.", description="Benefic in 12th exalted or conjunct/aspected by benefic: one will attain final emancipation (moksha).",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2302"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "any_malefic", "house": 12}],
      signal_group="h12_lord_malefic_wandering", direction="unfavorable", intensity="moderate",
      primary_domain="career",
      predictions=[{"entity": "native", "claim": "wander_from_country_to_country", "domain": "career", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.11", commentary_context="Santhanam: If 12th lord and house spoilt by malefics, native wanders. If connected with benefics, stays in own place.", description="12th lord and 12th house with malefics and aspected by malefics: wander from country to country.",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "alternative", "related_rules": ["BPHS2305"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "any_benefic", "house": 12}],
      signal_group="h12_lord_benefic_own_country", direction="favorable", intensity="moderate",
      primary_domain="wealth",
      predictions=[{"entity": "native", "claim": "move_in_own_country_progress", "domain": "wealth", "direction": "favorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.12", commentary_context="Contrary of BPHS2304 (wandering). Benefic influence on 12th house = local establishment rather than displacement.", description="12th lord and 12th with benefics: one will move in his own country and progress in his own place.",
      concordance_texts=["Saravali"],
      rule_relationship={"type": "contrary_mirror", "related_rules": ["BPHS2304"]})

b.add(conditions=[{"type": "planet_in_house", "planet": "Saturn", "house": 12}],
      signal_group="saturn_h12_sinful_earnings", direction="unfavorable", intensity="moderate",
      primary_domain="character",
      predictions=[{"entity": "native", "claim": "earnings_through_sinful_measures", "domain": "character", "direction": "unfavorable", "magnitude": 0.6}],
      verse_ref="Ch.23 v.13", commentary_context="No separate note. Malefic 12th without benefic aspect = income through unethical means.", description="12th occupied by Saturn/Mars + not aspected by benefic: earnings through sinful measures.",
      concordance_texts=["Saravali"],
      modifiers=[{"condition": "not_aspected_by_benefic", "effect": "attenuates", "target": "prediction", "strength": "medium", "scope": "local"}],
      rule_relationship={"type": "addition", "related_rules": ["BPHS2304"]})

b.add(conditions=[{"type": "lord_in_house", "lord_of": 1, "house": 12},
                   {"type": "planet_in_house", "planet": "Venus", "house": 12}],
      signal_group="lagna_lord_venus_h12_religious_expense", direction="favorable", intensity="moderate",
      primary_domain="spirituality",
      predictions=[{"entity": "native", "claim": "expenses_on_religious_grounds", "domain": "spirituality", "direction": "favorable", "magnitude": 0.5}],
      verse_ref="Ch.23 v.14", commentary_context="No separate note. Venus in 12th = one of Venus's best placements (bed pleasures, luxury). Combined with lagna lord = dharmic spending.", description="Ascendant lord in 12th + Venus in 12th: expenses on religious grounds.")


# ═══ v.7: Bhavat bhavam principle for relatives ══════════════════════════════
b.add(conditions=[],
      signal_group="bhavat_bhavam_relatives_principle", direction="neutral", intensity="moderate",
      primary_domain="progeny",
      predictions=[{"entity": "general", "claim": "predict_relative_events_from_derived_houses", "domain": "progeny", "direction": "neutral", "magnitude": 0.5}],
      entity_target="general",
      verse_ref="Ch.23 v.7",
      commentary_context="Santhanam: Hints for co-born, uncles etc. Brother\'s finances = 4th (2nd from 3rd). Brother\'s marriage = 9th (7th from 3rd). Father\'s health = 2nd (6th from 9th). Mother\'s health = 9th (6th from 4th). Wife\'s spending = 6th (12th from 7th). Proceeding on these lines, we can predict events for all relatives from the native\'s horoscope.",
      description="Effects derived from ascendant apply similarly to co-born (3rd), mother (4th), etc. through bhavat bhavam.",
      cross_chapter_refs=["Ch.14 (siblings)", "Ch.15 (mother)", "Ch.18 (spouse)", "Ch.20 (father)"],
      prediction_type="trait")

# ═══ v.8: Visible vs invisible half ══════════════════════════════════════════
b.add(conditions=[],
      signal_group="visible_invisible_half_principle", direction="neutral", intensity="moderate",
      primary_domain="career",
      predictions=[{"entity": "native", "claim": "visible_half_explicit_results_invisible_secret", "domain": "career", "direction": "neutral", "magnitude": 0.4}],
      entity_target="native",
      verse_ref="Ch.23 v.8",
      commentary_context="Santhanam: Visible half = 180 degrees from ascendant cusp backwards (via 10th cusp). A planet in visible half has more potential in effects — results are manifest and publicly recognized. Invisible half = less potential, unmanifest.",
      description="Planets in visible half of zodiac give explicit results; invisible half gives secret results.",
      prediction_type="trait")

BPHS_V2_CH23_REGISTRY = b.build()
