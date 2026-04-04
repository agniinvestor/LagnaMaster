"""Migration registry — per-chapter audit state for V1/V2 coexistence.

System Philosophy (decided S314):
    V2 rules = VERSE LAYER — canonical, atomic, provably faithful to BPHS text
    V1 rules = DERIVED LAYER — composite, interpretive, includes house
               significations, karaka extensions, and practitioner knowledge

    Both layers coexist in the corpus. V2 is NOT a replacement for V1.
    V1 contains valid astrological knowledge that is not in the BPHS verses.
    The migration audit proves V2 covers all verse content. It does NOT
    prove V1 is redundant.

    Legacy exclusion only applies when V1 rules are truly redundant
    (same claim, same source, same authority level). Most V1 rules
    are DERIVED, not redundant.

Status transitions:
    unaudited → verse_verified (V2 covers all verse claims)
    verse_verified is the terminal state for most chapters.
    Full exclusion requires a separate derivation-layer decision.
"""
from __future__ import annotations


# Per-chapter audit state. Key = (source, chapter).
MIGRATION_REGISTRY: dict[tuple[str, str], dict] = {
    # S314 audit results — all 15 V2 chapters reviewed
    # Status: verse_verified = V2 covers 100% of verse audit claims
    # V1 rules are NOT excluded — they contain derived knowledge
    ("BPHS", "Ch.12"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 26, "v1_excluded": 13, "v2_rules": 22,
        "finding": "V1 adds planet-in-lagna interpretations not in verse. All verse claims encoded.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.13"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 14, "v1_excluded": 12, "v2_rules": 26,
        "finding": "V1 adds planet-in-2nd wealth claims (house signification overlay). Verse covers eyes/speech/disease only.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.14"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 19, "v1_excluded": 11, "v2_rules": 22,
        "finding": "Same pattern — V1 adds house signification overlays.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.15"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 26, "v1_excluded": 13, "v2_rules": 14,
        "finding": "V1 adds Venus/Saturn-in-4th interpretations not in BPHS verse.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.16"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 24, "v1_excluded": 12, "v2_rules": 32,
        "finding": "1 unmapped = extraction failure (5th lord in 1st covered by Ch.24b BPHS2456).",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.17"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 14, "v1_excluded": 24, "v2_rules": 20,
        "finding": "V1 Saturn-victory-in-6th = modern upachaya interpretation, not in verse.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.18"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 18, "v1_excluded": 24, "v2_rules": 42,
        "finding": "Cleanest chapter — 0 unmapped. 27 partials are mechanism-level vocabulary differences.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.19"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 19, "v1_excluded": 26, "v2_rules": 6,
        "finding": "V1 inverts 8th lord in angle ('death-like experiences' vs verse 'long life'). V1 embellishment.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.20"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 22, "v1_excluded": 23, "v2_rules": 30,
        "finding": "Same pattern as other chapters — extraction failures + V1 derived content.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.21"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 19, "v1_excluded": 22, "v2_rules": 20,
        "finding": "All 8 unmapped = extraction failures. Every V1 claim has exact V2 match (same verse, same concept).",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.22"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 11, "v1_excluded": 23, "v2_rules": 10,
        "finding": "All 3 items (1 unmapped + 2 partial) = extraction failures. Zero real gaps.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.23"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 11, "v1_excluded": 28, "v2_rules": 10,
        "finding": "Same pattern — extraction failures and mechanism vocabulary differences.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.24"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 12, "v1_excluded": 27, "v2_rules": 158,
        "finding": "Deep-dived: 4 extraction failures, 1 V1 embellishment (spiritual liberation not in verse), 1 minor note (father's support in Santhanam notes). V2 is verse-faithful.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.25"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 0, "v1_excluded": 30, "v2_rules": 85,
        "finding": "VERSE_ONLY — no relevant V1 category. All V1 rules are cross-chapter noise.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.29"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 0, "v1_excluded": 30, "v2_rules": 40,
        "finding": "VERSE_ONLY — no relevant V1 category. All V1 rules are cross-chapter noise.",
        "verified_session": "S314",
    },
    ("BPHS", "Ch.30"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 0, "v1_excluded": 0, "v2_rules": 46,
        "finding": "Encoded from PDF in S315. 46 rules from 38 predictive slokas. Uses upa_pada + arudha_pada derivations.",
        "verified_session": "S315",
    },
    ("BPHS", "Ch.31"): {
        "status": "verse_verified",
        "verse_coverage": 1.0,
        "v1_rules": 0, "v1_excluded": 0, "v2_rules": 17,
        "finding": "Encoded from PDF in S315. 17 rules from 8 predictive slokas. All NON-COMPUTABLE (need argala_condition primitive). Slokas 1-10 are computational (Argala formation).",
        "verified_session": "S315",
    },
}


def _default_status_dict() -> dict:
    """Return default unaudited status dict with all required fields."""
    return {
        "status": "unaudited",
        "verse_coverage": 0.0,
        "v1_rules": 0,
        "v1_excluded": 0,
        "v2_rules": 0,
        "finding": "",
        "verified_session": "",
    }


def get_status(source: str, chapter: str) -> dict:
    """Get audit status for (source, chapter), returns default if not found."""
    return MIGRATION_REGISTRY.get((source, chapter), _default_status_dict())


def is_verified(source: str, chapter: str) -> bool:
    """Check if chapter's verse layer is verified.

    Note: verse_verified does NOT mean V1 should be excluded.
    V1 contains derived knowledge that may be valuable.
    This only confirms V2 covers all verse-level claims.
    """
    entry = MIGRATION_REGISTRY.get((source, chapter))
    if entry is None:
        return False
    return entry.get("status") == "verse_verified"
