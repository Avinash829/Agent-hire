"""
Hybrid Fake Job Detection - Backend Application Entry Point.

This module initializes and configures the FastAPI application,
including middleware, routers, and startup validation.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.settings import get_settings
from app.middleware.cors import configure_cors
from app.middleware.error_handler import register_exception_handlers
from app.logging.logger import configure_logging
from app.database.connection import connect_to_mongodb, close_mongodb_connection
from app.api.routes.auth import router as auth_router
from app.api.routes.verify import router as verify_router
from app.api.routes.history import router as history_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle: startup and shutdown events."""
    configure_logging()
    settings = get_settings()
    settings.validate_required_variables()
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    application = FastAPI(
        title="Hybrid Fake Job Detection API",
        description="Enterprise-grade API for detecting fraudulent job postings using "
        "Machine Learning and Agentic AI pipelines.",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    configure_cors(application)
    register_exception_handlers(application)

    application.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
    application.include_router(verify_router, prefix="/api/v1/verify", tags=["Verification"])
    application.include_router(history_router, prefix="/api/v1/history", tags=["History"])

    @application.get("/api/health")
    async def health_check():
        """Health check endpoint to verify the application is running."""
        return {"status": "healthy", "service": "hybrid-fake-job-detection"}

    return application


app = create_application()

