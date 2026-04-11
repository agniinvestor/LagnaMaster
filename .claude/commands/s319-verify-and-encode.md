# S319 Verify + or_group Fix + Encode Missing Chapter Content

Three-phase session: verify S319 fixes, close one governance gap, then encode ~40 missing rules.

## Session type

**Mixed (governance + encoding)** — Phase 1-2 are governance (~20 min), Phase 3 is encoding (~80% of session).

## Pre-flight

Read these first:
1. `lessons_learned.md`
2. `core_principles.md`
3. `docs/RULE_CONTRACT_V2.md`
4. `docs/ENCODING_GRANULARITY.md`
5. `tools/INDEX.md`

Baseline:
```
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```

---

## Phase 1: Spot-check S319 Bug Fixes (~15 min)

Verify the 5 parallel agents from S319 got their fixes right. Read the BPHS PDF
at the cited page, then read the rule in the corpus file. Confirm the condition
matches the verse.

### Priority checks (do ALL of these):

**1. BUG-089 Fix 9 — BPHS1402 (KNOWN ISSUE)**
- File: `src/corpus/bphs_v2_ch14.py`, line ~77
- Read BPHS PDF p.138, Ch.14 v.3
- Current code uses `sign_type: "malefic_ruled"` inside an `or_group`
- Problem: `"malefic_ruled"` is NOT in `VALID_SIGN_TYPES` (valid values: movable, fixed, dual, fire, earth, air, water, odd, even)
- The builder doesn't validate inside `or_group`, so this passes silently
- **FIX:** Determine from the verse what "malefic sign" actually means:
  - If it means signs ruled by malefics (Mars, Saturn, Sun, Rahu) → there's no single sign_type for this. Either add "malefic_ruled" to VALID_SIGN_TYPES in taxonomy.py and implement it in rule_firing.py, OR replace with the more precise condition. Read the verse to decide.
  - Alternative: use `planet_in_sign` with explicit sign list for malefic-ruled signs (Aries, Scorpio, Capricorn, Aquarius, Leo)
  - Whatever you choose, ensure rule_firing.py can actually evaluate it

**2. BUG-093 — Marriage Timing Ch.18 v.22-34 (MOST COMPLEX)**
- File: `src/corpus/bphs_v2_ch18.py`
- Read BPHS PDF pp.165-168
- Pick 3 of the 10 modified rules and verify:
  - v.22 (added Venus dignity condition)
  - v.26 (added Saturn in 7th from Venus)
  - v.32 (added Venus in Navamsa ascendant)
- For each: does the added condition match what the verse says?
- If any condition is wrong, fix it surgically

**3. BUG-091 — BPHS1600 (MOST STRUCTURAL)**
- File: `src/corpus/bphs_v2_ch16.py`, line ~21
- Read BPHS PDF p.145, Ch.16 v.1-3
- The fix added two or_groups (lord_of_1 and lord_of_5), each requiring own sign OR kendra OR trikona
- Verify: does the verse really say BOTH lords must satisfy the condition? Or just one?
- Verify: the or_group alternatives match the verse phrasing

### Report format for each check:
```
RULE: BPHS1402
VERSE: Ch.14 v.3, p.138
PDF SAYS: [quote or paraphrase]
CODE HAS: [condition as encoded]
VERDICT: CORRECT / WRONG — [explanation if wrong]
FIX: [if needed]
```

---

## Phase 2: Fix or_group Validation Gap (~15 min)

### The problem
`src/corpus/v2_builder.py` `_validate_add()` iterates `conditions` and validates
each by type (T1-1). But `or_group` conditions contain nested sub-conditions that
are NOT validated. Any invalid primitive, missing field, or bad sign_type inside
an `or_group` passes silently.

### Current state
- `or_group` is in `VALID_CONDITION_PRIMITIVES` (taxonomy.py line 74)
- `_validate_add()` checks `cond.get("type")` against the whitelist (line 474-479)
- But when type == "or_group", it does NOT recurse into `cond["conditions"]`
- grep confirms: zero mentions of "or_group" in v2_builder.py

### The fix
In `src/corpus/v2_builder.py`, `_validate_add()` method, after the condition
primitive whitelist check (line ~476), add recursion for or_group:

```python
# Inside the for loop over conditions:
if ctype == "or_group":
    sub_conditions = cond.get("conditions", [])
    if not sub_conditions:
        errors.append(
            f"T1-1: conditions[{i}] or_group has empty 'conditions' list"
        )
    for j, sub_cond in enumerate(sub_conditions):
        sub_type = sub_cond.get("type", "")
        if sub_type and sub_type not in VALID_CONDITION_PRIMITIVES:
            errors.append(
                f"T1-1: conditions[{i}].or_group[{j}].type='{sub_type}' "
                f"not a valid primitive — use: {sorted(VALID_CONDITION_PRIMITIVES)}"
            )
        # Recurse into sub-field validation (sign_type, planet, etc.)
        # Reuse the same validation logic from the elif blocks below
```

