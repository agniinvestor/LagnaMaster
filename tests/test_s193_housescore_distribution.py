"""
tests/test_s193_housescore_distribution.py — S193: HouseScore distribution dataclass

Verifies that:
  - HouseScore is a proper dataclass with required fields
  - HouseScore serialises to JSON
  - Distribution fields (mean, std, p10, p90) are present
  - p10 <= mean <= p90 (distribution ordering invariant)
  - compute_house_scores() returns dict[int, HouseScore] for all 12 houses
  - India 1947 chart: house 2 (wealth) score is negative

Source: LagnaMaster S193 deliverable specification
"""

from __future__ import annotations

import json


# ─────────────────────────────────────────────────────────────
# Fixture: India 1947 chart
# ─────────────────────────────────────────────────────────────

INDIA_BIRTH_LAT = 28.6139
INDIA_BIRTH_LON = 77.2090
INDIA_TZ_OFFSET = 5.5


def _india_chart():
    from src.ephemeris import compute_chart

    return compute_chart(
        year=1947,
        month=8,
        day=15,
        hour=0.0,
        lat=INDIA_BIRTH_LAT,
        lon=INDIA_BIRTH_LON,
        tz_offset=INDIA_TZ_OFFSET,
    )


# ─────────────────────────────────────────────────────────────
# 1. Dataclass fields
# ─────────────────────────────────────────────────────────────


def test_dataclass_fields():
    """HouseScore must expose house, score, mean, std, p10, p90 as attributes."""
    from src.calculations.house_score import HouseScore

    hs = HouseScore(house=1, score=1.5, mean=1.5, std=0.3, p10=1.1, p90=1.9)

    assert hs.house == 1
    assert hs.score == 1.5
    assert hs.mean == 1.5
    assert hs.std == 0.3
    assert hs.p10 == 1.1
    assert hs.p90 == 1.9


# ─────────────────────────────────────────────────────────────
# 2. JSON serialisation
# ─────────────────────────────────────────────────────────────


def test_dataclass_serializes_to_json():
    """HouseScore.to_dict() must produce a JSON-serialisable dict with all fields."""
    from src.calculations.house_score import HouseScore

    hs = HouseScore(house=4, score=-0.5, mean=-0.5, std=0.2, p10=-0.76, p90=-0.24)
    d = hs.to_dict()

    # Must be JSON serialisable without raising
    encoded = json.dumps(d)
    decoded = json.loads(encoded)

    assert decoded["house"] == 4
    assert decoded["score"] == -0.5
    assert decoded["mean"] == -0.5
    assert "std" in decoded
    assert "p10" in decoded
    assert "p90" in decoded


# ─────────────────────────────────────────────────────────────
# 3. Distribution fields present
# ─────────────────────────────────────────────────────────────


def test_distribution_has_mean_std_p10_p90():
    """HouseScore must carry mean, std, p10, p90 as numeric attributes."""
    from src.calculations.house_score import HouseScore

    hs = HouseScore(house=7, score=2.0, mean=2.0, std=0.5, p10=1.36, p90=2.64)

    assert isinstance(hs.mean, float)
    assert isinstance(hs.std, float)
    assert isinstance(hs.p10, float)
    assert isinstance(hs.p90, float)
    assert hs.std >= 0.0


# ─────────────────────────────────────────────────────────────
# 4. Distribution ordering invariant
# ─────────────────────────────────────────────────────────────


def test_distribution_range_valid():
    """p10 <= mean <= p90 must hold for any HouseScore."""
    from src.calculations.house_score import HouseScore

    for score in (-3.0, -1.0, 0.0, 1.5, 4.0):
        hs = HouseScore(
            house=1,
            score=score,
            mean=score,
            std=0.4,
            p10=score - 0.51,
            p90=score + 0.51,
        )
        assert hs.p10 <= hs.mean, f"p10 > mean for score={score}"
        assert hs.mean <= hs.p90, f"mean > p90 for score={score}"


# ─────────────────────────────────────────────────────────────
# 5. compute_house_scores returns dict[int, HouseScore]
# ─────────────────────────────────────────────────────────────


def test_score_returns_house_dict():
    """compute_house_scores() must return dict with int keys 1–12, HouseScore values."""
    from src.calculations.house_score import compute_house_scores

    chart = _india_chart()
    result = compute_house_scores(chart)

    assert isinstance(result, dict), "Expected dict"
    assert set(result.keys()) == set(range(1, 13)), "Must have keys 1–12"

    from src.calculations.house_score import HouseScore

    for house, hs in result.items():
        assert isinstance(hs, HouseScore), f"House {house} value is not HouseScore"
        assert hs.house == house, f"hs.house mismatch: {hs.house} != {house}"
        assert hs.p10 <= hs.mean, f"H{house}: p10 > mean"
        assert hs.mean <= hs.p90, f"H{house}: mean > p90"


# ─────────────────────────────────────────────────────────────
# 6. India 1947 — house 2 is negative
# ─────────────────────────────────────────────────────────────


def test_score_india_1947_h2_negative():
    """India 1947 chart: house 2 (wealth/accumulation) score must be negative."""
    from src.calculations.house_score import compute_house_scores

    chart = _india_chart()
    result = compute_house_scores(chart)

    h2 = result[2]
    assert h2.score < 0.0, (
        f"Expected H2 score < 0 for India 1947 (partition / economic distress), "
        f"got {h2.score}"
    )
