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

### 0e. Trace the DESIGNED architecture path (CRITICAL)

The architecture (ARCHITECTURE.md, PREDICTION_PIPELINE.md) proposes a specific data flow. This section traces that path through actual code to find where it breaks.

**Read FIRST (mandatory before running any grep):**
```
docs/ARCHITECTURE.md          — Convergence Layer → Module Mapping (lines ~82-133)
docs/PREDICTION_PIPELINE.md   — The Three Convergence Layers + 10 Build Layers
```

These documents claim a specific wiring:
- corpus rules → rule_firing.py → inference.py → scoring_v3.py → API/UI
- Layer I concordance computed across Parashari/KP/Jaimini schools
- Layer II promise/capacity/delivery gates activation timing
- Layer III empirical feedback calibrates Layer I weights

Now trace each link in the chain. For each, answer: EXISTS / BROKEN / NOT BUILT.

```bash
# ── LINK 1: Corpus → rule_firing.py ──────────────────────────────────────────
# Does rule_firing.py load and fire corpus rules against a chart?
grep -n 'build_corpus\|combined_corpus\|evaluate_chart\|fire_rules\|def evaluate' src/calculations/rule_firing.py | head -15
# READ rule_firing.py:evaluate_chart() — what does it do? Does it return fired rules?

# ── LINK 2: rule_firing.py → inference.py ────────────────────────────────────
# Does inference.py import and call rule_firing?
grep -n 'rule_firing\|evaluate_chart\|FiredRule' src/calculations/inference.py | head -15
# READ inference.py:aggregate_domains() — what does it produce?

# ── LINK 3: inference.py → scoring pipeline (THE BREAK POINT?) ──────────────
# Does scoring.py use inference or rule_firing?
grep -rn 'corpus\|rule_firing\|inference\|build_corpus\|FiredRule' src/scoring.py
# Does multi_axis_scoring.py use inference or rule_firing?
grep -rn 'corpus\|rule_firing\|inference\|build_corpus\|FiredRule' src/calculations/multi_axis_scoring.py
# Does scoring_v3.py use inference or rule_firing?
grep -rn 'corpus\|rule_firing\|inference\|build_corpus\|FiredRule' src/calculations/scoring_v3.py
# WHO calls inference.py in production?
grep -rn 'from src.calculations.inference\|import.*inference' src/ --include='*.py' | grep -v __pycache__ | grep -v inference.py | grep -v test

# ── LINK 4: Concordance computation ─────────────────────────────────────────
# ARCHITECTURE.md says Layer I produces concordance scores across schools.
# PREDICTION_PIPELINE.md says concordance < 0.35 = SUPPRESS (anti-prediction zone).
# Is concordance_score computed? Populated? Used in any scoring path?
grep -rn 'concordance_score\|concordance_weight\|anti.prediction\|concordance.*0\.35' src/ --include='*.py' | grep -v __pycache__
# Is there a school_concordance field in HouseScore or any output dataclass?
grep -rn 'school_concordance\|multi_school\|concordance' src/scoring.py src/calculations/scoring_v3.py src/calculations/multi_axis_scoring.py src/calculations/lpi.py

# ── LINK 5: Layer II Promise/Capacity/Delivery ──────────────────────────────
# ARCHITECTURE.md maps promise_engine.py L1=promise_present, L2=capacity, L3=delivery
# Is promise_engine called by any scoring path?
grep -rn 'promise_engine\|compute_promise\|compute_house_promise\|compute_full_promise' src/scoring.py src/calculations/scoring_v3.py src/calculations/multi_axis_scoring.py
# WHO calls promise_engine in production?
grep -rn 'from src.calculations.promise_engine' src/ --include='*.py' | grep -v __pycache__ | grep -v test | grep -v promise_engine.py

# ── LINK 6: Layer III feedback loop ──────────────────────────────────────────
grep -rn 'feedback\|bayesian_update\|empirical.*update\|posterior.*update\|user_prior_prob' src/ --include='*.py' | grep -v __pycache__ | grep -v test

# ── LINK 7: What scoring.py ACTUALLY does ───────────────────────────────────
# Read the 22 hardcoded rules:
grep -n 'def score_chart\|def score_house\|R01\|R02\|R03' src/scoring.py | head -20
# This is the ACTUAL scoring engine. Compare to what ARCHITECTURE.md claims.

# ── LINK 8: What scoring_v3 ACTUALLY does ───────────────────────────────────
# Read the imports — what modules does it orchestrate?
grep -n 'from src\.\|import src\.' src/calculations/scoring_v3.py | head -20
# Compare this list to the ARCHITECTURE.md Layer I module mapping.
# Which Layer I modules are LISTED but NOT IMPORTED?
# Which Layer II modules are LISTED but NOT IMPORTED?
```

