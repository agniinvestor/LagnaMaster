# tools/ — LagnaMaster Development Automation

This directory contains the session automation system. The goal is zero manual
orientation work: every session brief is machine-generated, every quality check
is automated, every docs sync is atomic with the code commit.

---

## Session Loop

```
python tools/start_session.py
  └─ reads: MEMORY.md, ROADMAP.md, GUARDRAILS.md
  └─ runs:  live test suite + ruff
  └─ builds: targeted READ LIST with line ranges
  └─ outputs: sub-400-token brief → paste to Claude

[paste brief to Claude as first message]
  └─ Claude reads only the specified files/line ranges
  └─ Claude writes tests
  └─ Claude writes implementation
  └─ Claude writes update_docs_s[N].py

python update_docs_s[N].py
  └─ updates: docs/MEMORY.md, docs/CHANGELOG.md, docs/BUGS.md, etc.
  └─ commits: docs changes

git push
  └─ pre-push hook: pytest + ruff + docs currency
  └─ blocks if any check fails
  └─ pushes if all pass
```

---

## Tools

### `start_session.py`

Generates the session brief for Claude.

```bash
# Default: uses next session from MEMORY.md
.venv/bin/python3 tools/start_session.py

# Override to run a specific session
.venv/bin/python3 tools/start_session.py --session S192

# Skip live test run (faster, uses MEMORY.md baseline)
.venv/bin/python3 tools/start_session.py --no-test-run
```

**What it produces:**
- Live test count (runs pytest)
- Git SHA
- Session plan from ROADMAP.md
- Active guardrails for this session
- Targeted READ LIST — exact files and line ranges Claude needs
- Acceptance criteria
- Instructions for Claude

**Brief is also saved to:** `.session_brief_s[n].txt`
```bash
pbcopy < .session_brief_s191.txt   # macOS — copies to clipboard
xclip -sel clip < .session_brief_s191.txt  # Linux
```

---

### `pre_push_hook.sh`

The unified quality gate. Runs automatically on `git push`.

**Three checks:**
1. Full pytest suite — must pass (0 failures)
2. Ruff lint — must have 0 errors
3. Docs currency — MEMORY.md test count must match live count

**If any check fails:** push is blocked with clear error message and fix commands.

**To install:**
```bash
.venv/bin/python3 tools/install_hooks.py
```

**Emergency bypass (do not use routinely):**
```bash
git push --no-verify
```

---

### `install_hooks.py`

One-shot installer for git hooks. Idempotent — safe to re-run.

```bash
.venv/bin/python3 tools/install_hooks.py
```

Installs `pre_push_hook.sh` → `.git/hooks/pre-push` with executable permissions.

---

## Design Principles

**One quality gate, not many.** The pre-push hook is the single point where tests,
lint, and docs currency are enforced. There are no intermediate manual review steps.
Green means push. Red means fix.

**Docs are atomic with code.** `update_docs_s[N].py` is produced by Claude as part
of the session, not as a separate post-session step. The pre-push hook verifies that
docs are current. A session without current docs cannot push.

**Briefs are machine-generated, not human-written.** `start_session.py` reads live
state from docs/ and the test suite. The brief is always accurate because it's
generated from current reality, not written from memory.

**READ LISTs are targeted, not broad.** The brief tells Claude exactly which files
and which line ranges to read. Not "read ARCHITECTURE.md" but
"docs/ARCHITECTURE.md:45-72". This eliminates orientation token spend.
