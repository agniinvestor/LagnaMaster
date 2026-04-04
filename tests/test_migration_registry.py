"""Tests for migration registry — per-chapter audit state tracking."""
from __future__ import annotations


def test_registry_initial_state():
    """Registry starts empty and returns unaudited by default."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, get_status

    # Clear registry for this test
    MIGRATION_REGISTRY.clear()

    status = get_status("BPHS", "Ch.1")
    assert status["status"] == "unaudited"
    assert status["coverage"] == 0.0
    assert status["confidence"] == 0.0


def test_registry_verified_chapter():
    """is_verified returns False for unknown chapters."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear registry for this test
    MIGRATION_REGISTRY.clear()

    # Unknown chapter should return False
    assert is_verified("BPHS", "Ch.999") is False


def test_registry_has_expected_structure():
    """All entries have required fields in default dict."""
    from src.corpus.migration_registry import get_status

    status = get_status("BR", "Ch.2")

    # Check all required fields exist
    required_fields = [
        "status",
        "coverage",
        "full_count",
        "partial_count",
        "gap_critical_count",
        "unmapped_count",
        "confidence",
        "verified_at",
        "verified_session",
        "partial_annotations",
        "notes",
    ]

    for field in required_fields:
        assert field in status, f"Missing required field: {field}"


def test_registry_verified_requires_status_verified():
    """is_verified returns False if status is not exactly 'verified'."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear and add entry with status="audited"
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "audited",
        "coverage": 1.0,
        "full_count": 10,
        "partial_count": 0,
        "gap_critical_count": 0,
        "unmapped_count": 0,
        "confidence": 0.8,
        "verified_at": "",
        "verified_session": "",
        "partial_annotations": [],
        "notes": "",
    }

    assert is_verified("BPHS", "Ch.1") is False


def test_registry_verified_blocks_on_gap_critical():
    """is_verified returns False if gap_critical_count > 0."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear and add entry with gap_critical_count > 0
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "verified",
        "coverage": 0.9,
        "full_count": 10,
        "partial_count": 0,
        "gap_critical_count": 1,
        "unmapped_count": 0,
        "confidence": 0.8,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [],
        "notes": "",
    }

    assert is_verified("BPHS", "Ch.1") is False


def test_registry_verified_blocks_on_unannotated_partials():
    """is_verified returns False if partial_annotations missing."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear and add entry with unannotated partials
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "verified",
        "coverage": 0.9,
        "full_count": 10,
        "partial_count": 2,
        "gap_critical_count": 0,
        "unmapped_count": 0,
        "confidence": 0.8,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [{"rule_id": "1", "annotation": "note"}],
        "notes": "",
    }

    # Only 1 annotation for 2 partials
    assert is_verified("BPHS", "Ch.1") is False


def test_registry_verified_blocks_on_low_confidence():
    """is_verified returns False if confidence < 0.7."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear and add entry with low confidence
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "verified",
        "coverage": 0.8,
        "full_count": 10,
        "partial_count": 0,
        "gap_critical_count": 0,
        "unmapped_count": 0,
        "confidence": 0.6,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [],
        "notes": "",
    }

    assert is_verified("BPHS", "Ch.1") is False


def test_registry_verified_passes_all_gates():
    """is_verified returns True when all gates pass."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Clear and add entry that passes all gates
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "verified",
        "coverage": 0.95,
        "full_count": 50,
        "partial_count": 2,
        "gap_critical_count": 0,
        "unmapped_count": 1,
        "confidence": 0.8,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [
            {"rule_id": "1", "annotation": "note 1"},
            {"rule_id": "2", "annotation": "note 2"},
        ],
        "notes": "Audit complete, confidence high",
    }

    assert is_verified("BPHS", "Ch.1") is True


def test_registry_verified_confidence_boundary():
    """is_verified passes at confidence==0.7 but fails at 0.69."""
    from src.corpus.migration_registry import MIGRATION_REGISTRY, is_verified

    # Test at boundary: 0.7 should pass
    MIGRATION_REGISTRY.clear()
    MIGRATION_REGISTRY[("BPHS", "Ch.1")] = {
        "status": "verified",
        "coverage": 1.0,
        "full_count": 10,
        "partial_count": 0,
        "gap_critical_count": 0,
        "unmapped_count": 0,
        "confidence": 0.7,
        "verified_at": "2026-04-04",
        "verified_session": "S314",
        "partial_annotations": [],
        "notes": "",
    }

    assert is_verified("BPHS", "Ch.1") is True

    # Test below boundary: 0.69 should fail
    MIGRATION_REGISTRY[("BPHS", "Ch.1")]["confidence"] = 0.69
    assert is_verified("BPHS", "Ch.1") is False
