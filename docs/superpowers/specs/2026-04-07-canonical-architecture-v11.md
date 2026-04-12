# LagnaMaster Canonical Architecture — v11

**Date:** 2026-04-07 (S318)
**Status:** Architecture specification — Phase -1 partially executed (S317-S323)
**Supersedes:** v10 (migration plan), v9 (graph schema)
**Score target:** 100/100 on 20-criteria review

> **Implementation status (2026-04-12 S323 audit):**
> - Stage 5 (consolidation) COMPLETE — `src/data/constants.py` golden source, 79 files refactored
> - Stage 1 (formula fixes) ~75% done — 12/16 critical bugs fixed, scoring_v2 + avastha deleted
> - Stage 6 (dead code) ~6% done — 5 modules deleted (1,392 lines of 22,692)
> - Stages 2, 3, 4, 7, 8 not started
> - Net effect: -1,830 lines, 14,806 tests passing, ruff clean

---

## Part 1: Purpose and Phasing (C -> A -> B)

### What LagnaMaster Is

A machine-readable encoding of classical Jyotish texts that can be queried computationally. Not a horoscope generator. Not an AI prediction engine. A corpus of 6,500+ rules from BPHS, Phaladeepika, Saravali, and Brihat Jataka, with a computation engine that evaluates them against birth charts, and a research layer that measures how well they predict real outcomes.

### Why C -> A -> B, Not Simultaneous

Each phase creates the precondition for the next. Without a correct corpus (C), practitioner queries return wrong answers. Without practitioner queries producing traced predictions (A), there is no research data to calibrate against. Building B before A is validated produces "garbage in, statistics out."

**Phase C — Knowledge System (the current phase, sessions S1-S800+)**

The deliverable is the corpus itself: every verse from every supported text, encoded as structured rules with verse citations, validated against PDF source material, with one canonical implementation per classical concept. The corpus is measured by completeness (% of verses encoded), correctness (% matching BPHS PDF), and computability (% of rules that can fire against a chart).

Exit criterion: >= 90% of BPHS Vol 1+2 verses encoded as computable V2 rules. Zero known factual errors. Every rule traces to a specific verse.

**Phase A — Practitioner Tool (sessions S800-S1400)**

The deliverable is a query interface: an astrologer provides a birth chart and a question ("what about my career?"), and the system returns predictions with verse citations, confidence levels, and school attributions. The astrologer can verify each prediction against the source text.

Exit criterion: An astrologer can reproduce any prediction by following the cited verses manually and arriving at the same conclusion.

**Phase B — Research Platform (sessions S1400-S2000+)**

The deliverable is empirical calibration: every prediction the system makes is stored with the chart data and (where available) actual outcomes. Statistical analysis reveals which rules predict well, which are noise, and where schools agree or diverge.

Exit criterion: Correlation coefficients computed per rule, per text, per school. Rules ranked by empirical performance with confidence intervals.

### Phase -1: Stop the Bleed (3-5 sessions, before anything else)

S318 audited every file in the codebase (660 files, 178,072 lines) and found 104 bugs, 143 silent exception handlers, 22,692 lines of dead code, and 42 formulas that produce wrong answers per BPHS PDF verification. Phase C cannot begin productive encoding on a foundation that computes Mars aspects wrong, ignores planetary dignity, and silently swallows errors.

Phase -1 is triage. It uses no new tools, creates no new modules, builds no new systems. It fixes what's broken, wires what's disconnected, consolidates what's duplicated, and deletes what's dead — using grep, ruff, pytest, and git.

**The work, driven by the 20 quality criteria:**

**Prediction Quality + Domain Fidelity** (the reason this project exists):
Fix 42 formulas that produce wrong answers. Each fix is 1-10 lines, cites a BPHS verse. Mars aspects `{3,9}` → `{3,7}` (BPHS Ch.26 v.5). Cancer yogakaraka Venus → Mars (Ch.34 v.27). Shadbala Tribhaga day lords Jupiter → Mercury (Ch.27 v.12). 9 divisional chart formulas (Ch.6). Sunapha/Anapha swap. Bhakut 5/9. Baladi even-sign reversal (Ch.45 v.3). Total: ~100 lines changed across ~30 files. Includes BUG-066 (data_minimisation.py broken retention query) for Data Sensitivity.
*Verify:* `.venv/bin/pytest tests/ -q --tb=short` passes. Each commit cites BPHS verse.

**Robustness + Observability** (stop hiding errors):
Fix 143 silent `except Exception: pass` handlers. Configure ruff rule BLE001 (blind-except) strictly. Replace `pass` with `logger.exception(msg); raise` for programming errors, `logger.warning(msg); return None` for expected failures. No custom AST tool — ruff already has this rule.
*Verify:* `.venv/bin/ruff check src/ --select BLE001` returns zero violations.

**Testability** (stop testing wrong things):
Fix 107 exact float equality assertions → `pytest.approx`. Delete 3 fake tests (test_panchanga_legacy.py empty stub, test_diverse_charts.py try/except pass tests). Fix 15 stale imports. Add India 1947 snapshot test: full 12-house score output locked in `tests/snapshots/india_1947_scores.json` with `pytest.approx(tolerance=0.01)`.
*Verify:* `grep -rn "assert.*==.*\." tests/ --include="*.py" | grep -v approx | grep -v "==" | wc -l` returns zero. Snapshot test exists and passes.

**Modularity + Explainability** (one engine, traceable results):
Fix `score_all_axes()` data bugs: Mars aspects, 8 inline constant copies replaced with imports from canonical sources (`house_lord.py`, `dignity.py`, `sputa_drishti.py`). Add per-rule `RuleResult` traceability to `score_all_axes()` (the one feature `score_chart()` has that it lacks). Keep the multi-axis architecture — it's the right design, just has wrong data.
*Verify:* `grep -rn "_SIGN_LORD\|_NAT_MALEFIC\|_KENDRA\|_EXALT" src/calculations/multi_axis_scoring.py` returns zero inline definitions.

