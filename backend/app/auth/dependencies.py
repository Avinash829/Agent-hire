"""
FastAPI Dependency Injection for Authentication.

Provides the get_current_user dependency to protect routes
and inject authenticated user data into request handlers.
"""

from fastapi import Header, HTTPException, status
from app.auth.firebase_auth import authenticate_user
from app.logging.logger import get_logger

logger = get_logger(__name__)


async def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Dependency that extracts and validates the Firebase JWT from the request.

    Expects the Authorization header to be in the format: "Bearer <token>".

    Args:
        authorization: The Authorization header value.

    Returns:
        dict: Authenticated user data (uid, email, name, picture).

    Raises:
        HTTPException: If the token is missing, malformed, or invalid.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "MISSING_TOKEN",
                "message": "Authorization header is required",
            },
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_TOKEN_FORMAT",
                "message": "Authorization header must be in format: Bearer <token>",
            },
        )

    token = parts[1]

    try:
        user_data = authenticate_user(token)
        return user_data
    except Exception as exception:
        logger.warning(f"Authentication failed: {str(exception)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_TOKEN",
                "message": "The provided token is invalid or expired",
            },
        )

