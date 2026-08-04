"""
Semantic search API for SmartReco.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductResponse
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"],
)


@router.get(
    "",
    response_model=list[ProductResponse],
)
def semantic_search(
    q: str = Query(
        ...,
        min_length=2,
        description="Search query",
    ),
    limit: int = Query(
        default=5,
        ge=1,
        le=20,
    ),
    db: Session = Depends(get_db),
):
    """
    Perform semantic product search.
    """

    service = SearchService(db)

    products = service.semantic_search(
        query=q,
        limit=limit,
    )

    return [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            difficulty=product.difficulty,
            rating=product.rating,
            category_id=product.category_id,
            category_name=(
                product.category.name
                if product.category
                else None
            ),
            image_url=product.image_url,
            attributes=product.attributes,
            chroma_document_id=product.chroma_document_id,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
        for product in products
    ]