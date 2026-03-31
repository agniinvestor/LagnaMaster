"""src/corpus/phase1a_deprecation.py — L021: Phase 1A dead weight decision.

DECISION (S311): Phase 1A rules (2,634) are deprecated. They remain in the
corpus for backward compatibility and as a breadth index, but they are:
  - Excluded from V2 audit
  - Excluded from ML feature extraction (Phase 6)
  - Excluded from rule_firing evaluation
  - Excluded from user-facing predictions (Phase 7)
  - Flagged in the scorecard as "legacy_deprecated"

They will be re-encoded at V2 standard as part of the Phase 1B re-encoding
roadmap (S316+ for BPHS, S340+ for other texts). Until then, they are
explicitly non-functional.

Usage:
    from src.corpus.phase1a_deprecation import is_deprecated, deprecation_stats

    if is_deprecated(rule):
        skip_rule()

    stats = deprecation_stats()
    print(stats)  # {"total": 2634, "percentage": 37.7, "status": "awaiting_v2_re-encode"}
"""
from __future__ import annotations


def is_deprecated(rule) -> bool:
    """Check if a rule is Phase 1A deprecated legacy."""
    return rule.phase == "1A_representative"


def is_production_ready(rule) -> bool:
    """Check if a rule meets V2 production standard."""
    if rule.phase == "1A_representative":
        return False
    if not rule.predictions:
        return False
    if not rule.signal_group:
        return False
    if not rule.timing_window:
        return False
    return True


def deprecation_stats() -> dict:
    """Get statistics on deprecated vs production-ready rules."""
    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    all_rules = corpus.all()
    deprecated = [r for r in all_rules if is_deprecated(r)]
    production = [r for r in all_rules if is_production_ready(r)]
    partial = [r for r in all_rules
               if not is_deprecated(r) and not is_production_ready(r)]

    return {
        "total_rules": len(all_rules),
        "deprecated_phase1a": len(deprecated),
        "production_ready_v2": len(production),
        "partial_phase1b": len(partial),
        "deprecated_percentage": round(100 * len(deprecated) / max(len(all_rules), 1), 1),
        "production_percentage": round(100 * len(production) / max(len(all_rules), 1), 1),
        "status": "awaiting_v2_re-encode",
    }
