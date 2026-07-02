from beanie import PydanticObjectId

from app.models.document import (
    DocumentModel,
    DocumentStatus,
)


class DocumentRepository:

    async def create(
        self,
        document: DocumentModel,
    ):
        await document.insert()

        return document

    async def get_by_id(
        self,
        document_id: str,
    ):

        return await DocumentModel.get(
            PydanticObjectId(document_id)
        )

    async def get_by_user_id(
        self,
        user_id: PydanticObjectId,
    ):
        return await DocumentModel.find(
            DocumentModel.user_id == user_id
        ).sort(-DocumentModel.created_at).to_list()

    async def update_status(
        self,
        document: DocumentModel,
        status: DocumentStatus,
    ):

        document.status = status

        await document.save()

        return document

    async def update(
        self,
        document: DocumentModel,
    ):

        await document.save()

        return document

    async def delete(
        self,
        document: DocumentModel,
    ):

        await document.delete()
    
    async def update(
        self,
        document: DocumentModel,
    ) -> DocumentModel:
        await document.save()
        return document



document_repository = DocumentRepository()