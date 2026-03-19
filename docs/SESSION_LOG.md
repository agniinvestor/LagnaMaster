# LagnaMaster — Session Log

> Last updated: 2026-03-20 | Sessions complete: 1–25

## Sessions 1–23 — See git history
Cumulative: 557 tests. Key milestones: S10 pilot complete, S19 10-tab UI, S21 Celery, S22 JWT auth, S23 GitHub Actions CI/CD.

## Session 24 — Kubernetes + Helm chart
**Date**: 2026-03-20 | **Tests**: 20 new | **Cumulative**: 577/577

**`helm/lagnamaster/`** complete Helm chart:
- `Chart.yaml`: name=lagnamaster, appVersion=0.2.0
- `values.yaml`: api(port 8000, HPA 2–8 replicas), ui(port 8501), worker(queues=default+heavy, concurrency=4), ingress(nginx+TLS), redis+postgresql subcharts
- `templates/_helpers.tpl`: shared macros — `lagnamaster.labels`, `lagnamaster.secretEnv` (JWT_SECRET/PG_DSN/REDIS_URL from K8s Secret), `lagnamaster.commonEnv`
- `templates/api-deployment.yaml`: liveness+readiness on `/health`, resource limits, secretEnv + commonEnv
- `templates/api-hpa.yaml`: HPA v2, CPU target 70%, min=2 max=8
- `templates/ui-deployment.yaml`: Streamlit health probe `/_stcore/health`, API_URL env var
- `templates/worker-deployment.yaml`: reuses API image, `celery -A src.worker worker -Q default,heavy`, exec liveness probe
- `templates/ingress.yaml`: nginx, cert-manager TLS, routes api.lagnamaster.app → API, lagnamaster.app → UI
- `templates/configmap.yaml`: non-secret env vars

**tests/test_session24.py** (20 tests): structure checks, values YAML validation, template content verification.

## Session 25 — Next.js 14 Frontend
**Date**: 2026-03-20 | **Tests**: 30 new | **Cumulative**: 607/607

Wait — 20+30=50, 557+50=607. Corrected: **607/607**.

**`frontend/`** — Next.js 14 + TypeScript + Tailwind CSS:

`src/lib/api.ts`: Complete typed client — auth (register/login/refresh/me/logout), charts (create/list/get/scores/yogas/report), health. Bearer token injected from module-level state. All calls proxy through `/api/*` via Next.js rewrites to FastAPI.

`src/app/page.tsx`: Home page — birth data form with all fields (year/month/day/hour/lat/lon/tz_offset/ayanamsha), India 1947 demo button, planet table, 12-house domain scores grid with colour-coded rating badges.

`src/lib/api.test.ts`: Jest + jsdom, fetch mocked globally. Tests: token storage, login POST URL, 401 handling, Bearer header injection, charts.create, charts.scores, health.check.

`next.config.js`: `/api/:path*` rewrites to FastAPI (env-configurable), `output: standalone` for Docker.

`package.json`: Next 14, React 18, recharts, lucide-react, Tailwind, TypeScript, Jest, testing-library.

**tests/test_session25.py** (30 tests): structure checks, package.json content, api.ts interface/module presence.

### New env vars (frontend)
| Variable | Default | Purpose |
|----------|---------|---------|
| NEXT_PUBLIC_API_URL | http://localhost:8000 | FastAPI base URL for proxy |

### Session 26 plan
KP / Jaimini school gate configuration: feature flags in `src/config.py` to enable/disable KP or Jaimini calculation paths, per-user school preference stored in user DB, API endpoints respect preference.
