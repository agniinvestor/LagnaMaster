"""tests/test_s221_bphs_lords_h11_h12.py — S221: BPHS 11th + 12th lord in houses (completes 144-rule lord set)."""
from __future__ import annotations


def test_bphs_lords_h11_h12_count():
    from src.corpus.bphs_lords_h11_h12 import BPHS_LORDS_H11_H12_REGISTRY
    assert BPHS_LORDS_H11_H12_REGISTRY.count() == 24


def test_bphs_lords_h11_h12_ids():
    from src.corpus.bphs_lords_h11_h12 import BPHS_LORDS_H11_H12_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H11_H12_REGISTRY.all()}
    for prefix in ("H11L", "H12L"):
        for i in range(1, 13):
            assert f"{prefix}{i:03d}" in ids


def test_combined_corpus_has_all_144_lord_rules():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    ids = {r.rule_id for r in registry.all()}
    # All 12 lords × 12 houses = 144 rules
    for n in range(1, 13):
        prefix = f"H{n}L"
        for h in range(1, 13):
            assert f"{prefix}{h:03d}" in ids, f"Missing {prefix}{h:03d}"


def test_combined_corpus_count_after_s221():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 279  # 135 + 144
