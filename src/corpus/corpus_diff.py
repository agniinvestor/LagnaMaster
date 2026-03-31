"""src/corpus/corpus_diff.py — Corpus diff tool (Tier 3, Item 5).

Compares two corpus snapshots and reports added, modified, and removed rules.
Critical for Phase 6 (tracking corpus changes between model training runs)
and operational governance (error forensics).

Usage:
    from src.corpus.corpus_diff import diff_snapshots

    result = diff_snapshots("data/corpus_snapshots/snap_a.json",
                            "data/corpus_snapshots/snap_b.json")
    print(result.summary())
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DiffResult:
    """Result of comparing two corpus snapshots."""
    snapshot_a_hash: str = ""
    snapshot_b_hash: str = ""
    snapshot_a_count: int = 0
    snapshot_b_count: int = 0
    added: list[str] = field(default_factory=list)        # rule_ids in B but not A
    removed: list[str] = field(default_factory=list)       # rule_ids in A but not B
    modified: list[dict] = field(default_factory=list)     # {rule_id, field, old, new}
    unchanged: int = 0

    def summary(self) -> str:
        lines = [
            f"Corpus Diff: {self.snapshot_a_hash} → {self.snapshot_b_hash}",
            f"  A: {self.snapshot_a_count} rules, B: {self.snapshot_b_count} rules",
            f"  Added: {len(self.added)}, Removed: {len(self.removed)}, "
            f"Modified: {len(self.modified)}, Unchanged: {self.unchanged}",
        ]
        if self.added:
            lines.append(f"  + Added: {', '.join(self.added[:10])}"
                        + (" ..." if len(self.added) > 10 else ""))
        if self.removed:
            lines.append(f"  - Removed: {', '.join(self.removed[:10])}"
                        + (" ..." if len(self.removed) > 10 else ""))
        if self.modified:
            lines.append("  ~ Modified fields:")
            for m in self.modified[:10]:
                lines.append(f"    {m['rule_id']}.{m['field']}: {m['old']!r} → {m['new']!r}")
        return "\n".join(lines)


# Fields that define rule identity (changes here = meaningful modification)
_IDENTITY_FIELDS = {
    "confidence", "outcome_direction", "outcome_intensity",
    "outcome_domains", "primary_condition", "predictions",
    "entity_target", "timing_window", "modifiers",
}


def diff_snapshots(path_a: str | Path, path_b: str | Path) -> DiffResult:
    """Compare two corpus snapshots."""
    a_data = json.loads(Path(path_a).read_text())
    b_data = json.loads(Path(path_b).read_text())

    a_rules = {r["rule_id"]: r for r in a_data["rules"]}
    b_rules = {r["rule_id"]: r for r in b_data["rules"]}

    result = DiffResult(
        snapshot_a_hash=a_data.get("hash", ""),
        snapshot_b_hash=b_data.get("hash", ""),
        snapshot_a_count=len(a_rules),
        snapshot_b_count=len(b_rules),
    )

    a_ids = set(a_rules.keys())
    b_ids = set(b_rules.keys())

    result.added = sorted(b_ids - a_ids)
    result.removed = sorted(a_ids - b_ids)

    common = a_ids & b_ids
    for rid in sorted(common):
        ra = a_rules[rid]
        rb = b_rules[rid]
        rule_modified = False
        for f in _IDENTITY_FIELDS:
            va = ra.get(f)
            vb = rb.get(f)
            if va != vb:
                result.modified.append({
                    "rule_id": rid, "field": f,
                    "old": va, "new": vb,
                })
                rule_modified = True
        if not rule_modified:
            result.unchanged += 1

    return result
