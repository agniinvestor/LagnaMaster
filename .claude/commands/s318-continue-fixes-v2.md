# S318 Phase -2: Complete Remaining Bug Fixes

## Context

S318 deep audit found 104 deduplicated bugs across 660 files (178,072 lines). The full audit is in `docs/s318_deep_audit.md`. 65 are fixed. 39 remain. This prompt uses the project's existing skills and parallel agent infrastructure to clear them efficiently.

## Already Fixed: 65 of 104

Prior sessions fixed BUG-001–013,015–017,024,025,028–037,039,040,043–055,056–058,064–066,068–074,079–081,083,085,088,095,096,099,101,102,104.

## What Remains: 39 bugs in 5 workstreams

| Workstream | Bugs | Independent? |
|-----------|------|-------------|
| A: Dead code cleanup | BUG-075,076,077,078 | Yes |
| B: Architecture flaws | BUG-082,084,086,087 | Yes |
| C: Data table + silent failure | BUG-054,067 | Yes |
| D: Test gaps | BUG-097,098,103 | Yes |
| E: Corpus data (DEFERRED) | BUG-089–094 | N/A — encoding session |

Workstreams A–D are independent and can run in parallel.

---

## Step 0: Session Startup (MANDATORY)

Read these files — do NOT skip:
1. `lessons_learned.md`
2. `core_principles.md`
3. `tools/INDEX.md`

Verify baseline:
```
.venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
.venv/bin/ruff check src/ tests/ 2>&1 | tail -1
```
Expected: 14743 passed, 0 lint errors.

---

## Step 1: Dispatch Parallel Agents for Workstreams A–D

Use the `superpowers:dispatching-parallel-agents` skill pattern. Spawn 4 agents using the Agent tool, one per workstream. Each agent works in an isolated worktree (`isolation: "worktree"`) so they don't conflict.

### Agent A: Dead Code Cleanup (BUG-075, 076, 077, 078)

```
prompt: |
  You are fixing dead code bugs in the LagnaMaster codebase. Read docs/s318_deep_audit.md 
  for full details.

  BUG-075: Delete orphaned modules with 0 production importers. For each, grep to verify 
  zero importers in src/, then delete. Modules: planet_avasthas.py, sayanadi_full.py, 
  friendship.py, yogas_additions.py, shodashavarga_bala.py, kp_full.py, kp_cuspal.py. 
  Also delete any test files that ONLY test these dead modules.

  BUG-076: Delete dead subsystem directories if completely unreachable:
  src/interfaces/, src/ci/, src/research/, src/ml/, src/feedback/, src/privacy/.
  Verify each with grep before deleting.

  BUG-077: Delete 12 dead expressions (computed, result discarded):
  dominance_engine.py:162, pressure_engine.py:162, pressure_engine.py:250, 
  promise_engine.py:131, planet_chains.py:95, extended_yogas.py:367, 
  nabhasa_yogas.py:100, longevity.py:68, scoring_v2.py:283, 
  divisional_charts.py:175, yogas_pvrnr.py:85.

  BUG-078: Delete 13 dead functions (0 callers): _houses_aspected_by (scoring.py), 
  score_chart_strict (scoring.py), _is_functional_benefic/_is_functional_malefic/
  SCHOOL_RULE_DECLARATIONS_LOADED (scoring_v3.py), _house_lord_sanity (scoring_v2.py), 
  _d9_sign_index (nakshatra.py), _KENDRA/_UPACHAYA (nabhasa_yogas.py), 
  _NAT_BENEFIC/_NAT_MALEFIC (multi_lagna.py), COMBUSTION_ORBS_RETROGRADE/
  compute_dignity_legacy (dignity.py).

  For EVERY deletion: grep first to confirm 0 callers/importers. Do NOT delete anything 
  with active references.

  After all deletions: run .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): BUG-075,076,077,078 — delete dead code (N files, M lines removed)
```

### Agent B: Architecture Flaws (BUG-082, 084, 086, 087)

```
prompt: |
  You are fixing architecture bugs in LagnaMaster. Read docs/s318_deep_audit.md for details.

  BUG-082: Add deprecation warning to score_all_axes() in multi_axis_scoring.py:
  import warnings; warnings.warn("score_all_axes is deprecated, use score_chart", 
  DeprecationWarning, stacklevel=2). This is the first step toward reconciliation.

  BUG-084: Two classes named CalcConfig exist. Find both with grep, rename the less-used 
  one to avoid confusion (e.g., CalcConfigV2 or EngineCalcConfig).

  BUG-086: functional_roles.py sometimes contradicts BPHS-verified 
  KNOWN_FUNCTIONAL_MALEFICS in functional_dignity.py. Find consumers of functional_roles 
  (grep "from src.calculations.functional_roles" src/) and redirect them to use 
  KNOWN_FUNCTIONAL_MALEFICS from functional_dignity.py as canonical source.

  BUG-087: pressure_engine.py imports from avastha.py (wrong multipliers). Change to 
  import from avasthas.py (BPHS-verified in S317). Grep to find the exact import and 
  update it. planet_avasthas.py and sayanadi_full.py deletion handled by Agent A.

  After all fixes: run .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit each bug separately:
  fix(S318): BUG-082 — add deprecation warning to score_all_axes
  fix(S318): BUG-084 — rename CalcConfig collision
  fix(S318): BUG-086 — canonical functional malefics source
  fix(S318): BUG-087 — pressure_engine uses avasthas.py
```

### Agent C: Data Table + Silent Failure (BUG-054, 067)

