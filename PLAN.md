# LagnaMaster — Programme Plan

## Status: COMPLETE — Sessions 1–40 ✅

743 tests passing. ENGINE_VERSION = "3.0.0". All planned phases delivered.

---

## Phase Summary

### Phase 1 — Pilot (Sessions 1–10) ✅ 222 tests
- S1: ephemeris.py (pyswisseph wrapper, Lahiri ayanamsha, 1947 fixture)
- S2: 7 calculation modules (dignity, nakshatra, friendship, house_lord, chara_karak, narayana_dasha, shadbala)
- S3: scoring.py + FastAPI + SQLite
- S4: Streamlit 3-tab UI
- S5: Docker Compose + integration tests
- S6: Vimshottari Dasha + SVG chart
- S7: Yogas (Pancha Mahapurusha, Gajakesari, Kemadruma)
- S8: Ashtakavarga (SAV bindus)
- S9: Gochara + Sade Sati
- S10: Panchanga + D9 Navamsha

### Phase 2 — Features (Sessions 11–19) ✅ 225 tests
- S11: Pushkara Navamsha + Monte Carlo birth-time sensitivity
- S12: Kundali Milan 36-point compatibility
- S13: PDF report generation (reportlab)
- S14: Jaimini Chara Dasha
- S15: KP Significators + sub-lord table
- S16: Varshaphala / Tajika annual chart
- S17: Compatibility scoring
- S18: API v2 endpoints
- S19: Streamlit 12-tab UI

### Phase 3 — Production (Sessions 20–27) ✅ 210 tests
- S20: PostgreSQL (db_pg.py) + Redis 3-tier caching
- S21: Celery async workers (compute_chart, monte_carlo, generate_pdf)
- S22: JWT multi-user auth
- S23: GitHub Actions CI/CD
- S24: Kubernetes Helm chart (HPA, ingress, secrets)
- S25: Next.js 14 frontend (TypeScript + Tailwind)
- S26: School gates (Parashari/KP/Jaimini per-user)
- S27: Monte Carlo Celery chord (parallel sampling)

### Phase 4 — Pressure Engine (Sessions 28–32) ✅ 36 tests
- S28: functional_roles.py (per-lagna maleficence, badhaka, maraka, yogakaraka)
- S29: avastha.py (Deeptadi/Baladi/Lajjitadi)
- S30: pressure_engine.py (Life Pressure Index v1, D1 approximation)
- S31: argala.py (Argala/Virodhargala + Arudha Lagna)
- S32: graha_yuddha.py + scoring_v2.py (ENGINE_VERSION="2.0.0")

### Phase 5 — Full Workbook Parity (Sessions 33–40) ✅ 50 tests
- S33: multi_lagna.py (Chandra/Surya/Karakamsha frames, all 12 Arudha Padas)
- S34: multi_axis_scoring.py (23-rule engine × 5 axes, R23 SAV, school weights)
- S35: rule_interaction.py (30 rule-pair modifiers from REF_RuleInteractionMatrix)
- S36: lpi.py (full 7-layer LPI, dasha modifier ×1.15, domain balance)
- S37: divisional_charts.py (all 16 vargas, Vimshopaka Bala, D60 Shastiamsha)
- S38: extended_yogas.py (Raja/Dhana/Viparita/NeechaBhanga, Rasi Drishti, Bhavat Bhavam)
- S39: avastha_v2.py (Baaladi even-sign fix), narrative.py
- S40: scoring_v3.py (ENGINE_VERSION="3.0.0"), scenario.py

---

## Remaining Gaps (out of scope)

| Sheet | Reason not built |
|-------|-----------------|
| UX_StudentMode | Pedagogical UI layer — product decision needed |
| API_ProkeralaScript | External API integration — not in scope |
| REF_EmpiricaSchema | Event log + statistical validation backend — requires real birth data corpus |
| NOTES_* / HOWTO_* | Documentation only — no code equivalent |
