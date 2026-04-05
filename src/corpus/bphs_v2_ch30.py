"""src/corpus/bphs_v2_ch30.py — BPHS Ch.30: Upa Pada.

S315: BPHS Phase 2 — Upa Pada predictions.
Slokas 1-6: Upa Pada computation + basic spouse effects.
Slokas 7-22: 2nd from Upa Pada — spouse characteristics, health, longevity.
Slokas 23-24: Methodology (multiple reference frames).
Slokas 25-30: Progeny from 9th of reference points.
Slokas 31-36: Co-born from 3rd/11th of Lagna Pada.
Slokas 37-43: Other effects from Lagna Pada + 7th lord.

Source: R. Santhanam, BPHS Vol 1, Ranjan Publications, pp.303-310.
Verse audit: data/verse_audits/ch30_audit.json (45 claims, 43 slokas).

Anchors used:
  derivation="upa_pada", base_house=1 → Upa Pada of ascendant
  derivation="arudha_pada", base_house=1 → Lagna Pada (Arudha of 1st)
Cross-refs to Ch.29 for overlapping Lagna Pada rules (v.39-40).
"""
from __future__ import annotations

from src.corpus.v2_builder import V2ChapterBuilder

b = V2ChapterBuilder(
    chapter="Ch.30", category="upa_pada_effects",
    id_start=3000, session="S315", sloka_count=43,
    chapter_tags=["upa_pada", "spouse", "progeny", "jaimini"],
    entity_target="native",
    prediction_type="trait",
    min_ratio=0.5,
)


def _up(offset: int, planet: str, mode: str, signal: str,
        direction: str, intensity: str, primary_domain: str,
        preds: list[dict], verse_ref: str, desc: str, commentary: str,
        extra_conditions: list[dict] | None = None,
        modifiers: list[dict] | None = None,
        rule_rel: dict | None = None,
        entity_target: str = "native",
        **kwargs) -> None:
    """Helper for planet_in_derived_house(upa_pada, base_house=1) rules."""
    conds = [{"type": "planet_in_derived_house", "derivation": "upa_pada",
              "base_house": 1, "offset": offset,
              "planet": planet, "mode": mode}]
    if extra_conditions:
        conds.extend(extra_conditions)
    b.add(
        conditions=conds,
        signal_group=signal,
        direction=direction, intensity=intensity,
        primary_domain=primary_domain,
        predictions=preds,
        verse_ref=verse_ref,
        description=desc,
        commentary_context=commentary,
        concordance_texts=[],
        modifiers=modifiers or [],
        rule_relationship=rule_rel or {},
        entity_target=entity_target,
        **kwargs,
    )


