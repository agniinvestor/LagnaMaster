# PROJECT_STRATEGY.md — LagnaMaster Golden Source

> **This is the single authoritative document for project state, architecture, and next steps.**
> Every session reads THIS instead of 10+ partial documents.
> Last verified: 2026-04-12 (W0 complete — all 30 duplication clusters resolved).

---

## Section 1: Where We Are (Diagnostic Facts)

### 1.1 Core Health Dashboard

| Metric | Value | Command | Last verified |
|--------|-------|---------|---------------|
| Tests passing | 14,811 | `.venv/bin/pytest tests/ -q --tb=short` | 2026-04-12 |
| Tests skipped | 210 | (same) | 2026-04-12 |
| Tests xfailed | 360 | (same) | 2026-04-12 |
| Lint errors | 0 | `.venv/bin/ruff check src/ tests/` | 2026-04-12 |
| Constants validated | PASS | `tools/validate_constants.py` | 2026-04-12 |
| Import boundaries | PASS (9 documented exceptions) | `tools/import_boundary_check.py` | 2026-04-12 |
| Reachable src/ files | 276/280 | `tools/reachability_analysis.py` | 2026-04-12 |
| Tools-only files | 4 | (same) | 2026-04-12 |
| Truly dead files | 0 | (same) | 2026-04-12 |
| Silent exception handlers | 8 | manual scan | 2026-04-12 |
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

The designed data flow is: corpus rules → rule_firing.py → inference.py → scoring → API/UI.

| # | Link | Architecture says | Code shows | Status |
|---|------|-------------------|-----------|--------|
| 1 | Corpus → rule_firing | rule_firing loads corpus and fires rules | `evaluate_chart()` calls `build_corpus()`, iterates rules | **EXISTS** |
| 2 | rule_firing → inference | inference calls evaluate_chart | `inference.py` imports `evaluate_chart`, `FiredRule` | **EXISTS** |
| 3 | inference → scoring | scoring_v3 uses inference output | **Neither scoring.py nor scoring_v3.py imports corpus, rule_firing, or inference** | **NOT WIRED** |
| 4 | Concordance scoring | Multi-school concordance computed | `concordance_score` field exists in rule_firing, populated as fraction. Not consumed by any scoring path | **COMPUTED, UNUSED** |
| 5 | Promise/Capacity/Delivery | promise_engine feeds scoring | `promise_engine.py` exists, called by `guidance_api.py` only. Not called by scoring.py or scoring_v3.py | **EXISTS, NOT WIRED** |
| 6 | Empirical feedback | Layer III calibrates Layer I | No feedback schema, no Bayesian pipeline, no posterior updates in production | **NOT BUILT** |
| 7 | Hardcoded vs corpus | scoring.py uses corpus rules | `scoring.py` evaluates R01-R24 (hardcoded). Does NOT consume corpus | **HARDCODED** |

**Where the chain breaks:** Link 3. The corpus pipeline (rule_firing → inference) terminates at the `/charts/{id}/analysis` API endpoint (`main.py:1000`). The scoring pipeline (scoring.py → scoring_v3.py) is completely separate and uses only 22 hardcoded rules (R01-R24).

**Consequence:** The 654 V2 rules do NOT affect chart scores. OB-3 calibration measures only the 22 hardcoded rules.

### 1.4 OB-3 Empirical Signal (hardcoded rules only)

| House | Outcome category | Spearman ρ | n |
|-------|-----------------|------------|---|
| House | Aggregate ρ | Verified |
|-------|-------------|----------|
| H01 | +0.459 | 2026-04-12 (post W0-14) |
| H03 | +0.447 | 2026-04-12 |
| H05 | +0.474 | 2026-04-12 |
| H07 | +0.474 | 2026-04-12 |
| H09 | +0.425 | 2026-04-12 |
| H10 | +0.389 | 2026-04-12 |

**Median ρ ≈ 0.45.** This is the baseline using 26 hardcoded rules (R01-R24 + D6 Avastha + WL War Loser). Unchanged through all W0 consolidation (no regression). Wiring 654 corpus rules should improve this — if it doesn't, the corpus rules are wrong.

### 1.5 v11 Execution Plan Stage Status (verified against code)

