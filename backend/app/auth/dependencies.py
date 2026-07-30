"""
FastAPI Dependency Injection for Authentication.

Provides the get_current_user dependency to protect routes
and inject authenticated user data into request handlers.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.firebase_auth import authenticate_user
from app.logging.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency that validates the Firebase JWT from the Authorization header.

    Expects:
        Authorization: Bearer <token>

    Returns:
        dict: Authenticated user data.
    """

    token = credentials.credentials

    try:
        user_data = authenticate_user(token)
        return user_data

    except Exception as exception:
        logger.warning(f"Authentication failed: {exception}")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_TOKEN",
                "message": "The provided token is invalid or expired",
            },
        )