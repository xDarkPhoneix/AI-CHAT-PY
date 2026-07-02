import hashlib


def build_chat_cache_key(
    user_id: str,
    document_id: str,
    question: str,
) -> str:

    question_hash = hashlib.sha256(
        question.strip().lower().encode()
    ).hexdigest()

    return (
        f"chat:{user_id}:{document_id}:{question_hash}"
    )