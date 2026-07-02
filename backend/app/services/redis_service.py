import redis

from app.core.config import settings


class RedisService:

    def __init__(self):

        self.client = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    def get(self, key: str):

        return self.client.get(key)

    def set(
        self,
        key: str,
        value: str,
        expire: int = 3600,
    ):

        self.client.set(
            key,
            value,
            ex=expire,
        )

    def delete(
        self,
        key: str,
    ):

        self.client.delete(key)

    def increment(
        self,
        key: str,
    ) -> int:

        return self.client.incr(key)

    def expire(
        self,
        key: str,
        seconds: int,
    ):

        self.client.expire(
            key,
            seconds,
        )

    def ttl(
        self,
        key: str,
    ) -> int:

        return self.client.ttl(key)


redis_service = RedisService()