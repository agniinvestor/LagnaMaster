# Codebase Health Assessment — Full Diagnostic Prompt

## Session type
**Governance** — no encoding, no new features. Pure diagnostic and strategic analysis.

## Purpose

Produce a brutally honest assessment of where this project actually stands — not where the docs say it stands. Juxtapose every diagnostic tool against the canonical architecture, the execution plan, and the accumulated audit history. The output is a decision document: what is the single RIGHT next step.

---

## Phase 0: Run every diagnostic (BEFORE any analysis)

Run ALL of the following. Record exact numbers. Do not interpret until all numbers are collected.

### 0a. Core health

```bash
.venv/bin/pytest tests/ -q --tb=short
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/validate_constants.py
PYTHONPATH=. .venv/bin/python tools/import_boundary_check.py
PYTHONPATH=. .venv/bin/python tools/reachability_analysis.py
```

### 0b. Corpus maturity (the single most important diagnostic)

```bash
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --v2-only   # V2 rules only
PYTHONPATH=. .venv/bin/python tools/v2_scorecard.py --all        # full corpus
PYTHONPATH=. .venv/bin/python tools/rule_grader.py               # L0-L5 distribution
PYTHONPATH=. .venv/bin/python tools/condition_modifier_audit.py   # misclassified flags
```

### 0c. Encoding pipeline quality

```bash
PYTHONPATH=. .venv/bin/python tools/rework_detector.py
find data/verse_audits/ -name '*.json' | wc -l
# For each chapter with a verse audit, check encoded-vs-audited claim count:
for f in data/verse_audits/ch*_audit.json; do
  ch=$(basename "$f" | sed 's/ch\([0-9]*\).*/\1/')
  echo "Ch.$ch: $(python3 -c "import json; d=json.load(open('$f')); print(len(d.get('claims',d.get('verses',[]))))" 2>/dev/null || echo 'parse error') claims"
done
```

### 0d. Cross-validation & empirical signal

```bash
# OB-3 calibration — does the engine produce any real signal?
PYTHONPATH=. .venv/bin/python tools/ob3_calibrate.py --report 2>&1 | head -50

# If ob3 requires data files that don't exist, note it — that's a finding.
```

### 0e. The corpus→engine disconnect probe (CRITICAL)

This is the most important diagnostic. It answers: "Does encoding more rules produce any effect on chart scoring?"

```bash
# 1. Does scoring.py import ANYTHING from src/corpus/?
grep -rn 'corpus\|rule_firing\|build_corpus\|FiredRule' src/scoring.py

# 2. Does multi_axis_scoring.py import ANYTHING from src/corpus/?
grep -rn 'corpus\|rule_firing\|build_corpus\|FiredRule' src/calculations/multi_axis_scoring.py

# 3. Does scoring_v3.py import ANYTHING from src/corpus/?
grep -rn 'corpus\|rule_firing\|build_corpus\|FiredRule' src/calculations/scoring_v3.py

# 4. What DOES rule_firing.py do, and who calls it?
grep -rn 'from src.calculations.rule_firing\|import.*rule_firing' src/ --include='*.py' | grep -v __pycache__ | grep -v rule_firing.py

# 5. Does rule_firing load the corpus and fire rules against a chart?
grep -n 'build_corpus\|combined_corpus\|evaluate_chart' src/calculations/rule_firing.py | head -10

# 6. Is inference.py (which imports rule_firing) called by any scoring path?
grep -rn 'from src.calculations.inference\|import.*inference' src/ --include='*.py' | grep -v __pycache__ | grep -v inference.py

# 7. Is concordance_score computed and USED anywhere?
grep -rn 'concordance_score\|concordance_weight' src/ --include='*.py' | grep -v __pycache__

# 8. What is the actual scoring pipeline?
# Trace: app.py → score_chart() → scoring.py → what rules does it apply?
grep -n 'def score_chart\|def score_house' src/scoring.py | head -5
# Then read scoring.py to see: does it use hardcoded R01-R22 weights or corpus rules?
```

If the answers to #1-#3 are all empty, that means: **the 7,466 encoded rules have zero effect on chart scoring.** Record this finding prominently.

### 0f. Layer implementation check

```bash
# Layer I: Classical Concordance — is concordance COMPUTED?
grep -rn 'concordance' src/ --include='*.py' | grep -v __pycache__ | grep -v 'corpus/' | grep -v 'test'

# Layer II: Structural Activation — is Promise/Capacity/Delivery wired into scoring?
grep -rn 'promise_engine\|compute_promise\|capacity\|delivery' src/scoring.py src/calculations/scoring_v3.py src/calculations/multi_axis_scoring.py

# Layer III: Empirical Convergence — does feedback flow back?
grep -rn 'feedback\|bayesian_update\|empirical.*update' src/ --include='*.py' | grep -v __pycache__ | grep -v test
```

### 0g. Guardrail enforcement audit

```bash
# How many of the 24 guardrails (G01-G24) have CODE enforcement?
# Read docs/GUARDRAILS.md for the list, then for each one:
for g in G01 G02 G03 G04 G05 G06 G07 G08 G09 G10 G11 G12 G13 G14 G15 G16 G17 G18 G19 G20 G21 G22 G23 G24; do
  count=$(grep -rn "$g" src/ tests/ tools/ --include='*.py' 2>/dev/null | grep -v __pycache__ | grep -v '\.md' | wc -l | tr -d ' ')
  echo "$g: $count code references"
done
```

### 0h. Codebase metrics

```bash
find src/ -name "*.py" -not -path "*__pycache__*" | wc -l
find src/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1
find tests/ -name "*.py" -not -path "*__pycache__*" | wc -l
find tests/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1

# Silent handlers
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
```

### 0i. Session velocity and effort distribution

```bash
# How many sessions were encoding vs governance vs surgery?
git log --oneline --all | grep -i 'feat\|encode\|chapter\|ch[0-9]' | wc -l
git log --oneline --all | grep -i 'refactor\|surgery\|governance\|fix\|bug' | wc -l
git log --oneline --all | grep -i 'docs\|plan\|roadmap\|memory\|changelog' | wc -l

# V2 rules produced per encoding session (efficiency metric)
# Count V2 rules: should be in v2_scorecard output
# Count encoding sessions: from git log
```

Record ALL results in a dashboard table before proceeding.

---

## Phase 1: Read the strategic documents

Read EVERY ONE of these. Do not skim. Do not paraphrase from memory.

| Document | What to extract |
|----------|----------------|
| `docs/ROADMAP.md` | Phase structure, session targets, gate criteria, current phase |
| `docs/ARCHITECTURE.md` | 3-layer convergence model, canonical data flow, what's supposed to exist |
| `docs/GUARDRAILS.md` | All 24 guardrails, their status, which have code enforcement |
| `docs/RULE_CONTRACT_V2.md` | The encoding schema — what makes a rule "V2 compliant" |
| `docs/ENCODING_GRANULARITY.md` | What constitutes one rule — granularity definition |
| `docs/CORPUS_MANIFEST.json` | Parse the JSON — rule count per source text, per chapter |
| `lessons_learned.md` | Every lesson (L001-L018+), which have controls, which are behavioral-only |
| `core_principles.md` | The 10+ governing principles — are they reflected in code? |
| `docs/MEMORY.md` | What it claims the current state is |
| `docs/CHANGELOG.md` | Last 10-15 session entries — what was actually done recently |
| `src/scoring.py` | Read the ACTUAL scoring logic — what 22 rules does it apply? |
| `src/calculations/rule_firing.py` | Read the corpus→engine bridge — is it used? |
| `src/calculations/inference.py` | Read the inference engine — is it called? |

For each document, note:
1. What it CLAIMS the current state is
2. Where it CONTRADICTS what the diagnostics show
3. What it implies about next steps

---

## Phase 2: The honest juxtaposition

Produce a comparison table:

| Dimension | Architecture/Roadmap claims | Diagnostics show | Gap | Severity |
|-----------|---------------------------|-------------------|-----|----------|

### A. Corpus depth and utility
- Roadmap targets 25,000 rules. How many exist at L0/L1/L2/L3/L4/L5?
- What percentage are V2-compliant (structured, computable)?
- What is the L1→L3 conversion rate? (How many prose rules became structured?)
- How many source texts have verse audits?
- **KEY: Do any of the 7,466 rules affect chart scoring?** If not, state this clearly.

### B. Engine-corpus connection (THE critical question)
- The scoring engine (scoring.py, multi_axis_scoring.py) uses hardcoded R01-R22 rules.
- The corpus has 7,466 encoded rules in src/corpus/.
- rule_firing.py can fire corpus rules against charts.
- **Is rule_firing.py called by the scoring pipeline? Or is it orphaned?**
- If the scoring engine and the corpus are disconnected, then encoding more rules produces zero effect on the product. State this finding clearly.
- What would it take to connect them?

### C. Convergence layer status
- Layer I (Classical Concordance): Is concordance_score populated? Computed? Used?
- Layer II (Structural Activation): Is promise/capacity/delivery flowing into scoring?
- Layer III (Empirical Convergence): Is any feedback mechanism operational?
- **How many of the 3 layers are actually implemented vs just documented?**

### D. Architecture alignment
- Does the codebase match the canonical architecture in ARCHITECTURE.md?
- How many condition primitives exist vs are used?
- What features does the engine have that the corpus doesn't use?
- What features does the corpus need that the engine doesn't have?

### E. Test reliability
- 14,800+ tests pass. What percentage test production-reachable code?
- Are there test files that test dead or disconnected modules?
- Do tests validate that the scoring engine produces correct scores, or just that functions run without error?
- Is there any test that fires a corpus rule and verifies the score changes?

### F. Governance and process
- Of 24 guardrails, how many have code enforcement?
- Of 18+ lessons learned, how many have code controls?
- Is MEMORY.md accurate against actual state?
- Is the 90% deliverable / 10% meta-work ratio being met?

---

## Phase 3: The strategic question

> **"What is the single most valuable thing to do next, and why is everything else less valuable?"**

