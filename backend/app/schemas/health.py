"""Health and readiness probe response schemas."""

from __future__ import annotations

from pydantic import Field
from sqlmodel import SQLModel


class HealthStatusResponse(SQLModel):
    """Standard payload for service liveness/readiness checks."""

    ok: bool = Field(
        description="Indicates whether the probe check succeeded.",
        examples=[True],
    )
