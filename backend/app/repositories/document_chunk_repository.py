from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    async def insert_many(
        self,
        chunks: list[DocumentChunk],
    ):
        await DocumentChunk.insert_many(chunks)


document_chunk_repository = DocumentChunkRepository()