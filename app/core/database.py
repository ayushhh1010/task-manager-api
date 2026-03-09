from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import certifi
import logging

logger = logging.getLogger(__name__)


async def init_db(models: list):
    logger.info("Connecting to MongoDB...")
    client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000,
        connectTimeoutMS=30000,
    )
    database = client[settings.DATABASE_NAME]
    await init_beanie(database=database, document_models=models)
    logger.info("Successfully connected to MongoDB!")