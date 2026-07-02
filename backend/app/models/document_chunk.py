from datetime import UTC, datetime

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import Field


class DocumentChunk(Document):
    document_id: PydanticObjectId

    user_id: PydanticObjectId

    chunk_index: int

    page_number: int

    content: str

    embedding: list[float]

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    class Settings:
        name = "document_chunks"

        indexes = [
            "document_id",
            "user_id",
        ]