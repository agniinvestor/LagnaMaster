# Condition Primitives & Encoding Governance — Implementation Plan

> **Status (2026-04-12 S323 audit): MOSTLY COMPLETE.**
> Taxonomy, builder validation, and audit tool all implemented. 4 new condition types
> (`planet_in_sign_type`, `planet_in_derived_house`, `upagraha_in_house`, `planet_in_house_from`)
> are in taxonomy.py, validated by v2_builder.py, and used in 8 V2 chapter files.
> `planet_in_house_from` and `upagraha_in_house` are evaluated by rule_firing.py.
> `planet_in_derived_house` and `planet_in_sign_type` are NOT yet in rule_firing.py (engine gap).
> Remaining: condition_modifier_fix.py not created, ENCODING_GRANULARITY.md not updated.

**Goal:** Add 3 new condition primitives (sign_type, derived_house, upagraha), fix condition/modifier misclassification across the V2 corpus, and update encoding guidelines.

**Architecture:** Schema-additive changes only. New condition `type` values added to taxonomy, validated in builder. Audit/fix scripts operate on chapter files. No RuleRecord changes. No engine changes.

**Tech Stack:** Python 3.14, pytest, ruff, existing V2ChapterBuilder

**Spec:** `docs/superpowers/specs/2026-04-02-condition-primitives-governance-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `src/corpus/taxonomy.py` | Modify | Add `VALID_SIGN_TYPES`, `VALID_DERIVATIONS`, `VALID_UPAGRAHAS`, `VALID_CONDITION_MODES`, extend `VALID_CONDITION_PRIMITIVES` |
| `src/corpus/v2_builder.py` | Modify | Validate new condition types in `_validate_add`, update `_build_primary_condition` |
| `tests/test_condition_primitives.py` | Create | Tests for new primitives — builder validation, rejection of invalid values |
| `tools/condition_modifier_audit.py` | Create | Audit script scanning V2 rules for misclassified conditions/modifiers |
| `tools/condition_modifier_fix.py` | Create | Fix script applying audit recommendations |
| `tests/test_condition_modifier_audit.py` | Create | Tests for audit script logic |
| `src/corpus/bphs_v2_ch25.py` | Modify | Replace `conditions=[]` with `upagraha_in_house` in `_upa` helper |
| `src/corpus/bphs_v2_ch16.py` | Modify | Fix BPHS1610 and BPHS1623 condition/modifier classification |
| `docs/ENCODING_GRANULARITY.md` | Modify | Add condition/modifier decision rule, anti-patterns, derived house guidance |
| `data/audit_trail/condition_modifier_fixes.json` | Create | Audit trail log for all auto-fixes |

---

### Task 1: Add new taxonomy sets

**Files:**
- Modify: `src/corpus/taxonomy.py`
- Create: `tests/test_condition_primitives.py`

- [ ] **Step 1: Write failing tests for new taxonomy sets**

```python
"""tests/test_condition_primitives.py — Tests for new condition primitives."""
from __future__ import annotations

import pytest

from src.corpus.taxonomy import (
    VALID_CONDITION_PRIMITIVES,
    VALID_SIGN_TYPES,
    VALID_DERIVATIONS,
    VALID_UPAGRAHAS,
    VALID_CONDITION_MODES,
)


# ── Taxonomy completeness ────────────────────────────────────────────────────

def test_sign_types_contains_movable():
    assert "movable" in VALID_SIGN_TYPES

def test_sign_types_contains_all_modalities():
    for st in ("movable", "fixed", "dual"):
        assert st in VALID_SIGN_TYPES

def test_sign_types_contains_all_elements():
    for st in ("fire", "earth", "air", "water"):
        assert st in VALID_SIGN_TYPES

def test_sign_types_contains_parity():
    for st in ("odd", "even"):
        assert st in VALID_SIGN_TYPES

def test_derivations_contains_arudha():
    assert "arudha_pada" in VALID_DERIVATIONS

def test_derivations_contains_upa_pada():
    assert "upa_pada" in VALID_DERIVATIONS

