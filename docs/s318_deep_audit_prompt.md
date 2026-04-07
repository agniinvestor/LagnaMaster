# S318 Deep Audit — Line-by-Line Code Reading

## HARD RULE: USE THE Read TOOL, NOT grep/Bash

S317 claimed "deep audit" but read 2.2% of the codebase. The rest was grepped. Grep finds PATTERNS (stale values, duplicate names). It does NOT find LOGIC BUGS (wrong formula, missing edge case, incorrect condition, off-by-one).

**Every file listed below must be opened with the Read tool and read in full.** Not grepped. Not sampled. Not skimmed via `head`. The Read tool, offset 0, reading to the end. For files over 200 lines, read in 200-line chunks until complete.

**Do NOT:**
- Run grep across files and call it "auditing"
- Read the first 30 lines and skip to the next file
- Commit findings after every file (batch per tier)
- Propose stopping before all tiers are read

**Evidence that reading works:** S317 read 15 modules and found bugs in ALL of them. Mars aspect wrong in multi_axis_scoring. Jupiter malefic for Cancer in functional_roles. Jaimini rasi drishti wrong in the dedicated module. Friendship values wrong in shadbala_patches. Every module read = bugs found. The remaining 110 modules are not cleaner — they just haven't been read.

## Context

S317 produced a full system audit (`docs/s317_full_audit.md`) that found 12 active contradictions, but only READ 2.2% of the codebase (3,600 of 166,500 lines). Every module that was actually read revealed bugs. The remaining 97.8% was grepped for patterns but not read for logic correctness.

## Task

Read EVERY .py file in the codebase line by line using the Read tool. For each file, check:

1. **Stale constants:** Does it define its own sign lords, exalt/debil, malefic/benefic, kendra/trikona/dusthana sets instead of importing from canonical sources (house_lord.py, dignity.py, rule_firing.py)?

2. **Logic correctness:** Does the computation match what it claims to compute? Check formulas against BPHS or cited source. Look for off-by-one, wrong sign (0-indexed vs 1-indexed), wrong modulo, missing edge cases.

3. **Contradictions with other modules:** Does this file compute the same thing as another file but differently? (Mars aspects, yogakarakas, functional malefics, dignity, nakshatra index, etc.)

4. **Error handling:** Does it swallow exceptions with `except Exception: return 0` or similar? Every such clause is a potential hidden bug.

5. **Source citations:** Does the code cite specific verses for its astrological claims? Uncited = unverified.

6. **Test coverage:** Is this module referenced by any test file?

7. **Dead code:** Functions defined but never called externally.

8. **Consumers:** Who imports this module? If a bug exists here, what downstream modules are affected?

## Known Contradictions Found in S317 (verify these propagate)

1. Mars aspects: scoring.py `{3,7}` CORRECT vs multi_axis_scoring `{3,9}` WRONG
2. Gentle signs: scoring.py has TWO sets that disagree in same file
3. Yogakarakas: 4 sources — functional_dignity (BPHS), functional_roles (dynamic), multi_lagna, scoring.py — Cancer differs across them
4. Functional malefics: functional_dignity vs functional_roles — Jupiter for Cancer differs. multi_axis_scoring uses the WRONG one (functional_roles)
5. Friendship: 4 copies (dignity.py, panchadha_maitri, friendship.py, sayanadi_full.py)
6. Rasi Drishti: jaimini_rashi_drishti.py says Aries aspects 11 signs (WRONG). extended_yogas.py says {4,7,10} (CORRECT)
7. Neecha Bhanga: dignity.py checks 6 conditions, extended_yogas checks 3
8. Nakshatra: 3 formulas, one documented as wrong in its own docstring
9. Saptavargaja: legacy SAPTAVARGAJA_VIRUPAS dict (corrected values) vs SAPTAVARGAJA_VIRUPAS_BPHS dict — both in shadbala.py
10. 107 except Exception clauses with zero logging

## Files to Read (prioritized by risk)

