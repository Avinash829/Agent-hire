"""
FastAPI Dependency Injection for Authentication.

Provides the get_current_user dependency to protect routes
and inject authenticated user data into request handlers.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional

from app.auth.firebase_auth import authenticate_user
from app.logging.logger import get_logger

logger = get_logger(__name__)

# auto_error=False lets us return a proper 401 (with WWW-Authenticate)
# instead of the default 403 that HTTPBearer raises when the header is absent.
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    Dependency that validates the Firebase JWT from the Authorization header.

    Expects:
        Authorization: Bearer <token>

    Returns:
        dict: Authenticated user data.

    Raises:
        HTTPException 401: If the Authorization header is missing or the token
        is invalid / expired.
    """
    _unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
        detail={
            "code": "UNAUTHORIZED",
            "message": "Authentication credentials were not provided or are invalid",
        },
    )

    if credentials is None:
        logger.warning("Request received with no Authorization header")
        raise _unauthorized

    token = credentials.credentials

    try:
        user_data = authenticate_user(token)
        return user_data

    except Exception as exception:
        logger.warning(f"Authentication failed: {exception}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail={
                "code": "INVALID_TOKEN",
                "message": "The provided token is invalid or expired",
            },
        )