| Stage | v11 claims | Code shows | Verified status |
|-------|-----------|-----------|----------------|
| 1. Fix wrong formulas | ~95% | All C01-C20 bugs fixed (confirmed in git) | **DONE (100%)** |
| 2. Tag verification levels | Partial | 9 files tagged, 104 untagged | **8% done** |
| 3. Module registry + enforcer | DONE | Both `MODULE_REGISTRY.py` + `import_boundary_check.py` exist, pass clean | **DONE** |
| 4. Silent exception handlers | ~84% | 8 silent handlers remain (down from 143) | **~94% done** |
| 5. Canonical primitives | DONE | `validate_constants.py` passes, 79 files refactored | **DONE** |
| 6. Delete dead code | ~10% | Reachability: 0 truly dead files, 4 tools-only | **DONE (for dead files)** |
| 7. Wire missing connections | DONE | R24 dignity wired in scoring.py, 2 new primitives | **DONE** |
| 8. Runtime invariant checker | DONE | `src/invariants.py` exists, called from `ephemeris.py` | **DONE** |

**Summary:** 5/8 stages DONE. Stage 1 is also done (all C-bugs fixed). Stage 2 (verification tags) is non-blocking. Stage 4 has 8 remaining silent handlers.

### 1.6 10-Layer Build Status (PREDICTION_PIPELINE.md)

| Layer | Description | Status |
|-------|------------|--------|
| L1 | Birth time sensitivity | NOT BUILT |
| L2 | 20Q personality verification | NOT BUILT |
| L3 | Conditional weight functions | NOT BUILT |
| L4 | Multi-school concordance | COMPUTED (in rule_firing), UNUSED by scoring |
| L5 | Bayesian posterior distributions | NOT BUILT |
| L6 | Dasha temporal model | BUILT + WIRED (scoring_v3 calls apply_dasha_scoring) |
| L7 | Autobiography date anchoring | NOT BUILT |
| L8 | Signal isolation | NOT BUILT |
| L9 | Chart clusters | NOT BUILT |
| L10 | Empirical weight updates | NOT BUILT |

**Summary:** 1/10 layers operational (L6 Dasha). L4 concordance is computed but unused. 8/10 not built.

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

```
Consolidate engines  ──→  Wire corpus → scoring  ──→  Validate with OB-3  ──→  Encode
       (W0)                      (W1)                       (W2)                (W3+)
```

**Everything below is ordered by this dependency chain.** Items that don't block the critical path are marked with their urgency.

### 3.2 Work Items (dependency-ordered)

#### CRITICAL PATH (blocks all encoding ROI)

| # | Item | Why it matters | Depends on | Unblocks | Effort | Status |
|---|------|---------------|-----------|----------|--------|--------|
| W0 | **Consolidate engines + unify computational primitives** | 112/112 modules audited. ~1,100 net lines removed, 64 files, 39 commits. All duplication resolved. 3 bugs fixed (ayurdaya formulas, chandrabala H5, upapada exception). 3 computational divergences unified (natural malefic → dignity.is_natural_malefic, dignity → dignity.compute_dignity, functional roles → KNOWN_FUNCTIONAL_MALEFICS table). Overlap analysis: corpus+hardcoded rules are complementary, not conflicting (12/26 hardcoded rules have zero corpus equivalent). Canonical Source Map in CLAUDE.md. | None | W1 | — | **DONE** |
| W1 | **Wire inference.py output into scoring_v3.py** | Without this, 654 V2 rules are inert data. The corpus→engine chain exists (Links 1-2) but terminates before scoring. This is the single highest-leverage fix. | W0 | W2, W3, all encoding | 1-2 sessions | NOT STARTED |
| W2 | **Run OB-3 with corpus-aware scoring, compare to baseline** | Measures whether 654 rules improve ρ over 22 hardcoded rules. If ρ improves, the architecture works. If not, the rules are wrong. | W1 | W3 (go/no-go) | 1 session | NOT STARTED |
| W3 | **Resume BPHS encoding (Ch.26+)** | Only productive AFTER W1+W2 confirm corpus rules improve scores | W2 (positive result) | Corpus growth | Ongoing | BLOCKED |

#### HIGH PRIORITY (non-blocking but high value)

| # | Item | Why it matters | Depends on | Effort | Status |
|---|------|---------------|-----------|--------|--------|
| W4 | Fix 24 condition_modifier_audit flags | Medium-confidence flags in existing V2 rules — potential encoding errors | None | 1 session | NOT STARTED |
| W5 | Fix 9 Shadbala gaps (Saptavargaja, Chesta, Ayana first) | Shadbala feeds dignity + strength, which feeds scoring. Wrong Shadbala = wrong scores | None | 2-3 sessions | NOT STARTED |
| W6 | Wire promise_engine into scoring_v3 | Promise/Capacity/Delivery (Layer II) is built but unwired. Wiring it adds structural convergence | W1 | 1 session | NOT STARTED |
| W7 | Re-encode 5 L2 rules to L3 | 5 Saravali rules with quality gaps (no commentary, non-canonical signal groups) | None | <1 session | NOT STARTED |

