# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook
into a deterministic, auditable Python web application.

**~789 tests passing | Sessions 1–48 complete | Engine v3.0.0**

---

## Quick Start

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |

**Local:**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ulimit -n 4096  # macOS: raise fd limit for test suite
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha)
3. Runs 23 BPHS scoring rules × 12 houses × 5 lagna axes (D1/Chandra/Surya/D9/D10)
4. Computes the 7-layer **Life Pressure Index** per house
5. Detects 200+ yogas (Nabhasa, Chandra, Surya, Dhana, Raja, Viparita, Jaimini)
6. Full KP sub-lord chain, Yogini Dasha, Ishta/Kashta Phala, longevity doctrine
7. Records birth-event correlations for empirical accuracy measurement
8. Serves results via FastAPI REST + Streamlit UI + Next.js frontend

---

## Life Pressure Index

```
LPI = D1×35% + Chandra×15% + Surya×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%
```

```python
from src.calculations.scoring_v3 import score_chart_v3

result = score_chart_v3(chart, dashas, on_date=date.today(), school="parashari")
for h, hl in result.lpi.houses.items():
    print(f"H{h}: {hl.full_index:+.2f} [{hl.rag}] {hl.confidence}")
print(result.lpi.domain_balance)  # Dharma/Artha/Kama/Moksha
```

---

## Regression Fixture — India 1947

| Field | Value |
|-------|-------|
| Birth | 1947-08-15 00:00 IST, New Delhi |
| Lagna | 7.7286° **Taurus** |
| Sun | 27.989° Cancer |
| Ayanamsha | Lahiri |
| Arudha Lagna | Virgo (H5) — verified |
| D9 Lagna | Pisces — verified |
| Baaladi Sun | Bala (even-sign reversal confirmed) |
| Baaladi Moon | Mrita (even-sign reversal confirmed) |
| KP Lagna nak lord | Sun (Krittika) — verified |

---

## Jyotish Coverage

| Module | Status |
|--------|--------|
| D1 scoring — 23 rules (R01–R23 incl. SAV) | ✅ |
| Chandra / Surya / D9 / D10 / Karakamsha axes | ✅ |
| 30-pair Rule Interaction Engine | ✅ |
| 7-layer Life Pressure Index | ✅ |
| All 12 Arudha Padas (AL, A2–A12, DL, UL) | ✅ |
| Vimshopaka Bala (16 vargas, max 20 pts) | ✅ |
| D60 Shastiamsha (60 named divisions) | ✅ |
| Raja + Dhana Yogas (13 pairs) | ✅ |
| Viparita Raja + Neecha Bhanga | ✅ |
| Nabhasa yogas (Rajju/Musala/Nala/Mala/Sarpa/Sankhya) | ✅ |
| Chandra yogas (Sunapha/Anapha/Durudhura/Kemadruma/Adhi) | ✅ |
| Surya yogas (Vesi/Vasi/Ubhayachari) | ✅ |
| Dhana yogas (Lakshmi/Duryoga/Daridra/Mahabhagya) | ✅ |
| Rasi Drishti (12×12 sign aspects) | ✅ |
| Bhavat Bhavam | ✅ |
| Baaladi avastha (even-sign reversal) | ✅ |
| Sayanadi avastha (12 mood states) | ✅ |
| Ishta / Kashta Phala (BPHS Ch.27) | ✅ |
| Longevity: Pindayu + Nisargayu + Amsayu | ✅ |
| Balarishta detection | ✅ |
| Yogini Dasha (8-lord 36-year cycle) | ✅ |
| Full KP sub-lord chain (sign→nak→sub→sub-sub) | ✅ |
| KP ruling planets + event promise | ✅ |
| Special lagnas (Hora/Ghati/Sree/Indu/Pranapada) | ✅ |
| Full Jaimini yogas + Karakamsha scoring | ✅ |
| Jaimini longevity (Brahma/Maheshvara/Rudra) | ✅ |
| Pada relationship scoring | ✅ |
| Empirical event log + accuracy metrics | ✅ |
| Shadbala | ✅ |
| Ashtakavarga (SAV) | ✅ |
| Vimshottari + Narayana + Chara + Yogini Dasha | ✅ |
| Gochara + Sade Sati | ✅ |
| KP Significators | ✅ |
| Varshaphala (Tajika) | ✅ |
| Kundali Milan (36-point) | ✅ |
| Monte Carlo birth-time sensitivity | ✅ |
| Narrative report + Scenario explorer | ✅ |

---

## API Reference

```
POST /charts                    compute + store chart
GET  /charts                    list recent charts
GET  /charts/{id}/scores        full 23-rule breakdown
POST /auth/register             register user
POST /auth/login                get JWT tokens
GET  /user/school               get scoring school
PUT  /user/school               set school (Parashari/KP/Jaimini)
POST /empirica/events           record birth event
GET  /empirica/events/{chart_id}  list events for chart
GET  /empirica/accuracy         per-rule accuracy metrics
```

---

## Session Progress

| Phase | Sessions | Key deliverables |
|-------|----------|-----------------|
| 1 — Pilot | 1–10 | Ephemeris, calc modules, D1 scoring, FastAPI, SQLite, Streamlit, Docker |
| 2 — Features | 11–19 | Pushkara, Kundali Milan, PDF, Jaimini, KP, Tajika, API v2, 12-tab UI |
| 3 — Production | 20–27 | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes, Next.js, School gates |
| 4 — Pressure Engine | 28–32 | Functional roles, Avastha, LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | Multi-lagna, 5-axis scoring, Rule interactions, 7-layer LPI, D60, Yogas, Scoring v3 |
| 6 — Classical Depth | 41–48 | Ishta/Kashta, Longevity, Yogini Dasha, Full KP, 200+ Yogas, Special Lagnas, Jaimini, Empirica |

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL via PG_DSN) |
| Cache | Redis (optional) |
| UI | Streamlit (10-tab) + Next.js 14 |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |

## Environment Variables

| Variable | Default | Notes |
|----------|---------|-------|
| PG_DSN | — | Absent = SQLite |
| REDIS_URL | redis://localhost:6379/0 | Empty = disabled |
| JWT_SECRET | dev-secret | **Change in prod** |
| ENABLE_KP | 1 | 0 = disable |
| ENABLE_JAIMINI | 1 | 0 = disable |