**For each link, produce a verdict table:**

| Link | Architecture says | Code shows | Status |
|------|-------------------|-----------|--------|
| 1. Corpus → rule_firing | rule_firing loads corpus and fires rules | ? | EXISTS / BROKEN / NOT BUILT |
| 2. rule_firing → inference | inference calls evaluate_chart | ? | EXISTS / BROKEN / NOT BUILT |
| 3. inference → scoring | scoring_v3 uses inference output | ? | EXISTS / BROKEN / NOT BUILT |
| 4. Concordance scoring | Multi-school concordance computed | ? | EXISTS / BROKEN / NOT BUILT |
| 5. Promise/Capacity/Delivery | promise_engine feeds scoring | ? | EXISTS / BROKEN / NOT BUILT |
| 6. Empirical feedback | Layer III calibrates Layer I | ? | EXISTS / BROKEN / NOT BUILT |
| 7. Hardcoded vs corpus | scoring.py uses corpus rules | ? | HARDCODED / CORPUS / HYBRID |

**This table is the single most important output of the entire assessment.** It tells you exactly where the architecture broke down and what the minimal fix is.

### 0f. v11 Execution Plan stage status (THE CURRENT PLAN)

The v11 execution plan (`docs/superpowers/specs/2026-04-07-v11-execution-plan.md`) has 8 stages with a status table at the top. But that table was last updated S324. Verify each stage's CLAIMED status against actual code:

```bash
# Stage 1: Fix wrong formulas (claimed ~95%)
# Check: are Mars aspects fixed? Is Cancer yogakaraka fixed?
grep -n 'Mars.*3.*7\|3, 7' src/calculations/sputa_drishti.py | head -3
grep -n 'Cancer\|yogakaraka' src/scoring.py | head -3

# Stage 2: Tag verification levels (claimed partial)
grep -rL "_VERIFICATION" src/calculations/*.py 2>/dev/null | wc -l  # files WITHOUT tags

# Stage 3: Module registry + enforcer (claimed DONE)
ls -la src/MODULE_REGISTRY.py tools/import_boundary_check.py 2>/dev/null

# Stage 4: Silent exception handlers (claimed ~84%)
# You already measured this in Phase 0h

# Stage 5: Consolidate to canonical primitives (claimed DONE)
PYTHONPATH=. .venv/bin/python tools/validate_constants.py

# Stage 6: Delete dead code (claimed ~10%)
# You already measured this via reachability analysis

# Stage 7: Wire missing connections (claimed DONE)
# CRITICAL: v11 says "R24 dignity wiring" and "score_all_axes deprecated"
grep -n 'R24\|dignity' src/scoring.py | head -5
grep -n 'DeprecationWarning\|deprecated' src/calculations/multi_axis_scoring.py | head -3

# Stage 8: Runtime invariant checker (claimed DONE)
ls -la src/invariants.py 2>/dev/null
grep -n 'check_chart_invariants\|invariants' src/ephemeris.py | head -3
```

Produce a verified stage status table:

| Stage | v11 claims | Actual code shows | Verified status |
|-------|-----------|-------------------|----------------|
| 1. Fix formulas | ~95% | ? | ? |
| 2. Verification tags | Partial | ? | ? |
| ... | ... | ... | ... |

### 0f-b. v11 20-criteria self-score verification

v11 self-scored 55/100. For the 5 criteria the plan scored lowest (2/5), verify:

```bash
# Criterion 5 (Prediction Quality, scored 2/5): Does dignity affect house scores?
grep -n 'dignity\|R24' src/scoring.py | head -10

# Criterion 12 (Observability, scored 2/5): Is DEBUG logging in canonical primitives?
grep -rn 'logger.debug' src/calculations/house_lord.py src/calculations/dignity.py src/calculations/shadbala.py | wc -l

# Criterion 19 (Versioning, scored 2/5): Is corpus_version tracked?
grep -rn 'corpus_version\|ENGINE_VERSION' src/ --include='*.py' | grep -v __pycache__ | head -5

# Criterion 20 (Runtime Correctness, scored 2/5): Does invariant checker run?
grep -rn 'check_chart_invariants\|validate_chart' src/ephemeris.py src/scoring.py | head -5

# Criterion 8 (Evolvability, scored 2/5): Do ADDING_A_TEXT.md and ADDING_A_SCHOOL.md exist?
ls docs/ADDING_A_TEXT.md docs/ADDING_A_SCHOOL.md 2>/dev/null
```

