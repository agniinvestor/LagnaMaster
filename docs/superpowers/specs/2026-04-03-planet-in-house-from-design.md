# Design Spec: `planet_in_house_from` Condition Primitive

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Approved
**Scope:** New condition primitive + migration of 9 existing workarounds

## Problem

BPHS frequently expresses conditions relative to a planet's position rather than the ascendant: "malefic in 5th from Jupiter", "Saturn in 8th from Rahu", "Venus in 7th from Moon". The current condition type system has no primitive for this. All 9 occurrences across Ch.16-18 are encoded as text-only modifiers with no engine evaluation, or in one case (Ch.17 v.20-22) completely unencoded.

## Decision

Add `planet_in_house_from` as a new condition primitive. Implement occupancy mode only. Schema accommodates future aspect mode without breaking changes.

## Schema

```json
{
  "type": "planet_in_house_from",
  "planet": "Saturn",
  "reference": "Rahu",
  "offset": 8,
  "mode": "occupies"
}
```

### Field Definitions

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `type` | string | yes | `"planet_in_house_from"` | Primitive identifier |
| `planet` | string | yes | Planet name, `any_malefic`, `any_benefic`, or `lord_of_N` | Who must be in the target house. Multi-resolvable. |
| `reference` | string | yes | Planet name or `lord_of_N`. NOT `any_malefic`/`any_benefic`. | The planet from which offset is computed. Must resolve to exactly one planet. |
| `offset` | int | yes | 1–12 | House offset from reference. 1 = same house, 7 = opposite, 12 = 12th from. |
| `mode` | string | yes | `"occupies"` only (validation rejects anything else) | Evaluation mode. Reserved for future `"aspects"` extension. |

### Resolution Rules

- **`planet`** (target): may resolve to N >= 1 candidates. Condition fires if ANY candidate occupies the computed target house.
- **`reference`** (origin): must resolve to exactly 1 planet. `any_malefic`/`any_benefic` rejected at builder validation because "Nth from any malefic" is undefined.
- **`lord_of_N`**: supported for both fields. Resolved via `_lord_of_house()`.
- **`any_planet`**: NOT supported (always true = useless condition).

### Offset Semantics

Offset uses BPHS counting convention (inclusive of starting house):
- offset=1 → same house as reference (equivalent to conjunction check)
- offset=5 → 5th house from reference
- offset=7 → opposite house from reference
- offset=12 → 12th from reference

Computation: `target_house = (reference_house + offset - 1) % 12 + 1`

### House System Assumption

This primitive assumes whole-sign house calculation. House positions are integer values 1-12 derived from sign indices. If house system changes in future (e.g., Placidus), this primitive must be re-evaluated.

### Planet Name Normalization

All planet identifiers must be normalized via a single helper (`_normalize_planet()` or equivalent). Direct string transformations (e.g., `.title()`) are not allowed in evaluation logic. This ensures consistency across rule_firing, lord resolution, and future alias handling.

### Failure Semantics

The condition returns `(False, 0)` if:
1. `reference` cannot be resolved to exactly one planet
2. No valid candidate planets are found for `planet`
3. No candidate occupies the computed target house

## Builder Validation

In `v2_builder.py:_validate_add()`:

```python
elif ctype == "planet_in_house_from":
    if not cond.get("planet"):
        errors.append(f"T1-1: conditions[{i}] planet_in_house_from missing 'planet'")
    ref = cond.get("reference", "")
    if not ref:
        errors.append(f"T1-1: conditions[{i}] planet_in_house_from missing 'reference'")
    elif ref in ("any_malefic", "any_benefic"):
        errors.append(
            f"T1-1: conditions[{i}] planet_in_house_from 'reference' must resolve "
            f"to single planet, not '{ref}'"
        )
    offset = cond.get("offset")
    if not isinstance(offset, int) or not (1 <= offset <= 12):
        errors.append(f"T1-1: conditions[{i}].offset={offset} must be int 1-12")
    mode = cond.get("mode", "")
    if mode != "occupies":
        errors.append(
            f"T1-1: conditions[{i}].mode='{mode}' must be 'occupies' "
            f"(only supported mode)"
        )
```

## Engine Evaluation

In `rule_firing.py:_check_compound_conditions()`:

```python
elif ctype == "planet_in_house_from":
    planet_spec = cond.get("planet", "")
    ref_spec = cond.get("reference", "")
    offset = cond.get("offset", 0)

    # Resolve reference → must be exactly 1 planet
    resolved_ref = []
    if ref_spec.startswith("lord_of_"):
        h = int(ref_spec.split("_")[-1])
        p = _lord_of_house(chart, h)
        if p:
            resolved_ref = [p]
    else:
        p = ref_spec.title()
        if _find_planet(chart, p):
            resolved_ref = [p]

    if len(resolved_ref) != 1:
        return False, 0

    ref_planet = resolved_ref[0]
    ref_house = _planet_house(chart, ref_planet)
    target_house = (ref_house + offset - 1) % 12 + 1

    # Resolve planet → may be multiple (any_malefic, etc.)
    if planet_spec == "any_malefic":
        candidates = _MALEFICS
    elif planet_spec == "any_benefic":
        candidates = _BENEFICS
    elif planet_spec.startswith("lord_of_"):
        lh = int(planet_spec.split("_")[-1])
        lord = _lord_of_house(chart, lh)
        candidates = [lord] if lord else []
    else:
        candidates = [planet_spec.title()]

    valid_candidates = [c for c in candidates if _find_planet(chart, c)]
    if not valid_candidates:
        return False, 0

    hit = any(_planet_house(chart, c) == target_house for c in valid_candidates)
    if not hit:
        return False, 0
    matched_house = matched_house or target_house
```

