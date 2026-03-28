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
    ]
    for source_reg in sources:
        for rule in source_reg.all():
            registry.add(rule)
    return registry


# Module-level singleton — import this for general use
COMBINED_CORPUS: CorpusRegistry = build_corpus()
