"""
Recommendation service for SmartReco.

Uses the LangGraph workflow to generate
personalized recommendations.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.agents.graph import RecommendationGraph
from app.models.behavior import BehaviorEvent


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

        return result[
            "recommendations"
        ]