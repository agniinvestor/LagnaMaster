# Modifier Semantics Standardization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate 89 modifiers across 16 chapters from 3 ambiguous effect labels to a strict 5-effect taxonomy with enforced effect-target constraints.

**Architecture:** Add new modifier constants to taxonomy → update builder validation to enforce new schema → write migration script that classifies all 89 modifiers → apply migration to all chapter files → update audit tool → verify.

**Tech Stack:** Python 3.14, pytest (existing)

**Spec:** `docs/superpowers/specs/2026-04-03-modifier-semantics-standardization-design.md`

---

### Task 1: Add modifier constants to taxonomy

**Files:**
- Modify: `src/corpus/taxonomy.py`

- [ ] **Step 1: Add constants after VALID_CONDITION_PRIMITIVES block**

```python
VALID_MODIFIER_EFFECTS = frozenset({
    "gates", "amplifies", "attenuates", "negates", "qualifies",
})

VALID_MODIFIER_TARGETS = frozenset({"rule", "prediction"})

VALID_MODIFIER_STRENGTHS = frozenset({"weak", "medium", "strong"})

EFFECT_TARGET_CONSTRAINTS: dict[str, str] = {
    "gates": "rule",
    "amplifies": "prediction",
    "attenuates": "prediction",
    "negates": "prediction",
    "qualifies": "prediction",
}
```

- [ ] **Step 2: Verify import**

Run: `PYTHONPATH=. .venv/bin/python -c "from src.corpus.taxonomy import VALID_MODIFIER_EFFECTS, EFFECT_TARGET_CONSTRAINTS; print('OK')"`

- [ ] **Step 3: Commit**

```bash
git add src/corpus/taxonomy.py
git commit -m "feat: add modifier taxonomy constants (5-effect system)"
```

---

### Task 2: Update builder validation

**Files:**
- Modify: `src/corpus/v2_builder.py:624-642`

- [ ] **Step 1: Replace existing T1-18 modifier validation block**

Find the block starting with `# T1-18: Modifier quality` (around line 624). Replace it entirely with:

```python
        # T1-18: Modifier semantic validation (strict 5-effect schema)
        from src.corpus.taxonomy import (
            VALID_MODIFIER_EFFECTS, VALID_MODIFIER_TARGETS,
            VALID_MODIFIER_STRENGTHS, EFFECT_TARGET_CONSTRAINTS,
        )
        if modifiers is None:
            modifiers = []
        for i, mod in enumerate(modifiers):
            if not isinstance(mod, dict):
                continue
            # Required fields
            cond = mod.get("condition", "")
            if not cond:
                errors.append(f"T1-18: modifiers[{i}] missing 'condition'")
            effect = mod.get("effect", "")
            if effect not in VALID_MODIFIER_EFFECTS:
                errors.append(
                    f"T1-18: modifiers[{i}].effect='{effect}' not valid — "
                    f"use: {sorted(VALID_MODIFIER_EFFECTS)}"
                )
            target = mod.get("target", "")
            if target not in VALID_MODIFIER_TARGETS:
                errors.append(
                    f"T1-18: modifiers[{i}].target='{target}' not valid — "
                    f"use: {sorted(VALID_MODIFIER_TARGETS)}"
                )
            # Effect-target constraint
            if effect in EFFECT_TARGET_CONSTRAINTS:
                expected_target = EFFECT_TARGET_CONSTRAINTS[effect]
                if target and target != expected_target:
                    errors.append(
                        f"T1-18: modifiers[{i}] effect='{effect}' requires "
                        f"target='{expected_target}', got '{target}'"
                    )
            strength = mod.get("strength", "")
            if strength not in VALID_MODIFIER_STRENGTHS:
                errors.append(
                    f"T1-18: modifiers[{i}].strength='{strength}' not valid — "
                    f"use: {sorted(VALID_MODIFIER_STRENGTHS)}"
                )
            scope = mod.get("scope", "")
            if scope != "local":
                errors.append(
                    f"T1-18: modifiers[{i}].scope='{scope}' must be 'local'"
                )
```

- [ ] **Step 2: Test that old-format modifiers now FAIL validation**

