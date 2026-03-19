# LagnaMaster

Vedic Jyotish birth chart scoring platform — fully production-ready + Phase 4 Pressure Engine.

**![CI](https://github.com/agniinvestor/LagnaMaster/actions/workflows/ci.yml/badge.svg) 717 tests passing | Sessions 1–32 complete**

## Quick Start

```
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

## Sessions

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1–10 | Pilot — ephemeris → panchanga | 222 |
| 11–19 | Feature expansion | 225 |
| 20–27 | Production hardening (PG, Redis, Celery, JWT, K8s, Next.js, school gates, MC scaling) | 210 |
| 28 | Functional roles: per-lagna maleficence, badhaka, maraka | 9 |
| 29 | Avastha systems: Deeptadi, Baladi, Lajjitadi | 6 |
| 30 | Life Pressure Index engine: vuln × dasha × transit ÷ resilience | 9 |
| 31 | Argala/Virodhargala + Arudha Lagna | 5 |
| 32 | Graha Yuddha + Scoring Engine v2 (declarative + versioned) | 7 |

**Total: 717/717 tests passing**

## The Life Pressure Index

The central Phase 4 feature. Gives a date-indexed pressure score [0–10]:

```python
from src.calculations.pressure_engine import compute_pressure_timeline

points = compute_pressure_timeline(chart, dashas,
    from_date=date(2024,1,1), to_date=date(2027,12,31), step_months=3)

for p in points:
    print(f"{p.date}  {p.pressure_index:5.2f}  {p.label}")
    print(f"  Drivers: {p.key_drivers}")
    print(f"  Dasha: {p.dasha_note}")
```

See [PLAN.md](PLAN.md) and [DOCS.md](DOCS.md) for full reference.
