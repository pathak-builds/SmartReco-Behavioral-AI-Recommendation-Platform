"""
Behavior Analyst Agent for SmartReco.

Analyzes user behavioral events and
creates a summary of user interests.
"""

from __future__ import annotations

from collections import Counter

from app.agents.mesh_client import get_mesh_client
from app.models.behavior import BehaviorEvent, EventType


class BehaviorAnalyst:
    """
    Analyze behavior events and infer
    user interests.
    """

    def __init__(self) -> None:
        self.client = get_mesh_client()

    # ======================================================
    # Analyze Behavior
    # ======================================================

    def analyze(
        self,
        events: list[BehaviorEvent],
    ) -> dict:
        """
        Analyze user behavior.
        """

        if not events:

            return {
                "summary": "New user.",
                "favorite_topics": [],
                "favorite_products": [],
                "search_queries": [],
                "activity_score": 0,
            }

        search_queries = []

        viewed_products = []

        pages = []

        for event in events:

            if event.search_query:
                search_queries.append(
                    event.search_query
                )

            if event.product_id:
                viewed_products.append(
                    event.product_id
                )

            if event.page_url:
                pages.append(
                    event.page_url
                )

        product_counter = Counter(
            viewed_products
        )

        prompt = f"""
You are an AI behavioral analyst.

The user performed {len(events)} actions.

Searches:
{search_queries}

Visited Pages:
{pages}

Viewed Products:
{viewed_products}

Summarize the user's interests in one paragraph.
"""

        summary = self.client.generate(
            prompt
        )

        return {

            "summary": summary,

            "favorite_topics":
                search_queries,

            "favorite_products":
                [
                    product
                    for product, _
                    in product_counter.most_common(5)
                ],

            "search_queries":
                search_queries,

            "activity_score":
                len(events),

        }