Update the 20-criteria score based on what the code shows NOW (post-surgery, post S324).

### 0f-c. Reconcile the TWO architecture documents

There are TWO architectures documented:
1. **ARCHITECTURE.md + PREDICTION_PIPELINE.md**: 3 convergence layers, 10 build layers, anti-prediction zone, Bayesian posteriors
2. **v11 spec**: 5-layer pipeline, canonical primitives model, C→A→B phasing, 20 quality criteria

Questions to answer:
- Are these complementary (v11 = implementation strategy for the convergence model)?
- Or contradictory (v11 replaces the convergence model)?
- Does v11's 5-layer pipeline map to the 3-convergence-layer model? If so, how?
- v11 says Phase C needs exactly 3 things: canonical primitives, a rule engine, validation gates. Does the current codebase have all 3?
- The convergence model talks about concordance scoring, anti-prediction zones, Bayesian posteriors. v11 says these are Phase A/B concerns. Which framing is correct for deciding NEXT STEPS?

**This reconciliation determines whether the assessment follows v11's roadmap or the convergence model's roadmap. They may prescribe different next steps.**

### 0f-d. The older 10-layer build status (PREDICTION_PIPELINE.md)

After reading PREDICTION_PIPELINE.md, check each of the 10 build layers. But note: v11 may explicitly defer some of these to Phase A/B.

```bash
# L1: Birth time sensitivity
grep -rn 'confidence_model\|birth_time_sensitivity' src/calculations/scoring_v3.py src/scoring.py

# L2: 20Q personality verification
find src/ -name '*personality*' -o -name '*20q*' -o -name '*verification_protocol*' 2>/dev/null

# L3: Conditional weight functions
grep -rn 'conditional_weights\|W(' src/calculations/multi_axis_scoring.py | head -5

# L4: Multi-school concordance
grep -rn 'concordance\|school_concordance\|multi_school' src/calculations/scoring_v3.py src/calculations/lpi.py

# L5: Bayesian posterior distributions
grep -rn 'posterior\|bayesian\|HouseScore.*std\|HouseScore.*p10' src/ --include='*.py' | grep -v test | grep -v __pycache__

# L6: Dasha temporal model
grep -rn 'dasha_scoring\|apply_dasha_scoring' src/calculations/scoring_v3.py

# L7-L10: All Phase 3+ (expected NOT BUILT)
echo "L7-L10: Phase 3+ — expected not built yet"
```

Produce a 10-row status table: BUILT+WIRED / BUILT+UNWIRED / NOT BUILT

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

### 0j. Document sprawl audit

The project has 10+ overlapping documents. Before reading them, map the contradictions:

```bash
# Two MEMORY.md files — which is current?
echo "Root MEMORY.md: $(wc -l < MEMORY.md) lines, last modified: $(stat -f %Sm MEMORY.md)"
echo "docs/MEMORY.md: $(wc -l < docs/MEMORY.md) lines, last modified: $(stat -f %Sm docs/MEMORY.md)"

# Two CHANGELOG.md files
echo "Root CHANGELOG.md: $(wc -l < CHANGELOG.md) lines"
echo "docs/CHANGELOG.md: $(wc -l < docs/CHANGELOG.md) lines"

# Two rule contracts
echo "RULE_CONTRACT_V2.md: $(wc -l < docs/RULE_CONTRACT_V2.md) lines"
echo "PHASE1B_RULE_CONTRACT.md: $(wc -l < docs/PHASE1B_RULE_CONTRACT.md) lines"
diff <(grep "^#" docs/RULE_CONTRACT_V2.md) <(grep "^#" docs/PHASE1B_RULE_CONTRACT.md) 2>/dev/null | head -20

# Two architecture documents (ARCHITECTURE.md vs v11)
echo "ARCHITECTURE.md: $(wc -l < docs/ARCHITECTURE.md) lines"
echo "v11: $(wc -l < docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md) lines"

# ENCODING_PROTOCOL_V2 vs CLAUDE.md encoding section
echo "ENCODING_PROTOCOL_V2.md: $(wc -l < docs/ENCODING_PROTOCOL_V2.md) lines"

# Total doc count
find . -name "*.md" -not -path "./.venv/*" -not -path "./.git/*" -not -path "./.claude/worktrees/*" -not -path "./.pytest_cache/*" | wc -l
```

