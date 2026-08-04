from __future__ import annotations

import logging
import uuid
from typing import Optional
from sqlalchemy import or_
import math
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.embedding_service import get_embedding_service

logger = logging.getLogger(__name__)


class ProductService:
    """Business logic for product management."""

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        # Singleton embedding service
        self.embedding_service = get_embedding_service()

    # ==========================================================
    # Create Product
    # ==========================================================

    def create_product(self, data: ProductCreate) -> Product:
        """
        Create a new product.
        """

        category = (
            self.db.query(Category)
            .filter(Category.id == data.category_id)
            .first()
        )

        if category is None:
            raise ValueError("Category does not exist.")

        product = Product(
            id=str(uuid.uuid4()),
            name=data.name,
            description=data.description,
            price=data.price,
            difficulty=data.difficulty,
            rating=data.rating,
            category_id=data.category_id,
            image_url=data.image_url,
            attributes=data.attributes,
            is_active=True,
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        
        # --------------------------------------------------
        # Sync product to ChromaDB
        # --------------------------------------------------

        try:

            self.embedding_service.collection.upsert(
                ids=[product.id],
                documents=[
                    self.embedding_service.build_document(product)
                ],
                embeddings=[
                    self.embedding_service.embed_text(
                        self.embedding_service.build_document(product)
                    )
                ],
                metadatas=[
                    self.embedding_service.build_metadata(product)
                ],
            )

            logger.info(
                "Product %s synced to ChromaDB.",
                product.id,
            )

        except Exception as exc:

            logger.exception(
                "Failed to sync product %s: %s",
                product.id,
                exc,
            )

        return product

    # ==========================================================
    # Get Product
    # ==========================================================

    def get_product(
        self,
        product_id: str,
    ) -> Product | None:
        """
        Retrieve a product by ID.
        """

        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(
                Product.id == product_id,
                Product.is_active.is_(True),
            )
            .first()
        )

    # ==========================================================
    # List Products
    # ==========================================================

    def list_products(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        """
        Return active products.
        """

        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_active.is_(True))
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # ==========================================================
    # Update Product
    # ==========================================================

    def update_product(
        self,
        product_id: str,
        data: ProductUpdate,
    ) -> Product | None:
        """
        Update a product.
        """

        product = self.get_product(product_id)

        if product is None:
            return None

        update_data = data.model_dump(exclude_unset=True)

        if "category_id" in update_data:

            category = (
                self.db.query(Category)
                .filter(Category.id == update_data["category_id"])
                .first()
            )

            if category is None:
                raise ValueError("Category does not exist.")

        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        
        try:

            self.embedding_service.collection.upsert(
                ids=[product.id],
                documents=[
                    self.embedding_service.build_document(product)
                ],
                embeddings=[
                    self.embedding_service.embed_text(
                        self.embedding_service.build_document(product)
                    )
                ],
                metadatas=[
                    self.embedding_service.build_metadata(product)
                ],
            )

            logger.info(
                "Updated embedding for product %s",
                product.id,
            )

        except Exception as exc:

            logger.exception(
                "Embedding update failed: %s",
                exc,
            )

        return product

    # ==========================================================
    # Soft Delete Product
    # ==========================================================

    def delete_product(
        self,
        product_id: str,
    ) -> bool:
        """
        Soft delete a product.
        """

        product = self.get_product(product_id)

        if product is None:
            return False

        product.is_active = False

        self.db.commit()
        
        
        try:

            self.embedding_service.collection.delete(
                ids=[product.id],
            )

            logger.info(
                "Deleted embedding for %s",
                product.id,
            )

        except Exception as exc:

            logger.exception(
                "Embedding deletion failed: %s",
                exc,
            )

        return True

    # ==========================================================
    # List Products By Category
    # ==========================================================

    def get_products_by_category(
        self,
        category_id: int,
    ) -> list[Product]:
        """
        Return all active products for a category.
        """

        return (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(
                Product.category_id == category_id,
                Product.is_active.is_(True),
            )
            .order_by(Product.rating.desc())
            .all()
        )
        
    # ==========================================================
    # Search Products
    # ==========================================================
    def search_products(
        self,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        difficulty: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        sort_by: str = "name",
        page: int = 1,
        page_size: int = 12,
    ) -> tuple[list[Product], int, int]:
        """
        Search, filter, sort and paginate products.

        Returns:
            (
                products,
                total_products,
                total_pages,
            )
        """

        q = (
            self.db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_active.is_(True))
        )

        # -------------------------------
        # Text Search
        # -------------------------------

        if query:

            term = f"%{query}%"

            q = q.filter(
                or_(
                    Product.name.ilike(term),
                    Product.description.ilike(term),
                )
            )

        # -------------------------------
        # Category
        # -------------------------------

        if category_id:

            q = q.filter(
                Product.category_id == category_id
            )


        # -------------------------------
        # Difficulty Filter
        # -------------------------------

        if difficulty:

            q = q.filter(
                Product.difficulty == difficulty
    )
        # -------------------------------
        # Price Filters
        # -------------------------------

        if min_price is not None:

            q = q.filter(
                Product.price >= min_price
            )

        if max_price is not None:

            q = q.filter(
                Product.price <= max_price
            )

        # -------------------------------
        # Sorting
        # -------------------------------

        if sort_by == "price_asc":

            q = q.order_by(
                Product.price.asc()
            )

        elif sort_by == "price_desc":

            q = q.order_by(
                Product.price.desc()
            )

        elif sort_by == "newest":

            q = q.order_by(
                Product.created_at.desc()
            )

        else:

            q = q.order_by(
                Product.name.asc()
            )

        total = q.count()

        total_pages = (
            math.ceil(total / page_size)
            if total
            else 1
        )

        page = max(
            1,
            min(page, total_pages),
        )

        products = (
            q.offset(
                (page - 1) * page_size
            )
            .limit(page_size)
            .all()
        )

        return (
            products,
            total,
            total_pages,
        )