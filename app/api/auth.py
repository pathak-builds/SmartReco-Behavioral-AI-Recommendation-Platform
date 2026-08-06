"""
Authentication API routes for SmartReco.

Provides:

- User Registration
- User Login (OAuth2 Password Flow)
- Current User
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import Form
from fastapi.responses import RedirectResponse




from app.api.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    MessageResponse,
    TokenResponse,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent.parent / "templates"
    )
)

# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """

    auth_service = AuthService(db)

    try:
        user = auth_service.register_user(user_data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return user


# ==========================================================
# Login (OAuth2 Password Flow)
# ==========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return an access token.
    """

    auth_service = AuthService(db)

    access_token = auth_service.login_user(
        username=form_data.username,
        password=form_data.password,
    )

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_authenticated_user(
    current_user: User = Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """

    return current_user


@router.get("/login-page")
def login_page(
    request: Request,
):
    """
    Render browser login page.
    """

    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "title": "Login",
        },
    )



@router.post("/login-page")
def login_page_submit(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Authenticate browser user.
    """

    auth_service = AuthService(db)

    access_token = auth_service.login_user(
        username=username,
        password=password,
    )

    if access_token is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    response = RedirectResponse(
        url="/",
        status_code=303,
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return response
# ==========================================================
# Health Check
# ==========================================================

@router.get(
    "/status",
    response_model=MessageResponse,
)
def auth_status():
    """
    Authentication service status.
    """

    return MessageResponse(
        message="Authentication service is running."
    )