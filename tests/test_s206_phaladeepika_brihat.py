"""
tests/test_s206_phaladeepika_brihat.py — S206: Phaladeepika + Brihat Jataka rule encoding

Two more classical texts encoded as RuleRecords. Combined corpus now
exceeds 100 rules — significant corpus depth milestone.
"""

from __future__ import annotations


# ── Phaladeepika rules ────────────────────────────────────────────────────────

def test_phaladeepika_registry_import():
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    assert PHALADEEPIKA_REGISTRY is not None


def test_phaladeepika_at_least_20_rules():
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    assert PHALADEEPIKA_REGISTRY.count() >= 20, (
        f"Expected ≥20 Phaladeepika rules, got {PHALADEEPIKA_REGISTRY.count()}"
    )


def test_phaladeepika_all_source_correct():
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    for r in PHALADEEPIKA_REGISTRY.all():
        assert r.source == "Phaladeepika", (
            f"{r.rule_id}: source={r.source!r}, expected 'Phaladeepika'"
        )


# ── Brihat Jataka rules ───────────────────────────────────────────────────────

def test_brihat_jataka_registry_import():
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    assert BRIHAT_JATAKA_REGISTRY is not None


def test_brihat_jataka_at_least_20_rules():
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    assert BRIHAT_JATAKA_REGISTRY.count() >= 20, (
        f"Expected ≥20 Brihat Jataka rules, got {BRIHAT_JATAKA_REGISTRY.count()}"
    )


def test_brihat_jataka_all_source_correct():
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    for r in BRIHAT_JATAKA_REGISTRY.all():
        assert r.source == "Brihat Jataka", (
            f"{r.rule_id}: source={r.source!r}"
        )


# ── Combined corpus milestone ─────────────────────────────────────────────────

def test_combined_corpus_exceeds_100_rules():
    """Corpus milestone: R01-R23 + B001-B031 + PH + BJ > 100 rules."""
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    total = (
        EXISTING_RULES_REGISTRY.count()
        + BPHS_EXTENDED_REGISTRY.count()
        + PHALADEEPIKA_REGISTRY.count()
        + BRIHAT_JATAKA_REGISTRY.count()
    )
    assert total > 100, f"Expected >100 rules in combined corpus, got {total}"


def test_no_id_collisions_across_registries():
    """All rule IDs must be unique across all registries."""
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.phaladeepika_rules import PHALADEEPIKA_REGISTRY
    from src.corpus.brihat_jataka_rules import BRIHAT_JATAKA_REGISTRY
    all_ids = []
    for reg in [EXISTING_RULES_REGISTRY, BPHS_EXTENDED_REGISTRY,
                PHALADEEPIKA_REGISTRY, BRIHAT_JATAKA_REGISTRY]:
        all_ids.extend(r.rule_id for r in reg.all())
    assert len(all_ids) == len(set(all_ids)), (
        "Duplicate rule IDs found across registries"
    )
