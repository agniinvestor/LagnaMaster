# PROJECT_STRATEGY.md — LagnaMaster Golden Source

> **This is the single authoritative document for project state, architecture, and next steps.**
> Every session reads THIS instead of 10+ partial documents.
> Last verified: 2026-04-14 (G1-G6 complete + D0-D24 resolved. Pipeline live. OB-4: +18% over OB-3).

---

## Section 1: Where We Are (Diagnostic Facts)

### 1.1 Core Health Dashboard

| Metric | Value | Command | Last verified |
|--------|-------|---------|---------------|
| Tests passing | 14,917 | `.venv/bin/pytest tests/ -q --tb=short` | 2026-04-14 |
| Tests skipped | 210 | (same) | 2026-04-14 |
| Tests xfailed | 360 | (same) | 2026-04-14 |
| Lint errors | 0 | `.venv/bin/ruff check src/ tests/` | 2026-04-14 |
| Constants validated | PASS | `tools/validate_constants.py` | 2026-04-12 |
| Import boundaries | PASS (9 documented exceptions) | `tools/import_boundary_check.py` | 2026-04-12 |
| Reachable src/ files | 276/280 | `tools/reachability_analysis.py` | 2026-04-12 |
| Tools-only files | 4 | (same) | 2026-04-12 |
| Truly dead files | 0 | (same) | 2026-04-12 |
| Silent exception handlers | 0 (12 fixed in D18) | manual scan | 2026-04-14 |
| src/ Python files | 280 | `find src/ -name "*.py"` | 2026-04-12 |
| src/ total lines | 121,314 | `wc -l` | 2026-04-12 |
| test files | 187 | `find tests/ -name "*.py"` | 2026-04-12 |
| test total lines | 28,739 | `wc -l` | 2026-04-12 |
| Markdown docs | 126 | `find . -name "*.md"` | 2026-04-12 |
| TODO/FIXME markers | 45 | `grep -rn 'TODO\|FIXME' src/` | 2026-04-12 |
| Rework signals | 0 | `tools/rework_detector.py` | 2026-04-12 |
| Verse audit files | 20 | `find data/verse_audits/ -name '*.json'` | 2026-04-12 |

### 1.2 Corpus Maturity

| Level | Count | % of 25K target | Description |
|-------|-------|------------------|-------------|
| L0 Unmapped | 17,534 | 70.1% | Not yet encoded |
| L1 Prose | 6,807 | 27.2% | Prose descriptions only, no structured conditions |
| L2 Structured | 5 | 0.0% | Partially structured (quality gaps) |
| L3 Complete | 625 | 2.5% | Full V2 schema, computable |
| L4 Compared | 29 | 0.1% | Cross-text comparison done |
| L5 Validated | 0 | 0.0% | Empirically validated |
| **Total encoded** | **7,466** | **29.9%** | |
| **V2 complete (L3+)** | **654** | **2.6%** | |

**V2 quality metrics (654 rules):**
- Predictions populated: 654/654 (100%)
- Computable conditions: 645/654 (98.6%)
- Signal groups: 654/654 (100%)
- Commentary: 654/654 (100%)
- Timing checked: 654/654 (100%, 71 with specific timing)
- Condition/modifier audit flags: 24 medium-confidence
- Ship-ready chapters: 19/19
- Verse-verified chapters: 17/17

**By source text (V2 rules):**
- BPHS: 654 V2 / 2,115 total (30.9%)
- All other texts (Saravali, Bhavartha Ratnakara, etc.): 0 V2

### 1.3 Architecture Link Status (THE critical diagnostic)

> **Updated 2026-04-14 after G1-G6 build + D0-D24 resolution.**

The new pipeline: `build_chart_context` → `evaluate_all_rules` → `converge` → `time_project`.
Entry point: `src/pipeline.py:run_pipeline()`. CLI: `python -m src.pipeline YEAR MONTH DAY HOUR LAT LON TZ`.

| # | Link | Status | Detail |
|---|------|--------|--------|
| 1 | Corpus → unified engine | **WIRED** | `evaluate_all_rules()` fires both 26 scoring rules AND 7,466 corpus rules via single `EvalResult` output |
| 2 | Scoring rules → data | **WIRED** | 26 rules migrated to `ScoringRule` data records in `scoring_rules.py`, evaluated by `scoring_rule_eval.py` |
| 3 | Unified → convergence | **WIRED** | `converge()` counts independent channels: scoring, D9, D10, BPHS, Saravali, yoga, other_text |
| 4 | Convergence → temporal | **WIRED** | `time_project()` overlays 7 timing systems (Vimshottari MD/AD, Yogini, Chara, Gochara, Varshaphala, PAD) |
| 5 | Pipeline → production | **WIRED** | `score_chart()` and `evaluate_chart()` auto-build ChartContext. API `create_chart()` calls `run_pipeline()`. |
| 6 | Weight versioning | **WIRED** | `WeightStore` with 3 version axes. Evaluator reads from store. Persists to JSON. |
| 7 | Empirical feedback | **NOT BUILT** | Phase B / G10. Requires user life event data. |
| 8 | Traceability | **WIRED** | Every EvalResult has rule_id + verse_ref + conditions_met. 348/348 corpus rules traced. |

