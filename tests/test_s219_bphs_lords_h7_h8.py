"""tests/test_s219_bphs_lords_h7_h8.py — S219: BPHS 7th lord + 8th lord in houses."""
from __future__ import annotations


def test_bphs_lords_h7_h8_count():
    from src.corpus.bphs_lords_h7_h8 import BPHS_LORDS_H7_H8_REGISTRY
    assert BPHS_LORDS_H7_H8_REGISTRY.count() == 24


def test_bphs_lords_h7_h8_ids():
    from src.corpus.bphs_lords_h7_h8 import BPHS_LORDS_H7_H8_REGISTRY
    ids = {r.rule_id for r in BPHS_LORDS_H7_H8_REGISTRY.all()}
    for prefix in ("H7L", "H8L"):
        for i in range(1, 13):
            assert f"{prefix}{i:03d}" in ids


def test_h7l007_own_house_strong_marriage():
    from src.corpus.bphs_lords_h7_h8 import BPHS_LORDS_H7_H8_REGISTRY
    rule = BPHS_LORDS_H7_H8_REGISTRY.get("H7L007")
    assert rule is not None
    assert "own" in rule.description.lower() or "own_house" in rule.keyword_tags
