"""
tests/test_s202_corpus_infrastructure.py — S202: RuleRecord + CorpusRegistry

Core corpus infrastructure: machine-readable classical rules with
metadata, registry for lookup/filter, foundation for Phase 1 encoding.
"""

from __future__ import annotations


# ── RuleRecord ────────────────────────────────────────────────────────────────

def test_rule_record_import():
    from src.corpus.rule_record import RuleRecord
    assert RuleRecord is not None


def test_rule_record_required_fields():
    import dataclasses
    from src.corpus.rule_record import RuleRecord
    field_names = {f.name for f in dataclasses.fields(RuleRecord)}
    required = {"rule_id", "source", "chapter", "school", "category",
                "description", "confidence"}
    assert required.issubset(field_names), f"Missing: {required - field_names}"


def test_rule_record_construction():
    from src.corpus.rule_record import RuleRecord
    r = RuleRecord(
        rule_id="R01",
        source="BPHS",
        chapter="Ch.11",
        school="parashari",
        category="house_quality",
        description="Gentle/benefic signs give benefic house results",
        confidence=0.9,
    )
    assert r.rule_id == "R01"
    assert r.school == "parashari"


def test_rule_record_to_dict():
    from src.corpus.rule_record import RuleRecord
    r = RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality",
                   "Test rule", 0.9)
    d = r.to_dict()
    assert d["rule_id"] == "R01"
    assert isinstance(d["confidence"], float)


def test_rule_record_confidence_in_range():
    from src.corpus.rule_record import RuleRecord
    r = RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "test", 0.9)
    assert 0.0 <= r.confidence <= 1.0


# ── CorpusRegistry ────────────────────────────────────────────────────────────

def test_corpus_registry_import():
    from src.corpus.registry import CorpusRegistry
    assert CorpusRegistry is not None


def test_corpus_registry_add_and_get():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    r = RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "test", 0.9)
    reg.add(r)
    assert reg.get("R01") is r


def test_corpus_registry_filter_by_school():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    reg.add(RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "t1", 0.9))
    reg.add(RuleRecord("R02", "BPHS", "Ch.12", "kp", "house_quality", "t2", 0.8))
    parashari = reg.filter(school="parashari")
    assert all(r.school == "parashari" for r in parashari)
    assert len(parashari) == 1


def test_corpus_registry_filter_by_category():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    reg.add(RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "t1", 0.9))
    reg.add(RuleRecord("R02", "BPHS", "Ch.12", "parashari", "dignity", "t2", 0.8))
    hq = reg.filter(category="house_quality")
    assert len(hq) == 1


def test_corpus_registry_all_rules():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    for i in range(5):
        reg.add(RuleRecord(f"R{i:02d}", "BPHS", "Ch.11", "parashari",
                           "house_quality", f"rule {i}", 0.9))
    assert len(reg.all()) == 5


def test_corpus_registry_no_duplicate_ids():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    r = RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "test", 0.9)
    reg.add(r)
    try:
        reg.add(RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "dup", 0.8))
        assert False, "Should have raised for duplicate rule_id"
    except ValueError:
        pass


def test_corpus_registry_count():
    from src.corpus.rule_record import RuleRecord
    from src.corpus.registry import CorpusRegistry
    reg = CorpusRegistry()
    reg.add(RuleRecord("R01", "BPHS", "Ch.11", "parashari", "house_quality", "t", 0.9))
    reg.add(RuleRecord("R02", "BPHS", "Ch.12", "kp", "dignity", "t2", 0.8))
    assert reg.count() == 2
