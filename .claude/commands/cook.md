Batch-execute LagnaMaster sessions $ARGUMENTS in sequence.

Read docs/ROADMAP.md to find each session entry in the range. For each session, in order:

1. Read only the files listed in that session's RELEVANT SIGNATURES (do not re-read MEMORY.md, CHANGELOG.md, or SESSION_LOG.md — use conversation context)
2. Write all tests to tests/test_s[N]_*.py — ALL FAILING before any implementation
3. Implement until `.venv/bin/ruff check src/ tests/` = 0 and all new tests pass
4. Create update_docs_s[N].py that patches CHANGELOG.md, MEMORY.md, SESSION_LOG.md, ROADMAP.md (mark ✅), ARCHITECTURE.md — then run it
5. `git add` exactly the files created/modified (never `git add -A`) → commit → push

Commit format: `feat(S[N]): [one-line description]\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`

On blocker: reduce scope to what passes, commit that, record blocker in CHANGELOG under "Known Issues", continue to next session without stopping.

Ship = pre-push hook green (runs full pytest + ruff automatically). Own all technical decisions — never ask permission.
