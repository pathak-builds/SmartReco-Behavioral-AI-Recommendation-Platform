"""
Database seed script for SmartReco.

Creates:
- Admin user
- Course categories
- Sample AI courses
"""

from __future__ import annotations

import uuid

from passlib.context import CryptContext

from app.database import SessionLocal
from app.models.category import Category
from app.models.product import Product
from app.models.user import User, UserRole

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def seed() -> None:
    """Populate the development database."""

    db = SessionLocal()

    try:
        # ------------------------------------------------------
        # Prevent duplicate seeding
        # ------------------------------------------------------
        if db.query(User).first():
            print("Database already seeded.")
            return

        # ------------------------------------------------------
        # Admin User
        # ------------------------------------------------------
        admin = User(
            id=str(uuid.uuid4()),
            username="admin",
            email="admin@smartreco.com",
            hashed_password=pwd_context.hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(admin)

        # ------------------------------------------------------
        # Categories
        # ------------------------------------------------------
        ai = Category(
            name="Artificial Intelligence",
            description="AI and Machine Learning courses",
        )

        llm = Category(
            name="Large Language Models",
            description="LLM Engineering",
        )

        rag = Category(
            name="Retrieval Augmented Generation",
            description="RAG Systems",
        )

        langgraph = Category(
            name="LangGraph",
            description="Agentic AI Workflows",
        )

        python = Category(
            name="Python",
            description="Python Programming",
        )

        db.add_all(
            [
                ai,
                llm,
                rag,
                langgraph,
                python,
            ]
        )

        db.flush()

        # ------------------------------------------------------
        # Products
        # ------------------------------------------------------
        products = [

            Product(
                id=str(uuid.uuid4()),
                name="Complete Generative AI Bootcamp",
                description="Learn LLMs, Prompt Engineering and AI applications from scratch.",
                price=99.0,
                difficulty="Beginner",
                rating=4.8,
                category_id=ai.id,
                image_url="https://placehold.co/600x400",
                attributes={
                    "duration": "35 hours",
                    "level": "Beginner",
                    "language": "English",
                },
            ),

            Product(
                id=str(uuid.uuid4()),
                name="Production RAG Systems",
                description="Build enterprise Retrieval-Augmented Generation applications.",
                price=129.0,
                difficulty="Intermediate",
                rating=4.9,
                category_id=rag.id,
                image_url="https://placehold.co/600x400",
                attributes={
                    "duration": "18 hours",
                    "level": "Intermediate",
                    "language": "English",
                },
            ),

            Product(
                id=str(uuid.uuid4()),
                name="LangGraph Masterclass",
                description="Design production multi-agent workflows using LangGraph.",
                price=149.0,
                difficulty="Advanced",
                rating=5.0,
                category_id=langgraph.id,
                image_url="https://placehold.co/600x400",
                attributes={
                    "duration": "22 hours",
                    "level": "Advanced",
                    "language": "English",
                },
            ),

            Product(
                id=str(uuid.uuid4()),
                name="Python for AI Engineers",
                description="Modern Python for machine learning and AI development.",
                price=79.0,
                difficulty="Beginner",
                rating=4.7,
                category_id=python.id,
                image_url="https://placehold.co/600x400",
                attributes={
                    "duration": "25 hours",
                    "level": "Beginner",
                    "language": "English",
                },
            ),

            Product(
                id=str(uuid.uuid4()),
                name="LLM Engineering Professional",
                description="Deploy production-ready LLM applications with modern tooling.",
                price=159.0,
                difficulty="Advanced",
                rating=4.9,
                category_id=llm.id,
                image_url="https://placehold.co/600x400",
                attributes={
                    "duration": "28 hours",
                    "level": "Advanced",
                    "language": "English",
                },
            ),
        ]

        db.add_all(products)

        db.commit()

        print("SmartReco database seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()