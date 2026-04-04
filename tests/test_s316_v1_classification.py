"""Test V1 derivation classification."""
from src.corpus.combined_corpus import _classify_v1_derivation


class _FakeRule:
    def __init__(self, verse_ref="", concordance_texts=None):
        self.verse_ref = verse_ref
        self.concordance_texts = concordance_texts or []


def test_verse_derived():
    assert _classify_v1_derivation(_FakeRule("Ch.12 v.1", ["PVRNR"])) == "verse_derived"


def test_commentary_derived():
    assert _classify_v1_derivation(_FakeRule("Ch.12 v.1")) == "commentary_derived"


def test_interpretive():
    assert _classify_v1_derivation(_FakeRule()) == "interpretive"
