"""
Recommendation service for SmartReco.

Uses the LangGraph workflow to generate
personalized recommendations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.graph import RecommendationGraph
from app.models.behavior import BehaviorEvent
from app.models.recommendation import Recommendation


class RecommendationService:
    """
    Service responsible for generating
    personalized recommendations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self.workflow = (
            RecommendationGraph()
            .compile()
        )
        
    # ======================================================
    # Recent Events
    # ======================================================

    def get_recent_events(
        self,
        user_id: str | None = None,
        session_id: str | None = None,
        limit: int = 50,
    ) -> list[BehaviorEvent]:
        """
        Load recent behavior events.
        """

        query = self.db.query(
            BehaviorEvent
        )

        if user_id:

            query = query.filter(
                BehaviorEvent.user_id == user_id
            )

        elif session_id:

            query = query.filter(
                BehaviorEvent.session_id == session_id
            )

        return (
            query.order_by(
                BehaviorEvent.event_timestamp.desc()
            )
            .limit(limit)
            .all()
        )
        
    # ======================================================
    # Recommendations
    # ======================================================

    def get_recommendations(
        self,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> list[dict]:
        """
        Generate recommendations.
        """

        events = self.get_recent_events(
            user_id=user_id,
            session_id=session_id,
        )

        state = {

            "events": events,

            "analysis": {},

            "profile": {},

            "retrieved": [],

            "ranked": [],

            "recommendations": [],

        }

        result = self.workflow.invoke(
            state
        )

        recommendations = result[
            "recommendations"
        ]

        self._save_recommendations(
            recommendations=recommendations,
            user_id=user_id,
        )

        return recommendations
        
    def _save_recommendations(
        self,
        recommendations: list[dict],
        user_id: str | None,
    ) -> None:
        
        print("=" * 60)
        print("USER ID:", user_id)
        print("=" * 60)
        """
        Persist generated recommendations.
        """

        if user_id is None:
            return

        for item in recommendations:

            recommendation = Recommendation(

                user_id=user_id,

                product_id=item["product"]["product_id"],

                confidence_score=item["score"],

                explanation=item["explanation"],

                recommendation_context={
                    "metadata": item["product"]["metadata"],
                },

            )

            self.db.add(
                recommendation
            )

        self.db.commit()