from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.api.deps import get_board_or_404, require_admin_auth
from app.core.auth import AuthContext
from app.db.session import get_session
from app.models.boards import Board
from app.schemas.boards import BoardCreate, BoardRead, BoardUpdate

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("", response_model=list[BoardRead])
def list_boards(
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> list[Board]:
    return list(session.exec(select(Board)))


@router.post("", response_model=BoardRead)
def create_board(
    payload: BoardCreate,
    session: Session = Depends(get_session),
    auth: AuthContext = Depends(require_admin_auth),
) -> Board:
    board = Board.model_validate(payload)
    session.add(board)
    session.commit()
    session.refresh(board)
    return board


@router.get("/{board_id}", response_model=BoardRead)
def get_board(
    board: Board = Depends(get_board_or_404),
    auth: AuthContext = Depends(require_admin_auth),
) -> Board:
    return board


@router.patch("/{board_id}", response_model=BoardRead)
def update_board(
    payload: BoardUpdate,
    session: Session = Depends(get_session),
    board: Board = Depends(get_board_or_404),
    auth: AuthContext = Depends(require_admin_auth),
) -> Board:
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(board, key, value)
    session.add(board)
    session.commit()
    session.refresh(board)
    return board


@router.delete("/{board_id}")
def delete_board(
    session: Session = Depends(get_session),
    board: Board = Depends(get_board_or_404),
    auth: AuthContext = Depends(require_admin_auth),
) -> dict[str, bool]:
    session.delete(board)
    session.commit()
    return {"ok": True}