For PROJECT_STRATEGY.md to be the golden source, you need to know WHICH documents it replaces and WHERE they contradict each other. This audit is the input for Section 2 (architecture reconciliation).

---

## Phase 1: Read the strategic documents

Read EVERY ONE of these. Do not skim. Do not paraphrase from memory.

**IMPORTANT: There are ~35 potentially relevant documents. You MUST read all of them listed below. The document sprawl IS the problem this session solves — you cannot consolidate what you haven't read.**

| Document | What to extract |
|----------|----------------|
| `docs/ROADMAP.md` | Phase structure, session targets, gate criteria, current phase |
| `docs/ARCHITECTURE.md` | OLDER architecture: 3-layer convergence model, Layer→Module mapping, "critical architectural principle" at line ~127. Note: may be SUPERSEDED by v11. |
| `docs/PREDICTION_PIPELINE.md` | OLDER pipeline: 10 build layers, 3 convergence layers, anti-prediction zone. Note: may be SUPERSEDED by v11. |
| `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md` | **THE LATEST ARCHITECTURE.** 5-layer pipeline (Astronomy→Conventions→Derived Facts→Rule Evaluation→Aggregation). C→A→B phasing. Phase -1 with 8 stages. Canonical primitives model. 20 quality criteria with honest 55/100 self-score. READ THIS ENTIRE FILE. |
| `docs/superpowers/specs/2026-04-07-v11-execution-plan.md` | **THE LATEST EXECUTION PLAN.** Stage-by-stage contracts with status table. Shows which stages are DONE/PARTIAL/NOT STARTED. Stage 7 scoring resolution. Testing strategy. READ THIS ENTIRE FILE. |
| `docs/GUARDRAILS.md` | All 24 guardrails, their status, which have code enforcement |
| `docs/RULE_CONTRACT_V2.md` | Encoding schema — what makes a rule "V2 compliant" |
| `docs/PHASE1B_RULE_CONTRACT.md` | **SEPARATE from above.** Phase 1B-specific rule contract. Note overlap/contradictions with RULE_CONTRACT_V2.md. |
| `docs/ENCODING_GRANULARITY.md` | What constitutes one rule — granularity definition |
| `docs/ENCODING_PROTOCOL_V2.md` | V2 encoding protocol — overlaps with CLAUDE.md encoding section? |
| `docs/CORPUS_MANIFEST.json` | Parse the JSON — rule count per source text, per chapter |
| `docs/CLASSICAL_CORPUS.md` | **CRITICAL.** Phase 1A vs 1B distinction. The 5.7x undershooting finding. Real corpus state. What "7,466 rules" actually means. |
| `docs/BPHS_ENCODING_ROADMAP.md` | BPHS-specific encoding plan and chapter priorities |
| `docs/coverage_maps/bphs.md` | Which BPHS chapters are encoded vs not — the ground truth on encoding progress |
| `docs/coverage_maps/saravali.md` | Saravali encoding coverage |
| `docs/coverage_maps/laghu_parashari.md` | Laghu Parashari encoding coverage |
| `docs/coverage_maps/bhavartha_ratnakara.md` | Bhavartha Ratnakara encoding coverage |
| `docs/s318_deep_audit.md` | **CRITICAL (1241 lines).** THE master bug list. C01-C20 bugs, H01-H12 handler categories, dead code inventory. v11's Phase -1 is built on this. Read to verify what's been fixed vs what remains. |
| `docs/s317_full_audit.md` | Earlier audit (read S318 references to understand what S317 found vs missed) |
| `docs/BUGS.md` | Open bug tracker — are any still open? |
| `docs/PHASE1B_CONCORDANCE_WORKFLOW.md` | How concordance is supposed to work — critical for Layer I strategy |
| `docs/CROSS_TEXT_GOVERNANCE.md` | Cross-text rules — critical for concordance scoring |
| `docs/KPIS.md` | What metrics exist, what targets, what's measured vs aspirational |
| `docs/GUARDRAILS.md` | All 24 guardrails, their status, which have code enforcement |
| `lessons_learned.md` | Every lesson (L001-L018+), which have controls, which are behavioral-only |
| `core_principles.md` | The 10+ governing principles — are they reflected in code? |
| `docs/MEMORY.md` | State tracker #1. Note: there is ALSO a root-level `MEMORY.md` (261 lines) — read both, note contradictions |
| `MEMORY.md` | State tracker #2 (root level). Compare to `docs/MEMORY.md` for drift. |
| `docs/CHANGELOG.md` | Last 10-15 session entries — what was actually done recently. Note: there is ALSO a root-level `CHANGELOG.md`. |
| `CHANGELOG.md` | Root-level changelog. Compare to `docs/CHANGELOG.md` for drift. |
| `tools/INDEX.md` | Tool inventory — what exists, prevents rebuilding |
| `docs/PHASE1B_OUTCOME_TAXONOMY.md` | Prediction type definitions for encoding. Critical for understanding what the corpus encodes. |
| `docs/s318_consolidation_plan.md` | The consolidation plan that v11 Stage 5 implements |
| `docs/s317_baseline.md` | Baseline measurements before S317-S324 fixes |
| `docs/DATA_GOVERNANCE_FRAMEWORK.md` | Data handling decisions (714 lines) — feeds into guardrails |
| `docs/shadbala_audit_gaps.md` | Open gaps in Shadbala (a key canonical module) |
| `docs/SESSION_LOG.md` | Session history (739 lines) — shows actual work pattern over time |
| `AUDIT.md` | Root-level audit doc |
| `docs/AUDIT_S305.md` | S305 audit — earlier audit baseline |
| `PLAN.md` | Current plan state (if any) |
| `DOCS.md` | Canonical API reference (672 lines). ARCHITECTURE.md references this. |
| `CLAUDE.md` | Session protocol, encoding protocol, project context. This is what every session reads FIRST. The golden source must align with or replace relevant sections. |
| `.claude/memory/MEMORY.md` | Auto-memory index — persistent cross-session memory entries |
| `.claude/memory/feedback_*.md` | All feedback memories — user preferences and corrections. Read each one. |
| `.claude/memory/project_*.md` | All project memories — decisions and findings. Read each one. |
| `src/scoring.py` | Read the ACTUAL scoring logic — what 22 rules does it apply? What data does it consume? |
| `src/calculations/multi_axis_scoring.py` | Read the extended scorer — what modules does it orchestrate? Compare to ARCHITECTURE.md Layer I list |
| `src/calculations/scoring_v3.py` | Read the v3 orchestrator — its imports ARE the actual Layer I. Compare to designed Layer I |
| `src/calculations/rule_firing.py` | Read the corpus→engine bridge — does evaluate_chart() work? What does it return? |
| `src/calculations/inference.py` | Read the inference engine — does aggregate_domains() produce something scoring could consume? |
| `src/calculations/promise_engine.py` | Read Layer II — does it compute Promise/Capacity/Delivery? Who calls it? |
| `src/calculations/lpi.py` | Read the 7-layer LPI — does it include concordance? Compare to PREDICTION_PIPELINE Layer 4 |

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

