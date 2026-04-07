# S317 Engineering Baseline — 2026-04-07

Snapshot of system state at end of S317. All numbers measured, not estimated.
This is the BEFORE measurement. S318 and onwards measure against this.

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
