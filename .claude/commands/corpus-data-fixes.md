# Corpus Data Fixes: BUG-089 through BUG-093

Fix the 5 remaining corpus data bugs from the S318 deep audit. These are all
in V2 corpus files under `src/corpus/bphs_v2_ch*.py`. Each fix requires reading
the BPHS PDF verse, comparing against the encoded rule, and correcting the
condition/structure.

Source audit: `docs/s318_deep_audit.md` lines 1168-1201.
PDF: `BPHS-Santhanam-Vol-1.pdf`

## Session type

**Encoding session** — no new tools, no framework debates, no lessons updates.
Use existing infrastructure only.

## Pre-flight

Read these files first (do NOT skip):
1. `lessons_learned.md`
2. `core_principles.md`
3. `docs/RULE_CONTRACT_V2.md`
4. `docs/ENCODING_GRANULARITY.md`

Verify baseline:
```
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```

---

## Workstream layout (5 independent workstreams)

Dispatch 5 parallel agents using the Agent tool with `isolation: "worktree"`.
Each agent handles one bug. All are independent — no shared files between bugs.

---

### Agent 1: BUG-089 — 10 Factual Errors (surgical edits)

```
prompt: |
  You are fixing 10 factual errors in V2 corpus rules. Each fix is a single
  condition value change (wrong house number, wrong planet, wrong condition type).

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  PDF: BPHS-Santhanam-Vol-1.pdf

  For EACH fix below:
  1. Read the BPHS PDF at the cited page to verify the correct value
  2. Read the corpus file to find the rule
  3. grep for the rule_id to check for callers/tests
  4. Make the surgical edit
  5. Run tests after each edit

  THE 10 FIXES (from docs/s318_deep_audit.md lines 1190-1201):

  1. BPHS1506 (src/corpus/bphs_v2_ch15.py)
     Ch.15 v.8, p.144: Saturn should be in house 9 (with Moon), NOT house 11.
     Fix: change "house": 11 → "house": 9

  2. BPHS1700 (src/corpus/bphs_v2_ch17.py)
     Ch.17 v.2, p.152: 6th lord should be in [1, 6, 8], NOT [1, 8].
     Fix: add 6 to the house list

  3. BPHS1715 (src/corpus/bphs_v2_ch17.py)
     Ch.17 v.22b, p.157: lord_of_8 should be in [2, 4, 5, 11, 12], NOT [1, 4, 5, 7, 9, 10].
     Fix: replace the entire house list

  4. BPHS2011 (src/corpus/bphs_v2_ch20.py)
     Ch.20 v.15, p.175: lord_of_1 should be in house 8, NOT house 2.
     Fix: change "house": 2 → "house": 8

  5. BPHS2021 (src/corpus/bphs_v2_ch20.py)
     Ch.20 v.30, p.176: Rahu should be in house 5 (9th from 9th), NOT house 9.
     Fix: change "house": 9 → "house": 5

  6. BPHS2029 (src/corpus/bphs_v2_ch20.py)
     Ch.20 v.29, p.176: Should be lord_of_1 in house 9 + lord_of_9 in house 1
     (exchange), NOT both lords in own houses. Read the verse to confirm the
     exchange direction. Fix the conditions to reflect a parivartana or
     mutual placement: lord_of_1 in 9 AND lord_of_9 in 1.

  7. BPHS2110 (src/corpus/bphs_v2_ch21.py)
     Ch.21 v.12, p.180: Jupiter should be in SIGN Pisces (sign index 11),
     NOT in house 12. Fix: change condition type from planet_in_house to
     planet_in_sign with sign index for Pisces.

  8. BPHS2303 (src/corpus/bphs_v2_ch23.py)
     Ch.23 v.10, p.188: Should be "12th LORD exalted," NOT "any benefic exalted."
     Fix: change condition to planet_dignity for lord_of_12, dignity=exalted.

  9. BPHS1402 (src/corpus/bphs_v2_ch14.py)
     Ch.14 v.3, p.138: Condition should be "with malefic or in malefic sign,"
     NOT dignity="weak". Read the verse. Fix: replace the dignity condition
     with an or_group containing planets_conjunct with any_malefic OR
     planet_in_sign_type with sign_type appropriate for malefic signs.
     If or_group is complex, use the simpler condition that best captures
     the verse and note the alternative in commentary_context.

  10. BPHS1407 (src/corpus/bphs_v2_ch14.py)
      Ch.14 v.7-11, p.139: Subject should be MARS exalted in trine, NOT
      lord_of_3 exalted. Fix: change "planet": "lord_of_3" to "planet": "Mars".

  IMPORTANT:
  - Read the PDF page for EACH fix to verify before editing
  - Do NOT change any field except the one that is wrong
  - Run .venv/bin/pytest tests/ -q --tb=short -x after all fixes
  - Run .venv/bin/ruff check src/ tests/

  Commit: fix(S319): BUG-089 — correct 10 factual errors in V2 corpus per BPHS PDF
```

---

### Agent 2: BUG-090 — Aspect vs Occupation Confusion (~4 rules need aspect variant)

