# S317 Full System Audit — 2026-04-07

**Scope:** Every directory, every module category, every document. Quantitative + content-verified where indicated.

## Summary of Critical Findings

### 🔴 ACTIVE BUGS (producing wrong results now)
1. **shadbala_patches.py had 4 wrong friendship values** — FIXED in this audit session
2. **11 modules have static malefic sets** that don't use chart-aware `is_natural_malefic()` — waning Moon and Mercury conjunction NOT considered in argala, arudha_perception, extended_yogas, functional_roles, longevity, multi_axis_scoring, multi_lagna, narayana_argala, yogas_extended, diagnostic_scorer, feature_decomp
3. **scoring_patches.py has stale ASPECT_STRENGTH** (0.75 fixed values) — not using BPHS speculum
4. **Only 23/7,412 rules (0.3%) marked "implemented"** — scoring engine can only evaluate 23 rules

### 🟠 HIGH RISK (will cause issues under stress)
5. **multi_axis_scoring.py: 13 importers, 1 test file** — core scoring engine nearly untested
6. **functional_roles.py: 7 importers, 1 test** — functional classification widely used, barely tested
7. **diagnostic_scorer.py: 351 lines, 0 tests** — completely untested
8. **36/125 calculation modules have ZERO source citations** — including house_lord.py (38 importers), vimshottari_dasa.py (25 importers)
9. **74/143 corpus files lack verse_ref** — 52% of corpus lacks verse traceability
10. **111/125 modules untouched by S317** — 89% of calculation code not verified against text

### 🟡 STRUCTURAL DEBT
11. **11 hardcoded _NAT_MALEFIC sets** across separate files — should import from one source
12. **5 inline sign lord tables** — should import from one source
13. **8 avastha modules** — 3 confirmed unwired, rest untested for consistency
14. **4 friendship table copies** — dignity.py, panchadha_maitri.py, friendship.py, sayanadi_full.py (all now correct post-S317, but 4 copies = 4× future drift risk)
15. **0% concordance computed** across 7,412 rules — multi-text value proposition not operational
16. **Only 22/143 corpus files (15%) use V2 builder** — 85% old format
17. **13 rules still entity_target="general"** — L004 violation

## Duplication Index (measured)

| What | Copies | Authoritative Source | Consumers of Copies |
|------|--------|---------------------|-------------------|
| Sign lord table | 5 inline + 7 via import | dignity.py, rule_firing.py | diagnostic_scorer, feature_decomp, avasthas(2), rule_firing |
| Malefic/benefic set | 11 static + 2 chart-aware | rule_firing.py:is_natural_malefic | argala, arudha_perception, diagnostic_scorer, extended_yogas, feature_decomp, functional_roles, longevity, multi_axis_scoring, multi_lagna, narayana_argala, yogas_extended |
| Friendship table | 4 full copies | dignity.py:_NAISARGIKA | panchadha_maitri.py, friendship.py, sayanadi_full.py |
| Exalt/debil tables | 26 files reference | dignity.py | Too many to list — every scoring/yoga module |
| Avastha modules | 8 files | avasthas.py (S317, BPHS) | avastha.py, avastha_v2.py, planet_avasthas.py, sayanadi_full.py + consumers |
| Scoring modules | 12 files | multi_axis_scoring.py | scoring.py, scoring_v2.py, scoring_v3.py, scoring_patches.py, etc. |
| ASPECT_STRENGTH | 2 copies | sputa_drishti.py (BPHS speculum) | scoring_patches.py (stale 0.75 values) |

## Source Coverage

| Category | With Citations | Without | Citation Rate |
|----------|---------------|---------|---------------|
| Calculation modules | 89/125 | 36/125 | 71% |
| Corpus files (verse_ref) | 69/143 | 74/143 | 48% |
| Corpus files (V2 builder) | 22/143 | 121/143 | 15% |

## Test Coverage

| Module | Lines | Importers | Test Files | Risk |
|--------|-------|-----------|-----------|------|
| multi_axis_scoring.py | 588 | 13 | 1 | 🔴 CRITICAL |
| functional_roles.py | 206 | 7 | 1 | 🔴 HIGH |
| diagnostic_scorer.py | 351 | 1 | 0 | 🟠 UNTESTED |
| feature_expansion.py | 171 | 0 | 0 | 🟡 ORPHAN + UNTESTED |
| rule_firing.py | 1,442 | 13 | 9 | 🟡 Large, moderate coverage |

