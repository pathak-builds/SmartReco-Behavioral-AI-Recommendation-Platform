"""
Authentication dependencies for SmartReco.

Provides reusable FastAPI dependencies for:

- OAuth2 bearer authentication
- Current authenticated user
- Current administrator
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.utils.security import validate_access_token


# ==========================================================
# OAuth2 Configuration
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


# ==========================================================
# Authentication Exception
# ==========================================================

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate the JWT access token and return the authenticated user.
    """

    try:
        payload = validate_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    auth_service = AuthService(db)

    user = auth_service.get_user_by_id(user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user


# ==========================================================
# Current Active Admin
# ==========================================================

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow access only to administrator users.
    """

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user