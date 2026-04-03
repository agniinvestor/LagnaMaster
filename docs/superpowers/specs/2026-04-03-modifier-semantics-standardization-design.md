# Design Spec: Modifier Semantics Standardization

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Approved
**Scope:** Standardize modifier data model across 496 rules (89 modifiers), in-place migration, no engine execution changes

## Problem

89 modifiers across 16 chapters use 3 effect labels (`conditionalizes: 42`, `amplifies: 37`, `negates: 10`) that conflate different runtime behaviors. "conditionalizes" is used for both gating (rule doesn't apply) and qualification (adds context). "amplifies" is used for both strengthening and outcome-reversal. This ambiguity blocks future inference, aggregation, and scoring.

## Decision

In-place migration to a strict 5-effect taxonomy with enforced effect-target constraints. Data model only — no engine execution changes. Modifiers remain metadata; execution semantics deferred to Track 5 (inference architecture).

## New Modifier Schema

```json
{
  "condition": "string",
  "effect": "gates | amplifies | attenuates | negates | qualifies",
  "target": "rule | prediction",
  "strength": "weak | medium | strong",
  "scope": "local"
}
```

### Effect Definitions

| Effect | Meaning | Test |
|--------|---------|------|
| `gates` | Controls whether the rule applies at all. If gate condition is absent, rule is inapplicable. | "Does the verse say this condition is REQUIRED for the prediction?" |
| `amplifies` | Increases the prediction's magnitude/confidence. Rule fires regardless. | "Does this make the prediction stronger without changing its nature?" |
| `attenuates` | Decreases the prediction's magnitude. Rule fires but weaker. | "Does this weaken the prediction without reversing it?" |
| `negates` | Suppresses or reverses the prediction entirely. | "Does this CANCEL or REVERSE the predicted outcome?" |
| `qualifies` | Changes interpretation context without changing direction or magnitude. | "Does this add a contextual nuance (e.g., 'more daughters than sons') without changing the base prediction?" |

### Gate vs Negate Boundary (Critical Invariant)

> If the condition determines WHETHER the rule applies → `gates` (target: rule)
> If the rule applies regardless but the condition changes the OUTCOME → `negates` (target: prediction)
>
> **Test:** "Does the base prediction still hold without this modifier?"
> - If NO (prediction is invalid without it) → `gates`
> - If YES (prediction holds, modifier changes it) → prediction-level effect

### Effect-Target Constraints (Builder-Enforced)

| Effect | Allowed target | Rationale |
|--------|---------------|-----------|
| `gates` | `rule` only | Gates control applicability, not prediction content |
| `amplifies` | `prediction` only | Strengthening acts on the prediction |
| `attenuates` | `prediction` only | Weakening acts on the prediction |
| `negates` | `prediction` only | Reversal acts on the prediction |
| `qualifies` | `prediction` only | Context change acts on the prediction |

Builder validation rejects any other combination.

### Strength Semantics

| Strength | Interpretation | Future aggregation weight |
|----------|---------------|--------------------------|
| `weak` | Minor influence | Low weight |
| `medium` | Moderate influence | Default weight |
| `strong` | Dominant influence | High weight, may override weaker signals |

### Scope

Always `"local"` for rule-level modifiers. `"global"` reserved for future meta-rules (not implemented).

## Migration Mapping

### Default Mapping (automated)

| Old effect | Default new effect | Default new target |
|---|---|---|
| `conditionalizes` | `gates` | `rule` |
| `amplifies` | `amplifies` | `prediction` |
| `negates` | `negates` | `prediction` |

### Override Rules (manual review required)

Do NOT key off wording — key off semantics.

| If the modifier... | Reclassify to |
|---|---|
| Introduces an ADDITIONAL EFFECT (not requirement) | `qualifies` |
| Weakens rather than strengthens | `attenuates` |
| Flips outcome direction (not just context) | `negates` |
| Adds contextual nuance without changing direction | `qualifies` |
| Was labeled `amplifies` but actually reverses outcome | `negates` |

### Negates vs Qualifies Guard

**Overusing `negates` is the primary misclassification risk.**

Example:
- "gives sons" + "with Venus → more daughters" → this is `qualifies`, NOT `negates` (prediction direction unchanged, interpretation shifts)
- "gives sons" + "with Mars → lose children" → this IS `negates` (prediction direction reversed)

### Strength Migration

| Old strength | New strength |
|---|---|
| `weak` | `weak` |
| `moderate` | `medium` |
| `strong` | `strong` |
| `none` | Remove modifier (was documentation, not a real modifier) |

## Builder Validation

In `v2_builder.py:_validate_add()`, add modifier validation:

```python
VALID_MODIFIER_EFFECTS = frozenset({"gates", "amplifies", "attenuates", "negates", "qualifies"})
VALID_MODIFIER_TARGETS = frozenset({"rule", "prediction"})
VALID_MODIFIER_STRENGTHS = frozenset({"weak", "medium", "strong"})

EFFECT_TARGET_CONSTRAINTS = {
    "gates": "rule",
    "amplifies": "prediction",
    "attenuates": "prediction",
    "negates": "prediction",
    "qualifies": "prediction",
}

for i, mod in enumerate(modifiers):
    effect = mod.get("effect", "")
    if effect not in VALID_MODIFIER_EFFECTS:
        errors.append(f"modifier[{i}].effect='{effect}' not valid")
    target = mod.get("target", "")
    if target not in VALID_MODIFIER_TARGETS:
        errors.append(f"modifier[{i}].target='{target}' not valid")
    if effect in EFFECT_TARGET_CONSTRAINTS and target != EFFECT_TARGET_CONSTRAINTS[effect]:
        errors.append(f"modifier[{i}] effect='{effect}' requires target='{EFFECT_TARGET_CONSTRAINTS[effect]}', got '{target}'")
    strength = mod.get("strength", "")
    if strength not in VALID_MODIFIER_STRENGTHS:
        errors.append(f"modifier[{i}].strength='{strength}' not valid")
    scope = mod.get("scope", "")
    if scope != "local":
        errors.append(f"modifier[{i}].scope='{scope}' must be 'local'")
    if not mod.get("condition"):
        errors.append(f"modifier[{i}] missing 'condition'")
```

## Migration Process

1. Add new constants to `taxonomy.py` (`VALID_MODIFIER_EFFECTS`, etc.)
2. Add validation block to `v2_builder.py`
3. Write migration script (`tools/migrate_modifiers.py`) that:
   - Loads all 89 modifiers
   - Applies default mapping
   - Flags edge cases for manual review
   - Outputs a classification report
4. Manual review of flagged modifiers (~20-30%)
5. Update all 16 chapter files with new modifier schema
6. Update `condition_modifier_audit.py` to validate new schema
7. Run full test suite + audit
8. Verify 0 old-format modifiers remain

## Files Changed

| File | Change |
|------|--------|
| `src/corpus/taxonomy.py` | Add `VALID_MODIFIER_EFFECTS`, `VALID_MODIFIER_TARGETS`, `VALID_MODIFIER_STRENGTHS`, `EFFECT_TARGET_CONSTRAINTS` |
| `src/corpus/v2_builder.py` | Add modifier validation in `_validate_add()` |
| `src/corpus/rule_record.py` | Update modifier type annotation (if typed) |
| `tools/migrate_modifiers.py` | New: migration script with classification report |
| `tools/condition_modifier_audit.py` | Update to validate new modifier schema |
| `src/corpus/bphs_v2_ch*.py` (16 files) | All modifier entries updated to new schema |

## Post-Migration Verification

1. Full test suite (14,497+ tests)
2. `condition_modifier_audit.py` — no old-format modifiers
3. `v2_scorecard.py --v2-only` — no regression (16/16 SHIP)
4. Builder validation — all 89 modifiers pass strict schema check

## Future Extensions (NOT implemented now)

- **Condition structuring:** Replace `"condition": "string"` with structured condition dict (same schema as rule conditions). Deferred until primitives cover all modifier condition types.
- **Engine execution:** Modifiers affecting rule firing. Deferred to Track 5 (inference architecture). Requires aggregation model first.
- **Scope: global:** For meta-rules that apply across all rules (e.g., BPHS2642 dispositor override). Deferred until meta-rule architecture is designed.
