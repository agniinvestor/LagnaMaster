"""
update_docs_s193.py — S193 documentation sync

Patches docs/CHANGELOG.md and docs/MEMORY.md to reflect:
  - HouseScore distribution dataclass (house_score.py)
  - compute_house_scores() public API
  - ChartScoresV3.house_distributions field
  - Test count: 1490 passing

Run:  python update_docs_s193.py
"""

from pathlib import Path

ROOT = Path(__file__).parent
CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
MEMORY = ROOT / "docs" / "MEMORY.md"

# ─── CHANGELOG patch ─────────────────────────────────────────────────────────

S193_ENTRY = """
---

## S193 — 2026-03-28 — HouseScore Distribution Dataclass

**Commit:** (see git log)
**Tests:** 1490 passing, 3 skipped (require live PG_DSN), 0 lint errors, CI green

### What was built
- `src/calculations/house_score.py`: `HouseScore` dataclass with fields
  `house`, `score`, `mean`, `std`, `p10`, `p90` plus `to_dict()` for JSON
  serialisation.  `compute_house_scores(chart, school)` wraps D1 scoring and
  confidence-interval propagation to produce `dict[int, HouseScore]`.
- `tests/test_s193_housescore_distribution.py`: 6 tests covering dataclass
  fields, JSON serialisation, distribution ordering (p10 ≤ mean ≤ p90),
  full dict shape, and India 1947 H2-negative regression.

### What was wired
- `ChartScoresV3` gains a `house_distributions: dict` field (backward-compat)
  populated by `compute_house_scores()` inside `score_chart_v3()`.

### New invariants
- #37: `HouseScore.p10 <= HouseScore.mean <= HouseScore.p90` — always enforced
  by construction (normal-distribution percentile derivation from 95 % CI).

### Three-Lens Notes
- Tech: House scores are now typed objects — consumers can extract uncertainty
  bands without re-running the confidence model.
- Astrology: Distribution width reflects birth-time uncertainty (±5 min) and
  Lagna/Moon nakshatra boundary proximity.
- Research: p10/p90 bands enable ensemble-style prediction intervals.

### Next session
S194 — [TBD]
"""

changelog_text = CHANGELOG.read_text()
if "## S193" not in changelog_text:
    CHANGELOG.write_text(changelog_text.rstrip() + "\n" + S193_ENTRY)
    print("CHANGELOG.md — S193 entry appended.")
else:
    print("CHANGELOG.md — S193 entry already present, skipped.")

# ─── MEMORY.md patch ─────────────────────────────────────────────────────────

OLD_NEXT = "- **Next session:** S193"
NEW_NEXT = (
    "- **Session 193:** HouseScore distribution dataclass — `house_score.py`,"
    " `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests\n"
    "- **Next session:** S194"
)

OLD_STATE = "## Actual Current State (Sessions 1–188 complete"
NEW_STATE = "## Actual Current State (Sessions 1–193 complete"

OLD_COUNT = "- **1484 passing, 3 skipped, 0 lint errors, CI green**"
NEW_COUNT = "- **1490 passing, 3 skipped, 0 lint errors, CI green**"

OLD_S192_LINE = "- **Session 192:** Protocol adapters — ScoringEngineAdapter, VimshottariDasaAdapter, NullFeedbackService, NullMLService"
NEW_S192_LINE = (
    "- **Session 192:** Protocol adapters — ScoringEngineAdapter, VimshottariDasaAdapter,"
    " NullFeedbackService, NullMLService\n"
    "- **Session 193:** HouseScore distribution dataclass — `house_score.py`,"
    " `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests"
)

memory_text = MEMORY.read_text()
patched = memory_text

for old, new in [
    (OLD_NEXT, NEW_NEXT),
    (OLD_STATE, NEW_STATE),
    (OLD_COUNT, NEW_COUNT),
    (OLD_S192_LINE, NEW_S192_LINE),
]:
    if old in patched:
        patched = patched.replace(old, new, 1)

if patched != memory_text:
    MEMORY.write_text(patched)
    print("MEMORY.md — patched.")
else:
    print("MEMORY.md — no changes needed (already up to date).")

print("update_docs_s193.py — done.")
