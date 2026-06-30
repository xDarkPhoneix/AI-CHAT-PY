from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models import ALL_MODELS
from app.core.logger import logger

client: AsyncIOMotorClient | None = None


async def connect_to_mongodb():
    global client

    client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        maxPoolSize=50,
        minPoolSize=5,
    )

    database = client[settings.DATABASE_NAME]

    await init_beanie(
        database=database,
        document_models=ALL_MODELS,
    )

    logger.info("MongoDB Connected")


async def close_mongodb_connection():
    global client

    if client:
        client.close()

    logger.info("MongoDB Closed")