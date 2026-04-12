# Tools Index — LagnaMaster

Read this at session start. Do NOT rebuild any tool that already exists here.

## Session Start

| Tool | Purpose |
|------|---------|
| `start_session.py` | Generate self-contained session packet with signatures and git commands |
| `install_hooks.py` | Install git hooks (pre-push + commit-msg) — run once after clone |

## Encoding Workflow

| Tool | Purpose |
|------|---------|
| `verse_audit.py` | Verse-by-verse granularity audit comparing encoded vs source claims |
| `v2_scorecard.py` | Exhaustive V2 encoding quality scorecard for any rule set |
| `validate_rules.py` | Pre-commit rule validator for V2 schema compliance |
| `tag_bb_chains.py` | Auto-tag derived_house_chains on V2 rules deterministically |
| `classify_prediction_types.py` | Assign prediction_type to rules missing it |

## Audit & Quality

| Tool | Purpose |
|------|---------|
| `condition_modifier_audit.py` | Audit V2 rules for condition/modifier misclassification |
| `migration_audit.py` | Audit legacy V1 rules against V2 structured rules for mapping |
| `corpus_audit.py` | Full corpus health check across all encoded files |
| `rework_detector.py` | Pre-commit rework and lesson detection for session protocol |
| `rework_counter.py` | Scan git history for rework indicators and iteration patterns |
| `rule_grader.py` | Corpus maturity scorecard across 25K rules (L0-L5 model) |

## Cross-Validation & Scoring

| Tool | Purpose |
|------|---------|
| `diff_engine.py` | Full cross-validation pipeline: LagnaMaster vs PyJHora field-by-field |
| `diff_engine_core.py` | Core diff engine with normalization and classification |
| `diff_report.py` | Aggregate reporting and health dashboard metrics across validations |
| `ob3_calibrate.py` | Empirical scoring calibration using 5,063 ADB charts |
| `normalize_outputs.py` | Normalization layer for cross-engine comparison before diffing |
| `classification.py` | Reclassify cross-engine disagreements into systematic or random |
| `vedastro_cross_validate.py` | Cross-validate LagnaMaster positions against VedAstro REST API |

## Data Import

| Tool | Purpose |
|------|---------|
| `adb_scraper.py` | Fetch verified birth data from Astro-Databank for fixtures |
| `adb_xml_importer.py` | Parse official ADB XML export and convert to LagnaMaster JSON |
| `adb_playwright_scraper.js` | JavaScript scraper for Astro-Databank (Playwright-based) |
| `scrape_200_aa.py` | Fetch and compute 200 Rodden AA charts from Astro-Databank |
| `select_360.py` | Deterministic selection of diverse charts from PyJHora pool |
| `compute_pyjhora_all.py` | Compute all ADB stubs with PyJHora for unbiased lagna distribution |
| `download_classical_texts.py` | Download classical Jyotish texts from archive.org |

## Migration (one-time use)

| Tool | Purpose |
|------|---------|
| `backfill_phase1b.py` | One-time Phase 1B compliance backfill for missing fields |
| `backfill_tz_offset.py` | Backfill timezone offset for ADB stubs using lat/lon |
| `migrate_domains.py` | Normalize domains from 15 to 8 primary domains |
| `migrate_modifier_conditions.py` | Migrate modifier condition strings to structured dicts |
| `migrate_modifiers.py` | Classify and migrate modifiers to new 5-effect schema |

## CI / Hooks

| Tool | Purpose |
|------|---------|
| `pre_push_hook.sh` | Unified quality gate: pytest + ruff + docs currency check |
| `validate_commits.py` | Pre-commit hook validating commit message format |
| `ci_watch.py` | Watch GitHub Actions CI and print failures locally |
| `setup_ci_guard.py` | Install pre-push hook and CI watch tool |

## Archive

`tools/archive/` contains 140+ deprecated scripts from prior sessions. Do not use directly — they are historical artifacts.

---

**Decision tree: "Which tool do I use?"**

- Starting a session? → `start_session.py`
- Encoding a chapter? → `verse_audit.py` (Gate 1) → encode → `v2_scorecard.py` (Gate 4) → `validate_rules.py` (pre-commit)
- Auditing the corpus? → `corpus_audit.py` (broad) or `condition_modifier_audit.py` (specific)
- Cross-validating positions? → `diff_engine.py` (vs PyJHora) or `vedastro_cross_validate.py` (vs VedAstro)
- Checking for rework? → `rework_detector.py` (pre-commit) or `rework_counter.py` (history scan)
- Importing chart data? → `adb_scraper.py` or `adb_xml_importer.py`