```
prompt: |
  You are fixing 2 bugs in LagnaMaster. Read docs/s318_deep_audit.md for details.

  BUG-054: H10 Sthir Karak disagreement. scoring.py has [Sun, Mercury, Jupiter, Saturn], 
  multi_axis_scoring.py has [Sun, Mercury, Saturn]. Read BPHS Vol 1 PDF (BPHS-Santhanam-Vol-1.pdf) 
  Ch.32 to verify which planets are correct H10 Sthir Karakas. Update both files to match.

  BUG-067: Review 21 silent except:pass blocks in src/ui/app.py. For each:
  - If it swallows a computation error that should propagate: add logger.exception()
  - If it's a UI-optional feature graceful degradation: add comment "# Graceful: [feature]"
  - Do NOT change the except:pass pattern for UI features — Streamlit needs them

  After all fixes: run .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): BUG-054,067 — H10 sthir karak + app.py silent handlers
```

### Agent D: Test Gaps (BUG-097, 098, 103)

```
prompt: |
  You are writing missing tests for LagnaMaster. Read docs/s318_deep_audit.md for details.

  BUG-097: Write tests for src/calculations/avasthas.py (currently 0 coverage). 
  Create tests/test_avasthas_coverage.py with tests for:
  - Baladi avastha: verify even-sign reversal per BPHS Ch.45 v.3
  - Jagradadi avastha: verify dignity-based classification per Ch.45 v.5
  - Lajjitadi avastha: verify 6 states per Ch.45 v.11-18
  Use the India 1947 fixture: compute_chart(year=1947, month=8, day=15, hour=0.0, 
  lat=28.6139, lon=77.2090, tz_offset=5.5)

  BUG-098: Find exact float assertions missing pytest.approx. Run:
  grep -rn "== [0-9]*\.[0-9]" tests/ | grep -v "approx" | grep -v "sign_index" | grep -v "house"
  Convert the most fragile ones (shadbala, scoring, ashtakavarga) to pytest.approx().
  Leave integer-like floats (== 0.0, == 1.0) alone.

  BUG-103: Write test for rule_firing.py list-valued conditions. Create test that verifies 
  planet_not_in_house and planet_not_aspecting check ALL houses in a list, not just the first.

  After all tests: run .venv/bin/pytest tests/ -q --tb=short -x && .venv/bin/ruff check src/ tests/
  
  Commit: fix(S318): BUG-097,098,103 — test coverage for avasthas, float assertions, list conditions
```

---

## Step 2: Reconcile Agent Results

After all 4 agents complete:

1. **Merge worktrees** — each agent's worktree has independent changes. Merge them sequentially:
   - Agent A first (deletions are cleanest)
   - Agent D next (new test files, no conflicts)
   - Agent B (architecture changes)
   - Agent C (data fixes)

2. **Run full verification** after merge:
   ```
   .venv/bin/pytest tests/ -q --tb=short -x
   .venv/bin/ruff check src/ tests/
   ```

3. **If merge conflicts:** resolve manually, prioritizing the agent that touched the file for a bug-specific fix.

---

## Step 3: Run /rework-check

Invoke the `/rework-check` skill to detect if any rework happened during the session. If rework is detected, follow the skill's mandatory lesson-learned protocol.

---

## Step 4: Invoke superpowers:verification-before-completion

Before claiming the session is done, invoke the `superpowers:verification-before-completion` skill. This ensures:
- All tests actually pass (not just claimed to pass)
- Lint is clean
- No regressions from baseline

---

## Step 5: Update Documentation

Update these files with session results:
- `docs/MEMORY.md` — test count, S318 Phase -2 entry
- `docs/CHANGELOG.md` — S318 Phase -2 entry with three-lens analysis
- `docs/SESSION_LOG.md` — S318 Phase -2 summary line

---

## Step 6: Completion Report

| Item | Value |
|------|-------|
| Bugs fixed this session | list each BUG-NNN |
| Bugs remaining | count (should be 6 — the deferred corpus bugs) |
| Tests before vs after | pass/fail/skip counts |
| Regressions | any (should be 0) |
| Dead code removed | file count + line count |
| Deferred to encoding | BUG-089–094 with reason |

---

## Corpus Data Bugs — DEFERRED (BUG-089–094)

These require BPHS PDF verification and the full encoding protocol. Do NOT attempt in this session.

| Bug | What | Why Deferred |
|-----|------|-------------|
| BUG-089 | 10 factual errors in V2 corpus | Verse-by-verse BPHS verification needed |
| BUG-090 | ~40 rules: aspect vs occupation confusion | Re-read BPHS text for each rule |
| BUG-091 | OR-vs-AND logic in 3 rules | BPHS text determines correct logic |
| BUG-092 | Relative→absolute house positions | Verse context needed |
| BUG-093 | 9 of 11 marriage timing rules incomplete | Missing conditions to encode |
| BUG-094 | Ch.19 missing 9 of 15 slokas | Full encoding session (BPHS Vol 1 pp.169-172) |

Use `/encode-chapter 19` in a future encoding session for BUG-094.

---

## Key Files

- Audit: `docs/s318_deep_audit.md`
- Architecture: `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`
- BPHS Vol 1: `BPHS-Santhanam-Vol-1.pdf`
- BPHS Vol 2: `BPHS-Santhanam-Vol-2.pdf`
- Tools index: `tools/INDEX.md`

## Session Type

**Governance/fix session** — no new corpus rules, no new features. Fix bugs, delete dead code, write missing tests.

## Baseline

- Tests: 14743 passed, 210 skipped, 360 xfailed
- Ruff: 0 errors
- Total fixed so far: 65 of 104
