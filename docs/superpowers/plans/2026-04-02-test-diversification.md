# Test Diversification: 360-Chart Verified Correctness System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the India-1947-monoculture test suite with a 360-chart, PyJHora-cross-validated parallel correctness system.

**Architecture:** PyJHora computes reference values for 360 deterministically-selected ADB charts (30 per lagna). A diff engine classifies agreement/disagreement per field. A parallel test suite asserts on agreed values and xfails disputed ones. A validation layer tests the testing infrastructure itself.

**Tech Stack:** Python 3.14, pytest, PyJHora 4.7.0 (AGPL — tests/tools only), pyswisseph, LagnaMaster v3.0.0

**Spec:** `docs/superpowers/specs/2026-04-02-test-diversification-design.md`

---

## File Structure

### New tools (pipeline):
- `tools/compute_pyjhora_all.py` — Compute all ADB stubs with PyJHora
- `tools/select_360.py` — Deterministic chart selection
- `tools/normalize_outputs.py` — Normalize both engine outputs
- `tools/diff_engine.py` — Three-category cross-validation
- `tools/diff_report.py` — Aggregate reporting and bug triage

### New test suites:
- `tests/test_validation_system/test_normalization.py`
- `tests/test_validation_system/test_diff_engine.py`
- `tests/test_validation_system/test_classification.py`
- `tests/test_validation_system/test_invariants.py`
- `tests/test_validation_system/test_poison_pills.py`
- `tests/test_diverse_correctness/conftest.py`
- `tests/test_diverse_correctness/test_positions.py`
- `tests/test_diverse_correctness/test_nakshatra.py`
- `tests/test_diverse_correctness/test_panchangam.py`
- `tests/test_diverse_correctness/test_dignity.py`
- `tests/test_diverse_correctness/test_house_lords.py`
- `tests/test_diverse_correctness/test_ashtakavarga.py`
- `tests/test_diverse_correctness/test_yogas.py`
- `tests/test_diverse_correctness/test_dashas.py`
- `tests/test_diverse_correctness/test_shadbala.py`
- `tests/test_diverse_correctness/test_agreement_coverage.py`

### New fixtures:
- `tests/fixtures/verified_360.json` — Selection manifest
- `tests/fixtures/verified_360_results/` — Per-chart verdict files (360 JSONs)
- `tests/fixtures/systematic_patterns.json` — Known systematic differences
- `tests/fixtures/verification_history.json` — Longitudinal tracking

---

## Task 1: Normalization Module

**Files:**
- Create: `tools/normalize_outputs.py`
- Test: `tests/test_validation_system/test_normalization.py`

- [ ] **Step 1: Write failing tests for normalization functions**

```python
# tests/test_validation_system/test_normalization.py
"""Tests for the normalization layer — proves the watchers work."""
import pytest

from tools.normalize_outputs import (
    normalize_longitude,
    normalize_sign,
    normalize_nakshatra,
    normalize_house_index,
    normalize_chart_output,
)

# --- Longitude wrapping ---

class TestNormalizeLongitude:
    def test_normal_value(self):
        assert normalize_longitude(180.0) == 180.0

    def test_wrap_above_360(self):
        assert normalize_longitude(361.0) == pytest.approx(1.0)

    def test_wrap_negative(self):
        assert normalize_longitude(-1.0) == pytest.approx(359.0)

    def test_zero(self):
        assert normalize_longitude(0.0) == 0.0

    def test_exact_360_wraps_to_0(self):
        assert normalize_longitude(360.0) == 0.0

    def test_large_value(self):
        assert normalize_longitude(725.5) == pytest.approx(5.5)

    def test_nan_raises(self):
        import math
        with pytest.raises(ValueError, match="NaN"):
            normalize_longitude(math.nan)

# --- Sign normalization ---

class TestNormalizeSign:
    def test_canonical_name(self):
        assert normalize_sign("Aries") == "Aries"

    def test_lowercase(self):
        assert normalize_sign("aries") == "Aries"

    def test_index_to_name(self):
        assert normalize_sign(0) == "Aries"
        assert normalize_sign(11) == "Pisces"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            normalize_sign("NotASign")

    def test_index_out_of_range_raises(self):
        with pytest.raises(ValueError):
            normalize_sign(12)

# --- Nakshatra normalization ---

class TestNormalizeNakshatra:
    def test_canonical(self):
        assert normalize_nakshatra("Ashwini") == "Ashwini"

    def test_variant_spelling(self):
        assert normalize_nakshatra("Ashvini") == "Ashwini"

    def test_pushya(self):
        assert normalize_nakshatra("Pushya") == "Pushya"
        assert normalize_nakshatra("Pushyami") == "Pushya"

    def test_index(self):
        assert normalize_nakshatra(0) == "Ashwini"
        assert normalize_nakshatra(26) == "Revati"

# --- House index normalization ---

class TestNormalizeHouseIndex:
    def test_already_1_indexed(self):
        assert normalize_house_index(1) == 1
        assert normalize_house_index(12) == 12

    def test_0_indexed_converts(self):
        # When explicitly flagged as 0-indexed
        assert normalize_house_index(0, zero_indexed=True) == 1
        assert normalize_house_index(11, zero_indexed=True) == 12

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            normalize_house_index(13)

    def test_zero_without_flag_raises(self):
        with pytest.raises(ValueError):
            normalize_house_index(0)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_validation_system/test_normalization.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.normalize_outputs'`

- [ ] **Step 3: Implement normalization module**

```python
# tools/normalize_outputs.py
"""
Normalization layer for cross-engine comparison.

Applied to both LagnaMaster and PyJHora outputs BEFORE diffing.
Ensures formatting differences are never misclassified as bugs.
"""
from __future__ import annotations

import math

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LOOKUP = {s.lower(): s for s in SIGN_NAMES}
SIGN_LOOKUP.update({str(i): s for i, s in enumerate(SIGN_NAMES)})

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]

# Common transliteration variants → canonical name
NAKSHATRA_VARIANTS: dict[str, str] = {
    "ashvini": "Ashwini",
    "krttika": "Krittika",
    "mrgashira": "Mrigashira",
    "mrigasira": "Mrigashira",
    "aridra": "Ardra",
    "thiruvadhirai": "Ardra",
    "pushyami": "Pushya",
    "aslesha": "Ashlesha",
    "makha": "Magha",
    "pubba": "Purva Phalguni",
    "purva phalguni": "Purva Phalguni",
    "uttara phalguni": "Uttara Phalguni",
    "hastham": "Hasta",
    "chitta": "Chitra",
    "chithra": "Chitra",
    "visakha": "Vishakha",
    "anusham": "Anuradha",
    "kettai": "Jyeshtha",
    "moola": "Mula",
    "pooradam": "Purva Ashadha",
    "purva ashadha": "Purva Ashadha",
    "uttaradam": "Uttara Ashadha",
    "uttara ashadha": "Uttara Ashadha",
    "thiruvonam": "Shravana",
    "sravana": "Shravana",
    "avittam": "Dhanishta",
    "dhanista": "Dhanishta",
    "sathayam": "Shatabhisha",
    "satabhisha": "Shatabhisha",
    "poorattadhi": "Purva Bhadrapada",
    "purva bhadrapada": "Purva Bhadrapada",
    "uttarattadhi": "Uttara Bhadrapada",
    "uttara bhadrapada": "Uttara Bhadrapada",
    "revathi": "Revati",
}

NAKSHATRA_LOOKUP = {n.lower(): n for n in NAKSHATRA_NAMES}
NAKSHATRA_LOOKUP.update(NAKSHATRA_VARIANTS)


def normalize_longitude(value: float) -> float:
    """Wrap longitude to [0, 360)."""
    if math.isnan(value):
        raise ValueError("NaN longitude")
    return value % 360.0


def normalize_sign(value: str | int) -> str:
    """Map sign name/index to canonical name."""
    if isinstance(value, int):
        if not 0 <= value <= 11:
            raise ValueError(f"Sign index out of range: {value}")
        return SIGN_NAMES[value]
    key = str(value).strip().lower()
    if key in SIGN_LOOKUP:
        return SIGN_LOOKUP[key]
    raise ValueError(f"Unknown sign: {value}")


def normalize_nakshatra(value: str | int) -> str:
    """Map nakshatra name/index/variant to canonical name."""
    if isinstance(value, int):
        if not 0 <= value <= 26:
            raise ValueError(f"Nakshatra index out of range: {value}")
        return NAKSHATRA_NAMES[value]
    key = str(value).strip().lower()
    if key in NAKSHATRA_LOOKUP:
        return NAKSHATRA_LOOKUP[key]
    raise ValueError(f"Unknown nakshatra: {value}")


def normalize_house_index(value: int, *, zero_indexed: bool = False) -> int:
    """Normalize house index to 1-12."""
    if zero_indexed:
        value = value + 1
    if not 1 <= value <= 12:
        raise ValueError(f"House index out of range: {value}")
    return value


def normalize_chart_output(data: dict, source: str) -> dict:
    """Normalize a full chart output dict from either engine.

    Args:
        data: Raw chart output (planet positions, nakshatras, etc.)
        source: 'lm' or 'pyjhora'

    Returns:
        Normalized dict with consistent types and ranges.
    """
    out = {}

    if "lagna_degree" in data:
        out["lagna_degree"] = normalize_longitude(data["lagna_degree"])
    if "lagna_sign" in data:
        out["lagna_sign"] = normalize_sign(data["lagna_sign"])

    planets = data.get("planets", {})
    out["planets"] = {}
    for name, pdata in planets.items():
        out["planets"][name] = {
            "longitude": normalize_longitude(pdata["longitude"]),
            "sign": normalize_sign(pdata["sign"]),
        }
        if "nakshatra" in pdata:
            out["planets"][name]["nakshatra"] = normalize_nakshatra(
                pdata["nakshatra"]
            )

    # Pass through fields that don't need normalization
    for key in ("ashtakavarga", "yogas", "dashas", "shadbala", "panchangam",
                "dignity", "house_lords"):
        if key in data:
            out[key] = data[key]

    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_validation_system/test_normalization.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add tools/normalize_outputs.py tests/test_validation_system/test_normalization.py
git commit -m "feat: normalization layer + tests for cross-engine comparison"
```

