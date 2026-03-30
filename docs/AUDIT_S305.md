# Project Audit — Post-S305 (March 30, 2026)

## Executive Summary

The project has 6,585 corpus rules but only 3,955 (60%) are Phase 1B compliant.
The remaining 2,630 Phase 1A rules — including all 1,239 BPHS rules — have zero
structured fields (no primary_condition, no outcome_domains, no verse_ref). BPHS
is the foundational concordance anchor for Parashari astrology and its absence
from the structured corpus means all concordance scoring is incomplete.

Three protocol gaps have caused rework this session: skipped concordance workflow,
skipped documentation updates, and rule counts anchored to arbitrary targets
instead of text depth. Machine enforcement exists for some protocols (pre-push
hook, contract tests) but not others (doc completeness, concordance generation,
modifier population).

---

## 1. Corpus Compliance Audit

### Phase 1B Sources (PRODUCTION READY with gaps)

| Source | Rules | primary_condition | outcome_domains | verse_ref | concordance | modifiers | exceptions | dasha_scope | lagna_scope |
|--------|-------|-------------------|-----------------|-----------|-------------|-----------|------------|-------------|-------------|
| BhavarthaRatnakara | 780 | 100% | 100% | 100% | 44% | 0% | 0% | 0% | 100% |
| LaghuParashari | 277 | 100% | 100% | 100% | 0% | 0% | 0% | 0% | 63% |
| Saravali | 2,898 | 100% | 100% | 100% | 9.5% | 0% | 0% | 0% | 0% |
| **Phase 1B Total** | **3,955** | **100%** | **100%** | **100%** | **16%** | **0%** | **0%** | **0%** | **25%** |

### Phase 1A Sources (REQUIRE RE-ENCODE)

| Source | Rules | primary_condition | outcome_domains | verse_ref | Status |
|--------|-------|-------------------|-----------------|-----------|--------|
| BPHS | 1,239 | 0% | 0% | 0% | CRITICAL — concordance anchor missing |
| Brihat Jataka | 190 | 0% | 0% | 0% | Needs 1B re-encode |
| Uttara Kalamrita | 201 | 0% | 0% | 0% | Needs 1B re-encode |
| Jataka Parijata | 197 | 0% | 0% | 0% | Needs 1B re-encode |
| Sarvartha Chintamani | 170 | 0% | 0% | 0% | Needs 1B re-encode |
| Jaimini Sutras | 178 | 0% | 0% | 0% | Needs 1B re-encode |
| Phaladeepika | 189 | 0% | 0% | 0% | Needs 1B re-encode |
| Lal Kitab | 120 | 0% | 0% | 0% | Needs 1B re-encode (separate schema) |
| Chandra Kala Nadi | 120 | 0% | 0% | 0% | Needs 1B re-encode (nadi schema) |
| KP | 30 | 0% | 0% | 0% | Needs 1B re-encode (school=kp) |
| **Phase 1A Total** | **2,630** | **0%** | **0%** | **0%** | **All need re-encode** |

### Fields Never Populated Anywhere

| Field | Status | Impact |
|-------|--------|--------|
| `modifiers` | 0/6,585 rules | Cannot evaluate "if aspected by Jupiter..." conditions |
| `exceptions` | 0/6,585 rules | Cannot evaluate "unless combust..." cancellations |
| `dasha_scope` | 0/6,585 rules | Cannot build temporal model (Phase 5 blocked) |

---

## 2. Text Scope Audit

### Texts in ROADMAP vs CLASSICAL_CORPUS.md vs Research Findings

