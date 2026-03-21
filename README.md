# LagnaMaster

Vedic Jyotish computation engine + consumer guidance platform.

**963 tests | Sessions 1–100 complete | 100 modules | Engine v3.0.0**

> **Classical Audit — March 2026:** An independent audit against BPHS, Phaladeepika,
> Saravali, Brihat Jataka and Jaimini Sutras is complete. The scoring engine is a
> heuristic — additive numeric weights are not a classical methodology. Phase 0
> correctness fixes (Sessions 101+) are in progress on remote. See [`AUDIT.md`](AUDIT.md).

---

## What This Is

A comprehensive Jyotish platform covering:
- **Natal analysis** — 63 calculation modules, 23 BPHS rules × 12 houses × 5 lagna axes
- **Muhurta** — electional astrology with Panchanga, Tarabala, Chandrabala, Hora, Choghadiya
- **Prashna** — horary Jyotish from query-moment chart
- **All major dashas** — Vimshottari, Narayana, Yogini, Chara, Kalachakra, Ashtottari, Shoola, Sudasa, Tara
- **Upaya** — classical remedial measures (gemstones, deities, mantras, charity)
- **Mundane** — nation charts, solar/lunar ingress, swearing-in charts
- **Consumer layer** — Bloomberg-style guidance with safety pipeline, GDPR compliance, feedback governance

---

## Quick Start

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster && docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit (analyst) | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |
| Next.js (consumer) | http://localhost:3000 |

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ulimit -n 4096
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## Muhurta (Electional Astrology)

```python
from src.calculations.panchanga import compute_panchanga, compute_hora, compute_choghadiya
from src.calculations.muhurta import score_muhurta
from datetime import datetime

p = compute_panchanga(sun_lon, moon_lon, datetime.now())
score = score_muhurta("marriage", p,
                       birth_nakshatra=7,
                       birth_moon_sign=3,
                       muhurta_lagna_sign=1)
print(score.quality)      # "Excellent"/"Good"/"Acceptable"/"Avoid"
print(score.total_score)  # 0–7
print(score.warnings)
```

---

## Prashna (Horary)

```python
from src.calculations.prashna import analyze_prashna

result = analyze_prashna(prashna_chart, query_type="career",
                          query_dt=datetime.now())
print(result.verdict)     # "Yes — strongly indicated" / "Unlikely" etc.
print(result.confidence)  # "High"/"Moderate"/"Low"
print(result.reasoning)
```

---

## All Supported Dashas

```python
from src.calculations.vimshottari_dasa   import compute_vimshottari_dasa   # 120yr, 9 planets
from src.calculations.narayana_dasha     import compute_narayana_dasha      # 81yr Rasi dasha
from src.calculations.yogini_dasha       import compute_yogini_dasha        # 36yr cycle
from src.calculations.chara_dasha        import compute_chara_dasha         # Jaimini
from src.calculations.kalachakra_dasha   import compute_kalachakra_dasha    # 100yr, Moon D9
from src.calculations.ashtottari_dasha   import compute_ashtottari_dasha    # 108yr (conditional)
from src.calculations.shoola_dasha       import compute_shoola_dasha        # Longevity/Ayur
from src.calculations.shoola_dasha       import compute_sudasa              # Material success
from src.calculations.tara_dasha         import compute_tara_dasha          # 9-category nakshatra
```

---

## Upaya (Remedial Measures)

```python
from src.calculations.upaya import get_chart_upayas

upayas = get_chart_upayas(chart)
for u in upayas:
    print(f"{u.planet} ({u.affliction_type}):")
    print(f"  Gemstone: {u.gemstone} in {u.gemstone_metal} on {u.gemstone_day}")
    print(f"  Deity: {u.primary_deity}")
    print(f"  {u.disclaimer}")   # always present — never removed
```

---

## Consumer Guidance API

```python
from src.guidance.guidance_api import get_guidance

r = get_guidance(chart, domain="career", depth="L1", dashas=dashas)
print(r.signal_display)   # ●●●○○
print(r.timing_label)     # "Mixed — lean in"
print(r.summary)          # Human-safe sentence; no raw scores at L1/L2
print(r.disclaimer)
```

---

## Session History

| Phase | Sessions | Status | Key Deliverables |
|-------|----------|--------|-----------------|
| 1–3   | 1–27     | ✅     | Engine, scoring, FastAPI, Streamlit, Docker, JWT, K8s |
| 4–5   | 28–40    | ✅     | LPI, 5-axis scoring, rule interactions, Scoring v3 |
| 6     | 41–48    | ✅     | Ishta/Kashta, Longevity, Yogini, KP, 200+ Yogas, Empirica |
| 7     | 49–56    | ✅     | Sayanadi (12-state), Panchadha Maitri, Dig Bala continuous, Config toggles |
| 8     | 57–63    | ✅     | Orb strength, Yoga fructification, Stronger-of-two, AV transit |
| 9     | 64–70    | ✅     | Dominance engine, Promise/Manifestation, Confidence model |
| 10–11 | 71–78    | ✅     | Language safety pipeline, GDPR/DPDP consent + erasure |
| 12–14 | 79–90    | ✅     | Bloomberg UI, feedback governance, educational layer, mobile router |
| 15–18 | 91–100   | ✅     | **Muhurta, Prashna, Kalachakra, Ashtottari, Shoola, Tara, Upaya, Mundane** |
| 19+   | 101–108  | 🔄     | Phase 0 classical correctness fixes (on remote — `git pull` to get) |

---

## Coverage

| Branch | Status |
|--------|--------|
| Natal analysis (BPHS + PVRNR) | ✅ Complete |
| Divisional charts (20 vargas) | ✅ Complete |
| All 9 dasha systems | ✅ Complete |
| Muhurta (electional) | ✅ Session 92 |
| Prashna (horary) | ✅ Session 93 |
| Upaya (remedial measures) | ✅ Session 97 |
| Mundane astrology | ✅ Session 98 |
| Consumer safety + GDPR | ✅ Sessions 71–78 |
| Bloomberg UI (Next.js) | ✅ Built — integration testing pending |
| Phase 0 correctness (classical audit) | 🔄 Sessions 101+ |

**Acknowledged limits** (correctly excluded):
Full Prashna Marga corpus · Desha-Kala-Patra in full · Gestalt expert synthesis · Medical/financial astrology

---

## Stack

| Layer | Technology |
|-------|-----------|
| Ephemeris | pyswisseph (Lahiri / Raman / KP / Fagan-Bradley) |
| Backend | FastAPI + Celery + Redis |
| Database | SQLite → PostgreSQL + consent/feedback tables |
| Consumer UI | Next.js 14 + TypeScript + Tailwind |
| Mobile | FastAPI /mobile router (React Native shell pending) |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT + bcrypt |
| CI/CD | GitHub Actions |
| Privacy | GDPR Art.7+17 · DPDP · CCPA/CPRA |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [`PLAN.md`](PLAN.md) | Full session-by-session build plan and phase roadmap |
| [`docs/MEMORY.md`](docs/MEMORY.md) | Project state for Claude Code sessions — module inventory, invariants |
| [`AUDIT.md`](AUDIT.md) | Classical audit findings — gaps, correctness issues, cited ślokas |
| [`CHANGELOG.md`](CHANGELOG.md) | Session-by-session delivery history |
