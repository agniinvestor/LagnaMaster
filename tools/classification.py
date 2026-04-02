"""
Three-category classification for cross-engine disagreements.

After diff_engine_core produces per-field verdicts, this module
reclassifies 'unclassified_disagreement' into either
'systematic_disagreement' or 'random_disagreement' based on frequency.
"""
from __future__ import annotations

import copy
import math
from collections import Counter
from dataclasses import dataclass

from tools.diff_engine_core import Verdict


@dataclass
class SystematicPattern:
    field_name: str
    error_signature: str
    count: int
    affected_charts: list[str]
    mean_diff: float | None = None


def _error_signature(verdict: Verdict) -> str:
    """Generate a deduplication key for a disagreement."""
    if verdict.diff is not None and verdict.diff > 0:
        magnitude = round(math.log10(max(abs(verdict.diff), 0.001)), 1)
        return f"{verdict.field_name}:magnitude_{magnitude}"
    return f"{verdict.field_name}:categorical_mismatch"


def classify_disagreements(
    all_verdicts: dict[str, dict[str, Verdict]],
    segment_size: int,
) -> dict[str, dict[str, Verdict]]:
    """Reclassify unclassified disagreements into systematic or random.

    Args:
        all_verdicts: {chart_id: {field_name: Verdict}}
        segment_size: Total charts in this segment (for threshold calc).

    Returns:
        Copy of all_verdicts with statuses updated.
    """
    result = copy.deepcopy(all_verdicts)
    threshold = max(10, int(0.25 * segment_size))

    # Count disagreements per (field_name, error_signature)
    pattern_count: Counter[str] = Counter()
    for chart_id, verdicts in all_verdicts.items():
        for field_name, verdict in verdicts.items():
            if verdict.status == "unclassified_disagreement":
                sig = _error_signature(verdict)
                pattern_count[sig] += 1

    # Reclassify
    for chart_id, verdicts in result.items():
        for field_name, verdict in verdicts.items():
            if verdict.status != "unclassified_disagreement":
                continue
            sig = _error_signature(verdict)
            if pattern_count[sig] >= threshold:
                verdict.status = "systematic_disagreement"
                verdict.pattern_id = sig
            else:
                verdict.status = "random_disagreement"

    return result


def deduplicate_patterns(
    verdicts: list[Verdict],
) -> list[SystematicPattern]:
    """Group disagreement verdicts by (field_name, error_signature)."""
    groups: dict[str, list[Verdict]] = {}
    for v in verdicts:
        sig = _error_signature(v)
        groups.setdefault(sig, []).append(v)

    patterns = []
    for sig, vs in groups.items():
        diffs = [v.diff for v in vs if v.diff is not None]
        patterns.append(SystematicPattern(
            field_name=vs[0].field_name,
            error_signature=sig,
            count=len(vs),
            affected_charts=[],
            mean_diff=sum(diffs) / len(diffs) if diffs else None,
        ))
    return patterns
