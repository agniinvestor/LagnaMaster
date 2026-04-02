# Test Diversification: 360-Chart Verified Correctness System

**Date:** 2026-04-02
**Status:** Approved
**Approach:** B — Parallel Suite (no modification to existing tests)

---

## Problem

529 references to India 1947 across 51 test files. 44% of the test suite validates against a single Taurus-lagna, Cancer-stellium chart. Only 4% of tests use diverse fixtures. A module could break for 11 other Lagnas and pass all tests.

## Solution

Build a parallel `tests/test_diverse_correctness/` suite validated against 360 JHora-verified reference charts (30 per lagna), cross-validated automatically using PyJHora. Existing 1947 tests remain untouched as a legacy regression layer.

---

## Section 1: Chart Selection — PyJHora-First, Deterministic, Edge-Aware

### Step 1: Compute All Stubs with PyJHora

`tools/compute_pyjhora_all.py` — compute all 5,243 ADB stubs with PyJHora (Lahiri ayanamsha). Produces unbiased lagna distribution. Eliminates circular dependency (LagnaMaster selecting its own test data).

### Step 2: Deterministic Selection

`tools/select_360.py` — composite score:

```
score = data_quality + diversity + edge_case_density
```

**Data quality:** Rodden AA = 1.0, A = 0.8. All others excluded.

**Diversity** (formalized): decade bucket (one-hot), hemisphere (N/S), time-of-day quadrant (night 00-06 / morning 06-12 / afternoon 12-18 / evening 18-24). Diversity score = coverage balance bonus within each lagna group.

**Edge-case density:** 8 binary flags per chart:

| Flag | Condition |
|------|-----------|
| `lagna_boundary` | Lagna degree < 1° or > 29° in sign |
| `nakshatra_boundary` | Moon within 0.5° of nakshatra boundary |
| `retrograde_present` | ≥ 1 planet retrograde |
| `combustion_edge` | Any planet within ±1° of its combustion threshold (Mercury 14°, Venus 10°, Mars 17°, Jupiter 11°, Saturn 15°) |
| `exact_conjunction` | Any two of Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn < 1° longitude separation |
| `midnight_window` | Birth time within ±10 min of 00:00 |
| `high_latitude` | \|lat\| ≥ 50° |
| `dst_transition` | Birth date ∈ known DST transition dates for that timezone AND time within ±2 hours of transition boundary |

`edge_case_density = sum(flags)`

**Per-lagna minimums (of 30 charts):**
- ≥ 2 `lagna_boundary`
- ≥ 2 `nakshatra_boundary`
- ≥ 2 `retrograde_present`
- ≥ 1 `high_latitude`
- ≥ 1 `midnight_window`

**Global assertion:** Each edge flag appears ≥ 20 times across all 360 charts.

**Deterministic tie-break:** score desc → birth_year asc → chart_id asc.

**Post-selection validation:** exactly 30 per lagna, 360 total.

### Step 3: Golden 50

Top 50 charts by `edge_case_density` tagged `"golden_50": true` for fast CI.

### Output: `tests/fixtures/verified_360.json`

```json
{
  "schema_version": "1.0",
  "generated_date": "2026-04-02",
  "engine_versions": {
    "lagnamaster": "3.0.0",
    "pyjhora": "<version>"
  },
  "selection_hash": "<sha256 of selection inputs>",
  "pyjhora_compute_hash": "<sha256 of pyjhora outputs>",
  "diff_engine_version": "1.0",
  "Aries": [
    {
      "chart_id": "armstrong_neil",
      "rodden_rating": "AA",
      "score": 4.2,
      "edge_case_flags": {
        "lagna_boundary": false,
        "nakshatra_boundary": true,
        "retrograde_present": true,
        "combustion_edge": false,
        "exact_conjunction": false,
        "midnight_window": false,
        "high_latitude": false,
        "dst_transition": false
      },
      "edge_case_count": 2,
      "pyjhora_lagna_degree": 284.32,
      "selection_rank": 3,
      "golden_50": true
    }
  ]
}
```

**Immutability rule:** This file and all result files are immutable unless engine version changes or a bug fix requires update (with diff logged).

---