| Text | ROADMAP | CLASSICAL_CORPUS | Research Finding | Gap |
|------|---------|------------------|-----------------|-----|
| BPHS (97 ch) | Not listed for 1B re-encode | Phase 1A only | ~4,000-5,000 rules at sutra level | CRITICAL: not planned for re-encode |
| Brihat Jataka (28 ch) | Not listed | Phase 1A only | ~800-1,000 at sutra level | Not planned |
| Phaladeepika (27 ch) | Not listed | Phase 1A only | ~500-700 at sutra level | Not planned |
| Uttara Kalamrita (7 ch) | Not listed | Phase 1A only | ~600-800 at sutra level | Not planned |
| Jataka Parijata (30 ch) | Not listed | Phase 1A only | ~600-800 at sutra level | Not planned |
| Sarvartha Chintamani | Not listed | Phase 1A only | ~500-600 at sutra level | Not planned |
| Jaimini Sutras | Not listed | Phase 1A only | ~400-500 at sutra level | Not planned |
| Laghu Parashari | ✅ Done | ✅ Done | 306 actual | Complete |
| Bhavartha Ratnakara | ✅ Done | ✅ Done | 780 actual | Complete |
| Saravali | ✅ Done | Outdated estimate | 2,898 actual | Complete |
| Chamatkara Chintamani | Planned S306-S312 | ~550 | Unknown at sutra level | Not started |
| Hora Ratnam | Planned S313-S320 | ~600 | Unknown at sutra level | Not started |
| Prasna Marga | Planned S321-S332 | ~950 | Unknown at sutra level | Not started |
| Tajika Neelakanthi | Planned S333-S338 | ~255 | Unknown at sutra level | Not started |
| Mansagari | Planned S339-S360 | ~300 (old) / ~3,300 (revised) | ~2,755-3,850 | Not started |
| Jataka Tattva | Planned S361-S390 | ~270 (old) / ~4,700 (revised) | ~3,940-5,460 | Not started |
| Stri Jataka | Planned S391-S400 | Bundled (old) / ~1,500 (revised) | ~1,300-1,840 | Not started |
| Muhurtha Chintamani | Planned S401-S410 | Not listed | ~2,310-3,120 | Not started |
| Yoga Expansion | Not listed | Not listed | ~1,649 | Not planned |
| KP Comprehensive | Old plan only | ~300 | Unknown at sutra level | Not planned in revised ROADMAP |
| Nadi texts (Bhrigu/Suka/Dhruva) | Old plan only | ~240 | Unknown | Not planned in revised ROADMAP |

**CRITICAL GAP:** The 7 primary Parashari texts (BPHS, Brihat Jataka, Phaladeepika,
Uttara Kalamrita, Jataka Parijata, Sarvartha Chintamani, Jaimini Sutras) have Phase 1A
encodings that are unusable for ML. They are not scheduled for Phase 1B re-encode in
either ROADMAP or CLASSICAL_CORPUS.md. Combined, these represent ~7,500-9,500 rules
at sutra level that are missing from the plan.

---

## 3. Protocol & Enforcement Audit

### What's Machine-Enforced (Cannot Be Skipped)

| Protocol | Mechanism | Blocks push? |
|----------|-----------|-------------|
| All tests pass | Pre-push hook → pytest | YES |
| Ruff lint clean | Pre-push hook → ruff | YES |
| MEMORY.md test count current | Pre-push hook → count check | YES |
| Phase 1B mandatory fields | test_phase1b_contract.py (11 tests) | YES |
| Confidence formula mechanical | test_phase1b_contract.py | YES |
| Outcome domains from taxonomy | test_phase1b_contract.py | YES |

### What's Memory-Only (Can Be Skipped — HAS Been Skipped)

| Protocol | Memory File | Times Skipped |
|----------|------------|---------------|
| Update all 5 docs | feedback_docs_protocol.md | 36 sessions (S270-S305) |
| Exhaustive rule counts | feedback_exhaustiveness.md | S281-S284 (trimmed to 130) |
| Concordance workflow | PHASE1B_CONCORDANCE_WORKFLOW.md | All sessions until backfill |
| Depth over throughput | feedback_depth_over_throughput.md | New — untested |
| Continuous ML integration | feedback_continuous_ml_integration.md | New — untested |
| VedAstro cross-validation | SESSION_TEMPLATE.md | All sessions |

### What Has No Enforcement At All

| Protocol | Status | Risk |
|----------|--------|------|
| SESSION_LOG.md updated | No check | Already failed for 36 sessions |
| ARCHITECTURE.md updated | No check | Already failed for 36 sessions |
| ROADMAP.md session marks | No check | Partially done |
| Coverage map created before encoding | No check | Saravali map created mid-session |
| Concordance run after each batch | No check | Skipped entirely until today |
| Modifiers/exceptions populated | No test | 0% populated, no test requires it |
| dasha_scope populated | No test | 0% populated, no test requires it |
| VedAstro cross-validation | No check | Never done |
| OB-3 measurement after batch | No check | First run today |

---

## 4. Recommendations

### R1: BPHS Phase 1B Re-Encode (HIGHEST PRIORITY)

BPHS is the concordance anchor. Without it, concordance scoring across all other
texts is incomplete. BPHS should be re-encoded at Phase 1B depth BEFORE any new
text encoding (Chamatkara Chintamani etc.) begins.

Scope: 97 chapters, estimated 4,000-5,000 rules at sutra level.
Approach: Chapter-by-chapter with coverage map, same protocol as Saravali.

### R2: Primary Parashari Texts Re-Encode (HIGH PRIORITY)

After BPHS, the 6 other primary Parashari texts (Brihat Jataka, Phaladeepika,
Uttara Kalamrita, Jataka Parijata, Sarvartha Chintamani, Jaimini Sutras) should
be re-encoded at Phase 1B depth. These are the concordance targets — without
them, the concordance system can only cross-reference Saravali↔BVR↔LP.

### R3: Pre-Session Checklist (Machine-Enforced)

Add to pre-push hook or as a separate test:
1. SESSION_LOG.md contains entry for current session range
2. ARCHITECTURE.md contains entry for any new src/ modules
3. Coverage map exists before any corpus module is committed
4. Concordance map regenerated after any corpus change
5. Rule-firing test run against India 1947 after corpus change

### R4: Per-Rule Quality Checklist

Each rule should be evaluated against:
1. Does the primary_condition capture the FULL triggering condition?
2. Are there modifiers (aspects, dignities) stated in the verse? → populate modifiers
3. Are there exceptions ("unless combust", "if retrograde") → populate exceptions
4. Is dasha_scope applicable? (dasha-result rules) → populate
5. Is lagna_scope applicable? (lagna-conditional rules) → populate
6. Does the verse state a DIFFERENT outcome than another text? → divergence_notes
7. Does the description lose nuance vs the original verse? → rewrite

### R5: Sutra-to-Rule Completeness Standard

A chapter is "complete" when:
1. Every predictive verse has been read and extracted
2. Each verse with multiple distinct outcomes produces multiple rules
3. Conditional clauses ("if aspected by...", "unless combust...") are modifiers, not ignored
4. Verse-level attribution is traceable (Ch.N v.M format)
5. The coverage map section shows actual count, not estimated count

### R6: Update CLASSICAL_CORPUS.md and ROADMAP.md

Both documents are stale. They need to reflect:
- BPHS + 6 primary texts planned for Phase 1B re-encode
- Corrected Saravali actual count (2,898 not ~1,400)
- KP, Nadi texts status (dropped or rescheduled?)
- Yoga Expansion (~1,649 rules) added or deferred?
- Muhurtha Chintamani separate pipeline documented

### R7: Modifier and Exception Population

Current: 0% of rules have modifiers or exceptions.
Target: Every rule with a conditional clause in the source verse should have
the condition encoded as a modifier or exception.

This is not rework — it's completing work that was started but not finished.
The fields exist on RuleRecord; they're just never populated.

### R8: dasha_scope Population

Current: 0% of rules have dasha_scope.
The temporal model (Phase 5) needs to know which rules are dasha-dependent.
Any rule with outcome_timing="dasha_dependent" should have dasha_scope
populated with relevant dasha lords.

---

## 5. Encoding Priority Order (Revised)

Based on this audit, the encoding priority should be:

1. **BPHS Phase 1B re-encode** (97 chapters) — concordance anchor
2. **Brihat Jataka Phase 1B re-encode** (28 chapters) — second most cited
3. **Phaladeepika Phase 1B re-encode** (27 chapters) — third most cited
4. **Remaining primary texts** (Uttara Kalamrita, Jataka Parijata, Sarvartha Chintamani)
5. **Chamatkara Chintamani** (new encoding)
6. **Hora Ratnam** (new encoding)
7. **Mansagari, Jataka Tattva, Stri Jataka** (new encoding)
8. **Prasna Marga** (system=horary, separate pipeline)
9. **Tajika Neelakanthi** (system=varshaphala, separate pipeline)
10. **Muhurtha Chintamani** (system=muhurtha, separate pipeline)
