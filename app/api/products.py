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

from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent.parent / "templates"
    )
)

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService
from app.services.category_service import CategoryService

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
# Product Catalog Page
# ==========================================================

@router.get(
    "/browse",
    include_in_schema=False,
)
def browse_products(
    request: Request,
    page: int = 1,
    query: str | None = None,
    category_id: str | None = None,
    difficulty: str | None = None,
    min_price: float | None = None,
    max_price: float |None = None,
    sort_by: str = "name",
    db: Session = Depends(get_db),
):
    """
    Render product catalog page.
    """
    # ---------------------------------------------
    # Normalize optional filters
    # ---------------------------------------------

    if category_id == "":
        category_id = None
    elif category_id is not None:
        category_id = int(category_id)

    if difficulty == "":
        difficulty = None

    if query == "":
        query = None
        
        
    service = ProductService(db)

    products, total, total_pages = (
        service.search_products(
            query=query,
            category_id=category_id,
            difficulty=difficulty,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            page=page,
        )
    )

    categories = (
        CategoryService(db)
        .list_categories()
    )

    return templates.TemplateResponse(
        "products/list.html",
        {
            "request": request,
            "products": products,
            "categories": categories,
            "difficulty": difficulty,
            "total": total,
            "page": page,
            "pages": total_pages,
            "query": query,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "sort_by": sort_by,
        },
    )
    
# ==========================================================
# Product Detail Page
# ==========================================================

@router.get(
    "/browse/{product_id}",
    include_in_schema=False,
)
def product_detail(
    product_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Render product detail page.
    """

    service = ProductService(db)

    product = service.get_product(product_id)

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    return templates.TemplateResponse(
        "products/detail.html",
        {
            "request": request,
            "product": product,
        },
    )
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
    
