"""src/auth.py - LagnaMaster Session 22 - Multi-user JWT auth."""
from __future__ import annotations
import os, sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import bcrypt; _BCRYPT = True
except ImportError:
    _BCRYPT = False

try:
    import jwt as pyjwt; _JWT = True
except ImportError:
    _JWT = False

_SECRET    = os.environ.get("JWT_SECRET", "dev-secret-change-in-production")
_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
_ACCESS_TTL  = int(os.environ.get("ACCESS_TTL_MIN",  "15"))
_REFRESH_TTL = int(os.environ.get("REFRESH_TTL_DAY",  "7"))

_SENTINEL = object()
USER_DB_PATH = str(Path(__file__).parent.parent / "data" / "users.db")

@dataclass
class UserRecord:
    id: int; username: str; email: str; created_at: str; is_active: bool

@dataclass
class TokenPair:
    access_token: str; refresh_token: str
    token_type: str = "bearer"
    access_expires_in: int = _ACCESS_TTL * 60
    refresh_expires_in: int = _REFRESH_TTL * 86400

_DDL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username COLLATE NOCASE);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email COLLATE NOCASE);
"""

def _db_path(path) -> str:
    return USER_DB_PATH if path is _SENTINEL else str(path)

def _connect(path):
    p = _db_path(path)
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_user_db(path=_SENTINEL) -> None:
    with _connect(path) as conn:
        conn.executescript(_DDL)

def _hash_password(plain: str) -> str:
    if not _BCRYPT:
        import hashlib, hmac
        return "sha256:" + hmac.new(_SECRET.encode(), plain.encode(), hashlib.sha256).hexdigest()
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()

def _verify_password(plain: str, hashed: str) -> bool:
    if hashed.startswith("sha256:"):
        import hashlib, hmac
        exp = hmac.new(_SECRET.encode(), plain.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(exp, hashed[7:])
    return _BCRYPT and bcrypt.checkpw(plain.encode(), hashed.encode())

def _make_token(user_id: int, kind: str, ttl: int) -> str:
    if not _JWT: raise RuntimeError("pip install pyjwt")
    now = datetime.now(timezone.utc)
    return pyjwt.encode({"sub": str(user_id), "kind": kind, "iat": now,
                          "exp": now + timedelta(seconds=ttl)}, _SECRET, algorithm=_ALGORITHM)

def _decode_token(token: str, kind: str) -> int:
    if not _JWT: raise RuntimeError("pip install pyjwt")
    try:
        p = pyjwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    except pyjwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except pyjwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")
    if p.get("kind") != kind:
        raise ValueError(f"Wrong token kind: expected {kind}")
    return int(p["sub"])

def register_user(username, email, password, path=_SENTINEL) -> UserRecord:
    if len(password) < 8: raise ValueError("Password must be at least 8 characters")
    hashed = _hash_password(password)
    now = datetime.now(timezone.utc).isoformat()
    try:
        with _connect(path) as conn:
            cur = conn.execute(
                "INSERT INTO users (username,email,password_hash,created_at) VALUES(?,?,?,?) RETURNING id",
                (username.strip(), email.strip().lower(), hashed, now))
            row = cur.fetchone()
            return UserRecord(id=row["id"], username=username.strip(),
                              email=email.strip().lower(), created_at=now, is_active=True)
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if "username" in msg: raise ValueError(f"Username '{username}' is already taken")
        if "email" in msg: raise ValueError(f"Email '{email}' is already registered")
        raise ValueError(str(e))

def authenticate_user(username, password, path=_SENTINEL) -> Optional[UserRecord]:
    with _connect(path) as conn:
        row = conn.execute("SELECT * FROM users WHERE username=? COLLATE NOCASE AND is_active=1",
                           (username.strip(),)).fetchone()
    if row is None or not _verify_password(password, row["password_hash"]):
        return None
    return UserRecord(id=row["id"], username=row["username"], email=row["email"],
                      created_at=row["created_at"], is_active=bool(row["is_active"]))

def create_token_pair(user_id: int) -> TokenPair:
    return TokenPair(
        access_token=_make_token(user_id, "access", _ACCESS_TTL * 60),
        refresh_token=_make_token(user_id, "refresh", _REFRESH_TTL * 86400))

def verify_access_token(token: str) -> int:
    return _decode_token(token, "access")

def verify_refresh_token(token: str) -> int:
    return _decode_token(token, "refresh")

def get_user_by_id(user_id: int, path=_SENTINEL) -> Optional[UserRecord]:
    with _connect(path) as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if row is None: return None
    return UserRecord(id=row["id"], username=row["username"], email=row["email"],
                      created_at=row["created_at"], is_active=bool(row["is_active"]))

def deactivate_user(user_id: int, path=_SENTINEL) -> None:
    with _connect(path) as conn:
        conn.execute("UPDATE users SET is_active=0 WHERE id=?", (user_id,))
