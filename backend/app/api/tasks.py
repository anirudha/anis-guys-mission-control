from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_board_or_404, get_task_or_404, require_admin_auth
from app.core.auth import AuthContext
from app.db.session import get_session
from app.models.boards import Board
from app.models.tasks import Task
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from app.services.activity_log import record_activity

router = APIRouter(prefix="/boards/{board_id}/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    board: Board = Depends(get_board_or_404),
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> list[Task]:
    return list(session.exec(select(Task).where(Task.board_id == board.id)))


@router.post("", response_model=TaskRead)
def create_task(
    payload: TaskCreate,
    board: Board = Depends(get_board_or_404),
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> Task:
    task = Task.model_validate(payload)
    task.board_id = board.id
    if task.created_by_user_id is None and auth.user is not None:
        task.created_by_user_id = auth.user.id
    session.add(task)
    session.commit()
    session.refresh(task)

    record_activity(
        session,
        event_type="task.created",
        task_id=task.id,
        message=f"Task created: {task.title}.",
    )
    session.commit()
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    payload: TaskUpdate,
    task: Task = Depends(get_task_or_404),
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> Task:
    previous_status = task.status
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    if "status" in updates and task.status != previous_status:
        event_type = "task.status_changed"
        message = f"Task moved to {task.status}: {task.title}."
    else:
        event_type = "task.updated"
        message = f"Task updated: {task.title}."
    record_activity(session, event_type=event_type, task_id=task.id, message=message)
    session.commit()
    return task


@router.delete("/{task_id}")
def delete_task(
    session: Session = Depends(get_session),
    task: Task = Depends(get_task_or_404),
    auth: AuthContext = Depends(require_admin_auth),
) -> dict[str, bool]:
    session.delete(task)
    session.commit()
    return {"ok": True}
