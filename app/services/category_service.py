"""
Category service for SmartReco.

Contains all business logic for:

- Create category
- Retrieve category
- List categories
- Update category
- Delete category
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryService:
    """Business logic for category management."""

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Create Category
    # ==========================================================

    def create_category(
        self,
        name: str,
        description: str | None = None,
        parent_id: int | None = None,
    ) -> Category:
        """
        Create a new category.
        """

        existing = (
            self.db.query(Category)
            .filter(Category.name == name)
            .first()
        )

        if existing:
            raise ValueError("Category already exists.")

        category = Category(
            name=name,
            description=description,
            parent_id=parent_id,
            is_active=True,
        )

        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category

    # ==========================================================
    # Get Category
    # ==========================================================

    def get_category(
        self,
        category_id: int,
    ) -> Category | None:
        """
        Retrieve a category by ID.
        """

        return (
            self.db.query(Category)
            .filter(
                Category.id == category_id,
                Category.is_active.is_(True),
            )
            .first()
        )

    # ==========================================================
    # List Categories
    # ==========================================================

    def list_categories(self) -> list[Category]:
        """
        Return all active categories.
        """

        return (
            self.db.query(Category)
            .filter(Category.is_active.is_(True))
            .order_by(Category.name.asc())
            .all()
        )

    # ==========================================================
    # Root Categories
    # ==========================================================

    def get_root_categories(self) -> list[Category]:
        """
        Return only top-level categories.
        """

        return (
            self.db.query(Category)
            .filter(
                Category.parent_id.is_(None),
                Category.is_active.is_(True),
            )
            .order_by(Category.name.asc())
            .all()
        )

    # ==========================================================
    # Update Category
    # ==========================================================

    def update_category(
        self,
        category_id: int,
        name: str | None = None,
        description: str | None = None,
        parent_id: int | None = None,
    ) -> Category | None:
        """
        Update a category.
        """

        category = self.get_category(category_id)

        if category is None:
            return None

        if name is not None:
            category.name = name

        if description is not None:
            category.description = description

        category.parent_id = parent_id

        self.db.commit()
        self.db.refresh(category)

        return category

    # ==========================================================
    # Delete Category
    # ==========================================================

    def delete_category(
        self,
        category_id: int,
    ) -> bool:
        """
        Soft delete a category.
        """

        category = self.get_category(category_id)

        if category is None:
            return False

        category.is_active = False

        self.db.commit()

        return True