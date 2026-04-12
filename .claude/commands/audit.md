Run the full LagnaMaster audit suite and report results.

Do the following steps sequentially, capturing output from each:

1. Run `.venv/bin/python tools/v2_scorecard.py` and capture the output as SCORECARD_OUTPUT.
2. Run `.venv/bin/python tools/verse_audit.py --compare` and capture the output as AUDIT_OUTPUT. Count lines that indicate unencoded claims.
3. Run `.venv/bin/pytest tests/ -q --tb=short` and capture the output as TEST_OUTPUT. Extract pass/fail counts.
4. Run `.venv/bin/ruff check src/ tests/` and capture the output as LINT_OUTPUT. Count lint errors.

After all four complete, print a summary table like this:

```
╔══════════════════════╦════════════╗
║ Check                ║ Result     ║
╠══════════════════════╬════════════╣
║ Scorecard            ║ <result>   ║
║ Unencoded claims     ║ <count>    ║
║ Tests                ║ X passed, Y failed ║
║ Lint                 ║ <count> errors ║
╚══════════════════════╩════════════╝
```

If ANY check has failures (scorecard below threshold, unencoded claims > 0, test failures > 0, or lint errors > 0):
- List each specific failure with details
- Recommend concrete next steps to fix each one

Keep output concise. Do not ask for confirmation. $ARGUMENTS is ignored.
