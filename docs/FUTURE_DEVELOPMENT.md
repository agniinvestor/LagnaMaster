# Future Development Inventory

**Created:** S316 (2026-04-05)
**Purpose:** Everything planned but not yet shipped, organized by priority tier.

---

## Phase E — Test Diversification

| # | Item | Scope | Dependency |
|---|------|-------|------------|
| E1 | `tools/select_360.py` — deterministic selection of 360 charts (30 per lagna) from ADB pool | Tool | 81 ADB charts already computed; pool expansion needed (only 180/5243 have valid birth_data) |
| E2 | `tests/fixtures/verified_360.json` — golden set with PyJHora cross-validation | Fixture | E1 |
| E3 | `tests/test_diverse_rule_firing.py` — 360 integration tests through full pipeline | Tests | E2 |
| E4 | "Golden 50" fast CI subset (4-5 charts per lagna) | Tests | E2 |
| E5 | Pool expansion — import more ADB charts with birth_data, re-run pipeline | Data | External data source |

**Spec:** `docs/superpowers/specs/2026-04-02-test-diversification-design.md`
**Plan:** `docs/superpowers/plans/2026-04-02-test-diversification.md`
**Risk:** India 1947 covers 44% of tests. Module could break for 11 lagnas and pass.

---

## Phase F — Quality Gate Enforcement

| # | Item | Scope | Dependency |
|---|------|-------|------------|
| F1 | 14-question encoding checklist in `V2ChapterBuilder._validate_add()` | Builder | None |
| F2 | Decision gate rationale field for deviations | Schema | F1 |
| F3 | Verse audit per-verse gap enumeration (Ch.12-23) | Tool | Scorecard 95% threshold (shipped S316) |
| F4 | Ch.31 retroactive maker-checker review | Process | External GPT review |

**Spec:** `docs/superpowers/specs/2026-04-02-encoding-quality-gates-design.md`

---

## Phase G — Legacy Migration Audit

| # | Item | Scope | Dependency |
|---|------|-------|------------|
| G1 | Run `tools/migration_audit.py` on all 15 V1/V2 chapters | Audit | Tool exists |
| G2 | Annotate all PARTIAL matches with reasons | Manual | G1 |
| G3 | Resolve all GAP_CRITICAL findings (encode or justify) | Encoding | G1 |
| G4 | Update migration_registry.py: all 15 chapters → VERIFIED | Registry | G2 + G3 |
| G5 | Activate gated V1 exclusion in combined_corpus.py | Schema | G4 (all chapters verified) |

**Spec:** `docs/superpowers/specs/2026-04-04-legacy-migration-audit-design.md`
**Impact:** 553 V1 legacy rules excluded once verified, reducing corpus noise.

---

## Phase H — Remaining Features

| # | Item | Scope | Impact |
|---|------|-------|--------|
| H1 | `planet_in_house_from_aspects` — aspect mode for planet_in_house_from | Primitive | Low — occupancy mode works |
| H2 | `derived_house_sign` — check what sign falls at derived position | Primitive | 2 Ch.30 rules |
| H3 | `condition_modifier_fix.py` — auto-fix high-confidence condition/modifier misclassifications | Tool | Quality |
| H4 | Dasha engine extensions: Ashtottari, Yogini, Kalachakra | Engine | Phase 5 (S361+) |
| H5 | Dasha/transit activation logic (hook exists, logic deferred) | Engine | Phase 5 (S611+) |

---

## Encoding Chapters — Now Unblocked

All primitives shipped in S316. These chapters are ready for encoding sessions:

| Block | Chapters | Rules (est.) | Primitive Used |
|-------|----------|-------------|----------------|
| C | Ch.32-33 (Karakas) | ~100 | `dynamic_karaka` |
| D | Ch.34-42 (Yogas, 9 chapters) | ~1,500 | `same_planet_constraint` (bind) |
| E | LP (Laghu Parashari) | ~306 | `functional_benefic` |

**After BPHS:** Brihat Jataka, Phaladeepika, Saravali, Jaimini, Hora Ratnam, Prasna Marga, Tajika Neelakanthi, Mansagari, Jataka Tattva, Stri Jataka, Muhurtha Chintamani (~18,000+ rules across 300+ chapters)

---

## Open Bugs

| Bug | Severity | Status | Fix |
|-----|----------|--------|-----|
| C-18: Edge cases not cross-validated | HIGH | Blocked on Phase 2 data | Extend diff_engine |
| PG-1: PostgreSQL tests skipped | HIGH | Open since S189 | Spin up Postgres, set PG_DSN |

---

## Guardrails (Product Layer — Not Engine)

8 CRITICAL + 6 HIGH guardrails documented in `docs/GUARDRAILS.md`. All are product-layer requirements (UI language, health content policy, DPDP/GDPR compliance, signal isolation, validation protocols). Not applicable until product phase (S791+).

---

## Roadmap Phases

| Phase | Sessions | Status |
|-------|----------|--------|
| Phase 0: Infrastructure | S191-S215 | Complete |
| Phase 1A: Classical corpus (V1) | S216-S262 | Complete (2,634 rules) |
| Phase 1B: Structured corpus (V2) | S263-S410 | In progress (600 V2 rules shipped) |
| Phase 2: Engine rebuild | S411-S470 | Not started |
| Phase 3: Feedback + Privacy | S471-S530 | Not started |
| Phase 4: Personality Protocol | S531-S610 | Not started |
| Phase 5: Temporal Model | S611-S700 | Not started |
| Phase 6: ML Pipeline | S701-S790 | Not started |
| Phase 7: Product + Revenue | S791-S840 | Not started |
| Phase 8-10: Research | S841-S1050+ | Not started |
