# CLAUDE.md — LagnaMaster

## /cook — Multi-session batch execution

**Usage:** `/cook S195–S200` or `/cook S[X]–S[Y]`

Executes sessions X through Y in sequence within a single conversation.

### Per-session execution order (mandatory)

1. Read `docs/ROADMAP.md` entry for this session (deliverable, guardrails, status)
2. Read only the files listed in that session's RELEVANT SIGNATURES
3. Write all tests to `tests/test_s[N]_*.py` — ALL FAILING before any implementation
4. Implement until `ruff check src/ tests/` = 0 errors and all new tests pass
5. Run `.venv/bin/python update_docs_s[N].py` (create it if it doesn't exist)
6. `git add` exactly the files created/modified + docs → `git commit` → `git push`

### Context inheritance (token efficiency)

- **Same conversation:** skip re-reading `docs/MEMORY.md`, `docs/CHANGELOG.md`,
  `docs/SESSION_LOG.md` — use conversation context already in scope
- **Fresh conversation (cold start):** read `docs/MEMORY.md` (current state) +
  `docs/ROADMAP.md` (next session entry) before starting S[X]

### Autonomy rules

- Own every technical decision. Tests pass + ruff 0 + pre-push hook green = ships.
- Never ask permission for implementation choices.
- **On blocker:** reduce scope to what passes, commit that, record blocker in
  CHANGELOG and MEMORY under "Known Issues", continue to next session.
- **On guardrail conflict:** note in commit message + CHANGELOG, do not skip or violate.

### Standard commit format

```
feat(S[N]): [one-line description]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Standard update_docs_s[N].py contract

Every session must produce an `update_docs_s[N].py` that patches:
- `docs/CHANGELOG.md` — new session entry (Three-Lens format)
- `docs/MEMORY.md` — test count, session progress line, Next session pointer
- `docs/SESSION_LOG.md` — session entry under correct Phase heading
- `docs/ROADMAP.md` — mark session ✅
- `docs/ARCHITECTURE.md` — new module entries if files were created

### Ship definition

A session is shipped when:
1. All new tests pass
2. `ruff check src/ tests/` = 0 errors
3. Pre-push hook passes (runs full pytest + ruff automatically)
4. `git push` succeeds

---

## Project context

- **Repo:** `github.com/agniinvestor/LagnaMaster`
- **Engine:** `v3.0.0` | **Python:** 3.14 | **Ephemeris:** pyswisseph JPL DE431
- **Venv:** `.venv/` — use `.venv/bin/pytest`, `.venv/bin/ruff`, `.venv/bin/python`
- **Test runner:** `pytest tests/ -q --tb=short`
- **Guardrails:** `docs/GUARDRAILS.md` — read the entry for any guardrail cited in ROADMAP
- **Pre-push hook:** `.git/hooks/pre-push` — runs full suite before every push
- **India 1947 fixture:** used in integration tests across many sessions
  ```python
  compute_chart(year=1947, month=8, day=15, hour=0.0,
                lat=28.6139, lon=77.2090, tz_offset=5.5)
  # Lagna: Taurus | Moon: Pushya (Saturn MD) | H2 score: negative
  ```

---

## What NOT to do

- Do not re-read `docs/MEMORY.md` mid-batch (stale relative to conversation context)
- Do not add features beyond the ROADMAP deliverable
- Do not modify `_WEIGHTS` tables in `multi_axis_scoring.py` unless the session
  explicitly targets scoring recalibration (breaks regression snapshots)
- Do not `git add -A` — always add specific files to avoid committing stale scripts
- Do not skip the pre-push hook (`--no-verify`)
