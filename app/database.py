"""
Database configuration and session management for SmartReco.

This module is responsible for:
- Creating the SQLAlchemy engine
- Managing database sessions
- Providing the declarative Base class
- Exposing the FastAPI database dependency
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


# ==========================================================
# Database Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    pool_pre_ping=True,                         # Checks stale connections
    echo=settings.DEBUG,                        # Show SQL queries in DEBUG mode
)


# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ==========================================================
# Base ORM Model
# ==========================================================

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass


# ==========================================================
# Database Dependency
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    The session is automatically closed after the request
    finishes.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================================
# Database Initialization
# ==========================================================

def create_database() -> None:
    """
    Create all database tables.

    This is mainly used during the early development phases.
    Later, Alembic migrations will manage the database schema.
    """

    Base.metadata.create_all(bind=engine)