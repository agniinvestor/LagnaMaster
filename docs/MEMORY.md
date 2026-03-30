# MEMORY.md — LagnaMaster Session State
> **⚠️ MANDATORY: Update this file at the END of every session without fail.**
> Ground truth = git commits + update_docs_s*.py scripts, NOT the GitHub UI (known caching issue).

---

## ⚠️ Git Caching Warning

The GitHub web interface shows stale data (Sessions 1–10, 222 tests). This is a known caching issue.
**Always verify via `git log --oneline -5 && git status` — never trust the GitHub UI.**

The `update_docs_s188.py` in the repo root is the canonical documentation-sync artifact.
When in doubt, read that file to reconstruct state.

---

## Actual Current State (Sessions 1–262 complete — March 2026)

### Repository
- **Repo:** `github.com/agniinvestor/LagnaMaster`
- **Engine version:** `v3.0.0`
- **Python:** `3.14`
- **Ephemeris:** pyswisseph **JPL DE431** real files (`sepl_18.se1` + `semo_18.se1`) — Moshier fallback **retired**
- **Historical charts (pre-1800):** use `seplm_18.se1` + `semom_18.se1`

### Test Status
- **2413 passing, 3 skipped, 0 lint errors, CI green**
- The 3 skipped tests require a live `PG_DSN` (PostgreSQL). They pass when a Postgres instance is wired.
- 200+ ADB fixture charts covering all 12 Lagnas

