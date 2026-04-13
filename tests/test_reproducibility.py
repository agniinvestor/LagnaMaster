"""tests/test_reproducibility.py — D22: Snapshot test for deterministic output.

Proves Q10: same inputs = identical output, no randomness.
Runs the full pipeline twice on the India 1947 chart and verifies
every output field is identical.
"""

from __future__ import annotations

from src.pipeline import run_pipeline

# India 1947 chart parameters
_PARAMS = dict(
    year=1947, month=8, day=15, hour=0.0,
    lat=28.6139, lon=77.2090, tz_offset=5.5,
)


def _run():
    """Run the full pipeline once."""
    return run_pipeline(**_PARAMS)


class TestReproducibility:
    """Two identical runs must produce identical results."""

    def setup_method(self):
        self.r1 = _run()
        self.r2 = _run()

    def test_same_prediction_count(self):
        """Same number of predictions."""
        assert len(self.r1.predictions) == len(self.r2.predictions), (
            f"Run 1: {len(self.r1.predictions)} predictions, "
            f"Run 2: {len(self.r2.predictions)} predictions"
        )

    def test_same_house_scores(self):
        """All 12 house scores are identical."""
        for h in range(1, 13):
            s1 = self.r1.scores.houses[h]
            s2 = self.r2.scores.houses[h]
            assert s1.final_score == s2.final_score, (
                f"H{h} score mismatch: {s1.final_score} vs {s2.final_score}"
            )
            assert s1.rating == s2.rating, (
                f"H{h} rating mismatch: {s1.rating} vs {s2.rating}"
            )

    def test_same_convergence_scores(self):
        """Convergence score and contra score identical per prediction."""
        for i, (p1, p2) in enumerate(
            zip(self.r1.predictions, self.r2.predictions)
        ):
            assert p1.house == p2.house, f"Prediction {i}: house mismatch"
            assert p1.direction == p2.direction, f"Prediction {i}: direction mismatch"
            assert p1.convergence_score == p2.convergence_score, (
                f"Prediction {i} (H{p1.house}): convergence "
                f"{p1.convergence_score} vs {p2.convergence_score}"
            )
            assert p1.contra_score == p2.contra_score, (
                f"Prediction {i} (H{p1.house}): contra "
                f"{p1.contra_score} vs {p2.contra_score}"
            )

    def test_same_timing_peak_windows(self):
        """Peak windows are identical per prediction."""
        for i, (p1, p2) in enumerate(
            zip(self.r1.predictions, self.r2.predictions)
        ):
            assert p1.peak_window == p2.peak_window, (
                f"Prediction {i} (H{p1.house}): peak_window "
                f"{p1.peak_window} vs {p2.peak_window}"
            )
            assert p1.timing_confidence == p2.timing_confidence, (
                f"Prediction {i} (H{p1.house}): timing_confidence "
                f"{p1.timing_confidence} vs {p2.timing_confidence}"
            )

    def test_same_version_info(self):
        """Version info is identical."""
        v1 = self.r1.version
        v2 = self.r2.version
        assert v1.corpus_version == v2.corpus_version, (
            f"corpus_version: {v1.corpus_version} vs {v2.corpus_version}"
        )
        assert v1.schema_version == v2.schema_version, (
            f"schema_version: {v1.schema_version} vs {v2.schema_version}"
        )
        assert v1.weight_version == v2.weight_version, (
            f"weight_version: {v1.weight_version} vs {v2.weight_version}"
        )

    def test_same_probability_by_year(self):
        """Year-level probability maps are identical."""
        for i, (p1, p2) in enumerate(
            zip(self.r1.predictions, self.r2.predictions)
        ):
            assert p1.probability_by_year == p2.probability_by_year, (
                f"Prediction {i} (H{p1.house}): probability_by_year differs"
            )

    def test_same_strength_labels(self):
        """Strength labels are identical."""
        for i, (p1, p2) in enumerate(
            zip(self.r1.predictions, self.r2.predictions)
        ):
            assert p1.strength_label == p2.strength_label, (
                f"Prediction {i} (H{p1.house}): strength_label "
                f"'{p1.strength_label}' vs '{p2.strength_label}'"
            )
