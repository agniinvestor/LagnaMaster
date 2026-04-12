# Health Check — Recurring Project Status Update

## Session type
**Governance** — no encoding, no new features. Diagnostics + update.

## Purpose

Re-run all diagnostics against the current codebase and update `docs/PROJECT_STRATEGY.md` with current numbers. This is the RECURRING version of `/health-assessment` (which produces PROJECT_STRATEGY.md from scratch).

**Prerequisite:** `docs/PROJECT_STRATEGY.md` must already exist. If it doesn't, run `/health-assessment` first.

---

## Step 1: Read the current baseline

Read `docs/PROJECT_STRATEGY.md` Section 1 (diagnostic dashboard). Record the PREVIOUS numbers.

---

## Step 2: Re-run all diagnostics

```bash
# ── Core health ──────────────────────────────────────────────────────────────
.venv/bin/pytest tests/ -q --tb=short
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/validate_constants.py
PYTHONPATH=. .venv/bin/python tools/import_boundary_check.py
PYTHONPATH=. .venv/bin/python tools/reachability_analysis.py

# ── Corpus maturity ──────────────────────────────────────────────────────────
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --all
PYTHONPATH=. .venv/bin/python tools/rule_grader.py
PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py

# ── Quality ──────────────────────────────────────────────────────────────────
PYTHONPATH=. .venv/bin/python tools/rework_detector.py

# ── Silent handlers ──────────────────────────────────────────────────────────
python3 -c "
import re
from pathlib import Path
silent = 0
for f in Path('src').rglob('*.py'):
    if '__pycache__' in str(f): continue
    lines = f.read_text().splitlines()
    for i, line in enumerate(lines):
        if not re.match(r'\s*except\s+(Exception|BaseException)', line): continue
        following = ' '.join(lines[i+1:i+6])
        if not any(kw in following for kw in ['logger','raise','log.','logging','warnings']):
            silent += 1
print(f'Silent handlers: {silent}')
"

# ── Counts ───────────────────────────────────────────────────────────────────
find src/ -name '*.py' -not -path '*__pycache__*' | wc -l
find src/ -name '*.py' -not -path '*__pycache__*' | xargs wc -l | tail -1
find tests/ -name '*.py' -not -path '*__pycache__*' | wc -l

# ── Architecture chain (quick verify) ────────────────────────────────────────
echo "=== Corpus→Engine connection ==="
grep -rn 'corpus\|rule_firing\|inference' src/scoring.py src/calculations/scoring_v3.py src/calculations/multi_axis_scoring.py 2>/dev/null | grep -v __pycache__ | wc -l
# 0 = DISCONNECTED, >0 = check what changed
```

---

## Step 3: Produce the delta report

Compare PREVIOUS numbers (from Step 1) to CURRENT numbers (from Step 2). Produce a table:

| Metric | Previous | Current | Delta | Direction |
|--------|----------|---------|-------|-----------|
| Tests passing | ? | ? | ? | better/worse/same |
| V2 rules (L3+) | ? | ? | ? | |
| Total rules | ? | ? | ? | |
| Silent handlers | ? | ? | ? | |
| Unreachable files | ? | ? | ? | |
| Condition/modifier flags | ? | ? | ? | |
| src/ files | ? | ? | ? | |
| src/ lines | ? | ? | ? | |

Highlight any metric that moved in the WRONG direction.

---

## Step 4: Check pending work progress

Read `docs/PROJECT_STRATEGY.md` Section 3 (the work list). For each OPEN item near the top of the priority order, check: has any work been done since the last health check?

```bash
# Check recent commits for work on top-priority items
git log --oneline --since="$(git log -1 --format=%ci docs/PROJECT_STRATEGY.md)" | head -20
```

Update the status of any items that moved from OPEN to DONE or IN PROGRESS.

---

## Step 5: Update PROJECT_STRATEGY.md

Edit `docs/PROJECT_STRATEGY.md`:
1. **Section 1**: Replace old diagnostic numbers with new ones. Update the "last verified" date.
2. **Section 3**: Update status of any work items that progressed.
3. **Section 6**: Add any new decisions made since the last check.

Do NOT rewrite Sections 2, 4, or 5 unless something fundamental changed (architecture decision, new lesson learned, new guardrail).

---

## Step 6: Commit

```
git add docs/PROJECT_STRATEGY.md
git commit -m "chore: health check update — [date] — [1-line summary of key changes]"
```

---

## Output

Print a short summary to the terminal:

```
=== HEALTH CHECK [date] ===
Tests:           [count] ([delta])
V2 rules:        [count] ([delta])
Silent handlers: [count] ([delta])
Corpus→Engine:   CONNECTED / DISCONNECTED
Top priority:    [item name] — [status]
Concerns:        [any metrics moving wrong direction]
```
