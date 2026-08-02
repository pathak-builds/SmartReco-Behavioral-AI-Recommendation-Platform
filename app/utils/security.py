"""
Security utilities for SmartReco.

Provides:
- Password hashing
- Password verification
- JWT access token creation
- JWT token validation
- SHA-256 hashing utility (used later for refresh tokens)
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# ==========================================================
# Password Hashing Configuration
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ==========================================================
# JWT Constants
# ==========================================================

ACCESS_TOKEN_TYPE = "access"

# ==========================================================
# Password Utilities
# ==========================================================


def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT Utilities
# ==========================================================


def create_access_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "type": ACCESS_TOKEN_TYPE,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Raises:
        JWTError
            If the token is invalid or expired.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )


def validate_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Validate an access token.
    """

    payload = decode_token(token)

    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise JWTError("Invalid token type.")

    if "sub" not in payload:
        raise JWTError("Token subject missing.")

    return payload


# ==========================================================
# SHA-256 Token Hashing
# (Used later for refresh tokens)
# ==========================================================


def hash_token(token: str) -> str:
    """
    Return a deterministic SHA-256 hash of a token.

    This is used for storing refresh tokens securely
    in the database without saving the raw token.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()