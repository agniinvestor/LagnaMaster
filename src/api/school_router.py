"""
src/api/school_router.py — LagnaMaster Session 26
REST endpoints for reading and updating a user's calculation school preference.

Endpoints
---------
GET  /user/school           return current user's school preference
PUT  /user/school           update current user's school preference
GET  /schools               list all supported schools with enabled status
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import src.config as cfg
from src.api.auth_router import get_current_user
import src.auth as auth_lib

router = APIRouter(prefix="/user", tags=["school"])


class SchoolOut(BaseModel):
    school: str
    enabled: bool


class SchoolsOut(BaseModel):
    schools: list[SchoolOut]
    default: str


class SetSchoolRequest(BaseModel):
    school: str


@router.get("/school", response_model=SchoolOut)
def get_school(user: auth_lib.UserRecord = Depends(get_current_user)):
    """Return the authenticated user's current school preference."""
    school = cfg.get_user_school(user.id)
    return SchoolOut(school=school, enabled=cfg.is_school_enabled(school))


@router.put("/school", response_model=SchoolOut)
def set_school(
    req: SetSchoolRequest,
    user: auth_lib.UserRecord = Depends(get_current_user),
):
    """Update the authenticated user's school preference."""
    try:
        cfg.set_user_school(user.id, req.school)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return SchoolOut(school=req.school, enabled=cfg.is_school_enabled(req.school))


@router.get("/schools", response_model=SchoolsOut)
def list_schools():
    """List all supported schools with their enabled status (no auth required)."""
    return SchoolsOut(
        schools=[
            SchoolOut(school=s, enabled=cfg.is_school_enabled(s))
            for s in sorted(cfg.SUPPORTED_SCHOOLS)
        ],
        default=cfg.DEFAULT_SCHOOL,
    )
