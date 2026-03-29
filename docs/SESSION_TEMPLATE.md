# SESSION_TEMPLATE.md — Session Planning Template
> Copy this template to plan each session. Use it BEFORE writing any code.

---

## Pre-Session Checklist (Always Run First)

```bash
# Ground truth only — ignore GitHub web UI (known caching issue)
cd ~/LagnaMaster && git log --oneline -5 && git status

# Lint check (must be 0)
.venv/bin/ruff check src/ tests/ tools/ 2>&1 | grep -c 'error'

# Test count (must match or exceed 1338)
PYTHONPATH=. .venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3
```

Then:
- [ ] MEMORY.md "Next Session" matches this session number
- [ ] All prerequisites listed below confirmed complete
- [ ] Applicable guardrails re-read from GUARDRAILS.md
- [ ] OSF status checked if running any empirical analysis (G22)
- [ ] VedAstro MCP available for chart verification if computing charts (G23)

---

## Session S[N] — [Title]

**Phase:** [Phase name]  
**Date:** [YYYY-MM-DD]  
**Prerequisites:** S[N-1] complete. [Any specific conditions.]

---

### GOAL

[1–2 sentences: what this session accomplishes and why it matters right now.]

---

### Three-Lens Planning

| Lens | What this session advances | Key question |
|------|--------------------------|-------------|
| 🏗 Tech | [module created/wired, protocol updated, debt reduced] | [specific question] |
| ⭐ Astrology | [rules added, calculations improved, corpus progress] | [specific question] |
| 🔬 Research | [KPI moved, bias addressed, pre-registration needed?] | [specific question] |

---

### Applicable Guardrails

- **G[N]:** [name] — [how this session must comply]

---

### INPUTS

```
src/[file].py
tests/[file].py
```

---

### OUTPUTS (Commit These)

```
src/[new].py      (NEW: [description])
src/[existing].py (UPDATED: [what changed exactly])
tests/test_[x].py (NEW/UPDATED: [what it tests])
```

---

### TESTS REQUIRED

Minimum new tests: [N]

| Test name | Assertion | Why it matters |
|-----------|-----------|---------------|
| `test_[name]` | [what it checks] | [reason] |

**Full test suite must still pass** at baseline count or above (the 200+ ADB diverse
fixture suite is the regression gate). India 1947 position verification only applies
when `ephemeris.py`, `varga.py`, `narayana_dasa.py`, `nakshatra.py`, or `dignity.py`
appear in the session READ LIST — the brief will note this explicitly when relevant.

---

### CROSS-VALIDATION

| Reference | Method | Tolerance |
|-----------|--------|-----------|
| VedAstro (MIT) | `pip install VedAstro`; compare [calculation] | Within [N]° |
| PyJHora (AGPL — study only) | Compare output values manually | Within [N]° |

---

### CLASSICAL SOURCE

| Text | Chapter/Verse | What it governs |
|------|--------------|----------------|
| BPHS Ch.[N] v.[N] | [exact ref] | [rule/calculation] |

---

### ACCEPTANCE CRITERIA

- [ ] All 1338+ existing tests still pass
- [ ] [N]+ new tests pass
- [ ] 0 ruff errors
- [ ] Full test suite: [baseline] → [baseline+N] (200+ ADB diverse fixtures pass)
- [ ] If READ LIST includes ephemeris/varga/nakshatra/dignity: verify India 1947
  positions (Lagna=7.7286°Tau ±0.05°, Sun=27.989°Can, Moon=3.9835°Can)
- [ ] [Functional requirement]

---

### RISK FLAGS

- **[Risk]:** [Description] → **Mitigation:** [How to handle]

---

### METRICS IMPACT

| Domain | Metric | Before | After |
|--------|--------|--------|-------|
| [Domain] | [Metric] | [value] | [expected] |

---

## Post-Session Protocol (MANDATORY)

```bash
# 1. Full test suite
PYTHONPATH=. .venv/bin/pytest tests/ -q 2>&1 | tail -5

# 2. Lint
.venv/bin/ruff check src/ tests/ tools/

# 3. Commit
git add -A && git commit -m "feat(S[N]): [description]"
git push

# 4. Run documentation sync script:
#    .venv/bin/python3 update_docs_s[N].py
#    git add MEMORY.md PLAN.md CHANGELOG.md README.md
#    git commit -m "docs(S[N]): sync documentation"

# 5. Update MEMORY.md:
#    - Change "Next Session" to S[N+1]
#    - Update test count if changed
#    - Note any new wiring gaps found OR confirmed closed
#    - Note any new scoring invariants

# 6. Append to CHANGELOG.md (use template below)
# 7. Mark fixed bugs in BUGS.md as ✅ FIXED [SHA]
# 8. Update KPIS.md if any metric moved
# 9. Update CLASSICAL_CORPUS.md if corpus grew
```

---


---

## Debugging Protocol (read before attempting any fix)

**Rule: Read the actual error before guessing at the cause. One diagnosis, one fix.**

### pytest exit codes — what they mean

| rc | Meaning | Correct action |
|----|---------|---------------|
| 0 | All tests passed | Nothing |
| 1 | **Tests ran but some failed** | Read the FAILED lines — fix the code |
| 2 | Interrupted (Ctrl-C or collection error) | Check for import errors or bad test syntax |
| 3 | Internal pytest error | Upgrade pytest or check conftest.py |
| 4 | Command-line usage error | Check pytest invocation flags |
| 5 | No tests collected | Check test file names and PYTHONPATH |

**rc=1 means tests ran and failed. It does NOT mean the environment is broken.**
If you see dots appearing (`...........`) before rc=1, pytest ran successfully — the
failures are in the test output, not in the invocation.

### macOS file descriptor limit (Errno 24 / "Too many open files")

Cause: macOS defaults to 256 open file descriptors. The 1300+ test suite exhausts
this when pytest is called twice in quick succession (e.g. pre-push hook + start_session.py).

Fix in bash scripts: `ulimit -n 4096` at the top of the script.
Fix in Python subprocess callers:
```python
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
```

### Diagnostic checklist before writing any fix

1. What is the exact error message or exit code?
2. What is the UNIQUE difference between the failing path and a working path?
   (e.g. pre-push hook works, start_session.py doesn't → the only difference is `ulimit`)
3. Does the error message directly point to a file, line, or known condition?
4. Only after answering 1–3: write the minimal fix that addresses the diagnosed cause.

**Do not ship a fix that addresses a hypothesised cause. Read the output.**

## CHANGELOG Entry Template

```markdown
## S[N] — [YYYY-MM-DD] — [Session Title]

**Commit:** [SHA]
**Tests:** [N passing / N skipped / 0 lint errors]

### What was built
- `[module].py`: [description]

### What was wired
- [Connection]: [description]

### New invariants
- #[N]: [description] — [classical source]

### Bugs fixed
- [Bug ID]: [fix description] (see BUGS.md)

### Three-Lens Notes
- Tech: [architectural impact]
- Astrology: [rules added, corpus progress]
- Research: [scientific integrity impact]

### Next session
S[N+1] — [Title]
```
