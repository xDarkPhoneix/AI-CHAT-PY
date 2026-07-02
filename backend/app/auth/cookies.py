from fastapi import Response


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
):

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Change to True in production (HTTPS)
        samesite="lax",
        max_age=15 * 60,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
    )


def clear_auth_cookies(
    response: Response,
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")