def test_derivations_contains_karakamsa():
    assert "karakamsa" in VALID_DERIVATIONS

def test_derivations_contains_all_special_lagnas():
    for d in ("navamsa_lagna", "hora_lagna", "ghati_lagna",
              "varnada_lagna", "sri_lagna", "indu_lagna", "pranapada_lagna"):
        assert d in VALID_DERIVATIONS

def test_upagrahas_contains_dhuma():
    assert "dhuma" in VALID_UPAGRAHAS

def test_upagrahas_contains_gulika():
    assert "gulika" in VALID_UPAGRAHAS

def test_upagrahas_contains_mandi():
    assert "mandi" in VALID_UPAGRAHAS

def test_condition_modes():
    assert VALID_CONDITION_MODES == frozenset({"occupies", "aspects"})

def test_new_primitives_in_valid_set():
    for p in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
        assert p in VALID_CONDITION_PRIMITIVES
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_condition_primitives.py -v`
Expected: FAIL — `ImportError: cannot import name 'VALID_SIGN_TYPES'`

- [ ] **Step 3: Implement taxonomy additions**

Add to `src/corpus/taxonomy.py` after `VALID_CONDITION_PRIMITIVES`:

```python
VALID_SIGN_TYPES = frozenset({
    "movable", "fixed", "dual",
    "fire", "earth", "air", "water",
    "odd", "even",
})

VALID_DERIVATIONS = frozenset({
    "arudha_pada", "upa_pada", "karakamsa",
    "navamsa_lagna", "hora_lagna", "ghati_lagna",
    "varnada_lagna", "sri_lagna", "indu_lagna", "pranapada_lagna",
})

VALID_UPAGRAHAS = frozenset({
    "dhuma", "vyatipata", "paridhi", "chapa", "dhwaja",
    "gulika", "pranapada", "mandi",
})

VALID_CONDITION_MODES = frozenset({
    "occupies", "aspects",
})
```

And extend `VALID_CONDITION_PRIMITIVES`:

```python
VALID_CONDITION_PRIMITIVES = frozenset({
    "planet_in_house", "planet_in_sign", "planets_conjunct_in_house",
    "planets_conjunct", "lord_in_house", "lord_in_sign",
    "planet_aspecting", "planet_dignity",
    # New primitives (S313 governance)
    "planet_in_sign_type",
    "planet_in_derived_house",
    "upagraha_in_house",
})
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_condition_primitives.py -v`
Expected: ALL PASS

- [ ] **Step 5: Run full test suite for regression**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 7,364+ passed, 0 failed

- [ ] **Step 6: Commit**

```bash
git add src/corpus/taxonomy.py tests/test_condition_primitives.py
git commit -m "feat: add VALID_SIGN_TYPES, VALID_DERIVATIONS, VALID_UPAGRAHAS, VALID_CONDITION_MODES to taxonomy

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Builder validation for new condition types

**Files:**
- Modify: `src/corpus/v2_builder.py`
- Modify: `tests/test_condition_primitives.py`

- [ ] **Step 1: Write failing tests for builder validation**

Append to `tests/test_condition_primitives.py`:

```python
from src.corpus.v2_builder import V2ChapterBuilder


def _make_builder(**kwargs):
    defaults = dict(
        chapter="Ch.99", category="test", id_start=9900,
        session="S999", sloka_count=10,
        chapter_tags=["test"],
    )
    defaults.update(kwargs)
    return V2ChapterBuilder(**defaults)


def _base_add(**overrides):
    """Return kwargs for a minimal valid b.add() call."""
    defaults = dict(
        conditions=[{"type": "planet_in_house", "planet": "sun", "house": 1}],
        signal_group="test_signal",
        direction="favorable", intensity="moderate",
        domains=["wealth"],
        predictions=[{"entity": "native", "claim": "test_claim_placeholder",
                       "domain": "wealth", "direction": "favorable", "magnitude": 0.5}],
        verse_ref="Ch.99 v.1",
        description="Test rule for condition primitive validation testing purposes.",
        commentary_context="Test commentary for validation.",
    )
    defaults.update(overrides)
    return defaults


# ── planet_in_sign_type validation ───────────────────────────────────────────

def test_sign_type_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"}],
    ))
    assert len(b.rules()) == 1


def test_sign_type_invalid_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "INVALID"}],
        ))


def test_sign_type_missing_sign_type_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5"}],
        ))


# ── planet_in_derived_house validation ───────────────────────────────────────

def test_derived_house_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 7, "planet": "rahu"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_invalid_derivation_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "INVALID",
                          "base_house": 1, "offset": 7, "planet": "rahu"}],
        ))


def test_derived_house_arudha_requires_base_house():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                          "offset": 7, "planet": "rahu"}],
        ))


def test_derived_house_karakamsa_no_base_house_ok():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "karakamsa",
                      "offset": 1, "planet": "jupiter"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_with_aspects_mode():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 11, "planet": "jupiter",
                      "mode": "aspects"}],
    ))
    assert len(b.rules()) == 1


def test_derived_house_invalid_mode_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                          "base_house": 1, "offset": 7, "planet": "rahu",
                          "mode": "INVALID"}],
        ))


# ── upagraha_in_house validation ────────────────────────────────────────────

def test_upagraha_valid_accepted():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma", "house": 3}],
    ))
    assert len(b.rules()) == 1


def test_upagraha_invalid_name_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "upagraha_in_house", "upagraha": "INVALID", "house": 3}],
        ))


def test_upagraha_missing_house_rejected():
    b = _make_builder()
    with pytest.raises(ValueError, match="T1-1"):
        b.add(**_base_add(
            conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma"}],
        ))


# ── _build_primary_condition for new types ───────────────────────────────────

def test_primary_condition_sign_type():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "planet_in_sign_type"
    assert r.primary_condition["planet"] == "lord_of_5"


def test_primary_condition_derived_house():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "planet_in_derived_house", "derivation": "arudha_pada",
                      "base_house": 1, "offset": 7, "planet": "rahu"}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "planet_in_derived_house"
    assert r.primary_condition["planet"] == "rahu"


def test_primary_condition_upagraha():
    b = _make_builder()
    b.add(**_base_add(
        conditions=[{"type": "upagraha_in_house", "upagraha": "dhuma", "house": 3}],
    ))
    r = b.rules()[0]
    assert r.primary_condition["placement_type"] == "upagraha_in_house"
    assert r.primary_condition["planet"] == "dhuma"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_condition_primitives.py -v -k "sign_type or derived_house or upagraha"`
Expected: FAIL — new condition types not validated, rejected by existing T1-1 whitelist (which will now include them but not validate sub-fields)

- [ ] **Step 3: Implement builder validation**

In `src/corpus/v2_builder.py`, inside `_validate_add`, after the existing T1-1 loop that checks `ctype not in VALID_CONDITION_PRIMITIVES`, add validation for new types:

```python
        # T1-1 extended: validate new condition primitives' sub-fields
        if ctype == "planet_in_sign_type":
            from src.corpus.taxonomy import VALID_SIGN_TYPES
            st = cond.get("sign_type", "")
            if not st or st not in VALID_SIGN_TYPES:
                errors.append(
                    f"T1-1: conditions[{i}].sign_type='{st}' not valid — "
                    f"use: {sorted(VALID_SIGN_TYPES)}"
                )
            if not cond.get("planet"):
                errors.append(f"T1-1: conditions[{i}] planet_in_sign_type missing 'planet'")

        elif ctype == "planet_in_derived_house":
            from src.corpus.taxonomy import VALID_DERIVATIONS, VALID_CONDITION_MODES
            deriv = cond.get("derivation", "")
            if not deriv or deriv not in VALID_DERIVATIONS:
                errors.append(
                    f"T1-1: conditions[{i}].derivation='{deriv}' not valid — "
                    f"use: {sorted(VALID_DERIVATIONS)}"
                )
            offset = cond.get("offset")
            if not isinstance(offset, int) or not (1 <= offset <= 12):
                errors.append(
                    f"T1-1: conditions[{i}].offset={offset} must be int 1-12"
                )
            if not cond.get("planet"):
                errors.append(f"T1-1: conditions[{i}] planet_in_derived_house missing 'planet'")
            mode = cond.get("mode", "occupies")
            if mode not in VALID_CONDITION_MODES:
                errors.append(
                    f"T1-1: conditions[{i}].mode='{mode}' not valid — "
                    f"use: {sorted(VALID_CONDITION_MODES)}"
                )
            # base_house required for house-based derivations
            _HOUSE_BASED = {"arudha_pada", "upa_pada"}
            if deriv in _HOUSE_BASED and not isinstance(cond.get("base_house"), int):
                errors.append(
                    f"T1-1: conditions[{i}] derivation='{deriv}' requires base_house (int 1-12)"
                )

        elif ctype == "upagraha_in_house":
            from src.corpus.taxonomy import VALID_UPAGRAHAS, VALID_CONDITION_MODES
            upa = cond.get("upagraha", "")
            if not upa or upa not in VALID_UPAGRAHAS:
                errors.append(
                    f"T1-1: conditions[{i}].upagraha='{upa}' not valid — "
                    f"use: {sorted(VALID_UPAGRAHAS)}"
                )
            house = cond.get("house")
            if not isinstance(house, int) or not (1 <= house <= 12):
                errors.append(
                    f"T1-1: conditions[{i}].house={house} must be int 1-12"
                )
            mode = cond.get("mode", "occupies")
            if mode not in VALID_CONDITION_MODES:
                errors.append(
                    f"T1-1: conditions[{i}].mode='{mode}' not valid — "
                    f"use: {sorted(VALID_CONDITION_MODES)}"
                )
```

In `_build_primary_condition`, add after the last `elif`:

```python
        elif ct in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
            pc["planet"] = c0.get("planet", c0.get("upagraha", "general"))
            pc["placement_type"] = ct
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_condition_primitives.py -v`
Expected: ALL PASS

- [ ] **Step 5: Run full test suite for regression**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 7,364+ passed, 0 failed

- [ ] **Step 6: Lint check**

Run: `.venv/bin/ruff check src/corpus/v2_builder.py src/corpus/taxonomy.py tests/test_condition_primitives.py`
Expected: 0 errors

- [ ] **Step 7: Commit**

```bash
git add src/corpus/v2_builder.py src/corpus/taxonomy.py tests/test_condition_primitives.py
git commit -m "feat: builder validation for planet_in_sign_type, planet_in_derived_house, upagraha_in_house

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Condition/modifier audit script

**Files:**
- Create: `tools/condition_modifier_audit.py`
- Create: `tests/test_condition_modifier_audit.py`

- [ ] **Step 1: Write failing tests for audit logic**

```python
"""tests/test_condition_modifier_audit.py — Tests for condition/modifier audit."""
from __future__ import annotations

from tools.condition_modifier_audit import classify_modifier, scan_commentary_for_missing_exceptions


def test_classify_must_keyword_high():
    result = classify_modifier(
        modifier={"condition": "2nd_lord_must_be_in_10th", "effect": "conditionalizes"},
        commentary="Santhanam: Eight sons if Jupiter in 5th/9th + 5th lord strong + 2nd lord in 10th.",
    )
    assert result["confidence"] == "high"
    assert result["type"] == "modifier_should_be_condition"


def test_classify_required_keyword_high():
    result = classify_modifier(
        modifier={"condition": "moon_rahu_conjunction_required", "effect": "amplifies"},
        commentary="Three conditions required: (a) Saturn in 5th (b) lord in movable (c) Moon with Rahu.",
    )
    assert result["confidence"] == "high"


def test_classify_enumeration_pattern_high():
    result = classify_modifier(
        modifier={"condition": "h5_lord_in_movable_sign", "effect": "conditionalizes"},
        commentary="Santhanam notes: 3 conditions — (a) 5th lord in movable sign, (b) Saturn in 5th, (c) Moon with Rahu.",
    )
    assert result["confidence"] == "high"