## Documentation Staleness (content-verified)

| Doc | Status | Key Issues |
|-----|--------|-----------|
| ARCHITECTURE.md | 🔴 STALE | Conflicts with graph spec. Wrong file paths. "12 modules" → 125. "22 rules" → 23. Missing PlanetPosition.latitude. Layer III references unreached sessions. |
| KPIS.md | 🟠 STALE NUMBERS, GOOD FRAMEWORK | Tests: 1338→14740. Rules: 23→7412. Framework is comprehensive and should be primary tracking instrument. |
| shadbala_audit_gaps.md | 🔴 FULLY STALE | Says 9 gaps open — all resolved in S317. |
| ROADMAP.md | 🟡 STRATEGIC CONTEXT | 1000-session plan. Graph architecture = Phase 2 (S411-S470). Must align. |
| GUARDRAILS.md | 🟠 ALL RED/ORANGE | 20 guardrails defined. Most not implemented. G02 (health/death) critical. |
| Makefile | 🔴 STALE | Says "76 tests" — actual 14,740. |
| BPHS_ENCODING_ROADMAP.md | 🟠 STALE | 6 chapter statuses not updated for S317. |

## API Layer

| Finding | Details |
|---------|---------|
| Two API versions | main.py (11 endpoints) + main_v2.py (5 endpoints). Both import from ephemeris + scoring. |
| Shared logic | Both call compute_chart → score_chart. main_v2.py is simpler subset. |
| DB routing | main.py uses db_pg (PostgreSQL). UI uses db (SQLite). Two DB paths. |

## Security

| Finding | Severity |
|---------|----------|
| JWT secret hardcoded fallback | 🔴 HIGH — "dev-secret-change-in-production" in auth.py:25 |
| Auth uses SQLite directly | 🟠 MEDIUM — Not using the db_pg routing layer |
| 0/21 dependencies pinned | 🟠 MEDIUM — All >= not == |
| No .env template | 🟡 LOW — Environment variables undocumented |

## Privacy & Guardrails

| Component | Status |
|-----------|--------|
| consent_engine.py | Exists (GDPR Art 7 + DPDP). Not audited for correctness. |
| data_minimisation.py | Exists (GDPR Art 5). Not audited. |
| family_consent.py | Exists. Not audited. |
| 20 G-series guardrails | Defined in GUARDRAILS.md. Most NOT implemented (🔴). |
| Health-sensitive handling | 772 references across codebase. Coverage unknown. |

## Infrastructure

| Component | Status |
|-----------|--------|
| Docker | Dockerfile + docker-compose.yml. api + ui services. |
| Makefile | 15 targets. Test count stale (76 vs 14740). |
| Pre-push hook | 7 checks (pytest, ruff, docs, scorecard, rework, maturity, completeness). |
| Pre-commit hook | Deferral language detection + scorecard on staged corpus. |
| Redis | Referenced in ARCHITECTURE.md as planned. Not implemented. |
| Celery | In requirements.txt. Worker exists (src/worker.py). |

## Unwired Infrastructure (ready to use, not connected)

| Module | Lines | What It Does | Should Connect To |
|--------|-------|-------------|-------------------|
| config_additions.py | 141 | 36 ayanamshas, AstronomicalConfig | ephemeris.py (replaces 3-ayanamsha hardcoded map) |
| yogas_additions.py | 307 | PM Yoga, Lunar/Solar yogas | Yoga detection pipeline |
| feature_expansion.py | 171 | V2 corpus → continuous features | Phase 2 scoring (premature) |

## What This Audit Did NOT Cover

- Line-by-line code correctness of 111 untouched modules
- API endpoint behavior testing
- UI functionality verification
- Privacy module correctness verification
- DB schema validation
- Docker build verification
- Celery worker functionality
- All 197 test files for test quality (testing the right things?)
- All 171 tools for correctness
- Performance profiling
- Security penetration testing
