"""Tests for migration registry — V1/V2 coexistence tracking."""
from __future__ import annotations


def test_registry_initial_state():
    """Unknown chapters return unaudited default."""
    from src.corpus.migration_registry import get_status
    status = get_status("BPHS", "Ch.999")
    assert status["status"] == "unaudited"
    assert status["verse_coverage"] == 0.0


def test_registry_verified_chapter():
    """is_verified returns False for unknown chapters."""
    from src.corpus.migration_registry import is_verified
    assert is_verified("BPHS", "Ch.999") is False


def test_registry_has_expected_structure():
    """Default status dict has required fields."""
    from src.corpus.migration_registry import get_status
    status = get_status("BR", "Ch.2")
    for field in ("status", "verse_coverage", "v1_rules", "v2_rules",
                  "finding", "verified_session"):
        assert field in status, f"Missing required field: {field}"


def test_registry_verse_verified_chapters():
    """All 15 V2 chapters should be verse_verified in registry."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified
    expected = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29]
    for n in expected:
        key = ("BPHS", f"Ch.{n}")
        assert key in MIGRATION_REGISTRY, f"Ch.{n} not in registry"
        assert is_verified("BPHS", f"Ch.{n}"), f"Ch.{n} not verse_verified"


def test_registry_is_verified_checks_status():
    """is_verified only returns True for verse_verified status."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified
    # Temporarily add an audited (not verified) entry
    MIGRATION_REGISTRY[("TEST", "Ch.1")] = {"status": "audited"}
    assert is_verified("TEST", "Ch.1") is False
    # Clean up
    del MIGRATION_REGISTRY[("TEST", "Ch.1")]


def test_registry_findings_non_empty():
    """Every verse_verified chapter should have a non-empty finding."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY
    for key, entry in MIGRATION_REGISTRY.items():
        if entry["status"] == "verse_verified":
            assert entry.get("finding"), f"{key} has empty finding"
