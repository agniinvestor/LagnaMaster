# Autonomous Bug Fixing Loop

Run an autonomous cycle: test, diagnose, fix root cause only, verify, commit, repeat.

## Setup

1. Confirm test command with user (default: `.venv/bin/pytest tests/ -q --tb=short -x`)
2. Set fix limit (default: 15 cycles — stop after 15 fixes or all green)
3. Create tracking scratch file: `fixes_log.md` with columns: cycle, test, file_changed, root_cause, status

## Loop (repeat until all green or limit reached)

### Step 1: Run Tests
```
.venv/bin/pytest tests/ -x --tb=short 2>&1 | head -80
```
If all green: report success and stop. If failure: proceed.

### Step 2: Diagnose
- Read the FAILING test file to understand what it expects
- Read the SOURCE code the test exercises
- Identify the ROOT CAUSE — not the symptom

### Step 3: Fix
- Fix ONLY the root cause
- NO refactoring, NO doc updates, NO tangential changes, NO "while I'm here" improvements
- ONE fix per cycle

### Step 4: Verify
- Re-run the SPECIFIC test file: `.venv/bin/pytest tests/path/to/test.py -x --tb=short`
- Same error twice: investigate deeper, do NOT move on
- Different error after fix: STOP and report (regression)
- Green: proceed

### Step 5: Commit
```
fix(S318): BUG-NNN — [one-line root cause description]
```

### Step 6: Log
Update `fixes_log.md` and return to Step 1.

## Rules
- If same test fails twice with different errors: STOP
- If fix limit reached: STOP and report remaining failures
- If fix causes >5 unrelated test failures: STOP and investigate
- Fixing test assertions to match wrong behavior = VIOLATION
- Refactoring during a fix cycle = VIOLATION
