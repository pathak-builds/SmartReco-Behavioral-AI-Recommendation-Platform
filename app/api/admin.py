"""
Admin API for SmartReco.

Provides administrator-only endpoints for managing:

- Products
- Categories

All routes require administrator authentication.
"""

from __future__ import annotations
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin
from app.database import get_db
from app.models.user import User
from app.schemas.product import (
    CategoryResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.category_service import CategoryService
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

templates = Jinja2Templates(
    directory=str(
        Path(__file__).parent.parent / "templates"
    )
)
# ==========================================================
# Helper
# ==========================================================

def build_product_response(product) -> ProductResponse:
    """
    Convert a Product ORM object into a ProductResponse.
    """

    return ProductResponse(
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
    
    # ==========================================================
# List Products
# ==========================================================

@router.get(
    "/products",
    response_model=list[ProductResponse],
)
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return all active products.
    """

    service = ProductService(db)

    products = service.list_products(
        skip=skip,
        limit=limit,
    )

    return [
        build_product_response(product)
        for product in products
    ]


# ==========================================================
# Get Product
# ==========================================================

@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return one product.
    """

    service = ProductService(db)

    product = service.get_product(product_id)

    if product is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return build_product_response(product)


# ==========================================================
# List Categories
# ==========================================================

@router.get(
    "/categories",
    response_model=list[CategoryResponse],
)
def list_categories(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Return every category.
    """

    service = CategoryService(db)

    return service.list_categories()

# ==========================================================
# Create Product
# ==========================================================

@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Create a new product.

    Administrator only.
    """

    service = ProductService(db)

    try:
        product = service.create_product(payload)

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return build_product_response(product)


# ==========================================================
# Update Product
# ==========================================================

@router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: str,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Update an existing product.

    Administrator only.
    """

    service = ProductService(db)

    try:

        product = service.update_product(
            product_id=product_id,
            data=payload,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    if product is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return build_product_response(product)

# ==========================================================
# Delete Product
# ==========================================================

@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """
    Soft delete a product.

    Administrator only.
    """

    service = ProductService(db)

    success = service.delete_product(product_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return None

@router.get(
    "/products-page",
    include_in_schema=False,
)
def products_page(
    request: Request,
    _: User = Depends(get_current_admin),
):
    """
    Product Management page.
    """

    return templates.TemplateResponse(
        "admin/products_list.html",
        {
            "request": request,
        },
    )
    
    
@router.get(
    "/products-page/create",
    include_in_schema=False,
)
def create_product_page(
    request: Request,
    _: User = Depends(get_current_admin),
):
    """
    Create Product page.
    """

    return templates.TemplateResponse(
        "admin/product_form.html",
        {
            "request": request,
            "product": None,
        },
    )
    
@router.get(
    "/products-page/{product_id}",
    include_in_schema=False,
)
def edit_product_page(
    product_id: str,
    request: Request,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):

    service = ProductService(db)

    product = service.get_product(product_id)

    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return templates.TemplateResponse(
        "admin/product_form.html",
        {
            "request": request,
            "product": product,
        },
    )