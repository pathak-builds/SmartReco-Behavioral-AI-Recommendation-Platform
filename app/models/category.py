"""
Category model for SmartReco.

Supports hierarchical product categories.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    """Product category."""

    __tablename__ = "categories"

    # ==========================================================
    # Primary Key
    # ==========================================================
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ==========================================================
    # Category Information
    # ==========================================================
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
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

    # Parent category
    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
    )

    # Child categories
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
    )

    # Products
    products = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    # ==========================================================
    # Representation
    # ==========================================================
    def __repr__(self) -> str:
        return (
            f"Category("
            f"id={self.id}, "
            f"name='{self.name}'"
            f")"
        )