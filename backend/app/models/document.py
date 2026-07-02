from datetime import UTC, datetime
from enum import Enum

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import Field


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"

    QUEUED = "queued"

    PROCESSING = "processing"

    COMPLETED = "completed"

    FAILED = "failed"


class DocumentModel(Document):
    user_id: PydanticObjectId

    original_filename: str

    stored_filename: str

    file_path: str

    file_size: int

    status: DocumentStatus = DocumentStatus.UPLOADED

    pages: int | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    class Settings:
        name = "documents"

        indexes = [
            "user_id",
            "status",
        ]