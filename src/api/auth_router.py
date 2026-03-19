"""src/api/auth_router.py - LagnaMaster Session 22 - FastAPI auth router."""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, field_validator
import src.auth as auth_lib

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer = HTTPBearer(auto_error=False)

class RegisterRequest(BaseModel):
    username: str; email: str; password: str
    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        v = v.strip()
        if len(v) < 3: raise ValueError("Username must be at least 3 characters")
        if len(v) > 30: raise ValueError("Username must be at most 30 characters")
        return v
    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 8: raise ValueError("Password must be at least 8 characters")
        return v

class LoginRequest(BaseModel):
    username: str; password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserOut(BaseModel):
    id: int; username: str; email: str; created_at: str; is_active: bool

class TokenOut(BaseModel):
    access_token: str; refresh_token: str; token_type: str
    access_expires_in: int; refresh_expires_in: int

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(_bearer)) -> auth_lib.UserRecord:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        user_id = auth_lib.verify_access_token(credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e),
                            headers={"WWW-Authenticate": "Bearer"})
    user = auth_lib.get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or deactivated")
    return user

@router.post("/register", response_model=UserOut, status_code=201)
def register(req: RegisterRequest):
    try:
        auth_lib.init_user_db()
        user = auth_lib.register_user(req.username, req.email, req.password)
        return UserOut(id=user.id, username=user.username, email=user.email,
                       created_at=user.created_at, is_active=user.is_active)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/login", response_model=TokenOut)
def login(req: LoginRequest):
    auth_lib.init_user_db()
    user = auth_lib.authenticate_user(req.username, req.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    pair = auth_lib.create_token_pair(user.id)
    return TokenOut(access_token=pair.access_token, refresh_token=pair.refresh_token,
                    token_type=pair.token_type, access_expires_in=pair.access_expires_in,
                    refresh_expires_in=pair.refresh_expires_in)

@router.post("/refresh", response_model=TokenOut)
def refresh(req: RefreshRequest):
    try:
        user_id = auth_lib.verify_refresh_token(req.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    user = auth_lib.get_user_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or deactivated")
    pair = auth_lib.create_token_pair(user_id)
    return TokenOut(access_token=pair.access_token, refresh_token=pair.refresh_token,
                    token_type=pair.token_type, access_expires_in=pair.access_expires_in,
                    refresh_expires_in=pair.refresh_expires_in)

@router.get("/me", response_model=UserOut)
def me(user: auth_lib.UserRecord = Depends(get_current_user)):
    return UserOut(id=user.id, username=user.username, email=user.email,
                   created_at=user.created_at, is_active=user.is_active)

@router.post("/logout", status_code=204)
def logout():
    return None
