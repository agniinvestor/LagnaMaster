"""
src/corpus/combined_corpus.py — Combined Corpus Loader

Loads all classical text registries into a single CorpusRegistry.
This is the authoritative corpus for Phase 1 encoding targets and
Phase 6 SHAP analysis (after OSF pre-registration per G22).

Current sources loaded:
  Phase 0 (S205-S210):
  - R01-R23    existing_rules (implemented)
  - B001-B031  bphs_extended
  - PH001-PH021 phaladeepika_rules
  - BJ001-BJ026 brihat_jataka_rules
  - UK001-UK017 uttara_kalamrita_rules
  - JP001-JP017 jataka_parijata_rules

  Phase 1 (S216-S228):
  - H1L-H2L (24 rules)  bphs_lords_h1_h2
  - H3L-H4L (24 rules)  bphs_lords_h3_h4
  - H5L-H6L (24 rules)  bphs_lords_h5_h6
  - H7L-H8L (24 rules)  bphs_lords_h7_h8
  - H9L-H10L (24 rules) bphs_lords_h9_h10
  - H11L-H12L (24 rules) bphs_lords_h11_h12
  - YB001-YB025 (25 rules) bphs_yogas_basic
  - RY001-RY025 (25 rules) bphs_raja_yoga
  - DY001-DY025 (25 rules) bphs_dhana_yoga
  - DIG001-DIG020 (20 rules) bphs_dignities_ext
  - ASP001-ASP020 (20 rules) bphs_aspects
  - DAR001-DAR020 (20 rules) bphs_dasha_results
  - SL001-SL020 (20 rules) bphs_special_lagnas

  Phase 1 (S229+):
  - SUR001-SUR012, MOR001-MOR012 (24 rules) bphs_graha_rashis_p1
  - MAR001-MAR012, BUR001-BUR012 (24 rules) bphs_graha_rashis_p2

Public API
----------
  COMBINED_CORPUS   — pre-populated CorpusRegistry singleton
  build_corpus()    — rebuild fresh (for testing or extension)
"""

from __future__ import annotations

from src.corpus.registry import CorpusRegistry


