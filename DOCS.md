# LagnaMaster — Technical Documentation

> Last updated: 2026-03-20 | Sessions 1–25 | 627/627 tests

## Repository Structure (Session 25)

```
LagnaMaster/
├── streamlit_app.py        Streamlit Cloud entry point
├── PLAN.md / DOCS.md / README.md
├── requirements.txt        16 Python packages
├── alembic.ini / migrations/
├── .github/workflows/ci.yml
├── helm/lagnamaster/       Kubernetes + Helm chart  [S24]
│   ├── Chart.yaml / values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── api-deployment.yaml / api-service.yaml / api-hpa.yaml
│       ├── ui-deployment.yaml / ui-service.yaml
│       ├── worker-deployment.yaml
│       ├── ingress.yaml / configmap.yaml
│       └── NOTES.txt
├── frontend/               Next.js 14 frontend  [S25]
│   ├── package.json / next.config.js / tsconfig.json
│   ├── tailwind.config.ts / jest.config.js
│   └── src/
│       ├── app/
│       │   ├── page.tsx        Home — birth form + chart display
│       │   ├── layout.tsx      Root layout
│       │   └── globals.css     Tailwind base
│       └── lib/
│           ├── api.ts          Typed fetch client for FastAPI
│           └── api.test.ts     Jest unit tests
├── docs/SESSION_LOG.md / MEMORY.md
└── src/  (Python backend — unchanged from S23)
```

## Session 24 — Kubernetes + Helm

**`helm/lagnamaster/`** — production-ready Helm chart deploying 3 workloads:

| Workload | Image | Replicas | Notes |
|----------|-------|----------|-------|
| `lagnamaster-api` | `ghcr.io/agniinvestor/lagnamaster-api` | 2 (HPA: 2–8) | `/health` liveness + readiness |
| `lagnamaster-ui` | `ghcr.io/agniinvestor/lagnamaster-ui` | 1 | `/_stcore/health` probe |
| `lagnamaster-worker` | `lagnamaster-api` (reused) | 2 | `celery -A src.worker worker -Q default,heavy` |

**Key features:**
- HPA on API: scales 2→8 pods at 70% CPU
- Ingress with TLS (cert-manager + letsencrypt-prod)
- Secrets: `lagnamaster-secrets` (JWT_SECRET, PG_DSN, REDIS_URL)
- `_helpers.tpl`: `lagnamaster.labels`, `lagnamaster.secretEnv`, `lagnamaster.commonEnv`

**Deploy:**
```bash
# Create secret first
kubectl create secret generic lagnamaster-secrets \
  --from-literal=JWT_SECRET=<secret> \
  --from-literal=PG_DSN=postgresql://... \
  --from-literal=REDIS_URL=redis://...

helm install lagnamaster ./helm/lagnamaster
helm upgrade lagnamaster ./helm/lagnamaster --set image.tag=<sha>
```

## Session 25 — Next.js Frontend

**`frontend/`** — Next.js 14 + TypeScript + Tailwind CSS.

**`src/lib/api.ts`** — typed fetch client:
```typescript
// Auth
auth.register(username, email, password) → UserOut
auth.login(username, password)           → TokenOut
auth.refresh(refresh_token)              → TokenOut
auth.me()                                → UserOut

// Charts
charts.create(BirthDataRequest)          → ChartOut
charts.list(limit?)                      → ChartOut[]
charts.get(id)                           → ChartOut
charts.scores(id)                        → ChartScoresOut
charts.yogas(id)                         → YogaOut[]
charts.report(id)                        → Blob  (PDF)

// Health
health.check()                           → HealthOut
```

All calls proxy through `/api/*` → FastAPI via `next.config.js` rewrites.

**`src/app/page.tsx`** — home page: birth data form (year/month/day/hour/lat/lon/tz/ayanamsha), India 1947 demo button, domain scores grid with rating badges.

**Run frontend:**
```bash
cd frontend
npm install
npm run dev    # http://localhost:3000
npm test       # Jest + fetch mock
```

## Test Suite — 627 total

```
S1–S10  pilot          222
S11–S19 features       225
S20–S23 prod infra     115
S24     helm            20   TestHelmStructure(12) TestHelmContent(8) TestTemplateSyntax(8)
S25     next.js         30   TestFrontendStructure(9) TestPackageJson(10) TestApiClient(11)
                       ────
                        627
```

## Helm Quick Reference

```bash
helm lint ./helm/lagnamaster
helm template ./helm/lagnamaster | kubectl apply --dry-run=client -f -
helm install lagnamaster ./helm/lagnamaster -n production --create-namespace
helm upgrade lagnamaster ./helm/lagnamaster --set image.tag=$(git rev-parse --short HEAD)
helm rollback lagnamaster 1
helm uninstall lagnamaster
```