**Where the chain breaks:** Link 7 only. The feedback loop requires Phase B user data (life events with dates).

**Consequence:** The full corpus (7,466 rules) now affects pipeline output. OB-4 confirms convergence outperforms raw house scores by +18% average ρ.

### 1.4 Empirical Signal — OB-3 (legacy) vs OB-4 (pipeline)

> Updated 2026-04-14. Full dataset: 4,832 AA+A Rodden-rated ADB charts.

| House | Domain | OB-3 (OLD) ρ | OB-4 (CONV) ρ | Δ | Verified |
|-------|--------|-------------|---------------|------|----------|
| H01 | Vitality | +0.458 | **+0.549** | +0.091 (+20%) | 2026-04-14 |
| H03 | Communication | +0.447 | **+0.528** | +0.082 (+18%) | 2026-04-14 |
| H05 | Children | +0.475 | **+0.553** | +0.079 (+17%) | 2026-04-14 |
| H07 | Relationships | +0.474 | **+0.571** | +0.098 (+21%) | 2026-04-14 |
| H09 | Higher learning | +0.425 | **+0.498** | +0.073 (+17%) | 2026-04-14 |
| H10 | Career | +0.389 | **+0.447** | +0.057 (+15%) | 2026-04-14 |

**Pipeline wins on all 6 houses. Average Δ = +0.080 (+18%).**

- **OB-3** measures `score_all_axes()` raw house floats (26 hardcoded rules). Unchanged through G1-G6 — this confirms zero regression.
- **OB-4** measures `converge()` independent channel count (26 scoring + 7,466 corpus rules, 7 convergence channels). This is the new metric.
- **TOTAL (natal+temporal) = CONV** because ADB labels have no dates. Temporal projection needs dated life events (Phase B) to show value.

**Interpretation:** ρ ≈ 0.50 is moderate. Not publishable (need ρ ≥ 0.70). Ceiling is limited by binary ADB labels and noisy category proxies. Per-prediction accuracy with dated life events (Phase B / G10) is the path to higher ρ.

**Tool:** `tools/ob4_pipeline_calibrate.py` (full run: ~70 min on 4,832 charts)

### 1.5 v11 Execution Plan Stage Status (verified against code)

| Stage | v11 claims | Code shows | Verified status |
|-------|-----------|-----------|----------------|
| 1. Fix wrong formulas | ~95% | All C01-C20 bugs fixed (confirmed in git) | **DONE (100%)** |
| 2. Tag verification levels | Partial | 15 files tagged (9 original + 6 pipeline), 97 untagged | **13% done** |
| 3. Module registry + enforcer | DONE | `MODULE_REGISTRY.py` (32 entries) + `import_boundary_check.py` exist | **DONE** |
| 4. Silent exception handlers | DONE | 0 silent handlers remain (12 fixed in D18, down from 143 originally) | **100% done** |
| 5. Canonical primitives | DONE | `validate_constants.py` passes, 79 files refactored | **DONE** |
| 6. Delete dead code | ~10% | Reachability: 0 truly dead files, 4 tools-only | **DONE (for dead files)** |
| 7. Wire missing connections | DONE | R24 dignity wired in scoring.py, 2 new primitives | **DONE** |
| 8. Runtime invariant checker | DONE | `src/invariants.py` exists, called from `ephemeris.py` | **DONE** |

**Summary:** 7/8 stages DONE. Stage 2 (verification tags) is non-blocking (13% tagged, all pipeline modules done).

### 1.6 Pipeline Layer Build Status (ARCHITECTURE_CURRENT_VS_TARGET.md)

> This replaces the old 10-layer model. The new architecture has 8 layers (see architecture doc).

