"""
Main application entry point for SmartReco.

This module creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager
from pathlib import Path
import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.utils.logging_config import setup_logging

from app.api.auth import router as auth_router
from app.api.products import router as products_router
from app.api.admin import router as admin_router
from app.api.search import router as search_router
from app.api.behavior import router as behavior_router
from app.api.pages import router as pages_router
from app.api.recommendation import (
    router as recommendations_router,
)

# ---------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events.
    """

    logger.info("=" * 70)
    logger.info("%s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Application starting...")
    logger.info("Environment: %s", "Development" if settings.DEBUG else "Production")
    logger.info("=" * 70)

    # Create required directories
    Path("logs").mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(parents=True, exist_ok=True)
    Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)

    yield

    logger.info("Application shutting down...")


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------

app.include_router(auth_router)
app.include_router(products_router)
app.include_router(admin_router)
app.include_router(search_router)
app.include_router(behavior_router)
app.include_router(
    recommendations_router
)
app.include_router(pages_router)
# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=str(static_dir)),
    name="static",
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(
    directory=str(templates_dir)
)


# ---------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected application errors.
    """

    logger.exception(
        "Unhandled exception occurred: %s",
        str(exc),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred."
        },
    )


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.get("/", tags=["Home"])
async def home(request: Request):
    """
    Landing page.
    """

    logger.debug("Home page requested.")

    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "title": settings.APP_NAME,
        },
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Application health check.
    """

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production",
    }

# Future routers
# app.include_router(user_router)
# app.include_router(product_router)
# app.include_router(recommendation_router)
