from fastapi import APIRouter, Depends
from app.core.rate_limiter import rate_limiter
from app.auth.dependencies import get_current_user
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.chat_service import chat_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    payload: ChatRequest,
    current_user=Depends(get_current_user),
):
    
    rate_limiter.check(
        key=f"chat:{current_user.id}",
        limit=30,
        window=60,
    )

    answer = await chat_service.ask(
        user_id=str(current_user.id),
        document_id=payload.document_id,
        question=payload.question,
    )

    return ChatResponse(
        answer=answer,
    )