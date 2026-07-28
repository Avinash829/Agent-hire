"""
Generic Response Schemas.

Defines standard response wrappers for consistent API responses.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional


class ErrorDetail(BaseModel):
    """Error detail for failed responses."""

    code: str = Field(..., description="Error code identifier")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[list] = Field(None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    success: bool = False
    error: ErrorDetail
    path: str = Field(..., description="Request URL path")
    method: str = Field(..., description="HTTP method")


class SuccessResponse(BaseModel):
    """Standard success response schema."""

    success: bool = True
    data: Any = Field(None, description="Response payload")
    message: str = Field("Request successful", description="Status message")

