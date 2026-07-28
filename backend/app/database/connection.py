"""
MongoDB Database Connection Module.

Manages async MongoDB connection using Motor driver.
Provides database instance for dependency injection.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config.settings import get_settings
from app.logging.logger import get_logger

logger = get_logger(__name__)

_mongo_client: AsyncIOMotorClient = None
_database: AsyncIOMotorDatabase = None


async def connect_to_mongodb() -> None:
    """Establish connection to MongoDB Atlas."""
    global _mongo_client, _database

    settings = get_settings()

    try:
        _mongo_client = AsyncIOMotorClient(
            settings.mongodb_uri,
            maxPoolSize=10,
            minPoolSize=2,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )

        _database = _mongo_client[settings.database_name]

        await _database.command("ping")
        logger.info(
            f"Connected to MongoDB database: {settings.database_name}"
        )
    except Exception as exception:
        logger.error(f"Failed to connect to MongoDB: {exception}")
        raise


async def close_mongodb_connection() -> None:
    """Close the MongoDB connection gracefully."""
    global _mongo_client

    if _mongo_client:
        _mongo_client.close()
        logger.info("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """Return the database instance for dependency injection."""
    if _database is None:
        raise RuntimeError(
            "Database not initialized. Call connect_to_mongodb() first."
        )
    return _database