Run: `PYTHONPATH=. .venv/bin/python -c "
from src.corpus.v2_builder import V2ChapterBuilder
b = V2ChapterBuilder(chapter='Test', category='test', id_start=9900, session='TEST', sloka_count=1, entity_target='native')
try:
    b.add(
        conditions=[{'type': 'planet_in_house', 'planet': 'Sun', 'house': 1}],
        signal_group='test_old_modifier', direction='favorable', intensity='moderate', domains=['wealth'],
        predictions=[{'entity': 'native', 'claim': 'test_old_format_modifier', 'domain': 'wealth', 'direction': 'favorable', 'magnitude': 0.5}],
        verse_ref='Test v.1', description='Test old modifier format', commentary_context='Test context',
        modifiers=[{'condition': 'old_format_modifier', 'effect': 'conditionalizes', 'strength': 'moderate'}]
    )
    print('ERROR: old format should fail')
except ValueError as e:
    print(f'Correctly rejected: old format')
"`

Expected: `Correctly rejected: old format` (because `conditionalizes` is no longer valid, and `target`/`scope` are missing)

- [ ] **Step 3: Test that new-format modifiers PASS validation**

Run: `PYTHONPATH=. .venv/bin/python -c "
from src.corpus.v2_builder import V2ChapterBuilder
b = V2ChapterBuilder(chapter='Test', category='test', id_start=9900, session='TEST', sloka_count=1, entity_target='native')
b.add(
    conditions=[{'type': 'planet_in_house', 'planet': 'Sun', 'house': 1}],
    signal_group='test_new_modifier', direction='favorable', intensity='moderate', domains=['wealth'],
    predictions=[{'entity': 'native', 'claim': 'test_new_format_modifier', 'domain': 'wealth', 'direction': 'favorable', 'magnitude': 0.5}],
    verse_ref='Test v.1', description='Test new modifier format', commentary_context='Test context',
    modifiers=[{'condition': 'jupiter_aspecting_lagna', 'effect': 'amplifies', 'target': 'prediction', 'strength': 'medium', 'scope': 'local'}]
)
print('Validation passed')
"`

Expected: `Validation passed`

- [ ] **Step 4: Commit**

```bash
git add src/corpus/v2_builder.py
git commit -m "feat: strict modifier validation (5-effect schema with target constraints)"
```

---

### Task 3: Write migration script

**Files:**
- Create: `tools/migrate_modifiers.py`

- [ ] **Step 1: Create the migration script**

```python
"""tools/migrate_modifiers.py — Classify and migrate modifiers to new 5-effect schema.

Usage:
    PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --report    # classification report only
    PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --apply     # apply migration in-place
"""
from __future__ import annotations
import argparse
import importlib
import json
import sys

# Default mapping: old effect → new effect + target
_DEFAULT_MAP = {
    "conditionalizes": ("gates", "rule"),
    "amplifies": ("amplifies", "prediction"),
    "negates": ("negates", "prediction"),
}

# Manual overrides: rule_id → modifier_index → (new_effect, new_target)
# These are modifiers that don't follow the default mapping.
# Populated after running --report and reviewing edge cases.
_MANUAL_OVERRIDES: dict[tuple[str, int], tuple[str, str]] = {
    # Example: ("BPHS1469", 0): ("qualifies", "prediction"),
}

# Strength normalization
_STRENGTH_MAP = {"weak": "weak", "moderate": "medium", "strong": "strong", "none": None}


def _load_all_modifiers():
    """Load all modifiers from all V2 chapter registries."""
    results = []
    chapters = [
        "12", "13", "14", "15", "16", "17", "18", "19",
        "20", "21", "22", "23", "24a", "24b", "24c", "25",
    ]
    for ch in chapters:
        mod = importlib.import_module(f"src.corpus.bphs_v2_ch{ch}")
        for attr in dir(mod):
            if "REGISTRY" in attr:
                reg = getattr(mod, attr)
                for r in reg.all():
                    for i, m in enumerate(r.modifiers or []):
                        results.append({
                            "rule_id": r.rule_id,
                            "chapter": ch,
                            "modifier_index": i,
                            "old": m,
                        })
    return results


def classify(rule_id: str, idx: int, old_mod: dict) -> dict:
    """Classify a single modifier into the new schema."""
    # Check manual override first
    key = (rule_id, idx)
    if key in _MANUAL_OVERRIDES:
        new_effect, new_target = _MANUAL_OVERRIDES[key]
    else:
        old_effect = old_mod.get("effect", "")
        new_effect, new_target = _DEFAULT_MAP.get(old_effect, ("qualifies", "prediction"))

    old_strength = old_mod.get("strength", "moderate")
    new_strength = _STRENGTH_MAP.get(old_strength)

    if new_strength is None:
        return None  # strength=none → remove modifier

    return {
        "condition": old_mod.get("condition", ""),
        "effect": new_effect,
        "target": new_target,
        "strength": new_strength,
        "scope": "local",
    }


def report(all_mods):
    """Print classification report for review."""
    by_effect = {"gates": [], "amplifies": [], "attenuates": [], "negates": [], "qualifies": [], "REMOVED": []}
    for entry in all_mods:
        new = classify(entry["rule_id"], entry["modifier_index"], entry["old"])
        if new is None:
            by_effect["REMOVED"].append(entry)
        else:
            by_effect[new["effect"]].append((entry, new))

    for effect, items in by_effect.items():
        print(f"\n=== {effect} ({len(items)}) ===")
        if effect == "REMOVED":
            for entry in items:
                print(f"  {entry['rule_id']}[{entry['modifier_index']}]: {entry['old']['condition']}")
        else:
            for entry, new in items:
                old_eff = entry["old"]["effect"]
                changed = " ← CHANGED" if old_eff != effect and not (old_eff == "conditionalizes" and effect == "gates") else ""
                print(f"  {entry['rule_id']}[{entry['modifier_index']}]: {new['condition'][:60]}{changed}")

    total = sum(len(v) for v in by_effect.values())
    print(f"\nTotal: {total} modifiers classified")
    print(f"  gates: {len(by_effect['gates'])}")
    print(f"  amplifies: {len(by_effect['amplifies'])}")
    print(f"  attenuates: {len(by_effect['attenuates'])}")
    print(f"  negates: {len(by_effect['negates'])}")
    print(f"  qualifies: {len(by_effect['qualifies'])}")
    print(f"  REMOVED: {len(by_effect['REMOVED'])}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true", help="Print classification report")
    parser.add_argument("--apply", action="store_true", help="Apply migration (NOT YET IMPLEMENTED)")
    args = parser.parse_args()

    all_mods = _load_all_modifiers()
    print(f"Loaded {len(all_mods)} modifiers from 16 chapters")

    if args.report:
        report(all_mods)
    elif args.apply:
        print("--apply not yet implemented. Use --report first, review, then implement.")
        sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the report**

Run: `PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --report`

Review the output. Identify modifiers that need manual override (where default mapping is wrong).

- [ ] **Step 3: Commit**

```bash
git add tools/migrate_modifiers.py
git commit -m "feat: modifier migration script with classification report"
```

---

### Task 4: Manual classification review

**Files:**
- Modify: `tools/migrate_modifiers.py` (add manual overrides)

- [ ] **Step 1: Review the --report output using the classification checklist**

For each modifier, apply:
1. Remove modifier mentally → does rule still make sense? No → `gates`. Yes → continue.
2. Changes magnitude? Yes stronger → `amplifies`. Yes weaker → `attenuates`. No → continue.
3. Changes type/nature of outcome? Yes → `qualifies`. No → continue.
4. Cancels/replaces outcome? Yes → `negates`. No → re-examine.

Focus on modifiers where the default mapping is wrong:
- `conditionalizes` that should be `qualifies` (adds effect, not requirement)
- `amplifies` that should be `negates` (reverses outcome)
- `amplifies` that should be `attenuates` (weakens)
- `amplifies` that should be `qualifies` (changes nature)

- [ ] **Step 2: Add manual overrides to `_MANUAL_OVERRIDES` dict**

For each misclassified modifier, add an entry:
```python
("BPHS_XXXX", modifier_index): ("correct_effect", "correct_target"),
```

- [ ] **Step 3: Re-run report and verify all classifications look correct**

Run: `PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --report`

- [ ] **Step 4: Commit**

```bash
git add tools/migrate_modifiers.py
git commit -m "fix: manual classification overrides for modifier migration"
```

---

### Task 5: Migrate all chapter files

**Files:**
- Modify: All 16 `src/corpus/bphs_v2_ch*.py` files

- [ ] **Step 1: For each chapter file, update every modifier entry to new schema**

For each modifier in each chapter file, replace:
```python
{"condition": "...", "effect": "conditionalizes", "strength": "moderate"}
```
with:
```python
{"condition": "...", "effect": "gates", "target": "rule", "strength": "medium", "scope": "local"}
```

Use the migration script's classification output as the source of truth. Apply manual overrides where flagged.

Key transformations:
- `"conditionalizes"` → `"gates"` (most cases) or `"qualifies"` (if override)
- `"amplifies"` → `"amplifies"` (most cases) or `"negates"`/`"attenuates"`/`"qualifies"` (if override)
- `"negates"` → `"negates"` (stays)
- `"moderate"` → `"medium"` (all cases)
- Add `"target":` field to every modifier
- Add `"scope": "local"` to every modifier

- [ ] **Step 2: Verify each chapter builds without validation errors**

Run for each chapter:
```bash
PYTHONPATH=. .venv/bin/python -c "from src.corpus.bphs_v2_ch12 import BPHS_V2_CH12_REGISTRY; print('Ch.12 OK')"
```
(Repeat for all 16 chapters)

- [ ] **Step 3: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`

