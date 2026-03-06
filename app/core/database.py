from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def init_db(models: list):
    client= AsyncIOMotorClient(settings.MONGODB_URL)
    database= client[settings.DATABASE_NAME]
    await init_beanie(database=database, document_models=models)