```
prompt: |
  You are fixing the "aspect vs occupation confusion" pattern in the V2 corpus.
  Multiple rules encode planet_in_house when BPHS says "conjunct OR aspected by."
  Only the occupation path is encoded; the aspect path is missing.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  PDF: BPHS-Santhanam-Vol-1.pdf

  AFFECTED RULES (from docs/s318_deep_audit.md line 1171-1172):
  - Ch.14 v.1 (p.137) — find the rule in src/corpus/bphs_v2_ch14.py
  - Ch.15 v.2 (p.142) — find the rule in src/corpus/bphs_v2_ch15.py
  - Ch.15 v.12 (p.144) — only 1 of 3 alternatives encoded
  - Ch.18 v.3 (p.160) — find the rule in src/corpus/bphs_v2_ch18.py

  FOR EACH affected rule:
  1. Read the BPHS PDF at the cited page
  2. Read the corpus file and find the rule by verse_ref
  3. Confirm the verse says "conjunct OR aspected by" (or similar phrasing)
  4. The EXISTING rule encodes the occupation/conjunction path — KEEP IT
  5. ADD A NEW RULE (aspect variant) using the same signal_group but with
     a planet_aspecting condition instead of planet_in_house
  6. Link the two rules with rule_relationship: {"type": "alternative"}
  7. The new rule should have all the same fields as the original except
     the condition and rule_id

  Use the V2ChapterBuilder — find where each chapter's b.add() calls are and
  add the new rule immediately after the existing one.

  The valid condition primitive for aspects is:
    {"type": "planet_aspecting", "planet": "...", "house": N}

  IMPORTANT:
  - Read the verse BEFORE adding any rule — confirm it really says "or aspected"
  - If the verse does NOT say "or aspected," do NOT add a rule — note it and move on
  - Some verses may say "conjunct" only (no aspect) — skip those
  - After all additions: .venv/bin/pytest tests/ -q --tb=short -x
  - Run .venv/bin/ruff check src/ tests/

  Commit: fix(S319): BUG-090 — add aspect-path variants where BPHS says "or aspected"
```

---

### Agent 3: BUG-091 — OR-vs-AND Logic Errors (3 rules)

```
prompt: |
  You are fixing 3 rules where alternative conditions (OR) are encoded as
  conjunctive (AND). BPHS says "condition A OR condition B" but the code
  requires both simultaneously.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  PDF: BPHS-Santhanam-Vol-1.pdf

  AFFECTED RULES (from docs/s318_deep_audit.md lines 1174-1176):
  1. BPHS1501 — Ch.15 v.3 (src/corpus/bphs_v2_ch15.py, p.142)
  2. BPHS1611 — Ch.16 v.16 (src/corpus/bphs_v2_ch16.py, p.148)
  3. BPHS1600 — Ch.16 v.1-3 (src/corpus/bphs_v2_ch16.py, p.145)

  FOR EACH rule:
  1. Read the BPHS PDF at the cited page
  2. Read the corpus file and find the rule
  3. Confirm the verse uses OR logic ("either...or", "condition A or condition B")
  4. The FIX depends on what the V2 condition DSL supports:

  OPTION A (preferred if conditions DSL supports or_group):
    Use the "or_group" condition primitive to wrap the alternatives:
    {"type": "or_group", "conditions": [
        {"type": "...", ...},  // condition A
        {"type": "...", ...},  // condition B
    ]}

  OPTION B (if or_group doesn't work cleanly):
    Split into 2 separate rules — one per alternative condition.
    Both share the same signal_group, predictions, and commentary.
    Link them with rule_relationship: {"type": "alternative"}.

  Check which approach the existing codebase uses by grepping:
    grep -r "or_group" src/corpus/  — if used elsewhere, use it here
    If not used, use Option B (split into separate rules)

  IMPORTANT:
  - Read the verse to confirm it's truly OR, not AND
  - If the verse is ambiguous, add a note in commentary_context and keep AND
  - After all fixes: .venv/bin/pytest tests/ -q --tb=short -x
  - Run .venv/bin/ruff check src/ tests/

  Commit: fix(S319): BUG-091 — correct AND→OR logic for 3 rules per BPHS text
```

---

### Agent 4: BUG-092 — Relative→Absolute House Positions (2 rules)

