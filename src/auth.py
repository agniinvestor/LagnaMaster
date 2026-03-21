"""src/auth.py — LagnaMaster Session 22 — multi-user JWT auth."""
from __future__ import annotations
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import bcrypt; _BC = True
except BaseException:
    _BC = False
try:
    import jwt as _jwt; _JW = True
except BaseException:
    _JW = False

_SEC = os.environ.get("JWT_SECRET", "dev-secret-change-in-production")
_ALG = os.environ.get("JWT_ALGORITHM", "HS256")
_ATT = int(os.environ.get("ACCESS_TTL_MIN", "15"))
_RTT = int(os.environ.get("REFRESH_TTL_DAY", "7"))
_SENTINEL = object()
USER_DB_PATH = str(Path(__file__).parent.parent / "data" / "users.db")

@dataclass
class UserRecord:
    id: int; username: str; email: str; created_at: str; is_active: bool

@dataclass
class TokenPair:
    access_token: str; refresh_token: str; token_type: str = "bearer"
    access_expires_in: int = _ATT * 60
    refresh_expires_in: int = _RTT * 86400

_DDL = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_un ON users(username COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_em ON users(email COLLATE NOCASE);
"""

def _p(path): return USER_DB_PATH if path is _SENTINEL else str(path)
def _cx(path):
    p = _p(path); Path(p).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(p); c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL"); return c

def init_user_db(path=_SENTINEL):
    with _cx(path) as c: c.executescript(_DDL)

def _hp(pw):
    if not _BC:
        import hashlib
        import hmac
        return "sha256:"+hmac.new(_SEC.encode(),pw.encode(),hashlib.sha256).hexdigest()
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=12)).decode()

def _vp(pw, h):
    if h.startswith("sha256:"):
        import hashlib
        import hmac
        e = hmac.new(_SEC.encode(),pw.encode(),hashlib.sha256).hexdigest()
        return hmac.compare_digest(e, h[7:])
    return _BC and bcrypt.checkpw(pw.encode(), h.encode())

def _mt(uid, kind, ttl):
    if not _JW: raise RuntimeError("pip install pyjwt")
    n = datetime.now(timezone.utc)
    return _jwt.encode({"sub":str(uid),"kind":kind,"iat":n,"exp":n+timedelta(seconds=ttl)},
                       _SEC, algorithm=_ALG)

def _dt(tok, kind):
    if not _JW: raise RuntimeError("pip install pyjwt")
    try: p = _jwt.decode(tok, _SEC, algorithms=[_ALG])
    except _jwt.ExpiredSignatureError: raise ValueError("Token has expired")
    except _jwt.InvalidTokenError as e: raise ValueError(f"Invalid token: {e}")
    if p.get("kind") != kind: raise ValueError(f"Wrong token kind: expected {kind}")
    return int(p["sub"])

def register_user(username, email, password, path=_SENTINEL):
    if len(password) < 8: raise ValueError("Password must be at least 8 characters")
    now = datetime.now(timezone.utc).isoformat()
    try:
        with _cx(path) as c:
            row = c.execute(
                "INSERT INTO users(username,email,password_hash,created_at) VALUES(?,?,?,?) RETURNING id",
                (username.strip(), email.strip().lower(), _hp(password), now)
            ).fetchone()
            return UserRecord(id=row["id"], username=username.strip(),
                              email=email.strip().lower(), created_at=now, is_active=True)
    except sqlite3.IntegrityError as e:
        m = str(e).lower()
        if "username" in m: raise ValueError(f"Username '{username}' is already taken")
        if "email" in m: raise ValueError(f"Email '{email}' is already registered")
        raise ValueError(str(e))

def authenticate_user(username, password, path=_SENTINEL) -> Optional[UserRecord]:
    with _cx(path) as c:
        row = c.execute("SELECT * FROM users WHERE username=? COLLATE NOCASE AND is_active=1",
                        (username.strip(),)).fetchone()
    if row is None or not _vp(password, row["password_hash"]): return None
    return UserRecord(id=row["id"], username=row["username"], email=row["email"],
                      created_at=row["created_at"], is_active=bool(row["is_active"]))

def create_token_pair(user_id: int) -> TokenPair:
    return TokenPair(access_token=_mt(user_id,"access",_ATT*60),
                     refresh_token=_mt(user_id,"refresh",_RTT*86400))

def verify_access_token(token: str) -> int: return _dt(token, "access")
def verify_refresh_token(token: str) -> int: return _dt(token, "refresh")

def get_user_by_id(user_id: int, path=_SENTINEL) -> Optional[UserRecord]:
    with _cx(path) as c:
        row = c.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if row is None: return None
    return UserRecord(id=row["id"], username=row["username"], email=row["email"],
                      created_at=row["created_at"], is_active=bool(row["is_active"]))

def deactivate_user(user_id: int, path=_SENTINEL):
    with _cx(path) as c: c.execute("UPDATE users SET is_active=0 WHERE id=?", (user_id,))


# ── Helpers for config.py (added by diagnose_and_fix.sh) ──────────────────────
def _db_path(path=_SENTINEL) -> str:
    """Return the resolved DB file path string."""
    return USER_DB_PATH if path is _SENTINEL else str(path)


def _connect(path=_SENTINEL):
    """Return a sqlite3 connection with row_factory set."""
    import sqlite3
    p = _db_path(path)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    return conn
