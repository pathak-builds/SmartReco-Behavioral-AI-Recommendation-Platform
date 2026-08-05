"""
Recommendation API.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

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
):
    """
    Return personalized recommendations.
    """

    service = RecommendationService(db)

    return service.get_recommendations(
        session_id=session_id,
    )