```
prompt: |
  You are fixing 2 rules where BPHS uses relative house positions ("trine FROM
  the 2nd lord") but the code uses absolute houses from lagna ({1,5,9}).

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  PDF: BPHS-Santhanam-Vol-1.pdf

  AFFECTED RULES (from docs/s318_deep_audit.md lines 1178-1180):
  1. BPHS1306 — Ch.13 v.5 (src/corpus/bphs_v2_ch13.py, p.134)
     Verse says "trine FROM the 2nd lord" but code has absolute houses {1,5,9}.
     Fix: Use the derived house condition primitive:
       {"type": "planet_in_house_from", "planet": "...", "from": "lord_of_2",
        "houses": [1, 5, 9]}
     OR if the DSL uses a different pattern, check how existing rules handle
     "from" references by grepping: grep -r "planet_in_house_from" src/corpus/
     Also check: grep -r "derived_house" src/corpus/

  2. BPHS2021 — Ch.20 v.30 (src/corpus/bphs_v2_ch20.py, p.176)
     Verse says Rahu in "9th from 9th" = house 5 from lagna.
     This is ALSO in BUG-089 (fix #5: house 9 → house 5).
     If BUG-089 agent already fixes this, just verify and move on.
     If not, fix: change Rahu's house from 9 to 5.
     Also add commentary noting "9th from 9th = 5th from lagna" derivation.

  FOR EACH rule:
  1. Read the BPHS PDF to confirm the relative reference
  2. Read the corpus file and find the rule
  3. Check existing DSL patterns for relative positioning:
     grep -r "planet_in_house_from\|planet_from_derived\|from.*lord" src/corpus/
  4. Apply the fix using whichever pattern exists in the codebase
  5. If no existing pattern handles this, use the nearest approximation and
     document the gap in commentary_context

  IMPORTANT:
  - The relative house calculation must be correct: if verse says "trine from
    2nd lord" and 2nd lord is in house 7, then trines are houses 7, 11, 3
    (not absolute 1, 5, 9)
  - After all fixes: .venv/bin/pytest tests/ -q --tb=short -x
  - Run .venv/bin/ruff check src/ tests/

  Commit: fix(S319): BUG-092 — relative house positions per BPHS verse context
```

---

### Agent 5: BUG-093 — Marriage Timing Rules Incomplete (Ch.18 v.22-34)

```
prompt: |
  You are fixing 9 of 11 marriage timing rules in Ch.18 that are systematically
  incomplete. Each rule was loop-generated and encodes only the FIRST condition
  from its verse, dropping 2nd/3rd planetary requirements.

  Environment: .venv/bin/pytest, .venv/bin/ruff, Python 3.14
  PDF: BPHS-Santhanam-Vol-1.pdf
  File: src/corpus/bphs_v2_ch18.py

  BACKGROUND (docs/s318_deep_audit.md line 1182-1183):
  Ch.18 v.22-34 (marriage timing) — pp.166-169 in the PDF.
  Loop-generated rules encode only the FIRST condition from each verse,
  dropping 2nd/3rd planetary requirements.

  PROCESS:
  1. Read the BPHS PDF pages 166-169 (Ch.18 v.22-34)
  2. Read src/corpus/bphs_v2_ch18.py — find the marriage timing rules
     (they will have verse_refs like "Ch.18 v.22" through "Ch.18 v.34")
  3. For each rule, compare the encoded conditions against the PDF verse:
     - Does the verse have 2-3 conditions but the rule only has 1?
     - What conditions are missing?
  4. Add the missing conditions to each rule's conditions list
  5. Update commentary_context to reflect the full verse

  EXAMPLE of what "incomplete" looks like:
  - Verse says: "Marriage will occur when the 7th lord dasha runs AND Venus
    is strong AND the 2nd lord aspects the 7th"
  - Rule only has: {"type": "lord_in_house", "lord_of": 7, ...}
  - Missing: Venus strength condition AND 2nd lord aspect condition

  HOW TO FIX:
  - Add the missing conditions to the existing rule's conditions list
  - Do NOT create new rules — just complete the existing ones
  - If a verse has truly independent alternatives (OR), then split per
    granularity rules. But most marriage timing verses are conjunctive (AND).

  IMPORTANT:
  - Read EVERY verse v.22 through v.34 from the PDF
  - Count how many conditions each verse has vs how many are encoded
  - Some rules (2 of 11) may already be complete — verify and skip those
  - Marriage timing rules often reference dasha periods — use
    {"type": "lord_in_house", ...} or timing_window fields as appropriate
  - After all fixes: .venv/bin/pytest tests/ -q --tb=short -x
  - Run .venv/bin/ruff check src/ tests/

  Commit: fix(S319): BUG-093 — complete marriage timing conditions Ch.18 v.22-34
```

---

## After all agents complete

1. Cherry-pick each agent's commits onto main (same pattern as S318 Final Sweep)
2. Resolve any merge conflicts (unlikely — each agent touches different chapter files)
3. Run full verification:
   ```
   .venv/bin/pytest tests/ -q --tb=short -x
   .venv/bin/ruff check src/ tests/
   PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --all
   ```
4. Update docs (MEMORY.md, CHANGELOG.md, SESSION_LOG.md)
5. Commit docs update

## Expected outcome

- BUG-089: 10 condition values corrected
- BUG-090: ~4 new aspect-variant rules added
- BUG-091: 3 rules converted from AND→OR logic
- BUG-092: 2 rules converted from absolute→relative houses
- BUG-093: 9 rules completed with missing conditions
- Total S318 bugs: 103/104 fixed (only BUG-094 remains — already done this session)
- All 104 bugs CLOSED

## Non-negotiable rules

1. Read the BPHS PDF verse BEFORE editing any rule
2. Do NOT change fields that are already correct
3. Do NOT touch scoring weights in multi_axis_scoring.py
4. Do NOT modify corpus files outside the specific rules listed
5. Run tests AFTER each fix, not just at the end
6. When the verse is ambiguous, keep the existing encoding and add a commentary note
