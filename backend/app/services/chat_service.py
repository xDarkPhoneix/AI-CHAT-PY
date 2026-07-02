from google import genai

from app.core.config import settings
from app.repositories.vector_repository import vector_repository
from app.services.embedding_service import embedding_service
from app.services.redis_service import redis_service
from app.utils.cache import build_chat_cache_key


class ChatService:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = "gemini-2.5-flash"

    async def ask(
        self,
        user_id: str,
        document_id: str,
        question: str,
    ) -> str:

        query_embedding = embedding_service.embed(question)

        cache_key = build_chat_cache_key(
           str(user_id),
            document_id,
            question,
     )

        cached = redis_service.get(cache_key)

        if cached:
             return cached

        chunks = await vector_repository.search(
            document_id=document_id,
            embedding=query_embedding,
        )

        if not chunks:
            return (
                "I couldn't find any relevant information "
                "in the uploaded document."
            )

        good_chunks = [
            chunk
            for chunk in chunks
            if chunk["score"] >= 0.75
        ]

        if not good_chunks:
            return (
                "I couldn't find any relevant information "
                "in the uploaded document."
            )

        context = self.build_context(good_chunks)

        prompt = self.build_prompt(
            context=context,
            question=question,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        redis_service.set(
        cache_key,
        response.text,
        expire=3600,
        )

        return response.text

    def build_context(
        self,
        chunks: list[dict],
    ) -> str:

        return "\n\n".join(
            chunk["content"]
            for chunk in chunks
        )

    def build_prompt(
        self,
        context: str,
        question: str,
    ) -> str:

        return f"""
You are an AI assistant specialized in answering questions from uploaded PDF documents.

Instructions:
- Answer ONLY using the provided context.
- If the answer cannot be answered from the context, reply:
  "I couldn't find the answer in the uploaded document."
- Do not use outside knowledge.
- Keep your answer concise and accurate.

Context:
{context}

Question:
{question}

Answer:
"""


chat_service = ChatService()