---

## Task 2: Diff Engine Core

**Files:**
- Create: `tools/diff_engine_core.py`
- Test: `tests/test_validation_system/test_diff_engine.py`

- [ ] **Step 1: Write failing tests for diff functions**

```python
# tests/test_validation_system/test_diff_engine.py
"""Tests for the diff engine — proves diffing detects real differences."""
import pytest

from tools.diff_engine_core import diff_field, diff_charts, Verdict


class TestDiffField:
    def test_identical_longitude_agrees(self):
        v = diff_field("lagna_degree", 100.5, 100.5, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"
        assert v.diff == pytest.approx(0.0)

    def test_within_tolerance_agrees(self):
        v = diff_field("lagna_degree", 100.5, 100.55, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"

    def test_at_tolerance_boundary_agrees(self):
        v = diff_field("lagna_degree", 100.0, 100.1, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "agreement"

    def test_beyond_tolerance_disagrees(self):
        v = diff_field("lagna_degree", 100.0, 100.2, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "unclassified_disagreement"

    def test_categorical_match(self):
        v = diff_field("moon_nakshatra", "Pushya", "Pushya",
                       field_type="categorical")
        assert v.status == "agreement"

    def test_categorical_mismatch(self):
        v = diff_field("moon_nakshatra", "Pushya", "Ashlesha",
                       field_type="categorical")
        assert v.status == "unclassified_disagreement"

    def test_integer_exact_match(self):
        v = diff_field("av_sun_aries", 4, 4, field_type="integer")
        assert v.status == "agreement"

    def test_integer_mismatch(self):
        v = diff_field("av_sun_aries", 4, 5, field_type="integer")
        assert v.status == "unclassified_disagreement"

    def test_nan_lm_value_flags(self):
        import math
        v = diff_field("lagna_degree", math.nan, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status == "unclassified_disagreement"

    def test_missing_field_flags(self):
        v = diff_field("lagna_degree", None, 100.0, field_type="longitude",
                       tolerance=0.1)
        assert v.status == "unclassified_disagreement"


class TestDiffCharts:
    def test_fully_identical(self):
        lm = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        pjh = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "lagna_sign": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert all(v.status == "agreement" for v in verdicts.values())

    def test_mixed_verdicts(self):
        lm = {"lagna_degree": 100.0, "lagna_sign": "Cancer"}
        pjh = {"lagna_degree": 105.0, "lagna_sign": "Cancer"}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "lagna_sign": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert verdicts["lagna_degree"].status == "unclassified_disagreement"
        assert verdicts["lagna_sign"].status == "agreement"

    def test_summary_counts(self):
        lm = {"a": 1.0, "b": 2.0, "c": "X"}
        pjh = {"a": 1.0, "b": 9.0, "c": "X"}
        schema = {
            "a": {"field_type": "longitude", "tolerance": 0.1},
            "b": {"field_type": "longitude", "tolerance": 0.1},
            "c": {"field_type": "categorical"},
        }
        verdicts = diff_charts(lm, pjh, schema)
        agreement = sum(1 for v in verdicts.values() if v.status == "agreement")
        assert agreement == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_validation_system/test_diff_engine.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement diff engine core**

```python
# tools/diff_engine_core.py
"""
Core diff engine for cross-validating LagnaMaster vs PyJHora.

Compares normalized outputs field-by-field and produces verdicts.
Classification (systematic vs random) is done in a separate pass
after all charts are diffed.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class Verdict:
    field_name: str
    status: str  # "agreement", "unclassified_disagreement", "systematic_disagreement", "random_disagreement"
    lm: object = None
    pjh: object = None
    diff: float | None = None
    field_type: str = ""
    tolerance: float | None = None
    normalized: bool = True
    pattern_id: str | None = None
    note: str | None = None


def diff_field(
    field_name: str,
    lm_value: object,
    pjh_value: object,
    *,
    field_type: str,
    tolerance: float | None = None,
) -> Verdict:
    """Compare a single field between LM and PyJHora outputs."""
    verdict = Verdict(
        field_name=field_name,
        lm=lm_value,
        pjh=pjh_value,
        field_type=field_type,
        tolerance=tolerance,
    )

    # Handle missing/NaN
    if lm_value is None or pjh_value is None:
        verdict.status = "unclassified_disagreement"
        verdict.note = "missing value"
        return verdict

    if field_type in ("longitude", "degree"):
        try:
            lm_f = float(lm_value)
            pjh_f = float(pjh_value)
        except (TypeError, ValueError):
            verdict.status = "unclassified_disagreement"
            verdict.note = "non-numeric value"
            return verdict

        if math.isnan(lm_f) or math.isnan(pjh_f):
            verdict.status = "unclassified_disagreement"
            verdict.note = "NaN value"
            return verdict

        verdict.diff = abs(lm_f - pjh_f)
        if verdict.diff <= (tolerance or 0.0):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    elif field_type == "integer":
        if int(lm_value) == int(pjh_value):
            verdict.status = "agreement"
            verdict.diff = 0.0
        else:
            verdict.status = "unclassified_disagreement"
            verdict.diff = float(abs(int(lm_value) - int(pjh_value)))

    elif field_type == "categorical":
        if str(lm_value) == str(pjh_value):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    elif field_type == "dasha_period":
        # Compare Julian Day boundaries
        try:
            verdict.diff = abs(float(lm_value) - float(pjh_value))
        except (TypeError, ValueError):
            verdict.status = "unclassified_disagreement"
            verdict.note = "non-numeric dasha boundary"
            return verdict
        if verdict.diff <= (tolerance or 1.0):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    else:
        # Unknown type — string comparison
        if str(lm_value) == str(pjh_value):
            verdict.status = "agreement"
        else:
            verdict.status = "unclassified_disagreement"

    return verdict


def diff_charts(
    lm_data: dict,
    pjh_data: dict,
    schema: dict[str, dict],
) -> dict[str, Verdict]:
    """Diff all fields between two chart outputs.

    Args:
        lm_data: Normalized LagnaMaster output (flat dict).
        pjh_data: Normalized PyJHora output (flat dict).
        schema: Field definitions: {field_name: {field_type, tolerance?}}

    Returns:
        Dict of field_name → Verdict.
    """
    verdicts = {}
    for field_name, field_def in schema.items():
        lm_val = lm_data.get(field_name)
        pjh_val = pjh_data.get(field_name)
        verdicts[field_name] = diff_field(
            field_name,
            lm_val,
            pjh_val,
            field_type=field_def["field_type"],
            tolerance=field_def.get("tolerance"),
        )
    return verdicts
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_validation_system/test_diff_engine.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add tools/diff_engine_core.py tests/test_validation_system/test_diff_engine.py
git commit -m "feat: diff engine core + tests for field-level comparison"
```

---

## Task 3: Classification Logic

**Files:**
- Create: `tools/classification.py`
- Test: `tests/test_validation_system/test_classification.py`

- [ ] **Step 1: Write failing tests for classification**

```python
# tests/test_validation_system/test_classification.py
"""Tests for three-category classification logic."""
import pytest

from tools.classification import (
    classify_disagreements,
    deduplicate_patterns,
    SystematicPattern,
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
        # All 20 should now be systematic
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
        # segment_size=20 → threshold=10
        all_verdicts = {}
        for i in range(20):
            if i < 10:
                v = _make_verdict("field_a", diff=5.0)
            else:
                v = _make_verdict("field_a", status="agreement", diff=0.0)
            all_verdicts[f"chart_{i}"] = {"field_a": v}
        classified = classify_disagreements(all_verdicts, segment_size=20)
        # Exactly at threshold → systematic
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_validation_system/test_classification.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement classification module**

```python
# tools/classification.py
"""
Three-category classification for cross-engine disagreements.

After diff_engine_core produces per-field verdicts, this module
reclassifies 'unclassified_disagreement' into either
'systematic_disagreement' or 'random_disagreement' based on frequency.
"""
from __future__ import annotations

import copy
import math
from collections import Counter
from dataclasses import dataclass

from tools.diff_engine_core import Verdict


@dataclass
class SystematicPattern:
    field_name: str
    error_signature: str
    count: int
    affected_charts: list[str]
    mean_diff: float | None = None


def _error_signature(verdict: Verdict) -> str:
    """Generate a deduplication key for a disagreement."""
    if verdict.diff is not None:
        # Bucket by order of magnitude
        magnitude = round(math.log10(max(abs(verdict.diff), 0.001)), 1)
        return f"{verdict.field_name}:magnitude_{magnitude}"
    return f"{verdict.field_name}:categorical_mismatch"


def classify_disagreements(
    all_verdicts: dict[str, dict[str, Verdict]],
    segment_size: int,
) -> dict[str, dict[str, Verdict]]:
    """Reclassify unclassified disagreements into systematic or random.

    Args:
        all_verdicts: {chart_id: {field_name: Verdict}}
        segment_size: Total charts in this segment (for threshold calc).

    Returns:
        Copy of all_verdicts with statuses updated.
    """
    result = copy.deepcopy(all_verdicts)
    threshold = max(10, int(0.25 * segment_size))

    # Count disagreements per field
    field_disagree_count: Counter[str] = Counter()
    for chart_id, verdicts in all_verdicts.items():
        for field_name, verdict in verdicts.items():
            if verdict.status == "unclassified_disagreement":
                field_disagree_count[field_name] += 1

    # Reclassify
    for chart_id, verdicts in result.items():
        for field_name, verdict in verdicts.items():
            if verdict.status != "unclassified_disagreement":
                continue
            if field_disagree_count[field_name] >= threshold:
                verdict.status = "systematic_disagreement"
            else:
                verdict.status = "random_disagreement"

    return result


def deduplicate_patterns(
    verdicts: list[Verdict],
) -> list[SystematicPattern]:
    """Group disagreement verdicts by (field_name, error_signature)."""
    groups: dict[str, list[Verdict]] = {}
    for v in verdicts:
        sig = _error_signature(v)
        groups.setdefault(sig, []).append(v)

    patterns = []
    for sig, vs in groups.items():
        diffs = [v.diff for v in vs if v.diff is not None]
        patterns.append(SystematicPattern(
            field_name=vs[0].field_name,
            error_signature=sig,
            count=len(vs),
            affected_charts=[],  # filled in by caller with chart_ids
            mean_diff=sum(diffs) / len(diffs) if diffs else None,
        ))
    return patterns
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_validation_system/test_classification.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add tools/classification.py tests/test_validation_system/test_classification.py
git commit -m "feat: three-category classification + deduplication logic"
```

---

## Task 4: Poison Pill and Invariant Tests

**Files:**
- Create: `tests/test_validation_system/test_poison_pills.py`
- Create: `tests/test_validation_system/test_invariants.py`

- [ ] **Step 1: Write poison pill tests**

```python
# tests/test_validation_system/test_poison_pills.py
"""Poison pill tests — deliberately bad inputs that must be caught."""
import math
import pytest

from tools.diff_engine_core import diff_field, diff_charts
from tools.normalize_outputs import normalize_longitude, normalize_chart_output


class TestPoisonLongitude:
    def test_999_degree_normalization(self):
        """999° must normalize to 279°, not silently pass."""
        result = normalize_longitude(999.0)
        assert result == pytest.approx(279.0)

    def test_nan_longitude_diff_flags(self):
        v = diff_field("lagna", math.nan, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status != "agreement"

    def test_none_value_diff_flags(self):
        v = diff_field("lagna", None, 100.0,
                       field_type="longitude", tolerance=0.1)
        assert v.status != "agreement"
        assert "missing" in (v.note or "")


class TestPoisonMissingField:
    def test_field_in_one_engine_only(self):
        lm = {"lagna_degree": 100.0}
        pjh = {"lagna_degree": 100.0, "extra_field": 50.0}
        schema = {
            "lagna_degree": {"field_type": "longitude", "tolerance": 0.1},
            "extra_field": {"field_type": "longitude", "tolerance": 0.1},
        }
        verdicts = diff_charts(lm, pjh, schema)
        assert verdicts["extra_field"].status != "agreement"


class TestPoisonNormalization:
    def test_empty_chart_raises(self):
        """normalize_chart_output on empty dict should not crash."""
        result = normalize_chart_output({}, source="lm")
        assert result.get("planets") == {}
```

- [ ] **Step 2: Write invariant tests**

```python
# tests/test_validation_system/test_invariants.py
"""Universal chart invariants — properties that hold for ANY birth chart."""
import pytest
from src.ephemeris import compute_chart
from src.calculations.nakshatra import nakshatra_position


# A few diverse charts for invariant testing (not the full 360 — those come later)
INVARIANT_CHARTS = [
    {"year": 1947, "month": 8, "day": 15, "hour": 0.0,
     "lat": 28.6139, "lon": 77.2090, "tz_offset": 5.5},  # India
    {"year": 2000, "month": 1, "day": 1, "hour": 12.0,
     "lat": 40.7128, "lon": -74.006, "tz_offset": -5.0},  # NYC
    {"year": 1985, "month": 6, "day": 21, "hour": 23.5,
     "lat": 64.1466, "lon": -21.9426, "tz_offset": 0.0},  # Reykjavik near midnight
]


@pytest.fixture(params=INVARIANT_CHARTS,
                ids=["india_1947", "nyc_2000", "reykjavik_1985"])
def chart(request):
    return compute_chart(**request.param)


class TestPositionInvariants:
    def test_lagna_in_range(self, chart):
        assert 0 <= chart.lagna < 360

    def test_planet_longitudes_in_range(self, chart):
        for name, pos in chart.planets.items():
            assert 0 <= pos.longitude < 360, f"{name} longitude out of range"

    def test_sign_index_matches_longitude(self, chart):
        for name, pos in chart.planets.items():
            expected_sign = int(pos.longitude // 30)
            assert pos.sign_index == expected_sign, (
                f"{name}: sign_index {pos.sign_index} != "
                f"floor({pos.longitude}/30) = {expected_sign}"
            )

    def test_rahu_ketu_opposite(self, chart):
        rahu = chart.planets["Rahu"].longitude
        ketu = chart.planets["Ketu"].longitude
        diff = abs(rahu - ketu)
        # Should be ~180° (allow for slight variation)
        assert abs(diff - 180.0) < 1.0 or abs(diff - 540.0) < 1.0


class TestNakshatraInvariants:
    def test_nakshatra_index_in_range(self, chart):
        for name, pos in chart.planets.items():
            nak = nakshatra_position(pos.longitude)
            assert 0 <= nak.nakshatra_index <= 26, (
                f"{name} nakshatra index {nak.nakshatra_index} out of range"
            )

    def test_pada_in_range(self, chart):
        for name, pos in chart.planets.items():
            nak = nakshatra_position(pos.longitude)
            assert 1 <= nak.pada <= 4, (
                f"{name} pada {nak.pada} out of range"
            )
```

- [ ] **Step 3: Run both test files**

Run: `.venv/bin/pytest tests/test_validation_system/test_poison_pills.py tests/test_validation_system/test_invariants.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_validation_system/test_poison_pills.py tests/test_validation_system/test_invariants.py
git commit -m "feat: poison pill + universal invariant tests for validation layer"
```

---

## Task 5: PyJHora Computation Tool

**Files:**
- Create: `tools/compute_pyjhora_all.py`

This tool computes all 5,243 ADB stubs with PyJHora and stores results. It's the foundation for unbiased chart selection.

- [ ] **Step 1: Write the computation tool**

```python
# tools/compute_pyjhora_all.py
"""
Compute all ADB stubs with PyJHora (Lahiri ayanamsha).