### Session Progress
- **Sessions 1–10:** Pilot build — 12 calculation modules, 222 tests, Docker, Streamlit UI
- **Sessions 11–160:** Classical depth — all major calculation modules, 1000+ tests
- **Sessions 161–162:** Wiring fixes — Topocentric Moon, functional dignity in R02/R09
- **Sessions 163–186:** Scoring depth, school-mixing fix, regression snapshot
- **Sessions 187–188:** Final wiring gaps + XIX output API + Postgres routing + Swiss Ephemeris upgrade
- **Sessions 189–191:** Phase 0 bootstrap — Kala Bala verification, C-18 stress fixtures, VedAstro install, Protocol stubs, ruff G17 rule
- **Session 192:** Protocol adapters — ScoringEngineAdapter, VimshottariDasaAdapter, NullFeedbackService, NullMLService
- **Session 193:** HouseScore distribution dataclass — `house_score.py`, `compute_house_scores()`, `ChartScoresV3.house_distributions`; 1490 tests
- **Session 194:** Conditional weight functions W(planet, house, lagna, functional_role) — `conditional_weights.py`, G06 g06_compliant flag; 1503 tests
- **Session 195:** Feature decomp infrastructure — `feature_decomp.py`, 4 extractors, 48 features; 1517 tests
- **Session 196:** +4 feature extractors (kartari, combust, retrograde, bhavesh_house_type); 1525 tests
- **Session 197:** +3 feature extractors (benefic_net_score, malefic_net_score, karak_score); 1530 tests
- **Session 198:** +2 extractors (pushkara_nav, war_loser); 156 features (≥150 ✅); 1535 tests
- **Session 199:** feature contract tests (10 tests, G22 gate); 1545 tests
- **Session 200:** ChartScoresV3 feature_vector field; ROADMAP S195–S200 ✅; 1550 tests
- **Session 201:** OSF schema (HypothesisSpec, CVStrategy, OSFRegistration) + OB-3 draft; 1558 tests
- **Session 202:** RuleRecord + CorpusRegistry corpus infrastructure; 1570 tests
- **Session 203:** ADB license + R01-R23 corpus encoding (EXISTING_RULES_REGISTRY); 1582 tests
- **Session 204:** TextExtractor Protocol + TimeBasedSplit CV splitter; 1592 tests
- **Session 205:** CorpusAudit + 31 BPHS extended rules (B001-B031); 1602 tests
- **Session 206:** Phaladeepika (21) + Brihat Jataka (26) rules; 101 total corpus rules; 1610 tests
- **Session 207:** Uttara Kalamrita (17) + Jataka Parijata (17); 135 total corpus rules; 1618 tests
- **Session 208:** BirthRecord + COMBINED_CORPUS (135+ rules, 6 texts); 1629 tests
- **Session 209:** Corpus pipeline integration tests (9 tests); 1638 tests
- **Session 210:** Corpus checkpoint; ROADMAP S201-S210 ✅; 135 rules across 6 texts
- **Session 211:** pgvector + TimescaleDB + MLflow + family schema; 1651 tests
- **Session 212:** KP ayanamsha enforcement (G06 🟡); compute_kp_chart(); 1660 tests
- **Sessions 213–215:** Protocol verification + CI observability + Phase 0 checkpoint; src/ci/ package; 1722 tests
- **Sessions 216–228:** Phase 1 Batch 1 — 299 new BPHS rules encoded (lords-in-houses 144, yogas 75, dignities/aspects/dasha/special-lagnas 80); corpus 135→434 rules; 1777 tests
- **Session 229:** Graha in rashis p1 — Sun+Moon in 12 rashis; 24 rules; corpus 458; 1788 tests
- **Session 230:** Graha in rashis p2 — Mars+Mercury in 12 rashis; 24 rules; corpus 482; 1799 tests
- **Session 231:** Graha in rashis p3 — Jupiter+Venus in 12 rashis; 24 rules; corpus 506; 1811 tests
- **Session 232:** Graha in rashis p4 — Saturn+Rahu+Ketu in 12 rashis; 36 rules; corpus 542; 1823 tests
- **Session 233:** KP Sublord system — 30 rules (KPS001-030); corpus 572; 1833 tests
- **Session 234:** Nakshatra rules p1 — nakshatras 1-14 + Moon; 28 rules; corpus 600; 1843 tests
- **Session 235:** Nakshatra rules p2 — nakshatras 15-27 + Moon; 26 rules; corpus 626; 1851 tests
- **Session 236:** Bhava karakas — naisargika+Jaimini chara+special; 30 rules; corpus 656; 1860 tests
- **Session 237:** Varga rules — D9/D10/D4/D7/D12+others; 30 rules; corpus 686; 1869 tests
- **Session 238:** Brihat Jataka extended — planetary natures+aspects+yogas+timing; 30 rules; corpus 716; 1877 tests
- **Session 239:** Phala Deepika extended — planets in houses+yogas+health; 30 rules; corpus 746; 1886 tests
- **Session 240:** Uttara Kalamrita extended — house+planet significations+principles; 30 rules; corpus 776; 1895 tests
- **Session 241:** Jataka Parijata extended — lagnas+yogas+all 9 Maha Dasha results; 30 rules; corpus 806; 1904 tests ✅ 800+ MILESTONE
- **Session 242:** Classical transit rules — Gochara/Vedha/Ashtakavarga/Sade Sati/double transit; 30 rules; corpus 836; 1914 tests
- **Session 243:** Ashtakavarga rules — BAV structure/Shodhana/Kakshya/planet BAVs/transit assessment; 30 rules; corpus 866; 1925 tests
- **Session 244:** Jaimini Sutras + Upagrahas — Chara Karakas/Rashi Drishti/Arudha/Chara Dasha/Gulika; 30 rules; corpus 896; 1936 tests
- **Session 245:** Shadbala rules — 6-fold strength/Sthana/Dig/Kala/Chesta/Naisargika/Drik; 30 rules; corpus 926; 1947 tests
- **Session 246:** Dasha systems — Vimshottari/Ashtottari/Yogini/Kalachakra/Maraka/planet results; 30 rules; corpus 956; 1958 tests
- **Session 247:** Extended yoga rules — Pancha Mahapurusha/Nabhasa/Viparita/Moon yogas/Kartari; 30 rules; corpus 986; 1969 tests
- **Session 248:** Lagna extended — all 12 lagna profiles/Yogakaraka/Kendra Adhipati/Vargottama; 30 rules; corpus 1016; 1979 tests ✅ 1000+ MILESTONE
- **Session 249:** Bhava Phala extended — all 12 house significations/Upachaya/Dusthana/Maraka; 30 rules; corpus 1046; 1990 tests
- **Session 250:** Graha Phala — planets in houses (all 7 planets + Rahu/Ketu, Mangal Dosha, combust); 30 rules; corpus 1076; 2001 tests
- **Session 251:** BPHS Graha-Bhava Complete — exhaustive 9×12 planet-house matrix (GBC001-108); 108 rules; corpus 1184; 2012 tests
- **Session 252:** BPHS Yoga Exhaustive — Ch.35-56, all yoga classes (YEX001-150); 150 rules; corpus 1334; 2028 tests
- **Session 253:** BPHS Bhava Exhaustive — Ch.11-22, all 12 houses deep (BVX001-120); 120 rules; corpus 1454; 2042 tests
- **Session 254:** BPHS Graha Characteristics — Ch.3-10, all 9 planets complete (GCH001-100); 100 rules; corpus 1554; 2057 tests
- **Session 255:** Brihat Jataka Exhaustive — all 25 chapters (BJX001-120); 120 rules; corpus 1674; 2075 tests
- **Session 256:** Uttara Kalamrita Exhaustive — all doctrines (UKX001-150); 150 rules; corpus 1824; 2098 tests
- **Session 257:** Jataka Parijata Exhaustive — all 18 chapters (JPX001-150); 150 rules; corpus 1974; 2121 tests
- **Session 258:** Sarvartha Chintamani Exhaustive — all chapters (SCX001-150); 150 rules; corpus 2124; 2141 tests
- **Session 259:** Jaimini Sutras Exhaustive — 4 Adhyayas (JMX001-150); 150 rules; corpus 2274; 2166 tests
- **Session 260:** Lal Kitab Exhaustive — 1939-1952 editions (LKX001-120); 120 rules; corpus 2394; 2185 tests
- **Session 261:** Chandra Kala Nadi Exhaustive — Deva Keralam (CKN001-120); 120 rules; corpus 2514; 2206 tests
- **Session 262:** Phaladeepika Exhaustive — Mantreswara 14th century (PHX001-120); 120 rules; corpus 2634; 2227 tests
- **Session 263:** Phase 1B Schema Definition — Rule Contract + Outcome Taxonomy + Coverage Map + Concordance Workflow; RuleRecord +14 fields; corpus unchanged; 2227 tests
- **Session 264:** Laghu Parashari Functional Nature Table — LPF001-108 (9×12); Phase 1B conditional; 6 yogakarakas; corpus 2742; 2250 tests
- **Session 265:** Laghu Parashari Sections B, C, D — LPY001-012 + LPK001-024 + LPD001-045; corpus 2823; 2270 tests
- **Session 266:** Laghu Parashari Sections E, F (complete) — LPA001-060 + LPM001-024; LP coverage map done; corpus 2907; 2295 tests
- **Session 267:** Bhavartha Ratnakara Aries + Taurus — BVR001-130; corpus 3037; 2309 tests
- **Session 268:** Bhavartha Ratnakara Gemini + Cancer — BVR131-260; corpus 3167; 2323 tests
- **Session 269:** Bhavartha Ratnakara Leo + Virgo — BVR261-390; corpus 3297; 2337 tests
- **Session 270:** Bhavartha Ratnakara Libra + Scorpio — BVR391-520; corpus 3427; 2351 tests
- **Session 271:** Bhavartha Ratnakara Sagittarius + Capricorn — BVR521-650; corpus 3557; 2365 tests
- **Session 272:** Bhavartha Ratnakara Aquarius + Pisces — BVR651-780; corpus 3687; 2379 tests — **BVR COMPLETE (780/780)**
- **Session 273:** Saravali Conjunctions 1 (Sun-Moon/Mars/Mercury) — SAV001-130; corpus 3817; 2393 tests
- **Session 274:** Saravali Conjunctions 2 (Sun-Jupiter/Venus/Saturn) — SAV131-260; corpus 3947; 2403 tests
- **Session 275:** Saravali Conjunctions 3 (Moon-Mars/Mercury/Jupiter) — SAV261-390; corpus 4077; 2413 tests
- **Next session:** S276