def build_corpus() -> CorpusRegistry:
    """Build a fresh combined corpus from all registered sources."""
    # ── Phase 0 sources ───────────────────────────────────────────────────────
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY

    # ── Phase 1 sources (S216–S228) ───────────────────────────────────────────
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY      # S216
    from src.corpus.bphs_lords_h3_h4 import BPHS_LORDS_H3_H4_REGISTRY      # S217
    from src.corpus.bphs_lords_h5_h6 import BPHS_LORDS_H5_H6_REGISTRY      # S218
    from src.corpus.bphs_lords_h7_h8 import BPHS_LORDS_H7_H8_REGISTRY      # S219
    from src.corpus.bphs_lords_h9_h10 import BPHS_LORDS_H9_H10_REGISTRY    # S220
    from src.corpus.bphs_lords_h11_h12 import BPHS_LORDS_H11_H12_REGISTRY  # S221
    from src.corpus.bphs_yogas_basic import BPHS_YOGAS_BASIC_REGISTRY       # S222
    from src.corpus.bphs_raja_yoga import BPHS_RAJA_YOGA_REGISTRY           # S223
    from src.corpus.bphs_dhana_yoga import BPHS_DHANA_YOGA_REGISTRY         # S224
    from src.corpus.bphs_dignities_ext import BPHS_DIGNITIES_EXT_REGISTRY   # S225
    from src.corpus.bphs_aspects import BPHS_ASPECTS_REGISTRY               # S226
    from src.corpus.bphs_dasha_results import BPHS_DASHA_RESULTS_REGISTRY   # S227
    from src.corpus.bphs_special_lagnas import BPHS_SPECIAL_LAGNAS_REGISTRY   # S228
    from src.corpus.bphs_graha_rashis_p1 import BPHS_GRAHA_RASHIS_P1_REGISTRY  # S229
    from src.corpus.bphs_graha_rashis_p2 import BPHS_GRAHA_RASHIS_P2_REGISTRY  # S230
    from src.corpus.bphs_graha_rashis_p3 import BPHS_GRAHA_RASHIS_P3_REGISTRY  # S231
    from src.corpus.bphs_graha_rashis_p4 import BPHS_GRAHA_RASHIS_P4_REGISTRY  # S232
    from src.corpus.kp_sublord_rules import KP_SUBLORD_RULES_REGISTRY  # S233
    from src.corpus.bphs_nakshatra_rules_p1 import BPHS_NAKSHATRA_RULES_P1_REGISTRY  # S234
    from src.corpus.bphs_nakshatra_rules_p2 import BPHS_NAKSHATRA_RULES_P2_REGISTRY  # S235
    from src.corpus.bphs_bhava_karakas import BPHS_BHAVA_KARAKAS_REGISTRY  # S236
    from src.corpus.bphs_varga_rules import BPHS_VARGA_RULES_REGISTRY  # S237
    from src.corpus.brihat_jataka_ext import BRIHAT_JATAKA_EXT_REGISTRY  # S238
    from src.corpus.phala_deepika_ext import PHALA_DEEPIKA_EXT_REGISTRY  # S239
    from src.corpus.uttara_kalamrita_ext import UTTARA_KALAMRITA_EXT_REGISTRY  # S240
    from src.corpus.jataka_parijata_ext import JATAKA_PARIJATA_EXT_REGISTRY  # S241
    from src.corpus.transit_rules import TRANSIT_RULES_REGISTRY  # S242
    from src.corpus.ashtakavarga_rules import ASHTAKAVARGA_RULES_REGISTRY  # S243
    from src.corpus.jaimini_sutras_rules import JAIMINI_SUTRAS_RULES_REGISTRY  # S244
    from src.corpus.shadbala_rules import SHADBALA_RULES_REGISTRY  # S245
    from src.corpus.dasha_systems_rules import DASHA_SYSTEMS_RULES_REGISTRY  # S246
    from src.corpus.yoga_extended_rules import YOGA_EXTENDED_RULES_REGISTRY  # S247
    from src.corpus.lagna_extended_rules import LAGNA_EXTENDED_RULES_REGISTRY  # S248
    from src.corpus.bhava_phala_rules import BHAVA_PHALA_RULES_REGISTRY  # S249
    from src.corpus.graha_phala_rules import GRAHA_PHALA_RULES_REGISTRY  # S250
    from src.corpus.bphs_graha_bhava_complete import BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY  # S251
    from src.corpus.bphs_yoga_exhaustive import BPHS_YOGA_EXHAUSTIVE_REGISTRY  # S252
    from src.corpus.bphs_bhava_exhaustive import BPHS_BHAVA_EXHAUSTIVE_REGISTRY  # S253
    from src.corpus.bphs_graha_characteristics import BPHS_GRAHA_CHARACTERISTICS_REGISTRY  # S254
    from src.corpus.brihat_jataka_exhaustive import BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY  # S255
    from src.corpus.uttara_kalamrita_exhaustive import UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY  # S256
    from src.corpus.jataka_parijata_exhaustive import JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY  # S257
    from src.corpus.sarvartha_chintamani_exhaustive import SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY  # S258
    from src.corpus.jaimini_sutras_exhaustive import JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY  # S259
    from src.corpus.lal_kitab_rules import LAL_KITAB_RULES_REGISTRY  # S260
    from src.corpus.chandra_kala_nadi_rules import CHANDRA_KALA_NADI_REGISTRY  # S261
    from src.corpus.phaladeepika_exhaustive import PHALADEEPIKA_EXHAUSTIVE_REGISTRY  # S262
    from src.corpus.laghu_parashari_functional import LAGHU_PARASHARI_FUNCTIONAL_REGISTRY  # S264
    from src.corpus.laghu_parashari_bcd import (  # S265
        LAGHU_PARASHARI_YOGAKARAKA_REGISTRY,
        LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY,
        LAGHU_PARASHARI_DASHA_REGISTRY,
    )
    from src.corpus.laghu_parashari_ef import (  # S266
        LAGHU_PARASHARI_ANTARDASHA_REGISTRY,
        LAGHU_PARASHARI_MARAKA_REGISTRY,
    )
    from src.corpus.bhavartha_ratnakara_1 import BHAVARTHA_RATNAKARA_1_REGISTRY  # S267
    from src.corpus.bhavartha_ratnakara_2 import BHAVARTHA_RATNAKARA_2_REGISTRY  # S268
    from src.corpus.bhavartha_ratnakara_3 import BHAVARTHA_RATNAKARA_3_REGISTRY  # S269
    from src.corpus.bhavartha_ratnakara_4 import BHAVARTHA_RATNAKARA_4_REGISTRY  # S270
    from src.corpus.bhavartha_ratnakara_5 import BHAVARTHA_RATNAKARA_5_REGISTRY  # S271
    from src.corpus.bhavartha_ratnakara_6 import BHAVARTHA_RATNAKARA_6_REGISTRY  # S272
    from src.corpus.saravali_conjunctions_1 import SARAVALI_CONJUNCTIONS_1_REGISTRY  # S273
    from src.corpus.saravali_conjunctions_2 import SARAVALI_CONJUNCTIONS_2_REGISTRY  # S274
    from src.corpus.saravali_conjunctions_3 import SARAVALI_CONJUNCTIONS_3_REGISTRY  # S275
    from src.corpus.saravali_conjunctions_4 import SARAVALI_CONJUNCTIONS_4_REGISTRY  # S276
    from src.corpus.saravali_conjunctions_5 import SARAVALI_CONJUNCTIONS_5_REGISTRY  # S277
    from src.corpus.saravali_conjunctions_6 import SARAVALI_CONJUNCTIONS_6_REGISTRY  # S278
    from src.corpus.saravali_conjunctions_7 import SARAVALI_CONJUNCTIONS_7_REGISTRY  # S279
    from src.corpus.saravali_conjunctions_8 import SARAVALI_CONJUNCTIONS_8_REGISTRY  # S280
    from src.corpus.saravali_signs_1 import SARAVALI_SIGNS_1_REGISTRY  # S281
    from src.corpus.saravali_signs_2 import SARAVALI_SIGNS_2_REGISTRY  # S282
    from src.corpus.saravali_signs_3 import SARAVALI_SIGNS_3_REGISTRY  # S283
    from src.corpus.saravali_signs_4 import SARAVALI_SIGNS_4_REGISTRY  # S284
    from src.corpus.saravali_signs_5 import SARAVALI_SIGNS_5_REGISTRY  # S285
    from src.corpus.saravali_signs_6 import SARAVALI_SIGNS_6_REGISTRY  # S286
    from src.corpus.saravali_signs_7 import SARAVALI_SIGNS_7_REGISTRY  # S287
    from src.corpus.saravali_signs_8 import SARAVALI_SIGNS_8_REGISTRY  # S288
    from src.corpus.saravali_houses_1 import SARAVALI_HOUSES_1_REGISTRY  # S289
    from src.corpus.saravali_houses_2 import SARAVALI_HOUSES_2_REGISTRY  # S290
    from src.corpus.saravali_houses_3 import SARAVALI_HOUSES_3_REGISTRY  # S291
    from src.corpus.saravali_houses_4 import SARAVALI_HOUSES_4_REGISTRY  # S292
    from src.corpus.saravali_houses_5 import SARAVALI_HOUSES_5_REGISTRY  # S293
    from src.corpus.saravali_houses_6 import SARAVALI_HOUSES_6_REGISTRY  # S294
    from src.corpus.saravali_houses_7 import SARAVALI_HOUSES_7_REGISTRY  # S295
    from src.corpus.saravali_houses_8 import SARAVALI_HOUSES_8_REGISTRY  # S296
    from src.corpus.saravali_special_1 import SARAVALI_SPECIAL_1_REGISTRY  # S297
    from src.corpus.saravali_special_2 import SARAVALI_SPECIAL_2_REGISTRY  # S298
    from src.corpus.saravali_special_3 import SARAVALI_SPECIAL_3_REGISTRY  # S299
    from src.corpus.saravali_special_4 import SARAVALI_SPECIAL_4_REGISTRY  # S300
    from src.corpus.saravali_special_5 import SARAVALI_SPECIAL_5_REGISTRY  # S301
    from src.corpus.saravali_special_6 import SARAVALI_SPECIAL_6_REGISTRY  # S302
    from src.corpus.saravali_special_7 import SARAVALI_SPECIAL_7_REGISTRY  # S303
    from src.corpus.saravali_special_8 import SARAVALI_SPECIAL_8_REGISTRY  # S304
    from src.corpus.saravali_special_9 import SARAVALI_SPECIAL_9_REGISTRY  # S305

    registry = CorpusRegistry()
    sources = [
        # Phase 0
        EXISTING_RULES_REGISTRY,
        BPHS_EXTENDED_REGISTRY,
        PHALADEEPIKA_REGISTRY,
        BRIHAT_JATAKA_REGISTRY,
        UTTARA_KALAMRITA_REGISTRY,
        JATAKA_PARIJATA_REGISTRY,
        # Phase 1 — S216-S228
        BPHS_LORDS_H1_H2_REGISTRY,
        BPHS_LORDS_H3_H4_REGISTRY,
        BPHS_LORDS_H5_H6_REGISTRY,
        BPHS_LORDS_H7_H8_REGISTRY,
        BPHS_LORDS_H9_H10_REGISTRY,
        BPHS_LORDS_H11_H12_REGISTRY,
        BPHS_YOGAS_BASIC_REGISTRY,
        BPHS_RAJA_YOGA_REGISTRY,
        BPHS_DHANA_YOGA_REGISTRY,
        BPHS_DIGNITIES_EXT_REGISTRY,
        BPHS_ASPECTS_REGISTRY,
        BPHS_DASHA_RESULTS_REGISTRY,
        BPHS_SPECIAL_LAGNAS_REGISTRY,
        # Phase 1 — S229+
        BPHS_GRAHA_RASHIS_P1_REGISTRY,
        BPHS_GRAHA_RASHIS_P2_REGISTRY,
        BPHS_GRAHA_RASHIS_P3_REGISTRY,
        BPHS_GRAHA_RASHIS_P4_REGISTRY,
        KP_SUBLORD_RULES_REGISTRY,
        BPHS_NAKSHATRA_RULES_P1_REGISTRY,
        BPHS_NAKSHATRA_RULES_P2_REGISTRY,
        BPHS_BHAVA_KARAKAS_REGISTRY,
        BPHS_VARGA_RULES_REGISTRY,
        BRIHAT_JATAKA_EXT_REGISTRY,
        PHALA_DEEPIKA_EXT_REGISTRY,
        UTTARA_KALAMRITA_EXT_REGISTRY,
        JATAKA_PARIJATA_EXT_REGISTRY,
        TRANSIT_RULES_REGISTRY,
        ASHTAKAVARGA_RULES_REGISTRY,
        JAIMINI_SUTRAS_RULES_REGISTRY,
        SHADBALA_RULES_REGISTRY,
        DASHA_SYSTEMS_RULES_REGISTRY,
        YOGA_EXTENDED_RULES_REGISTRY,
        LAGNA_EXTENDED_RULES_REGISTRY,
        BHAVA_PHALA_RULES_REGISTRY,
        GRAHA_PHALA_RULES_REGISTRY,
        BPHS_GRAHA_BHAVA_COMPLETE_REGISTRY,
        BPHS_YOGA_EXHAUSTIVE_REGISTRY,
        BPHS_BHAVA_EXHAUSTIVE_REGISTRY,
        BPHS_GRAHA_CHARACTERISTICS_REGISTRY,
        BRIHAT_JATAKA_EXHAUSTIVE_REGISTRY,
        UTTARA_KALAMRITA_EXHAUSTIVE_REGISTRY,
        JATAKA_PARIJATA_EXHAUSTIVE_REGISTRY,
        SARVARTHA_CHINTAMANI_EXHAUSTIVE_REGISTRY,
        JAIMINI_SUTRAS_EXHAUSTIVE_REGISTRY,
        LAL_KITAB_RULES_REGISTRY,
        CHANDRA_KALA_NADI_REGISTRY,
        PHALADEEPIKA_EXHAUSTIVE_REGISTRY,
        LAGHU_PARASHARI_FUNCTIONAL_REGISTRY,
        LAGHU_PARASHARI_YOGAKARAKA_REGISTRY,
        LAGHU_PARASHARI_KENDRADHIPATI_REGISTRY,
        LAGHU_PARASHARI_DASHA_REGISTRY,
        LAGHU_PARASHARI_ANTARDASHA_REGISTRY,
        LAGHU_PARASHARI_MARAKA_REGISTRY,
        BHAVARTHA_RATNAKARA_1_REGISTRY,
        BHAVARTHA_RATNAKARA_2_REGISTRY,
        BHAVARTHA_RATNAKARA_3_REGISTRY,
        BHAVARTHA_RATNAKARA_4_REGISTRY,
        BHAVARTHA_RATNAKARA_5_REGISTRY,
        BHAVARTHA_RATNAKARA_6_REGISTRY,
        SARAVALI_CONJUNCTIONS_1_REGISTRY,
        SARAVALI_CONJUNCTIONS_2_REGISTRY,
        SARAVALI_CONJUNCTIONS_3_REGISTRY,
        SARAVALI_CONJUNCTIONS_4_REGISTRY,
        SARAVALI_CONJUNCTIONS_5_REGISTRY,
        SARAVALI_CONJUNCTIONS_6_REGISTRY,
        SARAVALI_CONJUNCTIONS_7_REGISTRY,
        SARAVALI_CONJUNCTIONS_8_REGISTRY,
        SARAVALI_SIGNS_1_REGISTRY,
        SARAVALI_SIGNS_2_REGISTRY,
        SARAVALI_SIGNS_3_REGISTRY,
        SARAVALI_SIGNS_4_REGISTRY,
        SARAVALI_SIGNS_5_REGISTRY,
        SARAVALI_SIGNS_6_REGISTRY,
        SARAVALI_SIGNS_7_REGISTRY,
        SARAVALI_SIGNS_8_REGISTRY,
        SARAVALI_HOUSES_1_REGISTRY,
        SARAVALI_HOUSES_2_REGISTRY,
        SARAVALI_HOUSES_3_REGISTRY,
        SARAVALI_HOUSES_4_REGISTRY,
        SARAVALI_HOUSES_5_REGISTRY,
        SARAVALI_HOUSES_6_REGISTRY,
        SARAVALI_HOUSES_7_REGISTRY,
        SARAVALI_HOUSES_8_REGISTRY,
        SARAVALI_SPECIAL_1_REGISTRY,
        SARAVALI_SPECIAL_2_REGISTRY,
        SARAVALI_SPECIAL_3_REGISTRY,
        SARAVALI_SPECIAL_4_REGISTRY,
        SARAVALI_SPECIAL_5_REGISTRY,
        SARAVALI_SPECIAL_6_REGISTRY,
        SARAVALI_SPECIAL_7_REGISTRY,
        SARAVALI_SPECIAL_8_REGISTRY,
        SARAVALI_SPECIAL_9_REGISTRY,
    ]
    for source_reg in sources:
        for rule in source_reg.all():
            registry.add(rule)
    # Apply concordance data (generated by tools/backfill_phase1b.py)
    try:
        from src.corpus.concordance_map import get_concordance, get_divergence, mechanical_confidence
        for rule in registry.all():
            if rule.phase.startswith("1B"):
                conc = get_concordance(rule.rule_id)
                div = get_divergence(rule.rule_id)
                if conc:
                    rule.concordance_texts = conc
                if div:
                    rule.divergence_notes = ", ".join(div)
                rule.confidence = mechanical_confidence(rule.rule_id, bool(rule.verse_ref))
    except ImportError:
        pass  # concordance_map not yet generated
    # Apply S305 derived fields from descriptions
    _apply_derived_fields(registry)
    # Apply modifiers/exceptions from descriptions
    _apply_modifiers(registry)
    return registry


