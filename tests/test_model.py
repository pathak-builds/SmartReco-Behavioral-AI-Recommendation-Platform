"""
Basic model tests for SmartReco.
"""

from datetime import datetime, timezone
import uuid

import pytest

from app.database import Base, SessionLocal, engine
from app.models import (
    BehaviorEvent,
    Category,
    Product,
    Recommendation,
    User,
)
from app.models.behavior import EventType
from app.models.recommendation import (
    FeedbackType,
    RecommendationStatus,
)
from app.models.user import UserRole


# ==========================================================
# Test Database
# ==========================================================

@pytest.fixture(scope="function")
def db():
    """Create a clean database for every test."""

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# ==========================================================
# User
# ==========================================================

def test_create_user(db):

    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed-password",
        role=UserRole.USER,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"


# ==========================================================
# Category
# ==========================================================

def test_create_category(db):

    category = Category(
        name="Artificial Intelligence",
        description="AI Courses",
    )

    db.add(category)
    db.commit()

    assert db.query(Category).count() == 1


# ==========================================================
# Product
# ==========================================================

def test_create_product(db):

    category = Category(
        name="Python",
    )

    db.add(category)
    db.flush()

    product = Product(
        name="Python Bootcamp",
        description="Learn Python",
        price=99.0,
        difficulty="Beginner",
        rating=4.8,
        category_id=category.id,
    )

    db.add(product)
    db.commit()

    assert product.category.name == "Python"


# ==========================================================
# Behavior Event
# ==========================================================

def test_create_behavior_event(db):

    user = User(
        username="john",
        email="john@test.com",
        hashed_password="secret",
    )

    category = Category(name="AI")

    db.add_all([user, category])
    db.flush()

    product = Product(
        name="GenAI",
        price=100,
        category_id=category.id,
    )

    db.add(product)
    db.flush()

    event = BehaviorEvent(

        user_id=user.id,

        product_id=product.id,

        session_id="session-001",

        event_type=EventType.PRODUCT_VIEW,

        event_timestamp=datetime.now(timezone.utc),

        time_spent_seconds=15.6,

        event_metadata={
            "browser": "Chrome",
        },
    )

    db.add(event)

    db.commit()

    assert db.query(BehaviorEvent).count() == 1


# ==========================================================
# Recommendation
# ==========================================================

def test_create_recommendation(db):

    user = User(
        username="alice",
        email="alice@test.com",
        hashed_password="secret",
    )

    category = Category(
        name="LLM",
    )

    db.add_all([user, category])

    db.flush()

    product = Product(
        name="LLM Engineering",
        price=150,
        category_id=category.id,
    )

    db.add(product)

    db.flush()

    recommendation = Recommendation(

        user_id=user.id,

        product_id=product.id,

        confidence_score=0.95,

        explanation="Perfect course for your recent browsing activity.",

        recommendation_context={
            "reason": "Viewed multiple LLM products",
        },

        status=RecommendationStatus.ACTIVE,

        feedback=FeedbackType.NEUTRAL,
    )

    db.add(recommendation)

    db.commit()

    assert db.query(Recommendation).count() == 1

    assert recommendation.confidence_score == 0.95