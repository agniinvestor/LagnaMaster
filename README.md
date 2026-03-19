# LagnaMaster

Vedic Jyotish (Hindu astrology) analysis engine — web platform for deterministic, auditable birth chart scoring.

Transforms a 178-sheet Excel workbook (v5) into a multi-user web app with institutional-grade calculation accuracy.

## What it does

- Accepts birth date, time, and location
- Calculates Lagna (ascendant) and all 9 planet positions via pyswisseph DE441 ephemeris
- Runs 10 Jyotish calculation modules (Dignity, Shadbala, Narayana Dasha, Ashtakavarga, etc.)
- Scores 26 rules × 12 houses = 312 evaluations per chart
- Returns domain scores [-10, +10] for career, relationships, health, wealth, spirituality

## Stack

- **Ephemeris**: pyswisseph (Swiss Ephemeris DE441, ±0.004° accuracy)
- **Backend**: FastAPI + SQLite → PostgreSQL
- **UI**: Streamlit → Next.js
- **Deploy**: Docker Compose → K8s

## Status

- [ ] Session 1: pyswisseph wrapper + 1947 regression fixture
- [ ] Session 2: 10 Jyotish calculation modules
- [ ] Session 3: Scoring engine + FastAPI
- [ ] Session 4: Streamlit UI
- [ ] Session 5: SQLite persistence
- [ ] Session 6: Docker Compose

See [PLAN.md](PLAN.md) for full build plan.

## Regression Fixture

1947 India Independence Chart validates all modules:
- Birth: 1947-08-15 00:00 IST, New Delhi
- Lagna: 7.7286° Taurus | Sun: 27.989° Cancer | Ayanamsha: Lahiri
