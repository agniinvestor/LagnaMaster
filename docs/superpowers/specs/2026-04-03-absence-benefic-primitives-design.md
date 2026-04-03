# Design Spec: Absence + Benefic Classification Primitives

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Approved
**Scope:** Implement 2 condition primitives, migrate 7 modifier-blocked rules

## Problem

7 rules have conditions encoded as modifiers because no primitive exists for:
1. "No benefic in house X" / "not aspected by benefic" (absence conditions)
2. "Planet is a natural benefic" (benefic classification)

## Primitives

### 1. `planet_not_in_house` — absence of planet category in a house

```json
{
  "type": "planet_not_in_house",
  "planet": "any_benefic",
  "house": 5
}
```

Fires when NO planet matching the spec occupies the target house. Supports `any_benefic`, `any_malefic`, and specific planet names.

### 2. `planet_not_aspecting` — already whitelisted, needs engine implementation

```json
{
  "type": "planet_not_aspecting",
  "planet": "any_benefic",
  "house": 5
}
```

Fires when NO planet matching the spec aspects the target house.

Note: `planet_is_benefic` is NOT a separate primitive. "Lord is benefic" is chart-dependent (depends on which planet rules the house for this lagna). For the 4 benefic-check modifiers, we keep them as modifiers — they require functional benefic logic that depends on lagna, which is Track 7 scope.

## Blocked Rules

| Rule | Current modifier | New condition | Primitive |
|------|-----------------|---------------|-----------|
| BPHS1622 | `no_benefic_in_5th` (gates) | `planet_not_in_house(any_benefic, 5)` | planet_not_in_house |
| BPHS2306 | `not_aspected_by_benefic` (attenuates) | `planet_not_aspecting(any_benefic, 12)` | planet_not_aspecting |
| BPHS2415 | `no_benefic_aspect_or_conjunction` (attenuates) | `planet_not_in_house(any_benefic, 12)` + `planet_not_aspecting(any_benefic, 12)` | both |

The 4 benefic-check modifiers (BPHS1503, 1508, 2408, 2623) stay as modifiers — they require functional benefic classification per lagna.

## Engine Evaluation

### planet_not_in_house

```python
elif ctype == "planet_not_in_house":
    planet_spec = cond.get("planet", "")
    target_house = cond.get("house", 0)
    if planet_spec == "any_benefic":
        candidates = list(_BENEFICS)
    elif planet_spec == "any_malefic":
        candidates = list(_MALEFICS)
    else:
        candidates = [planet_spec.strip().title()]
    valid = [c for c in candidates if _find_planet(chart, c)]
    if any(_planet_house(chart, c) == target_house for c in valid):
        return False, 0  # planet IS there → absence condition fails
    matched_house = matched_house or target_house
```

### planet_not_aspecting

```python
elif ctype == "planet_not_aspecting":
    planet_spec = cond.get("planet", "")
    target_house = cond.get("house", 0)
    if planet_spec == "any_benefic":
        candidates = list(_BENEFICS)
    elif planet_spec == "any_malefic":
        candidates = list(_MALEFICS)
    else:
        candidates = [planet_spec.strip().title()]
    valid = [c for c in candidates if _find_planet(chart, c)]
    if any(_planet_aspects_house(chart, c, target_house) for c in valid):
        return False, 0  # planet DOES aspect → absence condition fails
    matched_house = matched_house or target_house
```

## Builder Validation

Both primitives require: `planet` (string) + `house` (int 1-12).

## Files Changed

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add `planet_not_in_house` to VALID_CONDITION_PRIMITIVES |
| `src/corpus/v2_builder.py` | Add validation for `planet_not_in_house` |
| `src/calculations/rule_firing.py` | Add engine evaluation for both primitives |
| `src/corpus/bphs_v2_ch16.py` | Migrate BPHS1622 |
| `src/corpus/bphs_v2_ch23.py` | Migrate BPHS2306 |
| `src/corpus/bphs_v2_ch24a.py` | Migrate BPHS2415 |
| `tests/test_rule_firing.py` | Add tests |
