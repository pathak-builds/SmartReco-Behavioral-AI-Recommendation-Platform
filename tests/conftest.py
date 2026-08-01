"""
Pytest configuration and shared fixtures for SmartReco.

This module provides reusable fixtures for all test modules.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


@pytest.fixture(scope="session")
def app_settings():
    """
    Return the application settings.

    Available to all tests.
    """
    return settings


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Create a FastAPI TestClient.

    A new client is created for each test function to ensure isolation.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def test_data_dir():
    """
    Directory for temporary test data.

    Future phases will use this for:
    - SQLite test database
    - ChromaDB test collections
    - Temporary uploaded files
    """
    return "tests/data"