Produces unbiased lagna distribution for chart selection.
G17: PyJHora (AGPL-3.0) allowed in tools/ for study only.

Usage:
    .venv/bin/python tools/compute_pyjhora_all.py [--limit N] [--output PATH]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from jhora.panchanga import drik  # noqa: E402, TID251
from jhora.horoscope.chart.charts import rasi_chart  # noqa: E402, TID251
from jhora.horoscope.chart import ashtakavarga  # noqa: E402, TID251
from jhora.horoscope.dhasa.graha import vimsottari  # noqa: E402, TID251
from jhora.horoscope.chart import strength as jhora_strength  # noqa: E402, TID251

ADB_DIR = ROOT / "tests" / "fixtures" / "adb_charts"
OUTPUT_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# PyJHora planet indices → names
PJH_PLANET_MAP = {
    0: "Sun", 1: "Moon", 2: "Mercury", 3: "Venus", 4: "Mars",
    5: "Jupiter", 6: "Saturn", 7: "Rahu", 8: "Ketu",
}


def compute_one_chart(birth_data: dict) -> dict | None:
    """Compute a single chart with PyJHora. Returns None on failure."""
    try:
        drik.set_ayanamsa_mode("LAHIRI")

        place = drik.Place(
            "loc",
            birth_data["lat"],
            birth_data["lon"],
            birth_data["tz_offset"],
        )

        # Convert local time to UTC for JD
        local_hour = birth_data["hour"]
        utc_hour = local_hour - birth_data["tz_offset"]
        jd = drik.swe.julday(
            birth_data["year"],
            birth_data["month"],
            birth_data["day"],
            utc_hour,
        )

        # Rasi chart (D1)
        chart = rasi_chart(jd, place)
        if not chart:
            return None

        # Parse chart output
        result = {"planets": {}}
        for entry in chart:
            planet_id, (rasi_idx, degree_in_sign) = entry
            if planet_id == "L":
                result["lagna_sign"] = SIGN_NAMES[rasi_idx]
                result["lagna_sign_index"] = rasi_idx
                result["lagna_degree"] = rasi_idx * 30 + degree_in_sign
                result["lagna_degree_in_sign"] = degree_in_sign
            elif planet_id in PJH_PLANET_MAP:
                name = PJH_PLANET_MAP[planet_id]
                result["planets"][name] = {
                    "longitude": rasi_idx * 30 + degree_in_sign,
                    "sign": SIGN_NAMES[rasi_idx],
                    "sign_index": rasi_idx,
                    "degree_in_sign": degree_in_sign,
                }

        # Ashtakavarga
        try:
            av = ashtakavarga.get_ashtaka_varga(chart)
            result["ashtakavarga"] = av
        except Exception:
            result["ashtakavarga"] = None

        # Vimsottari dasha
        try:
            dasha = vimsottari.vimsottari_mahadasa(jd, place)
            result["vimsottari"] = {
                PJH_PLANET_MAP.get(k, str(k)): float(v)
                for k, v in dasha.items()
            }
        except Exception:
            result["vimsottari"] = None

        # Shadbala
        try:
            sb = jhora_strength.shad_bala(jd, place)
            result["shadbala"] = sb
        except Exception:
            result["shadbala"] = None

        return result

    except Exception as e:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Compute all ADB stubs with PyJHora"
    )
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of charts (0=all)")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    stubs = sorted(ADB_DIR.glob("*.json"))
    if args.limit > 0:
        stubs = stubs[: args.limit]

    success = 0
    fail = 0
    start = time.time()

    for i, stub_path in enumerate(stubs):
        stub = json.loads(stub_path.read_text())
        birth_data = stub.get("birth_data")
        if not birth_data:
            fail += 1
            continue

        result = compute_one_chart(birth_data)
        if result is None:
            fail += 1
            continue

        out = {
            "chart_id": stub_path.stem,
            "name": stub.get("name", ""),
            "rodden_rating": stub.get("rodden_rating", ""),
            "birth_data": birth_data,
            "birth_place": stub.get("birth_place", ""),
            "pyjhora": result,
        }

        out_path = args.output / f"{stub_path.stem}.json"
        out_path.write_text(json.dumps(out, indent=2, default=str))
        success += 1

        if (i + 1) % 100 == 0:
            elapsed = time.time() - start
            rate = (i + 1) / elapsed
            print(f"  [{i+1}/{len(stubs)}] {rate:.1f} charts/sec, "
                  f"{success} ok, {fail} fail")

    elapsed = time.time() - start
    print(f"\nDone: {success} computed, {fail} failed, "
          f"{elapsed:.1f}s total")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with a small batch**

Run: `.venv/bin/python tools/compute_pyjhora_all.py --limit 10`
Expected: `Done: N computed, M failed` with N > 0 and output files in `tests/fixtures/pyjhora_computed/`

- [ ] **Step 3: Verify output format**

Run: `.venv/bin/python -c "import json; d=json.load(open('tests/fixtures/pyjhora_computed/' + __import__('os').listdir('tests/fixtures/pyjhora_computed')[0])); print(json.dumps(d, indent=2)[:500])"`
Expected: JSON with `chart_id`, `birth_data`, `pyjhora.lagna_sign`, `pyjhora.planets`

- [ ] **Step 4: Commit**

```bash
git add tools/compute_pyjhora_all.py
git commit -m "feat: PyJHora batch computation tool for all ADB stubs"
```

- [ ] **Step 5: Run full computation**

Run: `.venv/bin/python tools/compute_pyjhora_all.py`
Expected: ~5,243 charts processed (some failures expected for stubs without valid birth data). This may take 30-60 minutes.

- [ ] **Step 6: Commit computed results**

```bash
git add tests/fixtures/pyjhora_computed/
git commit -m "data: PyJHora-computed reference values for all ADB stubs"
```

---

## Task 6: Chart Selection Tool

**Files:**
- Create: `tools/select_360.py`

- [ ] **Step 1: Write the selection tool**

