# S317 Engineering Baseline — 2026-04-07

**QUANTITATIVE ONLY.** File counts, line counts, function counts, import counts are measured and accurate. CONTENT QUALITY (is the code correct? are docs accurate? do tests test the right things?) is NOT verified. This is a surface scan, not a content audit. S318 must read and verify the highest-risk files — the numbers here tell you WHERE to look, not WHAT you'll find.

## Corpus Quality

| Metric | Value | Target | Notes |
|--------|-------|--------|-------|
| Total rules | 7,412 | 10,000+ (Tier 2 encoding) | Across 14 source texts |
| V2 structured rules | 600 (8.1%) | 100% | Only V2 rules have predictions, entity_target, signal_group |
| With verse citation | 4,778 (64.5%) | 100% | 35.5% have chapter but no verse |
| With concordance | 0 (0.0%) | >30% | NO cross-text concordance computed |
| Entity target = "native" | 7,288 (98.3%) | <80% | Most rules default to native — L004 problem |
| Entity target = "general" | 13 (0.2%) | 0% | "General" is a cop-out per L004 |
| High confidence (≥0.8) | 2,597 (35.0%) | >50% | |
| Practitioner-validated | 0 | >0 | Zero external validation |

### Source Distribution
| Text | Rules | % | School |
|------|-------|---|--------|
| Saravali | 2,898 | 39.1% | parashari |
| BPHS | 2,061 | 27.8% | parashari |
| Bhavartha Ratnakara | 780 | 10.5% | kalidasa |
| Laghu Parashari | 277 | 3.7% | parashari |
| Uttara Kalamrita | 201 | 2.7% | parashari |
| Jataka Parijata | 197 | 2.7% | vaidyanatha |
| Brihat Jataka | 190 | 2.6% | varahamihira |
| Phaladeepika | 189 | 2.5% | mantreswara |
| Jaimini Sutras | 178 | 2.4% | jaimini |
| Sarvartha Chintamani | 170 | 2.3% | sarvartha |
| Lal Kitab | 120 | 1.6% | lal_kitab |
| Chandra Kala Nadi | 120 | 1.6% | nadi |
| KP | 30 | 0.4% | kp |
| General Jyotish | 1 | 0.0% | all |

## Codebase Health

| Metric | Value | Target (post-Phase 1) |
|--------|-------|-----------------------|
| Files in src/calculations/ | 125 | <80 (consolidation) |
| Lines in src/calculations/ | 30,880 | <25,000 |
| Files in src/corpus/ | 144 | stable (grows with encoding) |
| Lines in src/corpus/ | 86,151 | grows with encoding |
| Total src/ files | 335 | <280 |
| Total src/ lines | 127,511 | <110,000 |
| Test files | 197 | grows |
| Functions in src/calculations/ | 707 | <500 |

### Largest Modules (technical debt indicators)
| Module | Lines | Notes |
|--------|-------|-------|
| rule_firing.py | 1,442 | Needs graph migration (Phase 1 target) |
| shadbala.py | 874 | S317 major corrections applied |
| dignity.py | 837 | S317 audit, needs Layer 2/3/4 split |
| multi_axis_scoring.py | 588 | R01-R23 scoring engine |
| feature_decomp.py | 587 | Feature extraction |

### Duplication Index
| Cluster | Count | Target |
|---------|-------|--------|
| Sign lord inline tables | 4 | 1 |
| Exalt/debil references | 26 | 1 canonical + importers |
| Hardcoded malefic sets | 27 | 0 (use is_natural_malefic) |
| Avastha modules | 8 | 1-2 (BPHS + alternative school) |
| Scoring modules | 12 | 3 (graph evaluator + adapters) |

## Architecture Compliance

| Metric | Value | Target |
|--------|-------|--------|
| Direct chart.planets in scoring/rules | 10 | 0 (Phase 1 exit) |
| Graph-based rule evaluation | 0% | 100% (Phase 1 exit) |
| Tier 4 lazy evaluation | Not implemented | Full (Phase 1) |
| School-filtered edge queries | Not implemented | Full (Phase 1) |

## Lesson Enforcement

| Metric | Value |
|--------|-------|
| Total lessons (L001-L016) | 16 |
| With code controls (hooks, tests, builder gates) | 5 (31%) |
| Behavioral-only (no enforcement) | 5 (31%) |
| Behavioral lessons violated in same session written | 3 (L012, L016, plus L008 from S316) |

## Encoding Roadmap

| Category | Chapters | Status |
|----------|----------|--------|
| Encoded (V2 rules) | Ch.12-24 | 13/97 (13.4%) |
| Audited against text (S317) | Ch.3, 11, 26, 27, 34, 45 | 6/97 (6.2%) |
| Partially implemented | Ch.5-8, 25-31, 46, 49-50, 64 | ~15/97 |
| Not touched | Ch.1-2, 9-10, 32-33, 35-44, 47-48, 51-63, 65-97 | ~63/97 (64.9%) |

