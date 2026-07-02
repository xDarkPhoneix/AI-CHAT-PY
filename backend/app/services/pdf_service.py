from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.models.document import (
    DocumentModel,
    DocumentStatus,
)
from app.models.user import User
from app.repositories.document_repository import (
    document_repository,
)
from app.workers.pdf_tasks import process_pdf

UPLOAD_DIR = Path("app/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MAX_FILE_SIZE = 20 * 1024 * 1024


class PDFService:

    async def upload_pdf(
        self,
        user: User,
        file: UploadFile,
    ) -> DocumentModel:

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename is required.",
            )

        stored_filename, file_path, file_size = (
            await self.save_pdf(file)
        )

        document = DocumentModel(
            user_id=user.id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_path=file_path,
            file_size=file_size,
            status=DocumentStatus.QUEUED,
        )

        document = await document_repository.create(document)

        process_pdf.delay(str(document.id))

        return document



    async def save_pdf(
        self,
        file: UploadFile,
    ) -> tuple[str, str, int]:

        extension = Path(file.filename).suffix.lower()

        filename = f"{uuid4()}{extension}"

        file_path = UPLOAD_DIR / filename

        total_size = 0

        with open(file_path, "wb") as buffer:

            while chunk := await file.read(
                1024 * 1024
            ):

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:

                    buffer.close()

                    file_path.unlink(
                        missing_ok=True
                    )

                    raise HTTPException(
                        status_code=400,
                        detail="Maximum file size is 20 MB.",
                    )

                buffer.write(chunk)

        await file.close()

        return (
            filename,
            str(file_path),
            total_size,
        )


pdf_service = PDFService()