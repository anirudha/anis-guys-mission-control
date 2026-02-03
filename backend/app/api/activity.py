from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlmodel import Session, col, select

from app.api.deps import require_admin_auth
from app.core.auth import AuthContext
from app.db.session import get_session
from app.models.activity_events import ActivityEvent
from app.schemas.activity_events import ActivityEventRead

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("", response_model=list[ActivityEventRead])
def list_activity(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> list[ActivityEvent]:
    statement = (
        select(ActivityEvent)
        .order_by(desc(col(ActivityEvent.created_at)))
        .offset(offset)
        .limit(limit)
    )
    return list(session.exec(statement))
