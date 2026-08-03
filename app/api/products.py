"""
Public Product API for SmartReco.

Provides public endpoints for browsing products.

Endpoints
---------
GET /products
    List all active products.

GET /products/{product_id}
    Retrieve a single product by ID.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# ==========================================================
# List Products
# ==========================================================

@router.get(
    "",
    response_model=list[ProductResponse],
    summary="List Products",
    description="Return all active products.",
)
def list_products(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of products to skip.",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of products to return.",
    ),
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of active products.
    """

    service = ProductService(db)

    products = service.list_products(
        skip=skip,
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
            category_name=product.category.name if product.category else None,
            image_url=product.image_url,
            attributes=product.attributes,
            chroma_document_id=product.chroma_document_id,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
        for product in products
    ]


# ==========================================================
# Get Product
# ==========================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get Product",
    description="Return a single product.",
)
def get_product(
    product_id: str,
    db: Session =Depends(get_db),
):
    """
    Return a single active product.
    """

    service = ProductService(db)

    product = service.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        difficulty=product.difficulty,
        rating=product.rating,
        category_id=product.category_id,
        category_name=product.category.name if product.category else None,
        image_url=product.image_url,
        attributes=product.attributes,
        chroma_document_id=product.chroma_document_id,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )