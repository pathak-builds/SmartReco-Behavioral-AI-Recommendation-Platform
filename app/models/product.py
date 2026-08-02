"""
Product model for SmartReco.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.behavior import BehaviorEvent
    from app.models.recommendation import Recommendation


class Product(Base):
    """Product/Course model."""

    __tablename__ = "products"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # ==========================================================
    # Product Information
    # ==========================================================
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    price: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    difficulty: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    rating: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )

    attributes: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    chroma_document_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
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
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="products",
    )

    behavior_events: Mapped[list["BehaviorEvent"]] = relationship(
        "BehaviorEvent",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    recommendations: Mapped[list["Recommendation"]] = relationship(
        "Recommendation",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"Product("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"price={self.price}"
            f")"
        )