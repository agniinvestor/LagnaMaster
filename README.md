# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook
into a deterministic, auditable Python web application.

**~850 tests | Sessions 1–56 complete | Engine v3.0.0 | Every CALC_ sheet implemented**

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
ulimit -n 4096   # macOS: raise file descriptor limit
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri, Raman, KP, or Fagan-Bradley ayanamsha)
3. Runs 23 BPHS scoring rules × 12 houses × 5 lagna axes (D1/Chandra/Surya/D9/D10)
4. Applies Lagnesh global modifier, Dig Bala continuous scores, full 12-state Sayanadi
5. Computes the 7-layer **Life Pressure Index** with varga agreement confidence flags
6. Detects 200+ yogas (Nabhasa, Chandra, Surya, Dhana, Raja, Viparita, Graha, Jaimini)
7. Full KP sub-lord chain, Yogini Dasha, Ishta/Kashta Phala, three longevity methods
8. Records birth-event correlations for empirical accuracy measurement
9. Serves results via FastAPI REST + Streamlit UI + Next.js frontend

---

## Life Pressure Index

```
LPI = D1×35% + Chandra×15% + Surya×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%
```

Varga agreement confidence (Phase 7):
- ★★ D1/D9/D10 all agree → High confidence
- ★  D1+D9 agree → Moderate confidence
- ○  Vargas diverge → Low confidence (nuanced interpretation needed)

```python
from src.calculations.scoring_v3 import score_chart_v3
from src.calculations.varga_agreement import compute_varga_agreement

result = score_chart_v3(chart, dashas, on_date=date.today(), school="parashari")
agree  = compute_varga_agreement(chart)

for h, hl in result.lpi.houses.items():
    flag = agree.flag_for(h)
    print(f"H{h}: {hl.full_index:+.2f} [{hl.rag}] {flag} {hl.confidence}")
```

---

## Configuration Toggles (REF_Config)

All workbook configuration options are now exposed:

```python
from src.calculations.config_toggles import CalcConfig

cfg = CalcConfig(
    school="kp",                  # parashari | kp | jaimini
    ayanamsha="krishnamurti",     # lahiri | raman | krishnamurti | fagan_bradley
    retrograde_policy="classical",# apply | ignore | classical
    node_type="true",             # mean | true
    yogakaraka_weight=1.5,        # 1.5 | 1.25 | 1.0
    wc_aspect_weight=0.75,        # 0.5 | 0.75 | 1.0
)
```

---

## Regression Fixture — India 1947

| Field | Value | Verified |
|-------|-------|---------|
| Birth | 1947-08-15 00:00 IST, New Delhi | |
| Lagna | 7.7286° Taurus | ✓ |
| Sun | 27.989° Cancer | ✓ |
| Arudha Lagna | Virgo | ✓ |
| D9 Lagna | Pisces | ✓ |
| KP Lagna nak lord | Sun (Krittika) | ✓ |
| Baaladi Sun | Bala (even-sign reversal) | ✓ |
| Baaladi Moon | Mrita (even-sign reversal) | ✓ |
| Moon Sayanadi | Sthira (own sign Cancer) | ✓ |
| Lagnesh modifier | 0.00 (Venus H3, neutral) | ✓ |
| Dig Bala Sun | 0.167 (H3, peak H10, dist=5) | ✓ |
| Dig Bala Moon | 0.833 (H3, peak H4, dist=1) | ✓ |
| Budhaditya Yoga | Present (Sun+Mer in Cancer) | ✓ |
| Gaja Kesari Yoga | Present (Jup H6, Moon H3) | ✓ |
| H2 Wealth varga | ★★ (D1/D9/D10 all negative) | ✓ |

---

## Jyotish Coverage — Complete

### Parāśara (BPHS)
| Module | Status |
|--------|--------|
| D1 scoring — 23 rules (R01–R23) | ✅ |
| Panchadha Maitri (5-fold relationship) wired to R06/R07/R13/R14 | ✅ |
| Lagnesh global modifier (−0.75 to +0.75) applied to all 12 houses | ✅ |
| Dig Bala continuous 0.0–1.0 score (BPHS Ch.27) | ✅ |
| Baaladi avastha (even-sign reversal) | ✅ |
| Full 12-state Sayanadi (all decanate + dignity + war states) | ✅ |
| Ishta / Kashta Phala (BPHS Ch.27) | ✅ |
| Longevity: Pindayu + Nisargayu + Amsayu | ✅ |
| Balarishta detection | ✅ |
| Shadbala (6-fold strength) | ✅ |
| Ashtakavarga (SAV + R23 rule) | ✅ |
| Argala / Virodhargala | ✅ |
| Graha Yuddha (planetary war, celestial latitude winner) | ✅ |
| All 12 Arudha Padas | ✅ |
| Vimshopaka Bala (16 vargas, max 20 pts) | ✅ |
| D60 Shastiamsha (60 named divisions) | ✅ |
| Rasi Drishti (12×12 sign aspect matrix) | ✅ |
| Bhavat Bhavam | ✅ |
| Vimshottari + Narayana + Yogini + Chara Dasha | ✅ |
| Narayana Dasha Argala activation modifier (PVRNR Ch.5) | ✅ |
| Gochara + Sade Sati | ✅ |
| Varshaphala (Tajika) | ✅ |

