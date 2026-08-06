"""
Recommendation API.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import RedirectResponse

from fastapi import HTTPException, status




from app.schemas.recommendation import (
    RecommendationFeedbackRequest,
    MessageResponse,
)

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

templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent.parent / "templates"
    )
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
    
@router.post(
    "/{recommendation_id}/feedback",
    response_model=MessageResponse,
)
def submit_feedback(
    recommendation_id: str,
    payload: RecommendationFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Store user feedback for a recommendation.
    """

    service = RecommendationService(db)

    try:

        service.update_feedback(
            recommendation_id=recommendation_id,
            feedback=payload.feedback.value,
            user_id=str(current_user.id),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return MessageResponse(
        message="Feedback saved successfully."
    )
    
# @router.get("/history")
# def get_recommendation_history(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     """
#     Return recommendation history for the current user.
#     """

#     service = RecommendationService(db)

#     return service.get_history(
#         user_id=str(current_user.id),
#     )
    
@router.get("/page")
def recommendation_history_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """
    Render recommendation history page.
    """

    service = RecommendationService(db)

    recommendations = []

    if current_user:
        recommendations = service.get_history(
            user_id=str(current_user.id),
        )

    return templates.TemplateResponse(
        "recommendations/history.html",
        {
            "request": request,
            "recommendations": recommendations,
            "title": "Recommendation History",
        },
    )
    
@router.post("/refresh")
def refresh_recommendations(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """
    Generate fresh recommendations and
    redirect back to the history page.
    """

    if current_user is not None:

        service = RecommendationService(db)

        service.get_recommendations(
            user_id=str(current_user.id),
        )

    return RedirectResponse(
        url="/recommendations/page",
        status_code=303,
    )