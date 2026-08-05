"""
Persuasion Agent for SmartReco.

Generates human-friendly explanations
for recommendations.
"""

from __future__ import annotations

from app.agents.mesh_client import get_mesh_client


class PersuasionAgent:
    """
    Generates recommendation explanations.
    """

    def __init__(self) -> None:
        self.client = get_mesh_client()

    # ======================================================
    # Explain Recommendation
    # ======================================================

    def explain(
        self,
        product: dict,
        profile: dict,
    ) -> str:
        """
        Generate a personalized explanation.
        """

        metadata = product["metadata"]

        prompt = f"""
You are an AI recommendation assistant.

User Profile

Favorite Topic:
{profile.get("favorite_topic")}

Summary:
{profile.get("summary")}

Recommended Product

Name:
{metadata.get("name")}

Category:
{metadata.get("category_name")}

Difficulty:
{metadata.get("difficulty")}

Explain in 2 short sentences why this
product is a good recommendation.
"""

        return self.client.generate(prompt)
    
    # ======================================================
    # Build Recommendation
    # ======================================================

    def build_recommendation(
        self,
        product: dict,
        profile: dict,
    ) -> dict:
        """
        Build a complete recommendation.
        """

        explanation = self.explain(
            product,
            profile,
        )

        return {

            "product": product,

            "score": product["score"],

            "explanation": explanation,

        }