"""
Authentication service for SmartReco.

Handles:

- User registration
- User authentication
- JWT access token generation
- Current user lookup
"""

from __future__ import annotations

import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.auth import UserRegister
from app.utils.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


class AuthService:
    """
    Authentication business logic.
    """

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Register User
    # ==========================================================

    def register_user(
        self,
        data: UserRegister,
    ) -> User:
        """
        Register a new user.

        Raises:
            ValueError:
                If username or email already exists.
        """

        existing_user = (
            self.db.query(User)
            .filter(
                or_(
                    User.username == data.username,
                    User.email == data.email,
                )
            )
            .first()
        )

        if existing_user:
            raise ValueError(
                "Username or email already exists."
            )

        user = User(
            id=str(uuid.uuid4()),
            username=data.username.strip(),
            email=data.email.lower(),
            hashed_password=get_password_hash(data.password),
            role=UserRole.USER,
            is_active=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # ==========================================================
    # Authenticate User
    # ==========================================================

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> User | None:
        """
        Authenticate a user using username and password.
        """

        user = (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

        if user is None:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    # ==========================================================
    # Login
    # ==========================================================

    def login_user(
        self,
        username: str,
        password: str,
    ) -> str | None:
        """
        Authenticate a user and return an access token.
        """

        user = self.authenticate_user(
            username=username,
            password=password,
        )

        if user is None:
            return None

        access_token = create_access_token(
            subject=user.id,
            additional_claims={
                "username": user.username,
                "role": user.role.value,
            },
        )

        return access_token

    # ==========================================================
    # Get User
    # ==========================================================

    def get_user_by_id(
        self,
        user_id: str,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # ==========================================================
    # Get User By Username
    # ==========================================================

    def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.
        """

        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )