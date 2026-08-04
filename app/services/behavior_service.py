"""
Behavior service for SmartReco.

Handles recording and retrieving
user behavioral events.
"""

from __future__ import annotations

import logging
from datetime import timezone

from sqlalchemy.orm import Session

from app.models.behavior import BehaviorEvent
from app.schemas.behavior import (
    BehaviorEventCreate,
)

logger = logging.getLogger(__name__)


class BehaviorService:
    """
    Service responsible for storing
    behavioral events.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    # ==========================================================
    # Record Event
    # ==========================================================

    def record_event(
        self,
        payload: BehaviorEventCreate,
        user_id: str | None = None,
    ) -> BehaviorEvent:
        """
        Record a behavioral event.
        """

        timestamp = payload.timestamp

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(
                tzinfo=timezone.utc,
            )

        metadata = payload.event_data or {}

        event = BehaviorEvent(
            user_id=user_id,

            product_id=metadata.get("product_id"),

            session_id=payload.session_id,

            event_type=payload.event_type,

            search_query=metadata.get("query"),

            page_url=metadata.get("page"),

            time_spent_seconds=metadata.get(
                "time_spent_seconds"
            ),

            event_metadata=metadata,

            event_timestamp=timestamp,
        )

        self.db.add(event)

        self.db.commit()

        self.db.refresh(event)

        logger.info(
            "Recorded %s event",
            payload.event_type.value,
        )

        return event

    # ==========================================================
    # Get Events For Session
    # ==========================================================

    def get_session_events(
        self,
        session_id: str,
    ) -> list[BehaviorEvent]:
        """
        Return all events for a session.
        """

        return (
            self.db.query(BehaviorEvent)
            .filter(
                BehaviorEvent.session_id == session_id,
            )
            .order_by(
                BehaviorEvent.timestamp.asc(),
            )
            .all()
        )

    # ==========================================================
    # Get Events For User
    # ==========================================================

    def get_user_events(
        self,
        user_id: str,
    ) -> list[BehaviorEvent]:
        """
        Return all events for a user.
        """

        return (
            self.db.query(BehaviorEvent)
            .filter(
                BehaviorEvent.user_id == user_id,
            )
            .order_by(
                BehaviorEvent.timestamp.desc(),
            )
            .all()
        )

    # ==========================================================
    # Count Events
    # ==========================================================

    def count_events(self) -> int:
        """
        Return total number of
        behavioral events.
        """

        return (
            self.db.query(
                BehaviorEvent,
            )
            .count()
        )