from __future__ import annotations

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.core.auth import AuthContext, get_auth_context
from app.db.session import get_session
from app.models.boards import Board
from app.models.tasks import Task
from app.services.admin_access import require_admin


def require_admin_auth(auth: AuthContext = Depends(get_auth_context)) -> AuthContext:
    require_admin(auth)
    return auth


def get_board_or_404(
    board_id: str,
    session: Session = Depends(get_session),
) -> Board:
    board = session.get(Board, board_id)
    if board is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return board


def get_task_or_404(
    task_id: str,
    board: Board = Depends(get_board_or_404),
    session: Session = Depends(get_session),
) -> Task:
    task = session.get(Task, task_id)
    if task is None or task.board_id != board.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return task