---

## Session Startup Checklist (Run BEFORE Every Session)

```bash
# Step 1: Verify actual state — ignore GitHub UI
cd ~/LagnaMaster && git log --oneline -5 && git status

# Step 2: Lint check (must be 0)
.venv/bin/ruff check src/ tests/ tools/ 2>&1 | grep -c 'error'

# Step 3: Test count (must match or exceed 1338)
PYTHONPATH=. .venv/bin/pytest tests/ -q --tb=no 2>&1 | tail -3

# Step 4: Read docs/MEMORY.md — check "Next Session"
# Step 5: Read docs/CHANGELOG.md — last 30 lines
# Step 6: Read session entry in docs/ROADMAP.md
# Step 7: Check docs/GUARDRAILS.md for applicable guardrails
# Step 8: If running empirical analysis → verify OSF timestamp first (G22)
```

---

## Next Session: S263 — Phase 1B Schema Definition (non-coding)

S263 is a planning and schema session. No rules are encoded. It produces four
foundational documents that gate all Phase 1B encoding — no Phase 1B session begins
without all four committed:

| Deliverable | File | Purpose |
|-------------|------|---------|
| Rule Contract | `docs/PHASE1B_RULE_CONTRACT.md` | 12 mandatory fields + rejection criteria |
| Outcome Taxonomy | `docs/PHASE1B_OUTCOME_TAXONOMY.md` | 15 domains, fixed vocabulary |
| Coverage Map (Laghu Parashari) | `docs/coverage_maps/laghu_parashari.md` | First text, highest priority |
| Concordance Workflow | `docs/PHASE1B_CONCORDANCE_WORKFLOW.md` | Step-by-step real-time protocol |

