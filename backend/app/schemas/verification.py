"""
Pydantic Schemas for Job Verification Flow.

Defines request and response models for the verification API endpoints.
"""

from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional
from datetime import datetime


class VerificationRequest(BaseModel):
    """Request schema for submitting a job posting for verification."""

    job_description: str = Field(
        ...,
        min_length=20,
        description="Complete job posting text",
    )

    source_link: Optional[str] = Field(
        None,
        description="URL where the job posting was found",
    )

    application_link: Optional[str] = Field(
        None,
        description="URL where applicants submit their application",
    )

    @field_validator("job_description", mode="before")
    @classmethod
    def clean_job_description(cls, value):
        if not isinstance(value, str):
            return value

        return value.strip()[:5000]

class MLResult(BaseModel):
    """ML pipeline analysis result."""

    fraud_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Probability of fraud (0-1)"
    )
    risk_score: float = Field(
        ..., ge=0.0, le=1.0, description="Normalized risk score (0-1)"
    )
    suspicious_keywords: list = Field(
        default_factory=list, description="Detected suspicious keywords"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in the prediction"
    )


class AgentResult(BaseModel):
    """Agentic AI investigation result."""

    company_name: Optional[str] = Field(None, description="Extracted company name")
    company_domain: Optional[str] = Field(None, description="Extracted company domain")
    agent_verdict: Optional[str] = Field(None, description="Agent pipeline verdict: fraudulent, suspicious, or legitimate")
    gemini_reasoning: Optional[str] = Field(None, description="Gemini analysis reasoning text")
    agent_risk_score: Optional[float] = Field(None, description="Calculated AI risk score")

class SynthesisResult(BaseModel):
    """Combined synthesis result from ML and Agent pipelines."""

    overall_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall fraud risk score"
    )
    overall_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence level"
    )
    verdict: str = Field(
        ..., description="Final verdict: fraudulent, suspicious, or legitimate"
    )
    reasons: list = Field(
        default_factory=list, description="List of reasons for the verdict"
    )
    recommendations: list = Field(
        default_factory=list, description="Recommended actions"
    )


class VerificationResponse(BaseModel):
    """Complete verification response returned to the client."""

    success: bool = True
    verification_id: str = Field(..., description="Unique verification identifier")
    ml_result: MLResult
    agent_result: AgentResult
    synthesis: SynthesisResult
    evidence: dict = Field(
        default_factory=dict, description="Combined evidence from both pipelines"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class VerificationHistoryItem(BaseModel):
    """Individual verification history item."""

    verification_id: str
    job_description_preview: str = Field(
        ..., description="First 100 characters of job description"
    )
    overall_score: float
    verdict: str
    timestamp: datetime


class VerificationHistoryResponse(BaseModel):
    """List of verification history items with pagination metadata."""

    success: bool = True
    items: list[VerificationHistoryItem] = Field(default_factory=list)
    total: int = 0
    page: int = Field(1, description="Current page number")
    limit: int = Field(20, description="Items per page")
    total_pages: int = Field(0, description="Total number of pages")

