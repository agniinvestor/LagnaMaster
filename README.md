# LagnaMaster

Vedic Jyotish computation engine + consumer guidance platform.

**963 tests | Sessions 1–100 complete | 100 modules | Engine v3.0.0**

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

# Compute Panchanga (5 limbs of the almanac)
p = compute_panchanga(sun_lon, moon_lon, datetime.now())
print(p.tithi_name, p.vara_name, p.nakshatra_name)
print(p.amrita_siddhi, p.sarvaartha_siddhi)

# Score a muhurta for a specific task
score = score_muhurta("marriage", p,
                       birth_nakshatra=7,     # native's Moon nakshatra
                       birth_moon_sign=3,      # Cancer
                       muhurta_lagna_sign=1)   # proposed Taurus lagna
print(score.quality)       # "Excellent"/"Good"/"Acceptable"/"Avoid"
print(score.total_score)   # 0–7
print(score.warnings)      # list of inauspicious factors

# Hora and Choghadiya
hora_lord, hora_num = compute_hora(datetime.now())
chog = compute_choghadiya(datetime.now())
print(chog["quality"])     # "Excellent"/"Good"/"Neutral"/"Unfavorable"
```

---

## Prashna (Horary)

```python
from src.calculations.prashna import analyze_prashna
from datetime import datetime

# Chart is computed for the query moment
prashna_chart = compute_chart(...)   # at time of question
result = analyze_prashna(prashna_chart, query_type="career",
                          query_dt=datetime.now())
print(result.verdict)      # "Yes — strongly indicated" / "Unlikely" etc.
print(result.confidence)   # "High"/"Moderate"/"Low"
print(result.reasoning)    # list of supporting factors
```

---

## All Supported Dashas

```python
from src.calculations.vimshottari_dasa   import compute_vimshottari_dasa   # 120yr, 9 planets
from src.calculations.narayana_dasha     import compute_narayana_dasha      # Rasi dasha
from src.calculations.yogini_dasha       import compute_yogini_dasha        # 36yr cycle
from src.calculations.chara_dasha        import compute_chara_dasha         # Jaimini
from src.calculations.kalachakra_dasha   import compute_kalachakra_dasha    # 100yr, Moon D9
from src.calculations.ashtottari_dasha   import compute_ashtottari_dasha    # 108yr, 8 planets
from src.calculations.shoola_dasha       import compute_shoola_dasha        # Ayur/longevity
from src.calculations.shoola_dasha       import compute_sudasa              # Material success
from src.calculations.tara_dasha         import compute_tara_dasha          # 9-category Nakshatra
```

---

## Upaya (Remedial Measures)

```python
from src.calculations.upaya import get_upaya, get_chart_upayas

# Auto-detect afflictions and get classical prescriptions
upayas = get_chart_upayas(chart)
for u in upayas:
    print(f"{u.planet} ({u.affliction_type}):")
    print(f"  Gemstone: {u.gemstone} in {u.gemstone_metal} on {u.gemstone_day}")
    print(f"  Deity: {u.primary_deity}")
    print(f"  Mantra: recite {u.mantra_count} times")
    print(f"  Charity: {u.charitable_act}")
    print(f"  {u.disclaimer}")   # always present

# Single planet
u = get_upaya("Saturn", "debilitated")
```

---

## Mundane Astrology

```python
from src.calculations.mundane import analyze_mundane_chart, compress_vimshottari
from datetime import date

# Nation/ingress/swearing-in chart
result = analyze_mundane_chart(chart, "nation", "India 1947",
                                date(1947, 8, 15), "New Delhi")
print(result.key_themes)    # top activated mundane houses
print(result.challenges)    # stressed mundane houses

# Compress Vimshottari to 1-year period for annual prediction
compressed = compress_vimshottari(chart, birth_date, period_years=1.0)
```

---

## Consumer Guidance API

```python
from src.guidance.guidance_api import get_guidance

r = get_guidance(chart, domain="career", depth="L1", dashas=dashas)
print(r.signal_display)   # ●●●○○
print(r.timing_label)     # "Mixed — lean in"
print(r.summary)          # Human-safe sentence, no raw scores
print(r.disclaimer)       # Scope disclaimer
```

---

## Session History

| Phase | Sessions | Status | Key deliverables |
|-------|----------|--------|-----------------|
| 1–3 | 1–27 | ✅ | Engine, scoring, FastAPI, Streamlit, Docker, JWT, K8s |
| 4–5 | 28–40 | ✅ | LPI, 5-axis scoring, rule interactions, Scoring v3 |
| 6 | 41–48 | ✅ | Ishta/Kashta, Longevity, Yogini, KP, 200+ Yogas, Empirica |
| 7 | 49–56 | ✅ | Sayanadi, Panchadha Maitri, Dig Bala, Config toggles |
| 8 | 57–63 | ✅ | Orb strength, Yoga fructification, Stronger-of-two, AV transit |
| 9 | 64–70 | ✅ | Dominance engine, Promise/Manifestation, Confidence model |
| 10–11 | 71–78 | ✅ | Language safety pipeline, GDPR/DPDP consent + erasure |
| 12–14 | 79–90 | ✅ | Bloomberg UI, feedback governance, educational layer |
| 15–18 | 91–100 | ✅ | **Muhurta, Prashna, Kalachakra, Ashtottari, Shoola, Tara, Upaya, Mundane** |

---

## Coverage Class

**Comprehensive Jyotish Platform** — covers:
- All major branches of natal analysis
- Muhurta (electional) — complete Panchanga + task scoring
- Prashna (horary) — query-moment chart analysis
- All standard dasha systems including Kalachakra and Ashtottari
- Upaya (remedial measures) as classical prescriptions
- Mundane astrology — nation/ingress/swearing-in charts
- Consumer safety pipeline with GDPR compliance

**Acknowledged limits** (not parameterisable):
- Full Prashna Marga horary corpus (separate discipline)
- Kala, gender, social role modifiers (Desha-Kala-Patra)
- Gestalt expert synthesis beyond named rules
- Ritual/spiritual efficacy of remedies

---

## Stack

| Layer | Technology |
|-------|-----------|
| Ephemeris | pyswisseph (Lahiri/Raman/KP/Fagan-Bradley) |
| Backend | FastAPI + Celery + Redis |
| Database | SQLite → PostgreSQL + consent/feedback tables |
| Consumer UI | Next.js 14 + TypeScript + Tailwind |
| Mobile | FastAPI /mobile router |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT | CI/CD | GitHub Actions |
| Privacy | GDPR Art.7+17 · DPDP · CCPA/CPRA |
