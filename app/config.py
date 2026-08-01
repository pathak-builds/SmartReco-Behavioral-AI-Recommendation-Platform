"""
Application configuration for SmartReco.

This module loads configuration from environment variables and the local
`.env` file using Pydantic Settings.

All application components should import the singleton `settings` instance
instead of instantiating `Settings` directly.
"""

from functools import lru_cache
from typing import Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str = "SmartReco"
    APP_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = (
        "Behavioral AI Recommendation Platform"
    )

    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # ==========================================================
    # Security
    # ==========================================================
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="Secret key used to sign JWT tokens.",
    )

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        gt=0,
        description="JWT access token lifetime in minutes.",
    )

    # ==========================================================
    # Database
    # ==========================================================
    DATABASE_URL: str = Field(
        default="sqlite:///./data/smartreco.db",
        description="SQLAlchemy database connection URL.",
    )

    # ==========================================================
    # Vector Database
    # ==========================================================
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ==========================================================
    # AI / Mesh API
    # ==========================================================
    MESH_API_URL: str = "https://api.meshapi.ai/v1"

    MESH_API_KEY: Optional[str] = None

    MODEL_NAME: str = "openai/gpt-4.1-mini"

    # ==========================================================
    # Logging
    # ==========================================================
    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    # ==========================================================
    # Scheduler (used in later phases)
    # ==========================================================
    ENABLE_SCHEDULER: bool = True

    # ==========================================================
    # Pydantic Settings Configuration
    # ==========================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Using lru_cache ensures the configuration is loaded only once
    during the application's lifetime.
    """
    return Settings()


# Singleton settings instance
settings = get_settings()