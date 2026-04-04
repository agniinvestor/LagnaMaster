"""Migration registry — per-chapter audit state for legacy exclusion gating.

Tracks audit progress for each source/chapter pair. Enforces:
- status transitions: unaudited → audited → verified
- verification gate: gap_critical_count==0, all partials annotated, confidence>=0.7
- centralized state for combined_corpus gating decisions

No encoding starts without an entry. Entries created by audit tools.
Verification blocks legacy-to-v2 rules from being encoded.
"""
from __future__ import annotations


MIGRATION_REGISTRY: dict[tuple[str, str], dict] = {}


def _default_status_dict() -> dict:
    """Return default unaudited status dict with all required fields."""
    return {
        "status": "unaudited",
        "coverage": 0.0,
        "full_count": 0,
        "partial_count": 0,
        "gap_critical_count": 0,
        "unmapped_count": 0,
        "confidence": 0.0,
        "verified_at": "",
        "verified_session": "",
        "partial_annotations": [],
        "notes": "",
    }


def get_status(source: str, chapter: str) -> dict:
    """Get audit status for (source, chapter), returns default if not found.

    Args:
        source: source identifier (e.g., "BPHS", "BR")
        chapter: chapter identifier (e.g., "Ch.1", "Ch.16")

    Returns:
        Status dict with status, coverage, confidence, etc.
        Returns default unaudited dict if entry not found.
    """
    key = (source, chapter)
    if key not in MIGRATION_REGISTRY:
        return _default_status_dict()
    return MIGRATION_REGISTRY[key]


def is_verified(source: str, chapter: str) -> bool:
    """Check if (source, chapter) has passed verification gate.

    Verification gate:
    - status=="verified"
    - gap_critical_count==0
    - all partial_annotations filled (len == partial_count)
    - confidence>=0.7

    Args:
        source: source identifier (e.g., "BPHS", "BR")
        chapter: chapter identifier (e.g., "Ch.1", "Ch.16")

    Returns:
        True only if all verification conditions met. False otherwise.
    """
    entry = get_status(source, chapter)

    # Must be explicitly marked as verified
    if entry.get("status") != "verified":
        return False

    # No critical gaps
    if entry.get("gap_critical_count", 0) != 0:
        return False

    # All partials must be annotated
    partial_count = entry.get("partial_count", 0)
    annotations_count = len(entry.get("partial_annotations", []))
    if annotations_count != partial_count:
        return False

    # Confidence threshold
    if entry.get("confidence", 0.0) < 0.7:
        return False

    return True