def _lp(offset: int, planet: str, mode: str, signal: str,
        direction: str, intensity: str, primary_domain: str,
        preds: list[dict], verse_ref: str, desc: str, commentary: str,
        extra_conditions: list[dict] | None = None,
        modifiers: list[dict] | None = None,
        rule_rel: dict | None = None,
        entity_target: str = "native",
        **kwargs) -> None:
    """Helper for planet_in_derived_house(arudha_pada, base_house=1) rules."""
    conds = [{"type": "planet_in_derived_house", "derivation": "arudha_pada",
              "base_house": 1, "offset": offset,
              "planet": planet, "mode": mode}]
    if extra_conditions:
        conds.extend(extra_conditions)
    b.add(
        conditions=conds,
        signal_group=signal,
        direction=direction, intensity=intensity,
        primary_domain=primary_domain,
        predictions=preds,
        verse_ref=verse_ref,
        description=desc,
        commentary_context=commentary,
        concordance_texts=[],
        modifiers=modifiers or [],
        rule_relationship=rule_rel or {},
        entity_target=entity_target,
        **kwargs,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# UPA PADA BASIC EFFECTS (Slokas 1-6, pp.303-304)
# ═══════════════════════════════════════════════════════════════════════════════

# Benefic conjunct/aspecting UP → happiness from progeny and spouse
_up(1, "any_benefic", "occupies", "upa_pada_benefic_occ_spouse_progeny",
     "favorable", "strong", "relationships",
     [{"entity": "native", "claim": "full_happiness_from_progeny_and_spouse",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.8},
      {"entity": "native", "claim": "progeny_happiness",
       "domain": "progeny", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.1-6",
     "Upa Pada conjunct or aspected by benefic: full happiness from progeny and spouse.",
     "Santhanam: Upa Pada (Gauna Pada) is calculated for the bhava following the natal ascendant. If conjunct or aspected by a benefic, one will obtain full happiness from progeny and spouse.")

_up(1, "any_benefic", "aspects", "upa_pada_benefic_asp_spouse_progeny",
     "favorable", "strong", "relationships",
     [{"entity": "native", "claim": "full_happiness_from_progeny_and_spouse",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.8},
      {"entity": "native", "claim": "progeny_happiness",
       "domain": "progeny", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.1-6",
     "Upa Pada aspected by benefic: full happiness from progeny and spouse.",
     "Santhanam: Aspect variant. Text says 'conjunct or aspected.'",
     rule_rel={"type": "alternative", "related_rules": ["BPHS3000"]})

# Malefic sign/conjunction on UP → ascetic, no wife
_up(1, "any_malefic", "occupies", "upa_pada_malefic_occ_ascetic",
     "unfavorable", "strong", "relationships",
     [{"entity": "native", "claim": "become_ascetic_and_go_without_wife",
       "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8}],
     "Ch.30 v.1-6",
     "Upa Pada in malefic sign or conjunct malefic: native will become ascetic and go without wife.",
     "Santhanam: Should the Upa Pada be in a malefic's sign or is aspected by or conjunct a malefic, one will become an ascetic and go without a wife.",
     modifiers=[
         {"condition": "benefic_aspect_on_upa_pada_or_malefic", "effect": "negates",
          "target": "prediction", "strength": "strong", "scope": "local"},
     ])


# ═══════════════════════════════════════════════════════════════════════════════
# 2ND FROM UPA PADA — SPOUSE EFFECTS (Slokas 7-15, pp.305-306)
# ═══════════════════════════════════════════════════════════════════════════════

# Benefic sign/aspect on 2nd from UP → good results for wife and sons
_up(2, "any_benefic", "occupies", "upa_pada_h2_benefic_occ_good_wife_sons",
     "favorable", "strong", "relationships",
     [{"entity": "native", "claim": "good_results_for_wife_and_sons",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7},
      {"entity": "native", "claim": "wife_and_sons_prosper",
       "domain": "progeny", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.7-12",
     "2nd from Upa Pada is benefic sign or conjunct benefic: good results for wife and sons.",
     "Santhanam: The 2nd from Upa Pada determines spouse quality. A benefic here indicates happy marriage and healthy progeny.")

_up(2, "any_benefic", "aspects", "upa_pada_h2_benefic_asp_good_wife_sons",
     "favorable", "strong", "relationships",
     [{"entity": "native", "claim": "good_results_for_wife_and_sons",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.7-12",
     "2nd from Upa Pada aspected by benefic: good results for wife and sons.",
     "Santhanam: Aspect variant of the 2nd-from-UP benefic rule. Text says 'aspected by or conjunct with a benefic' — good results for wife and sons will come to pass.",
     rule_rel={"type": "alternative", "related_rules": ["BPHS3003"]})

# Debilitated/malefic planet in 2nd from UP → destruction of wife
# Text: "planet in debilitation sign/Amsa OR conjunct debilitated/malefic"
# This is broader than "any_malefic occupies" — it's any planet IF debilitated or with malefic
_up(2, "any_planet", "occupies", "upa_pada_h2_debilitated_or_malefic_wife_destruction",
     "unfavorable", "strong", "relationships",
     [{"entity": "spouse", "claim": "destruction_or_death_of_wife",
       "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8}],
     "Ch.30 v.7-12",
     "Planet in 2nd from Upa Pada in debilitation or conjunct malefic: destruction of wife.",
     "Santhanam: The condition is: any planet in the 2nd from UP that is (a) in debilitation sign/Amsa, or (b) conjunct a debilitated planet, or (c) conjunct a malefic. Not simply 'malefic in 2nd' — even a benefic in debilitation triggers this.",
     entity_target="spouse",
     extra_conditions=[
         {"type": "unstructured",
          "description": "planet_debilitated_or_conjunct_malefic: occupant must be in debilitation sign/Amsa, or conjunct a debilitated planet, or conjunct a malefic"},
     ])

# Exalted planet in 2nd from UP + aspected → many charming virtuous wives
_up(2, "any_planet", "occupies", "upa_pada_h2_exalted_occ_many_wives",
     "favorable", "strong", "relationships",
     [{"entity": "native", "claim": "many_charming_and_virtuous_wives",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.8}],
     "Ch.30 v.7-12",
     "Occupant of 2nd from Upa Pada in exaltation and aspected by another planet: many charming and virtuous wives.",
     "Santhanam: Exaltation status of the occupant is the key trigger. The aspect from another planet activates the result.",
     modifiers=[
         {"condition": [{"type": "planet_dignity", "planet": "trigger", "dignity": "exalted"}], "effect": "gates",
          "target": "rule", "strength": "strong", "scope": "local"},
         {"condition": "aspected_by_another_planet", "effect": "gates",
          "target": "rule", "strength": "medium", "scope": "local"},
     ])

# Gemini as 2nd from UP → many wives
# NON-COMPUTABLE: requires derived_house_sign primitive (checking what sign
# falls in the 2nd from Upa Pada). planet_in_sign is wrong — it checks
# planet's sign anywhere, not the sign of a derived house.
b.add(
    conditions=[
        {"type": "derived_house_sign", "derivation": "arudha_pada",
         "base_house": 12, "offset": 2, "sign": "gemini"},
    ],
    signal_group="upa_pada_h2_gemini_many_wives",
    direction="favorable", intensity="moderate",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "many_wives_from_gemini_upa_pada",
         "domain": "relationships", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.7-12",
    description="Gemini as 2nd from Upa Pada: there will be many wives.",
    commentary_context="Santhanam: O excellent of the Brahmins, if Gemini happens to be the 2nd from Upa Pada, then also there will be many wives. NON-COMPUTABLE: requires derived_house_sign primitive to check what sign falls in a derived house position.",
    concordance_texts=[],
)

# 2nd lord from UP in own house → wife at advanced age
# NON-COMPUTABLE: requires "lord of derived house in own sign" primitive
b.add(
    conditions=[
        {"type": "lord_of_derived_house", "derivation": "arudha_pada",
         "base_house": 12, "offset": 2, "lord_state": "own_sign"},
    ],
    signal_group="upa_pada_h2_lord_own_wife_long_lived",
    direction="favorable", intensity="moderate",
    primary_domain="longevity",
    predictions=[
        {"entity": "spouse", "claim": "wife_lives_to_advanced_age",
         "domain": "longevity", "direction": "favorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.7-12",
    description="Uparudha or 2nd therefrom occupied by own lord: wife will live to advanced age (spouse longevity).",
    commentary_context="Santhanam: If the 2nd lord from Uparudha is in the 2nd itself or in his other own house, the spouse will live to advanced age. The native is protected from calamity. NON-COMPUTABLE: requires lord_of_derived_house primitive.",
    concordance_texts=[],
    entity_target="spouse",
)

# Lord of UP or Venus in exaltation → wife from noble family
_up(2, "any_planet", "occupies", "upa_pada_lord_exalted_noble_wife",
     "favorable", "moderate", "relationships",
     [{"entity": "spouse", "claim": "wife_from_noble_family",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.13-15",
     "Lord of Upapada or constant significator of wife in exaltation: wife will be from noble family.",
     "Santhanam: If the lord of Upapada or the constant significator of wife is in exaltation, the wife will be from a noble family. Reverse if debilitated.",
     extra_conditions=[
         {"type": "unstructured",
          "description": "lord_of_upapada_or_venus_must_be_exalted: lord of Upapada or Venus (constant significator of wife) must be in exaltation"},
     ],
     entity_target="spouse")

# Contrary: debilitated → wife from low family
_up(2, "any_planet", "occupies", "upa_pada_lord_debilitated_low_wife",
     "unfavorable", "moderate", "relationships",
     [{"entity": "spouse", "claim": "wife_from_low_family",
       "domain": "relationships", "direction": "unfavorable", "magnitude": 0.7}],
     "Ch.30 v.13-15",
     "Lord of Upapada or significator of wife debilitated: wife from low family (contrary of exaltation rule).",
     "Santhanam: Contrary — if debilitated, reverse applies.",
     extra_conditions=[
         {"type": "unstructured",
          "description": "lord_of_upapada_or_venus_must_be_debilitated: lord of Upapada or Venus (constant significator of wife) must be in debilitation"},
     ],
     entity_target="spouse",
     rule_rel={"type": "contrary_mirror", "related_rules": ["BPHS3009"]})

# 2nd from UP related to benefic → wife beautiful, fortunate, virtuous
_up(2, "any_benefic", "occupies", "upa_pada_h2_benefic_beautiful_wife",
     "favorable", "moderate", "relationships",
     [{"entity": "spouse", "claim": "wife_beautiful_fortunate_virtuous",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.13-15",
     "2nd from Upapada related to benefic: wife will be beautiful, fortunate and virtuous.",
     "Santhanam: If the 2nd from Upapada is related to a benefic, the wife will be beautiful, fortunate and virtuous.",
     entity_target="spouse")


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIFIC PLANET COMBOS IN 2ND FROM UPA PADA (Slokas 16-22, pp.306-307)
# ═══════════════════════════════════════════════════════════════════════════════

# v.16: Saturn+Rahu in 2nd → wife loss
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_saturn_rahu_occ_wife_loss",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "native", "claim": "loss_of_wife_through_calumny_or_death",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.16",
    description="Saturn and Rahu in 2nd from Upa Pada: native will lose wife on account of calumny or through death.",
    commentary_context="Santhanam: Saturn (restriction/separation) combined with Rahu (deception/sudden events) in the 2nd from Upa Pada indicates loss of spouse either through scandal/false accusation or physical death.",
    concordance_texts=[],
)

# v.17: Venus+Ketu in 2nd from UP → wife's blood disorders
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "venus", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "ketu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_venus_ketu_occ_wife_blood",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "spouse", "claim": "wife_troubled_by_blood_disorders_leucorrhoea",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.17",
    description="Venus and Ketu in 2nd from Upapada: wife troubled by disorder of blood, leucorrhoea etc.",
    commentary_context="Santhanam: Venus (significator of spouse) combined with Ketu (headless, disruption) in the 2nd from Upa Pada affects the wife's reproductive/blood health.",
    concordance_texts=[],
    entity_target="spouse",
)

# v.18: Mercury+Ketu in 2nd → bone breakage; Rahu+Saturn+Sun → bone distress
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "mercury", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "ketu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_mercury_ketu_occ_bone_breakage",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "spouse", "claim": "breakage_of_bones",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.18",
    description="Mercury with Ketu in 2nd from Upapada: breakage of bones. Rahu, Saturn and Sun cause distress of bones.",
    commentary_context="Santhanam: Mercury + Ketu in the 2nd from Upa Pada causes bone-related health issues for the spouse. The additional mention of Rahu/Saturn/Sun extends the bone distress pattern.",
    concordance_texts=[],
    entity_target="spouse",
)

# v.19: Mercury+Rahu in 2nd → stout-bodied wife
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "mercury", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_mercury_rahu_occ_stout_wife",
    direction="neutral", intensity="moderate",
    primary_domain="character",
    predictions=[
        {"entity": "spouse", "claim": "stout_bodied_wife",
         "domain": "character", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.30 v.19-22",
    description="Mercury and Rahu in 2nd from Upapada: stout-bodied wife.",
    commentary_context="Santhanam: Physical characteristic of spouse — body type indication.",
    concordance_texts=[],
    entity_target="spouse",
)

# v.19-22: Mars+Saturn in 2nd (Mercury sign) → wife nasal disorders
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "mars", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_mars_saturn_occ_nasal",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "spouse", "claim": "wife_suffers_nasal_disorders",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.19-22",
    description="Mars and Saturn in 2nd from Upa Pada: wife suffers from nasal disorders.",
    commentary_context="Santhanam: Text specifies this when 2nd from UP is a sign of Mercury tenanted by Mars and Saturn, or a sign of Mars occupied by Mars and Saturn. Both conditions produce nasal problems for the spouse. Exception (v.22): these evils will not come to pass if benefic conjunction or aspect.",
    concordance_texts=[],
    entity_target="spouse",
    modifiers=[
        {"condition": "benefic_conjunction_or_aspect", "effect": "negates",
         "target": "prediction", "strength": "strong", "scope": "local"},
    ],
)

# v.19-22: Jupiter+Saturn in 2nd → wife ear/eye disorders
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "jupiter", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_jupiter_saturn_occ_ear_eye",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "spouse", "claim": "wife_disorders_of_ears_or_eyes",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.19-22",
    description="Jupiter and Saturn in 2nd from Upa Pada: wife will have disorders of ears/eyes.",
    commentary_context="Santhanam: Jupiter and Saturn, if in the 2nd from Upapada, cause disorders of ears/eyes to the wife. Exception (v.22): these evils will not come to pass if benefic conjunction or aspect.",
    concordance_texts=[],
    entity_target="spouse",
    modifiers=[
        {"condition": "benefic_conjunction_or_aspect", "effect": "negates",
         "target": "prediction", "strength": "strong", "scope": "local"},
    ],
)

# v.19-22: Saturn+Rahu in Saturn sign as 2nd → wife lameness/windy disorders
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 2, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h2_saturn_rahu_sign_lameness",
    direction="unfavorable", intensity="moderate",
    primary_domain="health",
    predictions=[
        {"entity": "spouse", "claim": "wife_lameness_or_windy_disorders",
         "domain": "health", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.19-22",
    description="Saturn and Rahu in sign of Saturn as 2nd from Upa Pada: wife will have lameness or windy disorders.",
    commentary_context="Santhanam: When the 2nd from Upa Pada is a sign of Saturn (Capricorn/Aquarius) and Saturn+Rahu are there, lameness or vata disorders affect the wife. Exception: these evils will not come to pass if there be benefic conjunction or aspect.",
    concordance_texts=[],
    entity_target="spouse",
    modifiers=[
        {"condition": "benefic_conjunction_or_aspect", "effect": "negates",
         "target": "prediction", "strength": "strong", "scope": "local"},
    ],
)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGENY FROM 9TH (Slokas 25-28, p.308)
# MULTI-ANCHOR AMBIGUITY: text says "9th from one of the said places"
# Sloka 23-24 defines: natal ascendant, Lagna Pada, 7th from Upa Pada.
# Encoded with upa_pada as anchor (chapter's primary reference frame).
# The rule ALSO applies from natal lagna and lagna_pada — noted in commentary.
# certainty_level for these rules should be treated as "context_dependent".
# ═══════════════════════════════════════════════════════════════════════════════

# Saturn+Moon in 9th → no son
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "moon", "mode": "occupies"},
    ],
    signal_group="upa_pada_h9_saturn_moon_no_son",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "no_son_at_all",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Saturn and Moon together in 9th from Upa Pada: no son at all.",
    commentary_context="Santhanam: '9th from one of the said places' (sloka 23 defines: natal ascendant, Lagna Pada, 7th from Upa Pada). Saturn+Moon in the 9th blocks male progeny entirely. Using Upa Pada as primary anchor; the rule applies from any of the three reference points.",
    concordance_texts=[],
)

# Sun+Jupiter+Rahu in 9th → number of sons + strong/valorous
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "sun", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "jupiter", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="upa_pada_h9_sun_jup_rahu_strong_sons",
    direction="favorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "number_of_sons_strong_valorous_successful",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Sun, Jupiter and Rahu in 9th from Upa Pada: son will be strong, valorous, greatly successful, and prevail over adversaries.",
    commentary_context="Santhanam: The conjunction of Sun (authority), Jupiter (wisdom), and Rahu (amplification) in the 9th from the reference point produces exceptional male progeny.",
    concordance_texts=[],
)

# Mars+Saturn in 9th → no son or adoption
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "mars", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "upa_pada",
         "base_house": 1, "offset": 9, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="upa_pada_h9_mars_saturn_no_son_adoption",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "no_son_or_obtained_by_adoption",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Mars and Saturn in 9th: no son, or a son obtained by adoption or brother's son will come in adoption.",
    commentary_context="Santhanam: Mars (aggression) + Saturn (denial) in the 9th from reference point blocks natural male progeny. Adoption becomes the path to sons.",
    concordance_texts=[],
)

# Lagna Pada variants for slokas 25-28 (text says "from one of the said places"
# = natal asc, lagna pada, 7th from upa pada — encoding lagna_pada as 2nd anchor)

# Saturn+Moon in 9th from Lagna Pada → no son
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "saturn", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "moon", "mode": "occupies"},
    ],
    signal_group="lagna_pada_h9_saturn_moon_no_son",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "no_son_at_all",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Saturn and Moon in 9th from Lagna Pada: no son at all (Lagna Pada anchor variant).",
    commentary_context="Santhanam: Lagna Pada variant of the same rule. Text says '9th from one of the said places' — this encodes the Lagna Pada reference frame. See BPHS3019 for Upa Pada anchor.",
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS3019"]},
)

# Sun+Jupiter+Rahu in 9th from Lagna Pada → strong sons
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "sun", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "jupiter", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "rahu", "mode": "occupies"},
    ],
    signal_group="lagna_pada_h9_sun_jup_rahu_strong_sons",
    direction="favorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "number_of_sons_strong_valorous_successful",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Sun, Jupiter and Rahu in 9th from Lagna Pada: son strong, valorous, successful (Lagna Pada variant).",
    commentary_context="Santhanam: Lagna Pada variant. See BPHS3020 for Upa Pada anchor.",
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS3020"]},
)

# Mars+Saturn in 9th from Lagna Pada → no son or adoption
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "mars", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 9, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="lagna_pada_h9_mars_saturn_no_son_adoption",
    direction="unfavorable", intensity="strong",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "no_son_or_obtained_by_adoption",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.25-28",
    description="Mars and Saturn in 9th from Lagna Pada: no son, or obtained by adoption (Lagna Pada variant).",
    commentary_context="Santhanam: Lagna Pada variant. See BPHS3021 for Upa Pada anchor.",
    concordance_texts=[],
    rule_relationship={"type": "addition", "related_rules": ["BPHS3021"]},
)

# Leo as Upa Pada + Moon aspect → limited children
b.add(
    conditions=[
        {"type": "derived_house_sign", "derivation": "arudha_pada",
         "base_house": 12, "offset": 1, "sign": "leo"},
    ],
    signal_group="upa_pada_leo_limited_children",
    direction="unfavorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "limited_number_of_children",
         "domain": "progeny", "direction": "unfavorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.29-30",
    description="Leo as Upapada aspected by Moon: limited number of children.",
    commentary_context="Santhanam: Sign-specific condition — requires checking if Upa Pada falls in Leo. Non-computable until sign-of-derived-house primitive is available.",
    concordance_texts=[],
)

# Virgo as Upa Pada → many daughters
b.add(
    conditions=[
        {"type": "derived_house_sign", "derivation": "arudha_pada",
         "base_house": 12, "offset": 1, "sign": "virgo"},
    ],
    signal_group="upa_pada_virgo_many_daughters",
    direction="favorable", intensity="moderate",
    primary_domain="progeny",
    predictions=[
        {"entity": "native", "claim": "many_daughters",
         "domain": "progeny", "direction": "favorable", "magnitude": 0.6},
    ],
    verse_ref="Ch.30 v.29-30",
    description="Virgo as Upapada: many daughters.",
    commentary_context="Santhanam: Sign-specific condition — Virgo Upa Pada produces female progeny predominantly.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# CO-BORN FROM 3RD/11TH OF LAGNA PADA (Slokas 31-36, pp.308-309)
# ═══════════════════════════════════════════════════════════════════════════════

# Rahu+Saturn in 3rd/11th from LP → destroy co-born
b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 3, "planet": "rahu", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 3, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="lagna_pada_h3_rahu_saturn_destroy_younger_coborn",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "siblings", "claim": "younger_coborn_destroyed",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.31",
    description="Rahu and Saturn in 3rd from Lagna Pada: younger co-born destroyed.",
    commentary_context="Santhanam: The 3rd from Lagna Pada governs younger siblings; 11th governs elder. Rahu+Saturn in the 3rd destroys younger brothers/sisters. Same combination in 11th destroys elder ones.",
    concordance_texts=[],
    entity_target="siblings",
)

b.add(
    conditions=[
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "rahu", "mode": "occupies"},
        {"type": "planet_in_derived_house", "derivation": "arudha_pada",
         "base_house": 1, "offset": 11, "planet": "saturn", "mode": "occupies"},
    ],
    signal_group="lagna_pada_h11_rahu_saturn_destroy_elder_coborn",
    direction="unfavorable", intensity="strong",
    primary_domain="relationships",
    predictions=[
        {"entity": "siblings", "claim": "elder_coborn_destroyed",
         "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8},
    ],
    verse_ref="Ch.30 v.31",
    description="Rahu and Saturn in 11th from Lagna Pada: elder co-born (brothers/sisters) destroyed.",
    commentary_context="Santhanam: 11th from Lagna Pada = elder siblings. Same Rahu+Saturn combination destroys elder co-born.",
    concordance_texts=[],
    entity_target="siblings",
)

# Venus in 3rd/11th from LP → abortion
_lp(3, "venus", "occupies", "lagna_pada_h3_venus_occ_abortion",
     "unfavorable", "strong", "progeny",
     [{"entity": "native", "claim": "abortion_or_miscarriage_earlier",
       "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7}],
     "Ch.30 v.32",
     "Venus in 3rd/11th from Lagna Pada: there would have been an abortion earlier.",
     "Santhanam: Venus in the 3rd or 11th from Lagna Pada indicates prior abortion/miscarriage. Same effect if Venus is in the 8th from natal ascendant or from Lagnarudha.")

_lp(11, "venus", "occupies", "lagna_pada_h11_venus_occ_abortion",
     "unfavorable", "strong", "progeny",
     [{"entity": "native", "claim": "abortion_or_miscarriage_earlier",
       "domain": "progeny", "direction": "unfavorable", "magnitude": 0.7}],
     "Ch.30 v.32",
     "Venus in 11th from Lagna Pada: there would have been an abortion earlier.",
     "Santhanam: 11th from Lagna Pada variant. Same prediction as 3rd placement.",
     rule_rel={"type": "alternative", "related_rules": ["BPHS3029"]})

# Moon/Jupiter/Mercury/Mars in 3rd/11th from LP → many valorous co-born
_lp(3, "any_benefic", "occupies", "lagna_pada_h3_benefic_occ_valorous_coborn",
     "favorable", "moderate", "relationships",
     [{"entity": "siblings", "claim": "many_valorous_coborn",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.33-36",
     "Moon, Jupiter, Mercury and Mars in 3rd/11th from Lagna Pada: many valorous co-born.",
     "Santhanam: These four planets (specifically Moon, Jupiter, Mercury, Mars) in the 3rd or 11th from Lagna Pada produce numerous courageous siblings.",
     entity_target="siblings")

# Saturn alone in 3rd/11th → native spared, co-born die
_lp(3, "saturn", "occupies", "lagna_pada_h3_saturn_alone_coborn_die",
     "unfavorable", "strong", "relationships",
     [{"entity": "siblings", "claim": "coborn_will_die_native_spared",
       "domain": "relationships", "direction": "unfavorable", "magnitude": 0.8}],
     "Ch.30 v.33-36",
     "Saturn alone in 3rd/11th from Lagna Pada: native will be spared while co-born will die.",
     "Santhanam: If Saturn is alone in one of these houses (without Mars), the native survives but siblings do not.",
     entity_target="siblings")

# Ketu in 3rd/11th from LP → happiness from sisters
_lp(3, "ketu", "occupies", "lagna_pada_h3_ketu_occ_happiness_sisters",
     "favorable", "moderate", "relationships",
     [{"entity": "native", "claim": "abundant_happiness_from_sisters",
       "domain": "relationships", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.33-36",
     "Ketu in 3rd/11th from Lagna Pada: abundant happiness from one's sisters.",
     "Santhanam: Ketu in the 3rd or 11th from Lagna Pada specifically benefits relationships with sisters.")


# ═══════════════════════════════════════════════════════════════════════════════
# OTHER EFFECTS FROM LAGNA PADA (Slokas 37-43, pp.309-310)
# ═══════════════════════════════════════════════════════════════════════════════

# 6th from LP + malefic without benefic → thief
_lp(6, "any_malefic", "occupies", "lagna_pada_h6_malefic_occ_thief",
     "unfavorable", "strong", "character",
     [{"entity": "native", "claim": "native_will_be_a_thief",
       "domain": "character", "direction": "unfavorable", "magnitude": 0.7}],
     "Ch.30 v.37",
     "6th from Lagna Pada occupied by malefic and bereft of benefic conjunction/aspect: native will be a thief.",
     "Santhanam: The 6th from Arudha Lagna with malefic influence and no benefic mitigation produces a thief.",
     modifiers=[
         {"condition": "benefic_conjunction_or_aspect", "effect": "negates",
          "target": "prediction", "strength": "strong", "scope": "local"},
     ])

# Rahu in 7th/12th from LP → spiritual knowledge
_lp(7, "rahu", "occupies", "lagna_pada_h7_rahu_occ_spiritual",
     "favorable", "strong", "spirituality",
     [{"entity": "native", "claim": "endowed_with_spiritual_knowledge_very_fortunate",
       "domain": "spirituality", "direction": "favorable", "magnitude": 0.8}],
     "Ch.30 v.38",
     "Rahu in 7th/12th from Lagna Pada or aspecting: endowed with spiritual knowledge and be very fortunate.",
     "Santhanam: Rahu in the 7th or 12th from Lagna Pada, or aspecting one of these houses, grants spiritual wisdom and exceptional good fortune.")

_lp(12, "rahu", "occupies", "lagna_pada_h12_rahu_occ_spiritual",
     "favorable", "strong", "spirituality",
     [{"entity": "native", "claim": "endowed_with_spiritual_knowledge_very_fortunate",
       "domain": "spirituality", "direction": "favorable", "magnitude": 0.8}],
     "Ch.30 v.38",
     "Rahu in 12th from Lagna Pada: spiritual knowledge and very fortunate.",
     "Santhanam: 12th from Lagna Pada variant.",
     rule_rel={"type": "alternative", "related_rules": ["BPHS3035"]})

# v.39: Mercury in LP → lord over country (cross-ref Ch.29 BPHS2932)
_lp(1, "mercury", "occupies", "lagna_pada_mercury_occ_lord_country",
     "favorable", "strong", "career",
     [{"entity": "native", "claim": "lord_over_whole_country",
       "domain": "career", "direction": "favorable", "magnitude": 0.9}],
     "Ch.30 v.39",
     "Mercury in Lagna Pada: native will lord over whole country.",
     "Santhanam: Reiteration of Ch.29 v.30-37 — same prediction. Also see verse 30, ch. 29.",
     rule_rel={"type": "addition", "related_rules": ["BPHS2932"]})

# Jupiter in LP → knower of all things
_lp(1, "jupiter", "occupies", "lagna_pada_jupiter_occ_knower",
     "favorable", "strong", "career",
     [{"entity": "native", "claim": "knower_of_all_things",
       "domain": "career", "direction": "favorable", "magnitude": 0.8}],
     "Ch.30 v.39",
     "Jupiter in Lagna Pada: will make him a knower of all things.",
     "Santhanam: Jupiter in the Arudha Lagna grants comprehensive knowledge and wisdom.")

# Venus in LP → poet/speaker (cross-ref Ch.29 BPHS2933)
_lp(1, "venus", "occupies", "lagna_pada_venus_occ_poet",
     "favorable", "moderate", "career",
     [{"entity": "native", "claim": "poet_or_speaker",
       "domain": "career", "direction": "favorable", "magnitude": 0.6}],
     "Ch.30 v.39",
     "Venus in Lagna Pada: denotes a poet/speaker.",
     "Santhanam: Reiteration of Ch.29 v.30-37. Venus in Arudha = creative expression through speech.",
     rule_rel={"type": "addition", "related_rules": ["BPHS2933"]})

# Benefics in 2nd from UP or LP → wealth + intelligent
_up(2, "any_benefic", "occupies", "upa_pada_h2_benefic_wealth_intelligent",
     "favorable", "strong", "wealth",
     [{"entity": "native", "claim": "endowed_with_all_kinds_of_wealth_and_intelligent",
       "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.40",
     "Benefics occupy 2nd from Upapada or from Lagna Pada: endowed with all kinds of wealth and be intelligent.",
     "Santhanam: Benefics in the 2nd from either Upa Pada or Lagna Pada produce wealth and intelligence. This is the Upa Pada anchor variant.")

# Lagna Pada variant of v.40
_lp(2, "any_benefic", "occupies", "lagna_pada_h2_benefic_wealth_intelligent",
     "favorable", "strong", "wealth",
     [{"entity": "native", "claim": "endowed_with_all_kinds_of_wealth_and_intelligent",
       "domain": "wealth", "direction": "favorable", "magnitude": 0.7}],
     "Ch.30 v.40",
     "Benefics occupy 2nd from Lagna Pada: endowed with all kinds of wealth and be intelligent.",
     "Santhanam: Lagna Pada variant. Text explicitly says '2nd from Upapada or from Lagna Pada.' See Upa Pada variant above.",
     rule_rel={"type": "addition", "related_rules": ["BPHS3037"]})

# Lord of 2nd from UP with malefic in 2nd from natal → thief
b.add(
    conditions=[
        {"type": "lord_of_derived_house", "derivation": "arudha_pada",
         "base_house": 12, "offset": 2, "lord_state": ""},
        {"type": "planet_in_house", "planet": "any_malefic", "house": 2},
    ],
    signal_group="upa_pada_h2_lord_malefic_natal_h2_thief",
    direction="unfavorable", intensity="strong",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "surely_become_a_thief",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.7},
    ],
    verse_ref="Ch.30 v.41",
    description="Lord of 2nd from Upapada in 2nd from natal ascendant with malefic: native will surely become a thief.",
    commentary_context="Santhanam: Cross-referencing Upa Pada 2nd lord with natal 2nd house. Non-computable until cross-anchor primitive is available.",
    concordance_texts=[],
)

# v.42-43: Rahu in 2nd from lord of 7th (from UP) → long projected teeth
b.add(
    conditions=[{"type": "planet_from_derived_lord", "derivation": "arudha_pada", "base_house": 12, "lord_offset": 7, "planet_offset": 2, "planet": "Rahu"}],
    signal_group="upa_pada_7lord_h2_rahu_long_teeth",
    direction="neutral", intensity="weak",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "long_and_projected_teeth",
         "domain": "character", "direction": "neutral", "magnitude": 0.5},
    ],
    verse_ref="Ch.30 v.42-43",
    description="Rahu in 2nd from lord of 7th counted from Upapada: long and projected teeth.",
    commentary_context="Santhanam: Physical characteristic based on complex derived position. Non-computable until planet_in_house_from for derived house lords is available.",
    concordance_texts=[],
)

b.add(
    conditions=[{"type": "planet_from_derived_lord", "derivation": "arudha_pada", "base_house": 12, "lord_offset": 7, "planet_offset": 2, "planet": "Ketu"}],
    signal_group="upa_pada_7lord_h2_ketu_stammering",
    direction="unfavorable", intensity="weak",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "stammering_in_speech",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.30 v.42-43",
    description="Ketu in 2nd from lord of 7th from Upapada: stammering.",
    commentary_context="Santhanam: Ketu (headless, disruption) in the 2nd from the 7th lord from Upa Pada disrupts speech.",
    concordance_texts=[],
)

b.add(
    conditions=[{"type": "planet_from_derived_lord", "derivation": "arudha_pada", "base_house": 12, "lord_offset": 7, "planet_offset": 2, "planet": "Saturn"}],
    signal_group="upa_pada_7lord_h2_saturn_ugly",
    direction="unfavorable", intensity="weak",
    primary_domain="character",
    predictions=[
        {"entity": "native", "claim": "ugly_appearance",
         "domain": "character", "direction": "unfavorable", "magnitude": 0.5},
    ],
    verse_ref="Ch.30 v.42-43",
    description="Saturn in 2nd from lord of 7th from Upapada: one will look ugly. Mixed planets = mixed effects.",
    commentary_context="Santhanam: Saturn (restriction, austerity) in this position produces unpleasant physical appearance. Mixed planetary influences produce mixed results.",
    concordance_texts=[],
)


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

BPHS_V2_CH30_REGISTRY = b.build()
