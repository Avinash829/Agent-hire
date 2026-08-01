"""
Application Configuration Module.

Loads and validates all environment variables required by the application.
Fails fast with meaningful error messages if required variables are missing.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Application
    app_env: str = "development"
    frontend_url: str = "http://localhost:5173"

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "job_detection"

    # Google Gemini
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None

    # Tavily Search API
    tavily_api_key: Optional[str] = None

    # Firebase
    firebase_project_id: Optional[str] = None
    firebase_client_email: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_storage_bucket: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    # ML Model Paths
    ml_model_path: str = "app/ml/models"
    tfidf_vectorizer_path: str = "app/ml/models/tfidf_vectorizer.pkl"
    classifier_model_path: str = "app/ml/models/classifier.pkl"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def validate_required_variables(self) -> None:
        """Validate that all required environment variables are set."""
        required_variables = {
            "MONGODB_URI": self.mongodb_uri,
            "GEMINI_API_KEY": self.gemini_api_key,
            "TAVILY_API_KEY": self.tavily_api_key,
            "FIREBASE_PROJECT_ID": self.firebase_project_id,
            "FIREBASE_CLIENT_EMAIL": self.firebase_client_email,
            "FIREBASE_PRIVATE_KEY": self.firebase_private_key,
        }

        missing_variables = [
            name for name, value in required_variables.items()
            if not value or value == "None"
        ]

        if missing_variables:
            error_message = (
                f"Missing required environment variables: {', '.join(missing_variables)}. "
                f"Please set them in your .env file or environment."
            )
            raise ValueError(error_message)


@lru_cache()
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()

