"""tests/test_s216_bphs_lords_h1_h2.py — S216: BPHS lagna lord + 2nd lord in houses."""
from __future__ import annotations


def test_bphs_lords_h1_h2_importable():
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY  # noqa: F401


def test_bphs_lords_h1_h2_count():
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY
    assert BPHS_LORDS_H1_H2_REGISTRY.count() == 24


def test_bphs_lords_h1_h2_all_parashari():
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY
    for rule in BPHS_LORDS_H1_H2_REGISTRY.all():
        assert rule.school == "parashari", f"{rule.rule_id} wrong school"


def test_bphs_lords_h1_h2_h1l_ids():
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H1_H2_REGISTRY.all()}
    for i in range(1, 13):
        assert f"H1L{i:03d}" in ids, f"H1L{i:03d} missing"


def test_bphs_lords_h1_h2_h2l_ids():
    from src.corpus.bphs_lords_h1_h2 import BPHS_LORDS_H1_H2_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H1_H2_REGISTRY.all()}
    for i in range(1, 13):
        assert f"H2L{i:03d}" in ids, f"H2L{i:03d} missing"


def test_combined_corpus_includes_h1_h2_lords():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    ids = {r.rule_id for r in registry.all()}
    assert "H1L001" in ids
    assert "H2L012" in ids


def test_combined_corpus_count_after_s216():
    from src.corpus.combined_corpus import build_corpus
    registry = build_corpus()
    assert registry.count() >= 159  # 135 + 24