Evaluate EACH candidate. For each, state: what it produces, what it depends on, what it enables, what it costs, and the devil's advocate argument against it.

### Candidates

1. **Resume BPHS encoding** (Ch.24+ → more L3 rules)
   - But: do more L3 rules matter if the scoring engine doesn't use them?

2. **Re-encode 6,807 L1 rules to L3** (make existing rules computable)
   - But: computable by what? If rule_firing isn't wired into scoring, computable rules are still inert.

3. **Wire rule_firing.py into scoring_v3** (make corpus rules affect scores)
   - This is the bridge. Without it, encoding is academic. With it, every new rule changes the product.
   - But: does rule_firing work correctly? Has it been validated?

4. **Build concordance scoring** (Layer I completion)
   - But: concordance requires multiple texts to encode the same verse. How many cross-text overlaps exist?

5. **Run OB-3 calibration** (empirical signal measurement)
   - But: if the scoring engine uses 22 hardcoded rules, OB-3 measures those 22 rules, not the corpus.

6. **Implement missing guardrails G01-G05** (consumer safety)
   - But: there are no consumers yet. Safety before product?

7. **Wire corpus rules into scoring** AND THEN encode more rules
   - This is the "connect then fill" strategy. Wire the bridge first, then every encoding session produces measurable product improvement.

8. **Validate the 654 V2 rules end-to-end** (fire them against test charts, verify scores change)
   - Before encoding thousands more, prove the existing 654 actually work when wired.

9. **Something else** — what do the diagnostics reveal?

**Make one recommendation. Defend it with specific numbers from the diagnostics.**

---

## Phase 4: The uncomfortable questions

Answer each honestly. If the answer is unflattering, say so. No hedging.

1. **Is the corpus connected to the engine?**
   The scoring pipeline is: `app.py → score_chart() → scoring.py (22 hardcoded rules)`. The corpus pipeline is: `src/corpus/*.py → 7,466 rules → rule_firing.py → inference.py`. These two pipelines do not intersect. Is this correct? If so, what has 200+ encoding sessions actually produced?

2. **Is the 25,000-rule target meaningful?**
   At ~30 V2 rules/session and 654 V2 rules after ~20 encoding sessions, reaching 25,000 requires ~810 more sessions. But if the scoring engine uses 22 hardcoded rules and ignores the corpus, what does 25,000 achieve? Is the target itself the right goal, or should the goal be "score charts using corpus rules"?

3. **Are the 6,807 L1 (prose) rules useful?**
   They're counted in "7,466 rules encoded" but they have no structured conditions, no signal_groups, no computable form. Does counting them create false confidence about progress?

4. **Are the 3 convergence layers built or just documented?**
   - Layer I: Concordance field exists in rule_firing.py. Is it populated? Is it used by any scoring path?
   - Layer II: promise_engine.py exists. Is it called by scoring_v3?
   - Layer III: No feedback schema exists in production.
   - Score: 0/3 layers operational, 1/3 partially scaffolded?

5. **Is the governance overhead justified?**
   Sessions S309-S324 produced 654 V2 rules but also: lessons_learned.md, core_principles.md, ENCODING_GRANULARITY.md, RULE_CONTRACT_V2.md, 15+ governance tools, 18 lessons, 10 principles. What is the ratio of governance-to-output? Is the project building the cathedral or writing the building code?

6. **What would happen if you deleted src/corpus/ entirely?**
   Would any user-visible behavior change? If score_chart() doesn't use the corpus, the answer may be no. This is the most damning question. If the corpus is a library that no one reads, the priority is clear: build the reader.

7. **Is the session-based approach causing this problem?**
   Each session optimizes for its own deliverable (encode chapter X, build tool Y). But the meta-objective — "make chart scores better using encoded knowledge" — requires someone to wire the pieces together. Has the session structure created islands of correct work that nobody connected?

---

## Output format

### Section 1: Diagnostic Dashboard
All numbers from Phase 0 in a single table. Two rows highlighted:
- **Corpus→Engine connection**: CONNECTED / DISCONNECTED
- **Convergence layers operational**: N/3

### Section 2: Strategic Juxtaposition
The Phase 2 table. Contradictions in bold. Severity rated: CRITICAL / HIGH / MEDIUM / LOW.

### Section 3: The Verdict
One paragraph. What is the RIGHT next step. What is the cost of being wrong. What is the cost of doing nothing.

### Section 4: Uncomfortable Answers
Numbered answers to Phase 4. No more than 3 sentences each. Lead with the answer, then the evidence.

### Section 5: If I'm wrong
State the strongest argument AGAINST your recommendation. What evidence would change your mind?

### Section 6: Completion checklist
1. Every diagnostic run (with exit code or result summary)
2. Every document read (with key finding)
3. What was NOT checked
4. What assumptions this depends on

---

## Ground rules

- **No encoding.** This is a measurement session.
- **No new code.** This is a diagnostic session.
- **No optimism.** If the picture is bad, say so.
- **No deferral.** Every question gets an answer in this session.
- **Numbers before narratives.** Run the tool, then talk.
- **Contradictions are findings.** If MEMORY.md says X and the diagnostic shows Y, that IS the output.
