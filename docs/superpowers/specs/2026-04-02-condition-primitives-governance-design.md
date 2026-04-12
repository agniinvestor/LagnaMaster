# Condition Primitives & Encoding Governance — Design Spec

**Date:** 2026-04-02
**Session type:** Governance
**Scope:** New condition primitives, condition/modifier classification, audit pipeline, encoding guidelines

> **Status (2026-04-12):** MOSTLY COMPLETE. All 4 primitives in taxonomy + builder. 2 of 4 in rule_firing engine. Used in 8 V2 chapters. See plan for remaining items.

---

## Problem Statement

Three gaps in the current encoding system:

1. **Missing condition primitives** — No way to express "planet in derived house" (Arudha Pada, Karakamsa), "planet in sign type" (movable/fixed/dual), or "upagraha in house." Ch.25 uses `conditions=[]` as a workaround. Ch.29+ is blocked entirely.

2. **Condition/modifier misclassification** — Required conditions are encoded as modifiers (e.g., BPHS1610 has 3 required conditions per commentary, but only 2 are in `conditions`). Missing exceptions where commentary says "nullified." No mechanical decision rule existed for classification.

3. **Encoding guideline gaps** — No documented anti-patterns. No decision rule for condition vs modifier boundary.

---

## Design Decisions

- **Schema-additive, non-breaking.** New condition `type` values added to taxonomy. No changes to RuleRecord dataclass. No changes to existing rule structure.
- **Source Fidelity preserved.** No "inferred conditions" — only encode what the text explicitly states.
- **Audit is separate from validation.** Builder validates schema correctness (T1 gates). Audit tools validate encoding quality. Different concerns, different tools.

---

## Section 1: New Condition Primitives

### 1.1 `planet_in_sign_type`

```python
{
    "type": "planet_in_sign_type",
    "planet": "lord_of_5",
    "sign_type": "movable"
}
```

**Purpose:** Express "5th lord in a movable sign" — currently hacked as `"house": "any"`.

**Taxonomy addition:**
```python
VALID_SIGN_TYPES = frozenset({
    "movable", "fixed", "dual",
    "fire", "earth", "air", "water",
    "odd", "even",
})
```

### 1.2 `planet_in_derived_house`

```python
{
    "type": "planet_in_derived_house",
    "derivation": "arudha_pada",
    "base_house": 1,
    "offset": 7,
    "planet": "rahu",
    "mode": "occupies"
}
```

**Purpose:** Express "Rahu in 7th from Arudha Lagna" and similar derived-house conditions.

**Fields:**
- `derivation` — which derived system. Validated against `VALID_DERIVATIONS`.
- `base_house` — which house's pada (1-12). **Required** for `arudha_pada` and `upa_pada`. Optional for planet-derived anchors (`karakamsa`, `navamsa_lagna`, etc.).
- `offset` — house counted from the derived anchor (1-12).
- `planet` — what occupies or aspects that position. Standard planet names from T1-3.
- `mode` — `"occupies"` (default) or `"aspects"`. No `"conjunct_lord"` — conjunction with a derived lord is a separate `planets_conjunct` condition.

**Taxonomy addition:**
```python
VALID_DERIVATIONS = frozenset({
    "arudha_pada", "upa_pada", "karakamsa",
    "navamsa_lagna", "hora_lagna", "ghati_lagna",
    "varnada_lagna", "sri_lagna", "indu_lagna", "pranapada_lagna",
})

VALID_CONDITION_MODES = frozenset({
    "occupies", "aspects",
})
```

**Engine resolution (internal, not exposed in condition dict):**
1. Resolve derived anchor from `derivation` + `base_house`
2. Count `offset` houses from anchor
3. Check `planet` occupancy or aspect per `mode`

### 1.3 `upagraha_in_house`

```python
{
    "type": "upagraha_in_house",
    "upagraha": "dhuma",
    "house": 3,
    "mode": "occupies"
}
```

**Purpose:** Replace `conditions=[]` in Ch.25 with proper structured conditions.

**Taxonomy addition:**
```python
VALID_UPAGRAHAS = frozenset({
    "dhuma", "vyatipata", "paridhi", "chapa", "dhwaja",
    "gulika", "pranapada", "mandi",
})
```

