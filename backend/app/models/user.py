from datetime import UTC, datetime
from enum import Enum

from beanie import Document
from pydantic import EmailStr, Field


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Document):
    full_name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    hashed_password: str

    role: UserRole = UserRole.USER

    is_active: bool = True

    is_verified: bool = False

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    class Settings:
        name = "users"

        indexes = [
            "email",
        ]