from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def create_documents(
        self,
        pages: list[Document],
    ) -> list[Document]:

        return self.text_splitter.split_documents(
            pages
        )


chunk_service = ChunkService()