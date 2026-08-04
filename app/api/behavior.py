"""
Behavior API for SmartReco.

Receives behavioral events from the frontend
and stores them in the database.
"""

from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_optional_user
from app.database import get_db
from app.models.user import User
from app.schemas.behavior import (
    BehaviorEventCreate,
    BehaviorEventResponse,
)
from app.services.behavior_service import (
    BehaviorService,
)

router = APIRouter(
    prefix="/behavior",
    tags=["Behavior"],
)


# ==========================================================
# Record Behavior Event
# ==========================================================

@router.post(
    "/event",
    response_model=BehaviorEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def record_behavior_event(
    payload: BehaviorEventCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """
    Record a behavioral event.

    If the user is authenticated,
    associate the event with that user.

    Otherwise only store the session.
    """

    service = BehaviorService(db)

    event = service.record_event(
        payload=payload,
        user_id=(
            str(current_user.id)
            if current_user
            else None
        ),
    )

    return event