## Section 2: Cross-Validation Pipeline and Three-Category Diff Engine

### Normalization Layer

`tools/normalize_outputs.py` — applied to both engines before comparison:
- Longitudes wrapped to 0–360
- Signs mapped to standard enum
- Nakshatras mapped to canonical names
- Houses normalized to 1–12

### Properties Compared (Full Stack)

| Layer | Properties |
|-------|-----------|
| Positions | Lagna degree, planet longitudes (9 planets), sign placements |
| Nakshatra | Moon nakshatra, nakshatra pada, all planet nakshatras |
| Dignity | Dignity level per planet (own/exalt/debil/friend/enemy/neutral) |
| Houses | House lord per house, planets-in-house mapping |
| Panchangam | Tithi, Vara, Yoga, Karana |
| Ashtakavarga | Binna AV per planet (8×12 matrix), Sarva AV per sign |
| Yogas | Canonicalized: standardized name + condition_signature |
| Dashas | Vimsottari MD/AD sequence + period boundaries |
| Shadbala | 6 strength components per planet |
| Vargas | D9 lagna, D9 planet placements (extend to other vargas later) |

### Tolerances

| Property type | Core threshold | Edge-case chart threshold |
|--------------|---------------|--------------------------|
| Longitude | < 0.1° | < 0.2° |
| Degree-based (Shadbala, etc.) | < 0.5° | < 0.5° |
| Integer (AV bindus) | Exact match | Exact match |
| Categorical (sign, nakshatra, dignity) | Exact match | Exact match |
| Dasha periods | < 1 day boundary | < 1 day boundary |

### Three-Category Classification

1. **Agreement** — LM == PyJHora within tolerance → locked as ground truth
2. **Systematic disagreement** — LM ≠ PyJHora, consistent pattern: `frequency ≥ max(10, 0.25 × charts_in_segment)`, segmented by lagna and module → tagged with pattern_id, documented
3. **Random disagreement** — LM ≠ PyJHora, sporadic, no pattern → flagged as probable bugs

### Output Per Chart: `tests/fixtures/verified_360_results/{chart_id}.json`

```json
{
  "chart_id": "armstrong_neil",
  "birth_data": {
    "year": 1930, "month": 8, "day": 5,
    "hour": 0.5, "lat": 40.0339, "lon": -84.2108,
    "tz_offset": -5.0, "ayanamsha": "lahiri"
  },
  "lm_values": {},
  "pyjhora_values": {},
  "verdicts": {
    "lagna_degree": {
      "status": "agreement",
      "lm": 284.32, "pjh": 284.31, "diff": 0.01,
      "field_type": "longitude",
      "tolerance": 0.1,
      "normalized": true
    },
    "moon_nakshatra": {
      "status": "agreement",
      "lm": "Shravana", "pjh": "Shravana",
      "field_type": "categorical",
      "tolerance": null,
      "normalized": true
    },
    "yoga_gajakesari": {
      "status": "systematic_disagreement",
      "pattern_id": "SYS-003",
      "note": "Definition mismatch: PyJHora requires Moon in kendra from Jupiter; LM uses broader definition",
      "field_type": "categorical",
      "tolerance": null,
      "normalized": true
    }
  },
  "summary": {
    "total_fields": 312,
    "agreement": 298,
    "systematic": 8,
    "random": 6
  },
  "confidence_score": 0.955
}
```

### Field Ownership Map

Routes each field to the responsible LagnaMaster module:

```json
{
  "lagna_degree": "ephemeris",
  "planet_longitudes": "ephemeris",
  "nakshatra": "nakshatra",
  "dignity": "dignity",
  "house_lords": "house_analysis",
  "panchangam": "panchanga",
  "ashtakavarga": "ashtakavarga",
  "yogas": "yogas",
  "dashas": "vimshottari_dasha",
  "shadbala": "shadbala",
  "vargas": "varga"
}
```

### Systematic Pattern Registry: `tests/fixtures/systematic_patterns.json`

Each entry:

```json
{
  "pattern_id": "SYS-003",
  "field": "yoga_gajakesari",
  "error_signature": "definition_mismatch_kendra_rule",
  "frequency": 42,
  "affected_charts": ["..."],
  "status": "definitional",
  "justification": "BPHS Ch.36 v.3: 'If Jupiter is in a kendra from Moon' — LM includes trikona per Phaladeepika commentary",
  "source": "BPHS 36.3, Phaladeepika 6.1",
  "reviewed_by": "harsh",
  "review_date": "2026-04-15",
  "resolution": "LM uses broader definition; documented as intentional divergence"
}
```

**Statuses:** `unresolved` → `investigated` → one of: `lm_correct` | `pyjhora_correct` | `definitional` → `resolved`

### Aggregate Report: `tools/diff_report.py`

Outputs:
- Agreement rate per module (stability index)
- Ranked list of random disagreements by frequency (deduplicated by `(field_name, error_signature)`)
- Systematic pattern summary
- Weekly delta: new disagreements introduced since last run

### Module Agreement Scores (Stability Index)

```json
{
  "positions": 0.998,
  "nakshatra": 1.000,
  "panchangam": 0.972,
  "dignity": 0.991,
  "ashtakavarga": 0.985,
  "yogas": 0.821,
  "dashas": 0.963,
  "shadbala": 0.944,
  "vargas": 0.970
}
```

---

## Section 3: Test Suite Architecture

### Location and Structure

```
tests/test_diverse_correctness/
├── conftest.py                    # shared fixtures, chart loading, computed_chart
├── test_positions.py              # Phase 1
├── test_nakshatra.py              # Phase 1
├── test_panchangam.py             # Phase 1
├── test_dignity.py                # Phase 2
├── test_house_lords.py            # Phase 2
├── test_aspects.py                # Phase 2
├── test_ashtakavarga.py           # Phase 3
├── test_yogas.py                  # Phase 3
├── test_dashas.py                 # Phase 3
├── test_shadbala.py               # Phase 3
├── test_vargas.py                 # Phase 3
├── test_agreement_coverage.py     # Meta: coverage guard
├── test_disagreement_tracking.py  # Meta: xfail tracking
```

### Phased Rollout (Bottom-Up)

| Phase | Modules | Gate |
|-------|---------|------|
| 1 | Positions, Nakshatra, Panchangam | Must pass before Phase 2 begins |
| 2 | Dignity, House Lords, Aspects | Must pass before Phase 3 begins |
| 3 | AV, Yogas, Dashas, Shadbala, Vargas | Full stack |

Phase gates enforced in CI: `pytest -m phase1 && pytest -m phase2 && pytest -m phase3`

### conftest.py

```python
import pytest, json
from pathlib import Path

VERIFIED_DIR = Path("tests/fixtures/verified_360_results")
MANIFEST = json.loads(Path("tests/fixtures/verified_360.json").read_text())

def _load_charts(subset="all"):
    charts = []
    for lagna, entries in MANIFEST.items():
        if lagna.startswith("schema_") or lagna.endswith("_hash") or lagna.endswith("_version") or lagna == "generated_date":
            continue
        for entry in entries:
            if subset == "golden_50" and not entry.get("golden_50"):
                continue
            if subset not in ("all", "golden_50") and lagna != subset:
                continue
            result_path = VERIFIED_DIR / f"{entry['chart_id']}.json"
            data = json.loads(result_path.read_text())
            charts.append(data)
    return charts

ALL_CHARTS = _load_charts("all")
GOLDEN_50 = _load_charts("golden_50")

@pytest.fixture(params=ALL_CHARTS, ids=lambda c: c["chart_id"])
def verified_chart(request):
    return request.param

@pytest.fixture(params=GOLDEN_50, ids=lambda c: c["chart_id"])
def golden_chart(request):
    return request.param

@pytest.fixture
def computed_chart(verified_chart):
    from lagnamaster import compute_chart
    return compute_chart(**verified_chart["birth_data"])
```

### Test Pattern

**Agreement tests** — assert on agreed fields:

```python
def test_lagna_degree(verified_chart, computed_chart):
    verdict = verified_chart["verdicts"]["lagna_degree"]
    if verdict["status"] != "agreement":
        pytest.skip(f"disputed: {verdict['status']}")
    assert abs(computed_chart.lagna - verdict["pjh"]) < verdict["tolerance"]
```

**Disagreement tests** — track known bugs as xfail:

```python
@pytest.mark.xfail(strict=False, reason="unresolved engine disagreement")
def test_random_disagreements(verified_chart, computed_chart):
    for field, verdict in verified_chart["verdicts"].items():
        if verdict["status"] == "random_disagreement":
            pytest.fail(f"Unresolved: {field} LM={verdict.get('lm')} PJH={verdict.get('pjh')}")
```

**Agreement coverage guard:**

```python
def test_minimum_agreement_coverage():
    total_fields = 0
    agreement_fields = 0
    for chart_data in ALL_CHARTS:
        for field, verdict in chart_data["verdicts"].items():
            total_fields += 1
            if verdict["status"] == "agreement":
                agreement_fields += 1
    assert agreement_fields / total_fields > 0.90, (
        f"Agreement coverage {agreement_fields/total_fields:.1%} below 90% threshold"
    )
```

### CI Integration

| Trigger | Command | Charts |
|---------|---------|--------|
| Pre-commit (encoding sessions) | `pytest -m smoke --maxfail=1` | Golden 50 |
| Pre-push | `pytest tests/test_diverse_correctness/ -m smoke -q` | Golden 50 |
| Nightly / full validation | `pytest tests/test_diverse_correctness/ -q` | All 360 |

### xfail Discipline

- xfail count must monotonically decrease over time
- Any xfail older than 5 sessions → escalate to governance session
- Tracked in `tests/fixtures/verification_history.json`

---

## Section 4: Governance Loop

### 4a. Bug Triage from Random Disagreements

`tools/diff_report.py` outputs ranked random disagreements, deduplicated by `(field_name, error_signature)`. Each unique pattern → bug entry in `docs/BUGS.md`:
- Field(s) affected
- Number of charts impacted
- Example chart_id + LM vs PyJHora values
- Responsible module (from field ownership map)

Priority: ≥ 5 charts = HIGH, < 5 = LOW (unless Phase 1 field → always HIGH).

### 4a-bis. PyJHora Gravity Mitigation

PyJHora is the cross-validation reference, not ground truth. For any persistent random disagreement in **Phase 1 fields** (positions, nakshatras, panchangam):
- Require at least one external validation source before fixing LM (ephemeris reference table, published chart, independent calculation tool)
- Document the external source in the bug entry

This prevents systematic bias toward PyJHora when PyJHora itself may be wrong.

### 4b. Systematic Pattern Resolution

Severity tiers:
- **HIGH** (Phase 1 fields) → resolve within 1 encoding session
- **MEDIUM** (Phase 2 fields) → resolve within 2 sessions
- **LOW** (Phase 3 fields) → backlog allowed

Every resolution requires: justification, BPHS/source reference, reviewer, date.

Terminal state: `resolved` — either LM fixed, or accepted as definitional and encoded in tests.

No pattern stays `unresolved` beyond its SLA without escalation to a governance session.

### 4c. Re-verification After Engine Fixes

1. Re-run `tools/diff_engine.py` for affected charts (Phase 1 fix → full 360)
2. Confirm: random_disagreement → agreement
3. **Field-level non-regression check:** no previously-agreed field may become random_disagreement. Auto-blocks commit if violated.
4. **Abort condition:** if fix increases total random_disagreement_count → rollback or block merge
5. Update verdict files + append to `verification_history.json`
6. Commit

### 4d. Schema Evolution

Versioned manifest with `schema_version`, `generated_date`, `engine_versions`, `selection_hash`, `pyjhora_compute_hash`, `diff_engine_version`.

When either engine updates:
- Re-run full pipeline
- Diff against previous verification_history.json
- **Diff budget:** if new disagreements > 2% of total fields → block upgrade until investigated
- Update versions in manifest
- Commit

### 4e. Success Metrics

| Metric | Rule |
|--------|------|
| Random disagreement count | Must trend down |
| Systematic pattern count | Stable or resolved |
| Agreement rate | Contextual — decrease acceptable only with documented reason (e.g., tighter tolerances) |
| xfail count | Must monotonically decrease; >5 sessions old → escalate |

---

## Section 5: Operational Playbook

