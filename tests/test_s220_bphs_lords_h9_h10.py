"""tests/test_s220_bphs_lords_h9_h10.py — S220: BPHS 9th lord + 10th lord in houses."""
from __future__ import annotations


def test_bphs_lords_h9_h10_count():
    from src.corpus.bphs_lords_h9_h10 import BPHS_LORDS_H9_H10_REGISTRY
    assert BPHS_LORDS_H9_H10_REGISTRY.count() == 24


def test_bphs_lords_h9_h10_ids():
    from src.corpus.bphs_lords_h9_h10 import BPHS_LORDS_H9_H10_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H9_H10_REGISTRY.all()}
    for prefix in ("H9L", "H10L"):
        for i in range(1, 13):
            assert f"{prefix}{i:03d}" in ids


def test_dharma_karma_adhipati_rule():
    """H10L009 and H9L010 should mention dharma_karma_adhipati."""
    from src.corpus.bphs_lords_h9_h10 import BPHS_LORDS_H9_H10_REGISTRY
    for rule_id in ("H9L010", "H10L009"):
        rule = BPHS_LORDS_H9_H10_REGISTRY.get(rule_id)
        assert rule is not None
        assert "dharma_karma_adhipati" in rule.keyword_tags, \
            f"{rule_id} missing dharma_karma_adhipati tag"
