"""Import all models here so Alembic can detect them."""

from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.behavior import BehaviorEvent
from app.models.recommendation import Recommendation
#from app.models.audit import AuditLog
#from app.models.user_profile import UserProfile
from app.models.refresh_token import RefreshToken

__all__ = [
    "User",
    "Category",
    "Product",
    "BehaviorEvent",
    "Recommendation",
    "RefreshToken",
    
]