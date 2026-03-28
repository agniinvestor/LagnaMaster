"""
src/research/cv_splitter.py — Time-Based Cross-Validation Splitter (S204)

Implements the G22 / OSF-required cross-validation strategy:
  - Training set: events with confirmed year ≤ train_cutoff_year
  - Test set:     events with confirmed year ≥ test_from_year

This hard time split prevents look-ahead leakage and matches the
pre-registration in docs/research/osf_draft_ob3.json.

OB-3 values: train_cutoff_year=2009, test_from_year=2010.

Public API
----------
  TimeBasedSplit   — splitter with is_train/is_test/split methods
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class TimeBasedSplit:
    """
    Hard time-based split for cross-validation.

    G22 requirement: train_cutoff_year and test_from_year must match
    the pre-registered values in the OSF filing before any analysis runs.

    Attributes
    ----------
    train_cutoff_year  Last year (inclusive) allowed in the training set
    test_from_year     First year (inclusive) in the held-out test set
    """
    train_cutoff_year: int
    test_from_year: int

    def __post_init__(self) -> None:
        if self.test_from_year <= self.train_cutoff_year:
            raise ValueError(
                f"test_from_year ({self.test_from_year}) must be > "
                f"train_cutoff_year ({self.train_cutoff_year})"
            )

    def is_train(self, year: int) -> bool:
        """True if the year belongs in the training set."""
        return year <= self.train_cutoff_year

    def is_test(self, year: int) -> bool:
        """True if the year belongs in the held-out test set."""
        return year >= self.test_from_year

    def split(
        self,
        records: list[dict[str, Any]],
        year_key: str = "year",
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """
        Split a list of records into (train, test) by year.

        Records with years in the gap [train_cutoff+1, test_from-1] are
        excluded from both sets (no gap in the standard OB-3 split since
        train_cutoff=2009 and test_from=2010 are adjacent).

        Args:
            records:  List of dicts containing a year field
            year_key: Key to use for the year value

        Returns:
            (train_records, test_records)
        """
        train = [r for r in records if self.is_train(r[year_key])]
        test = [r for r in records if self.is_test(r[year_key])]
        return train, test

    def description(self) -> str:
        return (
            f"TimeBasedSplit(train≤{self.train_cutoff_year}, "
            f"test≥{self.test_from_year})"
        )
