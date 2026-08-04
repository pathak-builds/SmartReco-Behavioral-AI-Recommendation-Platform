"""
Semantic search service for SmartReco.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.product import Product
from app.services.embedding_service import get_embedding_service


class SearchService:
    """Service for semantic product search."""

    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = get_embedding_service()

    def semantic_search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Product]:
        """
        Search products using semantic similarity.
        """

        results = self.embedding_service.search(
            query=query,
            limit=limit,
        )

        ids = []

        if results.get("ids"):
            ids = results["ids"][0]

        if not ids:
            return []

        products = (
            self.db.query(Product)
            .filter(Product.id.in_(ids))
            .all()
        )

        # Preserve ChromaDB ranking
        product_map = {
            product.id: product
            for product in products
        }

        return [
            product_map[pid]
            for pid in ids
            if pid in product_map
        ]