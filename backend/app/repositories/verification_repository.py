"""
Verification Repository Module.

Provides data access layer for verification records in MongoDB.
Follows the repository pattern to abstract database operations.
"""

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database.connection import get_database
from app.models.verification import VerificationDocument, VerificationCollection
from app.logging.logger import get_logger

logger = get_logger(__name__)


class VerificationRepository:
    """Repository for managing verification records in MongoDB."""

    def __init__(self, database: AsyncIOMotorDatabase = None):
        self._database = database or get_database()
        self._collection = self._database[VerificationCollection.COLLECTION_NAME]

    async def create_verification(self, verification: VerificationDocument) -> str:
        """
        Insert a new verification record into the database.

        Args:
            verification: The verification document to insert.

        Returns:
            str: The verification ID.

        Raises:
            DatabaseError: If the insert operation fails.
        """
        try:
            document = verification.model_dump(by_alias=True)
            await self._collection.insert_one(document)
            logger.info(
                "[MongoDB] Verification created: %s for user: %s",
                verification.verification_id,
                verification.firebase_uid,
            )
            return verification.verification_id
        except Exception as exception:
            logger.exception(
                "[MongoDB] Failed to create verification: %s", str(exception)
            )
            raise

    async def get_verification_by_id(
        self, verification_id: str, firebase_uid: str
    ) -> dict:
        """
        Retrieve a single verification record by ID and user.

        Args:
            verification_id: The verification record ID.
            firebase_uid: The Firebase UID of the user.

        Returns:
            dict: The verification document, or None if not found.
        """
        try:
            document = await self._collection.find_one(
                {"_id": verification_id, "firebase_uid": firebase_uid}
            )
            return document
        except Exception as exception:
            logger.exception(
                "[MongoDB] Failed to retrieve verification %s: %s",
                verification_id,
                str(exception),
            )
            raise

    async def get_user_verifications(
        self, firebase_uid: str, limit: int = 20, skip: int = 0
    ) -> list:
        """
        Retrieve paginated verification history for a user.

        Args:
            firebase_uid: The Firebase UID of the user.
            limit: Maximum number of records to return.
            skip: Number of records to skip.

        Returns:
            list: List of verification documents.
        """
        try:
            cursor = (
                self._collection.find(
                    {"firebase_uid": firebase_uid},
                    {
                        "_id": 1,
                        "job_description": 1,
                        "final_score": 1,
                        "verdict": 1,
                        "timestamp": 1,
                    },
                )
                .sort("timestamp", -1)
                .skip(skip)
                .limit(limit)
            )

            documents = await cursor.to_list(length=limit)
            return documents
        except Exception as exception:
            logger.exception(
                "[MongoDB] Failed to retrieve verifications for user %s: %s",
                firebase_uid,
                str(exception),
            )
            raise

    async def count_user_verifications(self, firebase_uid: str) -> int:
        """
        Count total verification records for a user.

        Args:
            firebase_uid: The Firebase UID of the user.

        Returns:
            int: Total number of verification records.
        """
        try:
            count = await self._collection.count_documents(
                {"firebase_uid": firebase_uid}
            )
            return count
        except Exception as exception:
            logger.exception(
                "[MongoDB] Failed to count verifications for user %s: %s",
                firebase_uid,
                str(exception),
            )
            raise

