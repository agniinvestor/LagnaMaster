# Codebase Health Assessment — Full Diagnostic Prompt

## Session type
**Governance** — no encoding, no new features. Pure diagnostic and strategic analysis.

## Purpose

Produce a brutally honest assessment of the LagnaMaster codebase as it stands today, juxtaposed against the canonical architecture, the execution plan, the legacy roadmap, and the accumulated audit history. The output is a decision document: what is the RIGHT next step — not the easiest, not the most convenient, not the expedient.

---

## Phase 0: Run every diagnostic tool (BEFORE any analysis)

Run ALL of the following. Record exact numbers. Do not interpret until all numbers are collected.

```bash
# ── Core health ──────────────────────────────────────────────────────────────
.venv/bin/pytest tests/ -q --tb=short                    # test count, failures, skips
.venv/bin/ruff check src/ tests/                          # lint violations
PYTHONPATH=. .venv/bin/python tools/validate_constants.py  # constant duplication
PYTHONPATH=. .venv/bin/python tools/import_boundary_check.py  # layer violations
PYTHONPATH=. .venv/bin/python tools/reachability_analysis.py  # unreachable files

# ── Corpus maturity ──────────────────────────────────────────────────────────
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only  # V2 quality (S310+ rules)
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --all      # full corpus quality
PYTHONPATH=. .venv/bin/python tools/rule_grader.py             # L0-L5 maturity distribution
PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py  # misclassified conditions/modifiers

# ── Encoding quality ─────────────────────────────────────────────────────────
PYTHONPATH=. .venv/bin/python tools/rework_detector.py         # rework patterns in git
find data/verse_audits/ -name '*.json' | wc -l                 # verse audit coverage

# ── Silent handler count ─────────────────────────────────────────────────────
# (use the Python script from codebase-surgery, not grep)
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
find src/ -name "*.py" -not -path "*__pycache__*" | wc -l       # src file count
find src/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1  # src line count
find tests/ -name "*.py" -not -path "*__pycache__*" | wc -l     # test file count
```

Record ALL results in a table before proceeding to analysis.

---

## Phase 1: Read the strategic documents

Read EVERY ONE of these files. Do not skim. Do not summarize from memory.

```
docs/ROADMAP.md              — the execution plan and phase gates
docs/ARCHITECTURE.md         — canonical architecture and convergence layers
docs/GUARDRAILS.md           — safety and compliance requirements
docs/RULE_CONTRACT_V2.md     — the encoding schema
docs/ENCODING_GRANULARITY.md — what constitutes one rule
docs/CORPUS_MANIFEST.json    — corpus inventory (parse the JSON)
lessons_learned.md           — every lesson from S309-S324
core_principles.md           — governing principles
docs/MEMORY.md               — current state as recorded
docs/CHANGELOG.md            — recent session history (last 10 entries)
```

For each document, extract:
1. What it CLAIMS the current state is
2. What it CLAIMS the next step is
3. Where it CONTRADICTS what the diagnostics show

---

## Phase 2: The honest juxtaposition

Produce a comparison table with these columns:

| Dimension | What the architecture says | What the roadmap says | What the diagnostics show | Gap |
|-----------|---------------------------|----------------------|---------------------------|-----|

Cover at MINIMUM these dimensions:

### A. Corpus depth
- How many rules does the roadmap target?
- How many exist at each maturity level (L0-L5)?
- What percentage are V2-compliant (structured, computable)?
- What is the L1→L3 conversion rate (prose→structured)?
- How many source texts have verse audits?
- What is the condition/modifier audit flag count?

### B. Engine capability
- How many condition primitives does the engine support?
- How many of those are actually used by V2 rules?
- What is the computable rule percentage?
- Does scoring_v3 actually USE the corpus rules, or does it use hardcoded logic?
- Is there a gap between the scoring engine's capabilities and the corpus's demands?

### C. Architecture alignment
- Does the codebase match the 3-layer convergence model?
- Is Layer I (Classical Concordance) wired and scoring?
- Is Layer II (Structural Activation) wired?
- Is Layer III (Empirical Convergence) scaffolded?
- How many of the 24 guardrails are actually enforced in code?

### D. Test reliability
- What percentage of tests actually test production-reachable code?
- Are there test files that don't correspond to any current module?
- What is the test-to-code ratio?
- Do tests validate BEHAVIOR or just EXISTENCE (i.e., "it runs without error")?

### E. Technical debt
- Silent exception handlers (count and distribution)
- Dead code (unreachable files, unused functions)
- Duplicate functionality (same calculation in multiple places)
- Import boundary violations
- Files without any production consumer

### F. Governance compliance
- Are lessons_learned entries current?
- Are all core_principles reflected in code controls?
- Is every lesson backed by a control?
- How many lessons are behavioral-only (no code enforcement)?
- Is MEMORY.md accurate against actual state?

---

## Phase 3: The strategic question

Answer this question explicitly, with evidence:

> **"What is the single most valuable thing to do next, and why is everything else less valuable?"**

Evaluate these candidates (and any others the diagnostics suggest):

1. **Resume BPHS encoding** (Ch.24+ → L3 rules) — deepens the corpus
2. **Re-encode L1 rules to L3** (6,807 prose rules → structured) — makes existing rules computable
3. **Build concordance scoring** — enables cross-text verification (Layer I gate)
4. **Implement missing guardrails** (G01-G05) — consumer safety
5. **Empirical calibration** (OB-3 rerun) — validates the engine produces signal
6. **More codebase surgery** — clean up remaining tech debt
7. **Wire corpus rules into the scoring engine** ��� make encoded rules actually score charts
8. **Build Layer II (Structural Activation)** — Promise/Capacity/Delivery pipeline
9. **Something else entirely** — what do the diagnostics reveal that nobody's been looking at?

For EACH candidate, state:
- What it produces (measurable output)
- What it depends on (prerequisites)
- What it enables (what becomes possible after)
- What it costs (sessions, complexity)
- Why it's NOT the right next step (devil's advocate)

Then make the call. One recommendation. Defended with evidence.

---

## Phase 4: The uncomfortable questions

Answer these honestly. If the answer is unflattering, say so.

1. **Is the 25,000-rule target realistic?** The current pace is ~30 V2 rules/session. At 654 V2 rules after ~20 encoding sessions, reaching 25,000 requires ~810 more sessions. Is this the right architecture, or should the approach change?

2. **Are the 6,807 L1 (prose) rules actually useful?** They're counted in "7,466 rules encoded" but they're not computable. Does counting them create false confidence?

3. **Does the scoring engine actually use the corpus?** Or does it use hardcoded rules in scoring.py/multi_axis_scoring.py that were written before the corpus existed? If the corpus and the engine are disconnected, what exactly does encoding more rules achieve?

4. **Is the 3-layer convergence model being built, or just documented?** Check: is concordance_score computed anywhere? Is Layer II promise/capacity/delivery wired? Is Layer III feedback captured?

5. **What would a new contributor need to understand to be productive?** If the answer takes more than 10 minutes to explain, the architecture may have become its own enemy.

---

## Output format

### Section 1: Diagnostic Dashboard
All numbers from Phase 0, in a single table. No prose.

### Section 2: Strategic Juxtaposition
The comparison table from Phase 2. Show contradictions in bold.

### Section 3: The Verdict
One paragraph: what is the RIGHT next step and why. Include the cost of being wrong.

### Section 4: Uncomfortable Answers
Honest answers to Phase 4 questions. No hedging.

### Section 5: Completion checklist
1. What specific diagnostics were run? (list each with exit code)
2. What documents were read? (list each)
3. What was NOT checked?
4. What assumptions does this assessment depend on?

---

## What this assessment is NOT

- Not a plan. Plans are hypotheses. This is a measurement.
- Not a defense of past decisions. Past work is sunk cost.
- Not an encoding session. Zero rules should be encoded.
- Not a feature session. Zero code should be written.
- Not a therapy session for technical debt feelings. Numbers, not narratives.

The only output is: where are we, where should we be, and what is the single next right thing.
