from google import genai

from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
)


class EmbeddingService:
    MODEL = "gemini-embedding-001"

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        response = client.models.embed_content(
            model=self.MODEL,
            contents=text,
        )

        return response.embeddings[0].values

    def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 100,
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts in a single request, chunked into batches.
        """
        from google.genai import errors
        import time
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.models.embed_content(
                        model=self.MODEL,
                        contents=batch,
                    )
                    all_embeddings.extend([
                        embedding.values
                        for embedding in response.embeddings
                    ])
                    break
                except errors.APIError as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(1)
            
            # Sleep slightly to avoid hitting aggressive rate limits on the free tier
            time.sleep(1)

        return all_embeddings


embedding_service = EmbeddingService()