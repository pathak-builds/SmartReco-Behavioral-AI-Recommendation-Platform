"""
Product and Category schemas for SmartReco.

Contains request and response models for:

- Product creation
- Product update
- Product response
- Category response
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ==========================================================
# Product Create
# ==========================================================

class ProductCreate(BaseModel):
    """Schema for creating a product."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    price: float = Field(
        ...,
        gt=0,
    )

    difficulty: str | None = Field(
        default=None,
        max_length=50,
    )

    rating: float = Field(
        default=0.0,
        ge=0,
        le=5,
    )

    category_id: int

    image_url: str | None = Field(
        default=None,
        max_length=500,
    )

    attributes: dict[str, Any] | None = None

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if value and not value.startswith(("http://", "https://")):
            raise ValueError(
                "Image URL must start with http:// or https://"
            )
        return value


# ==========================================================
# Product Update
# ==========================================================

class ProductUpdate(BaseModel):
    """Schema for updating a product."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    price: float | None = Field(
        default=None,
        gt=0,
    )

    difficulty: str | None = Field(
        default=None,
        max_length=50,
    )

    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
    )

    category_id: int | None = None

    image_url: str | None = Field(
        default=None,
        max_length=500,
    )

    attributes: dict[str, Any] | None = None

    is_active: bool | None = None

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value: str | None) -> str | None:
        if value and not value.startswith(("http://", "https://")):
            raise ValueError(
                "Image URL must start with http:// or https://"
            )
        return value


# ==========================================================
# Product Response
# ==========================================================

class ProductResponse(BaseModel):
    """Product response."""

    model_config = ConfigDict(from_attributes=True)

    id: str

    name: str

    description: str | None

    price: float

    difficulty: str | None

    rating: float

    category_id: int | None

    category_name: str | None = None

    image_url: str | None

    attributes: dict[str, Any] | None

    chroma_document_id: str | None

    is_active: bool

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Category Response
# ==========================================================

class CategoryResponse(BaseModel):
    """Category response."""

    model_config = ConfigDict(from_attributes=True)

    id: int

    name: str

    description: str | None

    parent_id: int | None

    is_active: bool

    created_at: datetime

    updated_at: datetime


# ==========================================================
# Product List Response
# ==========================================================

class ProductListResponse(BaseModel):
    """List of products."""

    products: list[ProductResponse]

    total: int