### 1.4 Updated `VALID_CONDITION_PRIMITIVES`

```python
VALID_CONDITION_PRIMITIVES = frozenset({
    # Existing
    "planet_in_house", "planet_in_sign", "planets_conjunct_in_house",
    "planets_conjunct", "lord_in_house", "lord_in_sign",
    "planet_aspecting", "planet_dignity",
    # New
    "planet_in_sign_type",
    "planet_in_derived_house",
    "upagraha_in_house",
})
```

---

## Section 2: Builder Updates

### 2.1 `_validate_add` additions (T1-1 loop)

For `planet_in_sign_type`:
- Validate `sign_type` present and in `VALID_SIGN_TYPES`
- Validate `planet` present

For `planet_in_derived_house`:
- Validate `derivation` present and in `VALID_DERIVATIONS`
- Validate `offset` present and in range 1-12
- Validate `planet` present
- Validate `mode` in `VALID_CONDITION_MODES` (default `"occupies"`)
- If `derivation` in `{"arudha_pada", "upa_pada"}`: validate `base_house` present and in 1-12

For `upagraha_in_house`:
- Validate `upagraha` present and in `VALID_UPAGRAHAS`
- Validate `house` present and in range 1-12
- Validate `mode` in `VALID_CONDITION_MODES` (default `"occupies"`)

### 2.2 `_build_primary_condition` changes

Stop proliferating `placement_type` strings. For new condition types:

```python
elif ct in ("planet_in_sign_type", "planet_in_derived_house", "upagraha_in_house"):
    pc["planet"] = c0.get("planet", c0.get("upagraha", "general"))
    pc["placement_type"] = ct  # reuse condition type directly
```

One source of truth: the `conditions` list. `primary_condition` is backward-compat only.

---

## Section 3: Condition/Modifier Classification Rule

### 3.1 Decision rule (added to ENCODING_GRANULARITY.md)

> If the commentary says the condition is **required** for the prediction to hold, it's a **condition**.
> If the commentary says the condition **strengthens, weakens, or contextualizes** an already-valid prediction, it's a **modifier**.
> If the commentary says the condition **completely cancels** the prediction, it's an **exception**.

### 3.2 Mechanical test

| Question | If yes | If no |
|----------|--------|-------|
| "Does the prediction fire WITHOUT this factor?" | modifier | condition |
| "Does this factor CANCEL the prediction entirely?" | exception | not an exception |
| "Is this factor REQUIRED by the text?" | condition | check first question |

### 3.3 Anti-patterns (added to ENCODING_GRANULARITY.md)

**Don't do:**
- `"house": "any"` — use `planet_in_sign_type` instead
- Required conditions as modifiers — if the commentary says "must" / "necessary" / enumerates as (a)(b)(c), these are conditions
- Empty `exceptions` when commentary says "nullified" / "cancelled"
- `conditions=[]` for upagrahas — use `upagraha_in_house`
- `conditions=[]` for derived houses — use `planet_in_derived_house`
- Literal number predictions without context — "8 sons" should remain literal (Source Fidelity) but add tag `symbolic_number` when the number likely represents abundance

**Do:**
- Use the "does it fire without it?" test for every modifier
- Split rules by entity per granularity principle #2
- Encode cancellation clauses as exceptions
- Use `planet_in_derived_house` for all Pada/Arudha/Karakamsa conditions

---

## Section 4: Audit and Fix Pipeline

### 4.1 `tools/condition_modifier_audit.py`

**Input:** All V2 chapter files (bphs_v2_ch*.py)

**Logic per rule:**
1. Parse `modifiers` list — extract each modifier's `condition` text
2. Parse `commentary_context`
3. **High confidence flags:**
   - Modifier `condition` contains "must", "required", "necessary"
   - Commentary contains enumeration pattern: `(a)`, `(b)`, `(c)` — and enumerated items appear in modifiers instead of conditions
   - Commentary contains "and X and Y" conjunction where X/Y are in modifiers
4. **Medium confidence flags:**
   - Modifier `condition` describes a placement or conjunction (contains "lord", "in_house", "conjunct", "in_sign")
   - Commentary mentions "nullified" / "cancelled" / "exception" but `exceptions` list is empty
