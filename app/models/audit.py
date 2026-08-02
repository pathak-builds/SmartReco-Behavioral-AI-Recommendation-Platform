"""
Audit log model for SmartReco.

Stores important user and system actions for monitoring,
security, debugging, and administration.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from __future__ import annotations

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AuditLog(Base):
    """Audit log entry."""

    __tablename__ = "audit_logs"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================================
    # Relationships
    # ==========================================================
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    # ==========================================================
    # Audit Information
    # ==========================================================
    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resource: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    resource_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True,
    )

    endpoint: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    details: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    # ==========================================================
    # Timestamp
    # ==========================================================
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================
    # user: Mapped[Optional["User"]] = relationship(
    #     "User",
    #     back_populates="audit_logs",
    # )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"AuditLog("
            f"id={self.id}, "
            f"action='{self.action}', "
            f"user_id='{self.user_id}'"
            f")"
        )