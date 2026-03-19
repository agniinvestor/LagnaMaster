# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

## Architecture

```
Birth Data → ephemeris.py → calculations/ (19 modules) → scoring.py
          → report.py → worker.py (Celery) → api/main_v2.py
          → db_pg.py / db.py + cache.py
          → src/ui/app.py  (Streamlit — still active)
          → frontend/      (Next.js — replaces Streamlit long-term)
Auth:  src/auth.py + src/api/auth_router.py
CI/CD: .github/workflows/ci.yml → GHCR
K8s:   helm/lagnamaster/ (api + ui + worker + ingress + HPA)
```

## Phase 1 — Pilot ✅ 222/222
S1–S10: ephemeris, 7 calc modules, scoring+api+db, UI, Docker, vimshottari+SVG, yogas, AV, gochara, panchanga+D9

## Phase 2 — Features ✅ 225/225
S11–S19: pushkara+MC, milan, PDF, jaimini, KP, tajika, compat, APIv2, UI10tabs

## Phase 3 — Production

| S | Deliverable | Status | Tests |
|---|-------------|--------|-------|
| 20 | PostgreSQL + Redis + Alembic | ✅ Done | 35 |
| 21 | Celery + full UI wiring | ✅ Done | 25 |
| 22 | JWT multi-user auth | ✅ Done | 25 |
| 23 | GitHub Actions CI/CD + GHCR | ✅ Done | 20 |
| 24 | Kubernetes manifests + Helm chart | ✅ Done | 20 |
| 25 | Next.js 14 frontend (TypeScript + Tailwind) | ✅ Done | 30 |
| 26 | KP / Jaimini school gate configuration | 🔲 Next | — |
| 27 | Monte Carlo Celery concurrent scaling | 🔲 | — |

**Grand total: 627/627 tests passing**

## Accuracy Audit ✅ All Resolved
P-1 ✅ P-4 ✅ N-1 ✅ S-2 ✅ E-1 ✅ A-2 ✅
