from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.dependencies import get_optional_user
from app.models.user import User
from app.services.recommendation_service import RecommendationService



templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["Pages"])





@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request},
    )


@router.get("/recommendations/history")
def recommendation_history(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    recommendations = []
    
    print("=" * 60)
    print("CURRENT USER:", current_user)
    print("COOKIES:", request.cookies)
    print("=" * 60)

    if current_user:
        service = RecommendationService(db)

        recommendations = service.get_history(
            user_id=str(current_user.id),
        )

    print("=" * 60)
    print("CURRENT USER:", current_user)
    print("NUMBER OF RECOMMENDATIONS:", len(recommendations))
    print("=" * 60)

    return templates.TemplateResponse(
        "recommendations/history.html",
        {
            "request": request,
            "recommendations": recommendations,
        },
    )