"""
tests/test_s205_corpus_audit.py — S205: CorpusAudit + 30 new BPHS rules

The audit script checks corpus completeness, detects gaps, and reports
unimplemented rules. BPHS encoding expands corpus beyond R01-R23.
"""

from __future__ import annotations


# ── CorpusAudit ───────────────────────────────────────────────────────────────

def test_corpus_audit_import():
    from src.corpus.corpus_audit import CorpusAudit
    assert CorpusAudit is not None


def test_corpus_audit_run_returns_report():
    from src.corpus.corpus_audit import CorpusAudit
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    audit = CorpusAudit(EXISTING_RULES_REGISTRY)
    report = audit.run()
    assert "total_rules" in report
    assert "implemented_count" in report
    assert "unimplemented_count" in report
    assert "by_school" in report
    assert "by_category" in report


def test_corpus_audit_implemented_count():
    from src.corpus.corpus_audit import CorpusAudit
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    audit = CorpusAudit(EXISTING_RULES_REGISTRY)
    report = audit.run()
    assert report["implemented_count"] == 23


def test_corpus_audit_text_output():
    from src.corpus.corpus_audit import CorpusAudit
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    audit = CorpusAudit(EXISTING_RULES_REGISTRY)
    txt = audit.text_report()
    assert "total" in txt.lower() or "rules" in txt.lower()


# ── BPHS extended rules ───────────────────────────────────────────────────────

def test_bphs_extended_import():
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    assert BPHS_EXTENDED_REGISTRY is not None


def test_bphs_extended_at_least_30_rules():
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    assert BPHS_EXTENDED_REGISTRY.count() >= 30, (
        f"Expected ≥30 BPHS extended rules, got {BPHS_EXTENDED_REGISTRY.count()}"
    )


def test_bphs_extended_all_have_source():
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    for r in BPHS_EXTENDED_REGISTRY.all():
        assert r.source == "BPHS", f"{r.rule_id} source={r.source!r}, expected BPHS"


def test_bphs_extended_no_collision_with_existing():
    """Extended BPHS rules must not duplicate R01-R23 IDs."""
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    existing_ids = {r.rule_id for r in EXISTING_RULES_REGISTRY.all()}
    ext_ids = {r.rule_id for r in BPHS_EXTENDED_REGISTRY.all()}
    overlap = existing_ids & ext_ids
    assert not overlap, f"ID collision between existing and extended: {overlap}"


def test_bphs_extended_confidence_values():
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    for r in BPHS_EXTENDED_REGISTRY.all():
        assert 0.0 <= r.confidence <= 1.0, f"{r.rule_id} confidence out of range"


def test_combined_corpus_over_50_rules():
    """Existing + extended BPHS together should exceed 50 rules."""
    from src.corpus.bphs_extended import BPHS_EXTENDED_REGISTRY
    from src.corpus.existing_rules import EXISTING_RULES_REGISTRY
    total = EXISTING_RULES_REGISTRY.count() + BPHS_EXTENDED_REGISTRY.count()
    assert total > 50, f"Expected >50 total rules, got {total}"
