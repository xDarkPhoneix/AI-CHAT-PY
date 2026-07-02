from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


client = AsyncIOMotorClient(
    settings.MONGODB_URL,
)

database = client[
    settings.DATABASE_NAME
]


class VectorRepository:

    async def search(
        self,
        document_id: str,
        embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": limit,
                    "filter": {
                        "document_id": ObjectId(document_id),
                    },
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "content": 1,
                    "score": {
                        "$meta": "vectorSearchScore",
                    },
                }
            },
        ]

        cursor = database.document_chunks.aggregate(
            pipeline
        )

        return await cursor.to_list(length=limit)


vector_repository = VectorRepository()