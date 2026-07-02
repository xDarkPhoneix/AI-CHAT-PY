from fastapi import APIRouter, status
from app.auth.cookies import set_auth_cookies, clear_auth_cookies
from app.schemas.auth import RegisterRequest,LoginRequest,LoginResponse,RefreshRequest
from app.schemas.user import UserResponse
from app.services.auth_service import auth_service
from fastapi import Depends
from fastapi import Cookie, Request, Response, HTTPException

from app.auth.dependencies import (
    get_current_user,
)

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
):

    user = await auth_service.register(
        request
    )

    return UserResponse(
        id=str(user.id),
        full_name=user.full_name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
    )

@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
):

    result = await auth_service.login(request)

    set_auth_cookies(
        response=response,
        access_token=result["access_token"],
        refresh_token=result["refresh_token"],
    )

    return {
        "message": "Login successful."
    }

@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return UserResponse(
        id=str(current_user.id),
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
    )

@router.post("/refresh")
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):

    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Missing refresh token",
        )

    result = await auth_service.refresh(
        refresh_token
    )

    set_auth_cookies(
        response=response,
        access_token=result["access_token"],
        refresh_token=refresh_token,
    )

    return {
        "message": "Token refreshed."
    }

@router.post("/logout")
async def logout(
    response: Response,
    current_user: User = Depends(
        get_current_user
    ),
):

    await auth_service.logout(current_user)

    clear_auth_cookies(response)

    return {
        "message": "Logged out successfully."
    }