### 5a. Initial Pipeline Run (One-Time)

```
1. pip install PyJHora in .venv (tests/tools only — G17 enforced by ruff)
2. tools/compute_pyjhora_all.py → compute 5,243 ADB stubs with PyJHora
3. tools/select_360.py → deterministic selection → verified_360.json
4. tools/diff_engine.py → compute both engines, normalize, diff → 360 result files
5. tools/diff_report.py → aggregate report, stability index, initial bug triage
6. Commit fixtures + results + systematic_patterns.json
7. pytest tests/test_diverse_correctness/ -m phase1 → must pass
8. pytest tests/test_diverse_correctness/ -m phase2 → must pass
9. pytest tests/test_diverse_correctness/ -m phase3 → baseline established
10. Record reproducibility lock (selection_hash, compute_hash, engine versions)
```

### 5b. Bug Lifecycle

```
diff_report.py flags random disagreement
    → Deduplicate by (field_name, error_signature)
    → File in docs/BUGS.md with priority
    → Fix in LagnaMaster engine
    → Re-verify (Phase 1 fix → full 360; else affected charts)
    → Confirm: disagreement → agreement
    → Check: no previously-agreed fields regressed
    → Check: total random_disagreement_count did not increase (else rollback)
    → Update verdict files + verification_history.json
    → Commit
```

### 5c. Systematic Pattern Lifecycle

```
diff_engine classifies pattern (frequency ≥ max(10, 0.25 × segment))
    → Entry in systematic_patterns.json (status: unresolved)
    → Investigate within SLA (HIGH=1 session, MEDIUM=2, LOW=backlog)
    → Classify: lm_correct | pyjhora_correct | definitional
    → Document: justification + source + reviewer + date
    → Status → resolved
```

### 5d. Encoding Session Integration

**Before encoding:**
- Check `diff_report.py` — any open random disagreements in modules this chapter touches?
- If yes, fix first (controls before work)

**After encoding:**
- `pytest -m smoke --maxfail=1` (golden 50)
- If new failures, investigate before committing

### 5e. Engine/PyJHora Version Upgrade

```
Either engine updates version
    → Re-run full pipeline (steps 2-5 from 5a)
    → Diff against previous verification_history.json
    → If new disagreements > 2% → block upgrade
    → Update schema_version + engine_versions
    → Commit
```

### 5f. Health Dashboard (Weekly Check)

| Metric | Source | Alert if |
|--------|--------|----------|
| Agreement rate | verification_history.json | Drops below previous (without documented reason) |
| Random disagreement count | diff_report.py | Increases |
| New disagreements this week | diff_report.py delta | > 0 without corresponding fix |
| Unresolved systematic patterns | systematic_patterns.json | Any beyond SLA |
| Stability index per module | diff_report.py | Any module < 0.90 |
| xfail count | pytest output | Not trending toward zero |
| xfail age | verification_history.json | Any > 5 sessions old |

---

## Replay Mode

`tools/diff_engine.py --replay <date>` reproduces a historical pipeline run using:
- The selection manifest from that date (via `selection_hash`)
- The engine versions recorded at that date
- The normalization rules from that date

Enabled by the reproducibility lock (selection_hash, compute_hash, engine versions) already stored in the manifest. Useful for debugging regressions that surface months later.

---

## Tools Summary

| Tool | Purpose |
|------|---------|
| `tools/compute_pyjhora_all.py` | Compute all 5,243 ADB stubs with PyJHora |
| `tools/select_360.py` | Deterministic chart selection with edge-case awareness |
| `tools/normalize_outputs.py` | Normalize both engine outputs before comparison |
| `tools/diff_engine.py` | Three-category cross-validation engine |
| `tools/diff_report.py` | Aggregate reporting, stability index, bug triage |

## Files Summary

| File | Purpose |
|------|---------|
| `tests/fixtures/verified_360.json` | Selection manifest (immutable between versions) |
| `tests/fixtures/verified_360_results/{id}.json` | Per-chart verdicts |
| `tests/fixtures/systematic_patterns.json` | Known systematic difference registry |
| `tests/fixtures/verification_history.json` | Longitudinal tracking of agreement metrics |
