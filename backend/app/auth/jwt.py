from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)


def create_access_token(data: dict[str, Any]) -> str:
    payload = data.copy()

    payload["type"] = "access"

    payload["exp"] = (
        datetime.now(UTC)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    payload = data.copy()

    payload["type"] = "refresh"

    payload["exp"] = (
        datetime.now(UTC)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except JWTError:
        return {}