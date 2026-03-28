"""tests/test_s217_bphs_lords_h3_h4.py — S217: BPHS 3rd lord + 4th lord in houses."""
from __future__ import annotations


def test_bphs_lords_h3_h4_count():
    from src.corpus.bphs_lords_h3_h4 import BPHS_LORDS_H3_H4_REGISTRY
    assert BPHS_LORDS_H3_H4_REGISTRY.count() == 24


def test_bphs_lords_h3_h4_h3l_ids():
    from src.corpus.bphs_lords_h3_h4 import BPHS_LORDS_H3_H4_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H3_H4_REGISTRY.all()}
    for i in range(1, 13):
        assert f"H3L{i:03d}" in ids


def test_bphs_lords_h3_h4_h4l_ids():
    from src.corpus.bphs_lords_h3_h4 import BPHS_LORDS_H3_H4_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H3_H4_REGISTRY.all()}
    for i in range(1, 13):
        assert f"H4L{i:03d}" in ids


def test_combined_corpus_includes_h3_h4_lords():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    ids = {r.rule_id for r in registry.all()}
    assert "H3L001" in ids and "H4L012" in ids
