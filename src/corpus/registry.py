"""
src/corpus/registry.py — CorpusRegistry (S202)

Central registry for all classical rule records.
Supports add, get, filter (by school/category/source), and count.

Usage
-----
  from src.corpus.registry import CorpusRegistry
  reg = CorpusRegistry()
  reg.add(rule_record)
  parashari = reg.filter(school="parashari")
"""

from __future__ import annotations

from src.corpus.rule_record import RuleRecord


class CorpusRegistry:
    """In-memory registry of RuleRecord objects."""

    def __init__(self) -> None:
        self._rules: dict[str, RuleRecord] = {}

    def add(self, rule: RuleRecord) -> None:
        """Add a rule. Raises ValueError if rule_id already registered."""
        if rule.rule_id in self._rules:
            raise ValueError(
                f"Duplicate rule_id '{rule.rule_id}' — use a unique identifier"
            )
        self._rules[rule.rule_id] = rule

    def get(self, rule_id: str) -> RuleRecord | None:
        """Return rule by ID, or None if not found."""
        return self._rules.get(rule_id)

    def all(self) -> list[RuleRecord]:
        """Return all rules in insertion order."""
        return list(self._rules.values())

    def filter(
        self,
        school: str | None = None,
        category: str | None = None,
        source: str | None = None,
        implemented: bool | None = None,
        min_confidence: float = 0.0,
    ) -> list[RuleRecord]:
        """Return rules matching all specified criteria."""
        result = []
        for r in self._rules.values():
            if school is not None and r.school not in (school, "all"):
                continue
            if category is not None and r.category != category:
                continue
            if source is not None and r.source != source:
                continue
            if implemented is not None and r.implemented != implemented:
                continue
            if r.confidence < min_confidence:
                continue
            result.append(r)
        return result

    def count(self) -> int:
        return len(self._rules)

    def summary(self) -> str:
        """Short text summary for display and audit."""
        lines = [f"CorpusRegistry: {self.count()} rules"]
        by_school: dict[str, int] = {}
        by_src: dict[str, int] = {}
        for r in self._rules.values():
            by_school[r.school] = by_school.get(r.school, 0) + 1
            by_src[r.source] = by_src.get(r.source, 0) + 1
        for s, n in sorted(by_school.items()):
            lines.append(f"  school={s}: {n}")
        for s, n in sorted(by_src.items()):
            lines.append(f"  source={s}: {n}")
        return "\n".join(lines)
