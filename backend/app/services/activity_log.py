from __future__ import annotations

from uuid import UUID

from sqlmodel import Session

from app.models.activity_events import ActivityEvent


def record_activity(
    session: Session,
    *,
    event_type: str,
    message: str,
    agent_id: UUID | None = None,
    task_id: UUID | None = None,
) -> ActivityEvent:
    event = ActivityEvent(
        event_type=event_type,
        message=message,
        agent_id=agent_id,
        task_id=task_id,
    )
    session.add(event)
    return event