def test_classify_placement_pattern_medium():
    result = classify_modifier(
        modifier={"condition": "benefic_in_12th", "effect": "amplifies"},
        commentary="No separate Santhanam note.",
    )
    assert result["confidence"] == "medium"


def test_classify_amplifier_low():
    result = classify_modifier(
        modifier={"condition": "aspected_by_benefic_more_favorable", "effect": "amplifies"},
        commentary="Benefic aspect makes results more favorable.",
    )
    assert result["confidence"] == "low"


def test_missing_exception_detected():
    flags = scan_commentary_for_missing_exceptions(
        commentary="The combinations get nullified if Jupiter aspects the 5th house.",
        exceptions=[],
    )
    assert len(flags) == 1
    assert "nullified" in flags[0]["evidence"].lower()


def test_no_false_positive_exception():
    flags = scan_commentary_for_missing_exceptions(
        commentary="No separate Santhanam note.",
        exceptions=[],
    )
    assert len(flags) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_condition_modifier_audit.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.condition_modifier_audit'`

- [ ] **Step 3: Implement audit script**

```python
"""tools/condition_modifier_audit.py — Audit V2 rules for condition/modifier misclassification.

Scans all bphs_v2_ch*.py files. For each rule, checks if any modifier
should actually be a condition (based on commentary evidence) and if any
exceptions are missing (based on "nullified"/"cancelled" keywords).

Usage:
    .venv/bin/python tools/condition_modifier_audit.py [--json]
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path


def classify_modifier(*, modifier: dict, commentary: str) -> dict:
    """Classify a single modifier as correctly placed or misclassified.

    Returns dict with 'type', 'confidence', 'evidence'.
    """
    cond_text = modifier.get("condition", "").lower()
    comm_lower = commentary.lower()

    # High confidence: "must", "required", "necessary" in modifier condition text
    _REQUIRED_KW = ("must", "required", "necessary")
    for kw in _REQUIRED_KW:
        if kw in cond_text:
            return {
                "type": "modifier_should_be_condition",
                "confidence": "high",
                "evidence": f"Modifier condition contains '{kw}'",
            }

    # High confidence: commentary has enumeration pattern (a), (b), (c)
    enum_pattern = re.search(r'\(a\).*\(b\)', comm_lower)
    if enum_pattern:
        # Check if this modifier's condition text appears near an enumeration item
        cond_words = set(cond_text.replace("_", " ").split())
        if len(cond_words & set(comm_lower.split())) >= 3:
            return {
                "type": "modifier_should_be_condition",
                "confidence": "high",
                "evidence": "Commentary enumerates conditions with (a)(b)(c) pattern",
            }

    # High confidence: commentary says "3 conditions" or "N conditions"
    if re.search(r'\d+\s+conditions?\s', comm_lower):
        return {
            "type": "modifier_should_be_condition",
            "confidence": "high",
            "evidence": "Commentary explicitly counts conditions",
        }

    # Medium confidence: modifier describes a placement/conjunction
    _PLACEMENT_KW = ("lord", "in_house", "in_h", "conjunct", "in_sign",
                      "in_movable", "in_fixed", "in_dual", "aspected")
    if any(kw in cond_text for kw in _PLACEMENT_KW):
        return {
            "type": "modifier_should_be_condition",
            "confidence": "medium",
            "evidence": "Modifier condition describes a placement or conjunction",
        }

    # Low confidence: ambiguous
    return {
        "type": "modifier_possibly_misclassified",
        "confidence": "low",
        "evidence": "Ambiguous — could be required or amplifying",
    }


def scan_commentary_for_missing_exceptions(*, commentary: str, exceptions: list) -> list[dict]:
    """Check if commentary mentions cancellation but exceptions list is empty."""
    if exceptions:
        return []

    flags = []
    _CANCEL_KW = ("nullified", "cancelled", "canceled", "exception",
                   "does not apply", "gets negated")
    comm_lower = commentary.lower()
    for kw in _CANCEL_KW:
        if kw in comm_lower:
            flags.append({
                "type": "missing_exception",
                "confidence": "medium",
                "evidence": f"Commentary contains '{kw}' but exceptions list is empty",
            })
            break  # one flag per rule for this check
    return flags


def audit_registry(registry, chapter_name: str) -> list[dict]:
    """Audit all rules in a registry. Returns list of flag dicts."""
    results = []
    for rule in registry.all():
        rule_flags = []

        # Check each modifier
        for i, mod in enumerate(rule.modifiers or []):
            classification = classify_modifier(
                modifier=mod,
                commentary=rule.commentary_context or "",
            )
            if classification["confidence"] != "low" or classification["type"] == "modifier_should_be_condition":
                rule_flags.append({
                    **classification,
                    "modifier_index": i,
                    "current_value": mod,
                })

        # Check for missing exceptions
        exception_flags = scan_commentary_for_missing_exceptions(
            commentary=rule.commentary_context or "",
            exceptions=rule.exceptions or [],
        )
        rule_flags.extend(exception_flags)

        if rule_flags:
            results.append({
                "rule_id": rule.rule_id,
                "chapter": chapter_name,
                "verse_ref": rule.verse_ref,
                "flags": rule_flags,
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Audit V2 rules for condition/modifier issues")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Find all V2 chapter modules
    corpus_dir = Path("src/corpus")
    chapters = sorted(corpus_dir.glob("bphs_v2_ch*.py"))

    all_results = []
    for ch_path in chapters:
        module_name = f"src.corpus.{ch_path.stem}"
        mod = importlib.import_module(module_name)
        # Find the registry (named BPHS_V2_CH*_REGISTRY)
        reg_name = [n for n in dir(mod) if n.endswith("_REGISTRY") and n.startswith("BPHS")]
        if not reg_name:
            continue
        registry = getattr(mod, reg_name[0])
        results = audit_registry(registry, ch_path.stem)
        all_results.extend(results)

    if args.json:
        print(json.dumps(all_results, indent=2))
    else:
        high = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "high")
        medium = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "medium")
        low = sum(1 for r in all_results for f in r["flags"] if f["confidence"] == "low")
        print(f"Audit complete: {len(all_results)} rules flagged")
        print(f"  High confidence:   {high}")
        print(f"  Medium confidence: {medium}")
        print(f"  Low confidence:    {low}")
        for r in all_results:
            for f in r["flags"]:
                if f["confidence"] in ("high", "medium"):
                    print(f"  {r['rule_id']} ({r['verse_ref']}): [{f['confidence']}] {f['evidence']}")

    sys.exit(1 if high > 0 else 0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_condition_modifier_audit.py -v`
