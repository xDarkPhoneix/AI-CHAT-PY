from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserResponse(BaseModel):
    id: str

    full_name: str

    email: EmailStr

    role: UserRole

    is_active: bool

    is_verified: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )