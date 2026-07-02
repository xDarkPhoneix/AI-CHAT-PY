from fastapi import HTTPException, status

from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.auth.password import (
    hash_password,
    verify_password,
)
from app.core.security import (
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.database.redis import set_value
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)
from app.auth.jwt import (
    decode_token,
)
from app.database.redis import (
    get_value,
)


class AuthService:

    async def register(
        self,
        data: RegisterRequest,
    ) -> User:

        existing_user = await user_repository.get_by_email(
            data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hash_password(
                data.password
            ),
        )

        return await user_repository.create(user)

    async def login(
        self,
        data: LoginRequest,
    ):

        user = await user_repository.get_by_email(
            data.email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        if not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        payload = {
            "sub": str(user.id),
            "email": user.email,
        }

        access_token = create_access_token(payload)

        refresh_token = create_refresh_token(payload)

        await set_value(
            key=f"refresh_token:{user.id}",
            value=refresh_token,
            expire=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user,
        } 


    async def refresh(
        self,
        refresh_token: str,
    ):

        payload = decode_token(
            refresh_token
        )

        if not payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )

        if payload["type"] != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )

        redis_token = await get_value(
            f"refresh_token:{payload['sub']}"
        )

        if redis_token != refresh_token:
            raise HTTPException(
                status_code=401,
                detail="Session expired",
            )

        new_access = create_access_token(
            {
                "sub": payload["sub"],
                "email": payload["email"],
            }
        )

        return {
            "access_token": new_access,
        }

    async def logout(self, user: User):
        from app.database.redis import delete_value
        await delete_value(f"refresh_token:{user.id}")


auth_service = AuthService()