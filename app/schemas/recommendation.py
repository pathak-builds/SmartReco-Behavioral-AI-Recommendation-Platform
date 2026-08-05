"""
Schemas for recommendation APIs.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class RecommendationFeedback(str, Enum):
    """Allowed feedback values."""

    like = "like"
    dislike = "dislike"


class RecommendationFeedbackRequest(BaseModel):
    """Feedback payload."""

    feedback: RecommendationFeedback


class MessageResponse(BaseModel):
    """Simple response."""

    message: str