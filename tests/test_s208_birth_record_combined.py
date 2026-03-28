"""
tests/test_s208_birth_record_combined.py — S208: BirthRecord + CombinedCorpus

BirthRecord is the ML pipeline's birth data schema (ADB-compatible).
CombinedCorpus loads all six text registries into one searchable registry.
"""

from __future__ import annotations


# ── BirthRecord ───────────────────────────────────────────────────────────────

def test_birth_record_import():
    from src.corpus.birth_record import BirthRecord
    assert BirthRecord is not None


def test_birth_record_required_fields():
    import dataclasses
    from src.corpus.birth_record import BirthRecord
    fields = {f.name for f in dataclasses.fields(BirthRecord)}
    required = {"record_id", "birth_year", "birth_month", "birth_day",
                "birth_hour", "latitude", "longitude", "data_source"}
    assert required.issubset(fields), f"Missing: {required - fields}"


def test_birth_record_construction():
    from src.corpus.birth_record import BirthRecord
    r = BirthRecord(
        record_id="ADB-001",
        birth_year=1947,
        birth_month=8,
        birth_day=15,
        birth_hour=0.0,
        latitude=28.6139,
        longitude=77.2090,
        data_source="PUBLIC_DOMAIN",
    )
    assert r.record_id == "ADB-001"
    assert r.birth_year == 1947


def test_birth_record_is_train():
    from src.corpus.birth_record import BirthRecord
    from src.research.cv_splitter import TimeBasedSplit
    r = BirthRecord("T1", 1990, 1, 1, 0.0, 0.0, 0.0, "ADB")
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    assert s.is_train(r.birth_year)


def test_birth_record_is_test():
    from src.corpus.birth_record import BirthRecord
    from src.research.cv_splitter import TimeBasedSplit
    r = BirthRecord("T2", 2015, 1, 1, 0.0, 0.0, 0.0, "ADB")
    s = TimeBasedSplit(train_cutoff_year=2009, test_from_year=2010)
    assert s.is_test(r.birth_year)


# ── CombinedCorpus ────────────────────────────────────────────────────────────

def test_combined_corpus_import():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    assert COMBINED_CORPUS is not None


def test_combined_corpus_count_at_least_135():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    assert COMBINED_CORPUS.count() >= 135, (
        f"Expected ≥135 rules in combined corpus, got {COMBINED_CORPUS.count()}"
    )


def test_combined_corpus_filter_implemented():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    implemented = COMBINED_CORPUS.filter(implemented=True)
    assert len(implemented) == 23  # only R01-R23 are implemented


def test_combined_corpus_filter_unimplemented():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    unimplemented = COMBINED_CORPUS.filter(implemented=False)
    assert len(unimplemented) >= 112  # all extended rules


def test_combined_corpus_filter_parashari():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    parashari = COMBINED_CORPUS.filter(school="parashari")
    assert len(parashari) > 50


def test_combined_corpus_no_duplicate_ids():
    from src.corpus.combined_corpus import COMBINED_CORPUS
    ids = [r.rule_id for r in COMBINED_CORPUS.all()]
    assert len(ids) == len(set(ids))
