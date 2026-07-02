import redis.asyncio as redis

from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


async def connect_to_redis():
    await redis_client.ping()


async def close_redis():
    await redis_client.aclose()


async def set_value(
    key: str,
    value: str,
    expire: int | None = None,
):
    await redis_client.set(
        key,
        value,
        ex=expire,
    )


async def get_value(key: str):
    return await redis_client.get(key)


async def delete_value(key: str):
    await redis_client.delete(key)