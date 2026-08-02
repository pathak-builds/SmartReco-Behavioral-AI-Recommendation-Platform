"""
Behavior event model for SmartReco.

Stores all meaningful user interactions that drive the recommendation engine.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    JSON,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class EventType(str, Enum):
    """Supported user behavior events."""

    PRODUCT_VIEW = "product_view"
    SEARCH = "search"
    CLICK = "click"
    SCROLL = "scroll"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"


class BehaviorEvent(Base):
    """Represents a tracked user behavior event."""

    __tablename__ = "behavior_events"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================
    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )

    product_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("products.id"),
        nullable=True,
        index=True,
    )

    # ==========================================================
    # Session Information
    # ==========================================================
    session_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Event Details
    # ==========================================================
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(
            EventType,
            native_enum=False,
            validate_strings=True,
        ),
        nullable=False,
    )

    search_query: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    page_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    time_spent_seconds: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    event_metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    # ==========================================================
    # Timestamps
    # ==========================================================
    event_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================
    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="behavior_events",
    )

    product: Mapped[Optional["Product"]] = relationship(
        "Product",
        back_populates="behavior_events",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"BehaviorEvent("
            f"id='{self.id}', "
            f"event_type='{self.event_type.value}', "
            f"user_id='{self.user_id}', "
            f"product_id='{self.product_id}'"
            f")"
        )