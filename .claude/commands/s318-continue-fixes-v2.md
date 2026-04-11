# S318 Phase -2: Complete Remaining Bug Fixes

## Context

S318 deep audit found 104 deduplicated bugs across 660 files (178,072 lines). The full audit is in `docs/s318_deep_audit.md`. The canonical architecture is in `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`.

## What's Already Fixed (65 of 104 bugs, across 12 commits)

### Prior session (35 bugs): commits 2d9887f0, 7518c15b, 93d61e14, 64751c97
BUG-001,002,003,004,005,006,007,008,009,010,011,012,013,015,016,017,024,025,028,029,030,031,032,033,034,035,036,037,039,040,050,056,057,058,066

### This session (30 bugs): commits 0a01bcb0 through e37799d4
- BUG-081: Dignity wired into scoring as R24 (scoring.py)
- BUG-043,044,045,046,047,048,049: KNOWN_GAP comments for missing features
- BUG-051,052,053,055,064,065: Data table corrections (gentle signs, sthir karaks, dig bala, SAV, yogakaraka)
- BUG-068,069,070,071,072,073,074: Silent failure fixes
- BUG-079,080: Broken `vargas` imports in 5 files, setup_ci_guard `__main__` guard
- BUG-083,085,088: Architecture fixes (weight alignment, mirror() deepcopy, scoring_v3 flagged)
- BUG-095,096: Corpus fixes (fabricated claim removed, header count)
- BUG-099,101,102,104: Test fixes (deleted stubs, added dignity tests, removed no-ops)

## What Remains (39 of 104 bugs)

### PRIORITY 1: Dead Code Cleanup (BUG-075, 076, 077, 078)

These are the largest remaining items by line count. Deleting dead code reduces confusion and prevents future bugs from copying wrong patterns.

**BUG-075: Delete 15 orphaned modules (0 production importers)**

Verify each has zero importers before deleting. The audit identified these:

| Module | Lines | Why Dead |
|--------|-------|----------|
| `planet_avasthas.py` | 271 | S138, replaced by avasthas.py |
| `sayanadi_full.py` | 256 | S49, replaced by avasthas.py |
| `friendship.py` | 142 | Replaced by panchadha_maitri.py |
| `yogas_additions.py` | 307 | 0 importers |
| `shodashavarga_bala.py` | 161 | Test-only |
| `kp_full.py` | 257 | Test-only |
| `kp_cuspal.py` | 258 | Test-only |

For each module:
1. `grep -r "from src.calculations.MODULE" src/` — verify 0 production importers
2. `grep -r "MODULE" tests/` — check if tests import it; if so, delete those tests too
3. Delete the file

**BUG-076: Delete ~124 remaining dead files (22,692 lines)**

The audit section "DEAD CODE SUMMARY" lists the full inventory. Focus on:
- 8 dead dasha systems: kalachakra, tara, ashtottari, yogini, drig, shoola, lagna_kendradi, pratyantar
- Full Jaimini subsystem if unused: jaimini_full, jaimini_rashi_drishti, karakamsha, stronger_of_two
- KP extensions: kp_cuspal, kp_full, kp_sublord, kp_ayanamsha
- Entire dead subsystems: `src/interfaces/`, `src/ci/`, `src/research/`, `src/ml/`, `src/feedback/`, `src/privacy/`

For each: verify zero production importers, check test-only usage, delete.

**BUG-077: 12 dead expressions (computed, result discarded)**

| File:Line | Expression |
|----------|-----------|
| dominance_engine.py:162 | `roles.house_lords.get(12, "")` |
| pressure_engine.py:162 | `roles.house_lords.get(12, "")` |
| pressure_engine.py:250 | `compute_house_map(chart)` |
| promise_engine.py:131 | `ph.get(lord, 0)` |
| planet_chains.py:95 | `compute_house_map(chart)` |
| extended_yogas.py:367 | `compute_house_map(chart)` |
| nabhasa_yogas.py:100 | panapara check result |
| longevity.py:68 | `_DEBIL_LON.get(planet)` |
| scoring_v2.py:283 | sign_index computation |
| divisional_charts.py:175 | `3 if si % 2 == 0 else 8` |
| yogas_pvrnr.py:85 | `ph.get(hmap.house_lord[9], 0)` |

For each: read the surrounding code, delete the dead expression or assign it if the computation was intended to be used.

**BUG-078: 13 dead functions**

| Function | File |
|----------|------|
| `_houses_aspected_by` | scoring.py |
| `score_chart_strict` | scoring.py |
| `_is_functional_benefic` | scoring_v3.py |
| `_is_functional_malefic` | scoring_v3.py |
| `SCHOOL_RULE_DECLARATIONS_LOADED` | scoring_v3.py |
| `_house_lord_sanity` | scoring_v2.py |
| `_d9_sign_index` | nakshatra.py |
| `_SIGN_NAMES` | yogas_additions.py (dead module) |
| `_KENDRA`, `_UPACHAYA` | nabhasa_yogas.py |
| `_NAT_BENEFIC`, `_NAT_MALEFIC` | multi_lagna.py |
| `COMBUSTION_ORBS_RETROGRADE` | dignity.py |
| `compute_dignity_legacy` | dignity.py |

For each: verify 0 callers with grep, then delete.

### PRIORITY 2: Architecture Flaws (BUG-082, 084, 086, 087)

