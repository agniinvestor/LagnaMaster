# LagnaMaster — Project Memory

> Last updated: 2026-03-21 (Session 108)

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–108 |
| Tests passing | 990 |
| Engine version | 3.0.0 |
| Status | Phase 19 complete — all branches delivered |
| Branch | `claude/update-lagna-docs-iE2L6` |

---

## Module inventory (current)

```
src/
  ephemeris.py          planetary calculation wrapper (pyswisseph)
  scoring.py            22-rule BPHS house scoring engine
  db.py / db_pg.py      SQLite / PostgreSQL ORM
  cache.py              3-tier caching (process → Redis → DB)
  report.py             PDF generation (ReportLab)
  worker.py             Celery async tasks
  auth.py               JWT authentication
  config.py             configuration
  montecarlo.py         Monte Carlo sampling entry

  calculations/         84 modules — Phases 1–19
    Phase 1–3 (core):   dignity, nakshatra, friendship, house_lord, chara_karak,
                        narayana_dasha, shadbala, vimshottari_dasa, ashtakavarga,
                        gochara, panchanga, pushkara_navamsha, kundali_milan,
                        chara_dasha, kp_significators, varshaphala, varga,
                        sapta_varga, kp_full, kp.py

    Phase 4–5:          functional_roles, avastha, pressure_engine, argala,
                        graha_yuddha, scoring_v2, multi_lagna, multi_axis_scoring,
                        rule_interaction, lpi, divisional_charts, extended_yogas,
                        avastha_v2, narrative, scoring_v3, scenario

    Phase 6–7:          ishta_kashta, longevity, yogini_dasha, yogas_extended,
                        special_lagnas, jaimini_full, empirica, sayanadi_full,
                        panchadha_maitri, lagnesh_strength, dig_bala, yogas_graha,
                        narayana_argala, config_toggles, varga_agreement

    Phase 8–9:          orb_strength, yoga_fructification, stronger_of_two,
                        av_transit, arudha_perception, yogas_pvrnr,
                        planet_effectiveness, dominance_engine, promise_engine,
                        domain_weighting, planet_chains, house_modulation,
                        confidence_model, chart_exceptions

    Phase 15–18:        panchanga (supersedes panchang.py), muhurta, prashna,
                        kalachakra_dasha, shoola_dasha, tara_dasha, upaya,
                        mundane, contextual, ashtottari_dasha

    Phase 19:           drig_dasha, lagna_kendradi_dasha, double_transit,
                        upapada_lagna, kala_sarpa, nabhasa_yogas,
                        pitr_dosha, rule_plugin

  guidance/             8 modules — Phases 10, 14
    score_to_language, fatalism_filter, explainability_tiers,
    guidance_api, disclaimer_engine, educational_layer,
    reflection_prompts, practitioner_handoff

  privacy/              3 modules — Phase 11
    consent_engine, family_consent, data_minimisation

  feedback/             3 modules — Phase 13
    feedback_loop, harm_escalation, dependency_prevention

  api/
    main.py, main_v2.py, auth_router.py, school_router.py,
    empirica_router.py, mobile_router.py, models.py

frontend/
  Next.js 14 + TypeScript + Tailwind
  src/components/guidance/   DomainCard.tsx, SignalBar.tsx
  src/components/timing/     TimingCalendar.tsx
  src/components/onboarding/ OnboardingFlow.tsx
  src/app/api/guidance/      route.ts
```

---

## All dasha systems

| Dasha | File | Cycle |
|-------|------|-------|
| Vimshottari | vimshottari_dasa.py | 120yr |
| Narayana | narayana_dasha.py | 108yr rasi |
| Yogini | yogini_dasha.py | 36yr |
| Chara | chara_dasha.py | variable Jaimini |
| Kalachakra | kalachakra_dasha.py | 100yr Moon D9 |
| Ashtottari | ashtottari_dasha.py | 108yr, 8 planets |
| Shoola | shoola_dasha.py | variable ayur |
| Sudasa | shoola_dasha.py | variable material |
| Tara | tara_dasha.py | 120yr nakshatra |
| Drig | drig_dasha.py | variable rasi aspects |
| Lagna Kendradi | lagna_kendradi_dasha.py | variable Kendra/Panapara/Apoklima |

---

## Critical invariants (all 72)

**Engine (Phases 1–7):**
1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. DignityLevel: DEEP_EXALT/EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL_SIGN/ENEMY_SIGN/DEBIL/DEEP_DEBIL
4. WC rules R03/R05/R07/R14: always ×0.5
5. Streamlit Cloud entry: streamlit_app.py
6. MonteCarloResult: base_scores, mean_scores, std_scores, sensitivity, sample_count
7. Baaladi even-sign: sequence REVERSES (Mrita→Vridha→Yuva→Kumar→Bala from 0°→30°)
8. Sayanadi priority: Kopa > Deena > Sthira > Mudita > Kshuditha > Trashita > decanate > Prakrita
9. Yogini Dasha: nak_idx = floor(moon_lon × 27 / 360), start = nak_idx % 8
10. KP sub-lord spans: proportional to Vimshottari years within each nakshatra
11. Empirica event types: Career/Marriage/Divorce/Health_Crisis/Finance/Travel/Loss/Education/Other
12. ENGINE_VERSION = "3.0.0" on every score_run
13. Lagnesh modifier: −0.75 to +0.75 applied uniformly to all 12 house scores
14. Dig Bala: continuous 0.0–1.0; peak=1.0, opposite=0.0
15. Panchadha Maitri: Naisargika × Tatkalik = 5-fold (Adhi Mitra +1.0 … Adhi Shatru −1.0)
16. Narayana Dasha Argala: net modifier −0.5 to +0.5 per PVRNR Ch.5
17. Varga agreement: ★★ = High, ★ = Moderate, ○ = Low
18. Tatkalik Friend houses from P1: {2,3,4,10,11,12}; Enemy: {1,5,6,7,8,9}
19. Ayanamsha IDs: Lahiri=1, Raman=3, Krishnamurti=5, Fagan-Bradley=0
20. Deena state: planet in yuddha_losers set passed from graha_yuddha.py