5. **Low confidence flags:**
   - Modifier `condition` is ambiguous (could be required or amplifying)

**Output:** JSON report:
```json
{
    "rule_id": "BPHS1610",
    "flags": [
        {
            "type": "modifier_should_be_condition",
            "modifier_index": 0,
            "evidence": "Commentary enumerates as condition (a)",
            "confidence": "high",
            "current_value": {"condition": "h5_lord_in_movable_sign", ...},
            "suggested_condition": {"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"}
        }
    ]
}
```

### 4.2 `tools/condition_modifier_fix.py`

**Input:** Audit report JSON + `--auto-fix` flag

**Behavior:**
- `--auto-fix`: Apply all `high` confidence fixes automatically. Report `medium` flags. Skip `low`.
- Without flag: Dry-run, report only.

**Auto-fix constraint — deterministic mappings only:**
- Only auto-convert a modifier string to a structured condition dict when the mapping is unambiguous and 1:1 (e.g., `"2nd_lord_must_be_in_10th"` → `{"type": "lord_in_house", "lord_of": 2, "house": 10}`)
- If the modifier string is ambiguous (e.g., `"Moon with Rahu"` could be `planets_conjunct` or `planets_conjunct_in_house`), move it to `conditions` as a raw descriptive string and flag for manual structuring
- This prevents silent schema corruption from aggressive parsing

**Per fix:**
1. Read chapter file
2. Move flagged modifier to `conditions` list, converting to proper condition dict only when deterministic
3. Add missing exceptions from "nullified" commentary clauses
4. Write updated file
5. Run `v2_scorecard.py --file <chapter>` to verify

### 4.3 Audit trail

The fix script writes all changes to `data/audit_trail/condition_modifier_fixes.json`:
```json
[
    {
        "rule_id": "BPHS1610",
        "date": "2026-04-02",
        "change_type": "modifier_to_condition",
        "confidence": "high",
        "before": {"condition": "h5_lord_in_movable_sign", "effect": "conditionalizes", "strength": "strong"},
        "after": {"type": "planet_in_sign_type", "planet": "lord_of_5", "sign_type": "movable"},
        "source": "auto_fix_deterministic"
    }
]
```

No RuleRecord schema changes. Traceability via external log file.

### 4.4 Scope

Only existing V2 chapter files (Ch.12-25). Does not touch legacy Phase 1A files.

---

## Section 5: Ch.25 Upagraha Fix

Update `bphs_v2_ch25.py`:

Change `_upa` helper from:
```python
conditions=[]
```
To:
```python
conditions=[{"type": "upagraha_in_house", "upagraha": upagraha, "house": house, "mode": "occupies"}]
```

No other changes to rules. 86 rules updated mechanically.

---

## Section 6: Validation

1. Run full test suite: `.venv/bin/pytest tests/ -q --tb=short`
2. Run scorecard: `.venv/bin/python tools/v2_scorecard.py --all`
3. Run lint: `.venv/bin/ruff check src/ tests/`
4. Run new audit script: `.venv/bin/python tools/condition_modifier_audit.py`
5. Verify 0 high-confidence flags remaining after fixes

---

## Files Modified

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add 4 new frozensets + extend `VALID_CONDITION_PRIMITIVES` |
| `src/corpus/v2_builder.py` | Add validation for 3 new types in `_validate_add`, update `_build_primary_condition` |
| `docs/ENCODING_GRANULARITY.md` | Add condition/modifier decision rule, anti-patterns section, derived house guidance |
| `tools/condition_modifier_audit.py` | New — audit script |
| `tools/condition_modifier_fix.py` | New — fix script |
| `src/corpus/bphs_v2_ch25.py` | Update 86 rules from `conditions=[]` to `upagraha_in_house` |
| `src/corpus/bphs_v2_ch16.py` | Fix BPHS1610 (conditions + exceptions) and BPHS1623 (condition reclassification) |
| `src/corpus/bphs_v2_ch13.py` | Fix BPHS1311 if audit flags it |

---

## Not In Scope

- No RuleRecord schema changes
- No engine computation of derived houses (future session)
- No "inferred conditions" — Source Fidelity preserved
- No signal→effects→domains pipeline redesign
- No chart-level regression testing (no engine changes to regress)
