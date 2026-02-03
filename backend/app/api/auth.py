from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import AuthContext, get_auth_context
from app.schemas.users import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/bootstrap", response_model=UserRead)
async def bootstrap_user(auth: AuthContext = Depends(get_auth_context)) -> UserRead:
    if auth.actor_type != "user" or auth.user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return UserRead.model_validate(auth.user)
