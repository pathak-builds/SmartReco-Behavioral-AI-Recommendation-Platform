"""
Embedding service for SmartReco.

Provides semantic vector storage using
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
    Singleton service responsible for
    creating and searching embeddings.
    """

    def __init__(self) -> None:
        logger.info(
            "Loading embedding model: %s",
            settings.EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

        chroma_dir = Path(
            settings.CHROMA_PERSIST_DIR
        )

        chroma_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(chroma_dir),
            settings=ChromaSettings(
                anonymized_telemetry=False,
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name="products",
            metadata={
                "hnsw:space": "cosine",
            },
        )

        logger.info(
            "Embedding service initialized successfully."
        )

    # ======================================================
    # Build Product Text
    # ======================================================

    def build_document(
        self,
        product: Any,
    ) -> str:
        """
        Convert a product into searchable text.
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
    ) -> dict:

        return {
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "category_id": (
                product.category_id
                if product.category_id
                else 0
            ),
            "difficulty": (
                product.difficulty
                if product.difficulty
                else ""
            ),
            "rating": product.rating,
            "image_url": (
                product.image_url
                if product.image_url
                else ""
            ),
        }

    # ======================================================
    # Create Embedding
    # ======================================================

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embedding vector.
        """

        return self.model.encode(
            text,
        ).tolist()

    # ======================================================
    # Collection Count
    # ======================================================

    def count(self) -> int:
        """
        Return number of documents.
        """

        return self.collection.count()
    
        # ======================================================
    # Upsert Product
    # ======================================================

    def upsert_product(self, product: Any) -> None:
        """
        Create or update a product embedding.
        """

        document = self.build_document(product)

        self.collection.upsert(
            ids=[product.id],
            documents=[document],
            embeddings=[self.embed_text(document)],
            metadatas=[self.build_metadata(product)],
        )

    # ======================================================
    # Delete Product
    # ======================================================

    def delete_product(self, product_id: str) -> None:
        """
        Remove a product embedding.
        """

        self.collection.delete(
            ids=[product_id],
        )

    # ======================================================
    # Search
    # ======================================================

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> dict:
        """
        Perform semantic search.
        """

        query_embedding = self.embed_text(query)

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
        )