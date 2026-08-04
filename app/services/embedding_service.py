"""
Embedding service for SmartReco.

Provides semantic search functionality using
Sentence Transformers and ChromaDB.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Handles embedding generation and
    ChromaDB operations.
    """

    def __init__(self) -> None:
        """
        Initialize embedding model and ChromaDB.
        """

        logger.info(
            "Loading embedding model: %s",
            settings.EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

        chroma_path = Path(
            settings.CHROMA_PERSIST_DIR
        )

        chroma_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(chroma_path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
            ),
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="products",
                metadata={
                    "hnsw:space": "cosine",
                },
            )
        )

        logger.info(
            "Embedding service initialized."
        )
        
    # ======================================================
    # Build Search Document
    # ======================================================

    def build_document(
        self,
        product: Any,
    ) -> str:
        """
        Convert a Product into searchable text.
        """

        parts: list[str] = []

        if product.name:
            parts.append(product.name)

        if product.description:
            parts.append(product.description)

        if getattr(product, "difficulty", None):
            parts.append(
                f"Difficulty {product.difficulty}"
            )

        if getattr(product, "category", None):
            if product.category:
                parts.append(
                    f"Category {product.category.name}"
                )

        parts.append(
            f"Price {product.price}"
        )

        if product.attributes:

            for key, value in product.attributes.items():

                parts.append(
                    f"{key} {value}"
                )

        return " ".join(parts)

    # ======================================================
    # Build Metadata
    # ======================================================

    def build_metadata(
        self,
        product: Any,
    ) -> dict[str, Any]:
        """
        Metadata stored alongside the embedding.
        """

        return {
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "rating": float(product.rating),
            "difficulty": (
                product.difficulty
                if product.difficulty
                else ""
            ),
            "category_id": (
                int(product.category_id)
                if product.category_id is not None
                else 0
            ),
            "category_name": (
                product.category.name
                if getattr(product, "category", None)
                else ""
            ),
            "image_url": (
                product.image_url
                if product.image_url
                else ""
            ),
            "is_active": bool(product.is_active),
        }
        
    # ======================================================
    # Generate Embedding
    # ======================================================

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate a vector embedding for text.
        """

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    # ======================================================
    # Upsert Product
    # ======================================================

    def upsert_product(
        self,
        product: Any,
    ) -> None:
        """
        Create or update a product embedding.
        """

        document = self.build_document(product)

        embedding = self.embed_text(document)

        metadata = self.build_metadata(product)

        self.collection.upsert(
            ids=[product.id],
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata],
        )

        logger.info(
            "Indexed product: %s",
            product.name,
        )

    # ======================================================
    # Delete Product
    # ======================================================

    def delete_product(
        self,
        product_id: str,
    ) -> None:
        """
        Remove a product from ChromaDB.
        """

        self.collection.delete(
            ids=[product_id],
        )

        logger.info(
            "Deleted embedding for product %s",
            product_id,
        )

    # ======================================================
    # Collection Count
    # ======================================================

    def count(self) -> int:
        """
        Return number of indexed products.
        """

        return self.collection.count()
    
    # ======================================================
    # Semantic Search
    # ======================================================

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> dict[str, Any]:
        """
        Perform semantic similarity search.
        """

        query_embedding = self.embed_text(query)

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
        )

    # ======================================================
    # Get Indexed Product IDs
    # ======================================================

    def get_product_ids(
        self,
    ) -> list[str]:
        """
        Return all indexed product IDs.
        """

        data = self.collection.get()

        return data.get(
            "ids",
            [],
        )