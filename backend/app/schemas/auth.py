"""
Pydantic Schemas for Authentication Flow.

Defines request and response models for authentication endpoints.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""

    success: bool = True
    uid: str = Field(..., description="Firebase user UID")
    email: Optional[str] = Field(None, description="User email address")
    name: Optional[str] = Field(None, description="User display name")
    picture: Optional[str] = Field(None, description="User profile picture URL")
    message: str = Field("Authentication successful", description="Status message")


class UserProfile(BaseModel):
    """User profile information."""

    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None