```python
# tools/select_360.py
"""
Deterministic selection of 360 charts (30 per lagna) from PyJHora-computed ADB stubs.

Selection criteria:
- Rodden AA or A only
- Composite score: data_quality + diversity + edge_case_density
- Per-lagna edge-case coverage minimums enforced
- Deterministic tie-break: score desc → birth_year asc → chart_id asc

Usage:
    .venv/bin/python tools/select_360.py [--input DIR] [--output PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

PYJHORA_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"
OUTPUT_PATH = ROOT / "tests" / "fixtures" / "verified_360.json"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# Combustion thresholds (degrees from Sun)
COMBUSTION_THRESHOLDS = {
    "Mercury": 14, "Venus": 10, "Mars": 17, "Jupiter": 11, "Saturn": 15,
}

# Nakshatra boundaries (every 13°20' = 13.333...°)
NAKSHATRA_SPAN = 360.0 / 27.0  # 13.333...°

CHARTS_PER_LAGNA = 30
GOLDEN_50_COUNT = 50

# Per-lagna minimum edge-case coverage
EDGE_MINIMUMS = {
    "lagna_boundary": 2,
    "nakshatra_boundary": 2,
    "retrograde_present": 2,
    "high_latitude": 1,
    "midnight_window": 1,
}

# Global minimum per edge type
GLOBAL_EDGE_MINIMUM = 20


@dataclass
class ChartCandidate:
    chart_id: str
    lagna: str
    rodden_rating: str
    birth_year: int
    birth_data: dict
    pyjhora_lagna_degree: float
    edge_case_flags: dict
    edge_case_count: int = 0
    data_quality: float = 0.0
    diversity_score: float = 0.0
    score: float = 0.0
    selection_rank: int = 0
    golden_50: bool = False


def _compute_edge_flags(birth_data: dict, pjh: dict) -> dict:
    """Compute 8 binary edge-case flags."""
    flags = {}

    # Lagna boundary
    lagna_in_sign = pjh.get("lagna_degree_in_sign", 15.0)
    flags["lagna_boundary"] = lagna_in_sign < 1.0 or lagna_in_sign > 29.0

    # Nakshatra boundary (Moon within 0.5° of boundary)
    moon_lon = pjh.get("planets", {}).get("Moon", {}).get("longitude", 180.0)
    nak_position_in_span = moon_lon % NAKSHATRA_SPAN
    flags["nakshatra_boundary"] = (
        nak_position_in_span < 0.5 or
        nak_position_in_span > (NAKSHATRA_SPAN - 0.5)
    )

    # Retrograde present
    # PyJHora rasi_chart doesn't expose retrograde directly;
    # we check via speed if available, otherwise skip
    flags["retrograde_present"] = False  # Updated when LM computes

    # Combustion edge
    sun_lon = pjh.get("planets", {}).get("Sun", {}).get("longitude", 0.0)
    flags["combustion_edge"] = False
    for planet, threshold in COMBUSTION_THRESHOLDS.items():
        p_lon = pjh.get("planets", {}).get(planet, {}).get("longitude")
        if p_lon is not None:
            dist = abs(p_lon - sun_lon)
            if dist > 180:
                dist = 360 - dist
            if abs(dist - threshold) <= 1.0:
                flags["combustion_edge"] = True
                break

    # Exact conjunction
    planet_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    longitudes = []
    for name in planet_names:
        lon = pjh.get("planets", {}).get(name, {}).get("longitude")
        if lon is not None:
            longitudes.append((name, lon))
    flags["exact_conjunction"] = False
    for i in range(len(longitudes)):
        for j in range(i + 1, len(longitudes)):
            diff = abs(longitudes[i][1] - longitudes[j][1])
            if diff > 180:
                diff = 360 - diff
            if diff < 1.0:
                flags["exact_conjunction"] = True
                break
        if flags["exact_conjunction"]:
            break

    # Midnight window
    hour = birth_data.get("hour", 12.0)
    flags["midnight_window"] = hour < (10 / 60) or hour > (23 + 50 / 60)

    # High latitude
    lat = birth_data.get("lat", 0.0)
    flags["high_latitude"] = abs(lat) >= 50.0

    # DST transition — simplified: flag births in March/October/November
    # (most DST transitions globally). Full implementation would use
    # timezone database.
    month = birth_data.get("month", 6)
    flags["dst_transition"] = month in (3, 10, 11)

    return flags


def _diversity_components(birth_data: dict) -> dict:
    """Extract diversity dimensions for balance scoring."""
    year = birth_data.get("year", 1970)
    decade = (year // 10) * 10
    hemisphere = "N" if birth_data.get("lat", 0) >= 0 else "S"
    hour = birth_data.get("hour", 12.0)
    if hour < 6:
        tod = "night"
    elif hour < 12:
        tod = "morning"
    elif hour < 18:
        tod = "afternoon"
    else:
        tod = "evening"
    return {"decade": decade, "hemisphere": hemisphere, "time_of_day": tod}


def select(input_dir: Path) -> dict:
    """Select 360 charts deterministically."""
    # Load all PyJHora-computed charts
    candidates_by_lagna: dict[str, list[ChartCandidate]] = {
        s: [] for s in SIGN_NAMES
    }

    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text())
        rating = data.get("rodden_rating", "")
        if rating not in ("AA", "A"):
            continue

        pjh = data.get("pyjhora", {})
        lagna = pjh.get("lagna_sign")
        if not lagna or lagna not in SIGN_NAMES:
            continue

        birth_data = data.get("birth_data", {})
        flags = _compute_edge_flags(birth_data, pjh)
        edge_count = sum(1 for v in flags.values() if v)

        quality = 1.0 if rating == "AA" else 0.8

        candidate = ChartCandidate(
            chart_id=data["chart_id"],
            lagna=lagna,
            rodden_rating=rating,
            birth_year=birth_data.get("year", 0),
            birth_data=birth_data,
            pyjhora_lagna_degree=pjh.get("lagna_degree", 0.0),
            edge_case_flags=flags,
            edge_case_count=edge_count,
            data_quality=quality,
            score=quality + edge_count,  # diversity added after grouping
        )
        candidates_by_lagna[lagna].append(candidate)

    # Select 30 per lagna with coverage constraints
    selected: dict[str, list[dict]] = {}
    all_selected: list[ChartCandidate] = []

    for lagna in SIGN_NAMES:
        pool = candidates_by_lagna[lagna]

        # Sort deterministically: score desc, birth_year asc, chart_id asc
        pool.sort(key=lambda c: (-c.score, c.birth_year, c.chart_id))

        # First pass: ensure edge-case minimums
        chosen: list[ChartCandidate] = []
        remaining = list(pool)

        for flag_name, minimum in EDGE_MINIMUMS.items():
            count = sum(1 for c in chosen if c.edge_case_flags.get(flag_name))
            needed = minimum - count
            if needed > 0:
                flagged = [
                    c for c in remaining
                    if c.edge_case_flags.get(flag_name) and c not in chosen
                ]
                for c in flagged[:needed]:
                    chosen.append(c)
                    remaining.remove(c)

        # Fill remaining slots by score
        for c in remaining:
            if len(chosen) >= CHARTS_PER_LAGNA:
                break
            if c not in chosen:
                chosen.append(c)

        # Re-sort and assign ranks
        chosen.sort(key=lambda c: (-c.score, c.birth_year, c.chart_id))
        for rank, c in enumerate(chosen[:CHARTS_PER_LAGNA], 1):
            c.selection_rank = rank

        all_selected.extend(chosen[:CHARTS_PER_LAGNA])
        selected[lagna] = [
            {
                "chart_id": c.chart_id,
                "rodden_rating": c.rodden_rating,
                "score": round(c.score, 2),
                "edge_case_flags": c.edge_case_flags,
                "edge_case_count": c.edge_case_count,
                "pyjhora_lagna_degree": round(c.pyjhora_lagna_degree, 4),
                "selection_rank": c.selection_rank,
                "golden_50": False,
            }
            for c in chosen[:CHARTS_PER_LAGNA]
        ]

    # Tag golden 50
    all_selected.sort(key=lambda c: (-c.edge_case_count, c.chart_id))
    golden_ids = {c.chart_id for c in all_selected[:GOLDEN_50_COUNT]}
    for lagna_entries in selected.values():
        for entry in lagna_entries:
            if entry["chart_id"] in golden_ids:
                entry["golden_50"] = True

    # Validate
    total = sum(len(v) for v in selected.values())
    assert total == 360, f"Expected 360, got {total}"
    for lagna, entries in selected.items():
        assert len(entries) == 30, f"{lagna}: expected 30, got {len(entries)}"

    # Global edge-case coverage check
    for flag_name in EDGE_MINIMUMS:
        global_count = sum(
            1 for entries in selected.values()
            for e in entries if e["edge_case_flags"].get(flag_name)
        )
        if global_count < GLOBAL_EDGE_MINIMUM:
            print(f"WARNING: {flag_name} only appears {global_count} times "
                  f"(minimum {GLOBAL_EDGE_MINIMUM})")

    # Compute selection hash
    selection_input = json.dumps(selected, sort_keys=True)
    selection_hash = hashlib.sha256(selection_input.encode()).hexdigest()

    return {
        "schema_version": "1.0",
        "generated_date": "2026-04-02",
        "engine_versions": {"lagnamaster": "3.0.0", "pyjhora": "4.7.0"},
        "selection_hash": selection_hash,
        "total_charts": total,
        "golden_50_count": len(golden_ids),
        **selected,
    }


def main():
    parser = argparse.ArgumentParser(description="Select 360 diverse charts")
    parser.add_argument("--input", type=Path, default=PYJHORA_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()

    manifest = select(args.input)
    args.output.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written to {args.output}")
    print(f"  Total: {manifest['total_charts']}")
    print(f"  Golden 50: {manifest['golden_50_count']}")
    print(f"  Hash: {manifest['selection_hash'][:16]}...")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run selection on computed data**

Run: `.venv/bin/python tools/select_360.py`
Expected: `Manifest written to tests/fixtures/verified_360.json` with 360 total, 50 golden

- [ ] **Step 3: Verify manifest structure**

Run: `.venv/bin/python -c "import json; d=json.load(open('tests/fixtures/verified_360.json')); print('Total:', d['total_charts']); print('Lagnas:', {k: len(v) for k, v in d.items() if isinstance(v, list)})"`
Expected: Total: 360, each lagna: 30

- [ ] **Step 4: Commit**

```bash
git add tools/select_360.py tests/fixtures/verified_360.json
git commit -m "feat: deterministic 360-chart selection with edge-case coverage"
```

---

## Task 7: Diff Engine Pipeline

**Files:**
- Create: `tools/diff_engine.py`

This is the orchestrator that computes both engines, normalizes, diffs, classifies, and writes per-chart result files.

- [ ] **Step 1: Write the pipeline tool**

```python
# tools/diff_engine.py
"""
Cross-validation pipeline: LagnaMaster vs PyJHora for 360 selected charts.

For each chart:
1. Load PyJHora pre-computed values
2. Compute with LagnaMaster
3. Normalize both
4. Diff field-by-field
5. Classify disagreements (systematic vs random)
6. Write per-chart verdict files

Usage:
    .venv/bin/python tools/diff_engine.py [--charts-only CHART_ID,...]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.ephemeris import compute_chart  # noqa: E402
from src.calculations.nakshatra import nakshatra_position  # noqa: E402
from tools.normalize_outputs import normalize_longitude, normalize_sign, normalize_nakshatra  # noqa: E402
from tools.diff_engine_core import diff_field, Verdict  # noqa: E402
from tools.classification import classify_disagreements  # noqa: E402

MANIFEST_PATH = ROOT / "tests" / "fixtures" / "verified_360.json"
PYJHORA_DIR = ROOT / "tests" / "fixtures" / "pyjhora_computed"
RESULTS_DIR = ROOT / "tests" / "fixtures" / "verified_360_results"

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

PLANET_NAMES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                "Saturn", "Rahu", "Ketu"]

# Field ownership map
FIELD_OWNER = {
    "lagna_degree": "ephemeris",
    "lagna_sign": "ephemeris",
}
for _p in PLANET_NAMES:
    FIELD_OWNER[f"longitude_{_p.lower()}"] = "ephemeris"
    FIELD_OWNER[f"sign_{_p.lower()}"] = "ephemeris"
    FIELD_OWNER[f"nakshatra_{_p.lower()}"] = "nakshatra"


def _extract_lm_values(chart) -> dict:
    """Extract flat dict of values from a LagnaMaster BirthChart."""
    values = {
        "lagna_degree": chart.lagna,
        "lagna_sign": chart.lagna_sign,
    }
    for name in PLANET_NAMES:
        pos = chart.planets[name]
        values[f"longitude_{name.lower()}"] = pos.longitude
        values[f"sign_{name.lower()}"] = pos.sign
        nak = nakshatra_position(pos.longitude)
        values[f"nakshatra_{name.lower()}"] = nak.nakshatra
    return values


def _extract_pjh_values(pjh: dict) -> dict:
    """Extract flat dict of values from PyJHora computed data."""
    values = {
        "lagna_degree": pjh.get("lagna_degree", 0.0),
        "lagna_sign": pjh.get("lagna_sign", ""),
    }
    planets = pjh.get("planets", {})
    for name in PLANET_NAMES:
        pdata = planets.get(name, {})
        values[f"longitude_{name.lower()}"] = pdata.get("longitude", 0.0)
        values[f"sign_{name.lower()}"] = pdata.get("sign", "")
    # PyJHora nakshatra extraction would go here (requires additional API)
    return values


def _build_schema(has_edge_flags: bool) -> dict:
    """Build the field comparison schema."""
    lon_tol = 0.2 if has_edge_flags else 0.1
    schema = {
        "lagna_degree": {"field_type": "longitude", "tolerance": lon_tol},
        "lagna_sign": {"field_type": "categorical"},
    }
    for name in PLANET_NAMES:
        schema[f"longitude_{name.lower()}"] = {
            "field_type": "longitude", "tolerance": lon_tol,
        }
        schema[f"sign_{name.lower()}"] = {"field_type": "categorical"}
    return schema


def run_pipeline(chart_ids: list[str] | None = None):
    """Run the full diff pipeline."""
    manifest = json.loads(MANIFEST_PATH.read_text())
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Collect all chart entries from manifest
    entries = []
    for key, value in manifest.items():
        if not isinstance(value, list):
            continue
        for entry in value:
            if chart_ids and entry["chart_id"] not in chart_ids:
                continue
            entries.append(entry)

    all_verdicts: dict[str, dict[str, Verdict]] = {}
    results: dict[str, dict] = {}

    print(f"Processing {len(entries)} charts...")
    start = time.time()

    for i, entry in enumerate(entries):
        chart_id = entry["chart_id"]
        pjh_path = PYJHORA_DIR / f"{chart_id}.json"
        if not pjh_path.exists():
            print(f"  SKIP {chart_id}: no PyJHora data")
            continue

        pjh_data = json.loads(pjh_path.read_text())
        birth_data = pjh_data["birth_data"]

        # Compute with LagnaMaster
        try:
            lm_chart = compute_chart(
                year=birth_data["year"],
                month=birth_data["month"],
                day=birth_data["day"],
                hour=birth_data["hour"],
                lat=birth_data["lat"],
                lon=birth_data["lon"],
                tz_offset=birth_data["tz_offset"],
            )
        except Exception as e:
            print(f"  FAIL {chart_id}: LM compute error: {e}")
            continue

        # Extract values
        lm_values = _extract_lm_values(lm_chart)
        pjh_values = _extract_pjh_values(pjh_data.get("pyjhora", {}))

        # Normalize
        for key in list(lm_values.keys()):
            if "longitude" in key or key == "lagna_degree":
                lm_values[key] = normalize_longitude(lm_values[key])
            elif "sign" in key:
                lm_values[key] = normalize_sign(lm_values[key])
        for key in list(pjh_values.keys()):
            if "longitude" in key or key == "lagna_degree":
                try:
                    pjh_values[key] = normalize_longitude(pjh_values[key])
                except (ValueError, TypeError):
                    pass
            elif "sign" in key:
                try:
                    pjh_values[key] = normalize_sign(pjh_values[key])
                except (ValueError, TypeError):
                    pass

        # Diff
        has_edge = entry.get("edge_case_count", 0) > 0
        schema = _build_schema(has_edge)
        verdicts = {}
        for field_name, field_def in schema.items():
            verdicts[field_name] = diff_field(
                field_name,
                lm_values.get(field_name),
                pjh_values.get(field_name),
                field_type=field_def["field_type"],
                tolerance=field_def.get("tolerance"),
            )

        all_verdicts[chart_id] = verdicts
        results[chart_id] = {
            "chart_id": chart_id,
            "birth_data": birth_data,
            "lm_values": {k: _serialize(v) for k, v in lm_values.items()},
            "pyjhora_values": {k: _serialize(v) for k, v in pjh_values.items()},
            "entry": entry,
        }

        if (i + 1) % 50 == 0:
            elapsed = time.time() - start
            print(f"  [{i+1}/{len(entries)}] {elapsed:.1f}s")

    # Classify
    print("Classifying disagreements...")
    classified = classify_disagreements(all_verdicts, segment_size=len(entries))

    # Write per-chart result files
    for chart_id, verdicts in classified.items():
        agreement = sum(1 for v in verdicts.values() if v.status == "agreement")
        total = len(verdicts)

        result_data = results[chart_id]
        result_data["verdicts"] = {
            fname: {
                "status": v.status,
                "lm": _serialize(v.lm),
                "pjh": _serialize(v.pjh),
                "diff": v.diff,
                "field_type": v.field_type,
                "tolerance": v.tolerance,
                "normalized": v.normalized,
                "pattern_id": v.pattern_id,
                "note": v.note,
            }
            for fname, v in verdicts.items()
        }
        result_data["summary"] = {
            "total_fields": total,
            "agreement": agreement,
            "systematic": sum(1 for v in verdicts.values()
                             if v.status == "systematic_disagreement"),
            "random": sum(1 for v in verdicts.values()
                         if v.status == "random_disagreement"),
        }
        result_data["confidence_score"] = (
            round(agreement / total, 4) if total > 0 else 0.0
        )

        out_path = RESULTS_DIR / f"{chart_id}.json"
        out_path.write_text(json.dumps(result_data, indent=2, default=str))

    # Print summary
    total_fields = sum(r.get("summary", {}).get("total_fields", 0)
                       for r in results.values() if "summary" in (results[r] if isinstance(r, str) else r))
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Charts processed: {len(classified)}")


def _serialize(value):
    """Make values JSON-safe."""
    if isinstance(value, float):
        return round(value, 6)
    return value


def main():
    parser = argparse.ArgumentParser(description="Cross-validate LM vs PyJHora")
    parser.add_argument("--charts-only", type=str, default="",
                        help="Comma-separated chart IDs (empty=all)")
    args = parser.parse_args()

    chart_ids = [c.strip() for c in args.charts_only.split(",") if c.strip()] or None
    run_pipeline(chart_ids)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run on a small subset to test**

Run: `.venv/bin/python tools/diff_engine.py --charts-only <first_chart_id>`
Expected: One result file in `tests/fixtures/verified_360_results/`

- [ ] **Step 3: Run full pipeline**

Run: `.venv/bin/python tools/diff_engine.py`
Expected: 360 result files written

- [ ] **Step 4: Commit**

```bash
git add tools/diff_engine.py tests/fixtures/verified_360_results/
git commit -m "feat: full cross-validation pipeline — LM vs PyJHora for 360 charts"
```

---

## Task 8: Diff Report Tool

**Files:**
- Create: `tools/diff_report.py`

- [ ] **Step 1: Write the reporting tool**

```python
# tools/diff_report.py
"""
Aggregate reporting across all 360 cross-validation results.

