"""
Behavior schemas for SmartReco.

Contains request schemas for recording
user behavioral events.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.behavior import EventType


# ==========================================================
# Create Behavior Event
# ==========================================================

class BehaviorEventCreate(BaseModel):
    """
    Schema used by the frontend tracker
    to record a behavioral event.
    """

    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    event_type: EventType

    event_data: dict[str, Any] | None = Field(
        default_factory=dict,
    )

    timestamp: datetime


# ==========================================================
# Behavior Event Response
# ==========================================================

class BehaviorEventResponse(BaseModel):
    """
    Response returned after
    successfully recording an event.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: str

    user_id: str | None

    product_id: str | None

    session_id: str

    event_type: EventType

    search_query: str | None

    page_url: str | None

    time_spent_seconds: float | None

    event_metadata: dict[str, Any] | None

    event_timestamp: datetime

    created_at: datetime