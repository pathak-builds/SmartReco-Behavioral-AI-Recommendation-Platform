"""
Refresh Token model for SmartReco.

Stores hashed refresh tokens for secure JWT authentication.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(Base):
    """Refresh token stored in the database."""

    __tablename__ = "refresh_tokens"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ==========================================================
    # Foreign Key
    # ==========================================================
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Token Information
    # ==========================================================
    token_hash: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ==========================================================
    # Audit Fields
    # ==========================================================
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"RefreshToken("
            f"id='{self.id}', "
            f"user_id='{self.user_id}', "
            f"revoked={self.revoked}"
            f")"
        )