### Tier 1 — Core scoring path (API-facing, highest impact)
```
src/scoring.py (619 lines) — PRIMARY API scoring engine
src/calculations/multi_axis_scoring.py (588 lines) — internal scoring, has Mars bug
src/calculations/rule_firing.py (1,442 lines) — rule evaluation, 32 condition types
src/calculations/feature_decomp.py (587 lines) — feature extraction, has Mars bug
src/calculations/scoring_v3.py (218 lines) — v3 scorer
src/calculations/scoring_patches.py (351 lines) — patches, stale ASPECT_STRENGTH
src/calculations/scoring_v2.py (416 lines) — v2 scorer
```

### Tier 2 — Computation modules (produce values consumed by scoring)
```
src/calculations/dignity.py (837 lines) — S317 corrected, verify no remaining issues
src/calculations/shadbala.py (874 lines) — S317 major corrections
src/calculations/functional_roles.py (206 lines) — Jupiter-Cancer bug confirmed
src/calculations/functional_dignity.py (271 lines) — S317 BPHS-verified
src/calculations/panchadha_maitri.py (136 lines) — S317 verified
src/calculations/avasthas.py (336 lines) — S317 new
src/calculations/avastha_v2.py (102 lines) — S317 rewired
src/calculations/avastha.py (202 lines) — OLD, possibly conflicting
src/calculations/planet_avasthas.py (271 lines) — S138, even-sign bug fixed
src/calculations/sayanadi_full.py (256 lines) — has own relationship tables
src/calculations/sputa_drishti.py (301 lines) — S317 new BPHS drishti
src/calculations/bhava_bala.py (149 lines) — S317 corrected
src/calculations/friendship.py (142 lines) — separate friendship module
src/calculations/diagnostic_scorer.py (351 lines) — 0 tests, own tables
```

### Tier 3 — Yoga detection (major feature area)
```
src/calculations/extended_yogas.py (405 lines) — raja/dhana/viparita/NB, rasi drishti
src/calculations/yogas.py (524 lines) — 13 yoga types
src/calculations/yogas_extended.py (489 lines) — additional yogas
src/calculations/yogas_pvrnr.py (245 lines)
src/calculations/yogas_graha.py (168 lines)
src/calculations/yogas_additions.py (307 lines) — orphaned
src/calculations/nabhasa_yogas.py (256 lines) — 32 Nabhasa
src/calculations/yoga_strength.py (374 lines) — yoga grading
src/calculations/yoga_fructification.py (324 lines)
```

### Tier 4 — Dasha/timing (next encoding priority)
```
src/calculations/vimshottari_dasa.py (221 lines)
src/calculations/pratyantar_dasha.py (109 lines) — has own VIMSHOTTARI_YEARS copy
src/calculations/ashtottari_dasha.py (112 lines)
src/calculations/kalachakra_dasha.py (192 lines)
src/calculations/chara_dasha.py (128 lines)
src/calculations/dasha_activation.py (348 lines)
src/calculations/dasha_scoring.py (235 lines)
src/calculations/dasha_sandhi.py (69 lines)
src/calculations/shoola_dasha.py (160 lines)
src/calculations/drig_dasha.py (140 lines)
src/calculations/tara_dasha.py (143 lines)
src/calculations/yogini_dasha.py (111 lines)
src/calculations/lagna_kendradi_dasha.py (104 lines)
```

### Tier 5 — Specialized computation
```
src/calculations/ashtakavarga.py (362 lines)
src/calculations/nakshatra.py (206 lines) — canonical nakshatra, has warning about wrong formula
src/calculations/panchanga.py (376 lines)
src/calculations/divisional_charts.py (464 lines)
src/calculations/varga.py (405 lines)
src/calculations/sapta_varga.py (454 lines)
src/calculations/shodashavarga_bala.py (161 lines)
src/calculations/jaimini_rashi_drishti.py (142 lines) — CONFIRMED WRONG rasi drishti
src/calculations/jaimini_full.py (371 lines)
src/calculations/kp.py (441 lines)
src/calculations/kp_sublord.py (292 lines)
src/calculations/kp_full.py (257 lines)
src/calculations/kp_cuspal.py (258 lines)
src/calculations/longevity.py (247 lines)
src/calculations/ayurdaya.py (155 lines)
src/calculations/kundali_milan.py (447 lines)
src/calculations/varshaphala.py (497 lines)
src/calculations/muhurtha_complete.py (390 lines)
```

