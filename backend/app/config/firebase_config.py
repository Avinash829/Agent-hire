"""
Firebase Configuration Module.

Initializes the Firebase Admin SDK for authentication verification.
"""

import firebase_admin
from firebase_admin import credentials, auth
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)

_firebase_app = None


def initialize_firebase() -> None:
    """Initialize Firebase Admin SDK with service account credentials."""
    global _firebase_app

    if _firebase_app is not None:
        return

    settings = get_settings()

    try:
        credential = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": settings.firebase_project_id,
                "private_key": (settings.firebase_private_key or "").replace("\\n", "\n"),
                "client_email": settings.firebase_client_email,
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        )
        _firebase_app = firebase_admin.initialize_app(
            credential,
            {"storageBucket": settings.firebase_storage_bucket},
        )
        logger.info("Firebase Admin SDK initialized successfully")
    except Exception as exception:
        logger.error(f"Failed to initialize Firebase: {exception}")
        raise


def verify_firebase_token(token: str) -> dict:
    """Verify a Firebase JWT token and return decoded claims."""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        logger.warning("Expired Firebase token provided")
        raise
    except auth.InvalidIdTokenError:
        logger.warning("Invalid Firebase token provided")
        raise
    except Exception as exception:
        logger.error(f"Firebase token verification failed: {exception}")
        raise

