"""
Core Exception Handler Registry.

Centralizes exception-to-response mapping for the application.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    ApplicationError,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    MLPipelineError,
    AgentPipelineError,
    DatabaseError,
    ExternalServiceError,
)
from app.logging.logger import get_logger

logger = get_logger(__name__)


EXCEPTION_MAPPING: dict = {
    AuthenticationError: status.HTTP_401_UNAUTHORIZED,
    AuthorizationError: status.HTTP_403_FORBIDDEN,
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    NotFoundError: status.HTTP_404_NOT_FOUND,
    MLPipelineError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    AgentPipelineError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ExternalServiceError: status.HTTP_502_BAD_GATEWAY,
}


def handle_application_error(request: Request, exception: ApplicationError) -> JSONResponse:
    """Handle ApplicationError and subclasses with consistent JSON responses."""
    status_code = EXCEPTION_MAPPING.get(type(exception), status.HTTP_500_INTERNAL_SERVER_ERROR)

    logger.error(
        f"Application error: {exception.error_code} - {exception.message} "
        f"on {request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": exception.error_code,
                "message": exception.message,
            },
            "path": request.url.path,
            "method": request.method,
        },
    )


def handle_unhandled_exception(request: Request, exception: Exception) -> JSONResponse:
    """Handle unexpected exceptions with a generic error response."""
    logger.error(
        f"Unhandled exception: {str(exception)} on {request.method} {request.url.path}",
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
            },
            "path": request.url.path,
            "method": request.method,
        },
    )

