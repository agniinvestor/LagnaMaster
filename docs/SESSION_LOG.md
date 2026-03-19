# LagnaMaster — Session Log

> Last updated: 2026-03-19 | Sessions complete: 1–22

## Sessions 1–21
See previous entries. Summary: 507 tests across pilot (S1–10), feature expansion (S11–19), and production hardening start (S20–21).

## Session 22 — Multi-user JWT Authentication
**Tests**: 25/25 | **Cumulative**: 532/532

### Deliverables

**`src/auth.py`**
- SQLite user store at `data/users.db` (_SENTINEL pattern for test isolation)
- `register_user`: bcrypt(rounds=12) password hashing, UNIQUE COLLATE NOCASE on username+email, SHA-256 HMAC fallback when bcrypt unavailable
- `authenticate_user`: returns UserRecord or None (no timing leak via constant-time compare)
- `create_token_pair`: HS256 JWT — access (15min) + refresh (7d), typed ("kind" claim)
- `verify_access_token` / `verify_refresh_token`: cross-kind rejection, expiry check
- `deactivate_user`: soft-delete (is_active=0)

**`src/api/auth_router.py`**
- `POST /auth/register` → 201 UserOut (409 on duplicate)
- `POST /auth/login` → 200 TokenOut (401 on bad credentials)
- `POST /auth/refresh` → 200 new TokenOut (401 on invalid/expired refresh)
- `GET /auth/me` → 200 UserOut (401 without valid Bearer)
- `POST /auth/logout` → 204 (stateless; client deletes tokens)
- `get_current_user` dependency exported for protecting other routers

**`requirements.txt`** additions: `pyjwt>=2.8.0`, `bcrypt>=4.1.0`

### Test coverage (25 tests)
- TestRegistration (6): returns user, duplicate username/email errors, short password, email lowercase, distinct IDs
- TestAuthentication (5): correct creds, wrong password, unknown user, case-insensitive lookup, deactivated user
- TestTokens (6): pair issued, access/refresh decode correctly, cross-kind rejected, tampering raises, access TTL < refresh TTL
- TestAuthRouter (8): register 201, conflict 409, login tokens, wrong pw 401, /me with token, /me without token 401, refresh, logout 204

### New environment variables
| Variable | Default | Purpose |
|----------|---------|---------|
| JWT_SECRET | dev-secret-change-in-production | **Change in production** |
| JWT_ALGORITHM | HS256 | Signing algorithm |
| ACCESS_TTL_MIN | 15 | Access token lifetime |
| REFRESH_TTL_DAY | 7 | Refresh token lifetime |

### Session 23 plan
GitHub Actions CI/CD: `.github/workflows/ci.yml` running pytest on push, Docker image build + push to GHCR, automatic Streamlit Cloud reboot on main merge.
