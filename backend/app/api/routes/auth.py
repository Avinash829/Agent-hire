"""
Authentication Routes.

Handles user authentication and profile verification via Firebase.
"""

from fastapi import APIRouter, Depends, Header
from app.auth.dependencies import get_current_user
from app.schemas.auth import AuthResponse
from app.logging.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/verify", response_model=AuthResponse)
async def verify_token(user: dict = Depends(get_current_user)):
    """
    Verify Firebase authentication token and return user profile.

    The token is extracted from the Authorization header (Bearer <token>).
    """
    logger.info(f"Token verified for user: {user.get('email')}")

    return AuthResponse(
        uid=user["uid"],
        email=user.get("email"),
        name=user.get("name"),
        picture=user.get("picture"),
        message="Authentication successful",
    )


@router.get("/profile", response_model=AuthResponse)
async def get_profile(user: dict = Depends(get_current_user)):
    """
    Get the authenticated user's profile information.
    """
    return AuthResponse(
        uid=user["uid"],
        email=user.get("email"),
        name=user.get("name"),
        picture=user.get("picture"),
        message="Profile retrieved successfully",
    )