### Yoga Library (200+)
| Category | Status |
|----------|--------|
| Pancha Mahapurusha (5 yogas) | ✅ |
| Raja Yogas — 8 Kendra×Trikona pairs | ✅ |
| Dhana Yogas — 5 pairs | ✅ |
| Viparita Raja (Harsha/Sarala/Vimala/Dainya) | ✅ |
| Neecha Bhanga — all 7 planets, 3 conditions | ✅ |
| Nabhasa (Rajju/Musala/Nala/Mala/Sarpa + Sankhya) | ✅ |
| Chandra yogas (Sunapha/Anapha/Durudhura/Kemadruma/Adhi) | ✅ |
| Surya yogas (Vesi/Vasi/Ubhayachari) | ✅ |
| Graha yogas (Budhaditya/Saraswati/Gaja Kesari/Chandra-Mangal/Kahala/Parvata) | ✅ |
| Dhana extended (Lakshmi/Duryoga/Daridra/Mahabhagya) | ✅ |

### KP (Krishnamurti Paddhati)
| Feature | Status |
|---------|--------|
| KP Significators | ✅ |
| Sub-lord chain (sign→nak→sub→sub-sub) | ✅ |
| Ruling Planets method | ✅ |
| Event promise evaluation | ✅ |
| KP cusps (Whole Sign approximation; Placidus via REF_Config) | ✅ |

### Jaimini
| Feature | Status |
|---------|--------|
| Chara Dasha | ✅ |
| Karakamsha scoring axis | ✅ |
| Jaimini yogas (AK kendra, AK+AmK, Gyana, Pada quality) | ✅ |
| Jaimini longevity (Brahma/Maheshvara/Rudra) | ✅ |
| Pada relationship scoring | ✅ |
| All 12 Arudha Padas | ✅ |

### Synthesis + Validation
| Feature | Status |
|---------|--------|
| 7-layer Life Pressure Index | ✅ |
| Varga agreement confidence flag (★★/★/○) | ✅ |
| 30-pair Rule Interaction Engine | ✅ |
| 5 special lagnas (Hora/Ghati/Sree/Indu/Pranapada) | ✅ |
| Monte Carlo birth-time sensitivity | ✅ |
| Narrative report generator | ✅ |
| Scenario / counterfactual explorer | ✅ |
| Empirical event log + per-rule accuracy metrics | ✅ |
| Kundali Milan (36-point compatibility) | ✅ |

---

## API Reference

```
POST /charts                         compute + store chart
GET  /charts                         list recent charts
GET  /charts/{id}/scores             full 23-rule breakdown by school
POST /auth/register                  register user
POST /auth/login                     get JWT tokens
GET  /user/school                    get scoring school
PUT  /user/school                    set school (Parashari/KP/Jaimini)
POST /empirica/events                record birth event
GET  /empirica/events/{chart_id}     list events for chart
GET  /empirica/accuracy              per-rule accuracy metrics + lift ratios
```

---

## Session History

| Phase | Sessions | Key deliverables |
|-------|----------|-----------------|
| 1 — Pilot | 1–10 | Ephemeris, calc modules, D1 scoring, FastAPI, SQLite, Streamlit, Docker |
| 2 — Features | 11–19 | Pushkara, Kundali Milan, PDF, Jaimini, KP, Tajika, API v2, 12-tab UI |
| 3 — Production | 20–27 | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes, Next.js, School gates |
| 4 — Pressure Engine | 28–32 | Functional roles, Avastha, LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | Multi-lagna, 5-axis scoring, Rule interactions, 7-layer LPI, D60, Yogas, Scoring v3 |
| 6 — Classical Depth | 41–48 | Ishta/Kashta, Longevity, Yogini Dasha, Full KP, 200+ Yogas, Special Lagnas, Jaimini, Empirica |
| 7 — Workbook Completeness | 49–56 | 12-state Sayanadi, Panchadha Maitri, Lagnesh modifier, Dig Bala continuous, Graha Yogas, ND Argala, Config toggles, Varga agreement |

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri/Raman/KP/Fagan-Bradley) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL via PG_DSN) + Empirica event log |
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