def _apply_modifiers(registry: CorpusRegistry) -> None:
    """Extract modifiers and exceptions from descriptions at build time."""
    from src.corpus.modifier_extractor import extract_modifiers_from_description
    for rule in registry.all():
        if not rule.phase.startswith("1B"):
            continue
        if rule.modifiers:  # already populated manually — don't overwrite
            continue
        mods, excs = extract_modifiers_from_description(rule.description)
        if mods:
            rule.modifiers = mods
        if excs and not rule.exceptions:
            rule.exceptions = excs


def _apply_derived_fields(registry: CorpusRegistry) -> None:
    """Derive S305 fields from rule descriptions at build time.

    Machine-derivable: prediction_type, gender_scope, certainty_level,
    strength_condition, ayanamsha_sensitive, evaluation_method, dasha_scope.
    """
    import re

    trait_words = {'personality', 'nature', 'character', 'temperament', 'appearance',
        'build', 'complexion', 'demeanor', 'disposition', 'constitution', 'bearing',
        'body', 'physique', 'stature'}
    event_words = {'marriage', 'death', 'accident', 'promotion', 'birth of child',
        'travel abroad', 'job loss', 'inheritance', 'litigation', 'surgery',
        'divorce'}
    female_words = {'female', 'woman', 'wife', 'stri jataka'}
    vague_pats = [re.compile(p) for p in [r'\bmay\b', r'\bmight\b', r'\bpossibly\b', r'\btends\b']]
    strength_map = [
        ('exalted', 'exalted'), ('debilitated', 'debilitated'),
        ('own sign', 'own_sign'), ('moolatrikona', 'moolatrikona'),
        ('combust', 'combust'),
    ]
    eval_map = {
        'house_placement': 'placement_check', 'sign_placement': 'placement_check',
        'conjunction_in_house': 'placement_check', 'conjunction_condition': 'placement_check',
        'multi_conjunction': 'placement_check', 'yoga': 'yoga_detection',
        'yogakaraka_designation': 'lordship_check', 'kendradhipati_doctrine': 'lordship_check',
        'maraka_designation': 'lordship_check', 'house_lordship': 'lordship_check',
        'house_lordship_dasha': 'dasha_activation', 'antardasha_combination': 'dasha_activation',
        'sign_condition': 'placement_check', 'house_condition': 'placement_check',
        'special': 'placement_check', 'general_condition': 'placement_check',
    }

    for rule in registry.all():
        if not rule.phase.startswith("1B"):
            continue

        desc = rule.description.lower()
        pc = rule.primary_condition
        ptype = pc.get("placement_type", "")
        planet = pc.get("planet", "")

        # prediction_type
        t_score = sum(1 for w in trait_words if w in desc)
        e_score = sum(1 for w in event_words if w in desc)
        if t_score > e_score:
            rule.prediction_type = "trait"
            # Fix outcome_timing: traits should not be dasha_dependent
            if rule.outcome_timing == "dasha_dependent":
                rule.outcome_timing = "natal_permanent"
        else:
            rule.prediction_type = "event"

        # gender_scope
        if any(w in desc for w in female_words):
            rule.gender_scope = "female"
        else:
            rule.gender_scope = "universal"

        # certainty_level
        if any(p.search(desc) for p in vague_pats):
            rule.certainty_level = "possible"
        else:
            rule.certainty_level = "definite"

        # strength_condition
        for keyword, value in strength_map:
            if keyword in desc:
                rule.strength_condition = value
                break

        # ayanamsha_sensitive
        rule.ayanamsha_sensitive = (ptype == "sign_placement")

        # evaluation_method
        rule.evaluation_method = eval_map.get(ptype, "placement_check")

        # dasha_scope — derive from planet in primary_condition
        if rule.outcome_timing == "dasha_dependent" and not rule.dasha_scope:
            if planet and planet not in ("general", "house_lord", "none", "nodes"):
                # For conjunction rules (sun_moon), both planets are dasha lords
                if "_" in planet:
                    parts = [p.strip() for p in planet.split("_")
                             if p.strip() not in ("general", "planet", "conjunction")]
                    rule.dasha_scope = parts
                else:
                    rule.dasha_scope = [planet]


# Module-level singleton — import this for general use
COMBINED_CORPUS: CorpusRegistry = build_corpus()