**BUG-082: Two parallel scoring engines**

`score_chart()` (scoring.py) and `score_all_axes()` (multi_axis_scoring.py) serve different API endpoints. Same chart, different scores. Add a deprecation warning to `score_all_axes()` and add RuleResult traceability to align them over time. Not a one-commit fix — add the deprecation warning and document the reconciliation plan.

**BUG-084: CalcConfig name collision**

Two different classes named `CalcConfig` exist. Find both, rename one to avoid confusion:
```
grep -rn "class CalcConfig" src/
```

**BUG-086: functional_dignity vs functional_roles disagree**

`functional_dignity.py` uses BPHS-verified `KNOWN_FUNCTIONAL_MALEFICS`. `functional_roles.py` uses algorithmic classification that sometimes contradicts. 10 consumers use functional_roles, 3 use functional_dignity. Fix: redirect the 10 consumers to use `KNOWN_FUNCTIONAL_MALEFICS` from functional_dignity as canonical.

**BUG-087: 5 avastha modules with 3 value sets**

`avastha.py`, `avastha_v2.py`, `avasthas.py`, `planet_avasthas.py`, `sayanadi_full.py` — three different multiplier sets. `avasthas.py` is canonical (BPHS-verified in S317). Redirect `pressure_engine.py` to import from `avasthas.py`. Delete `planet_avasthas.py` and `sayanadi_full.py` (already dead per BUG-075).

### PRIORITY 3: Remaining Data Table Error (BUG-054)

**BUG-054: H10 Sthir Karak**

scoring.py has [Sun, Mercury, Jupiter, Saturn], multi_axis has [Sun, Mercury, Saturn]. Need BPHS Ch.32 verification to decide whether Jupiter belongs. Read the BPHS PDF at the relevant page and update both files to match.

### PRIORITY 4: Silent Failure (BUG-067)

**BUG-067: 21 silent `except: pass` in app.py**

These are UI exception handlers (Streamlit). Most are acceptable for graceful degradation. Review each — if the handler swallows a computation error, add `logger.exception()`. If it's a UI-optional feature, leave as-is with a comment.

### PRIORITY 5: Test Gaps (BUG-097, 098, 103)

**BUG-097: avasthas.py has 0 test coverage**

Write tests for `avasthas.py` covering:
- Baladi avastha (even-sign reversal)
- Jagradadi avastha (dignity-based classification)
- Lajjitadi avastha (6 states)
Each test should cite the relevant BPHS chapter/verse.

**BUG-098: 107 exact float assertions → pytest.approx**

Search tests for `== float_literal` patterns and convert to `pytest.approx()`. Focus on:
```
grep -rn "== [0-9]*\.[0-9]" tests/ | grep -v "approx" | head -40
```

**BUG-103: List-valued conditions never tested**

Write test for `rule_firing.py` that verifies `planet_not_in_house` and `planet_not_aspecting` correctly check ALL houses in a list (the fix from BUG-035/036).

### DEFERRED TO ENCODING SESSIONS (BUG-089, 090, 091, 092, 093, 094)

These are corpus data errors that require BPHS PDF verification:

| Bug | What | Why Deferred |
|-----|------|-------------|
| BUG-089 | 10 factual errors in V2 corpus | Each needs verse-by-verse BPHS verification |
| BUG-090 | ~40 rules: aspect vs occupation confusion | Requires re-reading BPHS text for each rule |
| BUG-091 | OR-vs-AND logic in 3 rules (BPHS1501, BPHS1611, BPHS1600) | Needs BPHS text to determine correct logic |
| BUG-092 | Relative→absolute house positions | Needs verse context to fix correctly |
| BUG-093 | 9 of 11 marriage timing rules incomplete | Requires encoding missing conditions |
| BUG-094 | Ch.19 missing 9 of 15 slokas | Full encoding session needed (BPHS Vol 1 pp.169-172) |

**Do NOT attempt these in a fix session.** They require the full encoding protocol (OCR → Audit → Encode → Validate).

## Execution Protocol

Same as the previous continuation prompt — autonomous fix loop:

### Step 1: Pick Next Bug (priority order above)
### Step 2: Diagnose (read file:line from audit)
### Step 3: Fix (root cause only, no tangential changes)
### Step 4: Verify
- `.venv/bin/pytest tests/ -q --tb=short -x`
- `.venv/bin/ruff check src/ tests/`
### Step 5: Commit
```
fix(S318): BUG-NNN — [one-line root cause description]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```
### Step 6: Continue to next bug

### Stop Conditions
- 15 fix cycles completed → report progress
- Same test fails twice with different errors → STOP
- Fix causes >5 unrelated failures → STOP
- All 39 bugs cleared → report final tally

## Baseline

- Tests: 14743 passed, 210 skipped, 360 xfailed
- Ruff: 0 errors
- Total fixed so far: 65 of 104

## Key Files

- Audit: `docs/s318_deep_audit.md`
- Architecture: `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`
- BPHS Vol 1: `BPHS-Santhanam-Vol-1.pdf`
- BPHS Vol 2: `BPHS-Santhanam-Vol-2.pdf`
- Tools index: `tools/INDEX.md`

## Session Type

This is a **governance/fix session** (not encoding). No new corpus rules. Fix existing bugs, delete dead code, wire existing computations.
