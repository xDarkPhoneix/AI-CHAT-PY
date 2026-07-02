from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.auth.jwt import decode_token
from app.models.user import User

security = HTTPBearer()
from fastapi import Cookie, HTTPException

from app.auth.jwt import decode_token
from app.models.user import User


async def get_current_user(
    access_token: str | None = Cookie(default=None),
) -> User:

    if access_token is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    payload = decode_token(access_token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    if payload["type"] != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
        )

    user = await User.get(payload["sub"])

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user