Expected: ALL PASS

- [ ] **Step 5: Run audit on actual corpus**

Run: `.venv/bin/python tools/condition_modifier_audit.py`
Expected: Output showing flagged rules (BPHS1610, BPHS1623, possibly others)

- [ ] **Step 6: Lint check**

Run: `.venv/bin/ruff check tools/condition_modifier_audit.py tests/test_condition_modifier_audit.py`
Expected: 0 errors

- [ ] **Step 7: Commit**

```bash
git add tools/condition_modifier_audit.py tests/test_condition_modifier_audit.py
git commit -m "feat: condition/modifier audit script — detects misclassified conditions and missing exceptions

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Fix BPHS1610 and BPHS1623 (manual, high-value fixes)

**Files:**
- Modify: `src/corpus/bphs_v2_ch16.py`

- [ ] **Step 1: Read current BPHS1610 and BPHS1623 in ch16 file**

Read: `src/corpus/bphs_v2_ch16.py` and locate BPHS1610 (v.14) and BPHS1623 (v.26).

- [ ] **Step 2: Fix BPHS1610 — move modifiers to conditions, add exceptions**

Change BPHS1610 from:
```python
conditions=[
    {"type": "lord_in_house", "lord_of": 5, "house": "any"},
    {"type": "planet_in_house", "planet": "Saturn", "house": 5},
]
modifiers=[
    {"condition": "h5_lord_in_movable_sign", "effect": "conditionalizes", "strength": "strong"},
    {"condition": "moon_conjunct_rahu_in_5th_indicates_illegitimate_child", "effect": "amplifies", "strength": "moderate"},
]
exceptions=[]
```

To:
```python
conditions=[
    {"type": "planet_in_house", "planet": "Saturn", "house": 5},
    {"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"},
    {"type": "planets_conjunct", "planets": ["moon", "rahu"]},
]
modifiers=[]
exceptions=[
    "strong_jupiter_aspect_on_5th_nullifies",
    "5th_lord_exalted_and_unafflicted_nullifies",
]
```

- [ ] **Step 3: Fix BPHS1623 — move modifier to condition**

Change BPHS1623 from:
```python
modifiers=[
    {"condition": "2nd_lord_must_be_in_10th", "effect": "conditionalizes", "strength": "strong"},
]
```

To:
```python
conditions=[
    {"type": "planet_in_house", "planet": "Jupiter", "house": [5, 9]},
    {"type": "lord_in_house", "lord_of": 5, "house": "any"},
    {"type": "planet_dignity", "planet": "lord_of_5", "dignity": "strong"},
    {"type": "lord_in_house", "lord_of": 2, "house": 10},
]
modifiers=[]
```

- [ ] **Step 4: Run Ch.16 tests**

Run: `.venv/bin/pytest tests/ -q --tb=short -k "ch16 or ch_16"`
Expected: PASS

- [ ] **Step 5: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 7,364+ passed

- [ ] **Step 6: Create audit trail entry**

Create `data/audit_trail/condition_modifier_fixes.json`:
```json
[
    {
        "rule_id": "BPHS1610",
        "date": "2026-04-02",
        "change_type": "modifier_to_condition",
        "confidence": "high",
        "before_modifiers": [
            {"condition": "h5_lord_in_movable_sign", "effect": "conditionalizes", "strength": "strong"},
            {"condition": "moon_conjunct_rahu_in_5th_indicates_illegitimate_child", "effect": "amplifies", "strength": "moderate"}
        ],
        "after_conditions_added": [
            {"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"},
            {"type": "planets_conjunct", "planets": ["moon", "rahu"]}
        ],
        "exceptions_added": ["strong_jupiter_aspect_on_5th_nullifies", "5th_lord_exalted_and_unafflicted_nullifies"],
        "source": "manual_fix_from_commentary"
    },
    {
        "rule_id": "BPHS1623",
        "date": "2026-04-02",
        "change_type": "modifier_to_condition",
        "confidence": "high",
        "before_modifiers": [
            {"condition": "2nd_lord_must_be_in_10th", "effect": "conditionalizes", "strength": "strong"}
        ],
        "after_conditions_added": [
            {"type": "lord_in_house", "lord_of": 2, "house": 10}
        ],
        "source": "manual_fix_from_commentary"
    }
]
```

- [ ] **Step 7: Commit**

```bash
git add src/corpus/bphs_v2_ch16.py data/audit_trail/condition_modifier_fixes.json
git commit -m "fix: BPHS1610/1623 — move required conditions from modifiers, add missing exceptions

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Update Ch.25 upagrahas to use new primitive

