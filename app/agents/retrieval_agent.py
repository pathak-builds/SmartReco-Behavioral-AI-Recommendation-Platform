"""
Retrieval Agent for SmartReco.

Uses semantic search and user interests
to retrieve the best candidate products.
"""

from __future__ import annotations

from app.services.embedding_service import EmbeddingService


class RetrievalAgent:
    """
    Retrieves candidate products using
    semantic similarity.
    """

    def __init__(self) -> None:

        self.embedding = EmbeddingService()

    # ======================================================
    # Build Search Query
    # ======================================================

    def build_query(
        self,
        profile: dict,
    ) -> str:
        """
        Convert user profile into a search query.
        """

        parts = []

        favorite = profile.get(
            "favorite_topic"
        )

        if favorite:

            parts.append(favorite)

        topics = profile.get(
            "favorite_topics",
            [],
        )

        parts.extend(topics)

        summary = profile.get(
            "summary",
            "",
        )

        if summary:

            parts.append(summary)

        return " ".join(parts)

    # ======================================================
    # Retrieve Products
    # ======================================================

    def retrieve(
        self,
        profile: dict,
        limit: int = 10,
    ) -> list:
        """
        Retrieve candidate products.
        """

        query = self.build_query(
            profile
        )

        return self.embedding.semantic_search(
            query=query,
            limit=limit,
        )