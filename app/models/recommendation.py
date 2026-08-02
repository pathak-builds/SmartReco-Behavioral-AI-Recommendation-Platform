"""
Recommendation model for SmartReco.

Stores AI-generated recommendations along with the reasoning,
confidence score, and user feedback.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class FeedbackType(str, Enum):
    """User feedback on a recommendation."""

    LIKE = "like"
    DISLIKE = "dislike"
    NEUTRAL = "neutral"


class RecommendationStatus(str, Enum):
    """Current recommendation lifecycle state."""

    ACTIVE = "active"
    CLICKED = "clicked"
    DISMISSED = "dismissed"
    EXPIRED = "expired"


class Recommendation(Base):
    """AI-generated recommendation."""

    __tablename__ = "recommendations"

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
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    # ==========================================================
    # Recommendation Details
    # ==========================================================
    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    recommendation_context: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    generated_by: Mapped[str] = mapped_column(
        String(100),
        default="langgraph-agent",
        nullable=False,
    )

    status: Mapped[RecommendationStatus] = mapped_column(
        SQLEnum(
            RecommendationStatus,
            native_enum=False,
            validate_strings=True,
        ),
        default=RecommendationStatus.ACTIVE,
        nullable=False,
    )

    feedback: Mapped[FeedbackType] = mapped_column(
        SQLEnum(
            FeedbackType,
            native_enum=False,
            validate_strings=True,
        ),
        default=FeedbackType.NEUTRAL,
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

    # ==========================================================
    # Relationships
    # ==========================================================
    user: Mapped["User"] = relationship(
        "User",
        back_populates="recommendations",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="recommendations",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"Recommendation("
            f"id='{self.id}', "
            f"user_id='{self.user_id}', "
            f"product_id='{self.product_id}', "
            f"score={self.confidence_score:.2f}"
            f")"
        )