| Layer | Description | Status | Evidence |
|-------|------------|--------|----------|
| L1 | Astronomy (ephemeris) | **DONE** | Existed pre-G1 |
| L2 | ChartContext (5-tier derived facts) | **DONE (G1)** | `build_chart_context()`, 2.7ms, auto-built by `score_chart()` |
| L3 | Unified rule evaluation | **DONE (G2+G3)** | `evaluate_all_rules()`, 26 scoring + 7,466 corpus rules → `EvalResult` |
| L3a | Weight store (versioned) | **DONE (G4)** | `WeightStore`, 3 version axes, JSON persistence |
| L4 | Convergence | **DONE (G5)** | `converge()`, 7 channels, independent counting, contra-indicators |
| L5 | Temporal probability | **DONE (G6)** | `time_project()`, 7 timing systems, P(year), peak windows |
| L6 | Narrative synthesis | **NOT BUILT** | G7 — next on critical path |
| L7 | Verification + interaction | **NOT BUILT** | Phase A (20Q, life events) |
| L8 | Calibration + learning | **NOT BUILT** | Phase B (empirical feedback) |

**Summary:** 5/8 layers operational (L1-L5). L3a (weight store) is infrastructure. L6 (narrative) is next. L7-L8 are Phase A/B.

**Key metric shift:** OB-3 (raw scores) → OB-4 (convergence). Pipeline outperforms legacy by +18% average ρ across 4,832 charts.

### 1.7 Guardrail Enforcement

| Guardrail | Code refs | Enforced? |
|-----------|-----------|-----------|
| G01 (no 'prediction' framing) | 13 | Tests check language |
| G02 (no health/death timing) | 6 | Partial |
| G03 (DPDP/GDPR compliance) | 3 | Minimal |
| G04 (user_prior_prob) | 2 | Schema only |
| G05 (no 'certificate') | 0 | **NOT ENFORCED** |
| G06 (KP ayanamsha) | 41 | Enforced |
| G07 (20Q mandatory) | 1 | Comment only |
| G08-G15 | 0 each | **NOT ENFORCED** |
| G16 (cluster size) | 1 | Comment only |
| G17 (no PyJHora) | 12 | Enforced |
| G18-G21 | 0-2 | **NOT ENFORCED** |
| G22 (OSF pre-register) | 30 | Test checks |
| G23-G24 | 2-3 | Minimal |

