#!/bin/bash
# .git/hooks/pre-push (install via: tools/install_hooks.py)
#
# Unified quality gate — runs before every push:
#   1. pytest full suite
#   2. ruff lint
#   3. docs currency check (MEMORY.md test count matches live count)
#
# All three must pass. If any fails, the push is blocked.
# This is the single quality gate that replaces all manual review steps.

set -e
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Raise file descriptor limit — macOS default (256) exhausts under 1300+ test suite
ulimit -n 4096 2>/dev/null || true

PYTHON=".venv/bin/python3"
PYTEST=".venv/bin/pytest"
RUFF=".venv/bin/ruff"

# ── colours ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}  ✅ $1${NC}"; }
fail() { echo -e "${RED}  ❌ $1${NC}"; }
warn() { echo -e "${YELLOW}  ⚠️  $1${NC}"; }

echo ""
echo "🔍 Pre-push quality gate"
echo "────────────────────────"

FAILED=0

# ── 1. pytest ─────────────────────────────────────────────────────────────────
echo ""
echo "1/3  Running full test suite..."
PYTHONPATH="$ROOT" "$PYTEST" tests/ -q --tb=short 2>&1 | tee /tmp/lm_pytest_output.txt
PYTEST_EXIT=${PIPESTATUS[0]}

if [ $PYTEST_EXIT -eq 0 ]; then
    PASS_LINE=$(grep -E "^\d+ passed" /tmp/lm_pytest_output.txt | tail -1)
    pass "Tests: $PASS_LINE"
else
    fail "Tests failed — push blocked"
    FAILED=1
fi

# ── 2. ruff ───────────────────────────────────────────────────────────────────
echo ""
echo "2/3  Running ruff lint..."
RUFF_OUT=$("$RUFF" check src/ tests/ tools/ 2>&1)
RUFF_EXIT=$?

if [ $RUFF_EXIT -eq 0 ]; then
    pass "Ruff: 0 errors"
else
    fail "Ruff lint errors — push blocked"
    echo "$RUFF_OUT" | head -20
    FAILED=1
fi

# ── 3. Docs currency ──────────────────────────────────────────────────────────
echo ""
echo "3/3  Checking docs currency..."

# Extract live test count from pytest output
LIVE_COUNT=$(grep -oE "^[0-9]+ passed" /tmp/lm_pytest_output.txt | grep -oE "^[0-9]+" | tail -1)

# Extract documented test count from MEMORY.md
DOCS_COUNT=$(grep -oE "\*\*[0-9]+ passing" docs/MEMORY.md | grep -oE "[0-9]+" | head -1)

if [ -z "$LIVE_COUNT" ]; then
    warn "Could not parse live test count — skipping docs currency check"
elif [ -z "$DOCS_COUNT" ]; then
    warn "Could not parse MEMORY.md test count — docs/MEMORY.md may need updating"
else
    if [ "$LIVE_COUNT" -gt "$DOCS_COUNT" ]; then
        fail "Docs stale: MEMORY.md shows $DOCS_COUNT tests, live count is $LIVE_COUNT"
        fail "Run update_docs_s[N].py before pushing"
        FAILED=1
    elif [ "$LIVE_COUNT" -lt "$DOCS_COUNT" ]; then
        fail "Test regression: MEMORY.md shows $DOCS_COUNT tests, live count is $LIVE_COUNT"
        fail "Tests have been removed or are failing"
        FAILED=1
    else
        pass "Docs current: $LIVE_COUNT tests documented correctly"
    fi
fi

# Check MEMORY.md was modified in the last commit (if code files were changed)
CODE_CHANGED=$(git diff --cached --name-only 2>/dev/null | grep -cE "^src/|^tests/" || true)
DOCS_CHANGED=$(git diff --cached --name-only 2>/dev/null | grep -cE "^docs/" || true)

if [ "$CODE_CHANGED" -gt 0 ] && [ "$DOCS_CHANGED" -eq 0 ]; then
    warn "Code changed but docs/ unchanged — is docs sync included in this commit?"
    warn "If update_docs_s[N].py has been run, ignore this warning."
fi

# ── Result ────────────────────────────────────────────────────────────────────
echo ""
echo "────────────────────────"
if [ $FAILED -eq 0 ]; then
    pass "All checks passed — pushing"
    echo ""
    exit 0
else
    fail "Push blocked — fix errors above"
    echo ""
    echo "  Common fixes:"
    echo "    pytest:  PYTHONPATH=. .venv/bin/pytest tests/ -x --tb=short"
    echo "    ruff:    .venv/bin/ruff check src/ tests/ tools/ --fix"
    echo "    docs:    .venv/bin/python3 update_docs_s[N].py"
    echo ""
    exit 1
fi