### B. Architecture-to-implementation gap (THE critical dimension)

**Two architecture documents exist. You must reconcile them first (Phase 0f-c).**

v11 says Phase C needs exactly 3 things:
1. Canonical primitives (one implementation per concept, BPHS-verified)
2. A rule engine that evaluates encoded rules against charts
3. Validation gates that prevent encoding errors

Use the Phase 0e link-tracing table AND the Phase 0f stage status table. For each designed component:
- Does it exist in code?
- Is it wired into the production path?
- If broken, WHERE exactly does it break?
- What is the MINIMAL fix?

Then: does the PREDICTION_PIPELINE.md convergence model add requirements beyond v11's 3 things? If so, are those requirements Phase C or Phase A/B? This determines whether concordance scoring, anti-prediction zones, and Bayesian posteriors are prerequisites for the next step or future work.

### C. Convergence layer status (measured against PREDICTION_PIPELINE.md)
For each of the 3 convergence layers AND each of the 10 build layers:
- Does the module exist?
- Is it wired into the scoring pipeline that produces user-visible output?
- If unwired, what is the designed consumer (per ARCHITECTURE.md)?
- What would wiring it require?

**Do not conflate "module exists" with "module is wired."** A module that passes tests but isn't called by the scoring path produces zero product value.

### D. The scoring engine's actual decision surface
- scoring.py uses 22 hardcoded rules (R01-R22). Read them. What do they evaluate?
- multi_axis_scoring.py extends this with school gates and penalties. What additional signals?
- scoring_v3.py orchestrates multi-axis + LPI + avasthas. What's its full input set?
- **How does THIS compare to what the architecture says Layer I should do?**
- **What signals does the architecture claim but the engine doesn't compute?**
- This gap between "what the engine evaluates" and "what the architecture designs" is the actionable finding. Size it: how many missing signals? How complex to add?

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

