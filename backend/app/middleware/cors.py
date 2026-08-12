"""
CORS Middleware Configuration.

Configures Cross-Origin Resource Sharing for the application.
Restricts access to the configured frontend URL(s) in production.
Supports multiple origins via the FRONTEND_URLS environment variable
(comma-separated), e.g.:
    FRONTEND_URLS=https://frontend1.vercel.app,https://frontend2.vercel.app
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings


def configure_cors(application: FastAPI) -> None:
    """Configure CORS middleware with the application settings."""
    settings = get_settings()

    if settings.app_env == "development":
        allowed_origins = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
        ]
    else:
        allowed_origins = settings.frontend_urls_list

    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Accept",
            "Origin",
            "X-Requested-With",
        ],
        expose_headers=["Content-Disposition"],
        max_age=600,
    )

