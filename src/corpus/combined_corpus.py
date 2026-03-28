"""
src/corpus/combined_corpus.py — Combined Corpus Loader (S208)

Loads all classical text registries into a single CorpusRegistry.
This is the authoritative corpus for Phase 1 encoding targets and
Phase 6 SHAP analysis (after OSF pre-registration per G22).

Current sources loaded:
  - R01-R23    existing_rules (implemented)
  - B001-B031  bphs_extended
  - PH001-PH021 phaladeepika_rules
  - BJ001-BJ026 brihat_jataka_rules
  - UK001-UK017 uttara_kalamrita_rules
  - JP001-JP017 jataka_parijata_rules

Public API
----------
  COMBINED_CORPUS   — pre-populated CorpusRegistry singleton
  build_corpus()    — rebuild fresh (for testing or extension)
"""

from __future__ import annotations

from src.corpus.registry import CorpusRegistry


def build_corpus() -> CorpusRegistry:
    """Build a fresh combined corpus from all registered sources."""
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY

    registry = CorpusRegistry()
    sources = [
        EXISTING_RULES_REGISTRY,
        BPHS_EXTENDED_REGISTRY,
        PHALADEEPIKA_REGISTRY,
        BRIHAT_JATAKA_REGISTRY,
        UTTARA_KALAMRITA_REGISTRY,
        JATAKA_PARIJATA_REGISTRY,
    ]
    for source_reg in sources:
        for rule in source_reg.all():
            registry.add(rule)
    return registry


# Module-level singleton — import this for general use
COMBINED_CORPUS: CorpusRegistry = build_corpus()