Expected: 14,497+ passed, 0 failed

- [ ] **Step 4: Verify no old-format modifiers remain**

Run: `PYTHONPATH=. .venv/bin/python -c "
import importlib
old_format = 0
for ch in ['12','13','14','15','16','17','18','19','20','21','22','23','24a','24b','24c','25']:
    mod = importlib.import_module(f'src.corpus.bphs_v2_ch{ch}')
    for attr in dir(mod):
        if 'REGISTRY' in attr:
            reg = getattr(mod, attr)
            for r in reg.all():
                for m in (r.modifiers or []):
                    if m.get('effect') in ('conditionalizes', 'amplifies_old') or 'target' not in m:
                        old_format += 1
                        print(f'  OLD: {r.rule_id} {m}')
print(f'Old format remaining: {old_format}')
"`

Expected: `Old format remaining: 0`

- [ ] **Step 5: Commit**

```bash
git add src/corpus/bphs_v2_ch*.py
git commit -m "feat: migrate all 89 modifiers to 5-effect schema

gates: N, amplifies: N, attenuates: N, negates: N, qualifies: N
All modifiers now have: effect, target, strength, scope, condition
No old-format modifiers remain"
```

---

### Task 6: Update audit tool

**Files:**
- Modify: `tools/condition_modifier_audit.py`

- [ ] **Step 1: Update the audit tool to validate new modifier schema**

Find the section that checks modifier effects and update it to validate against the new taxonomy. Add checks for:
- `effect` in `VALID_MODIFIER_EFFECTS`
- `target` present and matches `EFFECT_TARGET_CONSTRAINTS[effect]`
- `strength` in `VALID_MODIFIER_STRENGTHS`
- `scope` == `"local"`

Remove or update any checks that reference old effect names (`conditionalizes`).

- [ ] **Step 2: Run the audit**

Run: `PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py 2>&1 | head -30`

Verify no old-format errors appear.

- [ ] **Step 3: Commit**

```bash
git add tools/condition_modifier_audit.py
git commit -m "fix: update audit tool for new modifier schema"
```

---

### Task 7: Post-migration verification

**Files:** none (verification only)

- [ ] **Step 1: Full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: 14,497+ passed

- [ ] **Step 2: Scorecard — no regression**

Run: `PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only 2>&1 | grep "Ship-ready"`
Expected: `Ship-ready: 16/16 chapters`

- [ ] **Step 3: Audit — modifier flags resolved**

Run: `PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py 2>&1 | grep -c "high"` 
Expected: 0

- [ ] **Step 4: Classification summary**

Run: `PYTHONPATH=. .venv/bin/python tools/migrate_modifiers.py --report 2>&1 | tail -10`

Print final distribution for commit message.
