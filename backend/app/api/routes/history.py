"""
Verification History Routes.

Handles retrieval of past verification records for authenticated users.
"""

from fastapi import APIRouter, Depends, Query
from app.auth.dependencies import get_current_user
from app.dependencies.container import get_container
from app.schemas.verification import VerificationHistoryResponse
from app.logging.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=VerificationHistoryResponse)
async def get_verification_history(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    user: dict = Depends(get_current_user),
):
    """
    Get paginated verification history for the authenticated user.
    """
    container = get_container()
    history_service = container.get_history_service()

    result = await history_service.get_history(
        firebase_uid=user["uid"],
        page=page,
        limit=limit,
    )

    return VerificationHistoryResponse(
        success=True,
        items=result["items"],
        total=result["total"],
        page=result.get("page", page),
        limit=result.get("limit", limit),
        total_pages=result.get("total_pages", 0),
    )


@router.get("/{verification_id}")
async def get_verification_detail(
    verification_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Get detailed result of a specific verification.
    """
    container = get_container()
    history_service = container.get_history_service()

    result = await history_service.get_verification_detail(
        verification_id=verification_id,
        firebase_uid=user["uid"],
    )

    return {"success": True, "data": result}

