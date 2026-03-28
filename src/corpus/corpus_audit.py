"""
src/corpus/corpus_audit.py — Corpus Completeness Audit (S205)

Audits a CorpusRegistry for completeness gaps, unimplemented rules,
and distribution across schools and categories. Used by CI and the
S201-S210 checkpoint to verify corpus quality.

Public API
----------
  CorpusAudit(registry)   — audit runner
  .run() -> dict          — structured report
  .text_report() -> str   — human-readable summary
"""

from __future__ import annotations

from src.corpus.registry import CorpusRegistry


class CorpusAudit:
    """Run completeness checks on a CorpusRegistry."""

    def __init__(self, registry: CorpusRegistry) -> None:
        self.registry = registry

    def run(self) -> dict:
        """Return a structured audit report."""
        rules = self.registry.all()
        total = len(rules)
        implemented = [r for r in rules if r.implemented]
        unimplemented = [r for r in rules if not r.implemented]

        by_school: dict[str, int] = {}
        by_category: dict[str, int] = {}
        by_source: dict[str, int] = {}
        low_confidence: list[str] = []

        for r in rules:
            by_school[r.school] = by_school.get(r.school, 0) + 1
            by_category[r.category] = by_category.get(r.category, 0) + 1
            by_source[r.source] = by_source.get(r.source, 0) + 1
            if r.confidence < 0.7:
                low_confidence.append(r.rule_id)

        return {
            "total_rules": total,
            "implemented_count": len(implemented),
            "unimplemented_count": len(unimplemented),
            "unimplemented_ids": [r.rule_id for r in unimplemented],
            "by_school": by_school,
            "by_category": by_category,
            "by_source": by_source,
            "low_confidence_ids": low_confidence,
            "errors": [],
        }

    def text_report(self) -> str:
        """Human-readable corpus audit summary."""
        r = self.run()
        lines = [
            f"Corpus Audit: {r['total_rules']} total rules",
            f"  Implemented:   {r['implemented_count']}",
            f"  Unimplemented: {r['unimplemented_count']}",
        ]
        lines.append("\nBy school:")
        for s, n in sorted(r["by_school"].items()):
            lines.append(f"  {s}: {n}")
        lines.append("\nBy category:")
        for c, n in sorted(r["by_category"].items()):
            lines.append(f"  {c}: {n}")
        lines.append("\nBy source:")
        for src, n in sorted(r["by_source"].items()):
            lines.append(f"  {src}: {n}")
        if r["unimplemented_ids"]:
            lines.append(f"\nUnimplemented: {', '.join(r['unimplemented_ids'][:10])}"
                         + (" ..." if len(r["unimplemented_ids"]) > 10 else ""))
        if r["low_confidence_ids"]:
            lines.append(f"Low confidence (<0.7): {', '.join(r['low_confidence_ids'])}")
        return "\n".join(lines)