**Prediction Quality** (the most important single fix):
Wire dignity into scoring. `compute_all_dignities()` is already called in `score_chart()` — the result is already available. Add R24: `dignity_bonus = DIGNITY_SCORE.get(dignities[bhavesh].dignity, 0.0)`. ~10 lines. Exalted bhavesh finally scores higher than debilitated bhavesh. Also wire into `score_all_axes()`.
*Verify:* Test that India 1947 H2 score changes when dignity is wired vs unwired.

**Runtime Correctness** (catch bugs at source):
Fix 5 rule_firing.py bugs: list-dropping in `planet_not_in_house` (use full list), MT degree ranges (add range check per BPHS Ch.3 v.51-54), dispositor "weak" inconsistency, unreachable lagna-scoped block. Add assertions inside canonical primitive functions: `assert 0 <= sign_index <= 11` in `sign_lord()`, `assert 1 <= house <= 12` in `is_kendra()`. ~50 lines total across ~12 files. Assertions go IN the functions, not in a separate checker module.
*Verify:* `.venv/bin/pytest tests/ -q --tb=short` passes. Invalid inputs raise AssertionError with clear message.

**Anti-Spaghetti + Cost of Change** (one source per concept):
Consolidate 14 inline constant sets to canonical imports. For each concept: `grep -rn "pattern" src/ --include="*.py"` → replace inline dict with `from src.calculations.house_lord import sign_lord` → delete inline dict → test. Sign lords (17→1), malefic sets (14→1), kendra/trikona/dusthana (20+→1 each), exaltation (8→1), aspects (21→1), yogakarakas (4→1). Add one grep command per concept to the existing pre-push hook to prevent re-duplication. No new tool — just `grep -c "_SIGN_LORD" src/calculations/ | grep -v "house_lord" | grep -v ":0$"` returns empty.
*Verify:* `tools/import_boundary_check.py` — wait, this doesn't exist. Instead: for each concept, `grep` returns only the canonical source file. Pre-push hook has the check.

**Simplicity + Developer Experience** (less to navigate):
Delete 22,692 lines of dead code across 151 files. The S318 import graph already identified every unreachable file. Modules with future roadmap value: `git mv` to `src/archive/` with a one-line comment. Everything else: `git rm`. Update any test files that import from deleted modules.
*Verify:* `find src/ -name "*.py" | xargs wc -l | tail -1` shows ~156,000 lines.

**Reproducibility + Versioning** (lock the outputs):
The India 1947 snapshot test (from Testability above) includes `corpus_version` (git commit hash) in the snapshot JSON. Any future formula change that alters scores must update the snapshot explicitly with the new expected values and the reason for the change.
*Verify:* Snapshot JSON has `corpus_version` field. `pytest tests/test_snapshot.py` passes.

**Phase A deferrals** (honestly not needed for Phase C):
Evolvability (no extension points needed — fix the foundation first), Performance (single-chart computation is fast enough for encoding sessions), Interoperability (no external API consumers yet), Concurrency (single-user encoding sessions).

**Exit criteria for Phase -1:**
- Zero CRITICAL bugs from S318 master list
- Zero silent exception handlers (ruff BLE001 clean)
- Zero inline definitions of protected constants outside canonical sources
- Zero exact float assertions in tests
- India 1947 snapshot test exists and passes
- Dignity affects house scores
- Codebase < 160,000 lines (down from 178,072)

**Estimated effort:** 3-5 sessions. ~300 lines changed, ~22,692 lines deleted. Net reduction: ~22,400 lines.

---

### What Phase C Needs From the Architecture

Phase C needs exactly three things:

1. **Canonical primitives** — One implementation per concept (sign lords, aspects, dignity, etc.), BPHS-verified, that all consumers import. No local copies.

2. **A rule engine that evaluates encoded rules against charts** — Takes a chart and a rule, returns whether the rule fires and what it predicts. Traceable to the exact conditions checked.

3. **Validation gates that prevent encoding errors** — Structural checks at encode-time that make systematic corpus bugs impossible (wrong primitive names, type mismatches, missing conditions).

Phase C does NOT need: a graph database, a declarative DSL, multi-tenancy, API versioning, or any infrastructure that serves A or B. The architecture must support these later without requiring them now.

---

## Part 2: Architecture Overview

### The System in One Sentence

A pipeline that turns birth data into planetary positions, evaluates classical text rules against those positions, and produces scored predictions with full traceability to source verses.

### Five Layers

```
Birth Data (date, time, location)
  |
[Layer 1] Astronomy — planetary positions from Swiss Ephemeris (immutable)
  |
[Layer 2] Conventions — house system, ayanamsha, MT ranges, combustion orbs (configurable)
  |
[Layer 3] Derived Facts — lordships, aspects, dignity, friendship, avasthas (computed once, read many)
  |
[Layer 4] Rule Evaluation — encoded rules tested against derived facts (one rule, one result)
  |
[Layer 5] Aggregation & Output — scores, groupings, verse citations, school attributions
```

The previous 6-layer pipeline (v9/v10) split "Graph Construction" and "Rule Engine" as separate layers, with an intermediate graph data structure. v11 merges them conceptually: Layer 3 computes derived facts, Layer 4 reads them. Whether the internal representation is a graph, a dictionary, or a flat struct is an implementation detail, not an architectural commitment. The architecture constrains what is computed and who can read it, not the data structure.

### Why Not a Graph-First Architecture

v9 spent 387 lines specifying graph node types, edge tiers, edge identity tuples, and query APIs. This was engineering from the inside out. The graph schema is a valid eventual implementation of Layer 3, but committing to it now:

- Creates 30-50 sessions of migration work before any bug gets fixed
- Introduces a new abstraction layer that all existing code must be rewritten against
- Risks building a "perfectly consistent system that is consistently wrong" (v10's own diagnosis)

v11's position: Fix the foundations first (wrong formulas, duplication, dead code). The derived facts layer can be backed by a graph later if the benefit justifies the cost. The architecture constrains the interfaces, not the implementation.

### The Canonical Primitives Model

The central architectural idea in v11 is not the graph. It is the **canonical primitive**: a single, BPHS-verified, importable function for each classical concept. Every consumer imports from the canonical source. No local copies. No parallel implementations.

A canonical primitive has four properties:
1. **Single source file** — there is exactly one `.py` file that computes this concept
2. **Verse citation** — the function docstring cites the BPHS chapter and verse it implements
3. **Verification tag** — a module-level `_VERIFICATION` constant declaring what level of verification was performed
4. **Import-only access** — consumers import the function, they never redefine the constant locally

The set of canonical primitives:

| Concept | Canonical Source | Current Copies | BPHS Reference |
|---------|-----------------|----------------|----------------|
| Sign lords | `house_lord.sign_lord()` | 17 | Ch.3 |
| House classification (kendra, trikona, dusthana) | `house_lord.is_kendra()` etc. | 20+ | Ch.3 |
| Exaltation/debilitation signs | `dignity.EXALT_SIGN` | 8+ | Ch.3 v.49-50 |
| Own signs | `dignity.OWN_SIGNS` | 7+ | Ch.3 v.47-48 |
| Mooltrikona ranges | `dignity.MOOLTRIKONA_RANGES` | 2 | Ch.3 v.51-54 |
| Natural friendship | `dignity._NAISARGIKA` | 4 | Ch.3 v.55 |
| Planetary aspects | `sputa_drishti.py` | 21 functions | Ch.26 v.2-12 |
| Yogakarakas | `functional_dignity.KNOWN_YOGAKARAKAS` | 4 | Ch.34 |
| Functional malefics | `functional_dignity.KNOWN_FUNCTIONAL_MALEFICS` | 2 | Ch.34 |
| Natural benefic/malefic | `rule_firing.is_natural_malefic()` | 14 sets | Ch.3 |
| Divisional charts | `varga.py` | 2 (divisional_charts.py) | Ch.6 |
| Avasthas (Baladi, Jagradadi, Lajjitadi) | `avasthas.py` | 5 modules | Ch.45 |
| Shadbala | `shadbala.py` | 1 | Ch.27 |
| Ashtakavarga | `ashtakavarga.py` | 1 | Ch.66-72 |

Enforcement: see Criterion 6 (Anti-Spaghetti).

---

## Part 3: The 20 Criteria

### 1. Simplicity

**What the architecture provides:**
Five layers, each with a one-sentence purpose. No intermediate graph data structure required. No declarative DSL required. The simplest correct path: import canonical primitives, compute derived facts, evaluate rules.

The previous architectures (v9/v10) had 6 layers, 4 graph tiers, 5 edge types per tier, edge identity tuples, lazy vs eager computation strategies, and a 25-primitive Rule IR DSL. All valid engineering, all premature. The current system has 104 bugs and 22,692 lines of dead code. The architecture that serves this system is one that makes fixing those bugs trivial, not one that introduces a new abstraction they must be ported to.

**How enforced:**
- Maximum one level of indirection between a consumer and a canonical primitive. A scoring function calls `sign_lord()`, not `graph.follow(sign, LORDS)`. If a graph is introduced later, it wraps the same canonical functions.
- Any new module that duplicates a canonical primitive's logic is rejected at review. The CI check for this is described under Criterion 6.

**Exit criterion:**
A new contributor can trace any prediction from output to verse citation in under 5 hops. Layer count <= 5. No module has more than 2 mandatory dependencies outside its own layer.


### 2. Robustness

**What the architecture provides:**
Every exception handler either logs with context and re-raises, or handles the error with a documented fallback. No silent `except Exception: pass`. No returning magic defaults (1.0, 66.0 years, "Moderate") when computation fails.

The S318 audit found 143 silent exception handlers across 50 files. The worst: `longevity.py` returns 66.0 years on any error. `dominance_engine.py` sets `jup_strong = True` on error. `pressure_engine.py` returns 1.0 ("dasha unavailable"). These are not error handling — they are error concealment.

**How enforced:**
- AST-based lint rule (custom ruff plugin or standalone script) that rejects `except Exception: pass` and `except Exception` blocks that don't contain `logger.`, `raise`, or `warnings.warn`. Run in CI.
- Every canonical primitive function declares its failure mode in its docstring: either it raises (caller must handle) or it returns a typed sentinel (e.g., `None`, never a plausible-looking default).

**Exit criterion:**
Zero silent exception handlers in `src/`. Every `except` block either logs+raises or uses a documented sentinel. Lint check passes in CI.


### 3. Testability

**What the architecture provides:**
Each canonical primitive is independently testable with minimal setup. A test for `sign_lord()` needs no chart, no pipeline, no config. A test for `compute_dignity()` needs a planet position and a sign, nothing more. A test for a rule evaluation needs a chart fixture and a rule definition, no database or API.

The S318 audit found: canonical `avasthas.py` has zero test coverage. 15 test imports reference stale modules. 107 assertions use exact float equality instead of `pytest.approx`. 1 empty test file provides false coverage.

**How enforced:**
- Coverage gate in CI: every canonical primitive module must have >= 80% line coverage. Modules below this threshold block the commit.
- No test may import from a non-canonical module for a concept that has a canonical source. This is enforced by the same import boundary check as Criterion 6.
- All float assertions use `pytest.approx` with explicit tolerance. A custom lint rule rejects `assert x == <float_literal>` without `approx`.

**Exit criterion:**
All canonical primitive modules >= 80% line coverage. Zero stale test imports. Zero exact float equality assertions. `pytest tests/ -q --tb=short` passes clean with zero warnings.


### 4. Modularity

**What the architecture provides:**
Each layer depends only on the layer directly below it. Within Layer 3 (Derived Facts), computation order follows a dependency DAG:

```
Tier 1: Positions + Conventions (from Layers 1-2)
  |
Tier 2: Lordships, House classification (from Tier 1)
  |
Tier 3: Aspects, Conjunction, Combustion, Friendship (from Tiers 1-2)
  |
Tier 4: Dignity, Avasthas (from Tiers 1-3)
  |
Tier 5: Shadbala, Functional roles, Bhava Bala (from Tiers 1-4, computed lazily)
```

This is the same tiering as v9's graph, but expressed as a computation dependency order rather than a graph edge tier system. The tiers are conceptual — they constrain what can depend on what, but don't require a graph implementation.

**How enforced:**
- Import direction check in CI: no file in Layer 1 imports from Layer 2+. No file in Layer 2 imports from Layer 3+. Within Layer 3, no Tier N module imports from Tier N+1.
- Module registry file (`src/MODULE_REGISTRY.py`) maps every `src/calculations/` file to its layer and tier. New files must be registered. The CI check validates import directions against this registry.

**Exit criterion:**
Zero cross-layer upward imports. Zero cross-tier upward imports within Layer 3. Module registry covers 100% of `src/calculations/` files.


### 5. Prediction Quality

**What the architecture provides:**
The architecture does not directly produce predictions — the corpus does. The architecture's job is to ensure that:
- Every encoded rule can actually fire (currently 58.5% cannot)
- Every relevant classical factor affects the score (currently dignity is ignored)
- Every scored prediction traces to specific verse conditions
- Contradictions between texts are visible, not silently resolved

**How enforced:**
- Computability gate: the rule builder rejects rules whose conditions reference unknown primitives or impossible states. A rule with `ctype: "planet_in_house"` and `house: 15` is rejected at encode-time.
- Wiring test: an integration test verifies that `compute_all_dignities()` output affects the final house scores. If dignity is disconnected again, the test fails.
- Calibration fixture: the India 1947 chart produces a stable set of house scores. These scores are snapshot-tested. Any change to scoring logic must update the snapshot explicitly.

**Exit criterion:**
>= 80% of encoded V2 rules can fire against the India 1947 fixture. Dignity affects house scores (verified by test). Calibration snapshot exists and is tested in CI.


### 6. Anti-Spaghetti

**What the architecture provides:**
The canonical primitives model eliminates the root cause of the 104 bugs: duplication leading to drift. When there is one sign lord table and 17 consumers import it, a correction is one fix. When there are 17 copies, a correction is 17 fixes and a guarantee that someone will miss one.

**How enforced — the Import Boundary Enforcer:**

A CI script (`tools/import_boundary_check.py`) that:

1. Reads `src/MODULE_REGISTRY.py` to get the canonical source for each concept
2. Scans all `.py` files for inline definitions of protected constants (sign lord dicts, kendra sets, malefic sets, exaltation tables, aspect house dicts, yogakaraka maps)
3. Fails CI if any file defines a protected constant outside the canonical source

The protected constants are identified by pattern matching (e.g., any dict literal mapping planet names to sign indices that isn't in `house_lord.py`). This is not foolproof — a creative programmer could obfuscate a local copy. But it catches the 95% case: someone copy-pasting a constant because it's faster than finding the import.

The remaining 5% is caught by code review, which is discipline-dependent. This is an honest limit.

Additionally:
- Each module has a single-sentence purpose declared in `MODULE_REGISTRY.py`. If the purpose cannot be stated in one sentence, the module is doing too much and must be split.
- No module exceeds 500 lines without a documented reason in the registry. This is not a hard limit on quality — it is a trigger for review. The review may conclude the module is correctly sized.

**Exit criterion:**
`tools/import_boundary_check.py` passes in CI. Zero inline definitions of protected constants outside canonical sources. Every module in `src/calculations/` registered with a one-sentence purpose.


### 7. Domain Fidelity

**What the architecture provides:**
Every canonical primitive cites the BPHS verse it implements. Every encoded rule cites its source text, chapter, and verse. Every formula can be verified by opening the PDF and reading the cited verse.

The S318 audit found: `extended_yogas.py` cites Ch.30 for Neecha Bhanga (correct source is Ch.49). `scoring.py` has a comment admitting Cancer yogakaraka is wrong. 9 of 16 divisional chart formulas are wrong per BPHS Ch.6.

**How enforced:**
- Verification tag system: every canonical module has `_VERIFICATION = "bphs_pdf" | "formula_compared" | "pattern_scanned" | "unverified"` with the specific verse cited.
- The module registry includes the verification level. A module tagged `unverified` cannot be the canonical source for consolidation.
- Encoding protocol (CLAUDE.md Gate 1-2) requires verse audit before encoding. The audit file is machine-readable and links every claim to a verse number.
- No formula change is committed without a BPHS verse citation in the commit message.

**Exit criterion:**
100% of canonical primitive modules tagged with verification level. Zero `unverified` canonical sources. Every formula-changing commit cites a BPHS verse.


### 8. Evolvability

**What the architecture provides:**
Adding a new text (Saravali, Phaladeepika) means adding new rules that import existing canonical primitives. No new computation modules needed. Adding a new school (Jaimini, KP) means adding school-specific computation modules for the concepts that differ (aspects, house system) and tagging rules with their school.

The architecture explicitly defers infrastructure that isn't needed yet:
- Graph data structure: deferred until Layer 3 consumers demonstrate need for multi-hop traversal
- Rule IR DSL: deferred until the procedural rule engine's bugs are fixed and a clear benefit case exists
- Multi-tenancy: deferred until Phase A
- API versioning: deferred until Phase A

**How enforced:**
- New text addition checklist in `docs/ADDING_A_TEXT.md`: (1) create verse audit, (2) encode rules using existing primitives, (3) tag rules with source text and school. If a new primitive is needed, it goes through the canonical primitive creation process (propose, verify against PDF, register, test).
- New school addition checklist in `docs/ADDING_A_SCHOOL.md`: (1) identify which concepts differ, (2) create school-specific modules for those concepts only, (3) register in MODULE_REGISTRY with school tag.
- Feature flags for experimental school support: `REGISTERED_SCHOOLS` in config.

**Exit criterion:**
Adding a new text's rules requires zero changes to the computation layer. Adding a new school requires changes only to the modules where that school differs from Parashari. Both checklists exist and are tested by at least one non-BPHS text.


### 9. Explainability / Traceability

**What the architecture provides:**
Every house score decomposes into: which rules fired, what conditions each rule checked, what values those conditions found in the chart, and which verse prescribed the prediction. An astrologer reading the output can verify each step against the source text.

Trace depth is configurable:
- **Minimal:** rule ID + verse citation + direction
- **Standard:** + condition values (planet positions, dignity levels, house placements)
- **Full:** + every intermediate computation (aspect strength values, shadbala components)

**How enforced:**
- Every `RuleResult` includes: `rule_id`, `source_text`, `chapter`, `verse`, `conditions_checked` (list of `{primitive, arguments, result}`), `prediction` (domain, direction, intensity, entity_target).
- The aggregation layer (Layer 5) preserves individual rule results — it groups and sums them but never discards them. The final output includes both the aggregate score and the contributing rules.
- Integration test: for the India 1947 fixture, every non-zero house score can be decomposed into specific rule firings, and every rule firing traces to a specific verse.

**Exit criterion:**
Any house score can be decomposed to individual rule firings in one function call. Each rule firing includes verse citation. Integration test verifies full trace for India 1947.


### 10. Developer Experience

**What the architecture provides:**
A developer (human or AI session) performing any of the three main activities — encoding a chapter, fixing a bug, adding a text — has a clear, documented workflow with explicit entry and exit criteria.

For encoding: Read CLAUDE.md encoding protocol. Run the 5 gates. Ship.
For bug fixing: Find the canonical source for the concept. Fix it there. Run tests. All consumers get the fix.
For adding a text: Follow the checklist. Import existing primitives. Encode rules.

**How enforced:**
- `CLAUDE.md` encoding protocol is non-negotiable (5 gates, no skipping)
- `src/MODULE_REGISTRY.py` answers "where is the canonical source for X?" without grep
- `tools/v2_scorecard.py` gives immediate feedback on rule encoding quality
- `ruff check` + `pytest` as pre-commit/pre-push hooks

**Exit criterion:**
A new encoding session can start producing correct rules within 15 minutes of reading `CLAUDE.md`. The MODULE_REGISTRY answers any "where is X?" question. No tribal knowledge required.


### 11. Reproducibility

**What the architecture provides:**
Given the same birth data, the same configuration, and the same corpus version, the system produces identical output. No randomness. No ambient state. No dependency on evaluation order.

**How enforced:**
- All computation is pure: same inputs produce same outputs. No global mutable state in Layer 1-4.
- Configuration is explicit: ayanamsha, house system, MT ranges, combustion orbs are parameters, not hardcoded values.
- Corpus version is tracked: every rule has a `corpus_version` field. Output includes the corpus version used.
- Snapshot tests: India 1947 fixture produces a deterministic set of scores. Any change to computation logic changes the snapshot (and requires explicit update).

**Exit criterion:**
Two runs of the same chart with the same config produce byte-identical JSON output. Snapshot test enforces this in CI.


### 12. Observability

**What the architecture provides:**
When something goes wrong — a score looks unreasonable, a rule fires unexpectedly, a computation takes too long — the system provides enough information to diagnose the problem without adding ad hoc logging.

**How enforced:**
- Every canonical primitive function logs at DEBUG level: what it computed, from what inputs. This is always available, not added during debugging.
- `RuleResult` trace (Criterion 9) provides rule-level observability.
- Silent exception handler elimination (Criterion 2) ensures errors are visible.
- Performance: `tools/benchmark_chart.py` measures time per layer. Any layer exceeding 50ms on a standard chart triggers investigation.

**Exit criterion:**
Any incorrect output can be diagnosed from existing logs (DEBUG level) + rule trace without modifying code. Zero silent exceptions. Benchmark script exists and runs in CI.


### 13. Data Sensitivity

**What the architecture provides:**
Birth data (date, time, location) is personally identifiable. The architecture separates birth data (Layer 1 input) from computed results (Layers 2-5 output). Birth data can be deleted without affecting the corpus or computation modules.

The S318 audit found: `data_minimisation.py` queries a `last_accessed` column that doesn't exist, making the retention policy non-functional.

**How enforced:**
- Birth data stored in a separate table/file from computed charts and predictions
- Retention policy actually works (fix the `last_accessed` bug)
- No birth data in log output (data masking in logger configuration)
- CORS and authentication for API endpoints (fix the `allow_origins=["*"]` and hardcoded JWT secret)

**Exit criterion:**
Retention policy deletes expired birth data (verified by test). No birth data in DEBUG logs. CORS restricted. JWT secret from environment variable.


### 14. Cost of Change

**What the architecture provides:**
Fixing a wrong formula is a 1-10 line change in one file. Currently, fixing Mars aspects requires changing 3 files because 3 files define their own aspect tables. After canonical primitive consolidation, it requires changing 1 file.

Adding a new chapter's rules is pure data: new JSON rule definitions that import existing primitives. Zero computation code changes.

**How enforced:**
- Canonical primitives model (Criterion 6): one source per concept means one place to fix
- Import boundary enforcer: prevents new duplications from being introduced
- Rule engine separation: corpus data (rules) is separate from evaluation logic (rule_firing.py). Changing rules doesn't change the engine.

**Exit criterion:**
Any single-concept formula fix (sign lords, aspects, dignity) requires changing exactly 1 file. Measured by: pick any 5 concepts, count files that would need changing. All must be 1.


### 15. Knowledge Preservation

**What the architecture provides:**
The corpus is the product. Every verse encoding preserves: the source text name, chapter, verse number, the original claim (in the verse audit file), the structured rule, and the prediction. Losing any of these makes the rule less valuable.

**How enforced:**
- Verse audit files (`data/verse_audits/chN_audit.json`) are required before encoding (Gate 1-2)
- Every rule JSON includes `source_text`, `chapter`, `verse`, `sloka` (original text reference)
- The verse audit file is version-controlled alongside the rules
- The builder validates that every rule has these fields (T1-1 through T1-5)

**Exit criterion:**
100% of encoded rules have complete provenance (text, chapter, verse). Verse audit files exist for all encoded chapters. Builder blocks on missing provenance.


### 16. Performance at Scale

**What the architecture provides:**
Phase C operates on single charts, evaluated one at a time. There is no scale pressure yet. The architecture prepares for Phase B scale (thousands of charts) by ensuring computation is stateless and parallelizable, but does not optimize prematurely.

**How enforced:**
- Chart computation is a pure function: `compute_chart(birth_data, config) -> ChartResult`. No shared state between charts. Embarrassingly parallel.
- Benchmark script (`tools/benchmark_chart.py`): measures end-to-end time for one chart. Current target: < 200ms for full computation (all rules, all lagnas).
- If Phase B requires batch processing, the pure function model allows `multiprocessing.Pool.map()` with zero architectural change.

**Exit criterion:**
Single chart computation < 200ms (benchmarked, not assumed). Computation function is pure (verified by running same chart twice, asserting identical output).


### 17. Interoperability

**What the architecture provides:**
Chart results are JSON-serializable. Rule definitions are JSON. Verse audits are JSON. All data interchange uses standard formats. No custom binary formats.

The API layer (Phase A) wraps computation results in REST endpoints with OpenAPI schemas. But the computation layer is API-agnostic — it returns Python objects that are trivially serializable.

**How enforced:**
- All data classes in Layer 4-5 output have `to_dict()` methods that produce JSON-serializable dicts
- No non-JSON serialization in production code (lint rule)
- Schema version field on all outputs: `{"schema_version": "1.0", "corpus_version": "...", ...}`

**Exit criterion:**
All computation outputs JSON-serializable. Zero non-JSON serialization in `src/`. Schema version on all outputs.


### 18. Concurrency / Multi-tenancy

**What the architecture provides:**
Phase C has one user (the encoding session). Multi-tenancy is a Phase A concern. The architecture prepares for it by ensuring computation is stateless (no global mutable state), but does not build multi-tenancy infrastructure now.

**How enforced:**
- No module-level mutable state in `src/calculations/`. All computation functions take inputs and return outputs. Verified by lint rule: no `global` keyword, no module-level mutable containers that are written to outside `__init__`.
- When Phase A arrives, concurrency is achieved by running computation functions in separate processes/threads with no shared state. Zero architectural change required.

**Exit criterion:**
Zero `global` keyword in `src/calculations/`. Zero module-level mutable state (verified by lint). Two concurrent chart computations produce correct, independent results (integration test).


### 19. Versioning / Backward Compatibility

**What the architecture provides:**
Three version axes:
1. **Corpus version** — incremented when rules are added, modified, or deleted. Tracked in corpus metadata.
2. **Schema version** — incremented when the output format changes. Tracked in output JSON.
3. **Convention version** — incremented when default ayanamsha, house system, or MT ranges change. Tracked in config.

A chart computed with corpus v47 and convention v3 can be exactly reproduced later by specifying those versions.

**How enforced:**
- Corpus version in every rule file header. Aggregated into computation output.
- Schema version in output format. Consumers check schema version before parsing.
- Convention version in config. Default conventions are versioned, not just named.
- Breaking changes require schema version bump. CI check: if output format fields change, schema version must change.

**Exit criterion:**
All three version axes tracked. Output includes all three versions. A chart from 6 months ago can be reproduced by specifying the versions used.


### 20. Runtime Correctness Verification

**What the architecture provides:**
The system can verify its own consistency at runtime, not just at test time. When a chart is computed, lightweight invariant checks run and flag violations without stopping computation.

Invariants:
- Every planet is in exactly one sign and one house
- Every house has exactly one lord
- Aspect strength is non-negative
- Dignity level is one of the defined enum values
- No rule fires with contradictory conditions (e.g., planet in house 5 AND planet not in house 5)

**How enforced:**
- `assert` statements in canonical primitives for impossible states (these are programming errors, not data errors — assertions are appropriate)
- Runtime invariant checker (`src/invariants.py`) runs after Layer 3 computation, before Layer 4. Returns list of violations. In development: raises. In production: logs and continues.
- Contradictory rule conditions detected at encode-time (builder validation) not runtime.

**Exit criterion:**
Invariant checker runs on every chart computation. Zero violations on the India 1947 fixture. Invariant checker catches at least: wrong planet count, duplicate lordships, negative aspect strengths.

---

## Part 4: Migration from Current State

### Honest Assessment of Where We Are

- 660 files, 178,072 lines
- 104 known bugs (20 critical, 17 high, 37 contradictions, 30 structural)
- 22,692 lines of dead code across 151 files
- 143 silent exception handlers
- 17 copies of sign lord tables
- 21 separate aspect computation functions
- 2 parallel scoring engines with different bugs
- 58.5% of encoded rules cannot fire
- Dignity (the most important classical factor) is computed and then ignored

### Migration Sequence

The migration is 8 stages. Each stage is independently valuable. Each produces a working system that is strictly better than the previous one. No stage requires a later stage to be useful. Stages 1-5 can be done in any order, though the listed order minimizes rework.

**Stage 1: Fix Wrong Formulas (3-5 sessions)**

Fix the 42 objectively wrong formulas identified in S318. Each fix is 1-10 lines. Each fix cites a BPHS verse in the commit message. No architecture changes. No new files. The system produces more correct answers immediately.

Exit: All 42 BUG-xxx fixes committed. Tests pass. Each commit cites BPHS verse.

**Stage 2: Tag Verification Levels (1 session)**

Add `_VERIFICATION` constant to every module in `src/calculations/`. No code behavior changes. This is metadata that prevents Stage 4 from consolidating to an unverified source.

Exit: Every module tagged. No behavior changes.

**Stage 3: Eliminate Silent Exception Handlers (2-3 sessions)**

Replace 143 `except Exception: pass` blocks with proper error handling: log + raise for programming errors, documented sentinels for expected failures. Add the AST lint rule to CI.

Exit: Zero silent exception handlers. Lint rule passes in CI.

**Stage 4: Consolidate to Canonical Primitives (5-8 sessions)**

For each concept in the canonical primitives table: redirect all consumers to import from the canonical source. Delete inline copies. Only consolidate modules tagged `bphs_pdf` or `formula_compared`.

This is the highest-leverage stage. It converts 17 sign lord copies into 1. It converts 21 aspect functions into 1 canonical import. Every future fix to any concept becomes a single-file change.

Exit: Zero inline definitions of protected constants outside canonical sources. Import boundary check passes in CI.

**Stage 5: Delete Dead Code (2-3 sessions)**

Delete the 22,692 lines across 151 files that have no production importers. Move files with future roadmap value to `src/archive/`. Delete everything else.

Exit: Only production-reachable code in `src/`. Codebase shrinks to ~435 files, ~156,000 lines.

**Stage 6: Wire Missing Connections (2-3 sessions)**

Make dignity affect house scores. Resolve the two-scoring-engine split (keep `score_chart()`, deprecate `score_all_axes()`). Fix the varga module import inconsistency.

Exit: Dignity affects house scores (tested). One primary scoring engine. All varga imports consistent.

**Stage 7: Build Module Registry and Import Boundary Enforcer (2-3 sessions)**

Create `src/MODULE_REGISTRY.py` and `tools/import_boundary_check.py`. Register all modules. Add the CI check.

Exit: All modules registered. Import boundary check runs in CI and passes.

**Stage 8: Build Runtime Invariant Checker (1-2 sessions)**

Create `src/invariants.py`. Wire it into chart computation pipeline. Write tests.

Exit: Invariant checker runs on every chart computation. Passes on India 1947 fixture.

### Total Estimated Effort: 18-28 Sessions

This is conservative. Each stage has clear scope and exit criteria. No stage involves "rewrite the architecture." The system gets better with each commit.

### What Comes After Stage 8

After Stage 8, the system is: correct (formulas verified), consolidated (one source per concept), clean (no dead code, no silent exceptions), observable (proper error handling, runtime invariants), and enforced (import boundaries, lint rules, CI checks).

At that point — and not before — the project evaluates whether a graph data structure or declarative Rule IR would provide incremental benefit. The evaluation criteria:

- **Graph:** Is there a concrete use case that requires multi-hop traversal across derived facts that the current dict/function-call model handles poorly?
- **Rule IR:** After the procedural rule engine's bugs are fixed (Stage 1), are there systematic encoding errors that a type system would prevent and that validation gates don't already catch?

If yes to either, they become Stage 9+. If no, the system is already correct and maintainable, and the engineering effort goes into corpus encoding (Phase C's actual deliverable).

### Phase A and Phase B Infrastructure

Phase A (practitioner tool, S800+) adds:
- API layer with authentication, rate limiting, versioned endpoints
- Multi-lagna evaluation (natal, chandra, surya) — currently partially implemented
- Multi-text concordance aggregation — new Layer 5 logic
- Query interface for specific domains ("what about career?")

Phase B (research platform, S1400+) adds:
- Outcome data ingestion and storage
- Per-rule correlation analysis
- Batch chart processing (leveraging pure computation functions)
- Statistical reporting

Both phases build ON the corrected, consolidated, enforced foundation. Neither requires changes to Stages 1-8 infrastructure. This is the purpose of the C -> A -> B sequencing.

---

## Part 5: What Can Go Wrong

### Risk 1: Canonical Source is Wrong

If the one canonical source for sign lords has a bug, every consumer gets the wrong answer. Previously, having 17 copies meant at least some were right. Consolidation concentrates risk.

**Mitigation:** Verification tags. Only `bphs_pdf`-verified modules become canonical sources. The verification was done by reading the BPHS PDF and comparing value-by-value. The risk is real but lower than the current state (where 3 of 17 copies have different bugs and there is no way to know which is right).

### Risk 2: Import Boundary Enforcer is Incomplete

Pattern-matching for inline constant definitions is heuristic. A developer can define `MY_SIGNS = {0: "Sun", ...}` and the enforcer won't catch it because the variable name doesn't match the protected pattern.

**Mitigation:** The enforcer catches the 95% case (obvious copies with similar names). The remaining 5% relies on code review. This is a discipline gap that the architecture acknowledges rather than pretends to solve.

### Risk 3: Wrong Formula Verified as Correct

A BPHS verse may be ambiguous. The translator's gloss may differ from the verse. A formula verified as `bphs_pdf` may still be wrong because the verification compared against a translation, not the Sanskrit original.

**Mitigation:** Verification tags include the specific verse citation. A future reviewer can re-verify against a different translation or the original. The tag doesn't claim "this is right" — it claims "this was compared against Santhanam translation at [verse]."

### Risk 4: Migration Stalls

18-28 sessions is a significant investment. If the project gets pulled into encoding work (Phase C's main deliverable) before migration completes, the foundation remains partially fixed.

**Mitigation:** Each stage is independently valuable. Even completing only Stages 1 and 4 (fix formulas + consolidate primitives) eliminates the majority of the 104 bugs. The stages are designed to be interruptible.

### Risk 5: Performance Degrades After Consolidation

Importing from canonical sources adds function call overhead compared to inline dicts. A hot path that currently does a dict lookup might become measurably slower with a function call.

**Mitigation:** Profile after Stage 4. If any path shows measurable degradation, the canonical function can cache or inline its result at module load time (computed once, stored as module-level constant). The import boundary enforcer allows this pattern — it checks for inline definitions, not inline caching of canonical values.

### Risk 6: Over-Engineering the Enforcer

The import boundary enforcer could become its own maintenance burden — a complex AST analysis tool that itself has bugs and generates false positives.

**Mitigation:** Keep it simple. Start with string/regex matching on known constant names (`_SIGN_LORD`, `_KENDRA`, `_EXALT_SIGN`, etc.). Graduate to AST analysis only if string matching produces too many false positives. The enforcer is a tool, not a product.

### Risk 7: The Graph Becomes Premature Again

After Stage 8, the evaluation of "should we build a graph?" might conclude yes, and the project spends 30-50 sessions on graph infrastructure while corpus encoding waits.

**Mitigation:** The evaluation criteria are explicit and measurable. "Is there a concrete use case that requires multi-hop traversal that the current model handles poorly?" If the answer is "maybe, in the future," the answer is no. The graph is built when the current model demonstrably fails, not when it might theoretically be suboptimal.

### What This Architecture Cannot Do

- It cannot prevent wrong verse interpretations. If an encoder reads BPHS Ch.24 v.21 and encodes the wrong prediction, the architecture accepts it. Maker-checker protocol (CLAUDE.md) is the mitigation, and it is discipline-dependent.
- It cannot handle a fundamentally different astrological system (Chinese, Western) without significant extension. The canonical primitives assume planets, signs, houses, and lordships.
- It cannot guarantee that the BPHS Santhanam translation is correct. All verifications are against this translation. A different translation might yield different formulas.
- It cannot prevent a determined developer from bypassing every check. `--no-verify` on git, commenting out lint rules, ignoring CI failures. The architecture makes the right path easy and the wrong path visible, but it cannot make the wrong path impossible.

---

## Appendix: Honest Score Against 20 Criteria

**Scoring rubric:**
- 5/5 = Implemented, tested, enforced in CI today
- 4/5 = Designed, partial implementation exists, <3 sessions to complete
- 3/5 = Problem identified, solution described with actionable detail, no implementation yet
- 2/5 = Problem identified, solution underspecified
- 1/5 = Problem mentioned but not addressed

This spec is a PLAN. It scores what the document provides, not what the codebase will look like after 18-28 sessions.

| # | Criterion | Score | Rationale |
|---|-----------|-------|-----------|
| 1 | Simplicity | 4/5 | 5-layer model sound. Enforcement unbuilt. |
| 2 | Robustness | 3/5 | 143 handlers identified, lint rule described but unbuilt. |
| 3 | Testability | 3/5 | Strategy described, infrastructure unbuilt. |
| 4 | Modularity | 3/5 | Tier model designed, MODULE_REGISTRY not created. |
| 5 | Prediction Quality | 2/5 | Dignity wiring described, formula unspecified. |
| 6 | Anti-Spaghetti | 3/5 | Import enforcer designed, not built. |
| 7 | Domain Fidelity | 3/5 | Verification tags designed, not added. |
| 8 | Evolvability | 2/5 | Checklists described, not written. |
| 9 | Explainability | 3/5 | Richer RuleResult described, not implemented. |
| 10 | Developer Experience | 3/5 | Registry described, not created. |
| 11 | Reproducibility | 3/5 | Snapshots described, not built. |
| 12 | Observability | 2/5 | Logging described, not added. |
| 13 | Data Sensitivity | 2/5 | Fixes identified, not done. |
| 14 | Cost of Change | 3/5 | Depends on consolidation (unbuilt). |
| 15 | Knowledge Preservation | 4/5 | Verse audits exist, builder validates. |
| 16 | Performance | 3/5 | Benchmark described, not built. |
| 17 | Interoperability | 3/5 | JSON works in practice, no schema versions. |
| 18 | Concurrency | 3/5 | Stateless in practice, no lint check. |
| 19 | Versioning | 2/5 | Three axes designed, zero implemented. |
| 20 | Runtime Correctness | 2/5 | Invariant checker designed, not built. |
| | **Total** | **55/100** | **This is a plan, not an implementation.** |

**Projected scores after migration:**

| Milestone | Score | What changes |
|-----------|-------|-------------|
| After Stages 1-2 (fix + tag) | ~60 | Formulas correct, verification explicit |
| After Stages 3-4 (registry + exceptions) | ~70 | Enforcement exists, silent failures eliminated |
| After Stages 5-6 (consolidate + delete) | ~80 | Single sources, dead code gone |
| After Stages 7-8 (wire + invariants) | ~90 | Dignity affects scores, runtime checks active |
| Remaining ~10 points | Phase A/B | Multi-tenancy, GDPR, empirical calibration |

**Companion document:** `2026-04-07-v11-execution-plan.md` contains session contracts, tool specifications, testing strategy, and Stage 7 scoring engine resolution detail.