**Summary:** 3 guardrails meaningfully enforced (G06, G17, G22). 15/24 have zero or comment-only code references. Most guardrails are Phase A/B concerns (consumer-facing features that don't exist yet).

### 1.8 Document Sprawl

| Document | Lines | Role | Current? |
|----------|-------|------|----------|
| docs/MEMORY.md | 297 | State tracker | Yes (S318+) |
| MEMORY.md (root) | 261 | State tracker | **STALE (S160 era)** |
| docs/CHANGELOG.md | 1,904 | Session history | Yes |
| CHANGELOG.md (root) | 294 | Session history | **STALE** |
| docs/ARCHITECTURE.md | 565 | Architecture (v1) | **SUPERSEDED by v11** |
| v11 architecture | 741 | Architecture (v2) | Yes |
| v11 execution plan | 293 | Execution plan | Yes |
| docs/PREDICTION_PIPELINE.md | 291 | Pipeline design | **ASPIRATIONAL (1/10 built)** |
| docs/ROADMAP.md | 288 | Session targets | Partially current |
| docs/s318_deep_audit.md | 1,241 | Bug audit | Yes (all bugs closed) |
| docs/SESSION_LOG.md | 739 | Session history | Yes |
| docs/GUARDRAILS.md | (24 items) | Safety | Yes (but mostly unenforced) |
| lessons_learned.md | (20 lessons) | Process | Yes |
| core_principles.md | (18 principles) | Process | Yes |
| docs/RULE_CONTRACT_V2.md | 144 | Encoding schema | Yes |
| docs/PHASE1B_RULE_CONTRACT.md | 308 | Encoding schema (extended) | Overlaps V2 contract |
| docs/ENCODING_PROTOCOL_V2.md | 201 | Encoding process | Overlaps CLAUDE.md |

**Key contradictions:**
1. Root MEMORY.md (261 lines, S160-era) contradicts docs/MEMORY.md (297 lines, S318+)
2. ARCHITECTURE.md describes 3-layer convergence model; v11 describes 5-layer pipeline — v11 is current
3. PREDICTION_PIPELINE.md describes 10 build layers; 9/10 are not built — it's a design doc, not a status doc
4. Two rule contracts (RULE_CONTRACT_V2.md + PHASE1B_RULE_CONTRACT.md) overlap significantly

---

## Section 2: What the System Is (Architecture, ONE Version)

### 2.1 The Pipeline (5 layers, from v11)

```
Layer 1: ASTRONOMY       Swiss Ephemeris → planetary positions (immutable)
Layer 2: CONVENTIONS      House system, ayanamsha, MT ranges, combustion orbs (configurable)
Layer 3: DERIVED FACTS    Lordships, aspects, dignity, friendship, avasthas (computed once)
Layer 4: RULE EVALUATION  Encoded rules tested against derived facts → fired/not-fired
Layer 5: AGGREGATION      Scores, groupings, verse citations, school attributions → output
```

### 2.2 How the Two Architecture Models Reconcile

The older 3-layer convergence model (ARCHITECTURE.md + PREDICTION_PIPELINE.md) and v11's 5-layer pipeline are **complementary, not contradictory**:

- **v11 Layers 1-3** = the computation substrate (what's computed)
- **v11 Layer 4** = where the older model's Layer I (classical convergence) and Layer II (structural convergence) operate
- **v11 Layer 5** = where the older model's aggregation and concordance produce final output
- **The older Layer III** (empirical convergence) = Phase B concern, explicitly deferred by v11

**DECISION:** v11 governs implementation. The convergence model's Layer I/II concepts (concordance, promise/capacity/delivery) are DESIGN TARGETS within v11's Layer 4-5, to be wired when the basic chain works. Layer III (Bayesian feedback) is Phase B (S1400+).

### 2.3 The C → A → B Phasing

| Phase | Goal | Scope | Status |
|-------|------|-------|--------|
| **Phase C** (Knowledge System) | Encode 90%+ BPHS as computable rules | Corpus encoding + rule engine + validation | IN PROGRESS |
| **Phase A** (Practitioner Tool) | Query interface for astrologers | UI, API, verse-traced predictions | NOT STARTED (S800+) |
| **Phase B** (Research Platform) | Empirical calibration against outcomes | Bayesian posteriors, outcome tracking | NOT STARTED (S1400+) |

**Phase C needs exactly 3 things:**
1. Canonical primitives (one implementation per concept, BPHS-verified) — **DONE** (v11 Stage 5)
2. A rule engine that evaluates encoded rules against charts — **DONE** (rule_firing.py + inference.py)
3. Validation gates that prevent encoding errors — **DONE** (v2_scorecard, verse_audit, condition_modifier_audit)

**Phase C's MISSING piece:** The rule engine output (inference.py) is not consumed by the scoring pipeline (scoring.py/scoring_v3.py). The three prerequisites exist but aren't connected.

### 2.4 The Scoring Engine Today

**RESOLVED (W0, 2026-04-12).** The two scoring engines have been consolidated:

- `multi_axis_scoring.py:evaluate_house_detailed()` is the **single canonical rule implementation** (26 rules: R01-R24 + D6 Avastha + WL War Loser)
- `scoring.py:score_chart()` is a **thin wrapper** that calls `evaluate_house_detailed()` for D1 and wraps results in ChartScores/HouseScore/RuleResult format
- Uses **functional benefic/malefic** classification (BPHS Ch.34) everywhere
- All weights aligned, R13/R16 mitigation per BPHS Ch.11 applied
- OB-3 median ρ ≈ 0.42 (unchanged from pre-consolidation)

**What scoring_v3.py orchestrates:**
- multi_axis_scoring (the 23 rules across 5 axes)
- dasha_scoring (temporal sensitization)
- LPI (7-layer weighted prediction index)
- divisional charts (vimshopaka)
- avasthas v2, raja yogas, neecha bhanga, rasi drishti, bhavat bhavam, arudha padas

**What it does NOT use:** corpus rules, rule_firing output, inference output, concordance, promise_engine.

### 2.4b Duplication Inventory (30 clusters, S326 audit → W0 consolidation)

**W0 COMPLETE (2026-04-12).** All identified duplication clusters resolved across 3 sessions (W0-1 through W0-15). Total: ~1,120 lines removed, 43 files touched, 15 commits. Zero OB-3 regression.

| Cluster | Status | Commit |
|---------|--------|--------|
| Scoring engines (scoring.py vs multi_axis) | **RESOLVED** — single `evaluate_house_detailed()` | W0-1 |
| Aspect functions (4 copies) | **RESOLVED** — 3 delegates to canonical | W0-2 |
| Dignity tables (6 files) | **RESOLVED** — all import from dignity.py | W0-3 |
| Friendship tables (3 files) | **RESOLVED** — all import from dignity._NAISARGIKA | W0-3 |
| Sign lords (5 files) | **RESOLVED** — all import from constants.SIGN_LORDS | W0-3 |
| Sign type constants (5 files) | **RESOLVED** — all import from constants.py | W0-4 |
| Navamsha D9 (nakshatra.py) | **RESOLVED** — imports from varga.py | W0-4 |
| Nakshatra names (panchanga.py) | **RESOLVED** — imports from constants.py | W0-4 |
| House domain mapping (app.py) | **RESOLVED** — imports from scoring.py | W0-4 |
| D9 formula in panchanga.py | **RESOLVED** — dead wrong code deleted (180/360° disagree) | W0-5 |
| rule_firing.py dignity tables | **RESOLVED** — imports from constants.py + extends with Rahu/Ketu | W0-6 |
| rule_firing.py _SPECIAL_ASPECTS | **RESOLVED** — deleted (dead code after W0-2) | W0-6 |
| nakshatra.py NAKSHATRA_NAMES | **RESOLVED** — imports from constants.py | W0-6 |
| nakshatra.py _D9_START | **RESOLVED** — deleted (unused after varga import) | W0-6 |
| _EXALT_LON/_DEBIL_LON tables | **RESOLVED** — canonical in constants.py, both files import | W0-7 |
| D9 in sapta_varga + divisional_charts | **RESOLVED** — both import from varga.py | W0-8 |
| Graha yuddha (planetary_state duplicate) | **RESOLVED** — orphaned duplicate deleted | W0-9 |
| Nabhasa yogas (yogas_extended reimpl) | **RESOLVED** — delegates to canonical nabhasa_yogas.py (7→32 yogas) | W0-10 |
| Chara karakas (chara_karak duplicate) | **RESOLVED** — delegates to chara_karaka_config.py | W0-11 |
| Karakamsha (chara_karaka_config duplicate) | **RESOLVED** — deleted, single impl in multi_lagna.py | W0-12 |
| Longevity (ayurdaya.py wrong formulas) | **RESOLVED** — ayurdaya delegates to longevity.py (Pindayu/Nisargayu were wrong) | W0-13 |
| Chandrabala H5 bug | **RESOLVED** — H5 removed from good positions per Phaladeepika | W0-14 |

**Intentionally separate (confirmed not-duplicates):**
- Vimshopaka: divisional_charts.py (16-varga Shodasavarga) vs sapta_varga.py (7-varga Sapta) — different classical systems
- Tarabala/Chandrabala: transit_quality_advanced.py (detailed analytical) vs muhurtha_complete.py (binary muhurtha) — different use cases, both have callers

**All W0 items resolved.** Remaining items are structurally different types, not duplications:
- Graha yuddha: fixed to use latitude-based winner per BPHS Ch.28 (W0-18)
- Yoga result types reduced 6→3: YogaResult (canonical), NabhasaYoga (domain-specific fields), RajYogaResult (structurally different). GrahaYogaResult/PluginYogaResult/NamedYogaResult unified into YogaResult (W0-17, W0-19).

**Canonical Source Map** added to CLAUDE.md (W0-15) — prevents future duplication by making canonical modules discoverable at session start.

### 2.5 Canonical Primitives (verified)

9 modules have `_VERIFICATION` tags:
- `argala.py`, `ashtakavarga.py`, `dignity.py`, `divisional_charts.py`
- `house_lord.py`, `panchanga.py`, `shadbala.py`, `sputa_drishti.py`, `varga.py`

104 modules lack verification tags (non-blocking, quality improvement).

### 2.6 Shadbala Gaps (9 open)

1. Saptavargaja Bala — uses static dignity instead of Panchadha per varga (highest impact)
2. Ojhayugma Bala — missing Navamsa check
3. Chesta Bala — wrong formula (needs mean longitude, not speed)
4. Nathonnata Bala — binary instead of continuous
5. Abda/Masa Bala — simplified lord computation
6. Ayana Bala — simplified to binary (needs declination)
7. Drik Bala — 1/4 adjustment refinement
8. Bhava Bala — not audited
9. Per-component minimums — low priority

---

## Section 3: What the System Needs (Prioritized, Sequenced)

### 3.1 The Critical Path

> **SUPERSEDED:** The W0/W1/W2/W3 work item model was replaced on 2026-04-13 by the
> full architecture redesign in `docs/ARCHITECTURE_CURRENT_VS_TARGET.md`.
> That document is the golden source for all work planning.

**W0 is DONE** (45 commits, 66 files, 1,096 net lines removed). All computational
primitives unified. All duplication resolved. Three divergences between rule_firing
and scoring engine fixed (natural malefic, dignity, functional classification).

**The new critical path** (from ARCHITECTURE_CURRENT_VS_TARGET.md):

```
G1 → G2 → G3 → G4 → G5 → G6 → Resume encoding
ChartCtx  Rules   Unified  Weight  Convergence  Temporal
          to data engine   store   layer        probability
```

Encoding resumes after G6 — when the e2e pipeline produces verse-cited predictions
with convergence confirmation, timing, and traceability. Not before.

See `docs/ARCHITECTURE_CURRENT_VS_TARGET.md` for:
- Full 8-layer target architecture
- 13 structural gaps + 14 engineering quality criteria
- Dependency Gantt chart with critical path and parallel tracks
- Detailed exit criteria per item

### 3.2 STOP List

| Item | Why NOT |
|------|---------|
| Encode BPHS chapters before G6 complete | Pipeline must produce verifiable predictions (convergence + timing + verse trace) before encoding resumes. "Does it fire?" is not validation. |
| Tactical wire (inference→scoring) without ChartContext | Adds another parallel result to a flat dispatcher. Doesn't fix 135× recomputation or two-engine split. |
| Build Phase A features before Phase C pipeline | No user concept, no predictions to show. Foundation must produce predictions first. |
| Build Phase B calibration before Phase A feedback | No outcome data to calibrate against without user feedback. |
| Write more governance/planning documents | ARCHITECTURE_CURRENT_VS_TARGET.md is the golden source. Don't fragment it. |

---

## Section 4: How to Do the Work (Process)

### 4.1 Session Types (NEVER MIX)

**Encoding session:** Read PDF → verse audit → encode rules → validate → commit. No framework changes.
**Governance session:** Build controls, update protocols, fix infrastructure. No encoding.
**Wiring session:** Connect existing modules, validate with tests. No encoding, no new modules.

### 4.2 Encoding Protocol (5 gates)

```
Gate 0: OCR Verification (scanned PDFs only)
  → Verify 3 verses against PDF image
  → Store in data/ocr/

Gate 1: Verse Audit
  → Read every sloka + commentary
  → Create data/verse_audits/chN_audit.json
  → Apply ENCODING_GRANULARITY.md (every if/unless/except = separate claim)

Gate 2: Audit Review (who audits the auditor?)
  → Claim count matches verse complexity
  → Contrary mirrors identified
  → Entity targets noted (not defaulted to native)
  → Keyword scanner: every "if/unless/except" has a corresponding claim

Gate 3: Encode from Audit
  → Each claim → one rule
  → Run tools/verse_audit.py --compare → zero unencoded claims

Gate 4: Validate
  → Run tools/v2_scorecard.py --file <chapter_file> → 0 errors, 0 warnings
  → Run full test suite + ruff check → all pass
  → Commit
```

### 4.3 Session Start Protocol

1. Read `docs/PROJECT_STRATEGY.md` (this document)
2. Read `CLAUDE.md` (session protocol, project context)
3. If encoding: read `docs/RULE_CONTRACT_V2.md`
4. Check `lessons_learned.md` for patterns relevant to today's work
5. Verify controls exist for planned work (Principle #4)

### 4.4 Session End Protocol

1. Did rework happen? → Add lesson to `lessons_learned.md`
2. Did an audit control catch an error? → Add lesson
3. Did the user correct you? → Add lesson
4. Update `lessons_learned.md` with any new entries
5. If a new pattern emerged → update `core_principles.md`

### 4.5 Quality Tools

| Tool | Purpose | When to run |
|------|---------|-------------|
| `tools/v2_scorecard.py --file F` | Validate single chapter | After encoding each chapter |
| `tools/v2_scorecard.py --v2-only` | V2 corpus quality | Start of encoding sessions |
| `tools/v2_scorecard.py --all` | Full corpus overview | Health assessments |
| `tools/rule_grader.py` | L0-L5 maturity distribution | Health assessments |
| `tools/condition_modifier_audit.py` | Flag misclassified conditions | After encoding, before commit |
| `tools/validate_constants.py` | Constants in canonical location | After touching calculations/ |
| `tools/import_boundary_check.py` | Layer boundary enforcement | After adding imports |
| `tools/reachability_analysis.py` | Dead code detection | Health assessments |
| `tools/rework_detector.py` | Detect encoding rework | Session end |
| `tools/ob3_calibrate.py --report` | Empirical signal measurement | After wiring changes |
| `tools/verse_audit.py --compare` | Audit-vs-encoding coverage | Gate 3 of encoding |

---

## Section 5: Lessons, Guardrails, and Principles

### 5.1 Active Lessons (from lessons_learned.md)

| # | Lesson | Has code control? |
|---|--------|-------------------|
| L001 | Fix now, not later | Yes: rework_detector.py SOURCE_DRIFT |
| L002 | Warnings are defects | Yes: pre-push hook blocks warnings |
| L003 | Never batch-automate encoding | Behavioral |
| L004 | 'general' not default entity target | Yes: V2ChapterBuilder T1-14 to T1-17 |
| L005 | Split mixed-entity rules | Yes: V2ChapterBuilder T1-15/T1-16 |
| L006 | Never weaken controls | Behavioral |
| L007 | Shortcut-driven = expensive path | Yes: 4-moment gate system |
| L008 | Don't propose premature closure | Yes: pre-commit hook blocks closure language |
| L009 | Context ≠ shortcut justification | Behavioral |
| L010 | Self-detection fails | Yes: V2ChapterBuilder gates |
| L011 | Read text, not tables | Yes: 102 regression tests |
| L012 | No parallel infrastructure without discussion | Behavioral |
| L013 | Translator notes ≠ verse text | Yes: clean sweep protocol |
| L014 | Overestimating cost feeds closure | Behavioral |
| L015 | Never defer without approval | Behavioral |
| L016 | Search before you build | Behavioral |
| L017 | Don't execute stale plans | Behavioral (5-min diagnostic required) |
| L018 | "Test-only" is a question, not a verdict | Yes: /codebase-surgery forces verdict |
| L019 | Coverage means all layers | Behavioral |
| L020 | Removing silent catch = bug discovery | Behavioral |

**Open loops (behavioral lessons without controls):** L003, L006, L009, L012, L014, L015, L016, L017, L019. These are judgment calls, not automatable.

### 5.2 Guardrail Status

**Enforced (3):** G06 (KP ayanamsha), G17 (no PyJHora), G22 (OSF pre-register)
**Partially enforced (4):** G01, G02, G03, G04
**Not enforced (17):** G05, G07-G16, G18-G21, G23-G24

Most unenforced guardrails gate Phase A/B consumer features that don't exist yet. They should be enforced when those features are built, not before.

### 5.3 Core Principles (from core_principles.md)

1. Long-term over quick
2. Nullify rework (gates before work)
3. Right over easy
4. Controls before work
5. Measure before claiming
6. System enforces, not person
7. Radical transparency
8. Source fidelity
9. Exhaust the problem before proposing
10. Close the feedback loop

Plus 8 encoding-specific principles (P11-P18): fix now, warnings = defects, one entity one rule, never weaken controls, user manages sessions, diagnose before executing, every file gets a verdict, coverage means all layers.

---

## Section 6: Decisions and Rationale

### D1: Is the corpus connected to the engine?

**FINDING: NO.** The scoring pipeline (`scoring.py` → 22 hardcoded rules) and the corpus pipeline (`rule_firing.py` → `inference.py` → 654 V2 rules) are completely separate. They share no code path. The corpus pipeline terminates at the `/charts/{id}/analysis` API endpoint. The scoring pipeline terminates at `/charts/{id}/scores`.

**DECISION:** This is the #1 priority to fix (W1). Wire `inference.py` output into `scoring_v3.py` so corpus rules affect house scores.

### D2: Is the 25,000-rule target meaningful?

**FINDING:** At 654 V2 rules after ~20 encoding sessions (~33 rules/session), reaching 25,000 V2 rules requires ~740 more sessions. But if the scoring engine ignores the corpus, 25,000 achieves nothing.

**DECISION:** The 25,000 target is a PHASE C completion criterion, not a near-term goal. The near-term goal is: "score charts using corpus rules" (W1). The number of rules matters AFTER the bridge is wired. Encoding should resume AFTER W1+W2 confirm rules improve scores.

### D3: Are the 6,807 L1 (prose) rules useful?

**FINDING:** L1 rules have no structured conditions, no signal_groups, no computable form. They cannot be fired by rule_firing.py. Counting them in "7,466 rules encoded" creates false confidence.

**DECISION:** L1 rules are catalog entries, not predictions. They have historical value (verse references, descriptions) but zero computational value. Progress should be measured in L3+ rules only. **Current real progress: 654 rules (2.6%), not 7,466 (29.9%).**

### D4: Are the 3 convergence layers built?

**FINDING:**
- Layer I (Classical Convergence): Partially built. rule_firing computes concordance_score but it's unused by scoring. Multi-school evaluation requires multiple texts encoding the same verses — currently 0 non-BPHS texts have V2 rules.
- Layer II (Structural Convergence): promise_engine.py exists, computes Promise/Capacity/Delivery. Called by guidance_api, not by scoring.
- Layer III (Empirical Convergence): Not built. No feedback schema, no Bayesian pipeline.

**DECISION:** Layer I concordance and Layer II promise_engine are Phase A concerns (need multiple texts + consumer features). Layer III is Phase B. For Phase C, the priority is the basic chain: corpus → scoring.

### D5: Which architecture model governs?

**DECISION:** v11's 5-layer pipeline governs implementation. The convergence model's concepts (concordance, promise/capacity/delivery, Bayesian posteriors) are design targets mapped onto v11's layers. The convergence model is not wrong — it's aspirational. v11 is operational.

### D6: Is the governance overhead justified?

**FINDING:** 126 markdown documents. 256 encoding commits, 316 surgery/fix commits, 202 docs commits. Roughly 26% of commits are documentation. The 90/10 rule (90% deliverables / 10% meta-work) has been violated in the macro view.

**DECISION:** Governance infrastructure (tools, gates, scorecards) has been valuable — it catches real errors. But governance DOCUMENTS (strategy docs, protocol specs, roadmaps) have proliferated beyond utility. This document (PROJECT_STRATEGY.md) is the consolidation. No new governance documents should be created. Use existing tools.

### D7: What would happen if you deleted src/corpus/?

**FINDING:** The `/charts/{id}/analysis` endpoint would break. The `/charts/{id}/scores` endpoint (the main scoring path) would be unaffected. OB-3 calibration would be unaffected. The primary user-visible behavior change: zero.

**DECISION:** This confirms W1 is the #1 priority. The corpus is a library that no one reads. Build the reader.

### D8: Is the session-based approach causing this problem?

**FINDING:** Yes, partially. Each session optimized for its own deliverable (encode chapter X, fix bug Y, build tool Z). The meta-objective — "make chart scores better using encoded knowledge" — requires connecting the pieces. 325 sessions of local optimization without a single session of integration.

**DECISION:** The next session (W1) is explicitly an integration session. No encoding, no governance, no new features. Connect the existing pieces.

### D9: What is the single most valuable next step?

**DECISION:** **W1: Wire inference.py output into scoring_v3.py.** This is the only action that makes all past encoding sessions retroactively productive and all future encoding sessions inherently productive. Estimated effort: 1-2 sessions.

**Defense:** Every other candidate (more encoding, re-encoding L1s, concordance, guardrails) depends on W1 to produce value. W1 has zero dependencies (W0 blocker removed). It unblocks everything. The code for both sides of the bridge already exists — rule_firing.py produces FiredRule objects, scoring_v3.py orchestrates modules. The missing piece is a function call.

**Devil's advocate:** What if the 654 rules make scores WORSE? That's what W2 (OB-3 validation) answers. But we can't answer that question without W1.

### D10: Did the W0 scoring consolidation change empirical signal?

**FINDING:** OB-3 median ρ ≈ 0.42 before and after consolidation. Despite switching from natural to functional benefic classification, aligning R16/R22 weights, and adding R13/R16 BPHS mitigations, the net impact on 4,832 diverse charts was negligible (±0.005 per house).

**INTERPRETATION:** The hardcoded R01-R24 rules are robust to these classification refinements at scale. Functional benefics change which planets trigger R02/R09 for specific lagnas, but across 4,832 charts with all 12 lagnas represented, the positive and negative shifts cancel. This validates the consolidation — the behavioral change was BPHS-correct without regressing the signal.

---

## Appendix A: Document Supersession Map

| Document | Status | Superseded by |
|----------|--------|---------------|
| docs/ARCHITECTURE.md | Historical reference | Section 2 of this document |
| docs/PREDICTION_PIPELINE.md | Historical reference (aspirational) | Section 2 of this document |
| docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md | Historical reference | Section 2 of this document |
| docs/superpowers/specs/2026-04-07-v11-execution-plan.md | Historical reference | Section 3 of this document |
| docs/ROADMAP.md | Historical reference | Section 3 of this document |
| MEMORY.md (root) | **STALE — delete or redirect** | docs/MEMORY.md |
| CHANGELOG.md (root) | **STALE — merge into docs/** | docs/CHANGELOG.md |
| docs/s318_deep_audit.md | Historical reference (all bugs closed) | Section 1.5 of this document |

**Documents that REMAIN authoritative:**
- `CLAUDE.md` — session protocol, project context (updated to reference this document)
- `docs/RULE_CONTRACT_V2.md` — encoding schema (canonical)
- `docs/ENCODING_GRANULARITY.md` — rule granularity definition
- `docs/GUARDRAILS.md` — guardrail definitions (enforcement status in Section 5.2)
- `lessons_learned.md` — lesson entries (summary in Section 5.1)
- `core_principles.md` — principle entries (summary in Section 5.3)
- `docs/CORPUS_MANIFEST.json` — rule inventory
- `tools/INDEX.md` — tool inventory
- `docs/BUGS.md` — bug tracker (2 open items, both non-code)

## Appendix B: How to Update This Document

When running `/health-assessment` or `/health-check`:
1. Re-run all Phase 0 diagnostic commands
2. Update Section 1 tables with new numbers and date
3. Check if any W-items in Section 3 have been completed → update status
4. If new work items discovered → add to Section 3 with dependency analysis
5. If a decision in Section 6 needs revisiting → add a new D-entry, don't modify old ones