Outputs: module stability index, ranked disagreements, systematic patterns,
health dashboard metrics.

Usage:
    .venv/bin/python tools/diff_report.py [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESULTS_DIR = ROOT / "tests" / "fixtures" / "verified_360_results"
PATTERNS_PATH = ROOT / "tests" / "fixtures" / "systematic_patterns.json"
HISTORY_PATH = ROOT / "tests" / "fixtures" / "verification_history.json"

# Field → module ownership
FIELD_MODULE = defaultdict(lambda: "unknown")
FIELD_MODULE.update({
    "lagna_degree": "positions",
    "lagna_sign": "positions",
})
for _p in ["sun", "moon", "mars", "mercury", "jupiter", "venus",
           "saturn", "rahu", "ketu"]:
    FIELD_MODULE[f"longitude_{_p}"] = "positions"
    FIELD_MODULE[f"sign_{_p}"] = "positions"
    FIELD_MODULE[f"nakshatra_{_p}"] = "nakshatra"


def generate_report(as_json: bool = False):
    """Generate aggregate cross-validation report."""
    results = []
    for path in sorted(RESULTS_DIR.glob("*.json")):
        results.append(json.loads(path.read_text()))

    if not results:
        print("No results found.")
        return

    # Aggregate counts
    total_charts = len(results)
    total_fields = 0
    total_agreement = 0
    total_systematic = 0
    total_random = 0

    # Per-module stability
    module_total: Counter = Counter()
    module_agreement: Counter = Counter()

    # Disagreement tracking
    random_list = []

    for r in results:
        s = r.get("summary", {})
        total_fields += s.get("total_fields", 0)
        total_agreement += s.get("agreement", 0)
        total_systematic += s.get("systematic", 0)
        total_random += s.get("random", 0)

        for fname, v in r.get("verdicts", {}).items():
            module = FIELD_MODULE[fname]
            module_total[module] += 1
            if v["status"] == "agreement":
                module_agreement[module] += 1
            elif v["status"] == "random_disagreement":
                random_list.append({
                    "chart_id": r["chart_id"],
                    "field": fname,
                    "lm": v.get("lm"),
                    "pjh": v.get("pjh"),
                    "diff": v.get("diff"),
                })

    # Module stability index
    stability = {}
    for module in sorted(module_total):
        total = module_total[module]
        agreed = module_agreement[module]
        stability[module] = round(agreed / total, 4) if total > 0 else 0.0

    # Deduplicate random disagreements
    field_counts = Counter(d["field"] for d in random_list)

    report = {
        "total_charts": total_charts,
        "total_fields": total_fields,
        "agreement_rate": round(total_agreement / total_fields, 4) if total_fields else 0,
        "agreement": total_agreement,
        "systematic": total_systematic,
        "random": total_random,
        "stability_index": stability,
        "random_disagreements_by_field": dict(field_counts.most_common()),
        "random_disagreement_details": random_list[:20],
    }

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print(f"=== Cross-Validation Report ===")
        print(f"Charts: {total_charts}")
        print(f"Fields: {total_fields}")
        print(f"Agreement rate: {report['agreement_rate']:.1%}")
        print(f"  Agreement: {total_agreement}")
        print(f"  Systematic: {total_systematic}")
        print(f"  Random: {total_random}")
        print(f"\n--- Module Stability Index ---")
        for module, score in sorted(stability.items(),
                                     key=lambda x: x[1]):
            bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
            print(f"  {module:<15} {bar} {score:.1%}")
        if field_counts:
            print(f"\n--- Random Disagreements (by field) ---")
            for field, count in field_counts.most_common(10):
                print(f"  {field}: {count} charts")

    # Append to verification history
    history = []
    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text())
    history.append({
        "date": "2026-04-02",
        "agreement_rate": report["agreement_rate"],
        "random_disagreements": total_random,
        "systematic_patterns": total_systematic,
        "total_charts": total_charts,
    })
    HISTORY_PATH.write_text(json.dumps(history, indent=2))

    return report