Use the Phase 0e link-tracing table to inform which candidates are viable.

1. **Resume BPHS encoding** (Ch.24+ → more L3 rules)
   - But: trace Link 3. If inference/rule_firing output doesn't reach scoring, more rules are inert data.

2. **Re-encode 6,807 L1 rules to L3** (make existing rules computable)
   - But: computable by rule_firing. If Link 3 is broken, computable rules still don't score.

3. **Close the broken links in the architecture chain** (restore the designed path)
   - Use the 0e table. For each BROKEN link, estimate the fix. This may be the ONLY candidate that makes all other candidates productive.
   - But: how much of the chain exists? Is it 1 missing import or a 2000-line rewrite?

4. **Build concordance scoring** (Layer I / Build Layer 4 completion)
   - PREDICTION_PIPELINE.md says concordance < 0.35 = SUPPRESS. This is the anti-prediction zone.
   - But: concordance requires multiple texts encoding the same verse. How many cross-text overlaps exist in the current 654 V2 rules? If zero, concordance is uncomputable regardless.

5. **Run OB-3 calibration** (empirical signal measurement)
   - But: OB-3 measures whatever scoring.py computes. If that's 22 hardcoded rules, OB-3 tests those 22 rules, not the corpus. Running OB-3 AFTER wiring the corpus would measure something different.

6. **Implement missing guardrails G01-G05** (consumer safety)
   - But: guardrails gate consumer output. If the scoring engine doesn't use the corpus, consumer output is based on 22 rules regardless. Safety of what?

7. **Wire corpus into scoring AND THEN encode** ("connect then fill")
   - Close the broken links first. Then every encoding session produces measurable score changes. This is the architecture's designed operating mode.
   - But: is the bridge (rule_firing → inference → scoring) validated? Does it produce sensible scores?

8. **Validate 654 V2 rules end-to-end** (fire them, verify scores change)
   - Smallest possible proof-of-concept: wire the bridge, fire 654 rules against India 1947 fixture, compare scores to hardcoded baseline. If scores improve, the architecture works. If they don't, encoding more rules is the wrong strategy.
   - This is the cheapest experiment that resolves the strategic question.

9. **Something the diagnostics reveal that nobody anticipated**
   - The 0e table may show that some links are ALREADY CONNECTED but just not called from the right entry point. That changes the estimate dramatically.

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

## Output: THE deliverable

The diagnostic findings (Phases 0-4) are intermediate work. The DELIVERABLE is a single document that replaces the current document sprawl.

### The problem this session solves

There are currently 10+ documents that partially describe the project state, architecture, and next steps:
- `docs/ARCHITECTURE.md` (older 3-layer convergence model)
- `docs/PREDICTION_PIPELINE.md` (older 10-layer build model)
- `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md` (latest architecture)
- `docs/superpowers/specs/2026-04-07-v11-execution-plan.md` (latest execution plan)
- `docs/ROADMAP.md` (legacy session-based roadmap)
- `docs/GUARDRAILS.md` (24 guardrails)
- `docs/RULE_CONTRACT_V2.md` (encoding schema)
- `docs/ENCODING_GRANULARITY.md` (rule definition)
- `docs/MEMORY.md` (state tracker)
- `lessons_learned.md` (18+ lessons)
- `core_principles.md` (10+ principles)

A new session reads 3 of these and misses the 4th that has the actual answer. They overlap, contradict, and none is authoritative. The following session starts from scratch reading stale documents.

### What you will produce: `docs/PROJECT_STRATEGY.md`