**Why S263 exists:** Phase 1A (S216–S262, 2,634 rules) produced representative samplings
labeled "exhaustive." The failure mode: definition-of-done was a rule count, not a coverage
specification. Encoding produced prose descriptions, not structured predictions. S263
installs the gates that prevent this from recurring.

**Phase 1B overview:**
- Target: ~9,200 structured predictions total (2,634 Phase 1A + ~6,600 Phase 1B)
- Encoding sessions: S264–S309 (~46 encoding sessions)
- Verification sessions: S310–S316 (one per text after completion)
- First text: Laghu Parashari (S264–S266) — functional nature table 9×12 is foundational
- Full plan: `docs/CLASSICAL_CORPUS.md` → Phase 1B Session Plan section

---

## All Wiring Gaps — Status (as of S188)

All critical wiring gaps are **CLOSED**. No outstanding gaps.

| Gap | Closed In | How Fixed |
|-----|-----------|-----------|
| Topocentric Moon (`FLG_TOPOCTR`) | S161 | `swe.set_topo()` + `SEFLG_TOPOCTR` in `ephemeris.py` |
| Functional dignity in R02/R09 | S162 | `compute_functional_classifications(lagna_si)` replacing natural classification |
| Dasha scoring wired to `score_chart_v3` | S187 | Real implementation replacing stub; mutates `axes.d1.scores` when `on_date` supplied |
| War loser penalty in `_score_one_house` | S187 | `getattr(chart, 'planetary_war_losers', set())`; −1.5 penalty (Saravali Ch.4 v.18-22) |
| `strict_school` param on `score_axis`/`score_all_axes` | S187 | Wire live; `school_score_adjustment()` called in strict mode |
| XIX SVG/PDF/guidance/confidence API | S188 | 5 new endpoints in `src/api/main.py` |
| Postgres routing (`db_pg` replaces `db`) | S188 | `db_pg` with automatic SQLite fallback when `PG_DSN` unset |
| Swiss Ephemeris real files | S188 | `sepl_18.se1` + `semo_18.se1` from `github.com/aloistr/swisseph` |

---

## Bug Status (all resolved as of S188)

