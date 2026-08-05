"""
Recommendation API.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.dependencies import get_optional_user
from app.models.user import User
from app.database import get_db
from app.services.recommendation_service import (
    RecommendationService,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

@router.get("/")
def get_recommendations(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """
    Return personalized recommendations.
    """

    service = RecommendationService(db)

    return service.get_recommendations(
        session_id=session_id,
        user_id=(
            str(current_user.id)
            if current_user
            else None
        ),
    )