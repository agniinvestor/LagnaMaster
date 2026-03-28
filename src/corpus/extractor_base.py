"""
src/corpus/extractor_base.py — TextExtractor Protocol + BaseExtractor (S204)

Defines the interface that all corpus rule extractors must implement.

Public API
----------
  TextExtractor   — typing.Protocol for duck-typed extractors
  BaseExtractor   — abstract base class with shared utilities

Usage
-----
  class MyExtractor(BaseExtractor):
      source_name = "BPHS"
      def extract(self) -> list[RuleRecord]:
          ...
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable
from src.corpus.rule_record import RuleRecord


@runtime_checkable
class TextExtractor(Protocol):
    """
    Protocol for classical text rule extractors.
    Any class implementing source_name and extract() satisfies this Protocol.
    """

    @property
    def source_name(self) -> str:
        """Short name of the classical source, e.g. 'BPHS'."""
        ...

    def extract(self) -> list[RuleRecord]:
        """Extract and return all rules from this source."""
        ...


class BaseExtractor:
    """
    Convenience base class for extractors.
    Subclasses must set source_name and implement extract().
    """

    source_name: str = ""

    def extract(self) -> list[RuleRecord]:
        raise NotImplementedError(f"{type(self).__name__} must implement extract()")

    def load_into(self, registry) -> int:
        """
        Extract rules and add them to a CorpusRegistry.
        Returns the count of rules added.
        Skips rules already present (duplicate rule_id silently ignored).
        """
        count = 0
        for rule in self.extract():
            try:
                registry.add(rule)
                count += 1
            except ValueError:
                pass
        return count
