"""
MongoDB Document Model for Verification Records.

Defines the schema structure for storing verification results
in MongoDB collections.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class VerificationDocument(BaseModel):
    """MongoDB document model for a single verification record."""

    verification_id: str = Field(..., alias="_id")
    firebase_uid: str = Field(..., description="Firebase user UID who submitted the verification")
    job_description: str = Field(..., description="Full job description text")
    source_link: Optional[str] = Field(None, description="URL where job was found")
    application_link: Optional[str] = Field(None, description="Application submission URL")

    ml_score: float = Field(..., ge=0.0, le=1.0, description="ML pipeline risk score")
    ml_confidence: float = Field(..., ge=0.0, le=1.0, description="ML pipeline confidence")
    agent_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Agent pipeline risk score")
    final_score: float = Field(..., ge=0.0, le=1.0, description="Synthesized final score")

    verdict: str = Field(..., description="Final verdict: fraudulent, suspicious, or legitimate")
    reasons: list = Field(default_factory=list, description="Reasons for the verdict")
    recommendations: list = Field(default_factory=list, description="Recommended actions")
    evidence: dict = Field(default_factory=dict, description="Detailed evidence from both pipelines")

    ml_result: dict = Field(default_factory=dict, description="Raw ML pipeline result")
    agent_result: dict = Field(default_factory=dict, description="Raw agent pipeline result")

    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Verification timestamp")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class VerificationCollection:
    """MongoDB collection name constant."""

    COLLECTION_NAME = "verifications"

    @staticmethod
    def indexes() -> list:
        """Return the indexes required for the verifications collection."""
        return [
            {"key": [("firebase_uid", 1), ("timestamp", -1)]},
            {"key": [("verification_id", 1)], "unique": True},
        ]

