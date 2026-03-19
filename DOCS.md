# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19 | Sessions complete: 1–22 | Tests: 532/532

## Table of Contents

1. Project Overview
2. Repository Structure
3. Regression Fixture
4. Module Reference (4.1–4.33)
5. API Reference
6. Scoring Engine Deep Dive
7. Known Bugs & Status
8. Test Suite
9. Development Setup

---

## 1. Project Overview

Transforms a 178-sheet Excel Jyotish workbook into a deterministic, auditable web platform.

Core flow: `ephemeris → 19 calc modules → scoring → report → Celery workers → FastAPI → DB/Cache → Streamlit UI`

Auth flow (S22): `POST /auth/register → /auth/login → Bearer token → protected endpoints`

---

## 2. Repository Structure

```
LagnaMaster/
├── streamlit_app.py          Streamlit Cloud entry point [S21 fix]
├── PLAN.md / DOCS.md / README.md
├── requirements.txt          +pyjwt>=2.8.0 +bcrypt>=4.1.0 [S22]
├── alembic.ini / migrations/ [S20]
├── docs/SESSION_LOG.md / MEMORY.md
├── src/
│   ├── __init__.py
│   ├── ephemeris.py          S1
│   ├── scoring.py            S3
│   ├── db.py                 S3
│   ├── db_pg.py              S20
│   ├── cache.py              S20
│   ├── report.py             S13
│   ├── worker.py             S21
│   ├── auth.py               S22  ← NEW
│   ├── calculations/
│   │   ├── __init__.py
│   │   ├── dignity.py        S2
│   │   ├── nakshatra.py      S2
│   │   ├── friendship.py     S2
│   │   ├── house_lord.py     S2
│   │   ├── chara_karak.py    S2
│   │   ├── narayana_dasa.py  S2
│   │   ├── shadbala.py       S2
│   │   ├── vimshottari_dasa.py S6
│   │   ├── yogas.py          S7
│   │   ├── ashtakavarga.py   S8
│   │   ├── gochara.py        S9
│   │   ├── panchanga.py      S10
│   │   ├── pushkara_navamsha.py S11
│   │   ├── kundali_milan.py  S12
│   │   ├── jaimini_chara_dasha.py S14
│   │   ├── kp_significators.py S15
│   │   ├── tajika.py         S16
│   │   └── compatibility_score.py S17
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app.py            S4,6–21
│   │   └── chart_visual.py   S6,10
│   └── api/
│       ├── __init__.py
│       ├── main.py           S3
│       ├── main_v2.py        S20
│       ├── auth_router.py    S22  ← NEW
│       └── models.py         S3,18
└── tests/
    ├── test_ephemeris.py     14  S1
    ├── test_calculations.py  36  S2
    ├── test_scoring.py       20  S3
    ├── test_integration.py   17  S5
    ├── test_vimshottari.py   20  S6
    ├── test_yogas.py         14  S7
    ├── test_ashtakavarga.py  26  S8
    ├── test_gochara.py       29  S9
    ├── test_panchanga.py     40  S10
    ├── test_pushkara.py      30  S11
    ├── test_kundali_milan.py 25  S12
    ├── test_report.py        15  S13
    ├── test_jaimini.py       20  S14
    ├── test_kp.py            22  S15
    ├── test_tajika.py        18  S16
    ├── test_compatibility.py 20  S17
    ├── test_api_v2.py        15  S18
    ├── test_ui_tabs.py       20  S19
    ├── test_session20.py     35  S20
    ├── test_session21.py     25  S21
    └── test_session22.py     25  S22
                             ────
                              532 total
```

---

## 3. Regression Fixture

```python
INDIA_1947 = {"year":1947,"month":8,"day":15,"hour":0.0,
              "lat":28.6139,"lon":77.2090,"tz_offset":5.5,"ayanamsha":"lahiri"}
# Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
```

---

## 4. Module Reference

*Sections 4.1–4.32 unchanged (ephemeris → worker, app). New:*