**Files:**
- Modify: `src/corpus/bphs_v2_ch25.py`

- [ ] **Step 1: Update `_upa` helper function**

Change:
```python
def _upa(upagraha: str, house: int, signal: str, direction: str,
         intensity: str, domains: list[str], claim: str,
         verse_ref: str, desc: str, commentary: str,
         concordance: list[str] | None = None,
         **kwargs) -> None:
    """Helper to add a upagraha-in-house rule with consistent structure."""
    b.add(
        conditions=[],
```

To:
```python
def _upa(upagraha: str, house: int, signal: str, direction: str,
         intensity: str, domains: list[str], claim: str,
         verse_ref: str, desc: str, commentary: str,
         concordance: list[str] | None = None,
         **kwargs) -> None:
    """Helper to add a upagraha-in-house rule with consistent structure."""
    b.add(
        conditions=[{"type": "upagraha_in_house", "upagraha": upagraha,
                      "house": house, "mode": "occupies"}],
```

- [ ] **Step 2: Run Ch.25 tests**

Run: `.venv/bin/pytest tests/ -q --tb=short -k "ch25 or ch_25"`
Expected: PASS

- [ ] **Step 3: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 7,364+ passed

- [ ] **Step 4: Commit**

```bash
git add src/corpus/bphs_v2_ch25.py
git commit -m "fix: Ch.25 upagrahas — replace conditions=[] with upagraha_in_house primitive

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Update encoding guidelines

**Files:**
- Modify: `docs/ENCODING_GRANULARITY.md`

- [ ] **Step 1: Add condition/modifier decision rule**

Append to `docs/ENCODING_GRANULARITY.md` after the "Mechanical Check" section:

```markdown
## Condition vs Modifier vs Exception — Decision Rule