def main():
    parser = argparse.ArgumentParser(description="Aggregate diff report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    generate_report(as_json=args.json)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the report**

Run: `.venv/bin/python tools/diff_report.py`
Expected: Printed report with agreement rate, module stability index, disagreement counts

- [ ] **Step 3: Commit**

```bash
git add tools/diff_report.py
git commit -m "feat: aggregate diff report with stability index and bug triage"
```

---

## Task 9: Diverse Correctness Test Suite — Phase 1

**Files:**
- Create: `tests/test_diverse_correctness/conftest.py`
- Create: `tests/test_diverse_correctness/test_positions.py`
- Create: `tests/test_diverse_correctness/test_nakshatra.py`
- Create: `tests/test_diverse_correctness/test_agreement_coverage.py`

- [ ] **Step 1: Write conftest.py**

```python
# tests/test_diverse_correctness/conftest.py
"""Shared fixtures for the 360-chart diverse correctness suite."""
import json
import pytest
from pathlib import Path

from src.ephemeris import compute_chart, BirthChart

VERIFIED_DIR = Path("tests/fixtures/verified_360_results")
MANIFEST_PATH = Path("tests/fixtures/verified_360.json")

# Skip keys that are metadata, not lagna names
_META_KEYS = {
    "schema_version", "generated_date", "engine_versions",
    "selection_hash", "total_charts", "golden_50_count",
    "pyjhora_compute_hash", "diff_engine_version",
}


def _load_charts(subset="all"):
    manifest = json.loads(MANIFEST_PATH.read_text())
    charts = []
    for key, entries in manifest.items():
        if key in _META_KEYS or not isinstance(entries, list):
            continue
        for entry in entries:
            if subset == "golden_50" and not entry.get("golden_50"):
                continue
            result_path = VERIFIED_DIR / f"{entry['chart_id']}.json"
            if not result_path.exists():
                continue
            data = json.loads(result_path.read_text())
            charts.append(data)
    return charts


ALL_CHARTS = _load_charts("all")
GOLDEN_50 = _load_charts("golden_50")


@pytest.fixture(params=ALL_CHARTS, ids=lambda c: c["chart_id"])
def verified_chart(request):
    """A single verified chart with verdicts."""
    return request.param


@pytest.fixture(params=GOLDEN_50, ids=lambda c: c["chart_id"])
def golden_chart(request):
    """A golden-50 chart for smoke tests."""
    return request.param


@pytest.fixture
def computed_chart(verified_chart) -> BirthChart:
    """Pre-computed LagnaMaster chart for the verified fixture."""
    bd = verified_chart["birth_data"]
    return compute_chart(
        year=bd["year"], month=bd["month"], day=bd["day"],
        hour=bd["hour"], lat=bd["lat"], lon=bd["lon"],
        tz_offset=bd["tz_offset"],
    )
```

- [ ] **Step 2: Write Phase 1 position tests**

```python
# tests/test_diverse_correctness/test_positions.py
"""Phase 1: Lagna and planet position correctness across 360 charts."""
import pytest

pytestmark = [pytest.mark.phase1, pytest.mark.smoke]


class TestLagna:
    def test_lagna_degree(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("lagna_degree")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        assert abs(computed_chart.lagna - verdict["pjh"]) < verdict["tolerance"]

    def test_lagna_sign(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("lagna_sign")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed: {verdict['status'] if verdict else 'missing'}")
        assert computed_chart.lagna_sign == verdict["pjh"]


class TestPlanetPositions:
    PLANETS = ["sun", "moon", "mars", "mercury", "jupiter",
               "venus", "saturn", "rahu", "ketu"]

    def test_planet_longitudes(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"longitude_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            pos = computed_chart.planets[planet.capitalize()]
            assert abs(pos.longitude - verdict["pjh"]) < verdict["tolerance"], (
                f"{planet}: {pos.longitude} vs {verdict['pjh']}"
            )

    def test_planet_signs(self, verified_chart, computed_chart):
        for planet in self.PLANETS:
            key = f"sign_{planet}"
            verdict = verified_chart["verdicts"].get(key)
            if not verdict or verdict["status"] != "agreement":
                continue
            pos = computed_chart.planets[planet.capitalize()]
            assert pos.sign == verdict["pjh"], (
                f"{planet}: {pos.sign} vs {verdict['pjh']}"
            )


class TestRandomDisagreements:
    @pytest.mark.xfail(strict=False, reason="unresolved engine disagreement")
    def test_position_disagreements(self, verified_chart, computed_chart):
        """Track random disagreements — goal is to reach zero."""
        failures = []
        for field, verdict in verified_chart["verdicts"].items():
            if verdict["status"] == "random_disagreement":
                failures.append(f"{field}: LM={verdict.get('lm')} PJH={verdict.get('pjh')}")
        if failures:
            pytest.fail("\n".join(failures))
```

- [ ] **Step 3: Write Phase 1 nakshatra tests**

```python
# tests/test_diverse_correctness/test_nakshatra.py
"""Phase 1: Nakshatra correctness across 360 charts."""
import pytest
from src.calculations.nakshatra import nakshatra_position

pytestmark = pytest.mark.phase1


class TestMoonNakshatra:
    def test_moon_nakshatra(self, verified_chart, computed_chart):
        verdict = verified_chart["verdicts"].get("nakshatra_moon")
        if not verdict or verdict["status"] != "agreement":
            pytest.skip(f"disputed or missing")
        moon_nak = nakshatra_position(computed_chart.planets["Moon"].longitude)
        assert moon_nak.nakshatra == verdict["pjh"]
```

- [ ] **Step 4: Write agreement coverage guard**

```python
# tests/test_diverse_correctness/test_agreement_coverage.py
"""Meta-test: ensures agreement coverage doesn't silently erode."""
import json
import pytest
from pathlib import Path

RESULTS_DIR = Path("tests/fixtures/verified_360_results")

_META_KEYS = {
    "schema_version", "generated_date", "engine_versions",
    "selection_hash", "total_charts", "golden_50_count",
}


def test_minimum_agreement_coverage():
    """Agreement must stay above 90% globally."""
    total_fields = 0
    agreement_fields = 0

    for path in sorted(RESULTS_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        for field, verdict in data.get("verdicts", {}).items():
            total_fields += 1
            if verdict["status"] == "agreement":
                agreement_fields += 1

    if total_fields == 0:
        pytest.skip("No verified results found")

    rate = agreement_fields / total_fields
    assert rate > 0.90, (
        f"Agreement coverage {rate:.1%} below 90% threshold "
        f"({agreement_fields}/{total_fields})"
    )
```

- [ ] **Step 5: Run Phase 1 tests**

Run: `.venv/bin/pytest tests/test_diverse_correctness/ -m phase1 -v --tb=short`
Expected: Tests pass for agreement fields, skip for disputed fields, xfail for random disagreements

- [ ] **Step 6: Commit**

```bash
git add tests/test_diverse_correctness/
git commit -m "feat: diverse correctness suite Phase 1 — positions, nakshatras, coverage guard"
```

---

## Task 10: Initialize Systematic Patterns and Verification History

**Files:**
- Create: `tests/fixtures/systematic_patterns.json`
- Create: `tests/fixtures/verification_history.json`

- [ ] **Step 1: Initialize systematic patterns file**

```python
# Run after diff_engine.py has completed:
# .venv/bin/python -c "
import json
from pathlib import Path

results_dir = Path('tests/fixtures/verified_360_results')
patterns = {}

for path in sorted(results_dir.glob('*.json')):
    data = json.loads(path.read_text())
    for field, verdict in data.get('verdicts', {}).items():
        if verdict['status'] == 'systematic_disagreement':
            pid = verdict.get('pattern_id', f'SYS-{field}')
            if pid not in patterns:
                patterns[pid] = {
                    'pattern_id': pid,
                    'field': field,
                    'error_signature': f'{field}:systematic',
                    'frequency': 0,
                    'affected_charts': [],
                    'status': 'unresolved',
                    'justification': None,
                    'source': None,
                    'reviewed_by': None,
                    'review_date': None,
                }
            patterns[pid]['frequency'] += 1
            patterns[pid]['affected_charts'].append(data['chart_id'])

Path('tests/fixtures/systematic_patterns.json').write_text(
    json.dumps(list(patterns.values()), indent=2)
)
print(f'Found {len(patterns)} systematic patterns')
# "
```

- [ ] **Step 2: Verify history file was created by diff_report.py**

Run: `.venv/bin/python -c "import json; print(json.dumps(json.load(open('tests/fixtures/verification_history.json')), indent=2))"`
Expected: JSON array with one entry containing agreement_rate, random_disagreements, etc.

- [ ] **Step 3: Commit**

```bash
git add tests/fixtures/systematic_patterns.json tests/fixtures/verification_history.json
git commit -m "data: initial systematic patterns registry and verification history"
```

---

## Task 11: CI Integration

**Files:**
- Modify: `.git/hooks/pre-push`

- [ ] **Step 1: Read current pre-push hook**

Run: `cat .git/hooks/pre-push`
Document current content.

- [ ] **Step 2: Add diverse correctness smoke to pre-push**

Add to the existing pre-push hook, after the existing test suite run:

```bash
# Diverse correctness smoke (golden 50)
echo "Running diverse correctness smoke tests..."
.venv/bin/pytest tests/test_validation_system/ -q --maxfail=1
.venv/bin/pytest tests/test_diverse_correctness/ -m smoke -q --maxfail=1
```

- [ ] **Step 3: Test the hook**

Run: `.venv/bin/pytest tests/test_validation_system/ -q --maxfail=1 && .venv/bin/pytest tests/test_diverse_correctness/ -m smoke -q --maxfail=1`
Expected: Both pass

- [ ] **Step 4: Commit**

```bash
git add .git/hooks/pre-push
git commit -m "ci: add validation layer + diverse correctness smoke to pre-push hook"
```

---

## Execution Order Summary

| Task | Description | Depends on |
|------|-------------|-----------|
| 1 | Normalization module + tests | — |
| 2 | Diff engine core + tests | — |
| 3 | Classification logic + tests | Task 2 |
| 4 | Poison pill + invariant tests | Tasks 1, 2 |
| 5 | PyJHora batch computation | — |
| 6 | Chart selection tool | Task 5 |
| 7 | Diff engine pipeline | Tasks 1, 2, 3, 6 |
| 8 | Diff report tool | Task 7 |
| 9 | Diverse correctness test suite | Task 7 |
| 10 | Systematic patterns + history | Task 7 |
| 11 | CI integration | Tasks 9, 4 |

**Parallelizable:** Tasks 1, 2, 5 can run in parallel. Tasks 4 depends on 1+2. Task 3 depends on 2. Everything from Task 6 onward is sequential.

---

## Phase 2/3 Test Files (Future Tasks)

Phase 2 and Phase 3 test files follow the identical pattern as Phase 1 but cover additional modules. They are not included in this plan because:

1. Phase 1 proves the infrastructure works end-to-end
2. The diff engine must first run to establish which Phase 2/3 fields have agreement
3. Each follows the same `verified_chart` + `computed_chart` fixture pattern

**Phase 2 (after Phase 1 passes):**
- `test_dignity.py` — dignity level per planet
- `test_house_lords.py` — lord per house, planets-in-house
- `test_aspects.py` — planetary aspects (requires extending diff_engine field schema)

**Phase 3 (after Phase 2 passes):**
- `test_ashtakavarga.py` — binna AV, sarva AV
- `test_yogas.py` — yoga detection (canonicalized)
- `test_dashas.py` — vimsottari MD/AD periods
- `test_shadbala.py` — 6 strength components
- `test_vargas.py` — D9+ placements

Each will be a separate plan task when Phase 1 is stable and the diff report shows which fields are ready.
