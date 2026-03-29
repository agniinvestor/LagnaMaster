"""tests/test_s218_bphs_lords_h5_h6.py — S218: BPHS 5th lord + 6th lord in houses."""
from __future__ import annotations


def test_bphs_lords_h5_h6_count():
    from src.corpus.bphs_lords_h5_h6 import BPHS_LORDS_H5_H6_REGISTRY
    assert BPHS_LORDS_H5_H6_REGISTRY.count() == 24


def test_bphs_lords_h5_h6_ids():
    from src.corpus.bphs_lords_h5_h6 import BPHS_LORDS_H5_H6_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H5_H6_REGISTRY.all()}
    for prefix in ("H5L", "H6L"):
        for i in range(1, 13):
            assert f"{prefix}{i:03d}" in ids


def test_viparita_yoga_in_h6_rules():
    """H6L006 should mention viparita raja yoga."""
    from src.corpus.bphs_lords_h5_h6 import BPHS_LORDS_H5_H6_REGISTRY
    rule = BPHS_LORDS_H5_H6_REGISTRY.get("H6L006")
    assert rule is not None
    assert "viparita" in rule.description.lower()
