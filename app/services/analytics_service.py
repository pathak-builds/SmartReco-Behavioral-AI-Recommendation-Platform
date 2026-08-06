"""
Analytics service for SmartReco.

Provides business analytics for:
- Users
- Products
- Behavior Events
- Recommendations
"""

from __future__ import annotations

from sqlalchemy.orm import Session


from sqlalchemy import func

from app.models.user import User
from app.models.product import Product
from app.models.behavior import BehaviorEvent
from app.models.recommendation import Recommendation

class AnalyticsService:
    """
    Business analytics for SmartReco.
    """

    def __init__(self, db: Session):
        self.db = db
        
    # ======================================================
    # Dashboard Statistics
    # ======================================================

    def get_dashboard_stats(self) -> dict:
        """
        Return overall dashboard statistics.
        """

        return {
            "total_users": self.db.query(User).count(),

            "total_products": self.db.query(Product).count(),

            "total_behavior_events": (
                self.db.query(BehaviorEvent).count()
            ),

            "total_recommendations": (
                self.db.query(Recommendation).count()
            ),
        }