Note: `_MALEFICS` and `_BENEFICS` should be module-level constants, not inline lists.

## Migration Plan

### 9 workaround sites to migrate:

| Rule | Chapter | Current | New Condition |
|------|---------|---------|---------------|
| BPHS1614 | Ch.16 v.20 | modifier: `venus_in_9th_from_jupiter` | `planet_in_house_from(Venus, Jupiter, 9, occupies)` |
| BPHS1616 | Ch.16 v.22 | modifier: `malefic_in_5th_from_jupiter` | `planet_in_house_from(any_malefic, Jupiter, 5, occupies)` |
| BPHS1629 | Ch.16 v.24-32 | modifier: `jupiter_5th_from_saturn_or_vice_versa` | Split into 2 alternative rules (see below) |
| BPHS1630 | Ch.16 v.24-32 | modifier: `saturn_5th_from_jupiter` | `planet_in_house_from(Saturn, Jupiter, 5, occupies)` |
| BPHS1713 | Ch.17 v.20-22 | unencoded (commentary only) | `planet_in_house_from(Moon, Sun, 12, occupies)` |
| BPHS1719 | Ch.17 v.20 | modifier: `saturn_in_8th_from_rahu` | `planet_in_house_from(Saturn, Rahu, 8, occupies)` |
| BPHS1818 | Ch.18 v.27 | 2 modifiers | `planet_in_house_from(Venus, Moon, 7, occupies)` + `planet_in_house_from(Saturn, Venus, 7, occupies)` |
| BPHS1834 | Ch.18 v.40-41 | 2 modifiers | `planet_in_house_from(Moon, Venus, 7, occupies)` + `planet_in_house_from(Mercury, Moon, 7, occupies)` |

### BPHS1629 special case (OR logic):
Split into two rules with `rule_relationship: alternative`:
- Rule A: `planet_in_house_from(Jupiter, Saturn, 5, occupies)`
- Rule B: `planet_in_house_from(Saturn, Jupiter, 5, occupies)`

### Migration safety check:
For each migrated rule, verify whether the planet-relative condition is:
- **Required** (verse says "and") → promote from modifier to condition
- **Optional** (verse says "if also") → keep as condition but review intensity

All 9 current sites are required conditions that were incorrectly encoded as modifiers.

## Test Plan

8 test cases using India 1947 fixture and/or purpose-built charts:

1. **Basic occupancy:** Known planet in computed target house → fires
2. **any_malefic resolution:** Multiple malefics, one in target → fires
3. **lord_of_N reference:** lord_of_5 resolves, offset computed → correct house
4. **offset=1 (same house):** Planet conjunct reference → fires
5. **Missing reference planet:** Reference not in chart → `(False, 0)`
6. **offset=12 (wrap-around):** Boundary arithmetic correct
7. **Multiple candidates, multiple hits:** 2 malefics in target → still fires (ANY)
8. **All candidates exist, none match:** any_benefic, none in target → `(False, 0)`

## Files Changed

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add `"planet_in_house_from"` to `VALID_CONDITION_PRIMITIVES` |
| `src/corpus/v2_builder.py` | Validation block in `_validate_add()` + mapping in `_build_primary_condition()` |
| `src/calculations/rule_firing.py` | Evaluation block + `_MALEFICS`/`_BENEFICS` constants |
| `tests/test_rule_firing.py` | 8 test cases |
| `src/corpus/bphs_v2_ch16.py` | Migrate 4 rules (BPHS1614, 1616, 1629→split, 1630) |
| `src/corpus/bphs_v2_ch17.py` | Migrate 2 rules (BPHS1713, 1719) |
| `src/corpus/bphs_v2_ch18.py` | Migrate 3 rules (BPHS1818, 1834) |

## Post-migration verification

1. Run full test suite (14,480+ tests)
2. Run `condition_modifier_audit.py` — relative-house flags should drop to near zero
3. Run `v2_scorecard.py --v2-only` — no regression in ship-ready count (8/16)
4. Verify no L2 regressions introduced

## Future Extensions (NOT implemented now)

- `mode: "aspects"` — graha drishti / rashi drishti from computed house. Deferred until real use cases emerge.
- `house_from_house` — bhavat-bhavam primitive (e.g., "4th from 9th = 12th"). Related but separate concern.
- Dispositor chains — "dispositor of X in house Y" is a different abstraction, not relative-house.