> If the commentary says the condition is **required** for the prediction to hold, it's a **condition**.
> If the commentary says the condition **strengthens, weakens, or contextualizes** an already-valid prediction, it's a **modifier**.
> If the commentary says the condition **completely cancels** the prediction, it's an **exception**.

### Mechanical Test

| Question | If yes | If no |
|----------|--------|-------|
| "Does the prediction fire WITHOUT this factor?" | modifier | condition |
| "Does this factor CANCEL the prediction entirely?" | exception | not an exception |
| "Is this factor REQUIRED by the text (must/necessary/enumerates)?" | condition | use first question |

### Anti-Patterns (DO NOT do these)

- `"house": "any"` — use `planet_in_sign_type` with appropriate `sign_type`
- Required conditions as modifiers — if commentary says "must" / "necessary" / enumerates as (a)(b)(c), these are conditions
- Empty `exceptions` when commentary says "nullified" / "cancelled" — encode the cancellation clause
- `conditions=[]` for upagrahas — use `upagraha_in_house`
- `conditions=[]` for derived houses — use `planet_in_derived_house`

### Derived House Conditions (Ch.29+)

For rules referencing houses counted from Arudha Pada, Upa Pada, Karakamsa, or other derived points:

```python
{"type": "planet_in_derived_house", "derivation": "arudha_pada",
 "base_house": 1, "offset": 7, "planet": "rahu", "mode": "occupies"}
```

- `derivation`: which derived system (arudha_pada, upa_pada, karakamsa, navamsa_lagna, etc.)
- `base_house`: which house's pada (1-12). Required for arudha_pada and upa_pada.
- `offset`: house counted from the derived anchor (1-12)
- `mode`: "occupies" (default) or "aspects"
```

- [ ] **Step 2: Commit**

```bash
git add docs/ENCODING_GRANULARITY.md
git commit -m "docs: add condition/modifier decision rule and anti-patterns to ENCODING_GRANULARITY

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Deferred: `tools/condition_modifier_fix.py`

The spec defines an automated fix script. This is deferred until after Task 3's audit reveals the full scope of medium-confidence flags. The known high-confidence fixes (BPHS1610, BPHS1623) are handled manually in Task 4. If the audit shows 10+ rules need fixing, build the fix script in a follow-up session.

---

### Task 7: Final validation

**Files:** None (validation only)

- [ ] **Step 1: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 7,364+ passed, 0 failed

- [ ] **Step 2: Run lint**

Run: `.venv/bin/ruff check src/ tests/ tools/`
Expected: 0 errors

- [ ] **Step 3: Run scorecard**

Run: `.venv/bin/python tools/v2_scorecard.py --all`
Expected: No regressions

- [ ] **Step 4: Run condition/modifier audit**

Run: `.venv/bin/python tools/condition_modifier_audit.py`
Expected: 0 high-confidence flags (BPHS1610 and BPHS1623 fixed)

- [ ] **Step 5: Verify Ch.25 conditions are populated**

Run: `.venv/bin/python -c "from src.corpus.bphs_v2_ch25 import BPHS_V2_CH25_REGISTRY; r=BPHS_V2_CH25_REGISTRY.all()[0]; print(r.primary_condition)"`
Expected: `placement_type` is `upagraha_in_house`, not empty

- [ ] **Step 6: Final commit (if any remaining changes)**

Only if lint or tests required fixes.
