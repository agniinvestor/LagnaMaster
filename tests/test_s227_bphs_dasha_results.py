"""tests/test_s227_bphs_dasha_results.py — S227: BPHS Vimshottari dasha result rules."""
from __future__ import annotations


def test_bphs_dasha_results_count():
    from src.corpus.bphs_dasha_results import BPHS_DASHA_RESULTS_REGISTRY
    assert BPHS_DASHA_RESULTS_REGISTRY.count() == 20


def test_all_nine_planets_have_maha_dasha_rule():
    from src.corpus.bphs_dasha_results import BPHS_DASHA_RESULTS_REGISTRY
    ids = {r.rule_id for r in BPHS_DASHA_RESULTS_REGISTRY.all()}
    for i in range(1, 10):
        assert f"DAR{i:03d}" in ids, f"DAR{i:03d} missing"


def test_venus_has_longest_dasha():
    from src.corpus.bphs_dasha_results import BPHS_DASHA_RESULTS_REGISTRY
    rule = BPHS_DASHA_RESULTS_REGISTRY.get("DAR009")
    assert rule is not None
    assert "20" in rule.description  # 20-year period


def test_dasha_yoga_activation_rule():
    from src.corpus.bphs_dasha_results import BPHS_DASHA_RESULTS_REGISTRY
    rule = BPHS_DASHA_RESULTS_REGISTRY.get("DAR014")
    assert rule is not None
    assert "yoga_activation" in rule.tags