### Tier 6 — Infrastructure / support
```
src/calculations/house_lord.py (82 lines) — canonical, verified clean
src/calculations/planetary_state.py (370 lines)
src/calculations/confidence_model.py (309 lines)
src/calculations/inference.py (450 lines)
src/calculations/lpi.py (274 lines)
src/calculations/multi_lagna.py (261 lines)
src/calculations/domain_weighting.py (210 lines)
src/calculations/dominance_engine.py (247 lines)
src/calculations/promise_engine.py (183 lines)
src/calculations/pressure_engine.py (439 lines)
src/calculations/orb_strength.py (159 lines)
src/calculations/stronger_of_two.py (163 lines)
src/calculations/planet_chains.py (284 lines)
src/calculations/planet_effectiveness.py (169 lines)
src/calculations/chart_exceptions.py (234 lines)
src/calculations/conditional_weights.py (172 lines)
src/calculations/calc_config.py (199 lines)
src/calculations/config_toggles.py (107 lines)
src/calculations/contextual.py (111 lines)
src/calculations/rule_interaction.py (99 lines)
src/calculations/rule_plugin.py (172 lines)
src/calculations/school_rules.py (172 lines)
src/calculations/narrative.py (154 lines)
src/calculations/monte_carlo.py (257 lines)
src/calculations/scenario.py (122 lines)
src/calculations/empirica.py (227 lines)
```

### Tier 7 — Non-calculation src/
```
src/ephemeris.py (270 lines)
src/scoring.py (619 lines) — already in Tier 1
src/worker.py (359 lines)
src/auth.py (235 lines) — JWT hardcoded
src/cache.py (208 lines)
src/config.py (117 lines)
src/db.py (133 lines)
src/db_pg.py (275 lines)
src/db_timescale.py (82 lines)
src/db_vector.py (72 lines)
src/db_family.py (104 lines)
src/montecarlo.py (139 lines)
src/pdf_export.py (386 lines)
src/regression_snap.py (217 lines)
src/api/main.py (603 lines)
src/api/main_v2.py (~200 lines)
src/api/auth_router.py (~130 lines)
src/api/models.py (199 lines)
src/api/mobile_router.py (90 lines)
src/api/empirica_router.py (62 lines)
src/api/school_router.py (~100 lines)
src/ui/app.py (1,415 lines)
src/ui/chart_visual.py (282 lines)
src/ui/confidence_tab.py (236 lines)
src/ui/kundali_page.py (300 lines)
src/guidance/*.py (8 files, ~1,000 lines)
src/privacy/*.py (3 files, ~518 lines)
src/ci/*.py (4 files, ~637 lines)
src/feedback/*.py (3 files, ~332 lines)
src/interfaces/*.py (5 files, ~322 lines)
src/research/*.py (3 files, ~297 lines)
src/ml/*.py (1 file, ~87 lines)
```

### Tier 8 — Tests (are they testing correct things?)
```
197 test files — check each imports the RIGHT module version and asserts CURRENT correct values
```

### Tier 9 — Tools
```
31 active tools — check each uses current table values and imports from canonical sources
```

## Output Format

For each file, produce ONE line:
```
filename.py (N lines): [CLEAN|BUGS|STALE|CONTRADICTION] — summary
```

For files with bugs, add detail:
```
  BUG: line N — description
  STALE: line N — old value X should be Y
  CONTRADICTION: disagrees with module Z on concept C
```

## What S317 Audit Already Documented

All findings are in `docs/s317_full_audit.md`. This session EXTENDS that document with line-by-line findings for the remaining 97.8% of the codebase.

## Key References
- `docs/s317_baseline.md` — quantitative baselines
- `docs/s317_full_audit.md` — current audit findings (12 contradictions)
- `docs/superpowers/specs/2026-04-06-canonical-architecture-v9.md` — architecture spec
- `docs/parallel_build_inventory.md` — duplication clusters
- `lessons_learned.md` — L001-L016
