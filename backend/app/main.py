from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger
from app.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
)
from app.database.redis import (
    connect_to_redis,
    close_redis,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    await connect_to_mongodb()
    await connect_to_redis()

    yield

    await close_mongodb_connection()
    await close_redis()

    logger.info("Application stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "PDF Chat AI API"
    }