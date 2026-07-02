from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: str

    filename: str

    status: str

    created_at: datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    status: str
    created_at: datetime