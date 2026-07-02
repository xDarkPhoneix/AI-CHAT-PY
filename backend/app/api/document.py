from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from app.core.rate_limiter import rate_limiter
from app.auth.dependencies import get_current_user
from app.models.document import DocumentModel
from app.models.user import User
from app.repositories.document_repository import (
    document_repository,
)
from app.schemas.document import UploadResponse, DocumentResponse
from app.services.pdf_service import pdf_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get(
    "/",
    response_model=list[DocumentResponse],
)
async def list_documents(
    current_user: User = Depends(get_current_user),
):
    docs = await document_repository.get_by_user_id(current_user.id)
    return [
        DocumentResponse(
            id=str(doc.id),
            filename=doc.original_filename,
            status=doc.status.value,
            created_at=doc.created_at,
        )
        for doc in docs
    ]

@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_user,
    ),
):
    
    rate_limiter.check(
    key=f"upload:{current_user.id}",
    limit=5,
    window=3600,
    ) 

    document = await pdf_service.upload_pdf(
        current_user,
        file,
    )

    return UploadResponse(
        id=str(document.id),
        filename=document.original_filename,
        status=document.status.value,
        created_at=document.created_at,
    )