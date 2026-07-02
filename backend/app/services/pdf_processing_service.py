from pathlib import Path
import logging

import fitz

from langchain_core.documents import Document as LangChainDocument

from app.models.document import DocumentModel, DocumentStatus
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    document_chunk_repository,
)
from app.repositories.document_repository import (
    document_repository,
)
from app.services.chunk_service import chunk_service
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


class PDFProcessingService:

    async def process(
        self,
        document_id: str,
    ) -> None:

        document = await document_repository.get_by_id(document_id)

        if document is None:
            logger.error("Document %s not found.", document_id)
            return

        try:
            await self.mark_processing(document)

            pages = self.extract_pages(document)

            chunks = self.create_chunks(pages)

            await self.store_chunks(
                document=document,
                chunks=chunks,
            )

            document.pages = len(pages)

            self.delete_pdf(document.file_path)

            await self.mark_completed(document)

            logger.info(
                "Successfully processed '%s'.",
                document.original_filename,
            )

        except Exception:

            logger.exception(
                "Failed processing document %s",
                document_id,
            )

            document.status = DocumentStatus.FAILED

            await document_repository.update(document)

    async def mark_processing(
        self,
        document: DocumentModel,
    ):

        document.status = DocumentStatus.PROCESSING

        await document_repository.update(document)

    async def mark_completed(
        self,
        document: DocumentModel,
    ):

        document.status = DocumentStatus.COMPLETED

        document.file_path = ""

        await document_repository.update(document)

    def extract_pages(
        self,
        document: DocumentModel,
    ) -> list[LangChainDocument]:

        documents = []

        with fitz.open(document.file_path) as pdf:

            for page_number, page in enumerate(pdf):

                text = page.get_text().strip()

                if not text:
                    continue

                documents.append(
                    LangChainDocument(
                        page_content=text,
                        metadata={
                            "page": page_number + 1,
                        },
                    )
                )

        logger.info(
            "Extracted %d pages",
            len(documents),
        )

        return documents

    def create_chunks(
        self,
        pages: list[LangChainDocument],
    ) -> list[LangChainDocument]:

        chunks = chunk_service.create_documents(
            pages
        )

        logger.info(
            "Generated %d chunks",
            len(chunks),
        )

        return chunks

    async def store_chunks(
        self,
        document: DocumentModel,
        chunks: list[LangChainDocument],
    ):

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = embedding_service.embed_batch(
            texts
        )

        chunk_documents = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            chunk_documents.append(
                DocumentChunk(
                    document_id=document.id,
                    user_id=document.user_id,
                    chunk_index=index,
                    content=chunk.page_content,
                    page_number=chunk.metadata["page"],
                    embedding=embedding,
                )
            )

        await document_chunk_repository.insert_many(
            chunk_documents
        )

    def delete_pdf(
        self,
        file_path: str,
    ):

        Path(file_path).unlink(
            missing_ok=True,
        )


pdf_processing_service = PDFProcessingService()