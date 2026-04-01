# CLAUDE.md — LagnaMaster

## Core Principles (NON-NEGOTIABLE — govern every decision)

1. **Long-term over quick** — evaluate every decision against the 1000+ session roadmap, not this session
2. **Nullify rework** — build controls BEFORE doing work. If a quality dimension exists, the gate must exist before encoding starts
3. **Right over easy** — always choose correct over convenient, even at 10× the effort. No shortcuts. No fake automation.
4. **Controls before work** — governance framework, validation, quality gates must exist BEFORE the work they govern
5. **Measure before claiming** — run the audit, run the scorecard, show the numbers. Never assume it passes.
6. **System enforces, not person** — if a standard matters, it's a code check. Markdown protocols are documentation; code is enforcement.
7. **Radical transparency** — when something is wrong, uncertain, or incomplete, say so immediately. Don't hide problems, optimise reporting, or hope issues self-resolve.
8. **Source fidelity** — record what the text says, not what you think it means. Interpretation goes in commentary, never in predictions or structured fields.
9. **Exhaust the problem before proposing** — when analysing gaps, designing controls, or planning work, assume your first pass is incomplete. Push yourself to find what you're missing before presenting. The user should not have to repeatedly ask "is that everything?" to get a thorough answer.
10. **Close the feedback loop** — when a mistake happens, it must flow through: Pattern → Lesson (lessons_learned.md) → Principle update (if systemic) → Control built (code enforcement) → Governance framework updated. A lesson without a corresponding control is an open loop. An open loop WILL recur.

## Session Types (NEVER MIX)

**Governance session:** Build controls, update protocols, add lessons, write tools. No encoding.
**Encoding session:** Read PDF, audit verses, encode rules, push. No framework debates, no tool building, no lessons updates. Use existing infrastructure only.

If an encoding session discovers a gap that needs a new control: NOTE IT and finish encoding. Build the control in the next governance session. Do not stop encoding to build infrastructure.

## Encoding Protocol (MANDATORY — 5 hard gates, no skipping)

```
OCR → [OCR Gate] → Audit → [Audit Gate] → Encode → [Validate Gate] → Ship
```

### Gate 0: OCR Verification (scanned PDFs only)
If source is a scanned PDF, run OCR first (`tesseract input.pdf output -l san+hin+eng pdf`).
Then verify: pick 3 verses spread across the chapter, compare OCR text against the PDF image.
If any verse has material errors (wrong numbers, dropped negations, garbled conditions), fix OCR before proceeding.
Store OCR'd text in `data/ocr/`. Skip this gate for text-based PDFs.

### Gate 1: Verse Audit
Read every sloka + commentary from the PDF/OCR text. Create `data/verse_audits/chN_audit.json` listing every claim per verse. Apply granularity definition (`docs/ENCODING_GRANULARITY.md`) — every distinct condition, exception, contrary, and direction-changing modifier is a separate claim.

### Gate 2: Audit Review (who audits the auditor?)
Before encoding, review the audit file for completeness. Check:
- Does claim count match verse complexity? (simple verse = 1-2 claims, complex = 3-6)
- Are contrary mirrors identified where text says "in contrary situation"?
- Are entity targets noted (father/spouse/children) not defaulted to native?
- Run the keyword scanner from ENCODING_GRANULARITY.md against the source text — any "if/unless/except" without a corresponding audit claim is a gap.

**The audit file is treated as ground truth downstream. Errors here propagate silently through every gate that follows.** This is the highest-leverage review point.

### Gate 3: Encode from Audit
The audit file is the spec. Each claim maps to a rule. When done, run `tools/verse_audit.py --compare` to verify zero unencoded claims.

### Gate 4: Validate (DURING work, not after)
Run `tools/v2_scorecard.py --file <chapter_file>` after completing each chapter file.
Fix all warnings and errors BEFORE moving to the next chapter or committing.
Do not accumulate warnings across files — each file must be clean before proceeding.

Then run full test suite + `ruff check` before commit. All must pass.

A chapter without a verse audit file CANNOT be encoded. The builder blocks with ValueError.
The builder also blocks on entity_target mismatches, mixed-entity rules, and prediction entity mismatches (T1-14 through T1-17).

## Plugin Usage by Session Type

**Encoding sessions — use these plugins:**
- **hookify** — enforce gates as pre-commit hooks (audit file exists, claim count matches, 5 docs updated)
- **code-review** — run on `chN_audit.json` at Gate 2 (review the audit, not the code)
- **commit-commands** — `/commit` to ship
- **security-guidance** — passive background monitoring
- **claude-md-management** — 5-doc update enforcement

**Governance sessions — use these plugins:**
- **superpowers** — `/brainstorm` + `/write-plan` for infrastructure design
- **feature-dev** — multi-agent feature development
- **pr-review-toolkit** — deep PR review for infrastructure changes
- **code-simplifier** — post-refactor cleanup

**Do NOT use in encoding sessions:**
- `/brainstorm` — the source text is the spec, not a design discussion
- `/write-plan` — the audit file is the plan
- `feature-dev` — encoding is not feature development
- `playwright` / `firecrawl` — all docs are local

## Session Protocol (MANDATORY)

**At session START:**
1. Read `lessons_learned.md` — check if any pattern is relevant to today's work
2. Read `core_principles.md` — refresh the decision-making constraints
3. Verify all controls exist for the work you're about to do (Principle #4)

**At session END:**
1. Did any rework happen this session? (amend commits, fix commits, re-encoding) → Add lesson
2. Did any audit control catch an error? → Add lesson about what the encoding missed
3. Did the user correct you on anything? → Add lesson about what should have been self-caught
4. Update lessons_learned.md with any new entries
5. If a new pattern emerged, update core_principles.md and governance framework

**A lesson without a control is an open loop. Close it before the session ends.**

---

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
