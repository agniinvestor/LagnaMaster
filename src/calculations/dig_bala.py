"""
src/calculations/dig_bala.py — Session 52

Dig Bala (directional strength) continuous score 0.0–1.0.
BPHS Ch.27 + CALC_DigBala col G.

Formula: score = 1 − (min circular distance from peak house) / 6
At peak house (dist=0): score = 1.0
At opposite house (dist=6): score = 0.0

Peak houses (primary):
  Sun    → H10  Mercury → H1   Mars → H10
  Moon   → H4   Venus   → H4   Jupiter → H1
  Saturn → H7

Verified against CALC_DigBala:
  Sun H3 → dist 5 → 0.17 ✓   Moon H3 → dist 1 → 0.83 ✓
  Mars H2 → dist 4 → 0.33 ✓  Mercury H3 → dist 2 → 0.67 ✓
  Jupiter H6 → dist 5 → 0.17 ✓  Venus H3 → dist 1 → 0.83 ✓
  Saturn H3 → dist 4 → 0.33 ✓
"""
from __future__ import annotations
from dataclasses import dataclass

# Primary peak house for each planet (1-based)
_DIG_BALA_PEAK = {
    "Sun":     10,
    "Moon":    4,
    "Mars":    10,
    "Mercury": 1,
    "Jupiter": 1,
    "Venus":   4,
    "Saturn":  7,
}


@dataclass
class DigBalaResult:
    planet: str
    peak_house: int
    current_house: int
    distance: int
    score: float       # 0.0 – 1.0
    full_strength: bool  # score >= 0.75 (3 or closer)

    def label(self) -> str:
        if self.score >= 0.75:  return "Strong"
        if self.score >= 0.50:  return "Moderate"
        if self.score >= 0.25:  return "Weak"
        return "Absent"


def compute_dig_bala(chart) -> dict[str, DigBalaResult]:
    """Compute continuous Dig Bala score for all 7 planets."""
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    results = {}

    for planet, peak in _DIG_BALA_PEAK.items():
        current = hmap.planet_house.get(planet, 1)
        # Circular minimum distance (houses 1–12)
        diff = abs(peak - current)
        dist = min(diff, 12 - diff)
        score = round(1.0 - dist / 6.0, 4)
        results[planet] = DigBalaResult(
            planet=planet, peak_house=peak, current_house=current,
            distance=dist, score=score, full_strength=dist <= 2,
        )

    return results