**Phase 8 (PVRNR Tier 1):**
21. Orb formula: `strength = max(0, 1 − orb_degrees / 15)` — 0.5 at 6°, 0.33 at 8°
22. Yoga fructification: all three PVRNR conditions must pass for Full verdict
23. Stronger-of-two hierarchy: cotenants > dignity > exalted cotenants > rasi aspects > degree
24. AV transit: BAV ≥5 rekhas = favorable, ≤3 = unfavorable
25. AL perception: strong house + weak AL = Hidden Success; weak + strong AL = Apparent Success
26. Planet effectiveness: summary-only — does NOT replace specific-purpose measures
27. Amsa level: uses minimum across yoga planets (weakest link)

**Phase 9 (Synthesis):**
28. Dominance engine: encodes named BPHS rules only — not gestalt synthesis
29. Promise: "dasha cannot produce what's absent" — ceiling applies even with activation
30. Domain weights all sum to exactly 1.0
31. Stellium = 3+ planets in same sign
32. Dispositor chain terminates at own-sign planet (max depth 9, cycle-safe)
33. Upachaya age modifier: 35y = 0.80×, 60y = 1.00×
34. Confidence: requires_expert_review when label="Uncertain" OR flags ≥ 3

**Consumer Pipeline (Phases 10–14):**
35. Raw LPI/house scores gated behind L3 explicit opt-in
36. L3 opt-in resets each session — no persistent L3 mode
37. Signal system is 5-bar (0–5) — never percentages or star ratings
38. All guidance uses possibility language — never deterministic claims
39. Feedback loop: human-supervised only — no automated parameter changes
40. Right-to-erasure cascade: outputs + birth data + event log → tombstone
41. Family cross-analysis requires active consent from every individual
42. Dependency nudge: ≥ 3 sessions/day or ≥ 15/week

**Privacy:**
43. Birth time stored to minute precision only (seconds stripped)
44. IP addresses hashed (SHA-256, first 16 chars) on ingress
45. Location stored to city level only
46. Raw birth data deleted after 90 days of user inactivity
47. Event log anonymised after 1 year (user_id → hash)
48. Age gate: under-18 blocked from chart creation

**Safety:**
49. Fatalism filter applied to ALL text before any API response
50. Harm escalation: gentle prompt only — no automatic intervention
51. No crisis resources surfaced unless explicitly requested by user
52. Practitioner referral when confidence = "Uncertain" or critical exceptions > 0
53. No streak mechanics, no badges, no unsolicited push notifications
54. Dependency nudge text: no shaming or alarming language

**Phase 15–18 (Muhurta/Prashna/Dashas/Upaya/Mundane):**
55. Muhurta score 0-7: Excellent≥5, Good≥4, Acceptable≥3, Avoid<3
56. Tarabala good groups: {1,3,5,7}
57. Chandrabala good positions: {1,3,6,7,10,11} from birth Moon sign
58. Kalachakra: BPHS Ch.36 canonical; Savya=odd-pada, Apasavya=even-pada
59. Ashtottari: only when Rahu NOT in H1 or H7
60. Tara good categories: Sampat/Kshema/Sadhana/Mitra/Ati-Mitra
61. Upaya disclaimer present on every recommendation — non-negotiable
62. Mundane SAV threshold: ≥30 rekhas = strong house
63. panchanga.py supersedes panchang.py; test_panchanga_legacy.py is empty stub
64. Bandhu Yoga in jaimini_full.py uses self-contained AK lookup

**Phase 19 (Advanced Dashas/Yogas/Plugins):**
65. Drig Dasha: starts Lagna if Lagna>Moon, else Moon sign; odd=forward, even=reverse
66. Lagna Kendradi: Kendra group first → Panapara → Apoklima; period = planets+1
67. Double Transit: Both Jupiter+Saturn must aspect for "Double confirmation"
68. Upapada: if computed UL falls H1 or H7 from AL, shift 10 signs (PVRNR exception)
69. Kala Sarpa: classical_disclaimer field mandatory — yoga not in BPHS
70. Nabhasa: only strongest yoga per group manifests; all 32 from BPHS Ch.35
71. Pitr Dosha: classical_disclaimer mandatory; modern convention not in BPHS
72. Plugin yogas: all results carry plugin_note; never override core engine outputs

---

## Remaining gaps (not omissions — correctly excluded)

| Item | Reason |
|------|--------|
| Prashna Marga full corpus | Separate text — different discipline |
| Full Desha-Kala-Patra | Requires practitioner situational judgment |
| Gestalt synthesis | Named BPHS rules encoded; nonlinear expert weighting is not |
| Medical/financial astrology | Separate discipline — outside scope |
| Kalachakra textual variants | BPHS version implemented; other commentators differ |

---

## Post-launch priorities (product decisions, not sessions)

1. End-to-end integration test: Next.js ↔ FastAPI ↔ guidance pipeline
2. React Native mobile shell (router complete at Session 90)
3. Practitioner opt-in directory (infrastructure at Session 89)
4. First 50 empirica events for accuracy baseline
5. GDPR-compliant privacy policy + ToS text (legal team)
