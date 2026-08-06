"""
Analytics API for SmartReco.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.behavior import BehaviorEvent, EventType
from app.models.product import Product
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.analytics_service import AnalyticsService

templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent.parent / "templates"
    )
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/dashboard")
def analytics_dashboard(
    db: Session = Depends(get_db),
):
    """
    Return dashboard statistics.
    """

    service = AnalyticsService(db)

    return service.get_dashboard_stats()


@router.get(
    "",
    include_in_schema=False,
)
def analytics_page(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Render analytics dashboard.
    """

    event_counts = (
        db.query(
            BehaviorEvent.event_type,
            func.count(BehaviorEvent.id),
        )
        .group_by(BehaviorEvent.event_type)
        .all()
    )
    
    feedback_counts = (
        db.query(
            Recommendation.feedback,
            func.count(Recommendation.id),
        )
        .group_by(
            Recommendation.feedback,
        )
        .all()
    )
    
    top_products = (
        db.query(
            Product.name,
            func.count(BehaviorEvent.id),
        )
        .join(
            BehaviorEvent,
            Product.id == BehaviorEvent.product_id,
        )
        .filter(
            BehaviorEvent.event_type == EventType.PRODUCT_VIEW
        )
        .group_by(Product.name)
        .order_by(func.count(BehaviorEvent.id).desc())
        .limit(5)
        .all()
    )
    
    recommendation_trend = (
        db.query(
            func.date(Recommendation.created_at),
            func.count(Recommendation.id),
        )
        .group_by(
            func.date(Recommendation.created_at)
        )
        .order_by(
            func.date(Recommendation.created_at)
        )
        .all()
    )
    
    top_searches = (
        db.query(
            BehaviorEvent.search_query,
            func.count(BehaviorEvent.id),
        )
        .filter(
            BehaviorEvent.event_type == EventType.SEARCH,
            BehaviorEvent.search_query.isnot(None),
        )
        .group_by(
            BehaviorEvent.search_query,
        )
        .order_by(
            func.count(BehaviorEvent.id).desc()
        )
        .limit(10)
        .all()
    )
        

    return templates.TemplateResponse(
        "admin/analytics.html",
        {
            "request": request,
            "total_users": db.query(User).count(),
            "total_products": db.query(Product).count(),
            "total_behavior_events": db.query(BehaviorEvent).count(),
            "total_recommendations": db.query(Recommendation).count(),
            "event_labels": [
                event.value
                for event, _ in event_counts
            ],
            "event_values": [
                count
                for _, count in event_counts
            ],
            
            "feedback_labels": [
                feedback.value for feedback, _ in feedback_counts
            ],

            "feedback_values": [
                count for _, count in feedback_counts
            ],
            "top_product_labels": [
                name for name, _ in top_products
            ],

            "top_product_values": [
                count for _, count in top_products
            ],
            "trend_labels": [
                str(date) for date, _ in recommendation_trend
            ],

            "trend_values": [
                count for _, count in recommendation_trend
            ],
            
            "search_labels": [
                query for query, _ in top_searches
            ],

            "search_values": [
                count for _, count in top_searches
            ],
            
            
        },
    )
    
    