The tricky part: the existing sub-field validation (planet_in_sign_type, planet_in_derived_house,
etc.) is in elif blocks below. You need to either:
- Extract the per-type validation into a helper method and call it for both top-level and or_group sub-conditions
- Or duplicate the validation inline (less clean but functional)

Prefer the helper method approach.

### After fixing:
1. Run `.venv/bin/pytest tests/ -q --tb=short -x` — some corpus tests may now FAIL because existing or_group sub-conditions have invalid fields (like malefic_ruled). Fix those too.
2. Run `.venv/bin/ruff check src/ tests/`
3. Commit: `fix(S319): or_group validation — recurse into sub-conditions for T1-1 gate`

### Then fix any corpus rules that the new validation catches
The known one is BPHS1402 with `malefic_ruled` — fix per Phase 1 findings.

---

## Phase 3: Encode Missing Chapter Content (~remaining session time)

The S318 deep audit (`docs/s318_deep_audit.md` lines 1203-1222) identified specific
gaps per chapter. Ch.19 gaps were already filled in S318. The remaining gaps:

| Chapter | Gaps | What's Missing | Priority |
|---------|------|----------------|----------|
| Ch.17 | 8 | v.9-12: only Sun has disease rule, need 6 more planets | HIGH — most rules |
| Ch.14 | 10 | male planet variants, sign-gender logic, multi-planet combos | HIGH |
| Ch.18 | 7 | v.7-8 planet-type block, v.9 appearance variants | MEDIUM |
| Ch.13 | 5 | v.5 relative positioning, v.6-7 11th lord conditions | MEDIUM |
| Ch.12 | 4 | v.3 ascendant branch, v.5-7 Mercury/Venus paths | MEDIUM |
| Ch.16 | 3 | v.11 under-encoded, v.29-31 counts | LOW |
| Ch.15 | 2 | minor gaps | LOW |
| Ch.23 | 2 | minor gaps | LOW |

### Encoding approach

Use **parallel agents** (3-4 at a time, worktree-isolated) to encode chapter gaps.
Group by chapter file to avoid merge conflicts:

**Batch 1 (parallel):**
- Agent A: Ch.17 gaps (8 rules) — v.9-12 disease rules for Moon, Mars, Mercury, Jupiter, Venus, Saturn
- Agent B: Ch.14 gaps (10 rules) — male planet variants, sign-gender conditions
- Agent C: Ch.13 gaps (5 rules) + Ch.12 gaps (4 rules) — same agent since both small

**Batch 2 (parallel, after Batch 1 merges):**
- Agent D: Ch.18 gaps (7 rules) — planet-type block, appearance variants
- Agent E: Ch.16 gaps (3 rules) + Ch.15 gaps (2 rules) + Ch.23 gaps (2 rules)

### Per-agent instructions (include in each agent prompt):

Each agent MUST:
1. Read the BPHS PDF at the cited pages
2. Read the existing chapter file to understand the pattern
3. Read `docs/ENCODING_GRANULARITY.md` for granularity rules
4. Create a mini verse audit (list claims per verse) BEFORE encoding
5. Encode using `b.add()` following the existing chapter's pattern
6. Run `.venv/bin/pytest tests/ -q --tb=short -x`
7. Run `.venv/bin/ruff check src/ tests/`
8. Commit with: `feat(S319): encode Ch.N gaps — [description]`

Each agent must NOT:
- Touch rules that already exist (only ADD new rules)
- Modify scoring weights or multi_axis_scoring.py
- Create new tools or infrastructure
- Skip PDF verification

### After all agents complete:
1. Cherry-pick commits onto main
2. Run full test suite + ruff + scorecard
3. Update docs (MEMORY.md, CHANGELOG.md, SESSION_LOG.md)
4. Report: rules added per chapter, total corpus rule count, gap closure percentage

---

## Success criteria

- [ ] Phase 1: 3+ rules spot-checked against PDF, all verdicts documented
- [ ] Phase 1: BPHS1402 malefic_ruled issue resolved
- [ ] Phase 2: or_group validation added to v2_builder.py
- [ ] Phase 2: All existing or_group rules pass the new validation
- [ ] Phase 3: 30+ new rules encoded from gap inventory
- [ ] All tests pass, ruff clean, scorecard no new warnings
- [ ] Docs updated

## Non-negotiable

1. Read the BPHS PDF verse BEFORE encoding any rule
2. Do NOT change existing rules (except Phase 1 fixes)
3. Do NOT modify scoring weights
4. Run tests AFTER each phase, not just at the end
5. When the verse is ambiguous, note it in commentary_context and move on