## Prediction Quality

| Metric | Value | Notes |
|--------|-------|-------|
| Practitioner validation | NONE | Zero charts reviewed by human astrologer |
| Gold standard chart set | NONE | No charts with expected practitioner results |
| Accuracy baseline (ρ) | 0.31 (23-rule engine, OB-3) | From S316, unvalidated comparison |
| Cross-text concordance | NOT IMPLEMENTED | Architecture spec defines it, code doesn't |

## Session Metrics (S317)

| Metric | Value |
|--------|-------|
| Commits | 41 |
| BPHS chapters audited | 6 |
| Bugs found and fixed | 14+ |
| Deferred items resolved | 23/23 |
| Architecture spec iterations | 9 |
| Lessons learned | 6 (L011-L016) |
| User pushbacks required | 8+ |
| Tests added | 102 BPHS-cited |
| Tests passing | 14,740 |

## Full System Inventory (beyond calculations + corpus)

| Layer | Files | Lines | Key Modules |
|-------|-------|-------|-------------|
| src/calculations/ | 125 | 30,880 | rule_firing (1,442), shadbala (874), dignity (837) |
| src/corpus/ | 144 | 86,151 | 7,412 rules across 14 texts |
| src/ root | 15 | 3,217 | ephemeris (270), scoring (619), worker (359), db (5 files, 666), auth (235), cache (208) |
| src/api/ | 8 | 1,443 | main.py (603), auth_router, mobile_router, empirica_router |
| src/ui/ | 5 | 2,233 | app.py (1,415), chart_visual, kundali_page |
| src/guidance/ | 9 | 995 | fatalism_filter, disclaimers, practitioner_handoff |
| src/privacy/ | 4 | 518 | Privacy/data protection |
| src/ci/ | 4 | 637 | health_check, protocol_compliance, phase0_checkpoint |
| src/interfaces/ | 5 | 322 | Adapter layer (scoring_engine, dasha_engine) |
| src/feedback/ | 4 | 332 | Feedback collection |
| src/ml/ | 2 | 89 | ML integration (minimal) |
| src/research/ | 4 | 298 | Research tooling |
| **tests/** | **197** | **—** | 14,740 passing |
| **tools/** | **171** | **9,055+** | ob3_calibrate, rule_grader, rework_counter, + archive |
| **docs/** | **58** | **—** | Specs, plans, roadmaps, memory |
| **.git/hooks/** | **2** | **—** | pre-push (quality gate), pre-commit (deferral check) |
| **Infrastructure** | **—** | **—** | Dockerfile, docker-compose.yml, Makefile, pytest.ini |

### Database Layer (not measured in original baseline)
5 database modules: db.py, db_pg.py, db_timescale.py, db_vector.py, db_family.py. PostgreSQL, TimescaleDB, vector store. Status unknown — may be partially implemented or stubs.

### API Layer
main.py (603 lines) — primary API. No main_v2.py found (may have been consolidated). Mobile router, empirica router, auth router present. API versioning status: unclear.

### Ethical Guardrails
9 guidance modules including fatalism_filter.py, disclaimer_engine.py, practitioner_handoff.py. These enforce G-series guardrails. Coverage and testing status: not measured.

### Privacy
4 modules, 518 lines. Scope: birth data handling. Compliance status: not audited.

## Dead Code & Orphans (CONTENT AUDITED)

| Module | Lines | Status | Audit Finding |
|--------|-------|--------|---------------|
| config_additions.py | 141 | UNWIRED, NOT dead | Contains 36 ayanamshas, node mode config, AstronomicalConfig dataclass. This is the Layer 2 conventions infrastructure the architecture spec needs. Should be wired into ephemeris.py (which hardcodes only 3 ayanamshas). |
| feature_expansion.py | 171 | UNWIRED, NOT dead | V2 corpus → continuous feature vectors. Phase 2 (S411-S425) work per its docstring. Premature — depends on full corpus. Uses old _EXALT/_DEBIL tables from diagnostic_scorer (may have stale values post-S317 fixes). |
| yogas_additions.py | 307 | UNWIRED, NOT dead | Pancha Mahapurusha, Sunapha/Anapha/Durudhura, Vesi/Vasi/Ubhayachari yoga definitions. Legitimate yoga detection code. Should be wired into yoga detection pipeline. |
| Circular imports | 0 | Clean | No circular import risk detected. |
| tools/archive/ | 140 files | Historical | Should not grow. |

## Security (CONTENT AUDITED)

| Finding | Severity | Details |
|---------|----------|---------|
| JWT secret | HIGH | auth.py:25 — `os.environ.get("JWT_SECRET", "dev-secret-change-in-production")`. Fallback is a static string. In production without JWT_SECRET env var, all JWTs use same secret. |
| .env file | MEDIUM | Does not exist. No template. Environment variables undocumented. |
| Dependencies | MEDIUM | 0/21 pinned. All `>=` not `==`. Supply chain risk — any dependency update could break build. |
| SQL injection | LOW | auth.py uses parameterized queries (?, ?). No raw string concatenation found. |
| CORS | INFO | Streamlit config has `enableCORS=false`. API CORS policy not audited. |

## Documentation Staleness (CONTENT AUDITED)

| Doc | Lines | Key Staleness Findings |
|-----|-------|----------------------|
| ARCHITECTURE.md | 565 | PlanetPosition missing `latitude` field. "12 Jyotish modules" → 125. "22 rules" → 23. Wrong file paths. 3-layer convergence model conflicts with graph architecture spec. Layer III references sessions 491-746 (not yet reached). |
| KPIS.md | 120 | Tests: "1338" → 14,740. Rules: "23 hard-coded" → 7,412. Texts: "2" → 14. FRAMEWORK is excellent — numbers need updating. This doc should be the primary tracking instrument, not my S317 baseline. |
| shadbala_audit_gaps.md | 159 | ALL 9 gaps say "open" but ALL were resolved in S317. Entire doc is stale. |
| ROADMAP.md | 288 | 1000-session plan through Phase 10 — this is the STRATEGIC context the graph architecture spec must align to. Graph spec = Phase 2 infrastructure (S411-S470), not standalone. |
| Makefile | — | Target `test` says "76 tests". Actual: 14,740. |
| BPHS_ENCODING_ROADMAP.md | 262 | Ch.3, 11, 26, 27, 34, 45 statuses not updated for S317 audit work. |

## API & Infrastructure

| Metric | Value |
|--------|-------|
| API endpoints | 29 (main: 11, auth: 5, main_v2: 5, empirica: 3, mobile: 2, school: 3) |
| API versions | 2 (main.py + main_v2.py) |
| UI streamlit refs | 343 (app.py: 273, kundali: 44, confidence: 26) |
| Docker services | api + ui (docker-compose.yml) |
| Makefile targets | 15 (up, down, test, etc.) |
| Makefile test count | Says "76 tests" — stale (actual: 14,740) |

## Documentation

| Doc | Lines | Last Modified | Stale? |
|-----|-------|---------------|--------|
| CHANGELOG.md | 1,600 | 7 days ago | Needs S317 entry |
| SESSION_LOG.md | 682 | 7 days ago | Needs S317 entry |
| ARCHITECTURE.md | 565 | 7 days ago | Pre-dates graph architecture spec |
| GUARDRAILS.md | 308 | 10 days ago | Not audited |
| ROADMAP.md | 288 | 7 days ago | Needs S317 status update |
| MEMORY.md (docs/) | 280 | 11 hours ago | Test count updated |
| BPHS_ENCODING_ROADMAP.md | 262 | 24 hours ago | Statuses stale for 6 audited chapters |
| shadbala_audit_gaps.md | 159 | 21 hours ago | ALL gaps resolved but doc says open |
| KPIS.md | 120 | 10 days ago | Not aligned with new baseline |
| **Total docs** | **58 files** | | Unknown how many are stale |

## Memory System

| Metric | Value |
|--------|-------|
| Memory files | 20 |
| MEMORY.md entries | 15 |
| Oldest memory | project_test_diversification (Apr 3) |
| Newest memory | feedback_s317_closure_fixture (Apr 6) |
| S316 memories | 8 (heaviest session in memory) |
| S317 memories | 2 |
| Verified as current | Unknown — no staleness check mechanism |

## Guardrails & Ethics

| Metric | Value |
|--------|-------|
| G-series references in code | 79 |
| Health-sensitive rule tracking | 3 modules (rule_record, v2_builder, rule_firing) |
| Guidance modules | 9 (fatalism filter, disclaimers, practitioner handoff, etc.) |
| Privacy modules | 4 (518 lines) |
| Guardrail test coverage | Not measured |

## Tools

| Category | Count | Lines |
|----------|-------|-------|
| Active tools | 31 | 9,055+ |
| Archived tools | 140 | Not measured |
| Largest tool | scrape_200_aa.py (1,042 lines) |
| v2_scorecard.py | 951 lines | Primary quality gate tool |
| Key tools | ob3_calibrate, rule_grader, rework_detector, verse_audit |

## What Doesn't Exist Yet

- Production monitoring/alerting
- Performance benchmarks in CI
- Line/branch coverage measurement
- Integration tests (full chart → score → output)
- Property-based tests (valid range checks for any chart)
- Adversarial tests (edge cases: 0° longitude, polar latitudes)
- Multi-school comparison tests
- Formal glossary (Sanskrit → English → code variable names)
- Stakeholder-readable progress reports
- Cost tracking (tokens per session, cost per rule)
- Encoding velocity trend (rules per session over time)
- Practitioner feedback loop
- API response time monitoring
- Deployment pipeline beyond git push
- Dependency pinning (0/21 dependencies pinned)
- Dead code removal process
- Documentation staleness checker
- Memory system verification
- Guardrail test coverage
- Security audit (JWT secret hardcoded)
