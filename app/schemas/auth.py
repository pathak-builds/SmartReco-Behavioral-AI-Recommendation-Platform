"""
Authentication schemas for SmartReco.

Contains request and response models for:

- User registration
- User login
- JWT authentication
- Current user information
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# ==========================================================
# User Role
# ==========================================================

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# ==========================================================
# Register Request
# ==========================================================

class UserRegister(BaseModel):
    """Schema used to register a new user."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["johnsmith"],
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["Password123"],
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if " " in value:
            raise ValueError("Username cannot contain spaces.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not any(c.isdigit() for c in value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        return value


# ==========================================================
# Login Request
# ==========================================================

class UserLogin(BaseModel):
    """Schema used during login."""

    username: str

    password: str


# ==========================================================
# JWT Token Response
# ==========================================================

class TokenResponse(BaseModel):
    """Returned after successful authentication."""

    access_token: str

    token_type: str = "bearer"


# ==========================================================
# Current User Response
# ==========================================================

class UserResponse(BaseModel):
    """Authenticated user."""

    model_config = ConfigDict(from_attributes=True)

    id: str

    username: str

    email: EmailStr

    role: UserRole

    is_active: bool

    created_at: datetime


# ==========================================================
# Authentication Message
# ==========================================================

class MessageResponse(BaseModel):
    """Simple success/error response."""

    message: str