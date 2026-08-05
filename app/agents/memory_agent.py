"""
Memory Agent for SmartReco.

Maintains a persistent understanding
of user interests across sessions.
"""

from __future__ import annotations

from collections import Counter


class MemoryAgent:
    """
    Maintains long-term user preferences.
    """

    def build_profile(
        self,
        analysis: dict,
    ) -> dict:
        """
        Build a persistent preference profile.
        """

        topics = analysis.get(
            "favorite_topics",
            [],
        )

        products = analysis.get(
            "favorite_products",
            [],
        )

        topic_counter = Counter(
            topics
        )

        profile = {

            "favorite_topic":

                topic_counter.most_common(1)[0][0]

                if topic_counter

                else None,

            "favorite_topics":

                [
                    topic
                    for topic, _
                    in topic_counter.most_common(5)
                ],

            "favorite_products":

                products,

            "activity_score":

                analysis.get(
                    "activity_score",
                    0,
                ),

            "summary":

                analysis.get(
                    "summary",
                    "",
                ),

        }

        return profile