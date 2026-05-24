"""Pydantic models for the Reports app.

Conventions:
  * `Report` is the raw, internal model — includes fields like `internal_id` and
    `owner_email` that MUST NEVER be exposed to end users.
  * `ReportPublic` is the response model used in public API responses. It explicitly
    omits the internal fields.

The CSV export feature added during the workshop must also honor this distinction.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReportStatus = Literal["pending", "approved", "rejected", "archived"]


class Report(BaseModel):
    """Internal report model. Holds every field, including internal-only ones."""

    model_config = ConfigDict(frozen=True)

    id: int
    internal_id: str  # INTERNAL ONLY — must never be exposed
    title: str
    status: ReportStatus
    owner: str
    owner_email: str  # INTERNAL ONLY — must never be exposed
    amount: float
    created_at: datetime


class ReportPublic(BaseModel):
    """Public response shape. Omits internal-only fields by construction."""

    id: int
    title: str
    status: ReportStatus
    owner: str
    amount: float
    created_at: datetime

    @classmethod
    def from_internal(cls, r: Report) -> "ReportPublic":
        return cls(
            id=r.id,
            title=r.title,
            status=r.status,
            owner=r.owner,
            amount=r.amount,
            created_at=r.created_at,
        )


class ReportListResponse(BaseModel):
    """Paginated list response."""

    items: list[ReportPublic]
    total: int = Field(description="Total number of rows matching the filter")
    offset: int
    limit: int
