"""
Global Error Handler Middleware.

Registers exception handlers for consistent JSON error responses
across all API endpoints.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import handle_application_error, handle_unhandled_exception
from app.exceptions.custom_exceptions import ApplicationError
from app.logging.logger import get_logger

logger = get_logger(__name__)


def register_exception_handlers(application: FastAPI) -> None:
    """Register global exception handlers for the FastAPI application."""

    @application.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, exception: ApplicationError):
        return handle_application_error(request, exception)

    @application.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exception: Exception):
        return handle_unhandled_exception(request, exception)

    @application.exception_handler(status.HTTP_422_UNPROCESSABLE_ENTITY)
    async def validation_error_handler(request: Request, exception: Exception):
        """Handle Pydantic validation errors with clean formatting."""
        errors = getattr(exception, "errors", lambda: [])()
        error_details = [
            {
                "field": " -> ".join(str(loc) for loc in error.get("loc", [])),
                "message": error.get("msg", ""),
                "type": error.get("type", ""),
            }
            for error in errors
        ]

        logger.warning(f"Validation error on {request.method} {request.url.path}: {error_details}")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": error_details,
                },
                "path": request.url.path,
                "method": request.method,
            },
        )