One document. The golden source. Every subsequent session reads THIS instead of 10 partial documents. It contains:

**Section 1: Where we are (diagnostic facts, dated)**

A dashboard table with every metric from Phase 0. Updated by subsequent sessions when diagnostics are re-run. Includes:
- Test count, lint status, reachability, silent handlers
- Corpus maturity (L0-L5 distribution, V2 completeness)
- Architecture link status (the 7-link chain verdict table from Phase 0e)
- v11 stage status (the 8-stage verified table from Phase 0f)
- v11 20-criteria score (updated from 55/100 to current actual)
- Date of last verification for each metric

**Section 2: What the system is (architecture, ONE version)**

Reconcile v11 and the convergence model into ONE coherent description:
- The 5-layer pipeline (v11) — what each layer does
- How the 3 convergence layers (PREDICTION_PIPELINE) map onto the 5 layers
- Which parts are Phase C (now) vs Phase A/B (later) — DECIDED, not debated
- The canonical primitives model — the list, their sources, their verification status
- The scoring engine — what it actually evaluates today, what it's designed to evaluate

This section REPLACES: ARCHITECTURE.md, PREDICTION_PIPELINE.md, the v11 spec's architecture sections.

**Section 3: What the system needs (the work, prioritized)**

Not a 1000-session roadmap. A prioritized list of concrete work items, each with:
- What it is (1 sentence)
- Why it matters (what breaks or stays broken without it)
- What it depends on (prerequisites)
- What it unblocks (what becomes possible after)
- Estimated effort (sessions, not hours)
- Status (NOT STARTED / IN PROGRESS / DONE)

This section REPLACES: ROADMAP.md session tables, v11 execution plan stages, the various "next steps" scattered across docs.

**Section 4: How to do the work (process, ONE version)**

- The encoding protocol (from CLAUDE.md, consolidated)
- The 5 gates
- The session start/end protocol
- Quality standards (from core_principles + lessons_learned, deduplicated)
- What tools to run and when

This section REPLACES: the encoding protocol in CLAUDE.md (which references this section instead of duplicating it), lessons_learned process entries, core_principles process entries.

**Section 5: What to watch out for (lessons and guardrails, consolidated)**

- Lessons learned (from lessons_learned.md) — kept, but with stale/resolved ones marked
- Guardrails (from GUARDRAILS.md) — kept, with actual enforcement status
- Core principles — kept, with code enforcement cross-references

This section REPLACES: lessons_learned.md as standalone, GUARDRAILS.md as standalone, core_principles.md as standalone. (Those files can remain but point to PROJECT_STRATEGY.md as the golden source.)

**Section 6: What we decided and why (decision log)**

Every strategic decision from the uncomfortable questions (Phase 4), with reasoning:
- Is the 25K target realistic? → DECISION + reasoning
- Are L1 rules useful? → DECISION + reasoning
- Is the corpus connected to the engine? → FINDING + what we're doing about it
- Which architecture model governs? → DECISION + reasoning

This section captures WHY so subsequent sessions don't re-litigate settled questions.

### What you will NOT produce

- A plan with session numbers. Session numbering is an implementation detail.
- A document longer than 1500 lines. If it's longer, it's not consolidated — it's accumulated.
- A document that requires reading other documents to understand. This IS the other document.
- Aspirational descriptions of things that don't exist. Every claim in Sections 1-2 is backed by a diagnostic command that verifies it.

### After writing PROJECT_STRATEGY.md

1. Update CLAUDE.md's "At session START" protocol: replace the 5-file read list with `Read docs/PROJECT_STRATEGY.md`
2. Add a header to each superseded doc pointing to PROJECT_STRATEGY.md as the golden source
3. Do NOT delete the old docs — they have historical value. But they are no longer authoritative.

---

## Ground rules

- **No encoding.** This is a measurement + synthesis session.
- **No new features.** This is a diagnostic + document session.
- **No optimism.** If the picture is bad, say so in PROJECT_STRATEGY.md.
- **No deferral.** Every question gets a DECISION, written into Section 6.
- **Numbers before narratives.** Run the tool, then write.
- **Contradictions are findings.** If MEMORY.md says X and the diagnostic shows Y, PROJECT_STRATEGY.md records Y with evidence.
- **One document to rule them all.** If information exists in PROJECT_STRATEGY.md AND another doc, the other doc is stale. PROJECT_STRATEGY.md wins.