### 4.33 `src/auth.py` + `src/api/auth_router.py` *(Session 22)*

**Purpose**: Multi-user authentication with bcrypt passwords and JWT tokens.

**`src/auth.py` public API**:
```python
init_user_db(path=_SENTINEL)                          → None
register_user(username, email, password, path)        → UserRecord
authenticate_user(username, password, path)           → UserRecord | None
create_token_pair(user_id)                            → TokenPair
verify_access_token(token)                            → int  (user_id)
verify_refresh_token(token)                           → int  (user_id)
get_user_by_id(user_id, path)                         → UserRecord | None
deactivate_user(user_id, path)                        → None
```

**Data classes**:
```python
@dataclass class UserRecord:
    id: int; username: str; email: str; created_at: str; is_active: bool

@dataclass class TokenPair:
    access_token: str; refresh_token: str; token_type: str = "bearer"
    access_expires_in: int   # seconds (default 15×60 = 900)
    refresh_expires_in: int  # seconds (default 7×86400 = 604800)
```

**Token security**:
- Access token: HS256 JWT, 15 minutes TTL (configurable via `ACCESS_TTL_MIN`)
- Refresh token: HS256 JWT, 7 days TTL (configurable via `REFRESH_TTL_DAY`)
- Tokens are typed (`"kind": "access"` / `"kind": "refresh"`) — cross-use raises `ValueError`
- bcrypt rounds=12; SHA-256 HMAC fallback when bcrypt unavailable (tests)

**User DB**:
- SQLite at `data/users.db` (separate from `data/charts.db`)
- Mirrors `_SENTINEL` pattern from `src/db.py` for test isolation
- `UNIQUE COLLATE NOCASE` on both `username` and `email`
- Soft-delete via `is_active=0`

**FastAPI router** (`src/api/auth_router.py`):

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | None | Create account → 201 UserOut |
| POST | `/auth/login` | None | Credentials → TokenOut |
| POST | `/auth/refresh` | None | Refresh token → new TokenOut |
| GET | `/auth/me` | Bearer | Current user profile |
| POST | `/auth/logout` | None | 204 (client deletes tokens) |

**`get_current_user` dependency** (use to protect any endpoint):
```python
from src.api.auth_router import get_current_user

@app.get("/charts")
def list_charts(user = Depends(get_current_user)):
    ...  # user.id, user.username available
```

**Environment variables**:

| Variable | Default | Purpose |
|----------|---------|---------|
| `JWT_SECRET` | `dev-secret-change-in-production` | HMAC signing key |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TTL_MIN` | `15` | Access token TTL minutes |
| `REFRESH_TTL_DAY` | `7` | Refresh token TTL days |

---

## 5. API Reference

All existing endpoints unchanged. New auth prefix:

```
POST /auth/register    → 201 UserOut
POST /auth/login       → 200 TokenOut
POST /auth/refresh     → 200 TokenOut
GET  /auth/me          → 200 UserOut  (requires Bearer)
POST /auth/logout      → 204
```

---

## 7. Known Bugs & Status

All 6 audit bugs resolved. No open bugs.

---

## 8. Test Suite

**532 tests, all passing** (Session 22):

```
test_session22.py    25   S22
  TestRegistration   (6): register, duplicate username/email, short pw, email lowercase, distinct ids
  TestAuthentication (5): correct creds, wrong pw, unknown user, case-insensitive, deactivated
  TestTokens         (6): pair, access decode, refresh decode, cross-token rejection, tamper, TTL order
  TestAuthRouter     (8): 201 register, 409 conflict, login tokens, 401 wrong pw, me profile,
                          me no token, refresh, logout 204
```

---

## 9. Development Setup

```bash
pip install -r requirements.txt          # now includes pyjwt, bcrypt

# Set production secrets
export JWT_SECRET=your-secret-key-here
export JWT_ALGORITHM=HS256

PYTHONPATH=. pytest tests/ -v            # 532 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
```