#### MEDIUM PRIORITY (quality improvements)

| # | Item | Why it matters | Depends on | Effort | Status |
|---|------|---------------|-----------|--------|--------|
| W8 | Tag remaining 104 modules with `_VERIFICATION` | Quality audit trail, non-blocking | None | 2-3 sessions | 8% done |
| W9 | Fix remaining 8 silent exception handlers | Down from 143, diminishing returns | None | <1 session | 94% done |
| W10 | Reduce 45 TODO/FIXME markers in src/ | Code hygiene | None | 1-2 sessions | NOT STARTED |
| W11 | Consolidate root MEMORY.md into docs/MEMORY.md | Root version is stale (S160 era). Merge unique content, delete or redirect root | None | <1 session | NOT STARTED |
| W12 | Consolidate root CHANGELOG.md into docs/CHANGELOG.md | Same issue as W11 | None | <1 session | NOT STARTED |

#### LOW PRIORITY / PHASE A-B (defer)

| # | Item | Why it matters | Depends on | Effort | Status |
|---|------|---------------|-----------|--------|--------|
| W13 | Build concordance into scoring | L4 concordance is computed in rule_firing but unused. Needs multiple texts encoding same verses | W3 (enough cross-text rules) | 2+ sessions | NOT STARTED |
| W14 | Enforce guardrails G05-G15 in code | Consumer safety — but no consumers exist yet | Phase A | 3-5 sessions | NOT STARTED |
| W15 | Build Layer III (empirical feedback) | Bayesian posteriors, outcome tracking | Phase B | 10+ sessions | NOT STARTED |
| W16 | 20Q personality verification (Build L2) | User verification protocol | Phase A | 5+ sessions | NOT STARTED |
| W17 | Birth time sensitivity model (Build L1) | Monte Carlo confidence intervals | Phase A | 3+ sessions | NOT STARTED |

### 3.3 STOP List (explicitly do NOT do)

| Item | Why NOT |
|------|---------|
| Wire corpus before consolidation (W1 before W0) | **BLOCKER REMOVED** (W0 complete). All duplication clusters resolved. W1 is unblocked. |
| Encode more BPHS chapters before W0+W1+W2 | Rules are inert until the corpus→scoring bridge is wired. Encoding without wiring adds to a library no one reads. |
| Re-encode 6,807 L1 rules to L3 | Same reason — and the volume (6,807 rules) makes this a multi-month effort that produces zero value until W1 |
| Build guardrail enforcement (G05-G15) | These gate consumer-facing features. No consumers exist. Effort is premature |
| Build convergence Layer III (Bayesian) | Phase B concern (S1400+). No outcome data to calibrate against |
| Write more governance documents | 126 .md files exist. The problem is connection, not documentation |
| Update ROADMAP.md with new session numbers | PROJECT_STRATEGY.md replaces session-numbered roadmaps. Work items here are sequenced by dependency, not session number |
| Build 20Q, birth-time sensitivity, or chart clusters | Phase A/B concerns. Foundation must work first |
| Refactor ARCHITECTURE.md or PREDICTION_PIPELINE.md | This document supersedes both. They remain for historical reference |

### 3.4 Dependency DAG (visual)

```
               ┌──────────┐
               │W0: Consol│
               │idate     │
               │engines   │
               └────┬─────┘
                    │
               ┌────▼─────┐
               │ W1: Wire │
               │ corpus   │
               │ →scoring │
               └────┬─────┘
                    │
               ┌────▼─────┐
               │ W2: OB-3 │
               │ validate │
               └────┬─────┘
                    │
         ┌──────────┼──────────┐
         │          │          │
    ┌────▼───┐ ┌───▼────┐ ┌──▼───┐
    │W3: BPHS│ │W6: Wire│ │W13:  │
    │encoding│ │promise │ │concor│
    │Ch.26+  │ │engine  │ │dance │
    └────────┘ └────────┘ └──────┘

Independent (can start now, parallel with W0):
  W4: Fix 24 audit flags
  W5: Fix Shadbala gaps
  W7: Fix 5 L2→L3 rules
  W8-W12: Quality improvements
```

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
