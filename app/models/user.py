"""
User model for SmartReco.
"""

import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, Enum):
    """Supported application roles."""

    USER = "user"
    ADMIN = "admin"


class User(Base):
    """Application user."""

    __tablename__ = "users"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ==========================================================
    # User Information
    # ==========================================================
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            native_enum=False,
            validate_strings=True,
        ),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
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
    behavior_events = relationship(
        "BehaviorEvent",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"User("
            f"id='{self.id}', "
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"role='{self.role.value}'"
            f")"
        )