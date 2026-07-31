"""
Job Verification Routes.

Handles submission of job postings for fraud verification.
"""

from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.schemas.verification import VerificationRequest, VerificationResponse
from app.dependencies.container import get_container
from app.logging.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/", response_model=VerificationResponse)
async def verify_job_posting(
    request: VerificationRequest,
    user: dict = Depends(get_current_user),
):
    """
    Submit a job posting for fraud verification.

    Runs both ML and Agent pipelines in parallel, then synthesizes results.
    """
    container = get_container()
    verification_service = container.get_verification_service()

    logger.info(
        "[API] Verification request received from user: %s",
        user.get("email"),
    )

    result = await verification_service.verify_job_posting(
        job_description=request.job_description,
        firebase_uid=user["uid"],
        source_link=request.source_link,
        application_link=request.application_link,
    )

    return VerificationResponse(
        success=True,
        verification_id=result["verification_id"],
        ml_result=result["ml_result"],
        agent_result=result["agent_result"],
        synthesis=result["synthesis"],
        evidence=result["evidence"],
        timestamp=result["timestamp"],
    )

