"""src/corpus/bphs_v2_ch31.py — BPHS Ch.31: Argala (Planetary Intervention).

S315: BPHS Phase 2 — Argala effect predictions.
Slokas 1-10: Argala formation rules (computational — NOT encoded as rules).
Slokas 11-17: Per-house Argala effects (predictive — encoded).
Sloka 18: Unobstructed Argala on ascendant/5th/9th → king.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.310-316.
Verse audit: data/verse_audits/ch31_audit.json (17 claims, 18 slokas).

ALL rules are NON-COMPUTABLE: require argala_condition primitive
(argala_on_house with type=unobstructed/obstructed/vipareeta).
The Argala formation logic (slokas 2-9) belongs in the engine layer,
not the rule corpus — same pattern as Ch.26-28.
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.31", category="argala_effects",
    id_start=3100, session="S315", sloka_count=18,
    chapter_tags=["argala", "intervention", "obstruction"],
    entity_target="native",
    prediction_type="trait",
    min_ratio=0.3,  # 8 predictive slokas from 18 total — many are computational
)


# ═══════════════════════════════════════════════════════════════════════════════
# ARGALA EFFECTS — GENERAL (Slokas 11-17, p.315)
# ALL NON-COMPUTABLE: require argala_condition primitive
# ═══════════════════════════════════════════════════════════════════════════════

# Argala for Arudha Pada + natal ascendant + 7th from both → famous + fortunate
b.add(
    conditions=[],  # NON-COMPUTABLE: needs argala_on_multiple_points(arudha, lagna, 7th)
    signal_group="argala_arudha_lagna_7th_famous_fortunate",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "famous_and_fortunate_through_argala",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.31 v.11-17",
    description="Argala for Arudha Pada, natal ascendant, and 7th from both: native will be famous and fortunate.",
    commentary_context="Santhanam: Should there be Argala for the Arudha Pada, for the natal ascendant, and for the 7th from both, the native will be famous and fortunate. This requires Argala (unobstructed intervention from 4th/2nd/11th houses) on multiple reference points simultaneously. NON-COMPUTABLE: needs argala_condition primitive with multi-point support.",
    concordance_texts=[],
)

# Benefic/malefic unobstructed Argala aspecting ascendant → famous
b.add(
    conditions=[],  # NON-COMPUTABLE: needs argala_aspecting_house(house=1, type=unobstructed)
    signal_group="argala_unobstructed_aspect_lagna_famous",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "made_famous_by_unobstructed_argala",
         "domain": "career", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.31 v.11-17",
    description="Benefic or malefic causing unobstructed Argala aspecting the ascendant: makes one famous.",
    commentary_context="Santhanam: A malefic or a benefic causing unobstructed Argala aspecting the ascendant will make one famous. NON-COMPUTABLE: needs argala_condition with aspect mode.",
    concordance_texts=[],
)

# Per-house Argala effects (12 houses)
_HOUSE_EFFECTS = [
    (2, "wealth", "acquisition_of_wealth_and_grains", "favorable", 0.7,
     "2nd house Argala: acquisition of wealth and grains."),
    (3, "relationships", "happiness_from_coborn_through_argala", "favorable", 0.7,
     "3rd house Argala: happiness from co-born."),
    (4, "wealth", "residences_quadrupeds_and_relatives", "favorable", 0.7,
     "4th house Argala: residences, quadrupeds and relatives."),
    (5, "progeny", "sons_grandsons_and_intelligence", "favorable", 0.7,
     "5th house Argala: sons, grand sons and intelligence."),
    (6, "health", "fear_from_enemies_through_argala", "unfavorable", 0.6,
     "6th house Argala: fear from enemies."),
    (7, "wealth", "abundant_wealth_and_marital_happiness", "favorable", 0.8,
     "7th house Argala: abundant wealth and marital happiness."),
    (8, "health", "difficulties_through_8th_house_argala", "unfavorable", 0.7,
     "8th house Argala: difficulties."),
    (9, "wealth", "fortunes_through_9th_house_argala", "favorable", 0.7,
     "9th house Argala: fortunes."),
    (10, "career", "royal_honour_through_10th_house_argala", "favorable", 0.8,
     "10th house Argala: royal honour."),
    (11, "wealth", "gains_through_11th_house_argala", "favorable", 0.7,
     "11th house Argala: gains."),
    (12, "wealth", "expenses_through_12th_house_argala", "unfavorable", 0.6,
     "12th house Argala: expenses."),
]

for house, domain, claim, direction, mag, desc in _HOUSE_EFFECTS:
    b.add(
        conditions=[],  # NON-COMPUTABLE: needs argala_on_house(house=N, type=unobstructed)
        signal_group=f"argala_h{house}_{domain}",
        direction=direction,
        intensity="moderate" if mag <= 0.7 else "strong",
        primary_domain=domain,
        predictions=[
            {"entity": "native", "claim": claim,
             "domain": domain, "direction": direction, "magnitude": mag},
        ],
        verse_ref="Ch.31 v.11-17",
        description=f"[BPHS — argala_effects] {desc}",
        commentary_context=f"Santhanam: Per-house Argala effect. When unobstructed Argala operates on the {house}th house (from ascendant or Arudha), the significations of that house are activated. Argala = planetary intervention from 4th/2nd/11th; obstruction from 10th/12th/3rd. NON-COMPUTABLE: needs argala_condition primitive.",
        concordance_texts=[],
    )

# Benefic Argala → various kinds of happiness
b.add(
    conditions=[],  # NON-COMPUTABLE
    signal_group="argala_benefic_happiness",
    direction="favorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "various_kinds_of_happiness_from_benefic_argala",
         "domain": "character", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.31 v.11-17",
    description="Benefic Argala: various kinds of happiness.",
    commentary_context="Santhanam: The Argala by benefics will give various kinds of happiness. This is a general principle — benefic planets causing Argala produce positive outcomes regardless of house. NON-COMPUTABLE: needs argala_condition with planet_type=benefic.",
    concordance_texts=[],
)

# Malefic Argala → malefic effects, meddling
b.add(
    conditions=[],  # NON-COMPUTABLE
    signal_group="argala_malefic_effects",
    direction="unfavorable", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "malefic_effects_meddling_from_malefic_argala",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.31 v.11-17",
    description="Malefic Argala: malefic effects will be meddling with malefic Argalas.",
    commentary_context="Santhanam: While benefic effects will be meddling with malefic Argalas. Malefic planets causing Argala produce negative outcomes. NON-COMPUTABLE: needs argala_condition with planet_type=malefic.",
    concordance_texts=[],
)

# Both benefic and malefic → mixed results
b.add(
    conditions=[],  # NON-COMPUTABLE
    signal_group="argala_mixed_effects",
    direction="mixed", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "mixed_results_from_dual_argala",
         "domain": "character", "direction": "mixed", "magnitude": 0.5},
    ],
    verse_ref="Ch.31 v.11-17",
    description="Argala by both benefics and malefics: mixed results.",
    commentary_context="Santhanam: Argala by both benefics and malefics will yield mixed results. NON-COMPUTABLE: needs argala_condition with planet_type=both.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# KING PREDICTION (Sloka 18, p.316)
# ═══════════════════════════════════════════════════════════════════════════════

b.add(
    conditions=[],  # NON-COMPUTABLE: needs argala_on_house for houses 1, 5, 9 simultaneously
    signal_group="argala_lagna_5_9_king",
    direction="favorable", intensity="strong",
    primary_domain="career",
    predictions=[
        {"entity": "native", "claim": "doubtlessly_become_king_and_fortunate",
         "domain": "career", "direction": "favorable", "magnitude": 0.9},
    ],
    verse_ref="Ch.31 v.18",
    description="Unobstructed Argala for ascendant, 5th and 9th: native will doubtlessly become a king and fortunate.",
    commentary_context="Santhanam: Should there be unobstructed Argala for the ascendant, the 5th and 9th, the native will doubtlessly become a king and fortunate. This is the strongest Argala-based prediction — all three trinal houses activated simultaneously. NON-COMPUTABLE: needs argala_on_house for multiple houses.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH31_REGISTRY = b.build()
