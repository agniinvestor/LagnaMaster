"""Tests for migration audit matching and reporting."""
from __future__ import annotations


def test_match_full_domain_and_mechanism():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable", "mechanisms": ["authority"],
           "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable",
            "mechanisms": ["authority", "virtue"]}]
    assert match_v1_to_v2(v1, v2s) == "FULL"


def test_match_partial_mechanism_missing():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable",
           "mechanisms": ["authority", "taxation"], "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable",
            "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "PARTIAL"


def test_match_gap_critical_no_domain():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "health_unfavorable",
           "mechanisms": ["digestive"], "confidence": 0.9}
    v2s = [{"domain_direction": "wealth_favorable",
            "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "GAP_CRITICAL"


def test_match_unmapped_low_confidence():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "", "mechanisms": [], "confidence": 0.2}
    v2s = [{"domain_direction": "wealth_favorable", "mechanisms": []}]
    assert match_v1_to_v2(v1, v2s) == "UNMAPPED"


def test_match_full_no_mechanisms():
    from tools.migration_audit import match_v1_to_v2
    v1 = {"domain_direction": "wealth_favorable", "mechanisms": [],
           "confidence": 0.8}
    v2s = [{"domain_direction": "wealth_favorable",
            "mechanisms": ["authority"]}]
    assert match_v1_to_v2(v1, v2s) == "FULL"


def test_audit_chapter_returns_report():
    from tools.migration_audit import audit_chapter
    report = audit_chapter("BPHS", "Ch.29")
    assert report["chapter"] == "Ch.29"
    assert "matching" in report
    assert report["v1_rules"] >= 0
    assert report["v2_rules_same_chapter"] >= 0
