"""
History Service Module.

Provides business logic for retrieving user verification history.
"""

from typing import Dict, Any, List
from app.repositories.verification_repository import VerificationRepository
from app.logging.logger import get_logger

logger = get_logger(__name__)


class HistoryService:
    """Service for managing user verification history."""

    def __init__(self, repository: VerificationRepository):
        self.repository = repository

    async def get_verification_detail(
        self, verification_id: str, firebase_uid: str
    ) -> Dict[str, Any]:
        """
        Retrieve detailed verification result.

        Args:
            verification_id: The verification record ID.
            firebase_uid: The Firebase UID of the requesting user.

        Returns:
            Dict: Full verification details.

        Raises:
            NotFoundError: If the verification record is not found.
        """
        logger.info(
            f"Fetching verification detail: {verification_id} for user {firebase_uid}"
        )

        document = await self.repository.get_verification_by_id(
            verification_id, firebase_uid
        )

        if not document:
            from app.exceptions.custom_exceptions import NotFoundError
            raise NotFoundError(
                message=f"Verification record {verification_id} not found"
            )

        document["_id"] = str(document["_id"])
        document["timestamp"] = (
            document["timestamp"].isoformat()
            if hasattr(document["timestamp"], "isoformat")
            else str(document["timestamp"])
        )

        return document

    async def get_history(
        self, firebase_uid: str, page: int = 1, limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get paginated verification history for a user.

        Args:
            firebase_uid: The Firebase UID of the user.
            page: Page number (1-indexed).
            limit: Items per page.

        Returns:
            Dict with items, total count, and pagination info.
        """
        logger.info(
            f"Fetching verification history for user {firebase_uid}: "
            f"page={page}, limit={limit}"
        )

        skip = (page - 1) * limit
        documents = await self.repository.get_user_verifications(
            firebase_uid, limit=limit, skip=skip
        )
        total = await self.repository.count_user_verifications(firebase_uid)

        items = []
        for document in documents:
            job_preview = (
                document.get("job_description", "")[:100] + "..."
                if len(document.get("job_description", "")) > 100
                else document.get("job_description", "")
            )

            timestamp = document.get("timestamp")
            if hasattr(timestamp, "isoformat"):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)

            items.append({
                "verification_id": str(document["_id"]),
                "job_description_preview": job_preview,
                "overall_score": document.get("final_score", 0),
                "verdict": document.get("verdict", "unknown"),
                "timestamp": timestamp,
            })

        return {
            "success": True,
            "items": items,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit if total > 0 else 0,
        }

    async def delete_verification(
        self, verification_id: str, firebase_uid: str
    ) -> bool:
        """
        Delete a verification record.

        Args:
            verification_id: The verification record ID.
            firebase_uid: The Firebase UID of the requesting user.

        Returns:
            bool: True if deleted successfully.

        Raises:
            NotFoundError: If the verification record is not found.
        """
        logger.info(
            f"Deleting verification: {verification_id} for user {firebase_uid}"
        )

        document = await self.repository.get_verification_by_id(
            verification_id, firebase_uid
        )

        if not document:
            from app.exceptions.custom_exceptions import NotFoundError
            raise NotFoundError(
                message=f"Verification record {verification_id} not found"
            )

        from app.database.connection import get_database
        database = get_database()
        result = await database["verifications"].delete_one(
            {"_id": verification_id, "firebase_uid": firebase_uid}
        )

        return result.deleted_count > 0

