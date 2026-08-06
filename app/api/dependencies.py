"""
Authentication dependencies for SmartReco.

Provides reusable FastAPI dependencies for:

- OAuth2 bearer authentication
- Current authenticated user
- Current administrator
"""

from __future__ import annotations

from fastapi import (
    Depends,
    HTTPException,
    status,
    Cookie,
)


from fastapi.security import (
    OAuth2PasswordBearer,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
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
    auto_error=False,
)

# ==========================================================
# Optional Bearer Authentication
# ==========================================================

optional_bearer = HTTPBearer(
    auto_error=False,
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
    token: str | None = Depends(oauth2_scheme),
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate the JWT access token and return the authenticated user.
    """
    if token is None:
        token = access_token

    if token is None:
        raise credentials_exception
    
    
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
# Optional Current User
# ==========================================================

def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        optional_bearer
    ),
    db: Session = Depends(get_db),
) -> User | None:
    """
    Return the authenticated user if a valid
    Bearer token is supplied.

    Otherwise return None.

    This allows anonymous visitors to use
    public pages while still recording
    behavioral events.
    """

    if credentials is None:
        return None

    token = credentials.credentials

    try:

        payload = validate_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            return None

    except JWTError:
        return None

    auth_service = AuthService(db)

    user = auth_service.get_user_by_id(user_id)

    if user is None:
        return None

    if not user.is_active:
        return None

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