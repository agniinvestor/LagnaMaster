"""src/api/auth_router.py — LagnaMaster Session 22 — FastAPI auth router."""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, field_validator
import src.auth as A

router = APIRouter(prefix="/auth", tags=["auth"])
_b = HTTPBearer(auto_error=False)


class RegReq(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def _u(cls, v):
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 30:
            raise ValueError("Username must be at most 30 characters")
        return v

    @field_validator("password")
    @classmethod
    def _p(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginReq(BaseModel):
    username: str
    password: str


class RefreshReq(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    is_active: bool


class TokOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_expires_in: int
    refresh_expires_in: int


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(_b)) -> A.UserRecord:
    if creds is None:
        raise HTTPException(
            401, "Not authenticated", headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        uid = A.verify_access_token(creds.credentials)
    except ValueError as e:
        raise HTTPException(401, str(e), headers={"WWW-Authenticate": "Bearer"})
    user = A.get_user_by_id(uid)
    if user is None or not user.is_active:
        raise HTTPException(401, "User not found or deactivated")
    return user


def _tout(pair):
    return TokOut(
        access_token=pair.access_token,
        refresh_token=pair.refresh_token,
        token_type=pair.token_type,
        access_expires_in=pair.access_expires_in,
        refresh_expires_in=pair.refresh_expires_in,
    )


def _uout(u):
    return UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        created_at=u.created_at,
        is_active=u.is_active,
    )


@router.post("/register", response_model=UserOut, status_code=201)
def register(req: RegReq):
    try:
        A.init_user_db()
        return _uout(A.register_user(req.username, req.email, req.password))
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.post("/login", response_model=TokOut)
def login(req: LoginReq):
    A.init_user_db()
    u = A.authenticate_user(req.username, req.password)
    if u is None:
        raise HTTPException(401, "Invalid username or password")
    return _tout(A.create_token_pair(u.id))


@router.post("/refresh", response_model=TokOut)
def refresh(req: RefreshReq):
    try:
        uid = A.verify_refresh_token(req.refresh_token)
    except ValueError as e:
        raise HTTPException(401, str(e))
    u = A.get_user_by_id(uid)
    if u is None or not u.is_active:
        raise HTTPException(401, "User not found or deactivated")
    return _tout(A.create_token_pair(uid))


@router.get("/me", response_model=UserOut)
def me(u: A.UserRecord = Depends(get_current_user)):
    return _uout(u)


@router.post("/logout", status_code=204)
def logout():
    return None
