from fastapi import HTTPException, status

from app.services.redis_service import (
    redis_service,
)


class RateLimiter:

    def check(
        self,
        key: str,
        limit: int,
        window: int,
    ):

        current = redis_service.increment(key)

        if current == 1:
            redis_service.expire(
                key,
                window,
            )

        if current > limit:

            ttl = redis_service.ttl(key)

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    f"Rate limit exceeded. "
                    f"Try again in {ttl} seconds."
                ),
            )


rate_limiter = RateLimiter()