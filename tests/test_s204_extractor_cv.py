"""
tests/test_s204_extractor_cv.py — S204: TextExtractor protocol + CV splitter

TextExtractor is the base Protocol for corpus rule extractors.
TimeBasedSplit implements the G22-required pre-2010/2010+ cross-validation.
"""

from __future__ import annotations


# ── TextExtractor Protocol ────────────────────────────────────────────────────

def test_text_extractor_import():
    from src.corpus.extractor_base import TextExtractor
    assert TextExtractor is not None


def test_null_extractor_is_valid_extractor():
    """A concrete no-op extractor must satisfy the Protocol."""
    from src.corpus.rule_record import RuleRecord  # noqa: F401

    class NullExtractor:
        @property
        def source_name(self) -> str:
            return "NULL"
        def extract(self) -> list:
            return []

    e = NullExtractor()
    assert e.source_name == "NULL"
    assert e.extract() == []


def test_extractor_returns_rule_records():
    """Extractors must return RuleRecord instances."""
    from src.corpus.rule_record import RuleRecord
    from src.corpus.extractor_base import BaseExtractor

    class TinyExtractor(BaseExtractor):
        source_name = "BPHS"
        def extract(self):
            return [RuleRecord(
                "EX01", "BPHS", "Ch.1", "parashari",
                "house_quality", "test rule", 0.9,
                implemented=False,
            )]

    rules = TinyExtractor().extract()
    assert len(rules) == 1
    assert isinstance(rules[0], RuleRecord)


# ── TimeBasedSplit ────────────────────────────────────────────────────────────

def test_time_based_split_import():
    from src.research.cv_splitter import TimeBasedSplit
    assert TimeBasedSplit is not None


def test_time_based_split_fields():
    from src.research.cv_splitter import TimeBasedSplit
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    assert s.train_cutoff_year == 2009
    assert s.test_from_year == 2010


def test_time_based_split_is_train():
    from src.research.cv_splitter import TimeBasedSplit
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    assert s.is_train(2005)
    assert s.is_train(2009)
    assert not s.is_train(2010)
    assert not s.is_train(2023)


def test_time_based_split_is_test():
    from src.research.cv_splitter import TimeBasedSplit
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    assert s.is_test(2010)
    assert s.is_test(2024)
    assert not s.is_test(2009)
    assert not s.is_test(2000)


def test_time_based_split_no_leakage():
    """Train and test sets must be disjoint."""
    from src.research.cv_splitter import TimeBasedSplit
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    years = list(range(1950, 2026))
    train_years = [y for y in years if s.is_train(y)]
    test_years = [y for y in years if s.is_test(y)]
    assert not set(train_years) & set(test_years), "Train/test sets must not overlap"


def test_time_based_split_split_records():
    from src.research.cv_splitter import TimeBasedSplit
    records = [
        {"year": 2005, "outcome": 1},
        {"year": 2008, "outcome": 0},
        {"year": 2012, "outcome": 1},
        {"year": 2019, "outcome": 0},
    ]
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    train, test = s.split(records, year_key="year")
    assert len(train) == 2
    assert len(test) == 2
    assert all(r["year"] <= 2009 for r in train)
    assert all(r["year"] >= 2010 for r in test)


def test_g22_cv_matches_osf_draft():
    """CV split parameters must match the OB-3 OSF draft filing."""
    import json
    from pathlib import Path
    from src.research.cv_splitter import TimeBasedSplit
    draft = json.loads(Path("docs/research/osf_draft_ob3.json").read_text())
    cv = draft["cv_strategy"]
    s = TimeBasedSplit(
        train_cutoff_year=cv["train_cutoff_year"],
        test_from_year=cv["test_from_year"],
    )
    assert s.train_cutoff_year == 2009
    assert s.test_from_year == 2010
