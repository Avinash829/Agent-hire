"""
Firebase Authentication Utilities.

Provides helper functions for Firebase token verification
and user data extraction.
"""

from app.config.firebase_config import verify_firebase_token
from app.logging.logger import get_logger

logger = get_logger(__name__)


def authenticate_user(token: str) -> dict:
    """
    Authenticate a user by verifying their Firebase JWT token.

    Args:
        token: The Firebase JWT token from the Authorization header.

    Returns:
        dict: Decoded token claims containing user information.

    Raises:
        AuthenticationError: If token is invalid or expired.
    """
    decoded_token = verify_firebase_token(token)

    user_data = {
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "name": decoded_token.get("name"),
        "picture": decoded_token.get("picture"),
    }

    logger.info(f"User authenticated: {user_data['email']}")
    return user_data