| ID | Status |
|----|--------|
| P-1 (midnight falsy) | ✅ FIXED S1-S2: `if hour is None` in `ephemeris.py` |
| P-4 (ayanamsha silent fail) | ✅ FIXED S1-S2: raises `ValueError` immediately |
| N-1 (Taurus=4yr) | ✅ FIXED S1-S2: corrected to 7yr in `narayana_dasa.py` |
| S-2 (J14=3851) | ✅ FIXED S8: `min(60, mean_motion/|speed|×60)` |
| E-1 | ✅ NOT PRESENT in Python — `swe.julday` handles it; regression test added |
| A-2 | ✅ NOT PRESENT in Python — `speed < 0` used directly; regression test added |

---

## Active Scoring Invariants (live as of S188)

| # | Invariant | Source |
|---|-----------|--------|
| 35 | War loser bhavesh = −1.5 penalty to house score (permanent) | Saravali Ch.4 v.18-22 |
| 36 | `strict_school=True` deducts Jaimini contributions in Parashari mode | Architecture decision |

Note: R17/R18 currently score 0.0 — so Invariant #36 has no numeric effect yet.

---

## Regression Standard

The regression suite is the **200+ ADB diverse fixture charts** (all 12 Lagnas,
Sections A–H of diverse_chart_fixtures.py). The pre-push hook runs the full
1338+ test suite. This is the quality gate for every session.

**India 1947 position verification** is NOT the standard regression gate.
It is only relevant in sessions where `ephemeris.py`, `varga.py`,
`narayana_dasa.py`, `nakshatra.py`, or `dignity.py` appear in the READ LIST
(i.e., sessions that touch the calculation substrate). The `start_session.py`
brief will call this out explicitly when relevant.

When India 1947 position verification IS needed:
```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,           # midnight IST — tests P-1 fix
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5, "ayanamsha": "lahiri",
}
# Lagna: 7.7286° Taurus (tolerance ±0.05°)
# Sun:   27.989° Cancer
# Moon:  3.9835° Cancer → Pushya nakshatra (index 7) → Saturn birth dasha (19yr)
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer
```

---

## Key Metrics (Post-S262)

| Metric | Current | Phase 1B Target | 2030 Target |
|--------|---------|-----------------|------------|
| Tests passing | **2,227** (3 skipped) | 4,000+ | 8,000+ |
| Lint errors | **0** | 0 | 0 |
| Corpus — Phase 1A representative | **2,634 rules** | complete | — |
| Corpus — Phase 1B sutra-level | **0 rules** | ~6,600 new | — |
| Corpus — combined target | 2,634 | **~9,200** | ~9,200+ |
| Phase 1B Rule Contract compliance | 0% | ≥90% of Phase 1B rules | 100% |
| Concordance ≥0.75 rules | 0 | ≥20% of Phase 1B | — |
| Ephemeris | **DE431 real files** | DE431 maintained | DE431 maintained |
| ADB fixtures | **200+** (all 12 Lagnas) | 200+ | 5,000+ |
| API endpoints | **10** | — | — |
| Brier score | Pre-baseline | Pre-baseline | ≤0.10 |
| Signal isolation | Pre-baseline | Pre-baseline | +0.22 |

---

## Session End Protocol (MANDATORY)

```bash
# 1. Full test suite
PYTHONPATH=. .venv/bin/pytest tests/ -q 2>&1 | tail -5

# 2. Lint
.venv/bin/ruff check src/ tests/ tools/

# 3. Commit
git add -A && git commit -m "feat(S[N]): [description]"
git push

# 4. Run documentation sync:
#    .venv/bin/python3 update_docs_s[N].py
#    git add docs/ MEMORY.md PLAN.md CHANGELOG.md README.md
#    git commit -m "docs(S[N]): sync documentation"

# 5. Update docs/MEMORY.md — change "Next Session", update metrics
# 6. Append to docs/CHANGELOG.md — use SESSION_TEMPLATE.md format
# 7. Mark fixed bugs in docs/BUGS.md
# 8. Update docs/KPIS.md if any metric moved
```
