"""Tests for three-category classification logic."""

from tools.classification import (
    classify_disagreements,
    deduplicate_patterns,
)
from tools.diff_engine_core import Verdict


def _make_verdict(field: str, status: str = "unclassified_disagreement",
                  diff: float = 5.0, lm=100.0, pjh=105.0) -> Verdict:
    return Verdict(field_name=field, status=status, lm=lm, pjh=pjh,
                   diff=diff, field_type="longitude", tolerance=0.1)


class TestClassifyDisagreements:
    def test_high_frequency_becomes_systematic(self):
        """20 identical disagreements in same field → systematic."""
        all_verdicts = {}
        for i in range(20):
            chart_id = f"chart_{i}"
            all_verdicts[chart_id] = {
                "lagna_degree": _make_verdict("lagna_degree", diff=5.0)
            }
        classified = classify_disagreements(all_verdicts, segment_size=20)
        for chart_id, verdicts in classified.items():
            assert verdicts["lagna_degree"].status == "systematic_disagreement"

    def test_low_frequency_stays_random(self):
        """2 disagreements out of 100 → random."""
        all_verdicts = {}
        for i in range(100):
            if i < 2:
                v = _make_verdict("lagna_degree", diff=5.0)
            else:
                v = _make_verdict("lagna_degree",
                                  status="agreement", diff=0.0)
            all_verdicts[f"chart_{i}"] = {"lagna_degree": v}
        classified = classify_disagreements(all_verdicts, segment_size=100)
        disagreeing = [
            cid for cid, vs in classified.items()
            if vs["lagna_degree"].status == "random_disagreement"
        ]
        assert len(disagreeing) == 2

    def test_threshold_formula(self):
        """Threshold is max(10, 0.25 * segment_size)."""
        all_verdicts = {}
        for i in range(20):
            if i < 10:
                v = _make_verdict("field_a", diff=5.0)
            else:
                v = _make_verdict("field_a", status="agreement", diff=0.0)
            all_verdicts[f"chart_{i}"] = {"field_a": v}
        classified = classify_disagreements(all_verdicts, segment_size=20)
        disagreeing = [
            cid for cid, vs in classified.items()
            if vs["field_a"].status == "systematic_disagreement"
        ]
        assert len(disagreeing) == 10

    def test_agreements_untouched(self):
        """Agreement verdicts are never reclassified."""
        all_verdicts = {
            "chart_0": {
                "lagna": _make_verdict("lagna", status="agreement", diff=0.01)
            }
        }
        classified = classify_disagreements(all_verdicts, segment_size=1)
        assert classified["chart_0"]["lagna"].status == "agreement"


class TestDeduplication:
    def test_same_field_same_signature_deduped(self):
        verdicts = [
            _make_verdict("lagna_degree", diff=5.0),
            _make_verdict("lagna_degree", diff=5.1),
            _make_verdict("lagna_degree", diff=4.9),
        ]
        patterns = deduplicate_patterns(verdicts)
        assert len(patterns) == 1
        assert patterns[0].count == 3

    def test_different_fields_separate(self):
        verdicts = [
            _make_verdict("lagna_degree", diff=5.0),
            _make_verdict("moon_longitude", diff=5.0),
        ]
        patterns = deduplicate_patterns(verdicts)
        assert len(patterns) == 2
