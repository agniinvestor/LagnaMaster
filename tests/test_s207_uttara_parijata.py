"""
tests/test_s207_uttara_parijata.py — S207: Uttara Kalamrita + Jataka Parijata rules

Two more classical texts encoded. Uttara Kalamrita is famous for timing
and special ascendant rules. Jataka Parijata for dignity and yoga combinations.
"""

from __future__ import annotations


def test_uttara_kalamrita_import():
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    assert UTTARA_KALAMRITA_REGISTRY is not None


def test_uttara_kalamrita_at_least_15_rules():
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    assert UTTARA_KALAMRITA_REGISTRY.count() >= 15


def test_uttara_kalamrita_source_correct():
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    for r in UTTARA_KALAMRITA_REGISTRY.all():
        assert r.source == "Uttara Kalamrita"


def test_jataka_parijata_import():
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    assert JATAKA_PARIJATA_REGISTRY is not None


def test_jataka_parijata_at_least_15_rules():
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    assert JATAKA_PARIJATA_REGISTRY.count() >= 15


def test_jataka_parijata_source_correct():
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    for r in JATAKA_PARIJATA_REGISTRY.all():
        assert r.source == "Jataka Parijata"


def test_five_text_corpus_over_130_rules():
    """After 5 texts: R01-R23 + BPHS + Phala + BJ + UK + JP > 130 rules."""
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    total = sum(r.count() for r in [
        EXISTING_RULES_REGISTRY, BPHS_EXTENDED_REGISTRY,
        PHALADEEPIKA_REGISTRY, BRIHAT_JATAKA_REGISTRY,
        UTTARA_KALAMRITA_REGISTRY, JATAKA_PARIJATA_REGISTRY,
    ])
    assert total > 130, f"Expected >130 corpus rules, got {total}"


def test_no_id_collisions_six_registries():
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    from src.corpus.uttara_kalamrita_rules import UTTARA_KALAMRITA_REGISTRY
    from src.corpus.jataka_parijata_rules import JATAKA_PARIJATA_REGISTRY
    all_ids = []
    for reg in [EXISTING_RULES_REGISTRY, BPHS_EXTENDED_REGISTRY,
                PHALADEEPIKA_REGISTRY, BRIHAT_JATAKA_REGISTRY,
                UTTARA_KALAMRITA_REGISTRY, JATAKA_PARIJATA_REGISTRY]:
        all_ids.extend(r.rule_id for r in reg.all())
    assert len(all_ids) == len(set(all_ids)), "Duplicate IDs across registries"
