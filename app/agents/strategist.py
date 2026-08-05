"""
Recommendation Strategist.

Ranks retrieved products using
multiple weighted signals.
"""

from __future__ import annotations


class RecommendationStrategist:
    """
    Hybrid recommendation ranking.
    """

    # ======================================================
    # Score One Product
    # ======================================================

    def score_product(
        self,
        product: dict,
        profile: dict,
    ) -> float:

        metadata = product["metadata"]

        score = 0.0

        # -------------------------------
        # Semantic Similarity
        # -------------------------------

        similarity = 1.0 - product["distance"]

        score += similarity * 0.40

        # -------------------------------
        # Rating
        # -------------------------------

        rating = metadata.get(
            "rating",
            0,
        )

        score += (rating / 5.0) * 0.25

        # -------------------------------
        # Favorite Topic Match
        # -------------------------------

        favorite = str(
            profile.get("favorite_topic") or ""
        ).lower()

        category = str(
            metadata.get("category_name") or ""
        ).lower()

        if favorite and favorite in category:

            score += 0.20

        # -------------------------------
        # Difficulty Preference
        # -------------------------------

        summary = str(
            profile.get("summary") or ""
        ).lower()

        difficulty = str(
            metadata.get("difficulty") or ""
        ).lower()

        if difficulty and difficulty in summary:

            score += 0.15

        return round(score, 4)

    # ======================================================
    # Rank Products
    # ======================================================

    def rank(
        self,
        products: list,
        profile: dict,
    ) -> list:

        ranked = []

        for product in products:

            product["score"] = self.score_product(
                product,
                profile,
            )

            ranked.append(product)

        ranked.sort(

            key=lambda p: p["score"],

            reverse=True,

        )

        return ranked