"""
Development entry point for SmartReco.

Run the application locally with:

    python run.py

For production, use:

    uvicorn app.main:app
"""

import uvicorn

from app.config import settings


def main() -> None:
    """Start the SmartReco application."""

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()